#!/usr/bin/env python3
"""Sonilo music cues for THE VAULTED SKY. Skips existing files."""
import re
import subprocess
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "music"
OUT.mkdir(exist_ok=True)

CUES = [
    ("mus_womb", 60,
     "Submerged amniotic ambient: soft underwater piano notes far away, warm "
     "amber drones, slow gentle pulses like a heartbeat monitor, womb-like and "
     "strange and tender. Background ambience, very quiet, no drums, no melody "
     "beyond fragments. Instrumental only, no vocals."),
    ("mus_fuji", 45,
     "A single warm intimate piano motif, simple and kind, like a handwritten "
     "note left for a lonely child; sparse notes, long pauses, quiet hope "
     "inside sadness. Solo piano. Instrumental only, no vocals."),
    ("mus_lies", 60,
     "Cold slow ambient unease: glassy frozen textures, a distant slow pulse, "
     "muted dissonant strings under the surface, a decade of quiet captivity, "
     "patient and bitter. Background ambience, no drums. Instrumental only, "
     "no vocals."),
    ("mus_sky", 45,
     "Overwhelming orchestral release: quiet trembling strings burst into a "
     "vast soaring swell with harp and horns, terror and rapture at seeing an "
     "endless sky for the first time, tears of joy, enormous and tender. "
     "Instrumental only, no vocals."),
    ("mus_machine", 60,
     "Low ominous corporate dread drone: deep sub bass, slow ticking metallic "
     "pulses like a clock, faint dissonant strings, polite menace in a "
     "windowless room. Background ambience, no melody, no drums. Instrumental "
     "only, no vocals."),
    ("mus_tulpa", 45,
     "Uncanny interior whisper-scape: detuned music-box notes, reversed "
     "breathy textures, soft overlapping echoes circling the ears, a mind "
     "talking to itself in the dark, unsettling but delicate. Background "
     "ambience, no drums. Instrumental only, no vocals."),
    ("mus_quake", 45,
     "Rising catastrophe drone: deep earth rumbles, alarms muffled through "
     "concrete, accelerating low pulses, red emergency light in sound form, "
     "dread building to a verge. Background ambience, no melody. Instrumental "
     "only, no vocals."),
    ("mus_escape", 75,
     "Relentless escape chase: driving low taiko and electronic percussion, "
     "surging dark strings, wind and velocity, a hunted creature flying for "
     "its life over a dark ocean, urgent and thrilling. Instrumental only, "
     "no vocals."),
    ("mus_stars", 75,
     "Weightless starlit ambient: vast quiet space pads, a fragile warm piano "
     "fragment drifting in and out, grief dissolving into freedom under an "
     "endless night sky, slow and floating and finally at peace. Instrumental "
     "only, no vocals."),
    ("mus_unown", 40,
     "Alien sacred wonder: hundreds of glassy chiming harmonics like tuning "
     "forks in slow rotating rings, choir-like shimmer without voices, "
     "beautiful and vast and faintly wrong. Instrumental only, no vocals."),
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
