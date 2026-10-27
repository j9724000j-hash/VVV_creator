#!/usr/bin/env python3
"""Build compressed VO + measure caption cue boundaries from actual audio energy."""
import subprocess, numpy as np, json, os, re
FF = os.path.expanduser("~/.local/bin/ffmpeg")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VO = os.path.join(ROOT, "extracted/Voice_Over.wav")
AUD = os.path.join(ROOT, "project/audio")
os.makedirs(AUD, exist_ok=True)

def silences(path, noise="-38dB", d=0.22):
    p = subprocess.run([FF, "-hide_banner", "-nostats", "-i", path,
        "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"],
        capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", p.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", p.stderr)]
    return list(zip(starts, ends))

raw = silences(VO)
gaps = [(s, e, e - s) for s, e in raw if 0.05 < s < 40.2]
print("RAW gaps:", [(round(s,3), round(e,3), round(d,3)) for s,e,d in gaps])

segs, cur = [], 0.299
for s, e, d in gaps:
    if d > 0.60:                       # plan §7.1: only block gaps > 0.6 s are cut
        segs.append((cur, s)); cur = e
segs.append((cur, 40.007))             # last speech sample at 40.007 (trailing silence dropped)
segs = [(a, b) for a, b in segs if b - a > 0.15]
print("SPEECH SEGMENTS (raw):", [(round(a,3), round(b,3)) for a,b in segs])

new_gap = {0: 0.400}  # after hook
HEAD = 0.299            # breathing lead-in before first word
parts, t, boundaries = [], 0.0, []
parts.append(("sil", HEAD)); t += HEAD
for i, (a, b) in enumerate(segs):
    dur = b - a
    parts.append(("seg", a, b))
    boundaries.append([i, round(t,3), round(t + dur,3), a, b])
    t += dur
    if i < len(segs) - 1:
        g = new_gap.get(i, 0.250 if (segs[i+1][0] - b) > 0.60 else (segs[i+1][0] - b))
        parts.append(("sil", g)); t += g
TOTAL = t
print("COMPRESSED TOTAL:", round(TOTAL, 3))

fc, n = "", 0
for p in parts:
    if p[0] == "seg":
        fc += f"[0]atrim={p[1]:.3f}:{p[2]:.3f},asetpts=PTS-STARTPTS[s{n}];"; n += 1
    else:
        fc += f"aevalsrc=0:d={p[1]:.3f}:s=24000[s{n}];"; n += 1
fc += "".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,aresample=48000:resampler=soxr,aformat=sample_fmts=flt:channel_layouts=stereo[out]"
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", VO,
    "-filter_complex", fc, "-map", "[out]", os.path.join(AUD, "VO_assembled.wav")], check=True)

raw_p = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", os.path.join(AUD, "VO_assembled.wav"),
    "-f", "f32le", "-ac", "1", "-ar", "24000", "-"], capture_output=True)
x = np.frombuffer(raw_p.stdout, dtype=np.float32)
hop = 240
m = len(x) // hop
env = np.sqrt((x[:m*hop].reshape(m, hop) ** 2).mean(axis=1))
np.save(os.path.join(AUD, "env.npy"), env)

def dip(span, guess, win=0.9):
    a, b = span
    lo = max(int((guess - win) * 100), int(a * 100) + 3)
    hi = min(int((guess + win) * 100), int(b * 100) - 3)
    if hi <= lo: return guess
    return (lo + int(np.argmin(env[lo:hi]))) / 100.0

fine = silences(os.path.join(AUD, "VO_assembled.wav"), noise="-33dB", d=0.18)
print("ASSEMBLED fine pauses:", [(round(s,2), round(e,2)) for s, e in fine])

# ---------- caption cue derivation (measured) ----------
segs_out = [(b[1], b[3]) for b in boundaries]          # (out_start, raw_start)
def out_of(raw_t):
    for i in range(len(segs_out) - 1, -1, -1):
        out_s, raw_s = segs_out[i]
        if raw_t >= raw_s - 1e-6:
            return out_s + (raw_t - raw_s)
    return segs_out[0][0]

