#!/usr/bin/env bash
# THE NEXT YES — rebuild the whole deliverable from source assets.
# Usage: bash FF_Vid/scripts/build_all.sh
set -euo pipefail

OM=/home/user/OpenMontage
P=$OM/remotion-composer/projects/thenextyes
OUT=/home/user/VVV_creator/FF_Vid
FF=/home/user/.local/bin/ffmpeg

echo "== 1/5  score + sound design (original, synthesised) =="
"$OM/.venv/bin/python" "$P/audio_build.py"

echo "== 2/5  narration prep · conform to 1080x1920/30p · EDL · SRT =="
"$OM/.venv/bin/python" "$P/build_edit.py"

echo "== 3/5  Remotion render (Atelier composition) =="
cd "$OM/remotion-composer"
npx remotion render projects/thenextyes/index.tsx TheNextYes \
  "$OUT/renders/picture_master.mp4" \
  --public-dir=projects/thenextyes/public \
  --codec=h264 --crf=16 --concurrency=2 --jpeg-quality=95 \
  --audio-codec=aac --audio-bitrate=320k --log=info

echo "== 4/5  loudness delivery pass: -14 LUFS / -1 dBTP =="
"$FF" -y -v error -i "$OUT/renders/picture_master.mp4" \
  -af "loudnorm=I=-14:TP=-1.0:LRA=7:print_format=summary" \
  -c:v copy -c:a aac -b:a 320k -ar 48000 -movflags +faststart \
  "$OUT/THE_NEXT_YES_9x16.mp4"

echo "== 5/5  verify =="
"$FF" -hide_banner -nostats -i "$OUT/THE_NEXT_YES_9x16.mp4" -af ebur128=peak=true -f null - 2>&1 | tail -12
/home/user/.local/bin/ffprobe -v error -show_entries \
  format=duration,size,bit_rate -show_entries \
  stream=codec_name,width,height,r_frame_rate,sample_rate,channels \
  -of default=noprint_wrappers=1 "$OUT/THE_NEXT_YES_9x16.mp4"
echo "done → $OUT/THE_NEXT_YES_9x16.mp4"
