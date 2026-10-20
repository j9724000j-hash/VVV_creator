#!/bin/bash
# OpenMontage sandbox environment — end-to-end smoke verification.
# Usage: bash scripts/verify_environment.sh
set -u
export PATH="$HOME/.local/bin:$PATH"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PASS=0; FAIL=0
ok()   { echo "  [PASS] $1"; PASS=$((PASS+1)); }
bad()  { echo "  [FAIL] $1"; FAIL=$((FAIL+1)); }
check(){ if eval "$2" >/dev/null 2>&1; then ok "$1"; else bad "$1"; fi; }

echo "== 1. Core binaries =="
check "ffmpeg on PATH (>=4.4 amix normalize)" "ffmpeg -hide_banner -h filter=amix | grep -q normalize"
check "ffprobe on PATH"        "ffprobe -version"
check "chromium wrapper"       "chromium --headless --version"
check "fc-list shim"           "fc-list | grep -q DejaVu"
check "pkg-config shim"        "pkg-config --version || pkg-config --exists x264 -C"

echo "== 2. FFmpeg functional =="
T=$(mktemp -d)
check "encode h264+aac test clip" "ffmpeg -y -v error -f lavfi -i testsrc=duration=1:size=320x240:rate=24 -f lavfi -i sine=duration=1 -c:v libx264 -preset ultrafast -c:a aac -shortest $T/t.mp4"
check "ffprobe reads it back"     "ffprobe -v error -show_entries format=duration -of csv=p=0 $T/t.mp4"
check "apad+shortest mux terminates" "ffmpeg -y -v error -f lavfi -i testsrc=duration=3:size=320x240:rate=24 -c:v libx264 -preset ultrafast $T/v.mp4 && ffmpeg -y -v error -f lavfi -i sine=duration=1 $T/a.wav && timeout 30 ffmpeg -y -v error -i $T/v.mp4 -i $T/a.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -af apad -shortest -movflags +faststart $T/m.mp4"
rm -rf "$T"

echo "== 3. Python environment =="
check "venv python imports"  "$ROOT/.venv/bin/python -c 'import yaml, pydantic, jsonschema, dotenv, PIL, numpy, requests, fastapi, uvicorn, watchfiles, piper, onnxruntime, fontTools, google.genai, openai'"
check "tool registry discover" "$ROOT/.venv/bin/python -c 'from tools.tool_registry import registry; registry.discover()'"

echo "== 4. Node / Remotion / HyperFrames =="
check "remotion composer node_modules" "test -x $ROOT/remotion-composer/node_modules/.bin/remotion"
check "remotion config pins browser"   "grep -q setBrowserExecutable $ROOT/remotion-composer/remotion.config.ts"
check "hyperframes npx cache"          "npx --no-install hyperframes --version || npx --yes hyperframes --version"

echo "== 5. Chromium CDP + WebGL =="
T2=$(mktemp -d)
nohup chromium --headless=new --remote-debugging-port=9333 --user-data-dir=$T2/prof about:blank >$T2/log 2>&1 &
CPID=$!
sleep 6
if curl -s --max-time 5 http://127.0.0.1:9333/json/version | grep -q HeadlessChrome; then ok "CDP /json/version responds"; else bad "CDP /json/version responds"; fi
kill $CPID 2>/dev/null; sleep 1; pkill -9 -x chromium 2>/dev/null
rm -rf "$T2"

echo
echo "RESULT: $PASS passed, $FAIL failed"
exit $FAIL
