#!/usr/bin/env python3
"""Assemble THE VAULTED SKY v1 into mewtwo/outputs/preview_v1.mp4.
Music: scene cues per the treatment; silence under most dialogue."""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
V2 = HERE / "outputs/v2"
V1 = HERE / "outputs/v1"
V1DUB = HERE / "outputs/v1_dub"
MUS = HERE / "music"


# dubbed takes are adopted ONLY where no recast speaker's mouth is visible
# (Long Game lesson: dubbing fails on visible lips); the rest keep original
# audio until re-rendered with ElevenLabs --audio refs
ADOPT_DUB = {"a1", "a3", "a4", "a5", "a6", "a7", "b1", "b2", "b4", "c1", "c2",
             "c4", "c5", "c6", "d6b", "e4", "e5a", "e5b", "e6", "e7", "e8",
             "f4a", "f4b", "f6b", "f7", "g2", "g3", "g5", "g6", "g7a", "g7b",
             "h1", "h2", "h3", "h4", "h5"}


def pick(name):
    dirs = (V2, V1DUB, V1) if name in ADOPT_DUB else (V2, V1)
    for d in dirs:
        if (d / f"{name}.mp4").exists():
            return d / f"{name}.mp4"
    return V1 / f"{name}.mp4"

# (clip, trim_start, trim_dur, mute, music_mark)  — "silence" ends the current bed
CUT = [
    # Act 1 — 2.351
    ("a1", 0, None, True, "womb"),   # muted: spoke a stage direction
    ("a2", 0, None, False, None),
    ("a3", 0, None, False, None),
    ("a4", 0, None, False, "silence"),
    ("a5", 0, None, False, "fuji"),
    ("a6", 0, None, False, "silence"),
    ("a7", 0, None, False, None),
    # Act 2 — ten years of lies
    ("b1", 0, None, False, "lies"),
    ("b1b", 0, None, False, None),
    ("b2", 0, None, False, None),
    ("b3", 0, None, False, "silence"),
    ("b4", 0, None, False, None),
    # Act 3 — the suit and the sky
    ("c1", 0, None, False, "silence"),
    ("c2", 0, None, False, None),
    ("c3", 0, None, False, None),
    ("c4", 0, None, False, "sky_build"),
    ("c5", 0, None, False, "sky"),
    ("c6", 0, None, False, "silence"),
    # Act 4 — the machine
    ("d1", 0, None, False, None),
    ("d2", 0, None, False, "machine"),
    ("d3", 0, None, False, "silence"),
    ("d4", 0, None, False, None),
    ("d5", 0, None, False, "machine2"),
    ("d6a", 0, None, False, None),
    ("d6b", 0, None, False, "silence"),
    # Act 5 — children of the mind
    ("e1", 0, None, False, None),
    ("e2", 0, None, False, None),
    ("e3", 0, None, False, "tulpa_walk"),
    ("e4", 0, None, False, "tulpa"),
    ("e5a", 0, None, False, "silence"),
    ("e5b", 0, None, False, None),
    ("e6", 0, None, False, None),
    ("e7", 0, None, False, None),
    ("e8", 0, None, False, "tulpa2"),
    # Act 6 — the window opens
    ("f1", 0, None, False, "quake"),
    ("f2", 0, None, False, "silence"),
    ("f3", 0, None, False, None),
    ("f4a", 0, None, False, None),
    ("f4b", 0, None, False, "quake2"),
    ("f5", 0, None, False, None),
    ("f6a", 0, None, False, "silence"),
    ("f6b", 0, None, False, None),
    ("f7", 0, None, False, None),
    ("f8", 0, None, False, None),
    # Act 7 — the escape
    ("g1", 0, None, False, "escape"),
    ("g2", 0, None, False, None),
    ("g3", 0, None, False, None),
    ("g4", 0, None, False, None),
    ("g5", 0, None, False, "silence"),
    ("g6", 0, None, False, None),
    ("g7a", 0, None, False, "silence"),
    ("g7b", 0, None, False, None),
    # Act 8 — the vaulted sky
    ("h1", 0, None, False, "stars"),
    ("h2", 0, None, False, None),
    ("h3", 0, None, False, "silence"),
    ("h4", 0, None, False, "stars_end"),
    ("h5", 0, None, False, "unown"),
    ("title", 0, None, False, "title"),
]

