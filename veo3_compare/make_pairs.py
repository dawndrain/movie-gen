#!/usr/bin/env python3
"""Cut the blind test pairs: pair01.mp4..pair10.mp4 in blind_pairs/.

Each pair plays take A then take B (8s each) with only "PAIR N - A/B" labels;
whether A is std or fast is randomized per pair and recorded in
blind_pairs/answer_key.txt — don't open it until you've scored all ten.
"""

import random
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "outputs" / "blind"
OUT = HERE / "blind_pairs"

NAMES = ["python", "spaghetti", "horsebar", "zebra", "hippotutu",
         "trex", "bear", "fishchain", "victorians", "kids1880s"]

OUT.mkdir(exist_ok=True)
rng = random.SystemRandom()
key_lines = []
order = rng.sample(NAMES, len(NAMES))  # shuffle pair order too

for idx, name in enumerate(order, 1):
    modes = ["std", "fast"]
    rng.shuffle(modes)
    inputs, filters, concat = [], [], ""
    for j, (slot, mode) in enumerate(zip("AB", modes)):
        inputs += ["-i", str(SRC / f"{name}_{mode}.mp4")]
        filters.append(
            f"[{j}:v]scale=854:480,setsar=1,fps=24,"
            f"drawtext=text='PAIR {idx} — {slot}':x=16:y=16:fontsize=30:"
            f"fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=8[v{j}];"
            f"[{j}:a]aresample=48000,aformat=channel_layouts=stereo[a{j}]")
        concat += f"[v{j}][a{j}]"
    graph = ";".join(filters) + f";{concat}concat=n=2:v=1:a=1[v][a]"
    dest = OUT / f"pair{idx:02d}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", *inputs, "-filter_complex", graph,
                    "-map", "[v]", "-map", "[a]", "-preset", "veryfast",
                    "-crf", "19", str(dest), "-y"], check=True)
    key_lines.append(f"pair{idx:02d}: {name:<11} A={modes[0]:<4} B={modes[1]}")
    print(f"built {dest.name} ({name})")

(OUT / "answer_key.txt").write_text("\n".join(key_lines) + "\n")
(OUT / "scoresheet.txt").write_text(
    "Blind std-vs-fast test — for each pair write A or B (the take you prefer)\n\n"
    + "\n".join(f"pair{i:02d}: " for i in range(1, 11)) + "\n")
print("answer key + scoresheet written (don't peek at answer_key.txt)")
