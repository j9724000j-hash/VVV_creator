#!/usr/bin/env python3
"""
THE NEXT YES — render through OpenMontage itself (Atelier authoring mode).

This is the in-framework path: `video_compose` is called with
`composition_mode: "atelier"`, which routes to `_render_via_atelier` and
bypasses the stock cut.type catalog / Explainer / CinematicRenderer entirely,
rendering the hand-authored entry below.

    cd /home/user/OpenMontage
    .venv/bin/python /home/user/VVV_creator/FF_Vid/scripts/run_openmontage_atelier.py

Notes
-----
* `bespoke.art_direction` is set, which is the doctrine check the tool runs
  (`_run_atelier_checks`) so the piece cannot ship without a declared direction.
* `edit_decisions.render_runtime = "remotion"` matches the proposal packet, so
  the final review will not flag `runtime_swap_detected`.
* The render is silent-by-default in atelier mode unless `audio_path` is given;
  here the composition carries its own audio, so none is passed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path("/home/user/OpenMontage")
sys.path.insert(0, str(REPO))

from tools.video.video_compose import VideoCompose  # noqa: E402

DELIVERY = Path("/home/user/VVV_creator/FF_Vid")
DECISIONS = json.loads((DELIVERY / "edit" / "edit_decisions.json").read_text())

edit_decisions = {
    "render_runtime": "remotion",
    "composition_mode": "atelier",
    "aspect_ratio": "9:16",
    "fps": DECISIONS["delivery"]["fps"],
    "duration_seconds": DECISIONS["delivery"]["duration_seconds"],
    "cuts": DECISIONS["cuts"],
    "bespoke": {
        "entry": "remotion-composer/projects/thenextyes/index.tsx",
        "composition_id": "TheNextYes",
        "public_dir": "remotion-composer/projects/thenextyes/public",
        "art_direction": "../FF_Vid/art-direction.md",
        "crf": 16,
        "concurrency": 2,
    },
}

tool = VideoCompose()
result = tool.run(
    {
        "operation": "render",
        "output_path": str(DELIVERY / "renders" / "picture_master.mp4"),
        "edit_decisions": edit_decisions,
    }
)

print("success:", result.success)
if not result.success:
    print("error:", result.error)
    sys.exit(1)

review = result.data.get("final_review", {})
print("final_review:", review.get("status"))
print("checks:", sorted(review.get("checks", {}).keys()))
for issue in review.get("issues_found", []):
    print(" •", issue)
print("output:", result.data.get("output"))
