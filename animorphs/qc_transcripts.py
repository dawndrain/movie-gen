#!/usr/bin/env python3
"""Transcribe every hb2 clip with whisper-cli and diff against the expected lines.
Flags: missing dialogue, extra/narrator speech, garbled words. Usage: python3 qc_transcripts.py"""
import re
import subprocess
import sys
from pathlib import Path

from vo_hb2 import LINES

HERE = Path(__file__).parent
CLIPS = HERE / "outputs/hb2"
MODEL = HERE.parent / ".whisper/ggml-small.en.bin"

SPLITS = {"e1a": [("e1", 0, 1)], "e1b": [("e1", 1, 3)]}


def norm(s):
    s = s.lower()
    s = re.sub(r"hork[\s\-]*b\w+", "HB", s)      # any rendering of Hork-Bajir
    s = re.sub(r"kah?[\s\-]*waht?[\s\-]*noh?j\w*|kawatnoj", "KAW", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s.replace("HB", "hbtoken").replace("KAW", "kawtoken"))
    return [w for w in s.split() if w]


def wer(ref, hyp):
    # simple word error rate via edit distance
    d = [[i + j if i * j == 0 else 0 for j in range(len(hyp) + 1)] for i in range(len(ref) + 1)]
    for i in range(1, len(ref) + 1):
        for j in range(1, len(hyp) + 1):
            d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1,
                          d[i-1][j-1] + (ref[i-1] != hyp[j-1]))
    return d[len(ref)][len(hyp)] / max(1, len(ref))


results = []
clips = sorted(CLIPS.glob("*.mp4"))
for clip in clips:
    shot = clip.stem
    if shot == "a3":
        continue
    if shot in SPLITS:
        key, lo, hi = SPLITS[shot][0]
        expected = " ".join(t for _, t in LINES[key][lo:hi])
    elif shot in LINES:
        expected = " ".join(t for _, t in LINES[shot])
    else:
        continue
    wav = Path("/tmp") / f"_qc_{shot}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(clip),
                    "-vn", "-ar", "16000", "-ac", "1", str(wav)])
    r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-np", str(wav)],
                       capture_output=True, text=True)
    hyp = " ".join(re.sub(r"\[.*?\]", "", ln).strip()
                   for ln in r.stdout.splitlines() if "-->" in ln or ln.strip())
    hyp = re.sub(r"\[.*?-->.*?\]", "", r.stdout).replace("\n", " ")
    e = wer(norm(expected), norm(hyp))
    flag = "OK " if e < 0.25 else ("~  " if e < 0.5 else "BAD")
    results.append((flag, shot, e, hyp.strip()[:160]))
    print(f"{flag} {shot:4s} wer={e:.2f}  {hyp.strip()[:120]}", flush=True)

bad = [r for r in results if r[0] != "OK "]
print(f"\n{len(results)} checked, {len(bad)} flagged")
for flag, shot, e, hyp in bad:
    print(f"  {flag} {shot} wer={e:.2f}")
