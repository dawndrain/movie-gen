#!/usr/bin/env python3
"""TARGETED EDIT of an existing frame — change one thing, keep everything else.

    python3 edit_frame.py s08_side_by_side "the teal mongoose is now a teal FOX"
    python3 edit_frame.py s39_fridge_handprints "..." --ref kid

Nano Banana Pro will faithfully preserve an image passed as an --image ref and
change only what you name. This is enormously cheaper than a re-roll: a re-roll
re-rolls EVERYTHING (faces, set, staging, light), so fixing one animal can lose
you the whole shot — the retake regression law. A targeted edit can't.

The current frame is archived to frames_prev/<name>_<n>.png first, so every edit
is revertible (and outputs/raw/ keeps every generation anyway).
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJ = Path(__file__).parent
GEN = PROJ.parent / "gen.py"
FRAMES = PROJ / "frames"
ANCH = PROJ / "anchors"
PREV = PROJ / "frames_prev"

KEEP = (
    "This is a targeted edit. Reproduce the reference image EXACTLY as it is — "
    "the identical composition, framing, camera angle, lens, lighting, colour "
    "grade, background, set, and every person, animal and object in it, all in "
    "exactly the same positions and poses — and change ONLY the one thing "
    "described below. Everything else in the picture must be pixel-for-pixel "
    "unchanged. Do not re-stage, do not re-light, do not re-frame, do not "
    "add or remove anything else. Photorealistic, no text, no watermark."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frame")
    ap.add_argument("change", help="what to change, in plain words")
    ap.add_argument("--ref", action="append", default=[],
                    help="extra anchor refs (e.g. --ref kid)")
    args = ap.parse_args()

    src = FRAMES / f"{args.frame}.png"
    if not src.exists():
        sys.exit(f"no such frame: {src}")

    PREV.mkdir(exist_ok=True)
    n = len(list(PREV.glob(f"{args.frame}_*.png")))
    backup = PREV / f"{args.frame}_{n}.png"
    shutil.copy(src, backup)

    prompt = f"{KEEP}\n\nTHE ONE CHANGE: {args.change}"
    cmd = [sys.executable, str(GEN), "image", prompt,
           "--resolution", "2k", "--aspect_ratio", "16:9",
           "--image", str(src)]
    for r in args.ref:
        cmd += ["--image", str(ANCH / f"{r}.png")]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not res.stdout.strip():
        sys.exit(f"edit failed:\n{(res.stdout + res.stderr)[-400:]}")

    out = Path(res.stdout.strip().splitlines()[-1])
    shutil.copy(out, src)
    print(f"edited  {args.frame}")
    print(f"  was   {backup}   (revert: cp that back over frames/{args.frame}.png)")


if __name__ == "__main__":
    main()
