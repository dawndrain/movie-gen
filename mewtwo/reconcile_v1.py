#!/usr/bin/env python3
"""Harvest completed server-side std seedance jobs into outputs/v1/<shot>.mp4.
Matches jobs to shots by exact prompt text from videos_v1.sh. Safe to re-run.
Usage: python3 reconcile_v1.py [--size 80]"""
import json
import shlex
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "outputs/v1"
OUT.mkdir(parents=True, exist_ok=True)

size = sys.argv[sys.argv.index("--size") + 1] if "--size" in sys.argv else "80"

# prompt -> shot from the batch script
prompt2shot = {}
for line in (HERE / "videos_v1.sh").read_text().splitlines():
    if line.startswith("gen "):
        toks = shlex.split(line)
        prompt2shot[" ".join(toks[3].split())] = toks[1]

r = subprocess.run(["higgsfield", "generate", "list", "--size", size, "--json"],
                   capture_output=True, text=True)
jobs = json.loads(r.stdout)
items = jobs if isinstance(jobs, list) else jobs.get("items", jobs.get("data", []))

stats = {"downloaded": 0, "in_progress": 0, "have": 0, "other": 0}
pending = []
for j in items:
    if "seedance" not in str(j.get("job_type", "")):
        continue
    p = j.get("params") or {}
    if p.get("mode") != "std":
        continue
    shot = prompt2shot.get(" ".join(str(p.get("prompt", "")).split()))
    if not shot:
        continue
    dest = OUT / f"{shot}.mp4"
    status = j.get("status")
    if dest.exists():
        stats["have"] += 1
        continue
    if status == "completed" and j.get("result_url") not in (None, "None", ""):
        urllib.request.urlretrieve(j["result_url"], dest)
        print(f"downloaded {shot}")
        stats["downloaded"] += 1
    elif status in ("in_progress", "queued", "created"):
        pending.append(shot)
        stats["in_progress"] += 1
    else:
        stats["other"] += 1

print(f"{stats}  pending: {sorted(set(pending))}")
