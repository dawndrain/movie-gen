#!/usr/bin/env python3
"""pool_run.py variant for draft passes: FAST mode instead of --std.

Usage: python3 pool_run_fast.py overwhelming_beauty/videos_tv1.sh overwhelming_beauty/outputs/tv1 [workers]
"""
import shlex
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).parent
script, outdir = ROOT / sys.argv[1], ROOT / sys.argv[2]
workers = int(sys.argv[3]) if len(sys.argv) > 3 else 7
outdir.mkdir(parents=True, exist_ok=True)

jobs = []
for line in script.read_text().splitlines():
    line = line.strip().rstrip("&").strip()
    if not line.startswith("gen "):
        continue
    toks = shlex.split(line)
    jobs.append((toks[1], toks[2], toks[3], toks[4:]))


def run(job):
    name, dur, prompt, rest = job
    dest = outdir / f"{name}.mp4"
    if dest.exists():
        return f"SKIP {name}"
    cmd = [str(ROOT / "gen.py"), "video", prompt,
           "--resolution", "480p", "--duration", dur] + rest
    for attempt in range(1, 9):
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        out = r.stdout.strip().splitlines()
        if r.returncode == 0 and out and Path(out[-1]).exists():
            subprocess.run(["cp", out[-1], str(dest)])
            return f"OK {name}"
        (outdir / f"{name}.err").write_text(r.stdout + r.stderr)
        if "rate_limit_reached" in (r.stdout + r.stderr):
            time.sleep(60)  # shared 8-job pool congested; wait it out
        elif attempt >= 2:
            break
    return f"FAIL {name}"


print(f"{len(jobs)} shots, {workers} workers (FAST mode)", flush=True)
with ThreadPoolExecutor(max_workers=workers) as ex:
    futs = [ex.submit(run, j) for j in jobs]
    for f in as_completed(futs):
        print(f.result(), flush=True)
print("ALLDONE")
