#!/usr/bin/env python3
"""Sonilo scratch music cues for the DCC animatic (specs in spec.MUSIC_CUES).
Each cue is downloaded then loudnorm'd to -30 LUFS so the assembler can treat
levels as plain dB offsets. Usage: python3 make_music.py  (skips existing)
"""
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from spec import MUSIC_CUES

HERE = Path(__file__).parent
MUS = HERE / "music"


def make(cue: str, prompt: str, dur: int) -> str:
    out = MUS / f"mus_{cue}.m4a"
    if out.exists():
        return f"skip {out.name}"
    err = ""
    for attempt in (1, 2, 3):
        res = subprocess.run(
            ["higgsfield", "generate", "create", "sonilo_music",
             "--prompt", prompt, "--duration", str(dur), "--wait"],
            capture_output=True, text=True)
        urls = re.findall(r"https://\S+\.(?:m4a|mp3|wav)", res.stdout + res.stderr)
        if urls:
            raw = MUS / f"mus_{cue}_raw.m4a"
            urllib.request.urlretrieve(urls[-1], raw)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
                            "-af", "loudnorm=I=-30:TP=-3:LRA=11",
                            "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
            return f"OK   {out.name}"
        err = (res.stdout + res.stderr).strip()[-200:]
        print(f"retry {cue} ({attempt}): {err}", flush=True)
    return f"FAIL {cue}: {err}"


if __name__ == "__main__":
    MUS.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = [pool.submit(make, c, p, d) for c, (p, d) in MUSIC_CUES.items()]
        for f in futs:
            print(f.result(), flush=True)
