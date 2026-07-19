#!/usr/bin/env python3
# TEMPLATE — batch Nano Banana anchors/frames from a spec.
# Originated in a local-only project; this template is the canonical copy.
# Project-specific paths/spec: copy into a new film folder and adapt.
"""Batch Nano Banana Pro images for a film's anchors and start frames.

Usage: python3 make_images.py <stage>    stage in {anchors, frames}
Skips images whose output exists (re-run = retry pass). `frames` needs
`anchors` done first. Specs live in spec.py (single source of truth).
"""
import subprocess
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import spec

HERE = Path(__file__).parent
GEN = HERE.parent / "gen.py"
ANCH = HERE / "anchors"
FRAMES = HERE / "frames"


def resolve_ref(r: str) -> Path:
    p = ANCH / f"{r}.png"
    if p.exists():
        return p
    raise FileNotFoundError(f"ref {r} not found in {ANCH}")


def make(outdir: Path, name: str, aspect: str, prompt: str, refs: list) -> str:
    out = outdir / f"{name}.png"
    if out.exists():
        return f"skip {name}"
    cmd = [sys.executable, str(GEN), "image", prompt,
           "--resolution", "2k", "--aspect_ratio", aspect]
    for r in refs:
        cmd += ["--image", str(resolve_ref(r))]
    err = ""
    for attempt in (1, 2, 3):
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            src = Path(res.stdout.strip().splitlines()[-1])
            shutil.copy(src, out)
            return f"OK   {name}"
        err = (res.stdout + res.stderr).strip()[-300:]
        print(f"retry {name} (attempt {attempt}): {err}", flush=True)
    return f"FAIL {name}"


def main():
    stage = sys.argv[1]
    if stage == "anchors":
        jobs, outdir = spec.ANCHORS, ANCH
    elif stage == "frames":
        jobs, outdir = spec.FRAMES, FRAMES
    else:
        sys.exit(f"unknown stage {stage}")
    # anchors with refs (donut_crowned) must run after their base exists:
    # split into ref-free and ref-having waves within the stage.
    outdir.mkdir(exist_ok=True)
    wave1 = [j for j in jobs if not j[3]]
    wave2 = [j for j in jobs if j[3]]
    for wave in (wave1, wave2):
        if not wave:
            continue
        with ThreadPoolExecutor(max_workers=5) as pool:
            futs = [pool.submit(make, outdir, n, a, p, r) for n, a, p, r in wave]
            for f in futs:
                print(f.result(), flush=True)


if __name__ == "__main__":
    main()
