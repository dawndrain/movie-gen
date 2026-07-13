#!/usr/bin/env python3
"""Assemble the Hork-Bajir Chronicles first pass into animorphs/outputs/preview_hb3.mp4.
Music: low beds on wonder/dread/battle/elegy beats, silence under most dialogue."""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
V1 = HERE / "outputs/hb1"
V2 = HERE / "outputs/hb2"
V3 = HERE / "outputs/hb3"
MUS = HERE / "music"


def pick(name):
    for d in (V3, V2, V1):
        if (d / f"{name}.mp4").exists():
            return d / f"{name}.mp4"
    return V1 / f"{name}.mp4"

# (clip, trim_start, trim_dur, mute, music_mark)
CUT = [
    ("f1", 0, None, False, "frame"),
    ("f2", 0, None, False, None),
    ("f3", 0, None, False, "wonder_title"),
    ("a1", 0, None, False, None),
    ("a2", 0, None, False, "silence"),
    ("a3", 0, None, False, "wonder_ridge"),
    ("b1", 0, None, False, None),
    ("b2", 0, None, False, "silence"),
    ("b3", 0, None, False, None),
    ("b4", 0, None, False, None),
    ("b5", 0, None, False, "wonder_stars"),
    ("b6", 0, None, False, "silence"),
    ("b7a", 0, None, False, "wonder_flight"),
    ("b7b", 0, None, False, None),
    ("c1", 0, None, False, "dread_deep"),
    ("c2", 0, None, False, None),
    ("c3", 0, None, False, "wonder_city"),
    ("c4", 0, None, False, "silence"),
    ("c5", 0, None, False, None),
    ("c6", 0, None, False, None),
    ("d1", 0, None, False, "dread_arrival"),
    ("d2", 0, None, False, "silence"),
    ("d3", 0, None, False, "dread_pool"),
    ("d4", 0, None, False, "dread_jagil"),
    ("d5", 0, None, False, "battle_dome"),
    ("d6", 0, None, False, "elegy_ash"),
    ("e1a", 0, None, False, "silence"),
    ("e1b", 0, None, False, None),
    ("e2", 0, None, False, None),
    ("e3", 0, None, False, "wonder_morph"),
    ("e4", 0, None, False, "battle_train"),
    ("e5", 0, None, False, "silence"),
    ("e6", 0, None, False, None),
    ("g1", 0, None, False, "silence"),
    ("g2", 0, None, False, None),
    ("g3", 0, None, False, "dread_vial"),
    ("g4", 0, None, False, "battle_heist"),
    ("g5", 0, None, False, None),
    ("g6", 0, None, False, "elegy_world"),
    ("h1", 0, None, False, "hope_dawn"),
    ("h2", 0, None, False, None),
    ("h3", 0, None, False, "dread_esplin"),
    ("i1", 0, None, False, "frame_close"),
    ("i2", 0, None, False, None),
    ("i3", 0, None, False, "hope_end"),
]

# (vo file, clip-relative offset seconds, volume) mixed over a clip's own audio
VO_OVERLAYS = {
    "g5": ("vo/g5_1_aldrea.mp3", 2.8, 0.9),
}

MUSIC = {
    "frame": ("mus_frame.m4a", 0.10),
    "wonder_title": ("mus_wonder.m4a", 0.16),
    "wonder_ridge": ("mus_wonder.m4a", 0.13),
    "wonder_stars": ("mus_wonder.m4a", 0.07),
    "dread_deep": ("mus_dread.m4a", 0.10),
    "wonder_city": ("mus_wonder.m4a", 0.12),
    "dread_arrival": ("mus_dread.m4a", 0.16),
    "dread_pool": ("mus_dread.m4a", 0.19),
    "dread_jagil": ("mus_dread.m4a", 0.11),
    "wonder_flight": ("mus_wonder.m4a", 0.15),
    "battle_dome": ("mus_battle.m4a", 0.14),
    "elegy_ash": ("mus_elegy.m4a", 0.12),
    "wonder_morph": ("mus_wonder.m4a", 0.16),
    "battle_train": ("mus_battle.m4a", 0.09),
    "dread_vial": ("mus_dread.m4a", 0.08),
    "battle_heist": ("mus_battle.m4a", 0.12),
    "elegy_world": ("mus_elegy.m4a", 0.18),
    "hope_dawn": ("mus_hope.m4a", 0.09),
    "dread_esplin": ("mus_dread.m4a", 0.12),
    "frame_close": ("mus_frame.m4a", 0.09),
    "hope_end": ("mus_hope.m4a", 0.18),
}


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


