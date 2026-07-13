#!/usr/bin/env python3
"""Build the ANIMATIC — v0 of the film, before a single video credit is spent.

Every Nano Banana start frame, held for exactly its cut window, hard-cutting on
the beat of the real master track, with the lyrics burned over the top. This is
how you find out whether the edit works before paying Seedance to animate it.

    python3 animatic.py            -> outputs/previews/animatic_v1.mp4

Shot timings come from storyboard_gen.SHOTS (single source of truth); the lyric
timings come from the whisper word-timestamps in lyrics_timed.md.
"""
import argparse
import importlib.util
import subprocess
from pathlib import Path

PROJ = Path(__file__).parent
FRAMES = PROJ / "frames"
AUDIO = PROJ / "audio/homo_sapien.m4a"
OUT = PROJ / "outputs/previews"
WORK = PROJ / "outputs/_animatic"

spec = importlib.util.spec_from_file_location("sg", PROJ / "storyboard_gen.py")
sg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sg)
SHOTS = [s for s in sg.SHOTS if s[0] != "__act"]

# (start, end, text) — the sung lyric, on the beat. Corrected against the release;
# whisper mishears "Homo Sapien" as "home, I'll stay behind".
LYRICS = [
    (17.5, 21.4, "First there was the big bang"),
    (21.5, 25.5, "and stars began to shine"),
    (25.6, 33.4, "Then there was existence, primordial slime"),
    (34.9, 41.2, "How I was waiting all that time"),
    (42.8, 50.3, "While we were evolving side by side"),
    (51.5, 54.6, "Rock to fish, monkey to man"),
    (55.5, 59.5, "It's why this love begun"),

    (60.5, 63.6, "Be my Homo Sapien"),
    (64.5, 67.6, "'Cause I evolved to love you"),
    (68.5, 71.6, "Let me hold you till the end"),
    (72.5, 76.5, "'Cause I evolved to love you"),
    (77.5, 80.7, "We will grow and change, my friend"),
    (81.5, 84.6, "But I'll evolve to love you"),
    (85.5, 89.5, "So be my Homo Sapien"),
    (90.5, 95.5, "'Cause I evolved to, I evolved to love you"),

    (103.8, 110.3, "We formed and mutated over time"),
    (111.7, 119.4, "We hunted and gathered, and played with fire"),
    (120.7, 127.4, "Every evolution, every step was divine"),

    (128.5, 132.5, "Be my Homo Sapien"),
    (133.5, 136.6, "'Cause I evolved to love you"),
    (137.5, 140.6, "Let me hold you till the end"),
    (141.5, 144.6, "'Cause I evolved to love you"),
    (145.5, 149.6, "We will grow and change, my friend"),
    (150.5, 153.6, "But I'll evolve to love you"),
    (154.5, 157.6, "So be my Homo Sapien"),
    (158.5, 164.4, "'Cause I evolved to, I evolved to love you"),

    (166.2, 174.0, "And procreate with you"),
    (175.5, 179.5, "Let's continue the species"),
    (184.5, 187.5, "Expand our family tree"),

    (214.5, 217.6, "So be my Homo Sapien"),
    (218.6, 225.4, "'Cause I evolved to, I evolved to love you"),
]


