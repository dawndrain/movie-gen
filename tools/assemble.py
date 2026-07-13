#!/usr/bin/env python3
"""Assemble a film from a spec module: one ffmpeg filtergraph, one encode.

Usage:
    python3 tools/assemble.py <film_spec.py> [--graph-only]

The spec is a plain python module (data, not code) defining:

  ROOT      Path of the project folder (usually Path(__file__).parent)
  OUT       output mp4 path, relative to ROOT
  GRAPH     filtergraph text file path, relative to ROOT (debuggable artifact)
  SIZE      (w, h) e.g. (854, 480);  FPS  e.g. 24
  CUT       [(clip_path, trim_start, trim_dur|None, mute, era_mark|None), ...]
            era_mark labels the FIRST clip of each music span; "silence" starts
            an unscored span; None continues the current span.
  MUSIC     {era_mark: {"file": name, "vol": float,
                        "fade_in": seconds | "span" | None(=1.5),
                        "fade_out": seconds | None(=3.0)}}
  MUS_DIR   directory of music files, relative to ROOT
  SPAN_MERGES  [(marker, prev_era, extend_s), ...] — a pseudo-mark that merges
            into the previous span if it is prev_era, extending it extend_s
            past the marker (e.g. warm 1926 cue running 3s into the next scene
            then cutting hard).
  AMBIENCE  [(start_stem, end_stem, bed_file, vol_or_dB_string), ...] — bed runs
            from the start of first clip named start_stem to the start of
            end_stem. Beds should be loudness-normalized first (see
            MOVIE_LESSONS.md "Sound").
  AMB_DIR   directory of ambience beds, relative to ROOT
  GRADE     {clip_stem: "ffmpeg,video,filters,"} (trailing comma), e.g. color
            grades or a fade to black on a final clip
  AFADE     {clip_stem: (fade_start_s, fade_dur_s)} audio fade-outs
  FREEZE    {clip_stem: extra_seconds} tail freeze-frames (tpad clone)

Any of MUSIC/AMBIENCE/GRADE/AFADE/FREEZE/SPAN_MERGES may be omitted or empty.
"""
import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--graph-only", action="store_true",
                help="write the filtergraph and span report, skip the encode")
args = ap.parse_args()

spec_path = Path(args.spec).resolve()
m = importlib.util.spec_from_file_location("film_spec", spec_path)
S = importlib.util.module_from_spec(m)
m.loader.exec_module(S)

ROOT = S.ROOT
CUT = S.CUT
MUSIC = getattr(S, "MUSIC", {})
MUS = ROOT / getattr(S, "MUS_DIR", "music")
AMBIENCE = getattr(S, "AMBIENCE", [])
AMB = ROOT / getattr(S, "AMB_DIR", "ambience")
GRADE = getattr(S, "GRADE", {})
AFADE = getattr(S, "AFADE", {})
FREEZE = getattr(S, "FREEZE", {})
SPAN_MERGES = getattr(S, "SPAN_MERGES", [])
W, H = getattr(S, "SIZE", (854, 480))
FPS = getattr(S, "FPS", 24)
OUT = ROOT / S.OUT
GRAPH = ROOT / S.GRAPH


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


missing = [str(p) for p, *_ in CUT if not p.exists()]
missing += [str(MUS / v["file"]) for v in MUSIC.values() if not (MUS / v["file"]).exists()]
missing += [str(AMB / f) for _, _, f, _ in AMBIENCE if not (AMB / f).exists()]
if missing:
    raise SystemExit("missing:\n" + "\n".join(sorted(set(missing))))

# first pass: durations + era span offsets
offsets, total = [], 0.0
for path, ts, td, mute, era in CUT:
    d = (td if td else dur(path) - ts) + FREEZE.get(path.stem, 0)
    offsets.append((total, d, era))
    total += d
spans = []  # (era, start, end)
cur = None
for (start, d, era) in offsets:
    if era is not None:
        if cur:
            spans.append((cur[0], cur[1], start))
        cur = (era, start)
for (start, d, era) in [offsets[-1]]:
    spans.append((cur[0], cur[1], start + d))
