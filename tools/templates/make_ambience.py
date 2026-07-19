#!/usr/bin/env python3
# TEMPLATE — copied from other_movies/carl/make_ambience.py (ambience beds (ElevenLabs sound-gen -> EQ -> stitch -> loudnorm)).
# Project-specific: expects that film's spec/paths. Copy into a new film
# folder and adapt; the original in other_movies/carl/ is the working example.
"""Ambience beds for DUNGEON CRAWLER CARL via ElevenLabs sound-generation.

Playbook recipe: 22s texture -> EQ (highpass 100 / lowpass 7k, kills the baked-in
HF whine) -> crossfade-stitch to ~300s loop -> loudnorm to -30 LUFS.
Usage: python3 make_ambience.py          (skips existing beds; re-run = retry)
"""
import json
import subprocess
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
AMB = HERE / "ambience"
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()

# name -> prompt. Textures only, steady, no events; name what NOT to include.
BEDS = {
    "suburb_night": (
        "Cold night wind over a flattened suburban ruin, distant creaking of "
        "settling debris, faint dust hiss, very sparse and desolate. Steady "
        "seamless loop, no sudden events, no voices, no sirens, no music, "
        "no birds, no crickets."),
    "dungeon_corridor": (
        "Vast underground stone dungeon corridor room tone: deep hollow air, "
        "faint distant drips of water, a very low stone rumble, subtle cave "
        "reverb. Steady seamless loop, no sudden events, no voices, no "
        "footsteps, no music, no monsters."),
    "safe_room": (
        "Cozy quiet tavern interior room tone: soft fireplace crackle, faint "
        "kitchen hum, gentle warm air. Steady seamless loop, no sudden events, "
        "no voices, no dishes clattering, no music."),
    "goblin_caves": (
        "Echoing cave system with faint dripping water, distant skittering, a "
        "low ominous air rumble, sparse. Steady seamless loop, no sudden "
        "events, no voices, no music, no screeches."),
    "boss_arena": (
        "Huge underground arena room tone: deep sub rumble, cavernous hollow "
        "air, faint metallic groans far away. Steady seamless loop, no sudden "
        "events, no voices, no crowd, no music."),
    "studio_crowd": (
        "Large indoor television-studio audience bed: a low continuous murmur "
        "of a big excited crowd, soft air-conditioned room tone. Steady "
        "seamless loop, no applause bursts, no laughter spikes, no "
        "intelligible words, no music."),
}

TARGET_LEN = 300.0
SRC_LEN = 22.0
XFADE = 2.0


def gen_bed(name: str, prompt: str) -> Path:
    raw = AMB / f"{name}_raw.mp3"
    if not raw.exists():
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/sound-generation",
            data=json.dumps({"text": prompt,
                             "duration_seconds": SRC_LEN,
                             "prompt_influence": 0.4}).encode(),
            headers={"xi-api-key": KEY, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            raw.write_bytes(r.read())
        print(f"gen  {raw.name}")
    return raw


def process(name: str) -> None:
    out = AMB / f"{name}_loop.m4a"
    if out.exists():
        print(f"skip {out.name}")
        return
    raw = gen_bed(name, BEDS[name])
    eq = AMB / f"{name}_eq.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
                    "-af", "highpass=f=100,lowpass=f=7000", str(eq)], check=True)
    # crossfade-stitch copies of the eq'd bed up to TARGET_LEN
    import math
    n = math.ceil((TARGET_LEN - XFADE) / (SRC_LEN - XFADE)) + 1
    inputs, fc = [], []
    for i in range(n):
        inputs += ["-i", str(eq)]
    cur = "[0:a]"
    for i in range(1, n):
        lab = f"[x{i}]" if i < n - 1 else "[out]"
        fc.append(f"{cur}[{i}:a]acrossfade=d={XFADE}:c1=tri:c2=tri{lab}")
        cur = lab
    fc.append(f"[out]atrim=duration={TARGET_LEN},"
              f"loudnorm=I=-30:TP=-3:LRA=7[fin]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs,
                    "-filter_complex", ";".join(fc).replace("[out]atrim", "[out]atrim"),
                    "-map", "[fin]", "-c:a", "aac", "-b:a", "160k", str(out)],
                   check=True)
    eq.unlink(missing_ok=True)
    print(f"OK   {out.name}")


if __name__ == "__main__":
    AMB.mkdir(exist_ok=True)
    for name in BEDS:
        process(name)
