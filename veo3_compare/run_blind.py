#!/usr/bin/env python3
"""Generate 10 prompts x {std, fast} at 480p/8s for the blind std-vs-fast test.

Fresh prompts from the veo3 montage list (so they also serve the then-vs-now
project). Results land in outputs/blind/<name>_<mode>.mp4; re-runs skip
existing files.
"""

import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
GEN = HERE.parent / "gen.py"
OUT = HERE / "outputs" / "blind"

PROMPTS = {
    "python": "A giant python slithers through the jungle eating fruit after fruit after fruit, growing larger with every bite like a real life game of snake",
    "spaghetti": "A humanoid spaghetti creature eats a bowl of spaghetti by twirling it around his fork. His mouth makes happy slurping sounds",
    "horsebar": "A horse walks into a bar. The bartender puts out a whiskey and the horse starts drinking it",
    "zebra": "A zebra wearing a machine gun stands at the top of an outcropping overlooking a vast savannah, where many lions bow in submission",
    "hippotutu": "A hippo wears a tutu and dances around",
    "trex": 'An ancient army stands menacingly. The camera pans to an opposing man riding a t-rex, who shouts "For Dinosaurus!" and charges straight at them',
    "bear": "A bear wakes up after a long hibernation as sun peaks through her den. She then grumpily moans and knocks some dirt to block the sun and goes back to sleep",
    "fishchain": "A medium sized fish chases down a smaller fish and gobbles it up... and then right after a giant fish swallows the medium one. Finally a shark swallows the giant fish.",
    "victorians": "A group of Victorians are going for a trot, but they're all riding different animals, including a llama, goat, pony, and panda.",
    "kids1880s": "A group of children from the 1880's huddle around an ancient looking television all playing video games together",
}


def make(name: str, mode: str) -> str:
    dest = OUT / f"{name}_{mode}.mp4"
    if dest.exists():
        return f"skip {dest.name} (exists)"
    cmd = [sys.executable, str(GEN), "video", PROMPTS[name],
           "--resolution", "480p", "--duration", "8"]
    if mode == "std":
        cmd.append("--std")
    for attempt in (1, 2, 3, 4):
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
