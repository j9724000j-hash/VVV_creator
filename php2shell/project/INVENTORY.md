# INVENTORY — Brain Code PHP2Shell (Step 1 output)
Sources: `extracted/` (from ABCA.zip + Brain_Code_ID.zip). Do NOT re-zip/re-analyze; work from this file.

## Audio (master clock)
| File | Duration | Format |
|---|---|---|
| `extracted/Voice_Over.wav` | **40.32 s** | PCM 16-bit, 24 kHz, mono — THE master clock, never stretched |
| `extracted/Background_musuc.mp3` | **155.95 s** | MP3 48 kHz stereo 128 kbps (+embedded cover art, ignore) |

## Visual assets (extracted/assets/)
- **01_Backgrounds** — all 1080×1920, no alpha: 01_Working_Website_Hidden_Risk, 02_Shield_Breach, 03_AI_Discovery, 04_Hidden_Runtime, 05_Navy_Grid, 06_Light_Editorial
- **02_Transparent_Elements** (alpha): 01_Readability_Shade 1080×1920 · 02_Browser_HUD 1000×760 · 03_Runtime_Layers 1080×900 · 04_PHP_Badge 640×640 · 05_Comments_CTA 1000×470 · 06_Down_Arrow 300×500 · 07_Cyan_Scan_Beam 1080×1920 · 08_Red_Warning_Glow 1000×1000 · 09_Neural_Network 1080×1920 · 10_Tech_Brand_Strip 1080×260
- **03_Titles_PNG** — 8 title cards, all 1080×1920 alpha (01_Hook_First_Line, 02_Hook_Question, 03_PHP2Shell_AI, 04_Discovery, 05_Check_PHP, 06_Question, 07_CTA, 08_Closing_Brand)
- **04_Titles_Editable_SVG** — same titles as SVG (fallback; PNG preferred)
- **05_Ready_Scenes** — 7 composited frames 1080×1920 (01_Scene…07_Scene) — match Scene Map 01–07
- **06_Fonts** — Sora-Bold, Sora-ExtraBold, Inter-SemiBold, Inter-Bold (+OFL licenses)
- **07_Edit_Guide** — Approved_Script_EN.txt, English_Captions_DRAFT.srt (14 cues), README_AR.md, manifest.json
- **08_Previous_Assets** — old Cairo-era pack (preferred: NO, use new Sora/Inter titles)
- **09_Captions_Transparent** — 14 caption cards 1080×1920 alpha, ordered = draft SRT cue order

## Brand (extracted/brand/) — governing identity (Step 2 → BRAND.md)
- `brain-code-visual-identity.md` (full guide) + `brain-code-visual-identity-board.png` 1536×1024

## Rendering capability (declared)
YES — ffmpeg 7.0.2 static available (imageio-ffmpeg, symlinked `~/.local/bin/ffmpeg`).
Real MP4 export possible: 1080×1920, 30 fps, H.264, AAC 48 kHz. No GPU (CPU x264 only). No ffprobe binary — use `project/tools/probe.py` (parses `ffmpeg -i`).

## Key paths
- Project state: `php2shell/project/` · Renders: `php2shell/project/renders/` · Scenes: `php2shell/project/scenes/`
- Assets root: `php2shell/extracted/assets/` · Brand: `php2shell/extracted/brand/`
- Fonts: `php2shell/extracted/assets/06_Fonts/`
- Deliverables (final): `php2shell/BrainCode_PHP2Shell_Final.mp4`, `BrainCode_PHP2Shell_Captions.srt`, `Cover_Frame.png`, `EDIT_REPORT.md`
