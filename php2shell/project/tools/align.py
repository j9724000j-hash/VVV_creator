#!/usr/bin/env python3
"""Word-level forced alignment of the assembled VO with pocketsphinx.
Output: project/audio/word_times.json + caption cue times derived ONLY from measured word bounds."""
import subprocess, json, os, sys
import numpy as np
from pocketsphinx import Decoder, Config, get_model_path, set_loglevel

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FF = os.path.expanduser("~/.local/bin/ffmpeg")
AUD = os.path.join(ROOT, "project/audio")

# 1) 16 kHz mono s16 raw for pocketsphinx
subprocess.run([FF, "-hide_banner", "-loglevel", "fatal", "-y", "-i",
                os.path.join(AUD, "VO_assembled.wav"),
                "-f", "s16le", "-ac", "1", "-ar", "16000", "/tmp/vo16k.raw"], check=True)
raw = open("/tmp/vo16k.raw", "rb").read()
print(f"audio: {len(raw)/32000:.3f} s @16kHz")

# 2) normalized alignment transcript (matches ACTUAL pronunciation; letters spelled out)
TEXT = ("your website works that doesn't mean it's safe "
        "behind every page code runs out of sight "
        "brain code's p h p to shell article explores what happens "
        "when a i helps uncover security flaws hiding in that foundation "
        "but discovery isn't protection "
        "a website can look perfectly normal "
        "while the software underneath still needs a security update "
        "the lesson check your php version not just your plugins "
        "so what does php to shell mean for your website "
        "and where does a i fit into the story "
        "you'll find the link in the comments")

mp = get_model_path()
set_loglevel("FATAL")
cfg = Config(hmm=os.path.join(mp, "en-us", "en-us"), dict=os.path.join(mp, "en-us", "cmudict-en-us.dict"),
             lm=None, loglevel="FATAL")
d = Decoder(cfg)
try:
    d.set_align_text(TEXT)
except RuntimeError as e:
    print("ALIGN TEXT ERROR:", e)
    # find OOV words
    for w in TEXT.split():
        if d.lookup_word(w) is None:
            print("OOV:", w)
    sys.exit(1)
d.start_utt()
d.process_raw(raw, full_utt=True)
d.end_utt()

words = []
for seg in d.seg():
    if seg.word in ("<s>", "</s>", "<sil>", "[SPEECH]", "[NOISE]"):
        continue
    words.append({"w": seg.word, "s": seg.start_frame / 100.0, "e": seg.end_frame / 100.0})
print(f"aligned words: {len(words)}  span: {words[0]['s']:.2f} → {words[-1]['e']:.2f}")
json.dump(words, open(os.path.join(AUD, "word_times.json"), "w"), indent=1)
for x in words:
    print(f"  {x['s']:6.2f} {x['e']:6.2f}  {x['w']}")
