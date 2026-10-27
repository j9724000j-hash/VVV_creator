# PROGRESS — Brain Code PHP2Shell
> Read this FIRST at every step. Update at end of every step.

## Status log
| Step | Task | Status | Output |
|---|---|---|---|
| 1 | Unzip + inventory + capability declaration | ✅ DONE | `INVENTORY.md`, this file |
| 2 | Brand extraction from Brain_Code_ID | ⏳ next | `BRAND.md` |
| 3 | VO duration + split into Blocks 1–6 | pending | timing table below |
| 4 | Music analysis + trim/extend plan | pending | music section below |
| 5 | Scene decisions 01–07 | pending | scene table below |
| 6–12 | Render scene 01…07 (one per step) | ✅ DONE (7/7, previews checked) | `scenes/Scene_01..07.mp4` |
| 13a | Final synced captions | ✅ DONE | `../BrainCode_PHP2Shell_Captions.srt` (12 cues) |
| 13b | Audio mix (ducking + fade + loudness) | ✅ DONE −14.1 LUFS / −1.5 dBTP | `audio/Final_Mix.wav` |
| 14 | Assembly/export + QC checklist | ✅ DONE all-PASS | `../BrainCode_PHP2Shell_Final.mp4` + `../EDIT_REPORT.md` + `../Cover_Frame.png` |

## Block timing table (Step 3 — measured via silencedetect -38dB + syllable density)
⚠️ KEY FINDING: recorded VO = 40.32 s. Final segment 38.80–40.01 contains only ~6–8 syllables
= **"You'll find the link in the comments."** — the CTA's first sentence ("Read Brain Code's full
PHP2Shell breakdown…") is NOT in the recording. Master-clock rule → sync to actual voice, no TTS
replacement, no stretching. Documented for EDIT_REPORT.md.

| Block | VO text (spoken) | Start | End | Scene |
|---|---|---|---|---|
| 1 | Your website works. / That doesn't mean it's safe. | 0.00 (voice 0.30) | 3.60 | 01 |
| 2a | Behind every page, code runs out of sight. | 3.60 (voice 4.27) | 7.16 | 02 |
| 2b | Brain Code's PHP2Shell article explores… foundation. | 7.16 | 13.92 | 03 |
| 3 | But discovery isn't protection. / A website can look… update. | 13.92 (voice 14.65) | 25.70 | 04 |
| 4 | The lesson? Check your PHP version, not just your plugins. | 25.70 (voice 26.38) | 31.51 | 05 |
| 5 | So what does PHP2Shell mean… AI fit into the story? | 31.51 (voice 32.16) | 38.24 | 06 |
| 6 | You'll find the link in the comments. (only) | 38.24 (voice 38.80) | 40.32 | 07 |

Internal sub-beats: "protection" ≈16.1s · "normal" ends 21.24 · "update" ends 25.70 ·
"version," ≈29.4s · "website," 35.86 · "comments" ends ≈40.01. Video total = 40.32 + end-freeze ≈ **41.3 s**.

## Music plan (Step 4 — measured: 155.95 s, mean RMS -15.2 dB, calm section 8–16 s)
- Source offset: start music at src 8.0 s (calm intro) → covers full video (needs 41.3 s).
- 150 ms fade-in; base gain ≈ -9.5 dB (≈ -24.5 dBFS), brief +3 dB swell 3.6→4.3 s (after hook).
- Ducking: sidechaincompress vs VO (threshold -26 dB, ratio 8, attack 15 ms, release 350 ms) → music ≈ -20 dB under voice per plan.
- Fade out 37.35 → 38.85 s on COMPRESSED timeline ("comments" ends 38.362; video total 38.90).
- Final program: loudnorm two-pass I=-14 LUFS, TP=-1.5 dBTP (≤ -1 required), LRA≈9. VO: 24 kHz mono → 48 kHz stereo.

## Scene decisions (Step 5)
| Scene | Span | Visual stack (bottom→top) | Motion |
|---|---|---|---|
| 01 Hook | 0.00–3.60 | bg01 → Title01 (0–3.1) → hard-cut Title02 (3.1–3.6, cyan→red accent pulse on "safe") → Readability Shade | zoom 100→106%; instant entry |
| 02 Title | 3.60–7.16 | bg03 AI_Discovery (pan down) → Title03 fade+scale @3.9 → Shade | pan 0→-3%, cross-dissolve 0.25 s in |
| 03 Hidden code | 7.16–13.92 | bg04 Hidden_Runtime → Runtime_Layers rise (7.6→9.6, bottom-up stagger) → PHP_Badge pop @9.8 → Scan_Beam sweep @10.4 (on "AI") → kicker text BEHIND EVERY PAGE, CODE RUNS. @7.4 | layered reveals; fade+scale elements |
| 04 Stakes | 13.92–25.70 | 04a 13.92–17.02: bg02 Shield_Breach + Title04 @14.7 + ONE red glow pulse @16.1 ("protection") · 04b 17.02–21.85: bg01 + Browser_HUD drift ("perfectly normal") · 04c 21.85–25.70: bg04 + Runtime_Layers + PHP_Badge + amber "UPDATE" beat @23.5 (internal hard cuts) | hard cuts on sub-beats |
| 05 Lesson | 25.70–31.51 | bg05 Navy_Grid (calm) → PHP_Badge center-left → Title05 line1 @26.9 → line2 @29.4 → Shade | visual de-escalation; slow zoom 102→104% |
| 06 Curiosity | 31.51–38.24 | bg05 → Neural_Network drift (opacity 0.85) → Title06 @32.2 → Shade | slow drift; open-question feel |
| 07 CTA | 38.24–41.30 | brand gradient (081320→0B1E32→007BFF) → Comments_CTA card @38.6 → Title07 LINK IN COMMENTS ↓ @39.0 → Down_Arrow loop → Closing_Brand @40.2 → freeze last 0.4 s | confident hold; subtle arrow bounce |

