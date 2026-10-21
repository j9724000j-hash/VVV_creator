#!/usr/bin/env python3
"""
THE NEXT YES — edit build (Atelier)
===================================
Turns the raw narration stems into a locked, frame-accurate edit decision list
and emits every timing artefact the Remotion composition consumes.

  public/vo/NN.wav        trimmed, de-clicked, level-matched narration
  public/props.json       timeline · captions · graphics cues · audio bed
  public/grain/grain-*.png   film-grain tiles
  ../FF_Vid/subtitles/THE_NEXT_YES.srt   delivery subtitles
  ../FF_Vid/edit/timing-report.md        human-readable EDL

Design note: every duration is DERIVED from the measured narration, never the
other way round — the script's 38–40 s grid could not hold 94 words *and* the
pauses it asks for (see timing-report.md).
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
PUB = ROOT / "public"
VO_IN = PUB / "vo"
VO_OUT = VO_IN
FF = "/home/user/.local/bin/ffmpeg"
FP = "/home/user/.local/bin/ffprobe"
FPS = 30
W, H = 1080, 1920

# ------------------------------------------------------------------ narration
# Unicode contractions are fine; the mix only needs clean phrasing.
VO_TEXT = {
    1: "At 52, she wasn't afraid of being alone.",
    2: "She was afraid of choosing wrong again.",
    3: "After a painful relationship, even a kind invitation felt risky.",
    4: "When someone asked her to dinner, she nearly said no.",
    5: "Not because she didn't want love, but because she remembered the cost.",
    6: "Then she asked herself.",
    7: "What if protecting my heart means never giving it a chance?",
    8: "She didn't promise herself a happy ending. She said yes, to one coffee.",
    9: "Because starting over doesn't mean trusting everyone.",
    10: "It means learning from the past, without letting it choose your future.",
}

# Captions are authored as explicit LINES (never auto-wrapped): a word that
# arrives must not reflow the line above it. [brackets] = emphasis.
CAPTIONS: dict[int, list[list[str]]] = {
    1: [["At 52,"], ["she wasn't afraid"], ["of being alone."]],
    2: [["She was afraid"], ["of [choosing wrong again]."]],
    3: [["After a painful relationship,"], ["even a kind invitation"], ["felt risky."]],
    4: [["When someone asked her to dinner,"], ["she nearly said no."]],
    5: [["Not because she didn't want love,"], ["but because she remembered"], ["[the cost]."]],
    6: [["Then she asked herself:"]],
    7: [["\u201cWhat if protecting my heart"], ["means never giving it a chance?\u201d"]],
    8: [["She didn't promise herself"], ["a happy ending."], ["She said yes to [one coffee]."]],
    9: [["Because starting over"], ["doesn't mean trusting everyone."]],
    10: [["It means learning from the past,"], ["without letting it choose"], ["[your future]."]],
}

# scene → (video file, source start s, narration keys, pre-roll, mid-gap, tail)
# paddings are silence, in seconds, and are the *drama*, not slack.
SCENE_PLAN = [
    dict(idx=1, src="s1.mp4", src_start=0.30, vo=[1], pre=0.30, mid=0.0, post=0.25,
         label="THE HOOK", cut="fade"),
    dict(idx=2, src="s2.mp4", src_start=1.20, vo=[2], pre=0.15, mid=0.0, post=0.30,
         label="THE REAL FEAR", cut="hard"),
    dict(idx=3, src="s3.mp4", src_start=0.60, vo=[3], pre=0.15, mid=0.0, post=0.40,
         label="THE INVITATION", cut="hard"),
    dict(idx=4, src="s4.mp4", src_start=1.00, vo=[4], pre=0.12, mid=0.0, post=0.85,
         label="THE HESITATION", cut="hard"),
    dict(idx=5, src="s5.mp4", src_start=1.00, vo=[5], pre=0.12, mid=0.0, post=0.35,
         label="WHY SHE ALMOST SAID NO", cut="hard"),
    dict(idx=6, src="s6.mp4", src_start=0.50, vo=[6, 7], pre=0.20, mid=0.50, post=0.70,
         label="THE TURNING POINT", cut="hard"),
    dict(idx=7, src="s7.mp4", src_start=0.80, vo=[8], pre=0.18, mid=0.0, post=0.35,
         label="ONE SMALL YES", cut="dissolve"),
    dict(idx=8, src="s8.mp4", src_start=0.00, vo=[9, 10], pre=0.20, mid=0.25, post=2.60,
         label="THE TAKEAWAY", cut="dissolve", rate=1.00),
]


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def probe_dur(p: Path) -> float:
    return float(run([FP, "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", str(p)]).strip())


def speech_bounds(p: Path) -> tuple[float, float]:
    """(start, end) of actual speech via silencedetect."""
    out = subprocess.run(
        [FF, "-hide_banner", "-nostats", "-i", str(p), "-af",
         "silencedetect=noise=-40dB:d=0.10", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    ends = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", out)]
    starts = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", out)]
    dur = probe_dur(p)
    return (ends[0] if ends else 0.0), (starts[-1] if starts else dur)


def prep_vo() -> dict[int, float]:
    """Trim edges, high-pass, gentle compression, match loudness. Returns durations."""
    durations: dict[int, float] = {}
    for i in sorted(VO_TEXT):
        src = VO_IN / f"{i:02d}.mp3"
        dst = VO_OUT / f"{i:02d}.wav"
        if not src.exists() and dst.exists():   # idempotent re-run
            durations[i] = round(probe_dur(dst), 4)
            print(f"  VO{i:02d}  (kept) {durations[i]:5.2f}s")
            continue
        s, e = speech_bounds(src)
        start = max(0.0, s - 0.06)
        end = min(probe_dur(src), e + 0.14)
        run([FF, "-y", "-v", "error", "-i", str(src),
             "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
             "-af", ("highpass=f=90,"
                     "equalizer=f=220:t=q:w=1.2:g=-1.2,"
                     "equalizer=f=3200:t=q:w=1.4:g=0.8,"
                     "acompressor=threshold=-20dB:ratio=2.2:attack=8:release=140:makeup=1.2,"
                     "loudnorm=I=-18:TP=-2.5:LRA=9"),
             "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(dst)])
        durations[i] = round(probe_dur(dst), 4)
        src.unlink()  # keep the public dir lean; the wav is canonical now
        print(f"  VO{i:02d}  speech {s:5.2f}–{e:5.2f}  →  {durations[i]:5.2f}s")
    return durations


# ------------------------------------------------------------------- captions
VOWELS = "aeiouy"


def syllables(word: str) -> int:
    w = re.sub(r"[^a-z']", "", word.lower())
    if not w:
        return 1
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee")):
        n -= 1
    return max(1, n)


def parse_phrase(phrase: str) -> tuple[list[str], list[bool]]:
    words, emph, inside = [], [], False
    for tok in phrase.split():
        a, b = tok.count("["), tok.count("]")
        e = inside or a > 0
        clean = tok.replace("[", "").replace("]", "")
        words.append(clean)
        emph.append(e)
        if b:
            inside = False
        if a:
            inside = True
    return words, emph


def build_cues(vo_start: dict[int, float], vo_dur: dict[int, float]) -> list[dict]:
    """One cue per authored line; per-word windows inside it, syllable-weighted."""
    cues: list[dict] = []
    for key, lines in CAPTIONS.items():
        total_syl = sum(syllables(w) for ln in lines for w in parse_phrase(" ".join(ln))[0])
        speech = vo_dur[key] - 0.10
        cursor = vo_start[key] + 0.05
        for li, line in enumerate(lines):
            words, emph = parse_phrase(" ".join(line))
            syl = sum(syllables(w) for w in words)
            span = speech * syl / total_syl
            wcursor = cursor
            wlist = []
            for w, e in zip(words, emph):
                ws = span * syllables(w) / syl
                wlist.append({"t": w, "from": round(wcursor, 3),
                              "to": round(wcursor + ws, 3), "e": e})
                wcursor += ws
            cues.append({
                "key": f"{key}-{li}",
                "vo": key,
                "text": " ".join(words),
                "from": round(cursor, 3),
                "to": round(cursor + span, 3),
                "words": wlist,
                "emphasis": any(emph),
            })
            cursor += span
    return cues


# -------------------------------------------------------------------- timeline
def main() -> None:
    print("=" * 68)
    print("THE NEXT YES — edit build")
    print("=" * 68)
    print("narration:")
    vo_dur = prep_vo()

    scenes, vo_entries, cues = [], [], []
    t = 0.0
    vo_start: dict[int, float] = {}
    for plan in SCENE_PLAN:
        s_from = t
        cursor = s_from + plan["pre"]
        for j, key in enumerate(plan["vo"]):
            if j:
                cursor += plan["mid"]
            vo_start[key] = cursor
            vo_entries.append({
                "file": f"vo/{key:02d}.wav",
                "start": round(cursor, 3),
                "dur": vo_dur[key],
            })
            cursor += vo_dur[key]
        s_to = cursor + plan["post"]
        rate = plan.get("rate", 1.0)
        need = (s_to - s_from) * rate  # source seconds consumed
        scenes.append({
            "idx": plan["idx"],
            "clipDur": 8.0,
            "label": plan["label"],
            "src": f"scenes/{plan['src']}",
            "from": round(s_from, 3),
            "to": round(s_to, 3),
            "srcStart": plan["src_start"],
            "rate": rate,
            "srcNeed": round(need, 3),
            "cut": plan["cut"],
        })
        t = s_to

    cues = build_cues(vo_start, vo_dur)
    total = round(t, 3)

    # dissolve tails: the outgoing scene keeps running under the incoming fade
    for i, sc in enumerate(scenes):
        sc["extend"] = 0.40 if (i + 1 < len(scenes) and scenes[i + 1]["cut"] == "dissolve") else 0.0
        consumed = sc["srcNeed"] + sc["extend"] * sc["rate"]
        sc["srcEnd"] = round(sc["srcStart"] + min(consumed, sc["clipDur"]), 3)
        spare = (sc["clipDur"] - sc["srcStart"]) / sc["rate"]
        dur = sc["to"] - sc["from"]
        sc["stillFrom"] = round(spare, 3) if spare < dur - 0.02 else None
        if sc["stillFrom"]:
            sc["stillSrc"] = f"scenes/s{sc['idx']}_last.png"

    # conform: trim + 1080x1920/30p, so the composition never scales or re-times
    conform(scenes)

    # last-frame stills for shots that outlast their source
    for sc in scenes:
        if sc.get("stillFrom"):
            subprocess.run([FF, "-y", "-v", "error", "-sseof", "-0.12",
                            "-i", str(PUB / sc["src"]), "-frames:v", "1",
                            "-vf", "scale=720:1280", str(PUB / sc["stillSrc"])], check=True)
            print(f"  still {sc['stillSrc']} @ {sc['stillFrom']:.2f}s")

    # --- graphics cue sheet (all times in scene-local seconds) --------------
    g = {}
    for sc in scenes:
        g[sc["idx"]] = {"from": sc["from"], "to": sc["to"], "local": {}}
    S = {sc["idx"]: sc for sc in scenes}
    total_frames = int(round(total * FPS))

    props = {
        "fps": FPS,
        "width": W,
        "height": H,
        "durationInFrames": total_frames,
        "totalSeconds": total,
        "title": "THE NEXT YES",
        "scenes": scenes,
        "vo": vo_entries,
        "captions": cues,
        "audio": {
            "music": [
                {"file": "audio/music_A.wav", "start": 0.0,
                 "end": round(S[7]["from"] + 0.9, 3), "gain": 0.17,
                 "fadeIn": 2.4, "fadeOut": 2.6},
                {"file": "audio/music_B.wav", "start": round(S[7]["from"] + 0.15, 3),
                 "end": total, "gain": 0.20, "fadeIn": 1.6, "fadeOut": 3.0},
            ],
            "sfx": [
                {"file": "audio/sfx_room.wav", "start": 0.0,
                 "end": round(S[7]["from"] + 0.6, 3), "gain": 0.30, "loop": True,
                 "fadeIn": 0.8, "fadeOut": 1.2},
                {"file": "audio/sfx_air.wav", "start": round(S[6]["from"] - 1.2, 3),
                 "dur": 4.5, "gain": 0.26, "fadeIn": 0.1, "fadeOut": 1.4},
                {"file": "audio/sfx_notification.wav",
                 "start": round(S[3]["from"] + 1.15, 3), "dur": 2.2, "gain": 0.30,
                 "fadeIn": 0.01, "fadeOut": 0.5},
                {"file": "audio/sfx_typing.wav", "start": round(S[6]["to"] - 1.9, 3),
                 "dur": 3.2, "gain": 0.22, "fadeIn": 0.05, "fadeOut": 0.6},
                {"file": "audio/sfx_cafe.wav", "start": round(S[7]["from"], 3),
                 "end": round(S[8]["from"] + 3.4, 3), "gain": 0.20, "loop": True,
                 "fadeIn": 1.2, "fadeOut": 2.4},
                {"file": "audio/sfx_street.wav", "start": round(S[8]["from"] + 0.3, 3),
                 "end": total, "gain": 0.17, "loop": True,
                 "fadeIn": 2.0, "fadeOut": 2.4},
            ],
        },
    }

    PUB.mkdir(parents=True, exist_ok=True)
    (PUB / "props.json").write_text(json.dumps(props, indent=2))
    print(f"\ntimeline locked: {total:.2f}s  ({total_frames} frames @ {FPS}fps)")

    # --- grain tiles -------------------------------------------------------
    make_grain()

    # --- side artefacts ----------------------------------------------------
    out = Path("/home/user/VVV_creator/FF_Vid")
    (out / "subtitles").mkdir(parents=True, exist_ok=True)
    (out / "edit").mkdir(parents=True, exist_ok=True)
    write_srt(out / "subtitles" / "THE_NEXT_YES.srt", cues)
    write_report(out / "edit" / "timing-report.md", scenes, vo_dur, vo_start, total, total_frames)
    print("artefacts: props.json · grain · srt · timing-report")


def conform(scenes: list[dict]) -> None:
    """Editor's conform step: each cut becomes a 1080x1920 / 30 fps, audio-less clip
    that starts at frame 0. Removes every fps / playbackRate ambiguity downstream."""
    out = PUB / "cuts"
    out.mkdir(exist_ok=True)
    for sc in scenes:
        dur = (sc["to"] - sc["from"]) + sc["extend"]        # screen seconds needed
        take = min(dur * sc["rate"], sc["clipDur"] - sc["srcStart"])
        dst = out / f"c{sc['idx']:02d}.mp4"
        run([FF, "-y", "-v", "error",
             "-ss", f"{sc['srcStart']:.3f}", "-t", f"{take:.3f}", "-i", str(PUB / sc["src"]),
             "-vf", ("fps=30,scale=1080:1920:flags=lanczos,"
                     "eq=contrast=1.035:saturation=1.04:brightness=0.004,"
                     "unsharp=5:5:0.30:5:5:0.0,format=yuv420p"),
             "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "15",
             "-profile:v", "high", "-x264-params", "keyint=30:min-keyint=15", str(dst)])
        sc["file"] = f"cuts/c{sc['idx']:02d}.mp4"
        sc["cutFrames"] = int(round(take / sc["rate"] * FPS))
        print(f"  cut {dst.name}  {take/max(sc['rate'],0.001):5.2f}s "
              f"({dst.stat().st_size/1e6:5.2f} MB)")


def make_grain() -> None:
    d = PUB / "grain"
    d.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    for i in range(3):
        h, w = 640, 360
        base = rng.normal(0, 1, (h, w))
        # soften a touch so it reads as emulsion, not digital hash
        k = np.ones((2, 2)) / 4
        base = np.pad(base, 1, mode="wrap")
        sm = sum(base[dy:dy + h, dx:dx + w] * k[dy, dx]
                 for dy in range(2) for dx in range(2))
        v = np.clip(128 + sm * 46, 0, 255).astype(np.uint8)
        rgb = np.stack([v, v, v], axis=2)
        path = d / f"grain-{i}.png"
        write_png(path, rgb)


def write_png(path: Path, rgb: np.ndarray) -> None:
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[y].tobytes() for y in range(h))

    def chunk(tag: bytes, data: bytes) -> bytes:
        import zlib
        return (len(data).to_bytes(4, "big") + tag + data +
                zlib.crc32(tag + data).to_bytes(4, "big"))

    import zlib
    png = (b"\x89PNG\r\n\x1a\n" +
           chunk(b"IHDR", w.to_bytes(4, "big") + h.to_bytes(4, "big") +
                 bytes([8, 2, 0, 0, 0])) +
           chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    path.write_bytes(png)


def ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(path: Path, cues: list[dict]) -> None:
    lines = []
    for i, c in enumerate(cues, 1):
        lines.append(f"{i}\n{ts(c['from'])} --> {ts(c['to'])}\n{c['text']}\n")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_report(path: Path, scenes, vo_dur, vo_start, total, frames) -> None:
    rows = []
    for sc in scenes:
        rows.append(f"| {sc['idx']} | {sc['label']} | {sc['from']:6.2f} – {sc['to']:6.2f} | "
                    f"{sc['to'] - sc['from']:5.2f}s | {sc['src'].split('/')[-1]} @ {sc['srcStart']:.2f}s "
                    f"×{sc['rate']:.2f} | {sc['cut']} |")
    vo_rows = [f"| {k:02d} | {vo_start[k]:6.2f} | {vo_dur[k]:5.2f} | {VO_TEXT[k]} |"
               for k in sorted(vo_dur)]
    words = sum(len(v.replace('-', ' ').split()) for v in VO_TEXT.values())
    path.write_text(f"""# THE NEXT YES — locked timing report