hook   = (boundaries[0][1], boundaries[0][2])
story  = (boundaries[1][1], boundaries[1][2])
stakes = (boundaries[2][1], boundaries[3][2])
lesson = (boundaries[4][1], boundaries[4][2])
q_cta  = (boundaries[5][1], boundaries[5][2])
q_end, cta_start = out_of(38.245), out_of(38.800)

def pause_after(t, idx=0):
    cand = [(s, e) for s, e in fine if s >= t - 0.05]
    return cand[idx] if len(cand) > idx else (t + 0.3, t + 0.5)

p1 = pause_after(hook[0])          # after "Your website works."
p2 = pause_after(p1[1])            # after "…it's safe."
p3 = pause_after(p2[1])            # after "…out of sight."
p4 = pause_after(stakes[0])        # after "…protection."
p5 = pause_after(p4[1])            # after "…perfectly normal"
p7 = pause_after(stakes[1] + 0.4)  # after "…security update."
p8 = pause_after(lesson[1] - 0.1)  # after "…plugins."
p9 = pause_after(q_cta[0])         # after "…for your website—"
p10 = pause_after(p9[1])           # after "…into the story?"

def dipv(a, b, guess, win=1.1):
    lo, hi = int((guess - win) * 100), int((guess + win) * 100)
    lo, hi = max(lo, int(a * 100) + 3), min(hi, int(b * 100) - 3)
    return (lo + int(np.argmin(env[lo:hi]))) / 100.0

PAD = 0.12
cues = [
    ("Your website works.",                          hook[0],         p1[0] + PAD),
    ("That doesn’t mean it’s safe.",                 p1[1],           p2[0] + PAD),
    ("Behind every page,\ncode runs out of sight.",  p2[1],           p3[0] + PAD),
    ("Brain Code’s PHP2Shell article\nexplores what happens", p3[1],  None),
    ("when AI helps uncover security flaws\nhiding in that foundation.", None, story[1] + PAD),
    ("But discovery isn’t protection.",              story[1] + 0.25, p4[0] + PAD),
    ("A website can look perfectly normal",          p4[1],           None),
    ("while the software underneath\nstill needs a security update.", None, stakes[1] + PAD),
    ("The lesson? Check your PHP version—\nnot just your plugins.", stakes[1] + 0.25, p8[0] + PAD),
    ("So what does PHP2Shell\nmean for your website—", lesson[1] + 0.25, p9[0] + PAD),
    ("and where does AI fit into the story?",        p9[1],           p10[0] + PAD),
    ("You’ll find the link in the comments.",        cta_start,       TOTAL + 0.20),
]
c4_end = dipv(p3[1], story[1], p3[1] + (story[1] - p3[1]) * 0.44)
c7_end = dipv(p4[1], stakes[1], p5[0] + 0.25, win=1.3)
cues[3] = (cues[3][0], cues[3][1], c4_end)
cues[4] = (cues[4][0], c4_end, cues[4][2])
cues[6] = (cues[6][0], cues[6][1], c7_end)
cues[7] = (cues[7][0], c7_end, cues[7][2])

print("\nCAPTION CUES (measured):")
for i, (txt, a, b) in enumerate(cues, 1):
    print(f"  c{i:02d}  {a:7.3f} → {b:7.3f}   {txt.splitlines()[0][:44]}")

json.dump({"cues": [{"i": i, "text": t, "start": round(a,3), "end": round(b,3)}
                    for i, (t, a, b) in enumerate(cues, 1)],
           "blocks": {"hook": hook, "story": story, "stakes": stakes, "lesson": lesson,
                      "question": (q_cta[0], q_end), "cta": (cta_start, TOTAL)},
           "total": round(TOTAL,3), "fine_pauses": fine},
          open(os.path.join(AUD, "timeline.json"), "w"), indent=1)
print("\nsaved timeline.json + VO_assembled.wav  | TOTAL =", round(TOTAL, 3))
