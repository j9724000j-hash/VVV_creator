#!/usr/bin/env python3
"""
THE NEXT YES — audio build (Atelier / Remotion pipeline)
========================================================
Generates every non-voice stem from scratch with numpy so the piece carries no
licensing risk:

  audio/music_A.wav   sparse, reflective piano        (a minor, 60 BPM)
  audio/music_B.wav   warm piano + pad + melody       (café / resolution)
  audio/sfx_room.wav  apartment room tone
  audio/sfx_notif.wav phone notification chime
  audio/sfx_cafe.wav  café murmur + cup clinks
  audio/sfx_street.wav late-morning street air
  audio/sfx_air.wav   sub-audible rising air swell (turning point)
  audio/sfx_typing.wav four soft key taps

Run:  .venv/bin/python projects/thenextyes/audio_build.py
"""
from __future__ import annotations

import math
import os
import wave
from pathlib import Path

import numpy as np

SR = 48000
OUT = Path(__file__).resolve().parent / "public" / "audio"
OUT.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(20261021)


# ----------------------------------------------------------------------------- io
def write_wav(path: Path, stereo: np.ndarray) -> None:
    data = np.clip(stereo, -1.0, 1.0)
    pcm = (data * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())
    print(f"  {path.name:22s} {len(stereo)/SR:6.2f}s  {path.stat().st_size/1e6:5.2f} MB")


def t_axis(seconds: float) -> np.ndarray:
    return np.arange(int(round(seconds * SR))) / SR


def midi(n: float) -> float:
    return 440.0 * 2.0 ** ((n - 69.0) / 12.0)


