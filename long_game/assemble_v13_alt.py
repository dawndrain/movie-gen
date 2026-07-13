#!/usr/bin/env python3
"""ALT ENDING: film cuts mid-second exit attempt; machine hum over black.
New: restructured arcade (arrogant Cass), escalating respawn gags, bronze wardrobe
sweep, roman sighs, 2044 bedroom, and a full music layer (sonilo cues per era,
mixed low under dialogue)."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
V1, V2, V3 = ROOT / "outputs/video", ROOT / "outputs/video2", ROOT / "outputs/video3"
V4, V5, V6 = ROOT / "outputs/video4", ROOT / "outputs/video5", ROOT / "outputs/video6"
V7 = ROOT / "outputs/video7"
V8 = ROOT / "outputs/video8"
V9 = ROOT / "outputs/video9"
V10 = ROOT / "outputs/video10"
V11 = ROOT / "outputs/video11"
V12 = ROOT / "outputs/video12"
V13 = ROOT / "outputs/video13"
WHITE = ROOT / "outputs/white_flash.mp4"
MUS = ROOT / "music"

# (clip path, trim_start, trim_dur, mute, era_mark)
# era_mark labels the FIRST clip of each music span (None = no new span)
CUT = [
    # --- Cold open + Arcade (restructured, tighter) ---
    (V13 / "t0_longgame.mp4", 0, None, False, "omen"),  # "The Long Game" redub
    (V6 / "a6_sign2.mp4", 0, None, False, "silence"),  # reverted to v6 take; arcade plays diegetic-only
    (V3 / "a7_dibs.mp4", 0, None, False, None),
    (WHITE, 0, None, False, None),                       # white cut: Deshawn goes in
    (V8 / "a_ski3.mp4", 0, None, False, None),
    (V9 / "a8_out3.mp4", 0, None, False, None),
    (V12 / "a_hard_fix.mp4", 0, None, False, None),  # "Subject 1" -> "Cass" dubbed
    # --- Bronze ---
    (V11 / "b1_wake5.mp4", 0, None, False, "silence"),
    (V2 / "2_2_water_carry.mp4", 0, None, False, "bronze"),
    (V3 / "b3_goat.mp4", 0, None, False, None),
    (V3 / "b12_cough.mp4", 0, None, False, "silence"),  # deaths/respawns play dry
    (V6 / "b5_afterlife2.mp4", 0, None, False, None),
    (V12 / "b6_fix.mp4", 0, None, False, None),      # v6 scream transplanted
    (V9 / "b7_name3.mp4", 0, None, False, None),
    (V13 / "b8_longgame.mp4", 0, None, False, None),   # "Long Game" spliced
    (V1 / "2_5_touched_woman.mp4", 0, None, False, None),  # reverted per note
    (V3 / "b10_forty.mp4", 0, None, False, None),  # reverted
    (V3 / "b12_cough.mp4", 0, None, False, None),        # same cough, death #2
    (V10 / "w1d.mp4", 0, None, False, None),          # reverted: child-voice "...Again."
    (V6 / "b13_cry2.mp4", 0, None, False, None),
    (V3 / "b14_three_lives.mp4", 0, None, False, None),
    (V10 / "w2d.mp4", 0, None, False, None),          # respawn: playing dead
    (V3 / "b15_five_lives.mp4", 0, 3.5, False, None),    # "...maybe five lives."
    (V10 / "w3d.mp4", 0, None, False, None),          # respawn: yoke drop
    (V6 / "b16_cure3.mp4", 0, None, False, None),
    (V3 / "b17_rant.mp4", 0, 2.90, False, None),
    (V3 / "b17_rant.mp4", 6.95, None, False, None),
    (V3 / "b18_germs.mp4", 0, None, False, None),
    (V7 / "b19_isa.mp4", 0, None, False, None),
    (V5 / "b20_solemn2.mp4", 0, None, False, None),
    (V8 / "b21_party3.mp4", 0, None, False, None),
    (V7 / "b22_wish3.mp4", 0, None, False, None),
    (V5 / "b23_finally2.mp4", 0, None, False, "omen_b23"),
    # --- Roman ---
    (V6 / "r1_sigh.mp4", 0, None, False, "silence"),
    (V7 / "r2_aq3.mp4", 0, None, False, None),
    (V3 / "r3_gesture_q.mp4", 0, None, False, None),
    (V9 / "r4_boil3.mp4", 0, None, False, None),
    (V5 / "r5_library2.mp4", 0, None, False, None),
    (V3 / "r6_scroll.mp4", 0, None, False, None),
    (V3 / "r7_bath_pitch.mp4", 0, None, False, None),
    (V13 / "r8_glass2.mp4", 0, None, False, None),   # "How do you MAKE glass?"
    (V13 / "r9_acid3.mp4", 0, None, False, None),    # high-schooler chemistry
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
    (V3 / "e3_flood.mp4", 0, None, False, None),        # the vow plays dry
    (V4 / "n5_type.mp4", 0, None, False, "ren_b"),      # music enters after the vow
    (V3 / "e4_montage.mp4", 0, None, False, None),
    (V4 / "n6_boiler.mp4", 0, None, False, "boiler"),
    (V4 / "n7_again.mp4", 0, None, False, "silence"),    # post-boom: no music
    (V4 / "n8_gauge.mp4", 0, None, False, None),
    (V13 / "n9_sixty3.mp4", 0, None, False, "m1926"),  # Cass in frame with the widow
    # --- 1926 ---
    (V5 / "m1_wake2.mp4", 0, None, False, None),
    (V5 / "m2_tram2.mp4", 0, None, False, None),
    (V12 / "m3_fix.mp4", 0, None, False, None),      # British read, "speedrun" fixed
    (V4 / "m4_teach.mp4", 0, None, False, None),
    (V7 / "m5_feet2.mp4", 0, None, False, None),
    (V4 / "m6_longtime.mp4", 0, None, False, None),
    (V4 / "m7_obit.mp4", 0, None, False, None),
    # --- The machine documented ---
    (V11 / "p1_dinner2.mp4", 0, None, False, "warmtail"),  # 1926 warmth runs into the dinner
    (V13 / "p2_board3.mp4", 0, None, False, None),   # "The Long Game" board
    (V12 / "p3_fix.mp4", 0, None, False, "machine"),  # "overrides" dubbed
    (V7 / "p4_exit3.mp4", 0, None, False, "silence"),
    # --- The arcade, again ---
    (V5 / "q1_off2.mp4", 0, None, False, "silence"),     # diegetic arcade only
    (V12 / "q2_fix.mp4", 0, None, False, None),      # freeze-cover: no double headset
    (V4 / "q3_walk.mp4", 0, None, False, None),
    (V6 / "q4_real2.mp4", 0, None, False, "omen_q4"),
    (V4 / "q5_nested.mp4", 0, None, False, "silence"),
    (V4 / "q6_longtime2.mp4", 0, None, False, None),
    (V6 / "q7_fail2.mp4", 0, 7.5, False, "end"),      # cuts mid-second attempt
    (ROOT / "outputs/end_reprise.mp4", 0, None, False, "silence"),  # cold-open hum over black
]

# era -> (music file, volume). "silence"/"boiler" handled via span logic below.
MUSIC = {
    "omen": ("mus_omen.m4a", 0.40),   # crescendo: full-span fade-in
    "arcade": ("mus_arcade2.m4a", 0.08),
    "bronze": ("mus_bronze.m4a", 0.09),      # chores montage only
    "omen_b23": ("mus_omen.m4a", 0.16),      # the gut-punch
    "ren_a": ("mus_ren.m4a", 0.07),          # arrival
    "ren_b": ("mus_ren.m4a", 0.12),          # the vow / flood montage
    "boiler": ("mus_boiler.m4a", 0.20),
    "m1926": ("mus_1926.m4a", 0.06),         # widow's nod -> 3s into the dinner
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

FREEZE = {}  # r3 tail-freeze removed (read as a weird pause)
GRADE = {"b7_name3": "eq=saturation=0.35:brightness=-0.02,"}  # grayer, washed-out

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
# merge the warmtail marker into m1926: the warm cue runs 3.0s into the dinner,
# then cuts out hard right as Peter pitches the booth
merged = []
for e, st, en in spans:
    if e == "warmtail":
        if merged and merged[-1][0] == "m1926":
            merged[-1] = ("m1926", merged[-1][1], st + 3.0)
        continue
    merged.append((e, st, en))
spans = [(e, st, en) for (e, st, en) in merged if e in MUSIC]

inputs, fc = [], []
for i, (path, ts, td, mute, era) in enumerate(CUT):
    d = offsets[i][1]
    fz = FREEZE.get(path.stem, 0)
    d0 = d - fz
    inputs += ["-i", str(path)]
    tpad = f"tpad=stop_mode=clone:stop_duration={fz}," if fz else ""
    grade = GRADE.get(path.stem, "")
    fc.append(f"[{i}:v]trim=start={ts}:end={ts + d0:.3f},setpts=PTS-STARTPTS,{tpad}{grade}"
              f"scale=854:480,setsar=1,fps=24[v{i}]")
    a = f"[{i}:a]atrim=start={ts}:end={ts + d0:.3f},asetpts=PTS-STARTPTS,aresample=48000"
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
    fade_in = span_d if era == "omen" else 1.5   # cold open: crescendo across the whole span
    fade_out = 0.25 if era == "m1926" else 3.0   # 1926 warmth cuts out at the pitch
    fc.append(f"[{idx}:a]aresample=48000,atrim=duration={span_d:.3f},"
              f"afade=t=in:d={fade_in:.3f},afade=t=out:st={max(0, span_d - fade_out):.3f}:d={fade_out},"
              f"volume={vol},adelay={int(s * 1000)}|{int(s * 1000)},"
              f"apad,atrim=duration={total:.3f}[m{k}]")
    mus_labels.append(f"[m{k}]")
fc.append("[ac]" + "".join(mus_labels)
          + f"amix=inputs={len(mus_labels) + 1}:normalize=0:duration=first[amx]")
fc.append(f"[amx]afade=t=out:st={total - 2.0:.2f}:d=2.0[am]")

graph_file = ROOT / "outputs/assemble_v13alt_graph.txt"
graph_file.write_text(";".join(fc))
print(f"{n} clips, {len(spans)} music spans, {total:.0f}s — encoding...", flush=True)
for e, s, t in spans:
    print(f"  music {e}: {s:.0f}s → {t:.0f}s")
subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs
               + ["-filter_complex_script", str(graph_file),
                  "-map", "[vc]", "-map", "[am]",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                  str(ROOT / "outputs/previews/preview_v13_alt_ending.mp4")], check=True)
print("wrote outputs/previews/preview_v13_alt_ending.mp4")
