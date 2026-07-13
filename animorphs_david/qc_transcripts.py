#!/usr/bin/env python3
"""Transcribe every dv1 clip with whisper-cli and diff against the expected lines.
Flags: missing dialogue, extra/narrator speech, garbled words. Usage: python3 qc_transcripts.py"""
import re
import subprocess
from pathlib import Path

from vo_david import LINES

HERE = Path(__file__).parent
CLIPS = HERE / "outputs/dv1"
MODEL = HERE.parent / ".whisper/ggml-small.en.bin"

# sub-shot -> (parent LINES key slices) for split shots
SPLITS = {
    "a4a": [("a4", 0, 2)], "a4b": [("a4", 2, 4)],
    "b2a": [("b2", 0, 1)], "b2b": [("b2", 1, 2)],
    "b4a": [("b4", 0, 1)], "b4b": [("b4", 1, 2)],
    "c1a": [("c1", 0, 1)], "c1b": [("c1", 1, 2)],
    "c2a": [("c2", 0, 1)], "c2b": [("c2", 1, 2)],
    "c4a": [("c4", 0, 1)], "c4b": [("c4", 1, 3)],
}
SILENT = {"a1", "a3", "a5", "a8", "b3", "b5", "b7b", "c3", "c13"}


def norm(s):
    s = s.lower()
    s = re.sub(r"yee?[\s\-]*erk\w*|yeerk\w*", "YK", s)
    s = re.sub(r"ell?[\s\-]*fan[\s\-]*gor\w*|elfangor\w*", "EG", s)
    s = re.sub(r"ess?[\s\-]*k[au]h?[\s\-]*fill?\w*|escafil\w*", "EF", s)
    s = s.replace("YK", "yktoken").replace("EG", "egtoken").replace("EF", "eftoken")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return [w for w in s.split() if w]


def wer(ref, hyp):
    d = [[i + j if i * j == 0 else 0 for j in range(len(hyp) + 1)] for i in range(len(ref) + 1)]
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
    hyp = re.sub(r"\[.*?-->.*?\]", "", r.stdout).replace("\n", " ")
    e = wer(norm(expected), norm(hyp))
    flag = "OK " if e < 0.25 else ("~  " if e < 0.5 else "BAD")
    results.append((flag, shot, e, hyp.strip()[:160]))
    print(f"{flag} {shot:4s} wer={e:.2f}  {hyp.strip()[:120]}", flush=True)

bad = [r for r in results if r[0] != "OK "]
print(f"\n{len(results)} checked, {len(bad)} flagged")
for flag, shot, e, hyp in bad:
    print(f"  {flag} {shot} wer={e:.2f}")
