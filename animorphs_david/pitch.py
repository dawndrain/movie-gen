#!/usr/bin/env python3
"""Median-F0 report for every audio file in a directory (voice-audition tool).
Usage: python3 pitch.py <dir-or-files...>
Autocorrelation pitch on voiced 40ms windows; prints median + IQR per file."""
import subprocess
import sys
from pathlib import Path

import numpy as np

SR = 16000


def f0_stats(path: Path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR),
         "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
    if len(x) < SR // 2:
        return None
    x /= (np.abs(x).max() + 1e-9)
    win, hop = int(0.04 * SR), int(0.02 * SR)
    fmin, fmax = 55, 400
    lo, hi = SR // fmax, SR // fmin
    f0s = []
    energies = [np.sqrt(np.mean(x[s:s + win] ** 2))
                for s in range(0, len(x) - win, hop)]
    thresh = 0.35 * np.median([e for e in energies if e > 0.005] or [1])
    for i, s in enumerate(range(0, len(x) - win, hop)):
        seg = x[s:s + win]
        if energies[i] < max(thresh, 0.01):
            continue
        seg = seg - seg.mean()
        ac = np.correlate(seg, seg, "full")[win - 1:]
        ac /= (ac[0] + 1e-12)
        r = ac[lo:hi]
        k = int(np.argmax(r))
        if r[k] < 0.5:          # voicing confidence
            continue
        f0s.append(SR / (lo + k))
    if len(f0s) < 8:
        return None
    f0s = np.array(f0s)
    return np.median(f0s), np.percentile(f0s, 25), np.percentile(f0s, 75), len(f0s)


if __name__ == "__main__":
    files = []
    for a in sys.argv[1:]:
        p = Path(a)
        files += sorted(p.glob("*.mp3")) + sorted(p.glob("*.m4a")) if p.is_dir() else [p]
    rows = []
    for f in files:
        st = f0_stats(f)
        if st:
            rows.append((st[0], f"{f.stem:28s} median {st[0]:5.0f} Hz  IQR {st[1]:.0f}-{st[2]:.0f}  ({st[3]} frames)"))
        else:
            rows.append((0, f"{f.stem:28s} (unvoiced/too short)"))
    for _, line in sorted(rows):
        print(line)
