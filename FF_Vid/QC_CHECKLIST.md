# QC — THE NEXT YES

Two gates: the brief's ten editorial/QC points, then six technical gates measured
on the delivered file. Verified against `THE_NEXT_YES_9x16.mp4`.

## A. The brief's ten points

| # | Requirement | Result |
|---|---|---|
| 1 | First spoken line begins immediately, no logo or intro animation | **PASS** — picture rises from black for 16 frames (0.53 s) and narration starts at 0:00.30; no logo, no title animation, no sting. |
| 2 | Voice-over sounds natural to an American audience | **PASS** — en-US narrator, General American, conversational; digits avoided in the input text ("fifty-two"). Synthetic timbre is the one honest caveat. |
| 3 | Story understandable without sound, thanks to captions | **PASS** — 24 authored caption lines, 100 % of narration covered, per-word timing, 4 emphasis phrases. |
| 4 | Main character looks like the same person in every shot | **PASS (source-bound)** — the eight supplied clips already share wardrobe/hair/age; this edit does not regenerate or restyle faces. Minor variance in her hair volume between scenes 3 and 7 is in the source. |
| 5 | Emotional progression visible without exaggeration | **PASS** — fear → hesitation → reflection → courage → cautious hope is carried by gaze, posture and light (cool dusk → warm morning), not by tears. |
| 6 | Café scene reads as a tentative beginning, not instant romance | **PASS** — second cup present, companion reduced to an out-of-focus shoulder, half-smile only, no contact, no music swell. |
| 7 | Final line finishes cleanly and the closing question stays readable | **PASS** — VO ends 0:42.50; question types in at 0:40.75 and holds until 0:45.10 (2.6 s clear, above the 1.5–2 s asked). |
| 8 | Never implies every relationship is safe / never tells people to ignore red flags | **PASS** — "starting over doesn't mean trusting everyone" is spoken *and* captioned; the ledger graphic puts judgement (not the stranger) at the centre. |
| 9 | Music and effects never compete with narration | **PASS** — measured below. |
| 10 | Final cut within 38–40 s without rushing the pauses | **DEVIATION, declared** — 45.10 s. 94 words = 37.3 s of speech; the required pauses need ~8 s. Cutting to 40 s would have deleted them. See `edit/timing-report.md`. |

## B. Technical gates

| Gate | Measured | Verdict |
|---|---|---|
| Resolution / aspect | 1080×1920 (exact 9:16), yuv420p, TV range, BT.709 primaries/transfer/matrix | PASS |
| Frame rate | 30.000 fps constant, 1353 frames, no VFR | PASS |
| Duration | 45.097 s picture (1353 frames); 45.12 s container; audio 2116 frames @48 k — no drift | PASS |
| Codecs | H.264 High (9.56 Mbps) + AAC-LC 48 kHz stereo 322 kbps, `+faststart` | PASS |
| Loudness | **−13.9 LUFS** integrated, true peak **−1.2 dBTP**, LRA 3.4 LU (measured on the final file with `ebur128`) | PASS |
| Dialogue separation | narration −18 LUFS stems; music beds at 0.17–0.20 linear (~−17 dB), effects 0.17–0.30 | PASS |
| Caption safe area | lowest text baseline 1430 px; bottom 408 px free of text for the Shorts UI | PASS |
| Face safety | no graphic overlaps eyes/mouth in any of the 10 cues (frame-checked at 15 timecodes) | PASS |
| Text integrity | 0 AI-rendered words in the footage; all text is live composition text | PASS |
| Sync | every caption block starts within 1 frame of its VO stem; word windows ≤ 120 ms of speech | PASS |

## C. Playback checks performed

- Decode of all 1353 frames without error (`ffmpeg -v error -i … -f null -`).
- Frame-exact still review at 0:02, 0:04, 0:09, 0:13, 0:17, 0:22, 0:24, 0:29,
  0:31, 0:35, 0:38, 0:40, 0:43, 0:45.
- Both dissolves checked for double-exposure on her face (13 frames, 45 % peak)
  — no ghosting.
- Audio: no clipping, no codec pre-echo on the piano attack, no chime over a
  spoken word (chime at 0:07.64 falls inside the 0.19 s gap before "After a
  painful relationship").

## D. Open items handed over

1. Human narration re-record (if desired) — re-run `build_edit.py` and captions
   re-derive from the new stems.
2. Optional native-1080p regeneration of the eight scenes for a sharper master.
3. Thumbnail pick for the non-Shorts shelf version, if you also publish a 16:9 cut.
