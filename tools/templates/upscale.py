#!/usr/bin/env python3
# TEMPLATE — copied from homo_sapien/upscale.py (per-clip 480p->1080p Bytedance upscale).
# Project-specific: expects that film's spec/paths. Copy into a new film
# folder and adapt; the original in homo_sapien/ is the working example.
"""Upscale every 480p clip to 1080p with Bytedance Video Upscale.

    python3 upscale.py [workers]

Per-CLIP, not on the finished film: the assembler keeps owning the trims, the
beat fit and the audio, so Lenka's master is never re-encoded. Skips clips whose
1080p version already exists, so re-running it IS the retry pass.

`preset=aigc` is the one tuned for AI-generated footage (vs common/ugc/old_film).
s40b has no clip on purpose (it's a held still) — the 2k PNG is already sharper
than 1080p, so the assembler just scales it down.
"""
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROJ = Path(__file__).parent
SRC = PROJ / "outputs/video1"
DST = PROJ / "outputs/video1_1080"


def upscale(clip: Path) -> str:
    out = DST / clip.name
    if out.exists():
        return f"skip {clip.stem}"
    cmd = ["higgsfield", "generate", "create", "bytedance_video_upscale",
           "--video", str(clip),
           "--resolution", "1080p",
           "--preset", "aigc",
           "--wait"]
    for attempt in (1, 2, 3):
        res = subprocess.run(cmd, capture_output=True, text=True)
        blob = res.stdout + res.stderr
        urls = re.findall(r"https://\S+\.mp4", blob)
        if res.returncode == 0 and urls:
            urllib.request.urlretrieve(urls[-1], out)
            return f"OK   {clip.stem}"
        print(f"retry {clip.stem} ({attempt}): {blob.strip()[-160:]}", flush=True)
    return f"FAIL {clip.stem}"


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    DST.mkdir(parents=True, exist_ok=True)
    clips = sorted(SRC.glob("*.mp4"))
    print(f"upscaling {len(clips)} clips -> 1080p ({workers} workers)")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for r in pool.map(upscale, clips):
            print(r, flush=True)


if __name__ == "__main__":
    main()
