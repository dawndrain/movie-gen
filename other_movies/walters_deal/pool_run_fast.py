#!/usr/bin/env python3
"""Fast-mode variant of pool_run.py for the Walter's Deal first pass.

Same batch-script format, but omits --std so gen.py uses Seedance fast mode
(draft passes per MOVIE_LESSONS.md). Paths resolve against walters_deal/.

Usage: python3 walters_deal/pool_run_fast.py walters_deal/videos_v1.sh walters_deal/outputs/video1 [workers]
"""
import shlex
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).parent.parent  # videogen/
PROJ = Path(__file__).parent         # walters_deal/
script, outdir = ROOT / sys.argv[1], ROOT / sys.argv[2]
workers = int(sys.argv[3]) if len(sys.argv) > 3 else 7
outdir.mkdir(parents=True, exist_ok=True)

VARS = {}
jobs = []
for line in script.read_text().splitlines():
    line = line.strip().rstrip("&").strip()
    if not line.startswith("gen "):
        if "=" in line and line.split("=")[0].isupper() and '"' in line:
            k, v = line.split("=", 1)
            VARS[k] = v.strip('"')
        continue
    toks = shlex.split(line)
    name, dur, prompt, rest = toks[1], toks[2], toks[3], toks[4:]
    for k, v in VARS.items():
        prompt = prompt.replace(f"${{{k}}}", v).replace(f"${k}", v)
    paths = {"$F": str(PROJ / "frames"), "$A": str(PROJ / "anchors"), "$V": str(outdir)}
    for k, v in paths.items():
        rest = [t.replace(k, v) for t in rest]
    jobs.append((name, dur, prompt, rest))


def run(job):
    name, dur, prompt, rest = job
    dest = outdir / f"{name}.mp4"
    if dest.exists():
        return f"SKIP {name}"
    cmd = [str(ROOT / "gen.py"), "video", prompt,
           "--resolution", "480p", "--duration", dur] + rest  # no --std → fast
    for attempt in (1, 2):
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        out = r.stdout.strip().splitlines()
        if r.returncode == 0 and out and Path(out[-1]).exists():
            subprocess.run(["cp", out[-1], str(dest)])
            return f"OK {name}"
        (outdir / f"{name}.err").write_text(r.stdout + r.stderr)
    return f"FAIL {name}"


print(f"{len(jobs)} shots, {workers} workers", flush=True)
with ThreadPoolExecutor(max_workers=workers) as ex:
    futs = [ex.submit(run, j) for j in jobs]
    for f in as_completed(futs):
        print(f.result(), flush=True)
print("ALLDONE")
