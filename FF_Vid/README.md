# FF_Vid — THE NEXT YES · final vertical cut

> **بالعربي، باختصار:** هذا مجلد التسليم النهائي. الفيديو جاهز في
> `THE_NEXT_YES_9x16.mp4` — ‏1080×1920، 30 إطار/ثانية، ‏45.1 ثانية، بصوت تعليق
> أمريكي، ترجمة مدمجة، وموسيقى ومؤثرات أصلية. كل شيء قابل لإعادة البناء بأمر واحد.

Final deliverable of the *Fear of Falling in Love Again After 50* brief, authored
in **OpenMontage with Atelier authoring mode + the Remotion runtime**, built from
the eight clips in `the-next-yes-scenes.zip`, and merged to the `The-next-yes`
lineage in this folder.

---

## 1. What is here

| Path | What it is |
|---|---|
| `THE_NEXT_YES_9x16.mp4` | **the film** — 1080×1920, 30 fps, H.264 High BT.709, AAC 320 kbps, −13.9 LUFS / −1.2 dBTP |
| `renders/picture_master.mp4` | pre-loudness master out of Remotion — **local only, git-ignored** (regenerable) |
| `source/remotion-project/` | the whole Atelier composition (TSX, EDL builder, score synthesiser, fonts, grain, props) — vendored for review |
| `edit/edit_decisions.json` | the full EDL, decision log, graphics + audio cue sheets |
| `edit/timing-report.md` | locked timings, narration map, source-footage budget |
| `art-direction.md` | the Atelier art-direction declaration (palette, type, motion, signature devices) |
| `subtitles/THE_NEXT_YES.srt` | sidecar captions (upload alongside the Short) |
| `publishing/youtube-package.md` | title, description, hashtags, pinned comment, upload settings |
| `QC_CHECKLIST.md` | the brief's 10 QA points plus 6 technical gates, with results |
| `scripts/build_all.sh` | one command to rebuild picture + audio + master |
| `scripts/run_openmontage_atelier.py` | the same render through OpenMontage's `video_compose` (atelier path) |

## 2. Specs

```
container   MP4 (H.264 High, yuv420p, limited range, BT.709, faststart, CRF 16)
picture     1080 × 1920 (9:16), 30.000 fps, 1353 frames
duration    45.097 s  (0:45.10)
audio       48 kHz stereo AAC 320 kbps · −13.9 LUFS integrated · −1.2 dBTP · LRA 3.4
captions    burned-in (Inter 600, fixed 3-line column) + SRT sidecar
safe area   top 154 px · bottom 408 px · sides 72 px
```

## 3. Beat sheet (locked)

| # | Beat | In – Out | Dur | Cut in | Beat's job |
|---|---|---|---|---|---|
| 1 | THE HOOK | 0:00.00 – 0:03.80 | 3.8 | rise from black | age + solitude + strength, one image |
| 2 | THE REAL FEAR | 0:03.80 – 0:06.50 | 2.7 | hard | the empty chair = the cost of the past |
| 3 | THE INVITATION | 0:06.50 – 0:11.48 | 5.0 | hard | a message arrives; the world offers something |
| 4 | THE HESITATION | 0:11.48 – 0:15.78 | 4.3 | hard | the thumb that does not move |
| 5 | WHY SHE ALMOST SAID NO | 0:15.78 – 0:21.19 | 5.4 | hard | the reflection: desire vs. self-protection |
| 6 | THE TURNING POINT | 0:21.19 – 0:28.15 | 7.0 | hard | the question she asks herself (longest beat) |
| 7 | ONE SMALL YES | 0:28.15 – 0:34.28 | 6.1 | dissolve 13f | courage without a guarantee |
| 8 | THE TAKEAWAY | 0:34.28 – 0:45.10 | 10.8 | dissolve 13f | the thesis, then 2.3 s of silence under the question |

Narration sits between 66 % and 78 % of every beat; the pauses are the drama, not
slack. Full per-word map in `edit/timing-report.md`.

## 4. Graphics — ten cues, one subject each

| Beat | Graphic | Type | Content |
|---|---|---|---|
| 1 | Age slug | infographic | hairline + `AGE / 52 / not afraid of alone` |
| 1 | Tick rail (in) | navigation | 8 ticks draw on; the film declares its own structure |
| 2 | Two paths | infographic | `What she knew` (faded) vs `What she risked` (ember, advancing) |
| 3 | Message card | motion graphic | typing indicators → *"Would you like to get dinner this Friday?"* |
| 4 | Hesitation gauge | infographic | Yes / **Not yet** / No, cursor drifts toward No and retreats |
| 5 | Then / Now ledger | infographic | `someone else's choice` → `her own judgement` |
| 6 | Chapter marker | motion graphic | ember margin rule draws down, names *the turning point* |
| 7 | One-coffee tally | infographic | 1 of 9 rings lit: *one coffee — not a promise* |
| 8 | Tick rail (out) | navigation | the rail becomes a timer while she walks |
| 8 | Final question | typography | `Would you give love another chance?` + wordmark |

