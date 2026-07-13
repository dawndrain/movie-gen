"""Scene start-frame prompts for the Hork-Bajir Chronicles. Loaded by make_images.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from make_images import STYLE, HORK, ANDALITE, ARN, VALLEY

NOMOUTH = "The Andalite face has NO mouth — eyes only."
MATCH = "Characters exactly match the reference images in anatomy, coloring and build."

# (name, aspect, prompt, [anchor refs])
FRAMES = [
    # ---- Act 0: frame story (Earth, golden hour) ----
    ("f1", "16:9",
     f"Aerial shot: a red-tailed hawk rides a thermal high over a hidden Sierra "
     f"Nevada valley at golden hour — granite walls, pines, a creek below. Wings "
     f"spread, feathers backlit. {MATCH} {STYLE}", ["tobias", "loc_earth_valley"]),
    ("f2", "16:9",
     f"In an earthly pine valley at golden hour, a red-tailed hawk perches on a low "
     f"branch, head cocked, listening to {HORK} — an older, battle-scarred male with "
     f"chipped blades — who sits on a fallen log facing the hawk, one clawed hand "
     f"raised mid-story. Warm, intimate firelight from a small camp fire. {MATCH} "
     f"{STYLE}", ["jara", "tobias", "loc_earth_valley"]),
    ("f3", "16:9",
     f"Movie title card: over a wide vista of {VALLEY}, enormous weathered "
     f"bone-white carved letters float, reading exactly: \"THE HORK-BAJIR "
     f"CHRONICLES\". Elegant epic title typography, letters like carved horn. "
     f"The title text must be spelled exactly as given. {STYLE}",
     ["loc_valley"]),

    # ---- Act 1: exile ----
    ("a1", "16:9",
     f"An Andalite dome ship — a vast elegant ivory starship shaped like a "
     f"transparent-domed disc containing a green meadow, atop a long slender "
     f"engine shaft — descends slowly through the pale sky over {VALLEY}. Scale: "
     f"the ship is dwarfed by the trees. {STYLE}", ["loc_valley"]),
    ("a2", "16:9",
     f"Inside a transparent geodesic dome on a ridge at dusk: an aging male "
     f"{ANDALITE} with greying fur gazes out at the colossal alien trees, while "
     f"his adolescent daughter — smaller, lavender-blue fur — stands behind him, "
     f"main eyes narrowed in frustration, arms crossed. {NOMOUTH} {MATCH} {STYLE}",
     ["seerow", "aldrea", "loc_dome"]),
    ("a3", "16:9",
     f"A young female {ANDALITE} gallops at full stride along a grassy ridge above "
     f"{VALLEY}, tail streaming, stalk eyes swiveled toward the vast trees below, "
     f"golden light, motion and joy. {NOMOUTH} {MATCH} {STYLE}",
     ["aldrea", "loc_valley"]),

    # ---- Act 2: Dak ----
    ("b1", "16:9",
     f"Peaceful daily life of the Hork-Bajir: on a branch wide as a road in "
     f"{VALLEY}, six or seven varied individuals of {HORK} — different heights, "
     f"skin tones and blade shapes, males and females and one small child — "
     f"placidly strip and eat bark with their wrist blades. Gentle pastoral mood. "
     f"{MATCH} {STYLE}", ["dak", "jagil", "loc_valley"]),
    ("b2", "16:9",
     f"Close on a young male {HORK} crouched on a branch, using one claw to draw "
     f"careful circles and spiral orbit-diagrams in pale bark-dust, his eyes "
     f"bright with focus, while a stockier bark-brown male watches over his "
     f"shoulder, baffled, mid-chew. {MATCH} {STYLE}", ["dak", "jagil"]),
    ("b3", "16:9",
     f"On a great branch at dusk, an ancient stooped grey {HORK} elder with "
     f"yellowed cracked blades raises both arms, pronouncing solemnly over the "
     f"young seer who kneels before him; a loose circle of a dozen Hork-Bajir "
     f"watch in awed silence, valley mist behind. {MATCH} {STYLE}",
     ["dak", "jagil", "loc_valley"]),
    ("b4", "16:9",
     f"First meeting: on a huge branch in {VALLEY}, a young male {HORK} freezes "
     f"mid-step, staring at a young female {ANDALITE} who stands calmly in dappled "
     f"light where no Andalite should be, her stalk eyes fixed on him, tail blade "
     f"lowered peaceably. Ten feet apart, wary and curious. {NOMOUTH} {MATCH} "
     f"{STYLE}", ["dak", "aldrea", "loc_valley"]),
    ("b5", "16:9",
     f"Night on a high branch: a glowing blue holographic star map — suns, orbit "
     f"rings, tiny worlds — spins in the air between a young female {ANDALITE} "
     f"and a young male {HORK} who reaches one careful claw toward a projected "
     f"star, his face lit blue with wonder. {NOMOUTH} {MATCH} {STYLE}",
     ["dak", "aldrea"]),
    ("b6", "16:9",
     f"Comedy beat in golden light: a young female {ANDALITE} lands awkwardly from "
     f"a branch-to-branch leap, all four legs splayed, dignity gone, while a young "
     f"male {HORK} throws his head back laughing, one arm pointing at her. Warm "
     f"friendship. {NOMOUTH} {MATCH} {STYLE}", ["dak", "aldrea", "loc_valley"]),

    # ---- Act 3: the Deep / the Arn ----
    ("c1", "16:9",
     f"A young male {HORK} and a young female {ANDALITE} pick their way down a "
     f"root the size of a cathedral buttress into the Deep — blue and violet "
     f"bioluminescent fungus shelves, thick mist below, the last daylight a faint "
     f"memory far above. {NOMOUTH} {MATCH} {STYLE}",
     ["dak", "aldrea", "loc_deep"]),
    ("c2", "16:9",
     f"Terror in the Deep: out of black mist a monstrous predator lunges — a "
     f"whale-sized armored horror of too many jaws and pale blind eyes, "
     f"bioluminescence glinting off wet plates — while a young {HORK} and a young "
     f"{ANDALITE} scramble up a root, barely ahead of it. {MATCH} {STYLE}",
     ["dak", "aldrea", "loc_deep"]),
    ("c3", "16:9",
     f"Reveal: from a high rock ledge, a young {HORK} and a young {ANDALITE} stand "
     f"silhouetted, tiny, gazing down on a hidden cavern city of polished amber "
     f"and jade towers and glowing terraced gardens stretching into the dark. "
     f"{MATCH} {STYLE}", ["dak", "aldrea", "loc_arn_city"]),
    ("c4", "16:9",
     f"On an amber terrace, {ARN} confronts the two intruders — a young {HORK} "
     f"and a young {ANDALITE} — crest flared in outrage, one thin arm pointing "
     f"at the Hork-Bajir accusingly. The Arn is small but utterly unafraid. "
     f"{NOMOUTH} {MATCH} {STYLE}", ["arn", "dak", "aldrea", "loc_arn_city"]),
    ("c5", "16:9",
     f"{ARN} stands before a wall of turquoise-glowing gene-tanks, gesturing "
     f"grandly at rows of pale embryonic Hork-Bajir shapes suspended inside "
     f"them, while a young male {HORK} stares at the tanks, seeing his own "
     f"reflection over the embryos. Devastating revelation. {MATCH} {STYLE}",
     ["arn", "dak", "loc_arn_city"]),
    ("c6", "16:9",
     f"Aftermath: a young male {HORK} sits slumped on a great root in blue "
     f"fungal light, shoulders down, blades dim, staring at his own open claws; "
     f"beside him a young female {ANDALITE} rests one slim hand on his shoulder. "
     f"Quiet grief and comfort. {NOMOUTH} {MATCH} {STYLE}",
     ["dak", "aldrea", "loc_deep"]),

    # ---- Act 4: the Yeerks arrive ----
    ("d1", "16:9",
     f"Dread establishing shot: a swarm of Yeerk bug fighters — cockroach-like "
     f"gunmetal attack ships, each with two long serrated spear-points thrust "
     f"forward — descends in formation through the pale sky of {VALLEY}, engine "
     f"glow reflecting off the canopy. {STYLE}", ["loc_valley"]),
    ("d2", "16:9",
     f"On the dark steel bridge of a pool ship, {HORK} stands unnaturally rigid "
     f"in a segmented black-and-crimson military harness, cold cruel eyes "
     f"reflecting a tactical display of the tree world, flanked by shadowed "
     f"consoles and orange industrial light. {MATCH} {STYLE}",
     ["esplin", "loc_poolship"]),
    ("d3", "16:9",
     f"Night horror, discreet staging: in a burned clearing among giant roots, a "
     f"freshly dug earthen pool of dull leaden-grey liquid steams under harsh "
     f"portable lights; armed Hork-Bajir guards in black harnesses flank a line "
     f"of unarmed Hork-Bajir, and at the pool's edge one kneels, head bowed "
     f"toward the grey water. Silhouettes and shadow, no gore. {MATCH} {STYLE}",
     ["dak", "loc_poolship"]),
    ("d4", "16:9",
     f"Two young male {HORK} face each other on a branch at dusk: the slimmer one "
     f"searching his friend's face with worried eyes, the stockier bark-brown one "
     f"standing too still, expression flat and wrong, eyes empty. Unease. {MATCH} "
     f"{STYLE}", ["dak", "jagil"]),
    ("d5", "16:9",
     f"Night attack: crimson energy beams rake the transparent dome outpost on "
     f"the ridge, panels shattering, meadow burning; an aging male {ANDALITE} "
     f"with greying fur wheels toward the camera mid-shout, main eyes wide, as "
     f"his daughter gallops away from the blast light. {NOMOUTH} {MATCH} {STYLE}",
     ["seerow", "aldrea", "loc_dome"]),
    ("d6", "16:9",
     f"Dawn after the attack: a young female {ANDALITE} stands alone amid the "
     f"smoking skeleton of the shattered dome, scorched grass, broken ivory "
     f"instruments, ash drifting like snow. She is very small in the wide frame. "
     f"{NOMOUTH} {MATCH} {STYLE}", ["aldrea", "loc_dome"]),

    # ---- Act 5: resistance ----
    ("e1", "16:9",
     f"On a storm-grey morning branch, a young female {ANDALITE} leans urgently "
     f"toward a young male {HORK}, tail blade quivering with intensity, while he "
     f"turns half away, torn, one hand gripping the bark. Argument between "
     f"friends. {NOMOUTH} {MATCH} {STYLE}", ["dak", "aldrea", "loc_valley"]),
    ("e2", "16:9",
     f"Quiet strange moment: a young female {ANDALITE} presses her slim "
     f"many-fingered hand flat against the chest of a young male {HORK}, whose "
     f"eyes have gone calm and unfocused, trance-like; faint light seems to pass "
     f"between them. {NOMOUTH} {MATCH} {STYLE}", ["dak", "aldrea"]),
    ("e3", "16:9",
     f"Transformation mid-frame: a creature caught halfway between {ANDALITE} and "
     f"{HORK} — blue fur receding into leathery green-brown skin, forehead blades "
     f"erupting, four legs fusing into two powerful ones, stalk eyes shrinking "
     f"away — body-horror wonder, backlit by sunrise on a great branch. {STYLE}",
     ["aldrea", "aldrea_hb"]),
    ("e4", "16:9",
     f"Training: on a wide branch, a young male {HORK} demonstrates a blade-block "
     f"stance before a ragged line of a dozen varied free Hork-Bajir who copy him "
     f"clumsily, gentle faces set with unfamiliar resolve; a slender female with "
     f"blue-grey sheen stands at his side. {MATCH} {STYLE}",
     ["dak", "aldrea_hb", "loc_valley"]),
    ("e5", "16:9",
     f"After the ambush, rain: a young male {HORK} stands over a fallen enemy of "
     f"his own species wearing a black-and-crimson harness, the victor's blades "
     f"lowered, his face grief-stricken rather than triumphant; other free "
     f"Hork-Bajir stand back in the mist. No gore. {MATCH} {STYLE}",
     ["dak", "loc_valley"]),
    ("e6", "16:9",
     f"On the pool ship bridge, the harnessed Hork-Bajir commander turns from a "
     f"flickering battle report hologram, head tilted with predatory interest, "
     f"cold eyes catching the light, subordinate Controllers rigid behind him. "
     f"{MATCH} {STYLE}", ["esplin", "loc_poolship"]),

    # ---- Act 6: Alloran and the virus ----
    ("g1", "16:9",
     f"Eight sleek ivory Andalite fighter craft stand on a scorched ridge "
     f"clearing at dawn; before them a powerfully built male {ANDALITE} warrior "
     f"with slate-blue fur, a flank scar and a military bandolier surveys the "
     f"burning valley below, tail blade high. {NOMOUTH} {MATCH} {STYLE}",
     ["alloran", "loc_valley"]),
    ("g2", "16:9",
     f"Face-off: the scarred war-prince {ANDALITE} and the young female {ANDALITE} "
     f"circle each other in dome-ship wreckage, tails half-raised, main eyes "
     f"locked, stalk eyes rigid — an argument on the edge of violence. {NOMOUTH} "
     f"{MATCH} {STYLE}", ["alloran", "aldrea"]),
    ("g3", "16:9",
     f"Close-up: the war-prince {ANDALITE}'s many-fingered hand holds up a small "
     f"crystalline vial in which a sickly blue-white light slowly swirls like "
     f"trapped smoke; his cold main eyes regard it with grim satisfaction. "
     f"{NOMOUTH} {MATCH} {STYLE}", ["alloran"]),
    ("g4", "16:9",
     f"Night heist: a young male {HORK} and a young female {ANDALITE} slip "
     f"between sleeping ivory fighter craft in an Andalite camp, the Hork-Bajir "
     f"cradling the glowing crystalline vial close to his chest, both crouched "
     f"low, moonlight and long shadows. {NOMOUTH} {MATCH} {STYLE}",
     ["dak", "aldrea"]),
    ("g5", "16:9",
     f"Ambush chaos at night in the branches: crimson energy fire streaks the "
     f"dark, bark exploding into splinters; a young male {HORK} is thrown back "
     f"clutching his side while the glowing crystalline vial spins away from his "
     f"open claw into the abyss below, shattering into blue-white mist. {MATCH} "
     f"{STYLE}", ["dak", "aldrea", "loc_valley"]),
    ("g6", "16:9",
     f"Devastation, silent wide shot: {VALLEY} desaturated and still — untended "
     f"bark peeling grey, empty branches, no movement anywhere, pale spores "
     f"drifting down like ash through shafts of cold light. {STYLE}",
     ["loc_valley"]),

    # ---- Act 7: nothlit / last stand ----
    ("h1", "16:9",
     f"Sunrise on a high branch: a young male {HORK} looks at a slender female of "
     f"his own species with a blue-grey sheen and large deep-green eyes; she "
     f"meets his gaze steadily, calm and resolved, the rising sun between them. "
     f"Tender, momentous. {MATCH} {STYLE}", ["dak", "aldrea_hb", "loc_valley"]),
    ("h2", "16:9",
     f"In the highest thin branches above the cloud layer, a small ragged band of "
     f"a dozen free Hork-Bajir — males, females, two children — shelter in a "
     f"woven-branch hide, the young seer standing watch at the edge with the "
     f"blue-sheened female beside him, dawn light on their blades. Hope amid "
     f"ruin. {MATCH} {STYLE}", ["dak", "aldrea_hb", "loc_valley"]),
    ("h3", "16:9",
     f"Epilogue: at a tall viewport of the pool ship bridge, the harnessed "
     f"Hork-Bajir commander stands alone gazing out at a field of stars, hands "
     f"clasped behind his back, the conquered tree world turning below. Cold "
     f"ambition. {MATCH} {STYLE}", ["esplin", "loc_poolship"]),

    # ---- Act 8: frame close (Earth, dusk) ----
    ("i1", "16:9",
     f"Back on Earth at dusk: the old scarred {HORK} spreads both arms wide, "
     f"finishing his tale before the red-tailed hawk on its low branch, camp "
     f"fire embers rising between them, first stars out. {MATCH} {STYLE}",
     ["jara", "tobias", "loc_earth_valley"]),
    ("i2", "16:9",
     f"An adolescent female {HORK} — smaller, slender, smooth olive-green skin, "
     f"strikingly focused eyes — steps into the firelight beside the old scarred "
     f"male, standing straight and proud before the watching hawk. {MATCH} "
     f"{STYLE}", ["toby", "jara", "tobias", "loc_earth_valley"]),
    ("i3", "16:9",
     f"Final shot: the red-tailed hawk lifts off a pine branch and flies away "
     f"over the darkening Sierra valley into a deep orange sunset, wings wide, "
     f"one bright star above. {MATCH} {STYLE}", ["tobias", "loc_earth_valley"]),
]