Caption cards (09_Captions_Transparent) re-timed to ACTUAL voice (draft cues 12–13 not spoken → omitted; card 14 used for the final line). Positions: captions band ≈ 62–78% height (above platform UI zone); final video keeps bottom 18% light where possible.

## FINAL COMPRESSED TIMELINE v2 (governs all rendering; replaces raw times above)
Silence compression (plan §7.1): gaps >0.6 s → 0.25 s (hook gap → 0.40 s dramatic; 0.555 s kept).
VO rebuilt from 7 zero-crossing cuts inside detected silence + inserted silence. No stretch.
Total video = **38.90 s** (1167 frames @30fps). Audio segments (VO src time): A 0.300–3.598 · B 4.274–13.922 ·
C 14.654–21.236 · D 21.853–25.702 · E 26.382–31.508 · F 32.161–38.245 · G 38.800–40.320.

| Scene | Video span | On-screen | Key beats |
|---|---|---|---|
| 01 | 0.000–3.598 | t01→t02 @2.75 + red mini-pulse @3.30 | zoom 100→106%, hook full <3 s |
| 02 | 3.998–6.881 | t03 @4.30 | bg03 pan down, dissolve in |
| 03 | 6.881–13.646 | kicker text @7.0 (drawtext), layers rise 7.3→9.3, PHP badge @9.5, scan sweep 10.2→11.9 | bg04 |
| 04a | 13.896–16.200 | t04 @14.60, red pulse @15.45 (word "protection" 15.72) | bg02, hard cut in |
| 04b | 16.200–20.728 | Browser_HUD drift | bg01 "looks normal" |
| 04c | 20.728–24.577 | layers+badge, amber UPDATE beat @23.30 | bg04 |
| 05 | 24.827–29.953 | t05 @25.65, line2 drawtext @27.85 | bg05 calm, PHP badge |
| 06 | 30.203–36.287 | t06 @30.50 | bg05 + neural drift |
| 07 | 36.842–38.900 | t07 @36.95, arrow bounce @37.35, t08 brand @38.16, freeze →38.90 | brand gradient |

Captions (video clock, card→span): c1 0.30–1.80 · c2 2.29–3.60 · c3 4.00–6.32 · c4 6.88–10.06 · c5 10.06–13.646 ·
c6 13.90–15.72 · c7 16.20–20.478 · c8 20.73–24.577 · c9 24.83–29.95 · c10 30.20–33.90 · c11 33.90–36.287 ·
c14 36.84–38.05. Cards 12–13 unused (lines not recorded). Brand: closing scene only (t08) — no strip clutter.

## Global decisions
- Target: 1080×1920 @30fps, H.264 yuv420p 12–20 Mbps, AAC 48 kHz ≥256 kbps, ~-14 LUFS, ≤-1 dBTP.
- Video length = VO 40.32 s + end freeze ≤1 s.
- Silence gaps >0.6 s → tighten to ~0.25 s (keep ~0.4 s dramatic pause after hook) — implement via per-block video segment cut points, never by editing VO audio.
- Render strategy: per-scene MP4 segments (frames generated by ffmpeg zoompan/overlay/fade on stills), then concat + audio mux.

## Refinements during render (authoritative)
- Scene 05: drawtext line2 y=1276, fade-in @3.27 (on "not just your plugins." beat).
- Scene 07: brand gradient via alpha fade-in overlay (imageio ffmpeg lacks xfade); verified OK.
- Caption boundary c4/c5 → 9.70 (proportional mid-sentence); c14 span 36.842–38.30.
- Music src offset 8.0 s: 8.0+38.9 = 46.9 ≤ 155.95 ✓.
- ffmpeg: full static 4.1.9 (johnvansickle via npm @ffmpeg-installer, has drawtext, lacks xfade)
  at ~/.local/bin/ffmpeg + ffprobe; imageio 7.0.2 as FFMPEG_OVERRIDE fallback.

## PROJECT COMPLETE (2026-10-27)
Final: `php2shell/BrainCode_PHP2Shell_Final.mp4` — 1080×1920@30, H.264, AAC 256k, 38.87 s, −14.1 LUFS.
WARNING documented: CTA first sentence not present in delivered VO recording (see EDIT_REPORT.md).