cut = [(pick(name), ts, td, mute, era) for name, ts, td, mute, era in CUT]
missing = [p.name for p, *_ in cut if not p.exists()]
missing += [f for f, _ in MUSIC.values() if not (MUS / f).exists()]
if missing:
    raise SystemExit("missing:\n" + "\n".join(sorted(set(missing))))

offsets, total = [], 0.0
for path, ts, td, mute, era in cut:
    d = td if td else dur(path) - ts
    offsets.append((total, d, era))
    total += d
spans, cur = [], None
for (start, d, era) in offsets:
    if era is not None:
        if cur:
            spans.append((cur[0], cur[1], start))
        cur = (era, start)
spans.append((cur[0], cur[1], offsets[-1][0] + offsets[-1][1]))
spans = [(e, s, t) for (e, s, t) in spans if e in MUSIC]

inputs, fc = [], []
extra_inputs = []
for i, (path, ts, td, mute, era) in enumerate(cut):
    d = offsets[i][1]
    inputs += ["-i", str(path)]
    fc.append(f"[{i}:v]trim=start={ts}:end={ts + d:.3f},setpts=PTS-STARTPTS,"
              f"scale=854:480,setsar=1,fps=24[v{i}]")
    a = f"[{i}:a]atrim=start={ts}:end={ts + d:.3f},asetpts=PTS-STARTPTS,aresample=48000"
    if mute:
        a += ",volume=0"
    name = CUT[i][0]
    if name in VO_OVERLAYS:
        vof, voff, vvol = VO_OVERLAYS[name]
        vidx = len(cut) + 100 + i
        extra_inputs.append((vidx, str(HERE / vof)))
        fc.append(a + f",apad,atrim=duration={d:.3f}[abase{i}]")
        fc.append(f"[{vidx}:a]aresample=48000,volume={vvol},"
                  f"adelay={int(voff*1000)}|{int(voff*1000)},apad,"
                  f"atrim=duration={d:.3f}[avo{i}]")
        fc.append(f"[abase{i}][avo{i}]amix=inputs=2:normalize=0:duration=first[a{i}]")
    else:
        fc.append(a + f",apad,atrim=duration={d:.3f}[a{i}]")
n = len(cut)
# remap extra vo inputs to sequential ffmpeg input indices
for j, (vidx, path) in enumerate(extra_inputs):
    real = n + j
    fc = [f.replace(f"[{vidx}:a]", f"[{real}:a]") for f in fc]
    inputs += ["-i", path]
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")

mus_labels = []
for k, (era, s, t) in enumerate(spans):
    f, vol = MUSIC[era]
    idx = n + len(extra_inputs) + k
    inputs += ["-i", str(MUS / f)]
    span_d = t - s
    fc.append(f"[{idx}:a]aresample=48000,atrim=duration={span_d:.3f},"
              f"afade=t=in:d=1.5,afade=t=out:st={max(0, span_d - 3):.3f}:d=3,"
              f"volume={vol},adelay={int(s * 1000)}|{int(s * 1000)},"
              f"apad,atrim=duration={total:.3f}[m{k}]")
    mus_labels.append(f"[m{k}]")
fc.append("[ac]" + "".join(mus_labels)
          + f"amix=inputs={len(mus_labels) + 1}:normalize=0:duration=first[amx]")
fc.append(f"[amx]afade=t=out:st={total - 2.5:.2f}:d=2.5[am]")

graph = HERE / "outputs/assemble_hb3_graph.txt"
graph.parent.mkdir(parents=True, exist_ok=True)
graph.write_text(";".join(fc))
print(f"{n} clips, {len(spans)} music spans, {total:.0f}s — encoding...", flush=True)
subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs
               + ["-filter_complex_script", str(graph),
                  "-map", "[vc]", "-map", "[am]",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                  str(HERE / "outputs/preview_hb3.mp4")], check=True)
print("wrote animorphs/outputs/preview_hb3.mp4")
