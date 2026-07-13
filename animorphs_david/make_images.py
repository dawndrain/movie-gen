#!/usr/bin/env python3
"""Batch Nano Banana Pro images for ANIMORPHS: THE DAVID TRILOGY.

Usage: python3 make_images.py <stage>     stage in {anchors1, anchors2, frames}
Skips images whose output file already exists (re-run = retry pass).
"""
import subprocess
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
GEN = HERE.parent / "gen.py"
HB_ANCH = HERE.parent / "animorphs" / "anchors"   # reuse HB hawk/andalite anchors
ANCH = HERE / "anchors"
FRAMES = HERE / "frames"

STYLE = (
    "Photorealistic cinematic film still from a live-action science-fiction "
    "thriller feature film, IMAX 35mm, natural volumetric lighting, "
    "practical-creature-effects realism, rich moody color grade. No text, no "
    "watermark, no captions, no cartoon or anime styling."
)

ANDALITE = (
    "an Andalite: a graceful alien centaur with a deer-like four-legged lower body "
    "covered in short blue-and-tan fur, a slim upright torso with two slender "
    "many-fingered arms, a triangular face with NO mouth, two large almond-shaped "
    "main eyes, two additional small eyes on flexible stalks on top of the head, "
    "and a long muscular tail arcing forward over the back, ending in a wicked "
    "curved scythe blade"
)

# canonical wardrobe (used again in frame + video prompts)
WARDROBE = {
    "jake":   "a sixteen-year-old boy, tall and broad-shouldered, short brown hair, "
              "steady serious brown eyes, olive-drab t-shirt and jeans",
    "rachel": "a sixteen-year-old girl, tall and athletic, long straight blonde "
              "hair, striking model-like face with fierce blue eyes, light-blue "
              "denim jacket over a white top and jeans",
    "cassie": "a sixteen-year-old Black girl, short, practical and warm, very "
              "short natural hair, kind steady dark eyes, tan work overalls over "
              "a green long-sleeve shirt, work boots",
    "marco":  "a sixteen-year-old Latino boy, shorter and wiry, shoulder-length "
              "dark hair, sharp amused dark eyes and a half-smirk, dark-red "
              "flannel shirt open over a black t-shirt, jeans",
    "david":  "a sixteen-year-old boy, lean and wiry, sandy-blond hair, sharp "
              "fox-like handsome face with pale calculating blue eyes, worn grey "
              "zip-up hoodie over a white t-shirt, dark jeans",
}

