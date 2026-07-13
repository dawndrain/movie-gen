#!/usr/bin/env python3
"""Generate videos (Seedance 2.0) and images (Nano Banana Pro) via the Higgsfield CLI.

Usage:
    ./gen.py video "drone shot over a mountain valley at sunrise"
    ./gen.py video "..." --resolution 720p --duration 10 --start-image ref.png
    ./gen.py image "a cozy cabin in a snowy forest at dusk"
    ./gen.py image "..." --resolution 2k --image ref1.png --image ref2.png

Requires `higgsfield auth login` once beforehand.
Results are downloaded to outputs/raw/<timestamp>_<slug>.<ext>.
"""

import argparse
import datetime
import os
import random
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

OUTPUTS = Path(__file__).parent / "outputs" / "raw"

# Cross-session semaphore for the 8-concurrent-seedance cap (ultra plan).
# Every gen.py video call (from any Claude session / terminal) claims a slot
# file before submitting and releases it after; submissions past the cap are
# insta-rejected server-side, so this is what actually shares the quota.
# Override with SEEDANCE_SLOTS (e.g. export SEEDANCE_SLOTS=4 when you're also
# submitting jobs outside gen.py, like the web UI).
SLOTS_DIR = Path(__file__).parent / ".seedance_slots"
MAX_SLOTS = int(os.environ.get("SEEDANCE_SLOTS", "8"))
SLOT_STALE_SEC = 40 * 60  # a video job should never take this long


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, ValueError):
        return False


def acquire_slot() -> Path:
    SLOTS_DIR.mkdir(exist_ok=True)
    while True:
        for i in range(MAX_SLOTS):
            p = SLOTS_DIR / f"slot_{i}"
            try:  # reclaim slots from dead or wedged processes
                pid = int(p.read_text().split()[0])
                if not _pid_alive(pid) or time.time() - p.stat().st_mtime > SLOT_STALE_SEC:
                    p.unlink()
            except (FileNotFoundError, ValueError, IndexError):
                pass
            try:
                fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, f"{os.getpid()} {int(time.time())}".encode())
                os.close(fd)
                return p
            except FileExistsError:
                continue
        time.sleep(5 + random.random() * 5)


def run(kind: str, args: argparse.Namespace) -> Path:
    if kind == "video":
        cmd = [
            "higgsfield", "generate", "create", args.model,
            "--prompt", args.prompt,
            "--resolution", args.resolution,
            "--duration", str(args.duration),
            "--aspect_ratio", args.aspect_ratio,
        ]
        # fast mode only supports 480p/720p
        if args.resolution in ("480p", "720p") and not args.std:
            cmd += ["--mode", "fast"]
        if args.start_image:
            cmd += ["--start-image", args.start_image]
        if args.end_image:
            cmd += ["--end-image", args.end_image]
        for ref in args.image or []:
            cmd += ["--image", ref]
        for ref in args.video or []:
            cmd += ["--video", ref]
        for ref in args.audio or []:
            cmd += ["--audio", ref]
        if args.no_audio:
            cmd += ["--generate_audio", "false"]
    else:
        cmd = [
            "higgsfield", "generate", "create", "nano_banana_2",
            "--prompt", args.prompt,
            "--resolution", args.resolution,
            "--aspect_ratio", args.aspect_ratio,
        ]
        for ref in args.image or []:
            cmd += ["--image", ref]
    cmd.append("--wait")

    print("+", " ".join(cmd), file=sys.stderr)
    slot = acquire_slot() if kind == "video" else None
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        if slot:
            slot.unlink(missing_ok=True)
    output = (result.stdout + result.stderr).strip()
    urls = re.findall(r"https://\S+\.(?:mp4|png|jpg|jpeg|webp)", output)
    if result.returncode != 0 or not urls:
        sys.exit(f"generation failed:\n{output}")

    url = urls[-1]
    slug = re.sub(r"[^a-z0-9]+", "-", args.prompt.lower())[:40].strip("-")
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    dest = OUTPUTS / f"{stamp}_{slug}{Path(url).suffix}"
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    print(url, file=sys.stderr)
    print(dest)
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="kind", required=True)

    video = sub.add_parser("video", help="Seedance 2.0 video")
    video.add_argument("prompt")
    video.add_argument("--model", default="seedance_2_0",
                       choices=["seedance_2_0", "seedance_2_0_mini"])
    video.add_argument("--resolution", default="480p",
                       choices=["480p", "720p", "1080p", "4k"])
    video.add_argument("--duration", type=int, default=5)
    video.add_argument("--aspect_ratio", default="16:9")
    video.add_argument("--std", action="store_true",
                       help="use std mode even at 480p/720p (default: fast)")
    video.add_argument("--start-image")
    video.add_argument("--end-image")
    video.add_argument("--image", action="append", help="image reference (up to 9)")
    video.add_argument("--video", action="append", help="video reference (up to 3)")
    video.add_argument("--audio", action="append", help="audio reference (up to 3)")
    video.add_argument("--no-audio", action="store_true")

    image = sub.add_parser("image", help="Nano Banana Pro image")
    image.add_argument("prompt")
    image.add_argument("--resolution", default="1k", choices=["1k", "2k", "4k"])
    image.add_argument("--aspect_ratio", default="16:9")
    image.add_argument("--image", action="append", help="image reference (up to 14)")

    args = parser.parse_args()
    run(args.kind, args)


if __name__ == "__main__":
    main()
