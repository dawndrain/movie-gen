#!/usr/bin/env python3
"""Assemble the film from real Seedance clips + Lenka's master track.

    python3 assemble_v1.py              # whatever clips exist in outputs/video1
    python3 assemble_v1.py --to 60.5    # just the first minute

Every clip is MUTED (Seedance's own audio would fight the vocal) and the master
track is laid over the whole timeline. Shots are placed at their ABSOLUTE
in-points from storyboard_gen.SHOTS — the song is the clock. A clip shorter than
its window freezes on its last frame to fill the gap; a longer one is trimmed.
Shots with no clip yet fall back to their Nano Banana start frame, so this runs
happily on a partial film.
"""
import argparse
import importlib.util
import subprocess
from pathlib import Path

PROJ = Path(__file__).parent
FRAMES = PROJ / "frames"
V1 = PROJ / "outputs/video1"
AUDIO = PROJ / "audio/homo_sapien.m4a"
OUT = PROJ / "outputs/previews"
WORK = PROJ / "outputs/_assemble"

spec = importlib.util.spec_from_file_location("sg", PROJ / "storyboard_gen.py")
sg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sg)
SHOTS = [s for s in sg.SHOTS if s[0] != "__act"]

END = 239.0
W, H, FPS = 854, 480, 24

# Beat fits from beatfit.py: {shot: (trim_start, rate)}. Seedance never hears the
# song, so sync is an edit-time job — slide the clip inside its window and retime
# it a few percent so the shot's ACCENT lands on a beat. <8% speed is invisible.
FITS = {
    # s01 gave a second to s02 (window is now 6.0-13.0) so the embrace has room to
    # land and be HELD rather than arriving on the cut. This fit puts the forehead
    # touch on the beat at 11.67s, leaving ~1.3s of them just holding it.
    "s02_two_dance": (0.001, 1.036),
}

ap = argparse.ArgumentParser()
ap.add_argument("--to", type=float, default=END, help="stop at this timestamp")
ap.add_argument("--out", default=None)
ap.add_argument("--master", action="store_true",
                help="1080p YouTube master from outputs/video1_1080 (upscale.py)")
args = ap.parse_args()

if args.master:
    V1 = PROJ / "outputs/video1_1080"
    W, H = 1920, 1080

OUT.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)

# window for each shot: its in-point until the next shot's in-point
plan = []
for i, (name, tin, _tout, *_) in enumerate(SHOTS):
    nxt = SHOTS[i + 1][1] if i + 1 < len(SHOTS) else END
    if tin >= args.to:
        break
    plan.append((name, tin, min(nxt, args.to) - tin))

inputs, parts, labels = [], [], []
for i, (name, tin, win) in enumerate(plan):
    clip = V1 / f"{name}.mp4"
    if clip.exists():
        off, rate = FITS.get(name, (0.0, 1.0))
        inputs += ["-i", str(clip)]
        # slide + retime to land the accent on the beat, then trim to the window;
        # if the clip still falls short, tpad freezes its last frame to fill.
        parts.append(
            f"[{i}:v]trim={off:.3f}:{off + win*rate:.3f},"
            f"setpts=(PTS-STARTPTS)/{rate:.4f},"
            f"scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},setsar=1,fps={FPS},"
            f"tpad=stop_mode=clone:stop_duration={win:.3f},"
            f"trim=0:{win:.3f},setpts=PTS-STARTPTS[v{i}];")
    else:  # no clip yet — hold the start frame
        inputs += ["-loop", "1", "-t", f"{win:.3f}", "-i", str(FRAMES / f"{name}.png")]
        parts.append(
            f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},setsar=1,fps={FPS},trim=0:{win:.3f},"
            f"setpts=PTS-STARTPTS[v{i}];")
    labels.append(f"[v{i}]")

graph = "".join(parts) + "".join(labels) + f"concat=n={len(plan)}:v=1:a=0[vout]"
gfile = WORK / "graph.txt"
gfile.write_text(graph)

dest = Path(args.out) if args.out else OUT / (
    "homo_sapien_1080p.mp4" if args.master else
    f"v1_first{int(args.to)}s.mp4" if args.to < END else "v1_full.mp4")

if args.master:
    # YouTube master: high-quality H.264, yuv420p, +faststart, AAC 320k.
    # Lenka's master track is copied through untouched apart from the AAC encode —
    # the picture is upscaled per-clip, never the finished film, so the audio is
    # only ever encoded once.
    venc = ["-c:v", "libx264", "-preset", "slow", "-crf", "17",
            "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.1",
            "-movflags", "+faststart", "-c:a", "aac", "-b:a", "320k", "-ar", "48000"]
else:
    venc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k"]

cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats", *inputs,
       "-i", str(AUDIO),
       "-filter_complex_script", str(gfile),
       "-map", "[vout]", "-map", f"{len(plan)}:a",   # audio = the master, clips muted
       "-t", f"{args.to:.3f}", *venc, str(dest)]
print(f"{len(plan)} shots, {sum(1 for n,_,_ in plan if (V1/f'{n}.mp4').exists())} with clips")
subprocess.run(cmd, check=True)
print(dest)
