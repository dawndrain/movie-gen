#!/usr/bin/env python3
"""Sonilo music cues for THE DAVID TRILOGY. Skips existing files."""
import re
import subprocess
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "music"
OUT.mkdir(exist_ok=True)

CUES = [
    ("mus_mystery", 75,
     "Nocturnal suburban mystery theme: soft ticking percussion, curious "
     "plucked strings, a faint synth shimmer like something glowing in the "
     "dark, wonder edged with wrongness. Background ambience, understated. "
     "Instrumental only, no vocals."),
    ("mus_dread", 60,
     "Low ominous sci-fi dread drone: deep sub bass, slow distant metallic "
     "pulses, faint dissonant strings, menace building quietly. Background "
     "ambience, no melody, no drums. Instrumental only, no vocals."),
    ("mus_wonder", 60,
     "Soaring first-flight wonder theme: harp and glassy shimmering textures "
     "lifting into slow ecstatic strings, night air and freedom, brief and "
     "beautiful. Instrumental only, no vocals."),
    ("mus_battle", 60,
     "Urgent predatory battle percussion: deep drums, driving low strings, "
     "two great beasts circling, relentless, organic, dangerous. Instrumental "
     "only, no vocals."),
    ("mus_elegy", 90,
     "Sparse devastated elegy: lone cello over ocean-deep silence, distant "
     "soft piano notes like drops of water, guilt and grief with no relief, "
     "very slow and quiet. Instrumental only, no vocals."),
]

for name, dur, prompt in CUES:
    dest = OUT / f"{name}.m4a"
    if dest.exists():
        print("skip", name)
        continue
    cmd = ["higgsfield", "generate", "create", "sonilo_music",
           "--prompt", prompt, "--duration", str(dur), "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout + r.stderr
    urls = re.findall(r"https://\S+\.(?:m4a|mp3|wav)\S*", out)
    if not urls:
        urls = re.findall(r"https://\S+", out)
    if r.returncode != 0 or not urls:
        print(f"FAIL {name}: {out.strip()[-200:]}")
        continue
    urllib.request.urlretrieve(urls[-1].rstrip('",'), dest)
    print("OK  ", name)
