#!/usr/bin/env python3
"""Estimate mean speaking pitch (fundamental frequency) of a clip's dialogue.
Rough autocorrelation-based f0 on voiced frames. Adult male ~85-155 Hz,
adult female ~165-255 Hz, child ~250-320 Hz.
Usage: python3 pitch_check.py clip.mp4 [start] [dur]"""
import subprocess, sys
import numpy as np

path = sys.argv[1]
ss = ["-ss", sys.argv[2]] if len(sys.argv) > 2 else []
t = ["-t", sys.argv[3]] if len(sys.argv) > 3 else []
raw = subprocess.run(["ffmpeg", "-v", "error", *ss, "-i", path, *t, "-vn",
                      "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
sr, win, hop = 16000, 1024, 512
f0s = []
for i in range(0, len(x) - win, hop):
    fr = x[i:i + win]
    if np.sqrt((fr ** 2).mean()) < 0.02:   # skip silence/quiet ambience
        continue
    fr = fr - fr.mean()
    ac = np.correlate(fr, fr, "full")[win - 1:]
    lo, hi = sr // 400, sr // 70          # 70-400 Hz plausible speech f0
    seg = ac[lo:hi]
    if seg.size == 0 or ac[0] <= 0:
        continue
    peak = seg.argmax() + lo
    if ac[peak] / ac[0] > 0.35:           # voiced frame
        f0s.append(sr / peak)
f0s = np.array(f0s)
if f0s.size < 10:
    print(f"{path}: not enough voiced frames")
else:
    med = np.median(f0s)
    label = ("adult male" if med < 160 else
             "adult female / high male" if med < 250 else "CHILD-LIKE")
    print(f"{path}: median f0 = {med:.0f} Hz ({f0s.size} voiced frames) -> {label}")
