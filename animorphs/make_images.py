#!/usr/bin/env python3
"""Batch Nano Banana Pro images for the Hork-Bajir Chronicles movie.

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
ANCH = HERE / "anchors"
FRAMES = HERE / "frames"

STYLE = (
    "Photorealistic cinematic film still from an epic live-action science-fiction "
    "feature film, IMAX 35mm, natural volumetric lighting, practical-creature-effects "
    "realism, rich moody color grade. No text, no watermark, no captions, no cartoon "
    "or anime styling."
)

HORK = (
    "a Hork-Bajir: a seven-foot-tall bipedal alien with powerful tyrannosaur-like "
    "legs, three-clawed feet, a long tail with small spikes, leathery green-brown "
    "skin, and wickedly curved scythe-like bone blades all over its body: three "
    "long blades raked back from the top of its skull like a crest, and large "
    "prominent curved blades jutting from each forearm, elbow and knee; a "
    "snake-like neck, a hawk-like beaked snout, and large intelligent green eyes; "
    "despite the fearsome blades its posture and expression are gentle and "
    "peaceable"
)

ANDALITE = (
    "an Andalite: a graceful alien centaur with a deer-like four-legged lower body "
    "covered in short blue-and-tan fur, a slim upright torso with two slender "
    "many-fingered arms, a triangular face with NO mouth, two large almond-shaped "
    "main eyes, two additional small eyes on flexible stalks on top of the head, "
    "and a long muscular tail arcing forward over the back, ending in a wicked "
    "curved scythe blade"
)

ARN = (
    "an Arn: a four-foot-tall alien of dazzling iridescent coloring — crimson, "
    "cobalt, emerald and gold — with a high feathered crest, huge amber eyes, a "
    "small delicate face, thin limbs, and membranous wing-flaps folded at its "
    "sides, like a cross between a parrot, a gecko and a mandrill; ancient, vain, "
    "haughty bearing"
)

VALLEY = (
    "the Hork-Bajir homeworld: a vertiginous valley whose walls are the trunks of "
    "trees two kilometers tall with smooth blue-grey bark, layered teal and "
    "turquoise foliage, branches wide as roads; far below the branches fade into "
    "bottomless indigo mist; hazy golden alien sunlight from a huge pale sky"
)

# (name, aspect, prompt, [refs])
ANCHORS1 = [
    ("dak", "3:4",
     f"Full-body character portrait of {HORK}. This is Dak Hamee, a young adult "
     f"male 'seer': slimmer than average, unscarred, alert curious wide eyes, head "
     f"tilted slightly as if studying something far away. He stands on a massive "
     f"tree branch in {VALLEY}. {STYLE}", []),
    ("aldrea", "3:4",
     f"Full-body character portrait of {ANDALITE}. This is Aldrea, an adolescent "
     f"female: smaller and lighter-built, fur with a faint lavender-blue sheen, "
     f"large defiant main eyes, stalk eyes turned alertly. She stands in tall "
     f"blue-green alien grass on a high ridge overlooking a valley of colossal "
     f"trees. {STYLE}", []),
    ("arn", "3:4",
     f"Full-body character portrait of {ARN}, standing on a polished amber terrace "
     f"of an underground alien city lit by bioluminescent gardens, regarding the "
     f"viewer with imperious disdain. {STYLE}", []),
    ("tobias", "3:4",
     f"Character portrait of a red-tailed hawk perched on a pine branch in a "
     f"Sierra Nevada valley at golden hour, fierce amber eyes, feather detail, "
     f"wildlife-documentary realism. {STYLE}", []),
    ("loc_valley", "16:9",
     f"Establishing wide shot, no characters: {VALLEY}. Drifting pollen catches "
     f"the light; tiny winged creatures give scale; waterfalls of mist between "
     f"branches. Awe-inspiring epic scale. {STYLE}", []),
    ("loc_deep", "16:9",
     "Establishing wide shot, no characters: the Deep — the lightless base of "
     "kilometer-tall alien trees, roots like cathedral buttresses, glowing blue "
     "and violet bioluminescent fungus shelves, dull red volcanic vents, thick "
     "mist, half-seen enormous shapes in the darkness. Oppressive, primordial. "
     f"{STYLE}", []),
    ("loc_arn_city", "16:9",
     "Establishing wide shot, no characters: a hidden alien city inside a vast "
     "cavern beneath giant tree roots — elegant organic towers of polished amber "
     "and jade, terraced bioluminescent gardens, rows of turquoise-glowing "
     "gene-tanks, lit like a jewel box; beautiful, ancient and sterile. "
     f"{STYLE}", []),
    ("loc_dome", "16:9",
     "Establishing wide shot, no characters: a small alien research outpost on a "
     "high rocky ridge — a transparent geodesic dome enclosing a meadow of "
     "blue-green grass and sleek ivory instruments — overlooking a valley of "
     "trees two kilometers tall under a huge pale alien sky at dusk. "
     f"{STYLE}", []),
    ("loc_poolship", "16:9",
     "Establishing wide shot, no characters: the interior of a sinister alien "
     "pool ship — a vast dark steel cavern around a lake of dull leaden-grey "
     "liquid, metal piers extending over the pool, harsh sodium-orange "
     "industrial light, rising steam, brutalist alien architecture. "
     f"{STYLE}", []),
    ("loc_earth_valley", "16:9",
     "Establishing wide shot, no characters: a hidden narrow valley in the "
     "Sierra Nevada at golden hour — steep granite walls, ponderosa pines and "
     "maples, a creek, and rough shelters woven from bark and living branches "
     "high in the trees; serene, secret, warm. "
     f"{STYLE}", []),
]

ANCHORS2 = [
    ("jara", "3:4",
     f"Full-body character portrait of the same alien species as the reference "
     f"image ({HORK}). This is Jara Hamee, an older male: heavier build, weathered "
     f"grey-green skin, several chipped and scarred blades, one notched forehead "
     f"blade, calm dignified bearing. He stands beneath ponderosa pines in an "
     f"earthly mountain valley at golden hour. {STYLE}", ["dak"]),
    ("jagil", "3:4",
     f"Full-body character portrait of the same alien species as the reference "
     f"image ({HORK}). This is Jagil, a young male: stockier than the reference, "
     f"darker bark-brown skin, shorter forehead blades, an open friendly face. "
     f"He stands on a wide branch chewing a strip of bark. {STYLE}", ["dak"]),
    ("toby", "3:4",
     f"Full-body character portrait of the same alien species as the reference "
     f"image ({HORK}). This is Toby, an adolescent female: two-thirds adult "
     f"height, slender, smooth unscarred olive-green skin, smaller blades, and "
     f"strikingly focused intelligent eyes. She stands beneath pines in an "
     f"earthly mountain valley at dusk. {STYLE}", ["dak"]),
    ("esplin", "3:4",
     f"Full-body character portrait of the same alien species as the reference "
     f"image ({HORK}), but this individual is possessed and hostile: standing "
     f"unnaturally rigid and imperious, wearing a segmented black-and-crimson "
     f"military harness with angular alien insignia, eyes cold, calculating and "
     f"cruel. Dark steel spaceship interior behind him, orange industrial light. "
     f"{STYLE}", ["dak"]),
    ("aldrea_hb", "3:4",
     f"Full-body character portrait of the same alien species as the reference "
     f"image ({HORK}). This is a female of the species: slightly smaller and more "
     f"slender than the male reference, smoother skin with a faint blue-grey "
     f"sheen, more delicate blades, and unusually large expressive deep-green "
     f"almond eyes. She stands on a massive branch at sunrise. {STYLE}", ["dak"]),
    ("seerow", "3:4",
     f"Full-body character portrait of the same alien species as the reference "
     f"image ({ANDALITE}). This is Prince Seerow, an aging male: larger than the "
     f"reference, fur dulled and greying at the muzzle and chest, a slight stoop, "
     f"kind tired eyes carrying old regret. He stands inside a transparent dome "
     f"on an alien ridge at dusk. {STYLE}", ["aldrea"]),
    ("alloran", "3:4",
     f"Full-body character portrait of an individual of EXACTLY the same alien "
     f"centaur species as the reference image, identical anatomy: deer-like "
     f"four-legged lower body, an upright slim humanoid torso with two arms, a "
     f"triangular face with NO mouth, two main eyes plus two small eyes on "
     f"flexible stalks atop the head, and a long tail ending in a scythe blade. "
     f"This individual is War-Prince Alloran: a powerfully built mature male, "
     f"darker slate-blue fur, a pale scar across the flank, a military "
     f"bandolier-harness across the torso, cold hard eyes, tail blade held high "
     f"and ready. He stands beside a sleek ivory alien fighter craft. {STYLE}",
     ["aldrea"]),
]

# Scene frames are defined in frames_spec.py (generated after anchors verified)
def load_frames():
    import importlib.util
    spec = importlib.util.spec_from_file_location("frames_spec", HERE / "frames_spec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FRAMES


def make(outdir: Path, name: str, aspect: str, prompt: str, refs: list[str],
         refdir: Path) -> str:
    out = outdir / f"{name}.png"
    if out.exists():
        return f"skip {name}"
    cmd = [sys.executable, str(GEN), "image", prompt,
           "--resolution", "2k", "--aspect_ratio", aspect]
    for r in refs:
        p = (refdir / f"{r}.png") if not r.endswith(".png") else HERE / r
        cmd += ["--image", str(p)]
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
        futs = [pool.submit(make, outdir, n, a, p, r, ANCH) for n, a, p, r in jobs]
        for f in futs:
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
