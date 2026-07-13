#!/usr/bin/env python3
"""Sonilo music cues for THE VARIANCE. Skips existing files."""
import re
import subprocess
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "music"
OUT.mkdir(exist_ok=True)

CUES = [
    ("mus_baseline", 60,
     "Cold minimalist ambient drone for a sterile utopia: soft airy synth "
     "pads, a faint distant mechanical hum, patient, emotionally flat, "
     "strangely beautiful, like a building breathing. Background ambience, "
     "no drums, no melody. Instrumental only, no vocals."),
    ("mus_drawer", 75,
     "Fragile hushed wonder: sparse single piano notes with long decay over "
     "very quiet sustained strings, the feeling of something opening for the "
     "first time, tender and slightly uneasy, very slow and quiet. "
     "Instrumental only, no vocals."),
    ("mus_alive", 90,
     "Warm intimate awakening theme: soft fingerpicked acoustic guitar, "
     "gentle swelling strings and light hand percussion arriving late, "
     "golden-hour joy discovered for the first time, alive and openhearted "
     "but never bombastic. Instrumental only, no vocals."),
    ("mus_collapse", 60,
     "Quiet overwhelm and fraying: trembling high dissonant strings over a "
     "soft accelerating heartbeat pulse, beauty curdling into panic, "
     "claustrophobic but hushed, no percussion hits, no melody. Background "
     "ambience. Instrumental only, no vocals."),
    ("mus_elegy", 90,
     "Sparse mournful elegy of acceptance: lone quiet piano and low warm "
     "strings, long silences between phrases, grief settling into calm, "
     "ending unresolved on a single held note. Very slow, very quiet. "
     "Instrumental only, no vocals."),
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
