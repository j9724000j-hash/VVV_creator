# OpenMontage — Sandbox Environment Setup (2026-10-20)

This environment has **no access to Debian/apt repositories and no GPU**. Only
GitHub (`github.com`, `api.github.com`, `codeload.github.com`), the npm
registry and PyPI are reachable. Everything below was installed exclusively
from those three sources. This document records what was installed, where it
lives, and why each substitute was chosen.

## Layout

| Component | Location | Source |
|---|---|---|
| OpenMontage repo | `/home/user/OpenMontage` | `git clone https://github.com/calesthio/OpenMontage` |
| Python venv (3.11) | `/home/user/OpenMontage/.venv` | system Python + PyPI |
| Node deps (Remotion composer) | `/home/user/OpenMontage/remotion-composer/node_modules` | registry.npmjs.org |
| FFmpeg 5.1.10 (static, built from source) | `~/.local/bin/ffmpeg` → `~/.local/ffmpeg5/bin/ffmpeg` | GitHub source (`FFmpeg/FFmpeg` tag n5.1.10) + `mirror/x264`, `lameproject/lame`, `fribidi/fribidi`, `freetype/freetype`, `harfbuzz/harfbuzz`, `libass/libass`, `madler/zlib`. Full feature set: libx264, libmp3lame, libfreetype (drawtext), libass (subtitles/ass), zlib (png). Build tooling (`cmake`, `ninja`, `meson`) installed from PyPI wheels; `pkg-config` is a local shim (`~/.local/bin/pkg-config`). |
| FFprobe 5.1.10 | `~/.local/bin/ffprobe` → `~/.local/ffmpeg5/bin/ffprobe` | same build |
| Font substitutes | `segoeui.ttf` / `segoeuib.ttf` symlinks (→ DejaVu Sans / Bold) in repo root | `showcase_card.py` passes bare Segoe-UI filenames to `drawtext`; without fontconfig these resolve relative to cwd, so the symlinks act as the stand-in fonts |
| `fc-list` substitute | `~/.local/bin/fc-list` | hand-written shim (fontTools name-table reader) — Pygments' ImageFormatter shells out to `fc-list`, unavailable without fontconfig CLI packages |
| Chromium 153 headless-shell | `~/.local/bin/chromium` → `~/.local/lib/chromium-runtime/` | npm `@sparticuz/chromium` v153 (binary + NSS/Vulkan/SwiftShader libs + fonts all inside the npm tarball) |
| HyperFrames runtime | npx cache | registry.npmjs.org (`hyperframes@0.8.181`) |
| Piper TTS (offline voice engine) | venv (`piper-tts` 1.8.0) | PyPI |

`~/.local/bin` is exported on `PATH` via `~/.bashrc` / `~/.profile`.

## FFmpeg version matrix (why 5.1)

OpenMontage's `audio_mixer` muxes tracks with
`-af apad -shortest` (infinite padding filter + stop-at-shortest). Behaviour
per FFmpeg generation, measured in this sandbox:

| FFmpeg | `amix normalize=` (needs ≥4.4) | `apad`+`-shortest` terminates | source tried |
|---|---|---|---|
| 4.1 (2018) | ✗ | ✓ | npm `@ffmpeg-installer/ffmpeg` |
| 4.2.2 | ✗ | ✓ | PyPI `imageio-ffmpeg` 0.5.x |
| **5.1.10** | **✓** | **✓** | **built from GitHub source** |
| 7.0.2 / 7.1 | ✓ | ✗ (encodes padded silence forever; `-shortest` semantics changed in FFmpeg ≥6) | PyPI `imageio-ffmpeg` 0.6.0 / Remotion compositor bundle |

FFmpeg ≥6 re-implemented `-shortest` against post-filter (infinite) streams,
so the mux never ends; <4.4 lacks `amix normalize`. 5.1 is the intersection.
Built with `--disable-asm` (no nasm/yasm in sandbox) — slower but correct.
Remotion/HyperFrames rendering is unaffected: Remotion encodes with its own
bundled `@remotion/compositor-linux-x64-gnu/ffmpeg` (n7.1).

## Substitutes and why

* **FFmpeg**: `apt install ffmpeg` impossible (Debian mirrors unreachable;
  GitHub release *assets* also redirect to a blocked host). The npm packages
  `@ffmpeg-installer/ffmpeg` + `@ffprobe-installer/ffprobe` ship fully static
  GPL builds (libx264, aac, prores, png, 125+ filters) inside the registry
  tarball itself. Verified: encode + probe of a test MP4.
