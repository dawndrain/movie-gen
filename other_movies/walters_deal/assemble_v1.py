#!/usr/bin/env python3
"""Assemble the Walter's Deal first-pass cut into walters_deal/outputs/preview_v1.mp4.

Entries: ("clip", name, trim_start, trim_dur|None, mute, music_mark)
         ("still", frame_name, duration, music_mark)   # title cards
Music marks name the span starting at that entry ("silence" = no music).
"""
import subprocess
from pathlib import Path

PROJ = Path(__file__).parent
V1 = PROJ / "outputs/video1"
F = PROJ / "frames"
MUS = PROJ / "music"

CUT = [
    ("still", "t_title", 3.0, "open"),
    # --- Act I: The Deal ---
    ("clip", "a1_rat", 0, None, False, None),
    ("clip", "a2_beaming", 0, None, False, "silence"),
    ("clip", "a3_mob", 0, None, False, None),
    ("clip", "a4_window", 0, None, False, None),
    ("clip", "a5_deal", 0, None, False, None),
    ("clip", "a6_lottery", 0, None, False, None),
    ("clip", "a7_jeremy", 0, None, False, None),
    ("clip", "a8_mayor", 0, None, False, None),
    # --- Act II: The Demonstration ---
    ("clip", "b1_warehouse", 0, None, False, None),
    ("clip", "b2_stowaway", 0, None, False, None),
    ("clip", "b3_demo", 0, None, False, None),
    ("clip", "b4_sniper", 0, None, False, None),
    # --- Act III: The Cracks ---
    ("still", "t_2years", 2.5, "silence"),
    ("clip", "c1_temple", 0, None, False, None),
    ("clip", "c2_rat2", 0, None, False, None),
    ("clip", "c3_confess", 0, None, False, None),
    ("clip", "c4_teens", 0, None, False, "omen1"),
    ("clip", "c5_press", 0, None, False, "silence"),
    ("clip", "c6_jeremy", 0, None, False, None),
    # --- Act IV: The Time Machine ---
    ("clip", "d1_epiphany", 0, None, False, None),
    ("clip", "d2_resurrect", 0, None, False, None),
    ("clip", "d3_lost", 0, None, False, None),
    ("clip", "d4_isela", 0, None, False, None),
    # --- Act V: The Fall ---
    ("still", "t_4years", 2.5, "silence"),
    ("clip", "e1_recluse", 0, None, False, None),
    ("clip", "e2_rescue", 0, None, False, None),
    ("clip", "e3_bernand", 0, None, False, "omen2"),
    ("clip", "e4_collapse", 0, None, False, "silence"),
    ("clip", "e5_shutdown", 0, None, False, None),
    ("clip", "e6_bomb", 0, None, False, None),
    # --- Act VI: Resurrections ---
    ("clip", "f1_sorry", 0, None, False, "omen3"),
    ("clip", "f2_awake", 0, None, False, "silence"),
    ("clip", "f3_price", 0, None, False, None),
    ("clip", "f4_catch", 0, None, False, None),
    ("clip", "f5_inside", 0, None, False, None),
    # --- Act VII: The Cemetery ---
    ("still", "t_6years", 2.5, "silence"),
    ("clip", "g1_interview", 0, None, False, None),
    ("clip", "g2_grave", 0, None, False, None),
    ("clip", "g3_funeral", 0, None, False, "end"),
    ("clip", "g4_end", 0, None, False, None),
]

MUSIC = {  # mark prefix -> (file, volume)
    "open": ("open.m4a", 0.10),
    "omen": ("omen.m4a", 0.16),
    "end": ("end.m4a", 0.12),
}


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


# resolve entries -> (kind, path, ts, d, mute, mark)
entries = []
for e in CUT:
    if e[0] == "still":
        _, name, d, mark = e
        p = F / f"{name}.png"
        if not p.exists():
            print(f"MISSING still {name}, skipping")
            continue
        entries.append(("still", p, 0, d, True, mark))
    else:
        _, name, ts, td, mute, mark = e
        p = V1 / f"{name}.mp4"
        if not p.exists():
            print(f"MISSING clip {name}, skipping")
            continue
        d = td if td is not None else dur(p) - ts
        entries.append(("clip", p, ts, d, mute, mark))

# music spans: (mark, start_t, end_t); a mark closes any open span,
# "silence" just closes, other marks open a new span.
spans, open_span, t = [], None, 0.0
for kind, p, ts, d, mute, mark in entries:
    if mark:
        if open_span:
            open_span[2] = t
            open_span = None
        if mark != "silence":
            open_span = [mark, t, None]
            spans.append(open_span)
    t += d
total = t
if open_span:
    open_span[2] = total

inputs, fc = [], []
for i, (kind, p, ts, d, mute, mark) in enumerate(entries):
    if kind == "still":
        inputs += ["-loop", "1", "-t", f"{d:.3f}", "-i", str(p)]
        fc.append(f"[{i}:v]scale=854:480,setsar=1,fps=24,trim=duration={d:.3f}[v{i}]")
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f}[a{i}]")
    else:
        inputs += ["-i", str(p)]
        fc.append(f"[{i}:v]trim=start={ts}:end={ts + d:.3f},setpts=PTS-STARTPTS,"
                  f"scale=854:480,setsar=1,fps=24[v{i}]")
        a = (f"[{i}:a]atrim=start={ts}:end={ts + d:.3f},asetpts=PTS-STARTPTS,"
             f"aresample=48000")
        if mute:
            a += ",volume=0"
        fc.append(a + f",apad,atrim=duration={d:.3f}[a{i}]")
n = len(entries)
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")

mus_labels = []
valid_spans = [s for s in spans if s and s[2] > s[1]]
for k, (mark, s, e) in enumerate(valid_spans):
    key = next((m for m in MUSIC if mark.startswith(m)), None)
    if not key:
        continue
    f, vol = MUSIC[key]
    if not (MUS / f).exists():
        print(f"MISSING music {f}, skipping span {mark}")
        continue
    idx = n + len(mus_labels)
    inputs += ["-i", str(MUS / f)]
    span_d = e - s
    fc.append(f"[{idx}:a]aresample=48000,atrim=duration={span_d:.3f},"
              f"afade=t=in:d=1.5,afade=t=out:st={max(0, span_d - 3):.3f}:d=3,"
              f"volume={vol},adelay={int(s * 1000)}|{int(s * 1000)},"
              f"apad,atrim=duration={total:.3f}[m{len(mus_labels)}]")
    mus_labels.append(f"[m{len(mus_labels)}]")
if mus_labels:
    fc.append("[ac]" + "".join(mus_labels)
              + f"amix=inputs={len(mus_labels) + 1}:normalize=0:duration=first[amx]")
else:
    fc.append("[ac]anull[amx]")
fc.append(f"[amx]afade=t=out:st={total - 2.0:.2f}:d=2.0[am]")

graph_file = PROJ / "outputs/assemble_v1_graph.txt"
graph_file.write_text(";".join(fc))
print(f"{n} entries, {len(mus_labels)} music spans, {total:.0f}s — encoding...", flush=True)
for s in valid_spans:
    print(f"  music {s[0]}: {s[1]:.0f}s -> {s[2]:.0f}s")
subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs
               + ["-filter_complex_script", str(graph_file),
                  "-map", "[vc]", "-map", "[am]",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                  str(PROJ / "outputs/preview_v1.mp4")], check=True)
print("wrote walters_deal/outputs/preview_v1.mp4")