def srt_time(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


W, H, FPS = 1280, 720, 24
SS = 2          # work at 2x, then downscale — see kenburns()

# Per-shot Ken Burns moves. Kept SMALL (3-5% over the whole window) — this should
# read as the film breathing, not as a camera move. Direction alternates so the
# cut rhythm doesn't feel mechanical; a few shots are deliberately LOCKED OFF
# (move=None) because they are about stillness and a drift would fight them.
KB = {
    "s07_waiting": None,          # the joke is that it does not move
    "s19_handprints": None,       # reverent; hold it
    "s36_glass_handprints": None, # "do not move the camera" — the whole point
    "s40b_earth": None,           # holds until the track fades
}
DEFAULT_MOVES = ["in", "out"]     # alternate for everything else


def kenburns(idx, name, dur):
    """One shot's Ken Burns move — or a plain hold.

    THE QUIVER BUG, and the actual fix.

    zoompan is the wrong tool. It TRUNCATES the crop origin to INTEGER pixels, so
    on a slow move the true origin advances a fraction of a pixel per frame, sits
    on one integer for several frames, then SNAPS a whole pixel. That snap is the
    quiver, and it is worst on slow zooms — i.e. exactly on Ken Burns. (Its usual
    z='min(zoom+0.001,1.1)' form is broken too: with d=1 the `zoom` accumulator
    RESETS every input frame, so it never accumulates — you get a static image
    that merely jerks. Measured: mean motion 0.000, variability 454%.)

    Supersampling before zoompan only shrinks the quantum (1/4 px at 4x); it never
    removes it. The RIGHT answer is continuous resampling: for each output pixel
    at time t, sample the source at an exact FRACTIONAL coordinate with a proper
    kernel — no integer grid anywhere. `perspective` does this: float corner
    coordinates, re-evaluated per frame (eval=frame), cubic interpolation.

    Measured frame-to-frame roughness on the same shot and move (lossless):
        zoompan 1x   162%   (73/168 snap frames)
        zoompan 4x    24%   ( 0/168)
        perspective  0.3%   ( 0/168)
    0.3% is encoder noise. This is smooth, not "smoother".

    Cost: the full 43-shot render goes 3:02 -> 5:56. Roughly 2x slower, and worth
    it — but that IS the tradeoff, so don't pretend otherwise.

    We work at 2x and downscale, which costs little and adds a clean box-average
    on top of the cubic sample.
    """
    n = max(int(round(dur * FPS)), 2)
    if name in KB and KB[name] is None:
        return (f"[{idx}:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
                f"crop={W}:{H},setsar=1,fps={FPS},trim=duration={dur:.3f},"
                f"setpts=PTS-STARTPTS[v{idx}];")

    move = DEFAULT_MOVES[idx % len(DEFAULT_MOVES)]
    amt = 0.045
    # z(t): the zoom factor at output frame `on`, computed fresh each frame.
    z = (f"(1+{amt}*on/{n-1})" if move == "in"
         else f"({1+amt}-{amt}*on/{n-1})")
    # The source rectangle to sample, in float pixels, centred: W/z by H/z.
    l, r = f"(W-W/{z})/2", f"(W+W/{z})/2"
    t, b = f"(H-H/{z})/2", f"(H+H/{z})/2"
    return (
        f"[{idx}:v]scale={W*SS}:{H*SS}:force_original_aspect_ratio=increase,"
        f"crop={W*SS}:{H*SS},fps={FPS},"
        f"perspective=eval=frame:interpolation=cubic:"
        f"x0='{l}':y0='{t}':x1='{r}':y1='{t}':"
        f"x2='{l}':y2='{b}':x3='{r}':y3='{b}',"
        f"scale={W}:{H},setsar=1,trim=duration={dur:.3f},"
        f"setpts=PTS-STARTPTS[v{idx}];")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kenburns", action="store_true",
                    help="slow 4.5%% push on each still (quiver-free; see kenburns())")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)

    # --- subtitle track: the lyrics, on the beat ---
    srt = WORK / "lyrics.srt"
    srt.write_text("".join(
        f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n\n"
        for i, (a, b, txt) in enumerate(LYRICS, 1)))

    # --- picture: each frame held for exactly its cut window ---
    missing = [n for n, *_ in SHOTS if not (FRAMES / f"{n}.png").exists()]
    if missing:
        raise SystemExit(f"missing frames: {missing}")

    # Each frame is held from its own in-point until the NEXT shot's in-point.
    # Using (out - in) instead would let any gap between windows collapse, and
    # concat has no timeline — every later cut would slide early and drift off
    # the beat. The song is the clock; the picture fills whatever it's given.
    END = 239.0
    plan = []
    for i, (name, tin, _tout, *_) in enumerate(SHOTS):
        nxt = SHOTS[i + 1][1] if i + 1 < len(SHOTS) else END
        plan.append((name, nxt - tin))

    style = ("FontName=Helvetica,FontSize=25,PrimaryColour=&H00FFFFFF,"
             "OutlineColour=&HC0000000,BorderStyle=1,Outline=2,Shadow=1,"
             "Alignment=2,MarginV=42,Bold=1")
    subs = f"subtitles='{srt.as_posix()}':force_style='{style}'"

    dest = Path(args.out) if args.out else OUT / (
        "animatic_v2_kenburns.mp4" if args.kenburns else "animatic_v1.mp4")

    if not args.kenburns:
        listfile = WORK / "images.txt"
        listfile.write_text("\n".join(
            f"file '{(FRAMES / f'{n}.png').as_posix()}'\nduration {d:.3f}"
            for n, d in plan) + f"\nfile '{(FRAMES / f'{plan[-1][0]}.png').as_posix()}'\n")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats",
               "-f", "concat", "-safe", "0", "-i", str(listfile),
               "-i", str(AUDIO),
               "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},fps={FPS},format=yuv420p,{subs}",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
               "-c:a", "aac", "-b:a", "192k", "-shortest", str(dest)]
    else:
        # One input per shot: the concat demuxer can't run a per-image filter, and
        # zoompan needs each still as its own stream.
        inputs, parts = [], []
        for i, (name, dur) in enumerate(plan):
            inputs += ["-loop", "1", "-t", f"{dur:.3f}",
                       "-i", str(FRAMES / f"{name}.png")]
            parts.append(kenburns(i, name, dur))
        graph = ("".join(parts)
                 + "".join(f"[v{i}]" for i in range(len(plan)))
                 + f"concat=n={len(plan)}:v=1:a=0[cat];"
                 + f"[cat]format=yuv420p,{subs}[vout]")
        gfile = WORK / "kb_graph.txt"
        gfile.write_text(graph)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats", *inputs,
               "-i", str(AUDIO),
               "-filter_complex_script", str(gfile),
               "-map", "[vout]", "-map", f"{len(plan)}:a",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
               "-c:a", "aac", "-b:a", "192k", "-shortest", str(dest)]

    n_moving = sum(1 for n, _ in plan if KB.get(n, "move") is not None)
    print(f"{len(plan)} shots"
          + (f", {n_moving} with a slow push, {len(plan)-n_moving} locked off"
             if args.kenburns else ", hard stills"))
    subprocess.run(cmd, check=True)
    print(dest)


if __name__ == "__main__":
    main()
