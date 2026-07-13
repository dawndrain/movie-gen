#!/usr/bin/env python3
"""Assemble the v7 cut into outputs/preview_v7.mp4.
New: restructured arcade (arrogant Cass), escalating respawn gags, bronze wardrobe
sweep, roman sighs, 2044 bedroom, and a full music layer (sonilo cues per era,
mixed low under dialogue)."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
V1, V2, V3 = ROOT / "outputs/video", ROOT / "outputs/video2", ROOT / "outputs/video3"
V4, V5, V6 = ROOT / "outputs/video4", ROOT / "outputs/video5", ROOT / "outputs/video6"
V7 = ROOT / "outputs/video7"
MUS = ROOT / "music"

# (clip path, trim_start, trim_dur, mute, era_mark)
# era_mark labels the FIRST clip of each music span (None = no new span)
CUT = [
    # --- Cold open + Arcade (restructured, tighter) ---
    (V5 / "t0_onelife.mp4", 0, None, False, "omen"),
    (V3 / "a5_what_it_means.mp4", 0, None, False, "arcade"),
    (V6 / "a6_sign2.mp4", 0, None, False, None),
    (V3 / "a7_dibs.mp4", 0, None, False, None),
    (V7 / "a_ski2.mp4", 0, None, False, None),
    (V5 / "a8_out2.mp4", 0, None, False, None),
    (V6 / "a_hard.mp4", 0, None, False, None),
    (V6 / "a10_v3.mp4", 0, None, False, None),
    # --- Bronze ---
    (V6 / "b1_wake3.mp4", 0, None, False, "silence"),
    (V2 / "2_2_water_carry.mp4", 0, None, False, "bronze"),
    (V3 / "b3_goat.mp4", 0, None, False, None),
    (V3 / "b12_cough.mp4", 0, None, False, "silence"),  # deaths/respawns play dry
    (V6 / "b5_afterlife2.mp4", 0, None, False, None),
    (V6 / "b6_scream2.mp4", 0, None, False, None),
    (V6 / "b7_name2.mp4", 0, None, False, None),
    (V3 / "b8_how_do_i_leave.mp4", 0, None, False, None),
    (V1 / "2_5_touched_woman.mp4", 0, None, False, None),
    (V3 / "b10_forty.mp4", 0, None, False, None),
    (V3 / "b12_cough.mp4", 0, None, False, None),        # same cough, death #2
    (V7 / "w1b.mp4", 0, None, False, None),         # respawn: "...Again."
    (V6 / "b13_cry2.mp4", 0, None, False, None),
    (V3 / "b14_three_lives.mp4", 0, None, False, None),
    (V7 / "w2b.mp4", 0, None, False, None),          # respawn: playing dead
    (V3 / "b15_five_lives.mp4", 0, 3.5, False, None),    # "...maybe five lives."
    (V6 / "w3_yoke.mp4", 0, None, False, None),          # respawn: yoke drop
    (V6 / "b16_cure3.mp4", 0, None, False, None),
    (V3 / "b17_rant.mp4", 0, 2.90, False, None),
    (V3 / "b17_rant.mp4", 6.95, None, False, None),
    (V3 / "b18_germs.mp4", 0, None, False, None),
    (V7 / "b19_isa.mp4", 0, None, False, None),
    (V5 / "b20_solemn2.mp4", 0, None, False, None),
    (V7 / "b21_party.mp4", 0, None, False, None),
    (V7 / "b22_wish3.mp4", 0, None, False, None),
    (V5 / "b23_finally2.mp4", 0, None, False, "omen_b23"),
    # --- Roman ---
    (V6 / "r1_sigh.mp4", 0, None, False, "silence"),
    (V7 / "r2_aq3.mp4", 0, None, False, None),
    (V3 / "r3_gesture_q.mp4", 0, None, False, None),
    (V6 / "r4_boil2.mp4", 0, None, False, None),
    (V5 / "r5_library2.mp4", 0, None, False, None),
    (V3 / "r6_scroll.mp4", 0, None, False, None),
    (V3 / "r7_bath_pitch.mp4", 0, None, False, "roman"),
    (V3 / "r8_glass.mp4", 0, None, False, None),
    (V5 / "r9_acid2.mp4", 0, None, False, None),
    (V3 / "r10_page.mp4", 0, None, False, None),
    (V3 / "r11_dictate_blood.mp4", 0, None, False, None),
    (V7 / "r12_salt4.mp4", 0, None, False, None),
    (V7 / "r13_sweet3.mp4", 0, None, False, None),
    # --- Renaissance ---
    (V4 / "n1_bridge.mp4", 0, None, False, "ren_a"),
    (V4 / "n2_widow.mp4", 0, None, False, None),
    (V4 / "n3_card.mp4", 0, None, False, None),
    (V3 / "e1_library2.mp4", 0, None, False, "silence"),
    (V3 / "e2_fire.mp4", 0, 6.9, False, None),
    (V4 / "n4_fireflash.mp4", 0, None, False, None),
    (V3 / "e2_fire.mp4", 6.9, None, False, None),
    (V3 / "e3_flood.mp4", 0, None, False, "ren_b"),     # vow -> type -> montage scored
    (V4 / "n5_type.mp4", 0, None, False, None),
    (V3 / "e4_montage.mp4", 0, None, False, None),
    (V4 / "n6_boiler.mp4", 0, None, False, "boiler"),
    (V4 / "n7_again.mp4", 0, None, False, "silence"),    # post-boom: no music
    (V4 / "n8_gauge.mp4", 0, None, False, None),
    (V4 / "n9_sixty.mp4", 0, None, False, "m1926"),
    # --- 1926 ---
    (V5 / "m1_wake2.mp4", 0, None, False, None),
    (V5 / "m2_tram2.mp4", 0, None, False, None),
    (V5 / "m3_twenty2.mp4", 0, None, False, None),
    (V4 / "m4_teach.mp4", 0, None, False, None),
    (V7 / "m5_feet2.mp4", 0, None, False, None),
    (V4 / "m6_longtime.mp4", 0, None, False, None),
    (V4 / "m7_obit.mp4", 0, None, False, None),
    # --- The machine documented ---
    (V4 / "p1_dinner.mp4", 0, None, False, "machine"),
    (V5 / "p2_board2.mp4", 0, None, False, None),
    (V4 / "p3_manual.mp4", 0, None, False, None),
    (V7 / "p4_exit3.mp4", 0, None, False, "silence"),
    # --- The arcade, again ---
    (V5 / "q1_off2.mp4", 0, None, False, "silence"),     # diegetic arcade only
    (V4 / "q2_longtime.mp4", 0, None, False, None),
    (V4 / "q3_walk.mp4", 0, None, False, None),
    (V6 / "q4_real2.mp4", 0, None, False, "omen_q4"),
    (V4 / "q5_nested.mp4", 0, None, False, "silence"),
    (V4 / "q6_longtime2.mp4", 0, None, False, None),
    (V6 / "q7_fail2.mp4", 0, None, False, "end"),
    (V7 / "q8_come3.mp4", 0, None, False, None),
]

# era -> (music file, volume). "silence"/"boiler" handled via span logic below.
MUSIC = {
    "omen": ("mus_omen.m4a", 0.20),
    "arcade": ("mus_arcade2.m4a", 0.08),
    "bronze": ("mus_bronze.m4a", 0.09),      # chores montage only
    "omen_b23": ("mus_omen.m4a", 0.16),      # the gut-punch
    "roman": ("mus_roman.m4a", 0.07),        # the project montage only
    "ren_a": ("mus_ren.m4a", 0.07),          # arrival
    "ren_b": ("mus_ren.m4a", 0.12),          # the vow / flood montage
    "boiler": ("mus_boiler.m4a", 0.20),
    "m1926": ("mus_1926.m4a", 0.09),         # from the widow's nod through Iris
    "machine": ("mus_machine.m4a", 0.09),
    "omen_q4": ("mus_omen.m4a", 0.14),       # dread before the white flash
    "end": ("mus_end.m4a", 0.10),            # only the resignation + door
}


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


missing = [str(p) for p, *_ in CUT if not p.exists()]
missing += [str(MUS / f) for f, _ in MUSIC.values() if not (MUS / f).exists()]
if missing:
    raise SystemExit("missing:\n" + "\n".join(sorted(set(missing))))

# first pass: durations + era span offsets
offsets, total = [], 0.0
for path, ts, td, mute, era in CUT:
    d = td if td else dur(path) - ts
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
spans = [(e, s, t) for (e, s, t) in spans if e in MUSIC]

inputs, fc = [], []
for i, (path, ts, td, mute, era) in enumerate(CUT):
    d = offsets[i][1]
    inputs += ["-i", str(path)]
    fc.append(f"[{i}:v]trim=start={ts}:end={ts + d:.3f},setpts=PTS-STARTPTS,"
              f"scale=854:480,setsar=1,fps=24[v{i}]")
    a = f"[{i}:a]atrim=start={ts}:end={ts + d:.3f},asetpts=PTS-STARTPTS,aresample=48000"
    if mute:
        a += ",volume=0"
    fc.append(a + f",apad,atrim=duration={d:.3f}[a{i}]")
n = len(CUT)
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")

# music beds
mus_labels = []
for k, (era, s, t) in enumerate(spans):
    f, vol = MUSIC[era]
    idx = n + k
    inputs += ["-i", str(MUS / f)]
    span_d = t - s
    fc.append(f"[{idx}:a]aresample=48000,atrim=duration={span_d:.3f},"
              f"afade=t=in:d=1.5,afade=t=out:st={max(0, span_d - 3):.3f}:d=3,"
              f"volume={vol},adelay={int(s * 1000)}|{int(s * 1000)},"
              f"apad,atrim=duration={total:.3f}[m{k}]")
    mus_labels.append(f"[m{k}]")
fc.append("[ac]" + "".join(mus_labels)
          + f"amix=inputs={len(mus_labels) + 1}:normalize=0:duration=first[amx]")
fc.append(f"[amx]afade=t=out:st={total - 2.0:.2f}:d=2.0[am]")

graph_file = ROOT / "outputs/assemble_v7_graph.txt"
graph_file.write_text(";".join(fc))
print(f"{n} clips, {len(spans)} music spans, {total:.0f}s — encoding...", flush=True)
for e, s, t in spans:
    print(f"  music {e}: {s:.0f}s → {t:.0f}s")
subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs
               + ["-filter_complex_script", str(graph_file),
                  "-map", "[vc]", "-map", "[am]",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                  str(ROOT / "outputs/preview_v7.mp4")], check=True)
print("wrote outputs/preview_v7.mp4")
