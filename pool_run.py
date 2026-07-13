#!/usr/bin/env python3
"""Run the gen calls from a batch script through a bounded worker pool.

Higgsfield ultra allows 8 concurrent seedance jobs; we keep 7 in flight. Skips shots
whose output mp4 already exists, so it double-serves as the retry runner.

Usage (from a PROJECT folder, e.g. long_game/):
    python3 ../pool_run.py videos_v3.sh outputs/video3 [workers] [fast]
Script, outdir, and all relative media paths resolve against the current working
directory (the project folder); gen.py is found next to this script.
Pass "fast" to drop --std (draft mode: ~3 min/clip, half credits).
"""
import shlex
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

TOOLS = Path(__file__).parent          # shared gen.py lives here
ROOT = Path.cwd()                       # the project folder
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
    paths = {"$F2": "frames2", "$F": "frames", "$A": "anchors", "$V": str(outdir)}
    for k, v in paths.items():
        rest = [t.replace(k, v) for t in rest]
    jobs.append((name, dur, prompt, rest))


def run(job):
    name, dur, prompt, rest = job
    dest = outdir / f"{name}.mp4"
    if dest.exists():
        return f"SKIP {name}"
    mode = [] if "fast" in sys.argv[4:] else ["--std"]
    cmd = [str(TOOLS / "gen.py"), "video", prompt,
           "--resolution", "480p", *mode, "--duration", dur] + rest
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
