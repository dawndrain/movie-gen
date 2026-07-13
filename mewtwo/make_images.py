#!/usr/bin/env python3
"""Batch Nano Banana Pro images for THE VAULTED SKY (Mewtwo / Origin of Species).

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
    "Photorealistic cinematic film still from a moody live-action science-fiction "
    "feature film, IMAX 35mm, natural volumetric lighting, practical-creature-effects "
    "realism, rich cinematic color grade. No text, no watermark, no captions, no "
    "cartoon or anime styling."
)

MEWTWO = (
    "Mewtwo: a six-and-a-half-foot bipedal feline-alien creature with smooth "
    "bone-white skin shading to pale grey-violet on the belly and a long thick "
    "muscular purple-grey tail; a pinched cat-like face with a short snout, NO "
    "visible mouth line, no eyebrows, and large luminous violet eyes; two short "
    "blunt horn-like ear ridges sweeping back from the skull; a thick cable-like "
    "cord of flesh running from the back of its skull down between its shoulders; "
    "slender powerful arms ending in three thick bulbous fingers per hand; "
    "digitigrade cat-like legs; an eerie, still, intelligent presence"
)

SUIT1 = (
    "a crude bulky life-support suit of rounded dull-steel tubes encasing torso, "
    "arms and legs, a boxy battery pack on the back, thin fluid hoses running "
    "into ports at the arms and thighs, and a full helmet with a single round "
    "glass visor over the face"
)

ARMOR = (
    "sleek angular dark-grey armor plates over torso, shoulders, forearms and "
    "shins, a partial helmet with two grooves fitted around its horn ridges and a "
    "clear glass visor over the face, slim fluid lines running under the plates, "
    "tail and lower thighs left exposed; imposing, sinister, elegant"
)

POD_ROOM = (
    "a circular underground laboratory chamber, dim blue-black darkness ringed by "
    "glowing monitors and equipment, dominated at center by a huge cylindrical "
    "glass biopod full of luminous amber fluid, thick cables and fluid tubes "
    "running from the pod into ceiling and floor, a heartbeat monitor glowing "
    "green nearby"
)

CLIFFTOP = (
    "a wide grassy plateau atop a sea cliff: wind-flattened green grass, weathered "
    "stone steps up to an elegant old stone mansion behind, the open ocean beyond "
    "the cliff edge, and a hazy volcanic peak rising at the island's center in the "
    "far distance"
)

# (name, aspect, prompt, [refs])
ANCHORS1 = [
    ("mewtwo_pod", "3:4",
     f"Full-body character portrait of {MEWTWO}. It floats curled semi-upright in "
     f"glowing translucent amber fluid inside a huge cylindrical glass biopod, "
     f"soft intravenous tubes trailing from ports on its arms, thighs and spine, "
     f"eyes open, gazing out through the glass with unsettling calm intelligence. "
     f"Dim laboratory darkness beyond the glass. {STYLE}", []),
    ("sabrina", "3:4",
     "Full-body character portrait of Sabrina, a pale Japanese woman of about 27: "
     "very long straight black hair falling like a curtain past her waist, calm "
     "unreadable dark eyes, minimal expression with quiet warmth underneath; "
     "dressed in an elegant simple dark tunic and trousers. She stands in a dim "
     f"laboratory corridor, lit softly from one side. {STYLE}", []),
    ("giovanni", "3:4",
     "Full-body character portrait of Giovanni, a powerfully built Japanese man "
     "of about 50: tall, strong shoulders, tan skin, strong jaw, close-cropped "
     "dark hair with grey at the temples, calm composed face with intense dark "
     "eyes; immaculate black three-piece suit, white pocket square. He stands in "
     "a dark wood-paneled office, hands clasped behind his back, radiating "
     f"unhurried command. {STYLE}", []),
    ("dr_light", "3:4",
     "Full-body character portrait of Dr. Ivy Light, a woman of about 55: sharp "
     "practical face, short iron-grey hair, tired intelligent eyes, reading "
     "glasses pushed up on her head; open white lab coat over sturdy dark field "
     "clothes, ID badge clipped to the pocket. She stands in a laboratory "
     f"corridor holding a clipboard, exhausted but composed. {STYLE}", []),
    ("shaw", "3:4",
     "Full-body character portrait of David Shaw, head of security, a weathered "
     "man of about 50: ex-cop build, buzz-cut grey hair, hard flat watchful eyes, "
     "a boxer's nose; dark tactical jacket, cargo trousers and boots, several "
     "pokeballs on his belt, one hand resting near a remote in his jacket pocket. "
     f"He stands on windswept grass in fading light. {STYLE}", []),
    ("fuji", "3:4",
     "Full-body character portrait of Dr. Fuji, an elderly Japanese scientist: "
     "thin, slightly stooped, unruly white hair, round glasses, a deeply kind "
     "face carved with old grief; rumpled lab coat over a cardigan. He sits at a "
     "cluttered desk lit only by a computer monitor in a dark office, looking "
     f"toward the camera with gentle sadness. {STYLE}", []),
    ("gyokusho", "3:4",
     "Full-body character portrait of Gyokusho, a Japanese man in his mid 20s: "
     "messy dark hair he is nervously patting down, an open earnest gentle face, "
     "quick shy smile; comfortable sweater, laboratory ID lanyard, a sketchbook "
     "and pencil held against his chest. He stands in the doorway of a small "
     f"warmly lit room. {STYLE}", []),
    ("eva", "3:4",
     "Full-body character portrait of Eva, a woman of about 60: soft grey-brown "
     "hair in a loose bun, reading glasses on a chain, a warm lined face; thick "
     "knitted cardigan over a blouse, a slim volume of poetry held open in one "
     "hand. She sits in a worn armchair beside a lamp in a small cozy room, "
     f"mid-recitation. {STYLE}", []),
    ("ayush", "3:4",
     "Full-body character portrait of Ayush, an Indian man in his early 30s: "
     "bright enthusiastic eyes, neat short black hair and stubble, a quick grin; "
     "engineer's utility vest full of tools over a thermal shirt, heavy gloves "
     "tucked in his belt, a diagnostic tablet in one hand. He stands on windy "
     f"clifftop grass. {STYLE}", []),
    ("collins", "3:4",
     "Full-body character portrait of Dr. Perry Collins, a scientist in his mid "
     "40s: thinning sandy hair, wire glasses, a soft nervous face with a "
     "salesman's ready smile going uneasy at the edges; lab coat over a checked "
     f"shirt and slacks. He stands beside a conference table, half-turned as if "
     f"about to leave. {STYLE}", []),
    ("loc_pod_room", "16:9",
     f"Establishing wide shot, no characters, the pod empty of any creature: "
     f"{POD_ROOM}. Cathedral-quiet, humming, the amber glow the only warmth in "
     f"the frame. {STYLE}", []),
    ("loc_lab_corridor", "16:9",
     "Establishing wide shot, no characters: a long white-grey underground "
     "laboratory corridor with heavy sliding doors, cable trays and pipes along "
     "the ceiling, cool clinical light, a wide staircase at the far end leading "
     f"up toward warmer light. Sterile, institutional, endless. {STYLE}", []),
    ("loc_conference", "16:9",
     "Establishing wide shot, no characters: a windowless laboratory conference "
     "room — long table ringed with chairs, scattered papers and mugs, a paper "
     "logbook, a whiteboard dense with project schedules, harsh fluorescent "
     f"light, no decoration. Overworked and airless. {STYLE}", []),
    ("loc_mansion", "16:9",
     "Establishing wide shot, no characters: the grand interior hall of an old "
     "stone island mansion — tiled floors, carved balconies, tall double doors "
     "standing open at the far end onto brilliant blue sky and sea light, the "
     f"hall in cool shadow. The light through the doors like a doorway to "
     f"another world. {STYLE}", []),
    ("loc_clifftop", "16:9",
     f"Establishing wide shot, no characters: {CLIFFTOP}. Late golden afternoon, "
     f"wind in the grass, gulls, the sea glittering azure and navy to the "
     f"horizon. Beautiful and lonely. {STYLE}", []),
    ("loc_training", "16:9",
     "Establishing wide shot, no characters: a stark white reinforced training "
     "hall, bare padded floor and walls with faint scuff marks, a long "
     "observation window of thick glass set high in one wall with silhouettes "
     f"of monitoring equipment behind it, even shadowless light. {STYLE}", []),
    ("loc_cave", "16:9",
     "Establishing wide shot, no characters: the inside of a pitch-black sea "
     "cave — a small crescent of wet sand beside a pool of still black water, "
     "walls of dark slick stone, the only light a faint cold blue glow from a "
     f"single small indicator lamp resting on the sand. Absolute silence. {STYLE}", []),
    ("loc_ocean_dusk", "16:9",
     "Establishing wide shot, no characters: the open ocean at stormy dusk — "
     "heavy swell, rain just ending, low broken clouds torn open by a violent "
     "orange-gold sunset on the horizon, a dark volcanic island silhouetted "
     f"behind. Vast, hostile, beautiful. {STYLE}", []),
    ("loc_nightsky", "16:9",
     "Establishing wide shot, no characters: a moonless night sky over a black "
     "calm ocean — the Milky Way blazing edge to edge, stars beyond counting, "
     f"the sea faintly mirroring them, no land in sight. Endless. {STYLE}", []),
]

ANCHORS2 = [
    ("mewtwo_suit1", "3:4",
     f"Full-body character portrait of EXACTLY the same creature as the reference "
     f"image ({MEWTWO}), now standing on wet laboratory floor wearing {SUIT1}. "
     f"Its posture is unsteady, hunched, newborn — one three-fingered hand "
     f"pressed to the glass wall for balance, tail low. Dim pod-room light. "
     f"{STYLE}", ["mewtwo_pod"]),
    ("mewtwo_armor", "3:4",
     f"Full-body character portrait of EXACTLY the same creature as the reference "
     f"image ({MEWTWO}), now standing tall and composed wearing {ARMOR}. It "
     f"stands on windswept clifftop grass in late golden light, tail curved "
     f"behind it, violet eyes calm behind the visor. {STYLE}",
     ["mewtwo_pod"]),
    ("mewtwo_free", "3:4",
     f"Full-body character portrait of EXACTLY the same creature as the reference "
     f"image ({MEWTWO}), wearing nothing at all — no suit, no armor, no tubes: "
     f"lean and weathered, skin faintly scuffed, standing on dark wet sand at "
     f"night with its long tail curled around its feet, violet eyes catching "
     f"starlight. {STYLE}", ["mewtwo_pod"]),
    ("sabrina_teen", "3:4",
     f"Full-body character portrait of the same woman as the reference image but "
     f"aged 17: the same long straight black hair and calm unreadable dark eyes "
     f"in a younger, thinner face; plain dark student clothing. She sits "
     f"cross-legged on a laboratory floor, hands loose in her lap, eyes closed "
     f"in concentration. {STYLE}", ["sabrina"]),
]


def load_frames(specfile="frames_spec.py"):
    import importlib.util
    spec = importlib.util.spec_from_file_location(specfile[:-3], HERE / specfile)
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
    elif stage == "frames2":
        jobs, outdir = load_frames("frames_spec2.py"), HERE / "frames2"
    else:
        sys.exit(f"unknown stage {stage}")
    outdir.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        futs = [pool.submit(make, outdir, n, a, p, r, ANCH) for n, a, p, r in jobs]
        for f in futs:
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
