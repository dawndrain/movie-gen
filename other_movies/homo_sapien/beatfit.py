#!/usr/bin/env python3
"""Land a clip's KEY MOMENT on a musical beat — without regenerating anything.

    python3 beatfit.py s02_two_dance --anchor settle

Seedance never hears the audio, so any apparent sync in a raw clip is luck (and
mostly the viewer's brain snapping near-periodic motion onto a strong pulse —
measured, our clips sit 14–30% off the song's pulse). Real sync is an EDIT
problem with two free levers, and no regeneration:

  1. OFFSET — where inside the generated clip the cut window starts. We generate
     ~2s longer than the cut precisely so there is slack to slide.
  2. RATE   — play a few percent faster/slower (setpts). Under ~8% this is
     invisible on human motion but retimes the whole clip.

WHAT NOT TO DO: cross-correlating the clip's raw motion energy against the song's
onset envelope. Tried it; it barely moves the needle (-0.05 -> +0.01) because a
person walking across a room is ONE long smooth motion, not a train of hits —
there is nothing for the correlation to grab, and the optimiser happily throws
away the first two seconds (and the whole entrance) chasing noise.

WHAT WORKS is what a human editor does: pick the ONE moment that matters — the
accent — and put it exactly on a beat. Everything else follows. Here the accent
is the "settle": the instant the movement stops because they've come together,
i.e. the forehead touch. We find the beat grid, find the settle, and solve for
the (offset, rate) that drops one onto the other while preserving the opening.
"""
import argparse
import importlib.util
import subprocess
import wave
from pathlib import Path

import numpy as np

PROJ = Path(__file__).parent
V1 = PROJ / "outputs/video1"
AUDIO = PROJ / "audio/homo_sapien.m4a"
OUT = PROJ / "outputs/previews"

spec = importlib.util.spec_from_file_location("sg", PROJ / "storyboard_gen.py")
sg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sg)
SHOTS = [s for s in sg.SHOTS if s[0] != "__act"]

AR, AHZ, VHZ = 8000, 100, 24


def onset_envelope(t0, dur):
    subprocess.run(["ffmpeg", "-y", "-v", "quiet", "-ss", f"{t0}", "-t", f"{dur}",
                    "-i", str(AUDIO), "-ac", "1", "-ar", str(AR),
                    "-f", "wav", "/tmp/bf.wav"], check=True)
    w = wave.open("/tmp/bf.wav")
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
    hop = AR // AHZ
    rms = np.array([np.sqrt((a[i*hop:(i+1)*hop]**2).mean())
                    for i in range(len(a) // hop)])
    env = np.maximum(0, np.diff(rms))
    return env / (env.max() or 1)


def beat_grid(env, bpm_lo=90, bpm_hi=140):
    """Tempo + phase: the times (s, relative to window start) the beats fall on."""
    e = env - env.mean()
    ac = np.correlate(e, e, "full")[len(e)-1:]
    ac = ac / (ac[0] or 1)
    lags = np.arange(1, len(ac)) / AHZ
    bpms = 60 / lags
    m = (bpms >= bpm_lo) & (bpms <= bpm_hi)
    v = ac[1:][m]
    period = 60 / bpms[m][int(np.argmax(v))]          # seconds per beat
    # phase: slide a pulse train, keep the phase with the most onset energy on it
    best, phase = -1, 0.0
    for ph in np.arange(0, period, 1 / AHZ):
        ts = np.arange(ph, len(env) / AHZ, period)
        idx = (ts * AHZ).astype(int)
        idx = idx[idx < len(env)]
        s = env[idx].sum() / max(len(idx), 1)
        if s > best:
            best, phase = s, ph
    return period, np.arange(phase, len(env) / AHZ, period)


def motion_envelope(clip):
    p = subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(clip),
                        "-vf", f"scale=96:54,format=gray,fps={VHZ}",
                        "-f", "rawvideo", "-"], capture_output=True)
    fr = np.frombuffer(p.stdout, dtype=np.uint8).reshape(-1, 54, 96).astype(float)
    m = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    m = m - m.min()
    return m / (m.max() or 1)


def find_settle(mot):
    """The accent: where sustained movement ENDS — they come together and stop."""
    k = int(0.35 * VHZ)
    sm = np.convolve(mot, np.ones(k) / k, mode="same")
    thr = 0.45 * sm.max()
    moving = sm > thr
    last = np.where(moving)[0]
    if len(last) == 0:
        return len(mot) / VHZ
    return (last[-1] + 1) / VHZ            # first quiet frame after the last big move


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shot")
    ap.add_argument("--max-rate", type=float, default=1.08)
    ap.add_argument("--keep-head", type=float, default=0.5,
                    help="max seconds to trim off the front (protects the entrance)")
    args = ap.parse_args()

    i = next(i for i, s in enumerate(SHOTS) if s[0] == args.shot)
    name, tin = SHOTS[i][0], SHOTS[i][1]
    tnext = SHOTS[i+1][1] if i + 1 < len(SHOTS) else 239.0
    win = tnext - tin

    clip = V1 / f"{name}.mp4"
    src = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of", "default=nw=1:nk=1", str(clip)],
                               capture_output=True, text=True).stdout)

    env = onset_envelope(tin, win)
    period, beats = beat_grid(env)
    mot = motion_envelope(clip)
    settle = find_settle(mot)

    print(f"{name}: window {tin:.1f}–{tnext:.1f}s ({win:.1f}s), source {src:.2f}s")
    print(f"  song here: {60/period:.1f} BPM, beat every {period:.3f}s")
    print(f"  beats at (song time): " +
          ", ".join(f"{tin+b:.2f}" for b in beats if b < win))
    print(f"  clip accent (they come together, motion stops): {settle:.2f}s into the clip")
    print(f"  currently lands at song {tin + settle:.2f}s")

    # solve: played(settle) = (settle - off)/rate  must equal some beat b
    cands = []
    for rate in np.arange(1/args.max_rate, args.max_rate + 1e-9, 0.002):
        for b in beats:
            if not (0.5 < b < win - 0.15):
                continue
            off = settle - b * rate
            if not (0 <= off <= min(args.keep_head, src - win * rate)):
                continue
            cands.append((abs(rate - 1) + 0.35 * off, off, rate, b))
    if not cands:
        print("\n  no fit inside the rate/head limits — loosen --keep-head or --max-rate")
        return
    _, off, rate, b = min(cands)

    print(f"\n  FIT: trim {off:.3f}s off the front, play at {rate:.3f}× "
          f"({(rate-1)*100:+.1f}%, invisible)")
    print(f"       → the forehead touch now lands on the beat at song {tin+b:.2f}s")

    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"beatfit_{name}.mp4"
    vf = (f"trim={off:.3f}:{off + win*rate:.3f},setpts=(PTS-STARTPTS)/{rate:.4f},"
          f"scale=854:480,setsar=1,fps={VHZ}")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip),
                    "-ss", f"{tin}", "-t", f"{win}", "-i", str(AUDIO),
                    "-filter_complex", f"[0:v]{vf}[v]", "-map", "[v]", "-map", "1:a",
                    "-t", f"{win}", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "19", "-c:a", "aac", str(dest)], check=True)
    print(f"  preview: {dest}")
    print(f"\n  assembler entry: ({name!r}, trim_start={off:.3f}, rate={rate:.3f})")


if __name__ == "__main__":
    main()
