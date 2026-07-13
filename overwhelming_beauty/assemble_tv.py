#!/usr/bin/env python3
"""Assemble THE VARIANCE first pass into outputs/preview_tv1.mp4.
Narrator VO is mixed on the GLOBAL timeline (can bridge cuts); music beds are
low; total silence under the bench scene."""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
DIRS = [HERE / "outputs/tv1"]  # later dirs win
MUS = HERE / "music"
VO = HERE / "vo"
OUT = HERE / "outputs/preview_tv1.mp4"


def pick(name):
    for d in reversed(DIRS):
        if (d / f"{name}.mp4").exists():
            return d / f"{name}.mp4"
    raise SystemExit(f"missing clip {name}")

# (clip, trim_start, trim_dur, mute, music_mark)
CUT = [
    ("t1", 0, None, False, "open"),
    ("t2", 0, None, False, "drawer"),
    ("t3", 0, None, False, None),
    ("t4", 0, None, False, None),
    ("t5", 0, None, False, None),
    ("t6", 0, None, False, "silence"),
    ("t7", 0, None, False, "drawer2"),
    ("t8", 0, None, False, None),
    ("t9", 0, None, False, None),
    ("t10", 0, None, False, None),
    ("t11a", 0, None, False, "silence"),
    ("t11b", 0, None, False, None),
    ("t12", 0, None, False, None),
    ("t13", 0, None, False, "alive"),
    ("t14", 0, None, False, None),
    ("t15", 0, None, False, None),
    ("t16a", 0, 5.2, False, "silence"),  # trim gibberish tail after the line
    ("t16b", 0, None, False, None),
    ("t17", 0, None, False, "collapse"),
    ("t18", 0, None, False, None),
    ("t19", 0, None, False, "silence"),
    ("t20a", 0, None, False, None),
    ("t20b", 0, None, False, None),
    ("t21", 0, None, False, "elegy"),
    ("t22", 0, None, False, None),
    ("t23", 0, None, False, None),
    ("t24", 0, None, False, None),
]

MUSIC = {  # mark -> (file, volume)
    "open": ("mus_baseline.m4a", 0.08),
    "drawer": ("mus_drawer.m4a", 0.10),
    "drawer2": ("mus_drawer.m4a", 0.07),
    "alive": ("mus_alive.m4a", 0.11),
    "collapse": ("mus_collapse.m4a", 0.11),
    "elegy": ("mus_elegy.m4a", 0.10),
}

# (vo file, shot, offset within shot, volume) — mixed on the global timeline
NARR = [
    ("n01_narr.mp3", "t1", 2.0, 1.0),
    ("n02_narr.mp3", "t3", 0.3, 1.0),
    ("n03_narr.mp3", "t5", 0.4, 1.0),
    ("n04_narr.mp3", "t8", 1.2, 1.0),
    ("n05_narr.mp3", "t10", 0.5, 1.0),
    ("n06_narr.mp3", "t13", 0.8, 1.0),
    ("n07_narr.mp3", "t17", 0.3, 1.0),
    ("n08_narr.mp3", "t18", 0.6, 1.0),
    ("n09_narr.mp3", "t21", 0.8, 1.0),
    ("n10_narr.mp3", "t22", 0.5, 1.0),
    ("n11_narr.mp3", "t24", 2.0, 1.0),
]


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


cut = [(pick(n), ts, td, m, mk) for n, ts, td, m, mk in CUT]
starts, total = {}, 0.0
for (path, ts, td, mute, mk), (name, *_) in zip(cut, CUT):
    d = td if td else dur(path) - ts
    starts[name] = (total, d)
    total += d

# music spans from marks
spans, cur = [], None
for name, *_rest in CUT:
    mk = _rest[-1]
    s = starts[name][0]
    if mk is not None:
        if cur:
            spans.append((cur[0], cur[1], s))
        cur = (mk, s)
spans.append((cur[0], cur[1], total))
spans = [(m, s, t) for (m, s, t) in spans if m in MUSIC]

inputs, fc = [], []
for i, (path, ts, td, mute, mk) in enumerate(cut):
    d = starts[CUT[i][0]][1]
    inputs += ["-i", str(path)]
    fc.append(f"[{i}:v]trim=start={ts}:end={ts + d:.3f},setpts=PTS-STARTPTS,"
              f"scale=854:480,setsar=1,fps=24[v{i}]")
    a = f"[{i}:a]atrim=start={ts}:end={ts + d:.3f},asetpts=PTS-STARTPTS,aresample=48000"
    if mute:
        a += ",volume=0"
    fc.append(a + f",apad,atrim=duration={d:.3f}[a{i}]")
n = len(cut)
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")

mix_labels = []
idx = n
for vof, shot, off, vol in NARR:
    at = starts[shot][0] + off
    inputs += ["-i", str(VO / vof)]
    fc.append(f"[{idx}:a]aresample=48000,volume={vol},"
              f"adelay={int(at * 1000)}|{int(at * 1000)},apad,"
              f"atrim=duration={total:.3f}[nv{idx}]")
    mix_labels.append(f"[nv{idx}]")
    idx += 1
for k, (mark, s, t) in enumerate(spans):
    f, vol = MUSIC[mark]
    inputs += ["-i", str(MUS / f)]
    span_d = t - s
    fc.append(f"[{idx}:a]aresample=48000,atrim=duration={span_d:.3f},"
              f"afade=t=in:d=2,afade=t=out:st={max(0, span_d - 3):.3f}:d=3,"
              f"volume={vol},adelay={int(s * 1000)}|{int(s * 1000)},"
              f"apad,atrim=duration={total:.3f}[m{k}]")
    mix_labels.append(f"[m{k}]")
    idx += 1

fc.append("[ac]" + "".join(mix_labels)
          + f"amix=inputs={len(mix_labels) + 1}:normalize=0:duration=first[amx]")
fc.append(f"[amx]afade=t=out:st={total - 3:.2f}:d=3[am]")
fc.append(f"[vc]fade=t=out:st={total - 2.5:.2f}:d=2.5[vf]")

graph = HERE / "outputs/assemble_tv1_graph.txt"
graph.parent.mkdir(parents=True, exist_ok=True)
graph.write_text(";".join(fc))
print(f"{n} clips, {len(NARR)} narr lines, {len(spans)} music spans, "
      f"{total:.0f}s — encoding...", flush=True)
subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs
               + ["-filter_complex_script", str(graph),
                  "-map", "[vf]", "-map", "[am]",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                  str(OUT)], check=True)
print(f"wrote {OUT}")
