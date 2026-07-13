#!/usr/bin/env python3
"""Assemble the narrated v2 cut (Chapters I-IV) into outputs/preview_v2.mp4.

Timeline rules: each shot may be tail-frozen (clone last frame) so its VO fits with at
most SPILL seconds carrying into the next shot; VO lines never overlap (later line waits
0.4s). Program audio ducks to 35% under narration. Final shot fades to white while the
last line finishes.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
V1, V2, VO = ROOT / "outputs/video", ROOT / "outputs/video2", ROOT / "vo"
SPILL = 1.5
DUCK = 0.35

# (shot, clip path) — order is the cut; VO file is vo/<shot>.mp3 if present
SHOTS = [
    ("1_1", V2 / "1_1_arcade_wide.mp4"),
    ("1_2", V2 / "1_2_placard.mp4"),
    ("1_3", V2 / "1_3_approach.mp4"),
    ("1_4", V2 / "1_4_screen_cu.mp4"),
    ("1_5", V2 / "1_5_deshawn_run.mp4"),
    ("1_6", V2 / "1_6_goading.mp4"),
    ("1_7", V2 / "1_7_toggle.mp4"),
    ("2_1", V1 / "2_1_eye_open.mp4"),
    ("2_2", V2 / "2_2_water_carry.mp4"),
    ("2_3", V1 / "2_3_mother.mp4"),
    ("2_4", V2 / "2_4_remembering.mp4"),
    ("2_5", V1 / "2_4_reset.mp4"),
    ("2_6", V1 / "2_5_touched_woman.mp4"),
    ("3_1", V2 / "3_1_salt_water.mp4"),
    ("3_2", V1 / "3_2_bronze_pour.mp4"),
    ("3_3", V2 / "3_3_good_years.mp4"),
    ("3_4", V1 / "3_3_water_greeting.mp4"),
    ("3_5", V1 / "3_4_bored_king.mp4"),
    ("3_6", V1 / "3_5_slave_nod.mp4"),
    ("3_7", V1 / "3_6_roman_wake.mp4"),
    ("4_1", V1 / "4_1_aqueduct.mp4"),
    ("4_2", V2 / "4_2_fountain_gesture.mp4"),
    ("4_3", V1 / "4_3_legend_scroll.mp4"),
    ("4_4", V1 / "4_4_workshop.mp4"),
    ("4_5", V1 / "4_5_vitriol.mp4"),
    ("4_6", V1 / "4_6_faustus.mp4"),
    ("4_7", V2 / "4_7_icecream_bench.mp4"),
    ("4_8", V1 / "4_7_bath_icecream.mp4"),
]


def dur(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def main() -> None:
    missing = [s for s, p in SHOTS if not p.exists()]
    if missing:
        raise SystemExit(f"missing clips: {missing}")

    # timeline
    t, prev_vo_end, plan = 0.0, 0.0, []
    for i, (shot, path) in enumerate(SHOTS):
        clip = dur(path)
        vo = VO / f"{shot}.mp3"
        vo_d = dur(vo) if vo.exists() else 0.0
        if vo_d:
            vo_start = max(t + 0.15, prev_vo_end + 0.4)
            vo_end = vo_start + vo_d
            prev_vo_end = vo_end
            last = i == len(SHOTS) - 1
            need = vo_end - t + (1.5 if last else 0.5 - SPILL)
            target = max(clip, need)
        else:
            vo_start = None
            target = clip
        plan.append((shot, path, clip, target, vo_start, vo_d))
        frozen = target - clip
        print(f"{shot}: clip {clip:5.1f}s -> {target:5.1f}s"
              + (f" (freeze {frozen:.1f}s)" if frozen > 0.05 else "")
              + (f", vo @ {vo_start:.1f}s ({vo_d:.1f}s)" if vo_start else ""))
        t += target

    total = t
    print(f"total: {total:.1f}s")

    # ffmpeg graph
    inputs, fc = [], []
    vo_shots = [(s, vs, vd) for s, _, _, _, vs, vd in plan if vs is not None]
    for i, (shot, path, clip, target, _, _) in enumerate(plan):
        inputs += ["-i", str(path)]
        pad = max(0.0, target - clip)
        vf = f"[{i}:v]scale=854:480,setsar=1,fps=24"
        if pad > 0.05:
            vf += f",tpad=stop_mode=clone:stop_duration={pad:.3f}"
        if i == len(plan) - 1:
            vf += f",fade=t=out:st={target - 1.8:.3f}:d=1.8:color=white"
        fc.append(vf + f",trim=duration={target:.3f}[v{i}]")
        fc.append(f"[{i}:a]aresample=48000,apad,atrim=duration={target:.3f}[a{i}]")
    n = len(plan)
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")

    duck = "+".join(f"between(t,{vs:.2f},{vs + vd:.2f})" for _, vs, vd in vo_shots)
    fc.append(f"[ac]volume={DUCK}:enable='{duck}'[acd]")
    for j, (shot, vs, _) in enumerate(vo_shots):
        inputs += ["-i", str(VO / f"{shot}.mp3")]
        ms = int(vs * 1000)
        fc.append(f"[{n + j}:a]aresample=48000,adelay={ms}|{ms},volume=1.9[n{j}]")
    fc.append("[acd]" + "".join(f"[n{j}]" for j in range(len(vo_shots)))
              + f"amix=inputs={len(vo_shots) + 1}:duration=first:normalize=0,"
              + f"afade=t=out:st={total - 1.8:.3f}:d=1.8[am]")

    graph = ";".join(fc)
    (ROOT / "outputs/assemble_graph.txt").write_text(graph)
    cmd = (["ffmpeg", "-y", "-v", "error"] + inputs
           + ["-filter_complex_script", str(ROOT / "outputs/assemble_graph.txt"),
              "-map", "[vc]", "-map", "[am]",
              "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
              "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
              str(ROOT / "outputs/preview_v2.mp4")])
    print("encoding...", flush=True)
    subprocess.run(cmd, check=True)
    print("wrote outputs/preview_v2.mp4")


main()
