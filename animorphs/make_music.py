#!/usr/bin/env python3
"""Sonilo music cues for the Hork-Bajir Chronicles. Skips existing files."""
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "music"
OUT.mkdir(exist_ok=True)

CUES = [
    ("mus_frame", 60,
     "Warm intimate campfire storytelling theme: soft acoustic guitar, gentle "
     "strings, a hint of Native-American flute, golden-hour warmth and old "
     "sorrow remembered in peace. Instrumental only, no vocals."),
    ("mus_wonder", 90,
     "Soaring orchestral wonder theme for a vast alien forest at dawn: glassy "
     "shimmering textures, harp, slow building strings, awe and discovery, "
     "gentle and majestic. Instrumental only, no vocals."),
    ("mus_dread", 60,
     "Low ominous sci-fi dread drone: deep sub bass, slow distant metallic "
     "pulses, faint dissonant strings, invasion menace building quietly. "
     "Background ambience, no melody, no drums. Instrumental only, no vocals."),
    ("mus_battle", 60,
     "Urgent primal battle percussion: deep taiko drums, driving low strings, "
     "desperate guerrilla-war energy, relentless but organic. Instrumental "
     "only, no vocals."),
    ("mus_elegy", 60,
     "Sparse mournful elegy: lone cello and distant soft choir pads, long "
     "silences, grief for a dying world, very slow and quiet. Instrumental "
     "only, no vocals."),
    ("mus_hope", 90,
     "Tender hopeful sunrise theme: quiet piano and warm swelling strings, "
     "loss transformed into resolve and love, ending on a rising unresolved "
     "note of hope. Instrumental only, no vocals."),
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