* **Chromium**: Remotion normally downloads Chrome Headless Shell from Google
  storage (blocked) and the sandbox lacks *all* GUI/NSS system libraries.
  `@sparticuz/chromium` (built for AWS Lambda) bundles the headless-shell
  binary **plus** the missing shared libraries (`libnss3`, `libnspr4`,
  `libnssutil3`, freebl/softokn, `libexpat`), the Khronos **Vulkan loader**
  (`libvulkan.so.1`) and **SwiftShader** software GL, and its own fonts.
  Installed pieces:
  * `~/.local/lib/chromium-runtime/chromium` — the binary
  * `~/.local/lib/chromium-runtime/lib/` — NSS + expat + `libvulkan.so.1`
    (+ `libvulkan.so` symlink — ANGLE dlopens the unversioned name) +
    `libvk_swiftshader.so`, `libGLESv2.so`, `libEGL.so`
  * `~/.local/lib/chromium-runtime/vk_swiftshader_icd.json` — ICD manifest
    (its `library_path` patched; also copied flat next to the binary)
  * `~/.local/lib/chromium-runtime/fonts/` — fontconfig dir
  * `~/.local/bin/chromium` — wrapper exporting `LD_LIBRARY_PATH`,
    `FONTCONFIG_PATH`, `VK_ICD_FILENAMES` and adding the flags this container
    needs: `--no-sandbox --disable-dev-shm-usage --single-process --no-zygote
    --use-angle=swiftshader --enable-unsafe-swiftshader`
  Verified: CDP handshake (`/json/version` → `HeadlessChrome/153.0.8010.0`),
  puppeteer-core screenshot, and `WEBGL_RENDERER = ANGLE (…, SwiftShader
  driver)`.
* **Remotion browser**: `remotion-composer/remotion.config.ts` pins
  `Config.setBrowserExecutable('~/.local/bin/chromium')` +
  `setChromiumOpenGlRenderer('swangle')` + `setConcurrency(2)` so
  `npx remotion render` never tries the blocked Google download.
* **Piper voices / Kokoro / whisper-cpp**: engine installed from PyPI; the
  *voice models* live on HuggingFace (unreachable here), so offline narration
  needs a later model drop or cloud TTS keys in `.env`.

## Verification performed

1. `make setup` — venv, Python deps, Remotion composer, piper-tts,
   HyperFrames cache-warm, `.env` creation: **OK**
   (`HyperFrames runtime_available=True`).
2. `make lint`, `make preflight` (tool registry provider menu): **OK**.
3. `make hyperframes-doctor`: **OK** — ffmpeg/ffprobe/chromium/node all
   detected (only optional extras missing: whisper-cpp, Kokoro, MusicGen,
   Docker).
4. `make test` — full pytest suite: **2043 passed, 0 failed**, 12 skipped,
   3 xfailed (5m20s).
5. `python render_demo.py focusflow-pitch` — full Remotion render of a
   zero-key demo to `projects/demos/renders/focusflow-pitch.mp4`
   (h264 1080p30 + AAC, 675 frames, 22.5 s) — proves browser + SwiftShader +
   ffmpeg chain end to end.
6. FFmpeg smoke test: `ffmpeg -f lavfi testsrc … -c:v libx264 -c:a aac` +
   `ffprobe` on the result.
7. Puppeteer screenshot + WebGL probe through the bundled Chromium.

## Re-running any of this

* Chromium wrapper: edit `~/.local/bin/chromium`.
* Rebuild the runtime dir from scratch:
  `cd ~/.local/lib/om-tools && npm i @sparticuz/chromium @ffmpeg-installer/ffmpeg @ffprobe-installer/ffprobe`
  then `node -e "import('@sparticuz/chromium').then(m=>m.default.executablePath())"`
  (inflates into `/tmp`), then copy `/tmp/chromium`, `/tmp/al2023/lib/*`,
  `/tmp/lib{vulkan.so.1,GLESv2.so,EGL.so,vk_swiftshader.so}`,
  `/tmp/vk_swiftshader_icd.json`, `/tmp/fonts` into
  `~/.local/lib/chromium-runtime/` as laid out above.
