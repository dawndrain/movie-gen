#!/usr/bin/env python3
"""Batch Nano Banana Pro images for THE BUSY BODY (Centlivre, 1709).

Usage: python3 make_images.py <stage>     stage in {anchors, variants, frames}
Skips images whose output file already exists (re-run = retry pass).
`variants` needs `anchors` done first (disguise anchors take the base
portrait as ref); `frames` needs both.
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
    "Photorealistic cinematic film still from a live-action period comedy "
    "feature film set in London in 1709, Queen Anne era. 35mm, natural window "
    "light and warm candlelight, rich painterly color grade like a Gainsborough "
    "brought to life. ONE single continuous photograph filling the whole frame, "
    "no borders, no collage, no text, no watermark, no captions, no cartoon "
    "styling."
)

SOLO = "This is the ONLY figure in the frame; the background contains no other people."

# canonical wardrobe — reuse VERBATIM in frame and video prompts
W = {
    "marplot":  "a man in his mid-20s with a round eager puppyish face, wide curious "
                "eyes, and a black sticking-plaster across the bridge of his nose, "
                "wearing a slightly-too-flashy mustard-yellow coat with worn cuffs, "
                "a long patterned waistcoat, breeches, scuffed buckled shoes, a small "
                "sword, and a brown bob-wig sitting slightly askew",
    "george":   "a tall handsome confident gentleman of 24 with a warm half-smile, "
                "wearing an immaculate sky-blue embroidered justacorps coat with "
                "silver lace, a lace cravat, breeches, white stockings, buckled "
                "shoes, a dress sword, and a full-bottomed dark periwig",
    "meanwell": "the same gentleman disguised as a sober English merchant: plain "
                "dark-brown broadcloth suit, simple linen cravat, modest tie-wig, "
                "no lace, carrying a folded letter",
    "charles":  "a lean earnest dark-eyed young gentleman of 21, wearing a "
                "well-cut but worn plain grey coat, dark waistcoat, breeches, "
                "riding boots, and a short chestnut-brown periwig (natural "
                "brown hair color, never grey or purple)",
    "diego":    "the same young gentleman disguised as a Spanish grandee in a "
                "theatrical black Spanish habit: short black cloak, stiff white "
                "golilla collar, slashed sleeves, and a broad-brimmed black Spanish "
                "hat with a red plume",
    "miranda":  "a poised young lady of 18 with sharp amused eyes and dark hair "
                "dressed high, wearing an elegant rose-and-cream silk mantua gown "
                "with a modest neckline, pearl earrings, and carrying a folding fan",
    "miranda_masked": "the same young lady incognito: a loose hooded dove-grey "
                "morning gown over her dress, the hood up, and a black vizard mask "
                "covering her face",
    "isabinda": "a gentle young lady of 19 with an oval face and dark ringlets, "
                "wearing a modest high-necked dove-grey gown with a white lace "
                "mantilla-style shawl pinned over her hair",
    "francis":  "a gaunt stooped old man of 65 with a sly toothy grin, wearing a "
                "rusty-black old-fashioned coat with worn rich trim, a long grey "
                "outdated wig, holding a bamboo cane, with a pocket watch on a "
                "chain and a leather purse at his belt",
    "jealous":  "a florid barrel-chested merchant in his late 50s with bristling "
                "grey brows, wearing a severe prosperous black merchant's coat of "
                "Spanish cut, a plain cravat, an iron-grey wig, and carrying a cane",
    "patch":    "a knowing sharp-faced maidservant in her 30s, wearing a crisp "
                "white cap and apron over a practical brown wool gown, with a "
                "tie-on pocket at her hip",
    "whisper":  "a wiry young footman in plain dark livery with a hunched "
                "conspiratorial posture, one hand cupped beside his mouth",
    "scentwell": "a bright-faced young maidservant, wearing a neat white cap and "
                "apron over a striped cotton gown",
}

# (name, aspect, prompt, [refs])  refs resolve against ANCH
ANCHORS = [
    ("marplot", "3:4",
     f"Full-body character portrait of {W['marplot']}. He stands on a gravel "
     f"park walk leaning slightly forward as if straining to overhear something "
     f"wonderful, eyes wide, mouth slightly open. {SOLO} {STYLE}", []),
    ("george", "3:4",
     f"Full-body character portrait of {W['george']}. He stands on a gravel park "
     f"walk, one hand resting on his sword hilt, chin up, amused and assured. "
     f"{SOLO} {STYLE}", []),
    ("charles", "3:4",
     f"Full-body character portrait of {W['charles']}. He stands in a plain "
     f"panelled lodging room, arms folded, jaw set, a young man out of money and "
     f"out of patience. {SOLO} {STYLE}", []),
    ("miranda", "3:4",
     f"Full-body character portrait of {W['miranda']}. She stands in a panelled "
     f"chamber beside a dressing table, fan half-open, one eyebrow raised in dry "
     f"amusement. {SOLO} {STYLE}", []),
    ("isabinda", "3:4",
     f"Full-body character portrait of {W['isabinda']}. She stands at a casement "
     f"window in a small chamber, one hand on the frame, wistful but resolute. "
     f"{SOLO} {STYLE}", []),
    ("francis", "3:4",
     f"Full-body character portrait of {W['francis']}. He stands in a dark "
     f"panelled parlor beside a strong-box, mid-giggle, one hand curled around "
     f"his purse. {SOLO} {STYLE}", []),
    ("jealous", "3:4",
     f"Full-body character portrait of {W['jealous']}. He stands before his "
     f"town-house door glaring down the street, cane planted, brows thunderous. "
     f"{SOLO} {STYLE}", []),
    ("patch", "3:4",
     f"Full-body character portrait of {W['patch']}. She stands in a panelled "
     f"hallway with a folded letter half-tucked into her bosom, finger to her "
     f"lips. {SOLO} {STYLE}", []),
    ("whisper", "3:4",
     f"Full-body character portrait of {W['whisper']}. He stands at a street "
     f"corner glancing over his shoulder, hand cupped beside his mouth. {SOLO} "
     f"{STYLE}", []),
    ("scentwell", "3:4",
     f"Full-body character portrait of {W['scentwell']}. She stands in a "
     f"chamber doorway holding a small jewel casket, cheerful and quick. {SOLO} "
     f"{STYLE}", []),
    # ---- location plates ----
    ("loc_park", "16:9",
     "Establishing wide shot, no people: St James's Park, London, 1709, early "
     "morning — a long gravel walk under an avenue of lime trees, dew on grass, "
     "deer grazing far off, low golden mist, an empty sedan chair standing at "
     f"the path's edge. {STYLE}", []),
    ("loc_gripe_parlor", "16:9",
     "Establishing interior shot, no people: the parlor of a rich London miser, "
     "1709 — dark old oak panelling, heavy worn furnishings a generation out of "
     "fashion, a ledger desk with quills, an iron strong-box, a cane leaning on "
     f"a chair, thin daylight through leaded windows. {STYLE}", []),
    ("loc_miranda_room", "16:9",
     "Establishing interior shot, no people: a young heiress's chamber in a 1709 "
     "London house — lighter oak panelling, a dressing table with a jewel casket "
     "and mirror, a mantelpiece crowded with blue-and-white china, and a wide "
     "fireplace completely sealed by a tall painted decorative chimney-board, "
     f"large enough to hide a man behind. Afternoon window light. {STYLE}", []),
    ("loc_garden_gate", "16:9",
     "Establishing shot, no people: a walled town garden at dusk, 1709 — old "
     "brick wall thick with ivy, a wooden garden gate standing ajar onto a dark "
     f"park beyond, a single lantern's warm glow, deep blue twilight. {STYLE}", []),
    ("loc_jealous_street", "16:9",
     "Establishing wide shot, no people: a London street of 1709 before a "
     "prosperous merchant's brick townhouse — stout painted front door with "
     "steps, and above it a practical first-floor BALCONY with a casement "
     "window, wrought-iron rail, cobbles below, evening light. The balcony is "
     f"low enough that a man might drop from it. {STYLE}", []),
    ("loc_isabinda_room", "16:9",
     "Establishing interior shot, no people: a locked daughter's chamber in a "
     "1709 merchant's house with Spanish touches — lattice-shaded casement "
     "window, a small spinet with sheet music, a supper table with one chair, "
     "and center-stage a stout CLOSET DOOR, candlelight, shadows to hide in. "
     f"{STYLE}", []),
    ("loc_jealous_hall", "16:9",
     "Establishing interior shot, no people: the receiving hall of a prosperous "
     "1709 London merchant obsessed with Spain — dark Spanish portraits, a "
     "Toledo sword displayed on the wall, heavy oak furniture, and at the back "
     f"a substantial parlor door, morning light. {STYLE}", []),
    ("loc_tavern", "16:9",
     "Establishing interior shot, no people: a private room in a 1709 London "
     "tavern — a plain wooden table with wine bottles and glasses, tallow "
     f"candles, dark beams, a small leaded window, convivial warm light. {STYLE}", []),
]

VARIANTS = [
    ("george_meanwell", "3:4",
     f"Full-body character portrait of the SAME man as the reference image — "
     f"identical face — now {W['meanwell']}. He stands in a merchant's hall, "
     f"hands folded soberly, the faintest suppressed smile. {SOLO} {STYLE}",
     ["george"]),
    ("charles_diego", "3:4",
     f"Full-body character portrait of the SAME man as the reference image — "
     f"identical face — now {W['diego']}. He stands mid-bow in a merchant's "
     f"hall, sweeping his plumed hat, theatrical and grand. {SOLO} {STYLE}",
     ["charles"]),
    ("miranda_masked", "3:4",
     f"Full-body character portrait of the SAME young lady as the reference "
     f"image — now {W['miranda_masked']}. She stands on a gravel park walk "
     f"beside a sedan chair, head tilted teasingly. {SOLO} {STYLE}",
     ["miranda"]),
]

# ---- start frames: (name, [refs], staging prompt) — all 16:9 ----
F = [
    # ACT I — the Park
    ("p1", ["loc_park"],
     "The park plate exactly as the reference image, with an ornate engraved "
     "period title card elegantly lettered across the sky in antique serif "
     "capitals, reading exactly: \"THE BUSY BODY\" and beneath it in smaller "
     "italic letters exactly: \"a comedy of 1709\". The lettering is crisp, "
     "correct, and spelled exactly as given."),
    ("p2", ["loc_park", "george", "charles"],
     f"Two gentlemen stroll together down the gravel walk in morning light: "
     f"{W['george']}, and {W['charles']}. George gestures expansively "
     f"mid-confession; Charles listens with a dry skeptical look. No other "
     f"people in the park."),
    ("p3", ["loc_park", "george", "charles", "marplot"],
     f"On the gravel walk, {W['marplot']} bounds eagerly up to the two "
     f"gentlemen from the reference portraits — George amused, Charles "
     f"long-suffering. Marplot beams, mid-bow, the black plaster prominent on "
     f"his nose."),
    ("p4", ["marplot"],
     f"Flashback vignette on a merchant's doorstep, slightly dreamlike softer "
     f"light: {W['marplot']} solemnly hands a sealed love letter to a stern "
     f"burly MERCHANT in a brown coat while presenting the reins of two "
     f"saddled horses to the merchant's astonished WIFE in a lace cap. Both "
     f"recipients stare at him."),
    ("p5", ["loc_park", "charles", "whisper", "marplot"],
     f"On the gravel walk, {W['whisper']} murmurs behind his cupped hand into "
     f"Charles's ear; Charles leans in. In the middle distance, Marplot "
     f"(plaster on nose, mustard coat) cranes toward them from behind a lime "
     f"tree, straining to hear."),
    ("p6", ["loc_park", "miranda_masked", "patch"],
     f"Beside the sedan chair on the park walk, {W['miranda_masked']} steps "
     f"out, taking the hand of {W['patch']}. Two chairmen in plain coats stand "
     f"at the poles, looking away."),
    ("p7", ["loc_park", "george", "francis", "miranda_masked", "patch"],
     f"By a large lime tree, {W['george']} pours gold coins from a purse into "
     f"the cupped hands of {W['francis']}, who grins toothily. Behind a shrub "
     f"in the foreground corner, the masked hooded lady and the maid Patch "
     f"peep out at them, unseen."),
    ("p8", ["loc_park", "george", "miranda_masked"],
     f"On the empty gravel walk, {W['george']} stands with his BACK fully "
     f"turned to {W['miranda_masked']}, his head high, mid-speech; behind his "
     f"back she is caught mid-tiptoe, skirts lifted an inch, sneaking away "
     f"toward the sedan chair with a gloved hand pressed to her masked mouth."),
    # ACT II — Gripe parlor / Dumb Scene / Jealous house
    ("g1", ["loc_gripe_parlor", "miranda", "francis"],
     f"In the miser's parlor, {W['miranda']} sits fanning herself sweetly "
     f"beside {W['francis']}, who perches on his chair mid-giggle, clasping "
     f"his cane; she smiles at him while her eyes slide sideways to the "
     f"camera, dry as dust."),
    ("g2", ["loc_gripe_parlor", "francis", "charles"],
     f"In the miser's parlor, {W['francis']} stands raising his bamboo cane "
     f"high, face flushed scarlet with outrage but with natural human skin, "
     f"while {W['charles']} backs toward the door, hands spread, pleading and "
     f"furious at once. All faces have natural realistic skin tones."),
    ("g3", ["loc_gripe_parlor", "george", "miranda", "francis"],
     f"The paid interview: in the parlor, {W['george']} bows low over the hand "
     f"of {W['miranda']}, who sits perfectly still and expressionless as a "
     f"statue, eyes forward; at the back of the room {W['francis']} leans in "
     f"an armchair holding his pocket watch open, scowling suspiciously."),
    ("j1", ["loc_jealous_street", "isabinda", "jealous"],
     f"Street view: on the first-floor balcony, {W['isabinda']} leans on the "
     f"iron rail taking the air; below on the front steps {W['jealous']} "
     f"points his cane up at her, mid-bellow, veins in his neck."),
    ("j2", ["loc_jealous_street", "jealous", "whisper"],
     f"At the front door, {W['jealous']} has caught {W['whisper']} by the "
     f"collar at arm's length, glaring nose to nose; Whisper's free hand is "
     f"raised in frantic innocent protest."),
    # ACT III
    ("j3", ["loc_isabinda_room", "charles", "isabinda", "patch"],
     f"In the daughter's chamber by candlelight, {W['charles']} clasps both "
     f"hands of {W['isabinda']}; a rope ladder hangs in through the open "
     f"casement behind him. At the door, {W['patch']} bursts in wide-eyed, "
     f"mid-warning."),
    ("j4", ["loc_jealous_street", "jealous", "marplot"],
     f"In the street at dusk, {W['jealous']} swats his cane at {W['marplot']}, "
     f"who scrambles away in a comic crouch, wig flying loose, arms shielding "
     f"his head. Cartoonish farce energy, no blood, no injury."),
    ("j5", ["loc_jealous_street", "charles", "marplot"],
     f"At the foot of the balcony at dusk, {W['charles']} and {W['marplot']} "
     f"lie sprawled in a tangled heap on the cobbles where Charles has just "
     f"dropped from the balcony onto him; Charles is already grabbing "
     f"Marplot's collar; Marplot grins up sheepishly, plaster askew."),
    ("g4", ["loc_gripe_parlor", "miranda", "francis", "marplot"],
     f"In the parlor, {W['miranda']} stands with her hand clasped warmly in "
     f"both hands of a beaming {W['francis']}; she addresses {W['marplot']}, "
     f"who stands scowling with folded arms by the door, refusing to look "
     f"convinced."),
    ("t1", ["loc_tavern", "george", "charles", "marplot"],
     f"In the tavern's private room over wine, {W['george']} has leapt to his "
     f"feet mid-epiphany, glass raised, delight breaking over his face; "
     f"{W['charles']} smirks into his wine; {W['marplot']} stands between them "
     f"utterly baffled, still mid-solemn-warning."),
    # ACT IV
    ("j6", ["loc_jealous_street", "patch", "jealous"],
     f"By the front steps, {W['patch']} walks away up the steps, a folded "
     f"letter slipping unnoticed from the tie-on pocket at her hip, frozen "
     f"mid-fall in the air behind her; further down the street {W['jealous']} "
     f"approaches, eyes already on the falling paper."),
    ("j7", ["loc_isabinda_room", "jealous", "patch", "isabinda"],
     f"In the chamber, {W['jealous']} brandishes the folded letter "
     f"accusingly; {W['patch']} clasps it back to her heart with a face of "
     f"wounded piety; {W['isabinda']} watches, hands clasped bloodlessly."),
    ("j8", ["loc_isabinda_room", "jealous", "isabinda", "patch"],
     f"Supper suspense: {W['jealous']} sits eating at the supper table; "
     f"{W['isabinda']} sits rigid at the spinet, fingers on the keys, eyes "
     f"locked sideways on the closet door; {W['patch']} stands singing beside "
     f"her, mouth open, also staring at the closet door; beyond the casement "
     f"window a rope ladder and a man's silhouette are just visible climbing."),
    ("j9", ["loc_isabinda_room", "jealous", "isabinda", "patch", "charles"],
     f"Chaos: the closet door stands flung open with {W['charles']} frozen "
     f"half-inside it, caught mid-poem; {W['jealous']} surges up from the "
     f"supper table knocking his chair back; {W['patch']} throws her arms up "
     f"shrieking; {W['isabinda']} swoons theatrically to the floor directly "
     f"across the closet doorway, the back of her hand to her brow."),
    ("j10", ["loc_jealous_street", "patch", "charles"],
     f"Night street under the unlit balcony: {W['patch']}, shawl clutched, "
     f"lays a calming hand on the sword-arm of {W['charles']}, whose blade is "
     f"half-drawn; she holds up a letter with a sly dawning smile; his face is "
     f"turning from fury to wonder."),
    ("g5", ["loc_garden_gate", "george", "scentwell"],
     f"At the ivy-clad garden gate at dusk, {W['scentwell']} holds up a "
     f"lantern and takes the hand of {W['george']}, leading him in through "
     f"the gate; he glances warily about, half-expecting an ambush."),
    ("g6", ["loc_miranda_room", "miranda", "george", "scentwell"],
     f"In the heiress's chamber by candlelight, {W['george']} holds both "
     f"hands of {W['miranda']}, forehead to forehead, both smiling; at the "
     f"door {W['scentwell']} bursts in mid-cry, pointing behind her."),
    ("g7", ["loc_miranda_room", "francis", "miranda", "marplot"],
     f"In the chamber, {W['francis']} stands directly before the painted "
     f"chimney-board, peeling an orange, the peel poised to toss behind the "
     f"board; {W['miranda']} lunges gracefully between him and the fireplace, "
     f"arms spread wide; {W['marplot']} peers hungrily at the board from "
     f"behind them both, on tiptoe."),
    ("g8", ["loc_miranda_room", "marplot", "george"],
     f"In the chamber, {W['marplot']} has pulled the chimney-board half aside "
     f"and reels back in terror; behind it in the fireplace alcove crouches "
     f"{W['george']}, furious, one hand shooting out to seize Marplot's "
     f"cravat; blue-and-white china plates cascade off the mantel mid-air, "
     f"frozen mid-fall."),
    ("g9", ["loc_miranda_room", "george", "marplot", "patch", "miranda"],
     f"In the chamber, {W['george']} marches a squirming {W['marplot']} "
     f"toward the door by the collar, both almost comic-dance partners; "
     f"{W['miranda']} and {W['patch']} confer urgently by the dressing table "
     f"over a note."),
    # ACT V
    ("g10", ["loc_miranda_room", "miranda", "francis", "scentwell"],
     f"Morning: {W['miranda']} stands frozen mid-gloat at the chamber door, "
     f"eyes wide in horror toward the camera, because directly behind her "
     f"stands {W['francis']}, beaming, hand raised to touch her shoulder; at "
     f"the side {W['scentwell']} enters dangling a diamond necklace and "
     f"freezes too."),
    ("g11", ["loc_gripe_parlor", "francis", "miranda"],
     f"{W['francis']} in his best rusty-black finery offers his arm grandly "
     f"to {W['miranda']}, who takes it, radiant, while turning her head to "
     f"give the camera a long dry conspiratorial look. He gazes upward in "
     f"bliss, oblivious."),
    ("j11", ["loc_jealous_hall", "charles_diego", "george_meanwell", "jealous"],
     f"In the merchant's hall, {W['diego']} sweeps a deep theatrical bow, "
     f"plumed hat flourished wide; beside him {W['meanwell']} stands soberly "
     f"presenting a sealed letter; {W['jealous']} spreads his arms in "
     f"delighted welcome."),
    ("j12", ["loc_jealous_hall", "charles_diego", "george_meanwell", "jealous"],
     f"In the hall, {W['jealous']} leans forward expectantly, palm out; "
     f"{W['meanwell']} has frozen mid-stammer, sweat at his temple, eyes "
     f"darting sideways; behind his raised Spanish hat {W['diego']} hisses "
     f"into Meanwell's ear."),
    ("j13", ["loc_jealous_hall", "isabinda", "jealous", "charles_diego", "george_meanwell"],
     f"In the hall, {W['isabinda']} kneels clinging to the knees of "
     f"{W['jealous']}, face averted from the Spaniard, eyes screwed shut; "
     f"{W['diego']} stands rigid two steps away, hands clenched behind his "
     f"back; {W['meanwell']} kneels solicitously beside her, lips at her ear."),
    ("j14", ["loc_jealous_street", "marplot", "whisper"],
     f"Dusk at the merchant's front door: {W['marplot']} interrogates a "
     f"stone-faced SERVANT in plain livery holding the door invitingly wide; "
     f"at the street corner behind them {W['whisper']} flattens himself "
     f"against the bricks, face in his hands in despair."),
    ("j15", ["loc_jealous_hall", "george", "jealous", "marplot"],
     f"Climax: before the parlor door, {W['george']} — his merchant disguise "
     f"half-off, sword DRAWN and level — stands guard, grinning; a huddle of "
     f"three SERVANTS with sticks shuffle at bay, none willing to be first; "
     f"{W['jealous']} vents his fury swatting his cane at a cowering "
     f"{W['marplot']}. Cartoonish farce, no blood."),
    ("j16", ["loc_jealous_hall", "charles_diego", "isabinda", "jealous"],
     f"The parlor doors stand open: {W['diego']}, Spanish hat cast off, one "
     f"arm around {W['isabinda']}, plants himself between his bride and "
     f"everyone else; {W['jealous']} staggers back a step, hand to his chest, "
     f"thunderstruck."),
    ("j17", ["loc_jealous_hall", "francis", "miranda", "george", "charles", "isabinda", "jealous"],
     f"Full-company tableau in the hall: {W['francis']} stands apoplectic, "
     f"cane raised at heaven, mid-curse; beside him {W['miranda']} calmly "
     f"hands a folded parchment to {W['charles']}; {W['george']} stands at "
     f"Miranda's shoulder, serene; {W['jealous']} is caught mid-laugh at his "
     f"fellow guardian; {W['isabinda']} beams on Charles's arm."),
    ("j18", ["loc_jealous_hall", "jealous", "charles", "isabinda", "george", "miranda", "marplot"],
     f"The finale: the hall warm with candlelight, two FIDDLERS playing in "
     f"the corner; {W['jealous']} clasps hands with {W['charles']} in "
     f"blessing; {W['george']} and {W['miranda']} and {W['isabinda']} raise "
     f"glasses; front and center {W['marplot']} rubs his bruises and musters "
     f"a brave hopeful smile at the camera."),
    ("j19", ["loc_jealous_hall", "jealous"],
     f"Close on {W['jealous']}, glass of wine raised directly to the camera, "
     f"warm and rueful, the wedding dance a whirl of color and candlelight "
     f"softly blurred behind him."),
]
FRAMES_SPEC = [(n, "16:9", p, r) for n, r, p in F]


def resolve_ref(r: str) -> Path:
    p = ANCH / f"{r}.png"
    if p.exists():
        return p
    raise FileNotFoundError(f"ref {r} not found in {ANCH}")


def make(outdir: Path, name: str, aspect: str, prompt: str, refs: list) -> str:
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
    if stage == "anchors":
        jobs, outdir = ANCHORS, ANCH
    elif stage == "variants":
        jobs, outdir = VARIANTS, ANCH
    elif stage == "frames":
        jobs, outdir = FRAMES_SPEC, FRAMES
    else:
        sys.exit(f"unknown stage {stage}")
    outdir.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        futs = [pool.submit(make, outdir, n, a, p, r) for n, a, p, r in jobs]
        for f in futs:
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
