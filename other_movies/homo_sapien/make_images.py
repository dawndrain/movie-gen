#!/usr/bin/env python3
"""Batch Nano Banana Pro images for HOME SAPIEN (Lenka music video).

Usage: python3 make_images.py <stage>   stage in {anchors1, anchors2, frames}
Skips images whose output file already exists (re-run = retry pass).
"""
import subprocess
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
GEN = HERE.parent / "gen.py"
ANCH = HERE / "anchors"
FRAMES = HERE / "frames"

STYLE = (
    "Photorealistic cinematic film still from a warm, handmade, slightly "
    "whimsical indie feature — 35mm, shallow depth of field, soft golden "
    "practical light, gentle film grain, tactile textures of wool, wood, "
    "paper and skin. Storybook warmth, never clinical, never chrome, never "
    "sci-fi blue. Sincere and a little funny. No text, no watermark, no "
    "captions, no subtitles. ONE single continuous photograph filling the "
    "whole frame, no borders, no collage, no split screen."
)

# Creatures MUST be photoreal living animals. The words "handmade / tactile /
# wool" in STYLE bled into the first fish + monkey anchors and produced KNITTED
# FELT PUPPETS — charming, but a completely different film from the photoreal
# humans. Creature prompts use this instead of STYLE.
CREATURE = (
    "Photorealistic wildlife cinematography — a real living animal, real wet "
    "skin, real fur, real eyes, natural history documentary realism, shot on "
    "35mm with a long lens, warm golden natural light, shallow depth of "
    "field, gentle film grain. Absolutely NOT knitted, NOT felt, NOT wool, "
    "NOT a puppet, NOT a plush toy, NOT clay, NOT a cartoon, NOT an "
    "illustration — a real photographed animal. No text, no watermark. ONE "
    "single continuous photograph filling the whole frame, no borders, no "
    "collage."
)

# Cosmic/creature shots share a painterly, hand-mixed look so they sit in the
# same world as the kitchen — no Hubble photorealism.
COSMIC = (
    "Painterly, hand-mixed, tactile cosmos — like ink and glitter suspended "
    "in water, warm amber and deep teal, not a photographic telescope image. "
    "Intimate rather than epic. No text, no watermark. ONE single continuous "
    "image filling the whole frame, no borders, no collage."
)

# canonical appearance locks — reuse VERBATIM in frame prompts
W = {
    "may":
        "a warm, funny woman of about thirty-two with dark curly shoulder-"
        "length hair, freckles, laugh lines and an enormous uncontrollable "
        "grin, wearing a soft coral-orange knitted cardigan over a cream "
        "t-shirt, faded jeans, and bare feet",
    "ollie":
        "a tall soft-featured gentle man of about thirty-four with messy "
        "light-brown hair, round wire glasses, a slightly startled kind face "
        "and stubble, wearing a rumpled teal-blue button-down shirt with the "
        "sleeves rolled up and grey jeans",
    "may_old":
        "the same woman aged to about seventy-five — the same freckles, the "
        "same laugh lines now deep, the same enormous grin, her curly hair "
        "now silver-white and short, wearing the same soft coral-orange "
        "knitted cardigan, now visibly worn and mended, over a cream blouse, "
        "and bare feet",
    "ollie_old":
        "the same man aged to about seventy-seven — the same round wire "
        "glasses, the same kind startled face, now thin white hair and a "
        "lined face, slightly stooped, wearing the same teal-blue button-"
        "down shirt, now faded and soft with age",
    "may_sapien":
        "a woman with EXACTLY the same face as the reference — the same "
        "freckles, the same enormous grin, the same dark curly hair, now "
        "matted and tied back with sinew — living forty thousand years ago: "
        "warm red-ochre paint in stripes across her cheekbones, wearing "
        "soft hide and fur clothing with a rust-orange ochre-dyed hide wrap "
        "across one shoulder, bone beads at her throat",
    "ollie_sapien":
        "a man with EXACTLY the same face as the reference — the same soft "
        "startled kind features, the same stubble, the same messy light-"
        "brown hair, now long and tangled (no glasses) — living forty "
        "thousand years ago: blue-grey clay markings on his forehead, "
        "wearing rough hide clothing with a plain teal-grey fur cloak over "
        "his shoulders. The cloak is a PLAIN CUT PANEL OF FUR ONLY — it has "
        "NO animal head, NO animal face, NO eyes, NO ears, NO snout, NO paws "
        "and NO tail attached to it anywhere; it must never look like a whole "
        "dead animal draped over him, only like a piece of worked hide",
    "kid":
        "a small round-faced four-year-old girl with wild dark curly hair "
        "exactly like her mother's, wearing a mustard-yellow t-shirt and "
        "spotty leggings, permanently mid-sprint",
}

