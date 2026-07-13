#!/usr/bin/env python3
"""Build the DCC animatic: TTS dialogue + stills held for their cut windows
with quiver-free perspective Ken Burns + music/ambience beds at LUFS-derived
levels. Specs live in spec.py.

Usage: python3 make_animatic.py tts          # vo/ mp3s (skips existing)
       python3 make_animatic.py build        # per-shot segments + concat
       python3 make_animatic.py mix [label]  # + music/ambience -> outputs/animatic_<label>.mp4
       python3 make_animatic.py all [label]
"""
import json
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import spec

HERE = Path(__file__).parent
VO = HERE / "vo"
SEG = HERE / "outputs" / "animatic_segs"
FRAMES = HERE / "frames"
MUS = HERE / "music"
AMB = HERE / "ambience"
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()

W, H, FPS, SS = 1280, 720, 24, 2
HEAD, GAP, TAIL = 0.5, 0.5, 0.9
DEFAULT_HOLD = 4.0
FONT = "/System/Library/Fonts/Helvetica.ttc"


def dur_of(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


# ------------------------------------------------------------------ tts ----

def tts_one(shot: str, i: int, speaker: str, text: str) -> str:
    out = VO / f"{shot}_{i}_{speaker}.mp3"
    if out.exists():
        return f"skip {out.name}"
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{spec.CAST[speaker]}",
        data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2"}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    err = ""
    for attempt in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out.write_bytes(r.read())
            return f"OK   {out.name}"
        except Exception as e:
            err = str(e)
    return f"FAIL {out.name}: {err}"


def tts_phase():
    VO.mkdir(exist_ok=True)
    jobs = [(s, i, sp, tx) for s in spec.ORDER
            for i, (sp, tx) in enumerate(spec.LINES[s])]
    print(f"{len(jobs)} lines, {sum(len(t) for *_, t in jobs)} chars")
    with ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(lambda j: tts_one(*j), jobs):
            print(r, flush=True)


# ------------------------------------------------------- segments (build) ----

def kenburns_vf(idx: int, shot: str, dur: float) -> str:
    """perspective-based sub-pixel Ken Burns (see homo_sapien/animatic.py)."""
    n = max(int(round(dur * FPS)), 2)
    if shot in spec.KB_LOCK:
        return (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                f"crop={W}:{H},setsar=1,fps={FPS}")
    move = "in" if idx % 2 == 0 else "out"
    amt = 0.045
    z = (f"(1+{amt}*on/{n - 1})" if move == "in"
         else f"({1 + amt}-{amt}*on/{n - 1})")
    ww, hh = W * SS, H * SS
    l, r = f"({ww}-{ww}/{z})/2", f"({ww}+{ww}/{z})/2"
    t, b = f"({hh}-{hh}/{z})/2", f"({hh}+{hh}/{z})/2"
    return (f"scale={ww}:{hh}:force_original_aspect_ratio=increase,"
            f"crop={ww}:{hh},fps={FPS},"
            f"perspective=eval=frame:interpolation=cubic:"
            f"x0='{l}':y0='{t}':x1='{r}':y1='{t}':"
            f"x2='{l}':y2='{b}':x3='{r}':y3='{b}',"
            f"scale={W}:{H},setsar=1")


def build_segment(idx: int, shot: str) -> tuple[Path, float]:
    lines = spec.LINES[shot]
    mp3s = [VO / f"{shot}_{i}_{sp}.mp3" for i, (sp, _) in enumerate(lines)]
    durs = [dur_of(m) for m in mp3s]
    total = (HEAD + sum(durs) + GAP * max(0, len(durs) - 1) + TAIL) if durs \
        else spec.SILENT_HOLD.get(shot, DEFAULT_HOLD)
    mp4 = SEG / f"{idx:02d}_{shot}.mp4"
    if mp4.exists():
        return mp4, dur_of(mp4)

    vf = kenburns_vf(idx, shot, total)
    if Path(FONT).exists():
        vf += (f",drawtext=fontfile={FONT}:text='{shot}':x=10:y=10:fontsize=16:"
               f"fontcolor=white@0.55:box=1:boxcolor=black@0.3:boxborderw=4")
    cmd = ["ffmpeg", "-y", "-v", "error",
           "-loop", "1", "-t", f"{total:.3f}", "-i", str(FRAMES / f"{shot}.png")]
    for m in mp3s:
        cmd += ["-i", str(m)]
    af = f"aevalsrc=0|0:s=48000:d={HEAD}[l];"
    parts = "[l]"
    for i in range(len(mp3s)):
        af += f"[{i + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo[a{i}];"
        parts += f"[a{i}]"
        if i < len(mp3s) - 1:
            af += f"aevalsrc=0|0:s=48000:d={GAP}[g{i}];"
            parts += f"[g{i}]"
    af += f"aevalsrc=0|0:s=48000:d={TAIL}[t];"
    parts += "[t]"
    af += f"{parts}concat=n={len(mp3s) * 2 + 1}:v=0:a=1[a]"
    if not mp3s:
        af = f"aevalsrc=0|0:s=48000:d={total:.3f}[a]"
    cmd += ["-filter_complex", f"[0:v]{vf},format=yuv420p[v];{af}",
            "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
            "-c:a", "aac", "-ar", "48000", "-b:a", "160k", str(mp4)]
    subprocess.run(cmd, check=True)
    return mp4, total


def build_phase() -> list[tuple[str, Path, float]]:
    SEG.mkdir(parents=True, exist_ok=True)
    missing = [s for s in spec.ORDER if not (FRAMES / f"{s}.png").exists()]
    if missing:
        raise SystemExit(f"missing frames: {missing}")
    out = []
    for idx, shot in enumerate(spec.ORDER):
        mp4, d = build_segment(idx, shot)
        out.append((shot, mp4, d))
        print(f"seg {shot}: {d:.1f}s", flush=True)
    return out


# ----------------------------------------------------------------- mix ----

def spans_from_marks(marks: dict, offsets: dict, total: float,
                     end_words: set) -> list[tuple[str, float, float]]:
    spans, cur = [], None
    for shot in spec.ORDER:
        if shot in marks:
            if cur:
                spans.append((cur[0], cur[1], offsets[shot]))
                cur = None
            if marks[shot] not in end_words:
                cur = (marks[shot], offsets[shot])
    if cur:
        spans.append((cur[0], cur[1], total))
    return spans


def measure_lufs(p: Path) -> float:
    res = subprocess.run(
        ["ffmpeg", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True)
    m = re.findall(r"I:\s*(-?[\d.]+)\s*LUFS", res.stderr)
    return float(m[-1])


def mix_phase(label: str):
    segs = build_phase()
    offsets, t = {}, 0.0
    for shot, _, d in segs:
        offsets[shot] = t
        t += d
    total = t

    concat_list = SEG / "concat.txt"
    concat_list.write_text("".join(f"file '{p.resolve()}'\n" for _, p, _ in segs))
    base = SEG / "_base.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(concat_list), "-c", "copy", str(base)], check=True)

    anchor = measure_lufs(base)
    mus_gain = (anchor + spec.MUSIC_DB) - (-30.0)
    amb_gain = (anchor + spec.AMB_DB) - (-30.0)
    print(f"dialogue anchor {anchor:.1f} LUFS -> music {mus_gain:+.1f} dB, "
          f"ambience {amb_gain:+.1f} dB")

    mspans = spans_from_marks(spec.MUSIC_MARKS, offsets, total, {"silence"})
    aspans = spans_from_marks(spec.AMB_MARKS, offsets, total, {"none"})
    mspans = [(c, s, e) for c, s, e in mspans if (MUS / f"mus_{c}.m4a").exists()]
    aspans = [(b, s, e) for b, s, e in aspans if (AMB / f"{b}_loop.m4a").exists()]
    print(f"{len(mspans)} music spans, {len(aspans)} ambience spans")

    inputs = ["-i", str(base)]
    fc, labels = [], []
    for k, (name, s, e) in enumerate(mspans + aspans):
        gain = mus_gain if k < len(mspans) else amb_gain
        f = (MUS / f"mus_{name}.m4a") if k < len(mspans) else (AMB / f"{name}_loop.m4a")
        idx = k + 1
        inputs += ["-stream_loop", "-1", "-i", str(f)]
        d = e - s
        fc.append(f"[{idx}:a]aresample=48000,atrim=duration={d:.3f},"
                  f"afade=t=in:d=1.5,afade=t=out:st={max(0, d - 3):.3f}:d=3,"
                  f"volume={gain:.1f}dB,adelay={int(s * 1000)}|{int(s * 1000)},"
                  f"apad,atrim=duration={total:.3f}[s{k}]")
        labels.append(f"[s{k}]")
    fc.append("[0:a]" + "".join(labels)
              + f"amix=inputs={len(labels) + 1}:normalize=0:duration=first,"
              + f"afade=t=out:st={total - 3:.2f}:d=3[am]")
    graph = SEG / "mix_graph.txt"
    graph.write_text(";".join(fc))
    out = HERE / "outputs" / f"animatic_{label}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs,
                    "-filter_complex_script", str(graph),
                    "-map", "0:v", "-map", "[am]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    str(out)], check=True)
    print(f"wrote {out} — {total / 60:.1f} min, {len(segs)} shots")


if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    label = sys.argv[2] if len(sys.argv) > 2 else "v1"
    if phase in ("tts", "all"):
        tts_phase()
    if phase == "build":
        build_phase()
    if phase in ("mix", "all"):
        mix_phase(label)
