#!/usr/bin/env python3
"""Transcribe every v1 clip with whisper-cli and diff against the expected lines.
Flags: missing dialogue, extra/narrator speech, garbled words.
Usage: python3 qc_transcripts.py [outputs/v1]"""
import re
import subprocess
import sys
from pathlib import Path

from vo_vs import LINES

HERE = Path(__file__).parent
CLIPS = HERE / (sys.argv[1] if len(sys.argv) > 1 else "outputs/v1")
MODEL = HERE.parent / ".whisper/ggml-small.en.bin"

SILENT = {"a2", "e3", "f1", "f5", "g1", "g4", "title"}


def norm(s):
    s = s.lower()
    s = re.sub(r"mew[\s\-]*two|mew\s*2|mu\s*two", "mewtwotoken", s)
    s = re.sub(r"maz[\s\-]*dah?|mazda", "mazdatoken", s)
    s = re.sub(r"grou?[\s\-]*don", "groudontoken", s)
    s = re.sub(r"poke[\s\-]*mon|pokemon", "pokemontoken", s)
    s = re.sub(r"two point three five one|2\.351|two three five one",
               "designationtoken", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return [w for w in s.split() if w]


def wer(ref, hyp):
    d = [[i + j if i * j == 0 else 0 for j in range(len(hyp) + 1)]
         for i in range(len(ref) + 1)]
    for i in range(1, len(ref) + 1):
        for j in range(1, len(hyp) + 1):
            d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1,
                          d[i-1][j-1] + (ref[i-1] != hyp[j-1]))
    return d[len(ref)][len(hyp)] / max(1, len(ref))


results = []
for clip in sorted(CLIPS.glob("*.mp4")):
    shot = clip.stem
    if shot in SILENT:
        continue
    if shot not in LINES:
        continue
    expected = " ".join(t for _, t in LINES[shot])
    wav = Path("/tmp") / f"_qc_{shot}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(clip),
                    "-vn", "-ar", "16000", "-ac", "1", str(wav)])
    r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-np", str(wav)],
                       capture_output=True, text=True)
    hyp = re.sub(r"\[.*?-->.*?\]", "", r.stdout).replace("\n", " ")
    e = wer(norm(expected), norm(hyp))
    flag = "OK " if e < 0.25 else ("~  " if e < 0.5 else "BAD")
    results.append((flag, shot, e, hyp.strip()[:160]))
    print(f"{flag} {shot:5s} wer={e:.2f}  {hyp.strip()[:120]}", flush=True)

bad = [r for r in results if r[0] != "OK "]
print(f"\n{len(results)} checked, {len(bad)} flagged")
for flag, shot, e, hyp in bad:
    print(f"  {flag} {shot} wer={e:.2f}")