# (name, aspect, prompt, [refs])
ANCHORS1 = [
    ("may", "3:4",
     f"Full-body character portrait of {W['may']}. She stands barefoot in a "
     f"small warm kitchen at night, holding a chipped mug in both hands, "
     f"laughing at something off camera. She is the ONLY figure in the frame. "
     f"{STYLE}", []),
    ("ollie", "3:4",
     f"Full-body character portrait of {W['ollie']}. He stands in a doorway "
     f"of a small warm kitchen at night, half asleep, hair flat on one side, "
     f"holding a book he has forgotten he is holding. He is the ONLY figure "
     f"in the frame. {STYLE}", []),
    ("kid", "3:4",
     f"Full-body character portrait of {W['kid']}. She stands on a wooden "
     f"floor in a cluttered family home, arms out, about to run somewhere "
     f"very fast for no reason. She is the ONLY figure in the frame. "
     f"{STYLE}", []),
    # ---- creature-pair anchors (recur in the museum dioramas at 3:15) ----
    ("pair_fish", "16:9",
     f"Two small REAL LIVING prehistoric lobe-finned fish hanging side by "
     f"side in green underwater light — wet iridescent scales, real slick "
     f"skin, real fins, photographed underwater with a macro lens. One is "
     f"warm coral-orange, the other deep teal-blue. Their stubby fins are "
     f"touching and their blunt snouts are nudged together. They are the "
     f"ONLY two creatures in the frame. Sweet and a little goofy, but they "
     f"are REAL ANIMALS. {CREATURE}", []),
    ("pair_monkeys", "16:9",
     f"Two small REAL LIVING early primates — real fur, real skin, real "
     f"eyes, photographed with a long lens in the wild — hanging upside-down "
     f"by their tails from the same jungle branch in dappled golden light, "
     f"holding hands, foreheads bonked together, eyes closed, blissful. One "
     f"has warm coral-orange fur, the other cool teal-grey fur. They are the "
     f"ONLY two creatures in the frame. They are REAL ANIMALS. {CREATURE}",
     []),
    ("pair_hominids", "16:9",
     f"Two early hominids — australopithecine, small, upright, and covered in "
     f"natural body hair — standing forehead to forehead in silhouette on an "
     f"African savanna at dawn, tender and still, holding each other's "
     f"forearms. They wear NO CLOTHING AT ALL and carry nothing: no hides, no "
     f"furs, no scraps of cloth, no tools, no ornaments — these are animals, "
     f"millions of years before clothing was invented, and they are naked and "
     f"hairy. The colour pairing lives in their natural FUR instead: one has "
     f"warm rust-orange hair, the other cool blue-grey hair, exactly like the "
     f"two primates before them. Seen in silhouette and rim-light so they read "
     f"as shapes, dignified and unsensational. They are the ONLY two figures "
     f"in the frame. Golden backlight, tall dry grass. {CREATURE}", []),
    # ---- location plates ----
    ("loc_kitchen", "16:9",
     f"Establishing interior shot, NO PEOPLE: a small shabby beloved kitchen "
     f"at one in the morning — worn yellow lino floor, mismatched wooden "
     f"chairs, a steaming kettle on the hob, one warm tungsten pendant lamp, "
     f"crowded shelves, a fridge covered in postcards and magnets, and one "
     f"window of deep blue night. Cosy, cluttered, deeply lived-in. "
     f"{STYLE}", []),
    ("loc_cave", "16:9",
     f"Establishing interior shot, NO PEOPLE: the mouth of a shallow cave "
     f"forty thousand years ago, at night — a small fire burning, warm light "
     f"on a rough pale rock wall, hide bedding, simple tools, and a sky of "
     f"enormous unpolluted stars beyond the cave mouth. Intimate and safe, "
     f"not grim. {STYLE}", []),
    ("loc_museum", "16:9",
     f"Establishing interior shot, NO PEOPLE: the great hall of an old "
     f"natural history museum after closing time — a whale skeleton "
     f"suspended overhead, a vaulted glass-and-iron dome, dark wood and "
     f"brass diorama cases glowing softly along both walls, a polished stone "
     f"floor, warm low after-hours lighting, dust in the light. Empty, "
     f"hushed, magical. {STYLE}", []),
    ("loc_savanna", "16:9",
     f"Establishing wide shot, NO PEOPLE AND NOTHING MAN-MADE: a completely "
     f"empty African savanna at dawn — tall dry golden grass, a lone "
     f"flat-topped acacia, low mist, an enormous orange sun just clearing "
     f"the horizon. No fences, no cloth, no bedding, no tools, no objects of "
     f"any kind — only grass, tree, mist and sun. {STYLE}", []),
]

