#!/usr/bin/env python3
"""Asset probe tool — PNG dimensions/alpha + audio duration via ffmpeg -i parsing."""
import os, re, struct, subprocess, json, sys

FF = os.environ.get("FFMPEG", "/usr/local/bin/ffmpeg")

def png_info(path):
    with open(path, "rb") as f:
        data = f.read(33)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    bit_depth, color_type = data[24], data[25]
    has_alpha = color_type in (4, 6)
    return {"w": w, "h": h, "has_alpha": has_alpha, "color_type": color_type}

def audio_info(path):
    """Parse `ffmpeg -i` stderr for duration and stream info."""
    p = subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True)
    err = p.stderr
    dur = None
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", err)
    if m:
        dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    streams = []
    for sm in re.finditer(r"Stream #0:(\d+).*?: (Audio|Video): (.*)", err):
        streams.append({"idx": int(sm.group(1)), "type": sm.group(2), "detail": sm.group(3).strip().rstrip(",").strip()})
    br = None
    m = re.search(r"bitrate:\s*(\d+)\s*kb/s", err)
    if m:
        br = int(m.group(1))
    return {"duration": dur, "streams": streams, "kbps": br}

def loudness(path, offset=None, dur=None):
    """Measure integrated loudness + true peak via ffmpeg loudnorm/ebur128."""
    cmd = [FF, "-hide_banner", "-nostats"]
    if offset is not None:
        cmd += ["-ss", str(offset)]
    cmd += ["-i", path, "-t", str(dur)] if dur else ["-i", path]
    cmd += ["-af", "ebur128=peak=true", "-f", "null", "-"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    err = p.stderr
    out = {}
    m = re.search(r"I:\s*(-?[\d.]+)\s*LUFS", err)
    if m: out["i_lufs"] = float(m.group(1))
    m = re.search(r"Peak:\s*(-?[\d.]+)\s*dBFS", err)
    if m: out["peak_dbfs"] = float(m.group(1))
    return out

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "png":
        print(json.dumps(png_info(sys.argv[2])))
    elif cmd == "audio":
        print(json.dumps(audio_info(sys.argv[2])))
    elif cmd == "loud":
        print(json.dumps(loudness(sys.argv[2])))