Generated by `remotion-composer/projects/thenextyes/build_edit.py`.
Every duration below is derived from the measured narration, not from a
pre-set grid. Total runtime **{total:.2f}s / {frames} frames @ 30 fps**.

## Why {total:.1f} s and not 38–40 s

The source script schedules 8 scenes on a 40.0 s grid *and* asks for pauses
(before and after the turning-point question, a hesitation hold, and 1.5–2 s of
on-screen question after the last word). Its 94 words alone run 37.3 s of
measured speech here — at the script's own 141 wpm that is 40.0 s of pure
speech, i.e. zero room for the pauses it demands. Cutting words would have
removed the pauses that carry the story, so the pauses were protected and the
runtime moved. **{total:.1f}s** is the honest number for this script.

## Scene sheet

| # | Beat | In – Out | Dur | Source | Cut |
|---|------|----------|-----|--------|-----|
{chr(10).join(rows)}

## Narration map

| VO | starts | dur | line |
|----|--------|-----|------|
{chr(10).join(vo_rows)}

Narration: {words} words · {sum(vo_dur.values()):.2f}s of speech · {sum(vo_dur.values())/total*100:.1f}% of runtime.
Silence (the pauses + margins) = {total - sum(vo_dur.values()):.2f}s.

## Source-footage budget

Every scene clip is 8.00 s @ 720×1280. Total available 64.0 s; used
{sum((s['to']-s['from'])*s['rate'] for s in scenes):.2f} s. Scene 8 is the only
beat longer than its clip (10.8 s on an 8.0 s shot), so its camera is already at
rest by 8.0 s and the **last frame is held** under the closing question — no
freeze mid-stride, no looping walk.
""", encoding="utf-8")


if __name__ == "__main__":
    main()
