# EDIT_REPORT — Brain Code PHP2Shell (Final)

**Date:** 2026-10-27 · **Editor:** Arena Agent (ffmpeg pipeline) · **Governing plan:** `BrainCode_PHP2Shell_Editing_Plan.md`

## Deliverables (in `php2shell/`)
| File | Spec | Result |
|---|---|---|
| `BrainCode_PHP2Shell_Final.mp4` | 1080×1920 · 30 fps · H.264 yuv420p · AAC 48 kHz ≥256 kbps | ✅ 38.87 s · 20.4 MB · video ~3.9 Mbps (see note 1) · audio 256 kbps stereo |
| `BrainCode_PHP2Shell_Captions.srt` | timed to actual voice | ✅ 12 cues, video-clock |
| `Cover_Frame.png` | from hook scene | ✅ frame @3.40 s (both hook lines + red pulse) |
| `Final_Mix.wav` | mix file | ✅ `project/audio/Final_Mix.wav` — 38.900 s |

## Key editorial finding ⚠️
The recorded VO (40.32 s) does **not** contain the CTA's first sentence ("Read Brain Code's full
PHP2Shell breakdown to understand the risk, the response, and what to check next."). The last
segment (38.80–40.01) holds only "You'll find the link in the comments." (verified by syllable
density). Per the master-clock rule the edit syncs to the actual voice; no replacement voice was
generated and no words were rewritten. Caption cards 12–13 (that sentence) are therefore unused.
→ If the missing line is recorded later, Blocks F/G and Scene 07 can be re-timed without touching
scenes 01–06.

## Timeline
- Raw VO gaps >0.6 s compressed to 0.25 s (hook gap → 0.40 s; 0.555 s kept as-is). 7 zero-crossing
  cuts inside detected silences; VO never stretched. Rebuilt VO = 38.362 s; program = 38.90 s
  (video 1166 frames = 38.867 s + audio tail to 38.90 s).
- Scene spans (video clock): 01 0–3.598 · 02 –6.881 · 03 –13.646 · 04a/b/c –24.577 · 05 –29.953 ·
  06 –36.287 · 07 –38.90 (freeze on final brand frame to end).

## Audio mix
- Music: source 8.0–46.90 s (calm intro section), fade-in 0.15 s, base gain −9.5 dB,
  +3 dB swell 3.60–4.30 s (after hook), sidechain ducking (thr −26 dB, ratio 8, att 15 ms,
  rel 350 ms), fade-out 37.35→38.85 s completing with "comments".
- Program loudness: **−14.1 LUFS integrated, true peak −1.5 dBTP** (target −14 / ≤−1 ✓).
- VO: 24 kHz mono → 48 kHz stereo, never pitch/speed altered.

## Identity (Brain_Code_ID.zip — governing)
- Palette used: Brain Navy `#081320`, Deep Navy, Electric Blue `#007BFF`, Signal Cyan `#00D4FF`,
  Paper White `#F6F8FA`, warning red `#FF465C` (2 pulses only), one amber beat.
- Fonts: Sora ExtraBold (titles, as shipped in title PNGs + drawn kickers), Inter SemiBold captions.
- Logo: closing brand card `08_Closing_Brand.png` only (as-is, no redraw/glow); no strip clutter.
- No heavy glitch, no external logos/fonts, script wording untouched.

## QC (plan §10)
| Check | Result |
|---|---|
| Duration = VO (38.362) + freeze ≤1 s | ✅ 38.90 s |
| Hook complete <3 s (visual+text) | ✅ line1 @0, line2 @2.75, full by 2.9 s |
| Every spoken word captioned, synced | ✅ 12/12 cues on voice-actual times |
| Texts verbatim from approved script | ✅ (title cards used as shipped) |
| Identity compliance | ✅ see above |
| Music under voice, clean fade-out | ✅ ~−20 dB under voice (−38.6 dB tail mean), fade completes |
| No black frames / distortion / out-of-margin text | ✅ (blackdetect flags at 36.5–38.8 are the deep-navy brand gradient — false positive, frames contain content) |
| Loudness −14 LUFS, peak ≤ −1 dBTP | ✅ −14.1 / −1.5 |
| Full playback without faults | ✅ decode: 0 errors, 1166/1166 frames |

## Notes / decisions
1. **Bitrate:** x264 two-pass @14 Mbps target yields ~3.9 Mbps actual — still imagery is
   compression-efficient and the qp floor caps quality spend; transparency is total. Hard cap
   20 Mbps of the plan is respected. (VBV minrate games only bloat without quality gain.)
2. `xfade` unavailable in shipped static ffmpeg → scene-07 gradient enters via alpha fade (same look).
3. Voice-over source is 24 kHz mono (as delivered); delivered at 48 kHz stereo AAC per spec.
4. Working files kept: `project/` (state files INVENTORY/BRAND/PROGRESS, scenes, audio, tools).
