#!/usr/bin/env python3
"""Generate 6 prompts x {std, fast} at 480p/8s for the veo3 vs seedance comparison.

Prompts are verbatim from Veo-Flow-prompts.txt (plus one new one) — deliberately
NO lock blocks / start frames, so it's a raw same-prompt comparison against the
year-old veo3 clips. Results land in veo3_compare/outputs/<name>_<mode>.mp4.
Re-running skips clips that already exist.
"""

import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
GEN = HERE.parent / "gen.py"
OUT = HERE / "outputs"

PROMPTS = {
    "piano": "A cavalier king charles spaniel playing a piano by walking on the keys and crooning along. The music sounds beautiful, a little jazzy and discordant",
    "jacuzzi": 'Several people are in a bubbling jacuzzi. One fat man says, "I shouldn\'t have had so many beans" and gets out of the tub, at which point it stops bubbling',
    "rockface": 'A staggeringly large face made out of rock, as large as a continent, descends upon Earth and thunders, "Show me what you got"',
    "wormrace": "Six extremely athletic track athletes line up at the 100 meter line. One of them jumps several feet in the air, showing off his athletic prowess. The referee shoots the starting pistol... and the racers immediately drop to the ground and race by doing the worm to propel themselves forward",
    "snail": 'A man stands paralyzed with fear as a snail crawls towards him from across the room. The man stands in place without moving, only quivering a tiny bit. As the snail gets slightly closer he shouts, "What do I do!? It\'s coming straight at me!"',
    "pups": "A nest of cavalier king charles spaniel pups hatching out of speckled eggs, shaking themselves dry, and immediately begging for treats",
}


def make(name: str, mode: str) -> str:
    dest = OUT / f"{name}_{mode}.mp4"
    if dest.exists():
        return f"skip {dest.name} (exists)"
    cmd = [sys.executable, str(GEN), "video", PROMPTS[name],
           "--resolution", "480p", "--duration", "8"]
    if mode == "std":
        cmd.append("--std")
    for attempt in (1, 2, 3):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            shutil.copy(r.stdout.strip().splitlines()[-1], dest)
            return f"done {dest.name}"
        print(f"attempt {attempt} failed for {name}_{mode}:\n{r.stderr[-500:]}",
              flush=True)
    return f"FAILED {name}_{mode}"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    jobs = [(n, m) for m in ("fast", "std") for n in PROMPTS]
    with ThreadPoolExecutor(max_workers=12) as pool:
        for msg in pool.map(lambda j: make(*j), jobs):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