# pseudo-marks that merge into the previous span and extend it
for marker, prev_era, extend in SPAN_MERGES:
    merged = []
    for e, st, en in spans:
        if e == marker:
            if merged and merged[-1][0] == prev_era:
                merged[-1] = (prev_era, merged[-1][1], st + extend)
            continue
        merged.append((e, st, en))
    spans = merged
spans = [(e, st, en) for (e, st, en) in spans if e in MUSIC]

inputs, fc = [], []
for i, (path, ts, td, mute, era) in enumerate(CUT):
    d = offsets[i][1]
    fz = FREEZE.get(path.stem, 0)
    d0 = d - fz
    inputs += ["-i", str(path)]
    tpad = f"tpad=stop_mode=clone:stop_duration={fz}," if fz else ""
    grade = GRADE.get(path.stem, "")
    fc.append(f"[{i}:v]trim=start={ts}:end={ts + d0:.3f},setpts=PTS-STARTPTS,{tpad}{grade}"
              f"scale={W}:{H},setsar=1,fps={FPS}[v{i}]")
    a = f"[{i}:a]atrim=start={ts}:end={ts + d0:.3f},asetpts=PTS-STARTPTS,aresample=48000"
    if mute:
        a += ",volume=0"
    if path.stem in AFADE:
        fs, fd = AFADE[path.stem]
        a += f",afade=t=out:st={fs}:d={fd}"
    fc.append(a + f",apad,atrim=duration={d:.3f}[a{i}]")
n = len(CUT)
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")

# music beds
mus_labels = []
for k, (era, s, t) in enumerate(spans):
    mv = MUSIC[era]
    idx = n + k
    inputs += ["-i", str(MUS / mv["file"])]
    span_d = t - s
    fi = mv.get("fade_in")
    fade_in = span_d if fi == "span" else (fi if fi is not None else 1.5)
    fo = mv.get("fade_out")
    fade_out = fo if fo is not None else 3.0
    fc.append(f"[{idx}:a]aresample=48000,atrim=duration={span_d:.3f},"
              f"afade=t=in:d={fade_in:.3f},afade=t=out:st={max(0, span_d - fade_out):.3f}:d={fade_out},"
              f"volume={mv['vol']},adelay={int(s * 1000)}|{int(s * 1000)},"
              f"apad,atrim=duration={total:.3f}[m{k}]")
    mus_labels.append(f"[m{k}]")

# ambience beds
first_at = {}
for k, (st, d, era) in enumerate(offsets):
    stem = CUT[k][0].stem
    if stem not in first_at:
        first_at[stem] = st
amb_labels = []
for k, (s0, s1, f, vol) in enumerate(AMBIENCE):
    a0, a1 = first_at[s0], first_at[s1]
    span_d = a1 - a0
    idx = len(inputs) // 2
    inputs += ["-i", str(AMB / f)]
    fc.append(f"[{idx}:a]aresample=48000,atrim=duration={span_d:.3f},"
              f"afade=t=in:d=1.5,afade=t=out:st={max(0, span_d - 1.5):.3f}:d=1.5,"
              f"volume={vol},adelay={int(a0 * 1000)}|{int(a0 * 1000)},"
              f"apad,atrim=duration={total:.3f}[amb{k}]")
    amb_labels.append(f"[amb{k}]")
fc.append("[ac]" + "".join(mus_labels) + "".join(amb_labels)
          + f"amix=inputs={len(mus_labels) + len(amb_labels) + 1}:normalize=0:duration=first[amx]")
fc.append(f"[amx]afade=t=out:st={total - 2.0:.2f}:d=2.0[am]")

GRAPH.parent.mkdir(parents=True, exist_ok=True)
GRAPH.write_text(";".join(fc))
print(f"{n} clips, {len(spans)} music spans, {len(amb_labels)} ambience beds, "
      f"{total:.0f}s — {'graph only' if args.graph_only else 'encoding...'}", flush=True)
for e, s, t in spans:
    print(f"  music {e}: {s:.0f}s → {t:.0f}s")
if args.graph_only:
    sys.exit(0)
OUT.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs
               + ["-filter_complex_script", str(GRAPH),
                  "-map", "[vc]", "-map", "[am]",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                  str(OUT)], check=True)
print(f"wrote {OUT.relative_to(ROOT)}")
