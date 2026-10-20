# OpenMontage — sandbox environment kit

Artifacts produced while setting up the OpenMontage (free/open-source) video
production environment inside this sandbox (2026-10-20):

| File | Purpose |
|---|---|
| `ENVIRONMENT_SETUP.md` | Full record: what was installed, where, and why each substitute was needed (no apt, no GPU, network limited to GitHub/npm/PyPI) |
| `verify_environment.sh` | End-to-end smoke test (14 checks): ffmpeg/ffprobe/chromium/fc-list/pkg-config, encode + `apad -shortest` mux, venv imports, tool registry, Remotion composer, HyperFrames cache, Chromium CDP |
| `remotion.config.ts` | Remotion config pinned to the self-contained Chromium at `~/.local/bin/chromium` (copy lives at `OpenMontage/remotion-composer/remotion.config.ts`) |

The live installation itself is **not** vendored here:
- project clone: `/home/user/OpenMontage` (github.com/calesthio/OpenMontage)
- toolchain: `~/.local/bin` (ffmpeg 5.1.10 built from source, chromium 153
  wrapper, fc-list/pkg-config shims), `~/.local/lib/chromium-runtime`,
  `~/.local/ffmpeg5`
- python venv: `/home/user/OpenMontage/.venv`

Re-verify anytime with: `bash openmontage-env/verify_environment.sh`
(result at setup time: 14/14 PASS; full project pytest suite: 2043 passed).