NOTE = {n: i for i, n in enumerate(
    ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def n(name: str) -> float:
    """'A4' -> midi number."""
    i = 1 if len(name) == 2 else 2
    return 12 * (int(name[i:]) + 1) + NOTE[name[:i]]


# ------------------------------------------------------------------------- dsp
def one_pole_lp(x: np.ndarray, cutoff: float) -> np.ndarray:
    a = math.exp(-2.0 * math.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def lp_fast(x: np.ndarray, cutoff: float) -> np.ndarray:
    """Vectorised one-pole low-pass via recursive filter (scipy-free)."""
    from numpy.lib.stride_tricks import sliding_window_view  # noqa: F401
    # FFT-based brickwall-ish shelf: gentle, no ringing for our noise beds.
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    H = 1.0 / np.sqrt(1.0 + (f / max(cutoff, 20.0)) ** 2)
    return np.fft.irfft(X * H, n=len(x))


def hp_fast(x: np.ndarray, cutoff: float) -> np.ndarray:
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    H = 1.0 - 1.0 / np.sqrt(1.0 + (f / max(cutoff, 20.0)) ** 2)
    return np.fft.irfft(X * H, n=len(x))


def band_fast(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return hp_fast(lp_fast(x, hi), lo)


def make_ir(seconds: float = 2.6, predelay: float = 0.022, bright: float = 3200.0):
    """Synthetic stereo hall IR: decorrelated decaying noise, darker tail."""
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = np.zeros((n, 2))
    for ch in range(2):
        noise = RNG.standard_normal(n)
        env = np.exp(-t / 0.62)
        tail = lp_fast(noise, bright) * env
        tail /= np.max(np.abs(tail)) + 1e-12
        ir[:, ch] = tail
    pre = int(predelay * SR)
    ir = np.vstack([np.zeros((pre, 2)), ir])
    ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))[:, None]
    return ir


IR = make_ir()


def reverb(x: np.ndarray, wet: float = 0.28, ir: np.ndarray = IR) -> np.ndarray:
    """x: (n,2). FFT convolution with our synthetic IR."""
    n = len(x) + len(ir) - 1
    size = 1 << (n - 1).bit_length()
    out = np.zeros((len(x), 2))
    for ch in range(2):
        X = np.fft.rfft(x[:, ch], size)
        H = np.fft.rfft(ir[:, ch], size)
        y = np.fft.irfft(X * H, size)[: len(x)]
        out[:, ch] = y
    peak = np.max(np.abs(out)) + 1e-12
    out /= peak
    dry_peak = np.max(np.abs(x)) + 1e-12
    return ((1 - wet) * x / dry_peak + wet * out) * dry_peak


# ---------------------------------------------------------------------- piano
def piano_note(freq: float, dur: float, vel: float = 1.0, pan: float = 0.0) -> np.ndarray:
    """Additive 'felt piano': inharmonic partials, per-partial decay, hammer noise."""
    length = int((dur + 0.55) * SR)
    t = np.arange(length) / SR
    out = np.zeros(length)
    B = 0.00035
    partials = 14
    for k in range(1, partials + 1):
        fk = freq * k * math.sqrt(1.0 + B * k * k)
        if fk > 15500:
            break
        decay = 1.05 + 0.62 * k + 0.05 * k * k
        amp = (1.0 / k ** 1.62) * (0.86 + 0.14 * RNG.random())
        if k == 1:
            amp *= 1.28
        env = np.exp(-t * decay)
        out += amp * env * np.sin(2 * math.pi * fk * t + RNG.random() * 0.4)
    # felt hammer: short filtered noise burst
    nh = int(0.028 * SR)
    th = np.arange(nh) / SR
    hammer = lp_fast(RNG.standard_normal(nh), 2600) * np.exp(-th / 0.008) * 0.055
    out[:nh] += hammer
    # body / soundboard thump
    out[: int(0.09 * SR)] += 0.04 * np.sin(2 * math.pi * freq * 0.5 * np.arange(int(0.09 * SR)) / SR)
    # attack shaping + release taper
    at = int(0.0035 * SR)
    out[:at] *= np.linspace(0, 1, at) ** 1.5
    rel = int(min(0.35, dur) * SR)
    out[-rel:] *= np.linspace(1, 0, rel) ** 2
    out *= vel * 0.5
    # constant-power pan
    p = (pan + 1) * math.pi / 4
    return np.stack([out * math.cos(p), out * math.sin(p)], axis=1)


def pad_chord(freqs, dur, vel=1.0, pan=0.0):
    length = int((dur + 1.2) * SR)
    t = np.arange(length) / SR
    out = np.zeros(length)
    for f in freqs:
        for det in (-0.0018, 0.0018):
            vib = 1.0 + 0.0015 * np.sin(2 * math.pi * 0.13 * t + RNG.random() * 6)
            out += np.sin(2 * math.pi * f * (1 + det) * vib * t) / len(freqs)
    # slow swell
    a = int(1.1 * SR)
    env = np.ones(length)
    env[:a] = (np.linspace(0, 1, a) ** 2)
    r = int(0.9 * SR)
    env[-r:] *= np.linspace(1, 0, r) ** 2.2
    out *= env * vel * 0.16
    out = lp_fast(out, 1500)
    p = (pan + 1) * math.pi / 4
    return np.stack([out * math.cos(p), out * math.sin(p)], axis=1)


def add(buf: np.ndarray, sig: np.ndarray, at_sec: float) -> None:
    i = int(round(at_sec * SR))
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


# ---------------------------------------------------------------- music: A section
def build_music_a() -> np.ndarray:
    """8 bars @60 BPM = 32 s. Sparse, reflective, a-minor."""
    bar = 4.0
    total = 34.5
    buf = np.zeros((int(total * SR), 2))
    # bars: root, chord tones (left hand), melody (right hand)
    prog = [
        ("A2", ["A3", "E4", "C5"], [(0.0, "E5", 0.85), (2.5, "C5", 0.6)]),
        ("F2", ["F3", "C4", "A4"], [(0.0, "A4", 0.72), (2.0, "C5", 0.55)]),
        ("C3", ["C4", "G4", "E5"], [(0.0, "G4", 0.7), (2.5, "E5", 0.6)]),
        ("G2", ["G3", "D4", "B4"], [(0.0, "D5", 0.75)]),
        ("A2", ["A3", "E4", "C5"], [(0.5, "E5", 0.8), (2.5, "A5", 0.55)]),
        ("F2", ["F3", "C4", "A4"], [(0.0, "F5", 0.7), (2.0, "C5", 0.5)]),
        ("C3", ["C4", "G4", "E5"], [(0.0, "E5", 0.72), (2.5, "G5", 0.55)]),
        ("G2", ["G3", "D4", "B4"], [(0.0, "D5", 0.7)]),
    ]
    for b, (root, tones, mel) in enumerate(prog):
        t0 = b * bar
        add(buf, piano_note(midi(n(root)), 3.6, 0.85, pan=-0.28), t0)
        add(buf, piano_note(midi(n(tones[1])), 3.0, 0.42, pan=-0.1), t0 + 0.02)
        add(buf, piano_note(midi(n(tones[2])), 2.6, 0.34, pan=0.12), t0 + 0.03)
        # soft arpeggio shimmer high up
        arp = [tones[2], tones[1], tones[0]]
        for k, a in enumerate(arp):
            add(buf, piano_note(midi(n(a)) * 2, 1.8, 0.11, pan=0.3 - 0.15 * k), t0 + 1.0 + k * 0.5)
        for dt, name, vel in mel:
            add(buf, piano_note(midi(n(name)), 3.2, vel * 0.62, pan=0.16), t0 + dt)
    # final tonic, long
    add(buf, piano_note(midi(n("A2")), 4.0, 0.7, pan=-0.2), 32.0)
    add(buf, piano_note(midi(n("E5")), 3.6, 0.4, pan=0.15), 32.05)
    out = reverb(buf, wet=0.3)
    out = master(out, fade_in=2.2, fade_out=1.8)
    return out


# ---------------------------------------------------------------- music: B section
def build_music_b() -> np.ndarray:
    """6 bars @60 BPM = 24 s. Warmer: pad + singing melody, resolves on C."""
    bar = 4.0
    total = 26.5
    buf = np.zeros((int(total * SR), 2))
    prog = [
        ("F2", ["F3", "C4", "A4"], [(0.0, "A5", 0.6), (1.5, "G5", 0.5), (2.5, "E5", 0.5)]),
        ("C3", ["C4", "G4", "E5"], [(0.0, "G5", 0.6), (2.0, "E5", 0.5)]),
        ("G2", ["G3", "D4", "B4"], [(0.0, "D5", 0.55), (2.5, "B4", 0.45)]),
        ("A2", ["A3", "E4", "C5"], [(0.0, "C5", 0.55), (2.0, "E5", 0.5)]),
        ("F2", ["F3", "C4", "A4"], [(0.0, "F5", 0.55), (2.5, "A5", 0.5)]),
        ("C3", ["C4", "G4", "E5"], [(0.0, "G5", 0.5), (2.0, "E5", 0.4)]),
    ]
    for b, (root, tones, mel) in enumerate(prog):
        t0 = b * bar
        add(buf, piano_note(midi(n(root)), 3.7, 0.8, pan=-0.26), t0)
        add(buf, piano_note(midi(n(tones[1])), 3.2, 0.45, pan=-0.08), t0 + 0.02)
        add(buf, piano_note(midi(n(tones[2])), 2.8, 0.38, pan=0.14), t0 + 0.03)
        add(buf, pad_chord([midi(n(tones[0])), midi(n(tones[1])), midi(n(tones[2]))], bar + 0.6, 0.9), t0)
        for k, a in enumerate([tones[0], tones[1], tones[2]]):
            add(buf, piano_note(midi(n(a)) * 2, 1.7, 0.1, pan=0.35 - 0.2 * k), t0 + 1.2 + k * 0.5)
        for dt, name, vel in mel:
            add(buf, piano_note(midi(n(name)), 3.0, vel, pan=0.18), t0 + dt)
    # closing colour: C(add9) held
    for i, name in enumerate(["C3", "G3", "E4", "D5"]):
        add(buf, piano_note(midi(n(name)), 4.2, 0.5 - i * 0.06, pan=-0.2 + i * 0.13), 24.0 + i * 0.035)
    add(buf, pad_chord([midi(n("C3")), midi(n("G3")), midi(n("E4")), midi(n("D5"))], 3.4, 0.85), 24.0)
    out = reverb(buf, wet=0.34)
    out = master(out, fade_in=1.6, fade_out=2.6)
    return out


def master(x: np.ndarray, fade_in: float, fade_out: float) -> np.ndarray:
    x = x - x.mean(axis=0, keepdims=True)
    peak = np.max(np.abs(x)) + 1e-12
    x = x / peak * 0.72
    n = len(x)
    fi = min(int(fade_in * SR), n)
    fo = min(int(fade_out * SR), n)
    x[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.4
    x[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.3
    return x


# ------------------------------------------------------------------------- sfx
def sfx_room(seconds=14.0) -> np.ndarray:
    n = int(seconds * SR)
    base = RNG.standard_normal(n)
    out = lp_fast(base, 340) * 0.5 + hp_fast(base, 60) * 0.06
    # slow breathing of the room
    t = np.arange(n) / SR
    out *= 0.85 + 0.15 * np.sin(2 * math.pi * 0.07 * t)
    out = np.stack([out, np.roll(out, 911)], axis=1) * 0.035
    # loop-safe crossfade
    k = int(1.0 * SR)
    out[:k] = out[:k] * np.linspace(0, 1, k)[:, None] ** 0.5 + out[-k:] * np.linspace(1, 0, k)[:, None] ** 0.5
    return out


def sfx_notification() -> np.ndarray:
    total = 2.2
    buf = np.zeros((int(total * SR), 2))
    for dt, f, v in [(0.0, midi(n("E6")), 0.5), (0.13, midi(n("A6")), 0.42)]:
        length = int(1.7 * SR)
        t = np.arange(length) / SR
        tone = (np.sin(2 * math.pi * f * t) + 0.32 * np.sin(2 * math.pi * f * 2.01 * t)
                + 0.12 * np.sin(2 * math.pi * f * 3.02 * t))
        tone *= np.exp(-t / 0.30) * (1 - np.exp(-t / 0.004))
        sig = np.stack([tone, tone * 0.96], axis=1) * v * 0.5
        add(buf, sig, dt)
    return reverb(buf, wet=0.22)


def sfx_cafe(seconds=26.0) -> np.ndarray:
    n = int(seconds * SR)
    murmur = RNG.standard_normal(n)
    # speech-like amplitude modulation + formant-ish bands
    t = np.arange(n) / SR
    mod = (0.55 + 0.45 * np.abs(np.sin(2 * math.pi * 0.9 * t + 1.1) *
                                np.sin(2 * math.pi * 0.27 * t))) ** 2
    murmur = band_fast(murmur, 180, 2400) * mod
    air = band_fast(RNG.standard_normal(n), 3000, 9000) * 0.05
    left = murmur * 0.9 + air
    right = np.roll(murmur, 1300) * 0.9 + air
    buf = np.stack([left, right], axis=1)
    # cup / saucer clinks
    for at, f0, v in [(3.4, 2100, 0.20), (8.1, 1750, 0.14), (13.9, 2350, 0.17), (19.4, 1900, 0.12)]:
        length = int(0.9 * SR)
        tt = np.arange(length) / SR
        clink = (np.sin(2 * math.pi * f0 * tt) + 0.5 * np.sin(2 * math.pi * f0 * 2.7 * tt)
                 + 0.3 * np.sin(2 * math.pi * f0 * 4.3 * tt)) * np.exp(-tt / 0.09)
        clink *= (1 - np.exp(-tt / 0.001))
        add(buf, np.stack([clink, clink * 0.8], axis=1) * v, at)
    # gentle chair move
    length = int(0.5 * SR)
    tt = np.arange(length) / SR
    scuff = lp_fast(RNG.standard_normal(length), 900) * np.exp(-tt / 0.12) * 0.07
    add(buf, np.stack([scuff, scuff], axis=1), 11.2)
    buf /= np.max(np.abs(buf)) + 1e-12
    return buf * 0.5


def sfx_street(seconds=22.0) -> np.ndarray:
    n = int(seconds * SR)
    base = RNG.standard_normal(n)
    t = np.arange(n) / SR
    air = band_fast(base, 220, 5200)
    air *= 0.7 + 0.3 * np.sin(2 * math.pi * 0.12 * t)
    left = air
    right = np.roll(air, 2400) * 0.95
    buf = np.stack([left, right], axis=1)
    # distant car pass
    for at, v in [(6.0, 0.22), (15.5, 0.16)]:
        length = int(3.4 * SR)
        tt = np.arange(length) / SR
        env = np.exp(-((tt - 1.5) ** 2) / 0.55) * v
        veh = lp_fast(RNG.standard_normal(length), 700) * env
        add(buf, np.stack([veh, np.roll(veh, 700)], axis=1), at)
    buf /= np.max(np.abs(buf)) + 1e-12
    return buf * 0.42


def sfx_air(seconds=4.5) -> np.ndarray:
    n = int(seconds * SR)
    t = np.arange(n) / SR
    base = RNG.standard_normal(n)
    swell = np.exp(-((t - seconds * 0.62) ** 2) / (2 * (seconds * 0.22) ** 2))
    s = band_fast(base, 300, 4200) * swell
    sub = np.sin(2 * math.pi * 55 * t) * swell * 0.35
    s = s + sub
    s /= np.max(np.abs(s)) + 1e-12
    return np.stack([s, np.roll(s, 300)], axis=1) * 0.4


def sfx_typing() -> np.ndarray:
    total = 3.2
    buf = np.zeros((int(total * SR), 2))
    for i, at in enumerate([0.0, 0.34, 0.71, 1.05, 1.36]):
        length = int(0.09 * SR)
        tt = np.arange(length) / SR
        tap = band_fast(RNG.standard_normal(length), 900, 7000) * np.exp(-tt / 0.012)
        tap *= (1 - np.exp(-tt / 0.0012))
        add(buf, np.stack([tap, tap * 0.85], axis=1) * (0.17 - i * 0.012), at)
    return buf


def main() -> None:
    print("=" * 62)
    print("THE NEXT YES — audio build")
    print("=" * 62)
    jobs = [
        ("music_A.wav", build_music_a),
        ("music_B.wav", build_music_b),
        ("sfx_room.wav", sfx_room),
        ("sfx_notification.wav", sfx_notification),
        ("sfx_cafe.wav", sfx_cafe),
        ("sfx_street.wav", sfx_street),
        ("sfx_air.wav", sfx_air),
        ("sfx_typing.wav", sfx_typing),
    ]
    for name, fn in jobs:
        write_wav(OUT / name, fn())
    print("done.")


if __name__ == "__main__":
    main()
