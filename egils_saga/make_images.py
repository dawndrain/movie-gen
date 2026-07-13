#!/usr/bin/env python3
"""Batch Nano Banana Pro images for EGIL (Egil's Saga).

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
    "Photorealistic cinematic film still from a live-action historical "
    "Viking-age epic feature film, IMAX 35mm, natural volumetric light, "
    "moody overcast Nordic color grade, rich texture of wool, iron, timber "
    "and turf. Historically grounded 9th-10th century Norse costume and "
    "props. No text, no watermark, no captions, no cartoon styling, no "
    "horned helmets. ONE single continuous photograph filling the whole "
    "frame, no borders, no collage."
)

# canonical wardrobe/appearance locks — reuse VERBATIM in frame + clip prompts
W = {
    "kveldulf":
        "an enormous old Norse chieftain in his late sixties, grizzled grey "
        "hair and a full grey beard, heavy brow, deep-set wolfish eyes, "
        "wearing a coarse iron-grey wool knee-length tunic, a broad leather "
        "belt with an iron buckle, a dark bearskin mantle over his "
        "shoulders, wool leg-wrappings and leather turnshoes",
    "thorolf_k":
        "a tall handsome fair-haired Norse warrior of about thirty, golden "
        "shoulder-length hair, a short golden beard, a bright open face, "
        "wearing a fine scarlet wool tunic with tablet-woven gold trim, a "
        "silver penannular cloak-brooch, a blue wool cloak, and a sword on "
        "a baldric",
    "harald":
        "a Norse king of about forty with an extraordinary mane of thick "
        "unbound tawny-gold hair falling past his shoulders, sharp cold "
        "eyes, a controlled unreadable face, wearing a deep green kingly "
        "tunic with a gold-embroidered hem, heavy gold arm-rings on both "
        "arms, an ermine-trimmed wool mantle and a plain gold circlet",
    "skallagrim":
        "a hulking swarthy Norse farmer-smith with a completely bald head, "
        "a black bushy beard, ugly heavy features, huge shoulders and "
        "thick smith's forearms, wearing a soot-dark undyed wool tunic, a "
        "plain iron-buckled belt and a black wool cloak",
    "egil_child":
        "a startling Norse child who looks far too big and strong for his "
        "young age, with shaggy coal-black hair, heavy black brows, ugly "
        "blunt features and intense black eyes, wearing a small "
        "russet-brown wool tunic, a child's leather belt and small leather "
        "shoes",
    "egil":
        "a massive ugly Norse warrior-poet, more than commonly tall, "
        "large-featured with a broad forehead, large eyebrows, a very "
        "thick short nose, wide long lips, an exceedingly broad chin and "
        "jaw, a thick neck, shoulders bigger than other men's, "
        "hard-featured and grim, thick wolf-grey hair around a balding "
        "crown, black eyes and brown weathered skin, wearing a "
        "charcoal-black wool tunic, a wolf-grey wool cloak pinned with an "
        "iron penannular brooch, a wide leather belt and a sword at his hip",
    "egil_old":
        "the same massive ugly Norse man aged to about eighty-five: the "
        "same broad forehead, thick nose, exceedingly broad jaw and heavy "
        "brows, now with a straggling white beard, milky blind pale eyes, "
        "a bald age-spotted head, stooped but still huge, gripping a "
        "walking staff, wearing a worn undyed wool tunic and a shapeless "
        "dark cloak",
    "thorolf_s":
        "a tall handsome fair-haired Norse warrior of about thirty with "
        "golden shoulder-length hair, a short golden beard and a bright "
        "open face, wearing a russet-red wool tunic, a fine grey cloak, "
        "carrying an ample round shield and a great halberd with a long "
        "feather-shaped blade, wearing a strong plain helmet and NO "
        "mail-shirt",
    "eirik":
        "a Norse king of about forty with dark red hair and a short red "
        "beard, a handsome cruel face and terrifying keen glittering eyes, "
        "wearing a blood-red kingly tunic with gold trim, a black mantle "
        "with a gold clasp, a gold circlet, and an ornate axe at his belt",
    "gunnhild":
        "a Norse queen in her thirties with long raven-black hair in "
        "braids, a pale sharp face and unblinking watchful eyes, wearing a "
        "deep midnight-blue apron-dress over a white linen underdress, "
        "twin oval bronze brooches with hanging amber beads, a silver "
        "diadem and a dark fur-lined cloak",
    "arinbjorn":
        "a sturdy noble Norse baron of about forty with brown hair, a "
        "trimmed brown beard and a calm loyal face, wearing a forest-green "
        "baron's tunic with fine trim, a gold arm-ring, a brown "
        "fur-trimmed cloak and a sword at his hip",
    "athelstan":
        "an Anglo-Saxon king of England of about thirty-five, clean-shaven "
        "with fair cropped hair and a refined intelligent face, wearing a "
        "long white and gold Anglo-Saxon royal tunic to the ankle, a "
        "jewelled purple mantle clasped with a gold cross-brooch, a gold "
        "crown and rings on his fingers",
    "thorgerd":
        "a tall Norse woman of about thirty-five with ash-brown braided "
        "hair and a strong handsome face with a heavy jaw and dark brows, "
        "wearing a madder-red apron-dress over a cream linen underdress, "
        "twin oval bronze brooches and a hooded riding cloak",
    "brak":
        "a big weathered Norse serving-woman in her forties, strong as a "
        "man, with a kind fierce face, wearing a plain slate-grey working "
        "dress, a linen head-kerchief and a wool shawl",
    "bard":
        "a smug well-fed Norse steward in his forties with thinning brown "
        "hair and a neat beard, wearing a fine ochre-yellow tunic with a "
        "ring of iron keys at his belt",
}

# (name, aspect, prompt, [refs])
ANCHORS1 = [
    ("kveldulf", "3:4",
     f"Full-body character portrait of {W['kveldulf']}. He stands before a "
     f"dark timber longhouse wall at dusk, a long-hafted battle-axe in one "
     f"hand, utterly still, staring into the failing light. He is the ONLY "
     f"figure in the frame. {STYLE}", []),
    ("thorolf_k", "3:4",
     f"Full-body character portrait of {W['thorolf_k']}. He stands on a "
     f"wooden jetty by a fjord in morning light, confident and open-faced. "
     f"He is the ONLY figure in the frame. {STYLE}", []),
    ("harald", "3:4",
     f"Full-body character portrait of {W['harald']}. He sits on a carved "
     f"wooden high seat in a torchlit hall, hands on the armrests, "
     f"watching. He is the ONLY figure in the frame. {STYLE}", []),
    ("skallagrim", "3:4",
     f"Full-body character portrait of {W['skallagrim']}. He stands at a "
     f"glowing forge inside a dark smithy, a smith's hammer in one hand, "
     f"glowering at the viewer. He is the ONLY figure in the frame. "
     f"{STYLE}", []),
    ("egil_child", "3:4",
     f"Full-body character portrait of {W['egil_child']}. He stands on "
     f"open Icelandic moorland under a grey sky, fists at his sides, "
     f"glaring with unsettling adult intensity. He is the ONLY figure in "
     f"the frame. {STYLE}", []),
    ("egil", "3:4",
     f"Full-body character portrait of {W['egil']}. He stands in a dark "
     f"turf-walled hall lit by a long fire, one eyebrow drawn down low and "
     f"the other raised high, a grim half-mocking expression. He is the "
     f"ONLY figure in the frame. {STYLE}", []),
    ("gunnhild", "3:4",
     f"Full-body character portrait of {W['gunnhild']}. She stands in a "
     f"torchlit royal hall beside a carved pillar, composed and watchful. "
     f"She is the ONLY figure in the frame. {STYLE}", []),
    ("eirik", "3:4",
     f"Full-body character portrait of {W['eirik']}. He stands in a "
     f"torchlit stone-and-timber hall, one hand resting on the ornate axe "
     f"at his belt. He is the ONLY figure in the frame. {STYLE}", []),
    ("arinbjorn", "3:4",
     f"Full-body character portrait of {W['arinbjorn']}. He stands at the "
     f"carved door of a great hall holding a torch, steady and "
     f"unsurprised. He is the ONLY figure in the frame. {STYLE}", []),
    ("athelstan", "3:4",
     f"Full-body character portrait of {W['athelstan']}. He stands in an "
     f"Anglo-Saxon royal hall with tapestried walls, thoughtful and "
     f"composed. He is the ONLY figure in the frame. {STYLE}", []),
    ("thorgerd", "3:4",
     f"Full-body character portrait of {W['thorgerd']}. She stands in the "
     f"doorway of a turf longhouse, travel-worn from riding, resolute. "
     f"She is the ONLY figure in the frame. {STYLE}", []),
    ("brak", "3:4",
     f"Full-body character portrait of {W['brak']}. She stands on a rocky "
     f"Icelandic shore in wind, steady and unafraid. She is the ONLY "
     f"figure in the frame. {STYLE}", []),
    ("bard", "3:4",
     f"Full-body character portrait of {W['bard']}. He stands in a "
     f"banquet-hall doorway holding a drinking horn, wearing an oily "
     f"insincere smile. He is the ONLY figure in the frame. {STYLE}", []),
    # ---- location plates ----
    ("loc_kveldulf_hall", "16:9",
     f"Establishing wide shot, no people: a Norwegian chieftain's timber "
     f"longhouse at dusk — turf roof, carved doorposts, smoke from the "
     f"roof-vent, a dark fjord and pine ridges behind, last cold light on "
     f"the water. Ominous and quiet. {STYLE}", []),
    ("loc_sandness", "16:9",
     f"Establishing wide shot, no people: a great northern Norwegian hall "
     f"at night — long timber walls, birch-bark and turf roof, outbuildings, "
     f"a pale summer night sky, the sea glinting beyond. Tense stillness. "
     f"{STYLE}", []),
    ("loc_longship", "16:9",
     f"Establishing wide shot, no people: an open Viking longship under a "
     f"single square blue-and-red striped wool sail on a grey North "
     f"Atlantic swell, no land in sight, low clouds, spray off the bow. "
     f"{STYLE}", []),
    ("loc_borg", "16:9",
     f"Establishing wide shot, no people: an Icelandic turf longhouse "
     f"homestead under a rocky hill beside a wide firth — green treeless "
     f"moor, a milky glacier-fed river braiding to the sea, black distant "
     f"fells, driftwood on the shore. {STYLE}", []),
    ("loc_borg_hall", "16:9",
     f"Establishing interior shot, no people: inside a dark Icelandic "
     f"turf-and-timber hall — a long fire-pit down the middle, a carved "
     f"high seat, weapons and shields on the walls, smoke curling in the "
     f"rafters, and against one wall a lockable wooden bed-closet with a "
     f"small carved door. {STYLE}", []),
    ("loc_vinheath", "16:9",
     f"Establishing wide shot, no people: a level open heath between a "
     f"river and a dark wood — rows of tall pale war-tents pitched in a "
     f"long wall, hazel poles planted in lines marking a battlefield, "
     f"overcast English light. {STYLE}", []),
    ("loc_athelstan_hall", "16:9",
     f"Establishing interior shot, no people: an Anglo-Saxon royal feast "
     f"hall — carved oak pillars, embroidered tapestries, two facing "
     f"high seats, and a LONG OPEN FIRE burning in a trench down the "
     f"middle of the floor between them, torchlight and deep shadow. "
     f"{STYLE}", []),
    ("loc_york", "16:9",
     f"Establishing interior shot, no people: a Northumbrian king's hall "
     f"at York — Roman stone walls patched with Norse timber, torches in "
     f"iron brackets, a raised dais with a carved throne, spears stacked "
     f"by the door, hostile shadows. {STYLE}", []),
    ("loc_gulathing", "16:9",
     f"Establishing wide shot, no people: an open-air Norse law assembly "
     f"ground on a level field by a fjord — hazel poles planted in a wide "
     f"ring joined by twisted ropes, empty judges' benches within the "
     f"ring, grey morning light. {STYLE}", []),
    ("loc_nithing_rock", "16:9",
     f"Establishing wide shot, no people: a bare rocky headland at dusk "
     f"above a leaden sea, wind-flattened grass, a rift in the summit "
     f"rock, dark mainland mountains across the water, storm light. "
     f"{STYLE}", []),
    ("loc_moor_bog", "16:9",
     f"Establishing wide shot, no people: Icelandic moorland in half-light "
     f"— steaming hot-spring holes, black peat bogs, a thaw-swollen stream "
     f"cutting a small ravine, mist, no trees. Uncanny and still. {STYLE}",
     []),
    ("loc_mound", "16:9",
     f"Establishing wide shot, no people: a grassy burial mound on a low "
     f"ness above calm water, evening light, long shadows, distant black "
     f"fells across the firth. {STYLE}", []),
]

# second pass: anchors that reference first-pass anchors
ANCHORS2 = [
    ("thorolf_s", "3:4",
     f"Full-body character portrait of a man with EXACTLY the same face as "
     f"the man in the reference image — the same golden hair, short golden "
     f"beard and bright open features. This is {W['thorolf_s']}. He stands "
     f"on the open heath before rows of war-tents, shield on his arm and "
     f"the great halberd in hand. He is the ONLY figure in the frame. "
     f"{STYLE}", ["thorolf_k"]),
    ("egil_old", "3:4",
     f"Full-body character portrait of the SAME man as in the reference "
     f"image aged to eighty-five years old: {W['egil_old']}. The broad "
     f"jaw, thick nose and heavy brow of the reference face are still "
     f"clearly recognizable under the age. He stands groping with one "
     f"hand along a turf hall wall, staff in the other hand, blind eyes "
     f"open. He is the ONLY figure in the frame. {STYLE}", ["egil"]),
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
