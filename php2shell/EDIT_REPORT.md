# EDIT_REPORT v2 — Brain Code PHP2Shell (Re-edit)

**Date:** 2026-10-27 · **Supersedes:** v1 report · **Governing plan:** `BrainCode_PHP2Shell_Editing_Plan.md`

## Why a re-edit (user feedback → fixes)
1. **Captions out of sync (visible ~16–17 s)** → root-caused and fixed: cue boundaries are now
   **measured from the actual rebuilt audio** (silencedetect at −45 dB + 10 ms energy-envelope
   minima), not proportional guesses. The v1 c7/c8 boundary was ~0.25 s early; v2 puts the switch
   exactly in the measured compressed silence **20.478–20.728 s**. All 12 cues verified frame-accurate
   (see `project/renders/caption_sync_proof.jpg` — one frame grabbed at the midpoint of every cue).
2. **Weak ending / resources under-used** → ending redesigned: navy gradient rises *under* the
   spoken line; **Comments_CTA bubble + bouncing Down_Arrow** (previously unused assets) appear
   with "You'll find the link in the comments."; then a 1.4 s branded outro card (BRAIN CODE,
   centered) holds to the end. Total now 40.90 s (was 38.87).
3. **Inconsistent frames** → unified design system: `Tech_Brand_Strip` identity thread top-center
   in scenes 02–06 (+ readability cap under it), Sora kickers only in scene 03, single caption
   zone, dissolves only inside scenes, hard cuts exactly on sentence boundaries.
4. **Music too quiet** → base gain raised **+4.3 dB** (0.335→0.55 ≈ −5.2 dBFS), hook swell +3 dB
   kept, stronger ducking (ratio 8→6, threshold −26.9 dB) so voice stays dominant; music-only tail
   rings ~−27 dB mean through the outro; final fade 38.2→40.3 s.

## Deliverables (in `php2shell/`)
| File | Spec | Result |
|---|---|---|
| `BrainCode_PHP2Shell_Final.mp4` | 1080×1920 · 30 fps · H.264 yuv420p · AAC 48 kHz 256 kbps | ✅ **40.90 s** · 20.3 MB · −14.2 LUFS · peak −1.1 dBTP |
| `BrainCode_PHP2Shell_Captions.srt` | timed to actual voice | ✅ 12 cues, **measured** times |
| `Cover_Frame.png` | hook peak | ✅ frame @3.35 s (IS IT SAFE? + red pulse) |
| `Final_Mix.wav` | mix | ✅ `project/audio/Final_Mix2.wav` (40.90 s) |

## Timeline (measured; VO rebuilt 40.32→40.05 s + 0.299 s lead-in = program 40.90 s)
Only gaps >0.6 s compressed (→0.25 s; hook gap→0.40 s). Voice never stretched. Segments:
0.299–3.598 · 4.274–13.922 · 14.654–21.236 · 21.853–25.702 · 26.382–31.508 · 32.161–40.007 (raw).

| Scene | Video | Caption cue(s) | Design |
|---|---|---|---|
| 01 Hook | 0.000–3.598 | c1, c2 | t01→t02 hard-swap @2.90–3.05 + red pulse @3.25 on "safe"; zoom→106% |
| 02 Title | 3.598–6.880 | c3 | AI bg pan-down w/ 0.25 s dissolve; strip+cap in @0.45 |
| 03 Layers | 6.880–13.896 | c4 (ends @measured dip 10.16), c5 | kicker fade-in; layers rise 0.52→2.42; badge @2.15; scan @3.28 (on "AI") |
| 04 Stakes | 13.896–24.577 | c6, c7 (→20.700), c8 | 04a shield+title+red pulse @15.5 ("protection") · 04b browser drift · 04c layers+amber beat @23.4 |
| 05 Lesson | 24.577–30.203 | c9 | calm grid; badge; title @1.2 |
| 06 Question | 30.203–36.842 | c10 (→34.002), c11 | neural drift over grid |
| 07 CTA+Outro | 36.842–40.900 | c12 | gradient rise; CTA bubble @0.16 + arrow @0.42 (bounce); brand card @1.95 → hold |

## QC v2
- Decode full-pass: 0 errors. Duration 40.90 s (= VO program 40.348 + branded outro tail).
- Loudness −14.2 LUFS / peak −1.1 dBTP (≤ −1 ✓). Music clearly present under voice, ducked,
  fade completes 40.3 s. No black frames (end-frames are the brand navy gradient by design).
- Hook complete <3 s. Captions: 12/12 measured & burned; SRT matches burned cues exactly.
- Identity: strip thread + closing brand card; Sora/Inter only; red ×2, amber ×1.

## Known limitation (unchanged, documented)
The delivered VO recording does not contain the CTA's first sentence ("Read Brain Code's full
PHP2Shell breakdown…"); the edit syncs to the actual voice (master-clock rule). Caption cards
12–13 remain unused; scene 07 timing can absorb the sentence if it is recorded later.