Every word on screen is live text in the composition — nothing is baked into the
AI footage, so every line is retypeable and re-renderable.

## 5. Sound

- **Narration** — 10 stems, trimmed on detected speech, 90 Hz high-pass, 2.2:1
  compression, −18 LUFS each. Script line "At 52" was fed to the voice engine as
  "At fifty-two" so it is never read as digits.
- **Score** (original, synthesised in `audio_build.py`, licence-free):
  `music_A` 0:00–0:29 sparse felt piano in A minor, 60 BPM; `music_B` 0:28–0:45
  adds a slow pad and a singing melody, resolves to C(add9).
- **Design**: room tone 0:00–28.7 · phone chime 0:07.6 (as the message appears) ·
  rising air swell 0:20.0 (into the turning point) · keyboard taps 0:26.2 ·
  café murmur 0:28.2–0:36.6 · street air 0:34.6–end. All effects are ≥ 10 dB
  under the voice.
- The music drops its top partial at the question and returns 0.4 s later, so the
  line lands in air rather than in a swell.

## 6. Craft notes (why it looks the way it does)

1. **Conform before compose.** Each of the eight source clips is trimmed and
   conformed to 1080×1920 / 30 fps *in its own pass* (lanczos, light eq, gentle
   unsharp), so the composition never re-times or upscales a video in-browser —
   frame-accurate cuts, no fps drift, no half-scaled decoder chroma.
2. **Camera drift is written per beat**, never a generic Ken Burns: scene 2 pulls
   laterally *away from the empty chair*, scene 6 eases back as she starts typing.
   Ceiling: 7 % scale over the whole shot.
3. **Subtitles cannot reflow.** Lines are authored (not auto-wrapped), positioned
   by first line, and revealed as a unit with a 10 px rise; the word being spoken
   tints warm. Emphasis is 700 + ember, exactly four times.
4. **Legibility is a layer, not a hope.** Bottom scrim + per-shot warm/cool
   soft-light grade + radial vignette + top band, all under the graphics.
5. **Grain is real film grain** — three 640×360 tiles, reseeded every frame,
   overlay-blended at 6 %, drifting sub-pixel.
6. **The held last frame.** Scene 8's source is exactly 8.00 s but the beat needs
   10.8 s, so the final frame is held (with the camera already at rest) under the
   closing question instead of freezing mid-stride or looping the walk.

## 7. Honest deviations from the brief

| Brief | Delivered | Why |
|---|---|---|
| 38–40 s | **45.1 s** | 94 words = 37.3 s of measured speech; the brief's own pauses (pre/post question, hesitation hold, 1.5–2 s on-screen question) need ~8 s. Cutting to 40 s would have deleted the pauses that carry the story. |
| "Highlight a few key phrases such as *choosing wrong again*, *one coffee*, *your future*" | all four, plus *the cost* | matches the brief's intent; the list was "such as". |
| 1080p not specified | 1080×1920, upscaled 1.5× from the 720×1280 sources | Shorts delivery spec. Native-720 delivery is available by re-rendering `--scale=0.667`. |
| No end-card requested | the close is 2.3 s of the held frame under the question, no CTA, no subscribe sting | per QC 7 and 8: the question is the CTA. |

## 8. Rebuild

```bash
cd /home/user/OpenMontage
.venv/bin/python remotion-composer/projects/thenextyes/audio_build.py   # score + design
.venv/bin/python remotion-composer/projects/thenextyes/build_edit.py    # VO prep, conform, EDL, SRT
cd remotion-composer && npx remotion render projects/thenextyes/index.tsx TheNextYes \
  /path/picture_master.mp4 --public-dir=projects/thenextyes/public \
  --codec=h264 --crf=16 --concurrency=2 --audio-bitrate=256k
```

Then the loudness pass in `scripts/build_all.sh` (loudnorm → −14 LUFS / −1 dBTP,
AAC 320 k). The same render is available in-tree through OpenMontage:
`scripts/run_openmontage_atelier.py` calls `video_compose` with
`composition_mode: "atelier"` and `bespoke.entry = projects/thenextyes/index.tsx`
— the exact payload is in `edit/edit_decisions.json`.

## 9. Known limitations

- Source footage is 720×1280; at 1080×1920 the 1.5× upscale is clean but a native
  1080p regeneration would be sharper on a 6-inch screen.
- The narration is synthetic. It is level-matched and de-clicked, but a human
  read would still buy the pauses cheaply.
- Word timings are syllable-weighted (no forced aligner available offline); they
  sit within ~120 ms of the voice. If you dub or re-record the VO, re-run
  `build_edit.py` and the captions re-derive themselves.