# (vo file, clip-relative offset seconds, volume) mixed over a clip's own audio —
# rescue slot for shouted lines that don't survive generation (e.g. g3 "CATCH!").
# clip -> list of (vo file, clip-relative offset s, volume). These shots were
# rendered SILENT (audio refs kept tripping the input filter); their lip-free
# dialogue is mixed here at animatic spacing.
VO_OVERLAYS = {
    "e3": [("vo_el/e3_1_mewtwo.mp3", 1.2, 0.9)],
    "a1": [["vo_el/a1_1_mewtwo.mp3", 1.0, 0.9]],
    "a4": [["vo_el/a4_1_sabrina.mp3", 1.0, 0.9], ["vo_el/a4_2_mewtwo.mp3", 10.61, 0.9], ["vo_el/a4_3_sabrina.mp3", 12.6, 0.9], ["vo_el/a4_4_mewtwo.mp3", 15.52, 0.9]],
    "a6": [["vo_el/a6_1_mewtwo.mp3", 1.0, 0.9], ["vo_el/a6_2_sabrina.mp3", 2.98, 0.9]],
    "a7": [["vo_el/a7_1_giovanni.mp3", 1.0, 0.9], ["vo_el/a7_2_giovanni.mp3", 13.3, 0.9]],
    "b1b": [["vo_el/b1b_1_mewtwo.mp3", 1.0, 0.9], ["vo_el/b1b_2_sabrina.mp3", 3.72, 0.9], ["vo_el/b1b_3_mewtwo.mp3", 7.79, 0.9]],
    "b4": [["vo_el/b4_1_sabrina.mp3", 1.0, 0.9], ["vo_el/b4_2_mewtwo.mp3", 4.19, 0.9]],
    "h3": [["vo_el/h3_1_mewtwo.mp3", 1.0, 0.9]],
}

MUSIC = {
    "womb":      ("mus_womb.m4a", 0.14),
    "fuji":      ("mus_fuji.m4a", 0.10),
    "lies":      ("mus_lies.m4a", 0.10),
    "sky_build": ("mus_sky.m4a", 0.09),
    "sky":       ("mus_sky.m4a", 0.18),
    "machine":   ("mus_machine.m4a", 0.10),
    "machine2":  ("mus_machine.m4a", 0.09),
    "tulpa_walk": ("mus_tulpa.m4a", 0.08),
    "tulpa":     ("mus_tulpa.m4a", 0.12),
    "tulpa2":    ("mus_tulpa.m4a", 0.12),
    "quake":     ("mus_quake.m4a", 0.16),
    "quake2":    ("mus_quake.m4a", 0.10),
    "escape":    ("mus_escape.m4a", 0.16),
    "stars":     ("mus_stars.m4a", 0.12),
    "stars_end": ("mus_fuji.m4a", 0.09),
    "unown":     ("mus_unown.m4a", 0.14),
    "title":     ("mus_stars.m4a", 0.14),
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
        ovs = VO_OVERLAYS[name]
        fc.append(a + f",apad,atrim=duration={d:.3f}[abase{i}]")
        labels = [f"[abase{i}]"]
        for k, (vof, voff, vvol) in enumerate(ovs):
            vidx = len(cut) + 100 + i * 10 + k
            extra_inputs.append((vidx, str(HERE / vof)))
            fc.append(f"[{vidx}:a]aresample=48000,volume={vvol},"
                      f"adelay={int(voff*1000)}|{int(voff*1000)},apad,"
                      f"atrim=duration={d:.3f}[avo{i}_{k}]")
            labels.append(f"[avo{i}_{k}]")
        fc.append("".join(labels) +
                  f"amix=inputs={len(labels)}:normalize=0:duration=first[a{i}]")
    else:
        fc.append(a + f",apad,atrim=duration={d:.3f}[a{i}]")
n = len(cut)
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
fc.append(f"[amx]afade=t=out:st={total - 3.0:.2f}:d=3.0[am]")

graph = HERE / "outputs/assemble_v3_graph.txt"
graph.parent.mkdir(parents=True, exist_ok=True)
graph.write_text(";".join(fc))
print(f"{n} clips, {len(spans)} music spans, {total:.0f}s — encoding...", flush=True)
subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs
               + ["-filter_complex_script", str(graph),
                  "-map", "[vc]", "-map", "[am]",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                  str(HERE / "outputs/preview_v3.mp4")], check=True)
print("wrote mewtwo/outputs/preview_v3.mp4")