# second pass: anchors that reference first-pass anchors
ANCHORS2 = [
    ("may_old", "3:4",
     f"Full-body character portrait of the SAME woman as in the reference "
     f"image, aged to seventy-five: {W['may_old']}. Her face is clearly "
     f"recognizably the same person as the reference. She stands barefoot in "
     f"a small warm kitchen at night, laughing. She is the ONLY figure in "
     f"the frame. {STYLE}", ["may"]),
    ("ollie_old", "3:4",
     f"Full-body character portrait of the SAME man as in the reference "
     f"image, aged to seventy-seven: {W['ollie_old']}. His face is clearly "
     f"recognizably the same person as the reference. He stands in a kitchen "
     f"doorway at night, gentle and amused. He is the ONLY figure in the "
     f"frame. {STYLE}", ["ollie"]),
    ("may_sapien", "3:4",
     f"Full-body character portrait of {W['may_sapien']}. She stands at the "
     f"mouth of a cave in firelight, grinning with total confidence. She is "
     f"the ONLY figure in the frame. {STYLE}", ["may"]),
    ("ollie_sapien", "3:4",
     f"Full-body character portrait of {W['ollie_sapien']}. He stands at the "
     f"mouth of a cave in firelight, holding a badly-made spear, looking "
     f"gently bewildered. He is the ONLY figure in the frame. {STYLE}",
     ["ollie"]),
]


def load_frames():
    import importlib.util
    spec = importlib.util.spec_from_file_location("frames_spec", HERE / "frames_spec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FRAMES


def resolve_ref(r: str) -> Path:
    p = ANCH / f"{r}.png"
    if p.exists():
        return p
    raise FileNotFoundError(f"ref {r} not found in {ANCH}")


def make(outdir: Path, name: str, aspect: str, prompt: str, refs: list[str]) -> str:
    out = outdir / f"{name}.png"
    if out.exists():
        return f"skip {name}"
    cmd = [sys.executable, str(GEN), "image", prompt,
           "--resolution", "2k", "--aspect_ratio", aspect]
    for r in refs:
        cmd += ["--image", str(resolve_ref(r))]
    for attempt in (1, 2, 3):
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            src = Path(res.stdout.strip().splitlines()[-1])
            shutil.copy(src, out)
            return f"OK   {name}"
        err = (res.stdout + res.stderr).strip()[-300:]
        print(f"retry {name} (attempt {attempt}): {err}", flush=True)
    return f"FAIL {name}"


def main():
    stage = sys.argv[1]
    if stage == "anchors1":
        jobs, outdir = ANCHORS1, ANCH
    elif stage == "anchors2":
        jobs, outdir = ANCHORS2, ANCH
    elif stage == "frames":
        jobs, outdir = load_frames(), FRAMES
    else:
        sys.exit(f"unknown stage {stage}")
    outdir.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        futs = [pool.submit(make, outdir, n, a, p, r) for n, a, p, r in jobs]
        for f in futs:
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