# (name, aspect, prompt, [refs])  refs resolve against ANCH then HB_ANCH
ANCHORS1 = [
    ("jake", "3:4",
     f"Full-body character portrait of {WARDROBE['jake']}. He stands in a dim barn "
     f"doorway at dusk, weight square, the posture of a reluctant leader carrying "
     f"too much. {STYLE}", []),
    ("rachel", "3:4",
     f"Full-body character portrait of {WARDROBE['rachel']}. She stands in a barn "
     f"lit by lantern light, chin up, arms loose, utterly unafraid. She is the ONLY "
     f"figure in the frame; the barn behind her is empty — no people, no animals, "
     f"no creatures. {STYLE}", []),
    ("cassie", "3:4",
     f"Full-body character portrait of {WARDROBE['cassie']}. She stands among "
     f"wire animal cages in a barn wildlife clinic, a bandaged bird on the table "
     f"beside her. {STYLE}", []),
    ("marco", "3:4",
     f"Full-body character portrait of {WARDROBE['marco']}. He leans against a "
     f"barn post with his arms crossed, one eyebrow raised. He is the ONLY figure "
     f"in the frame; the barn behind him is empty — no people, no animals, no "
     f"creatures. {STYLE}", []),
    ("david", "3:4",
     f"Full-body character portrait of {WARDROBE['david']}. He stands on a night "
     f"suburban street half-lit by a streetlamp, hands in hoodie pockets, a "
     f"glowing blue cube tucked under one arm, expression somewhere between "
     f"charm and menace. {STYLE}", []),
    ("loc_construction", "16:9",
     "Establishing wide shot, no characters: a half-built suburban subdivision at "
     "night — skeletal plywood house frames, mud and tire ruts, stacked lumber, "
     "chain-link fence, a single distant work light, cold moonlight. Ominous and "
     f"quiet. {STYLE}", []),
    ("loc_barn", "16:9",
     "Establishing interior shot, no characters: a big old wooden barn used as a "
     "wildlife rescue clinic at night — hay bales, rows of wire cages with "
     "recovering owls and raccoons, a single hanging lantern making a warm pool "
     "of light, wide gapped plank floorboards, moonlight through slat gaps. "
     f"{STYLE}", []),
    ("loc_hotel", "16:9",
     "Establishing wide shot, no characters: a glassy oceanfront resort hotel at "
     "night hosting an international summit — flags of many nations along the "
     "drive, black SUVs, security barricades, warm lobby light spilling out. "
     f"{STYLE}", []),
    ("loc_meadow", "16:9",
     "Establishing wide shot, no characters: a quiet meadow at golden hour with "
     "one huge lone oak tree, long grass, low sun through drifting seed fluff, "
     f"forest edge beyond. Peaceful, warm. {STYLE}", []),
    ("loc_cove", "16:9",
     "Establishing wide shot, no characters: a rocky Pacific cove at cold grey "
     "dawn — cliffs, sea stacks, tide pools, wet black boulders, low mist over "
     f"the water, a narrow strip of dark sand. Tense, expectant. {STYLE}", []),
    ("loc_island", "16:9",
     "Establishing wide shot, no characters: a tiny barren rock island a few "
     "hundred yards offshore — bare wave-washed grey stone, no vegetation, white "
     "surf breaking around it, wheeling gulls, flat grey ocean to the horizon. "
     f"Desolate. {STYLE}", []),
    ("loc_bladeship", "16:9",
     "Establishing interior shot, no characters: the bridge of a sinister alien "
     "warship — black ribbed steel like a blade's spine, a wide viewport onto "
     "starfield, deep red instrument light, catwalks over darkness. Menacing. "
     f"{STYLE}", []),
]

ANCHORS2 = [
    ("ax", "3:4",
     f"Full-body character portrait of an individual of EXACTLY the same alien "
     f"centaur species as the reference images. CRITICAL anatomy checklist, never "
     f"violated: he is a CENTAUR with SIX limbs — a deer-like four-legged lower "
     f"body in blue-and-tan fur, AND an upright slim humanoid torso rising "
     f"vertically from the shoulders of the four-legged body, with two slender "
     f"many-fingered arms and hands; a triangular face with NO mouth and two "
     f"large almond main eyes; two additional small eyes on flexible stalks on "
     f"top of the head; and a long muscular tail arcing forward over the back "
     f"ending in a curved scythe blade. He is NEVER a simple four-legged deer — "
     f"the upright torso, arms and head are clearly visible above the four legs. "
     f"His ENTIRE body — lower body, torso, arms and face — is covered in short "
     f"dense fur in cool BLUE and TAN: sky-blue across the back, shoulders and "
     f"face, sandy tan on the underside and legs. No bare pink skin anywhere, "
     f"never pink or purple or iridescent. This individual is Aximili, an "
     f"adolescent male cadet: slim, bright-eyed, alert curious stalk eyes, tail "
     f"blade in a neutral formal guard. He stands on gapped wooden barn "
     f"floorboards in warm lantern light, slightly too large for the human space "
     f"around him. {STYLE}", ["aldrea", "visser"]),
    ("visser", "3:4",
     f"Full-body character portrait of an individual of EXACTLY the same alien "
     f"centaur species as the reference image, identical anatomy: {ANDALITE}. "
     f"This individual is possessed and evil: a powerfully built mature male "
     f"with dark slate-blue fur, old scars across the flank and muzzle, main "
     f"eyes cold and cruel, stalk eyes fixed forward, tail blade raised high "
     f"and ready. He stands on the black steel bridge of a warship in deep red "
     f"light. {STYLE}", ["alloran"]),
]


def load_frames():
    import importlib.util
    spec = importlib.util.spec_from_file_location("frames_spec", HERE / "frames_spec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FRAMES


def resolve_ref(r: str) -> Path:
    for d in (ANCH, HB_ANCH):
        p = d / f"{r}.png"
        if p.exists():
            return p
    raise FileNotFoundError(f"ref {r} not found in {ANCH} or {HB_ANCH}")


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
