#!/usr/bin/env python3
"""Assemble the v3 comedy cut into outputs/preview_v3.mp4. No narration — dialogue
carries everything. Supports per-entry trims (for the thud running gag) and per-entry
mute. Straight concat; era jumps use the white washes baked into the clips."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
V1, V2, V3 = ROOT / "outputs/video", ROOT / "outputs/video2", ROOT / "outputs/video3"

# (clip path, trim_start, trim_dur, mute) — trim_dur None = to end
CUT = [
    # --- Arcade ---
    (V3 / "a1_ddr.mp4", 0, None, False),
    (V3 / "a2_placard.mp4", 0, None, False),
    (V2 / "1_4_screen_cu.mp4", 0, None, False),          # instructions CU
    (V3 / "a4_milo_arrives.mp4", 0, None, False),
    (V3 / "a5_what_it_means.mp4", 0, None, False),
    (V3 / "a6_out_of_order.mp4", 0, None, False),
    (V3 / "a7_dibs.mp4", 0, None, False),
    (V3 / "a8_deshawn_out.mp4", 0, None, False),
    (V3 / "a9_your_turn.mp4", 0, None, False),
    (V3 / "a10_harder.mp4", 0, None, False),
    # --- Bronze ---
    (V3 / "b1_wake_mom.mp4", 0, None, False),
    (V2 / "2_2_water_carry.mp4", 0, None, False),        # water chore
    (V3 / "b3_goat.mp4", 0, None, False),
    (V3 / "b4_collapse.mp4", 0, None, False),
    (V3 / "b5_afterlife.mp4", 0, None, False),
    (V3 / "b6_wake2_scream.mp4", 0, None, False),
    (V3 / "b7_my_name.mp4", 0, None, False),
    (V3 / "b8_how_do_i_leave.mp4", 0, None, False),
    (V1 / "2_5_touched_woman.mp4", 0, None, False),      # forty summers
    (V3 / "b10_forty.mp4", 0, None, False),
    (V3 / "b12_cough.mp4", 0, None, False),
    (V3 / "b11_thud.mp4", 0, None, False),
    (V3 / "b13_cry.mp4", 0, None, False),
    (V3 / "b14_three_lives.mp4", 0, None, False),
    (V3 / "b11_thud.mp4", 0, 2.2, False),
    (V3 / "b15_five_lives.mp4", 0, 3.5, False),          # "...maybe five lives."
    (V3 / "b11_thud.mp4", 0, 2.2, False),
    (V3 / "b11_thud.mp4", 0, 2.2, False),
    (V3 / "b15_five_lives.mp4", 3.5, None, False),       # eyes close, mom mid-lecture
    (V3 / "b16_cure.mp4", 0, None, False),
    (V3 / "b17_rant.mp4", 0, None, False),
    (V3 / "b18_germs.mp4", 0, None, False),
    (V2 / "3_1_salt_water.mp4", 0, None, False),         # saves Isa
    (V3 / "b20_solemn.mp4", 0, None, False),
    (V2 / "3_3_good_years.mp4", 0, None, False),         # party
    (V3 / "b22_wish.mp4", 0, None, False),
    (V3 / "b23_finally.mp4", 0, None, False),
    # --- Roman ---
    (V1 / "3_6_roman_wake.mp4", 0, None, False),
    (V1 / "4_1_aqueduct.mp4", 0, None, True),            # user: no audio
    (V3 / "r3_gesture_q.mp4", 0, None, False),
    (V3 / "r4_boil_it.mp4", 0, None, False),
    (V3 / "r5_library.mp4", 0, None, False),
    (V3 / "r6_scroll.mp4", 0, None, False),
    (V3 / "r7_bath_pitch.mp4", 0, None, False),
    (V3 / "r8_glass.mp4", 0, None, False),
    (V3 / "r9_dictate_acid.mp4", 0, None, False),
    (V3 / "r10_page.mp4", 0, None, False),
    (V3 / "r11_dictate_blood.mp4", 0, None, False),
    (V3 / "r12_salt_ice.mp4", 0, None, False),
    (V3 / "r13_sweet.mp4", 0, None, False),
    # --- Enlightenment teaser ---
    (V3 / "e1_library2.mp4", 0, None, False),
    (V3 / "e2_fire.mp4", 0, None, False),
    (V3 / "e3_flood.mp4", 0, None, False),
    (V3 / "e4_montage.mp4", 0, None, False),
]


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


missing = [str(p) for p, *_ in CUT if not p.exists()]
if missing:
    raise SystemExit("missing clips:\n" + "\n".join(sorted(set(missing))))

inputs, fc, total = [], [], 0.0
for i, (path, ts, td, mute) in enumerate(CUT):
    d = td if td else dur(path) - ts
    total += d
    inputs += ["-i", str(path)]
    fc.append(f"[{i}:v]trim=start={ts}:duration={ts + d:.3f}".replace(f"duration={ts + d:.3f}", f"end={ts + d:.3f}")
              + f",setpts=PTS-STARTPTS,scale=854:480,setsar=1,fps=24[v{i}]")
    a = f"[{i}:a]atrim=start={ts}:end={ts + d:.3f},asetpts=PTS-STARTPTS,aresample=48000"
    if mute:
        a += ",volume=0"
    fc.append(a + f",apad,atrim=duration={d:.3f}[a{i}]")
n = len(CUT)
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
fc.append(f"[ac]afade=t=out:st={total - 1.5:.2f}:d=1.5[am]")

graph_file = ROOT / "outputs/assemble_v3_graph.txt"
graph_file.write_text(";".join(fc))
print(f"{n} entries, {total:.0f}s — encoding...", flush=True)
subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs
               + ["-filter_complex_script", str(graph_file),
                  "-map", "[vc]", "-map", "[am]",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                  str(ROOT / "outputs/preview_v3.mp4")], check=True)
print("wrote outputs/preview_v3.mp4")
