#!/usr/bin/env python3
"""Round 2: 10 more prompts x {std, fast} at 480p/8s for the blind test."""

import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
GEN = HERE.parent / "gen.py"
OUT = HERE / "outputs" / "blind2"

PROMPTS = {
    "contortionist": "A contortionist is all curled up in a ball, while a couple people try to untangle her",
    "somersault": "Several competitors are lined up at the top of a hill. A ref shoots a starting gun, and then the competitors all start somersaulting down the hill as quickly as they can",
    "coffeeflames": "A woman sits at a table drinking a cup of coffee, while the entire room is engulfed in giant flames. She turns the page of her paper",
    "toelicker": 'A fat man licks his orange toes several times before looking at the camera and saying, "It\'s not like you don\'t do this too"',
    "pizzadim": "A dimension in which all the sentient beings walking around and enjoying life are pizzas. Meanwhile all the furniture and appliances are made out of people",
    "toys": "A bunch of sentient toys are playing with each other. Someone opens the door, and then they all fall to the floor before the person can see them",
    "hawkmorph": "A thirteen year old boy morphing into a red-tailed hawk and taking to the skies",
    "monsters": "A man putters around into his dark bedroom. He turns on the light, and then it's revealed that there's a group of monsters that were waiting for him!",
    "molecity": "An underground city, in which mole-like people walk around",
    "blankets": 'A man shivers and shouts "Does anyone have a blanket", so one woman after another wraps him in a blanket, with at least ten blankets by the end, at which point he says, "That\'s more like it"',
}


def make(name: str, mode: str) -> str:
    dest = OUT / f"{name}_{mode}.mp4"
    if dest.exists():
        return f"skip {dest.name} (exists)"
    cmd = [sys.executable, str(GEN), "video", PROMPTS[name],
           "--resolution", "480p", "--duration", "8"]
    if mode == "std":
        cmd.append("--std")
    for attempt in range(1, 7):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            shutil.copy(r.stdout.strip().splitlines()[-1], dest)
            return f"done {dest.name}"
        print(f"attempt {attempt} failed for {name}_{mode}:\n{r.stderr[-300:]}",
              flush=True)
    return f"FAILED {name}_{mode}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(n, m) for m in ("fast", "std") for n in PROMPTS]
    with ThreadPoolExecutor(max_workers=20) as pool:
        for msg in pool.map(lambda j: make(*j), jobs):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
