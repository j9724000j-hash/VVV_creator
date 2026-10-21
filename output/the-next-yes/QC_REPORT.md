# THE NEXT YES — Quality Control Report

**Status:** Rendered and checked; delivery includes the noted limitations below.  
**Final file:** `the-next-yes_final.mp4`

## Verified output

- Duration: **40.000 s** (container and video stream probe)
- Video: **H.264 / AVC**, **1080×1920**, progressive, **30 fps**, 9:16
- Audio: **AAC-LC**, **48 kHz**, stereo; 40.000 s
- Measured decoded audio sample peak via FFmpeg `volumedetect`: **−1.8 dBFS**; mean **−20.0 dBFS**. This is sample-peak measurement, not a true-peak measurement.
- File size: **36,382,493 bytes** (MP4, fast-start metadata); file was reopened/probed after muxing.
- Eight supplied scene clips were used, in script order. Scene 8's embedded horizontal letterbox was cropped/reframed to fill the 9:16 output without stretching.
- English captions are burned into the MP4 and also delivered as an SRT. The invitation and closing question are separate post-production text overlays, not baked into source footage.
- Opening begins on the first scene with narration; there is no opening logo/title. The final question is visible from 38.3 s to the end (about 1.7 s).
- Spot-checks were made at the opening, scene boundaries, invitation overlay, café, and final card; output has playable video/audio streams and no intentional blank gaps.

## Important limitations

- No OpenMontage checkout was mounted in this runtime despite the repository's setup note. The available local tools were FFmpeg/FFprobe. The render is an FFmpeg-based edit, not an OpenMontage project render.
- No configured natural-voice provider or downloaded neural voice model was available. The narration was generated locally with eSpeak NG (female English-US voice variant), then mixed and processed. It is intelligible and timed to the cut, but it does **not** meet the brief's premium natural human-voice target; review/replace with an approved human or natural neural performance before publication if that target is essential.
- The music and ambience are original procedural synthesis made for this cut. The piano is restrained, but it is a synthesized tonal score rather than a performed/licensed acoustic piano recording. No paid service was used.
- Subtitle timing is phrase-level editorial timing, aligned to the generated narration segments. A human listening pass is recommended because the local TTS is synthetic.
- No dedicated true-peak meter, automated transcription, or full subjective loudspeaker/headphone review was available. Do not interpret the reported sample peak as dBTP.

## QC outcome

The MP4 is present and readable; its duration, dimensions, frame rate, codecs, audio channels/sample rate, and sample peak were verified. Scene continuity and overlays were frame-sampled. The limitations above are material, especially narration quality; the file is an actual render, not a silent placeholder, but should be auditioned before publishing.
