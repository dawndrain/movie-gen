#!/usr/bin/env python3
"""Batch Nano Banana Pro images for THE VARIANCE.

Usage: python3 make_images.py <stage>     stage in {anchors, frames}
Skips images whose output file already exists (re-run = retry pass).
"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
GEN = HERE.parent / "gen.py"
ANCH = HERE / "anchors"
FRAMES = HERE / "frames"

# Baseline world grade (acts 1, 2, 5)
COLD = (
    "Photorealistic cinematic film still from a quiet dystopian science-fiction "
    "feature film in the vein of Never Let Me Go and Gattaca: muted desaturated "
    "teal-grey color grade, soft overcast light, clean minimal near-future "
    "architecture in pale concrete and frosted glass, everything ordered and "
    "gentle and slightly too clean, 35mm, shallow depth of field. No text, no "
    "watermark, no captions, no logos."
)
# The eleven days (act 3)
WARM = (
    "Photorealistic cinematic film still from a quiet science-fiction feature "
    "film, but this scene is ALIVE: warm golden-hour light, rich saturated "
    "living color, gentle handheld framing, air full of dust motes and light, "
    "35mm, shallow depth of field. No text, no watermark, no captions, no logos."
)

OREN = (
    "Oren, a man in his mid-twenties: short dark neatly-cut hair, a placid, "
    "gentle, unremarkable face, pale from indoor life, medium build, wearing a "
    "plain slate-blue standard-issue worker jumpsuit with a small blank fabric "
    "tab on the chest"
)
PETRA = (
    "Petra, a woman in her late forties: grey-streaked dark hair pinned back "
    "neatly, a calm, professionally kind, unlined face, wearing a charcoal-grey "
    "supervisor's uniform with a thin silver collar line"
)
DEZ = (
    "Dez, a woman in her late twenties: loose curly dark hair, bright quick "
    "eyes, a wide easy smile, wearing layered non-standard clothes — a "
    "rust-orange scarf and a patched olive canvas jacket — the only warm color "
    "in the frame"
)

# (name, aspect, prompt, [refs])
ANCHORS = [
    ("oren", "3:4",
     f"Full-body character portrait of {OREN}. He stands on a covered walkway "
     f"of pale concrete, expression neutral and mild, hands at his sides. "
     f"{COLD}", []),
    ("petra", "3:4",
     f"Full-body character portrait of {PETRA}. She stands in a minimal pale "
     f"office, posture composed, expression firm and empathic within bounds. "
     f"ONE single continuous photograph filling the whole frame — never a "
     f"collage, triptych, contact sheet or multi-panel layout, no borders. "
     f"{COLD}", []),
    ("dez", "3:4",
     f"Full-body character portrait of {DEZ}. She stands in a narrow old brick "
     f"street strung with warm hanging lights, caught mid-laugh. ONE single "
     f"full-bleed photograph filling the entire frame edge to edge — no film "
     f"borders, no frames, no collage. {WARM}", []),
    ("loc_path", "16:9",
     "Establishing wide shot, no people: a long covered pedestrian commuter "
     "path at dawn — a strip of pale concrete beneath a continuous arched "
     "transparent weather-shield, dormitory blocks of pale concrete on either "
     "side, the shield glass faintly reflective, a deep blue morning sky "
     f"visible through it. Symmetrical one-point perspective. {COLD}", []),
    ("loc_fab", "16:9",
     "Establishing wide shot: the interior of a vast fabrication complex — "
     "hundreds of identical white workstations in perfect rows receding into "
     "haze, each with a pale glowing screen, uniformed workers seated "
     f"motionless at them, high frosted skylights. {COLD}", []),
    ("loc_cafeteria", "16:9",
     "Establishing wide shot: a large clean institutional cafeteria — long "
     "pale tables in rows, uniformed workers eating quietly and identically, "
     f"soft even light, no decoration of any kind. {COLD}", []),
    ("loc_courtyard", "16:9",
     "Establishing shot, no people: a small forgotten concrete courtyard "
     "behind a dormitory block — one weathered bench; on the left wall a large "
     "old moisture stain shaped uncannily like a human figure running; in the "
     "center of the cracked pavement a single dead woody plant stem, waist "
     f"high, pushing up through the concrete like a monument. {COLD}", []),
    ("loc_archive", "16:9",
     "Establishing shot, no people: a forgotten archive room deep in an "
     "institutional building — steel shelves of old paper books, dust thick in "
     "a single shaft of light from a high window, decades undisturbed. "
     f"{COLD}", []),
    ("loc_oldquarter", "16:9",
     "Establishing wide shot: an old quarter of the city at dusk — narrow "
     "crooked streets of aged brick, warm strings of hanging lights, laundry "
     "lines between balconies, small crowded doorways spilling amber light, "
     f"people in varied colorful non-uniform clothes. {WARM}", []),
    ("loc_recal", "16:9",
     "Establishing shot, no people: a recalibration suite — a white, soft, "
     "kind clinical room with one reclined padded chair beneath a smooth "
     "white instrument halo on an articulated arm, diffuse shadowless light, "
     f"gentle and terrifying in its cleanliness. {COLD}", []),
]


def make(outdir: Path, name: str, aspect: str, prompt: str, refs: list,
         refdir: Path) -> str:
    out = outdir / f"{name}.png"
    if out.exists():
        return f"skip {name}"
    cmd = [sys.executable, str(GEN), "image", prompt,
           "--resolution", "2k", "--aspect_ratio", aspect]
    for r in refs:
        cmd += ["--image", str(refdir / f"{r}.png")]
    for attempt in (1, 2, 3):
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            src = Path(res.stdout.strip().splitlines()[-1])
            shutil.copy(src, out)
            return f"OK   {name}"
        err = (res.stdout + res.stderr).strip()[-300:]
        print(f"retry {name} (attempt {attempt}): {err}", flush=True)
    return f"FAIL {name}"


def load_frames():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "frames_spec", HERE / "frames_spec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FRAMES


def main():
    stage = sys.argv[1]
    if stage == "anchors":
        jobs, outdir = ANCHORS, ANCH
    elif stage == "frames":
        jobs, outdir = load_frames(), FRAMES
    else:
        sys.exit(f"unknown stage {stage}")
    outdir.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        futs = [pool.submit(make, outdir, n, a, p, r, ANCH) for n, a, p, r in jobs]
        for f in futs:
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
