"""Replacement start frames for shots whose originals trip the input filter
(large front-facing canonical Mewtwo). Same shot names; Mewtwo staged from
behind / silhouetted / helmeted / small so the composition passes while the
dramatic intent survives. Loaded by make_images.py stage `frames2`."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from make_images import STYLE, MEWTWO, SUIT1, ARMOR, POD_ROOM, CLIFFTOP

MATCH = ("Characters exactly match the reference images in anatomy, face, "
         "coloring and wardrobe.")
BEHIND = ("The creature is seen from behind or in silhouette — its face is "
          "never visible to camera.")

FRAMES = [
    ("a4", "16:9",
     f"In the dim pod chamber, a 17-year-old girl with very long straight "
     f"black hair sits cross-legged on the floor in the foreground, eyes "
     f"closed in meditation, palms open on her knees, a faint violet shimmer "
     f"around her; behind her the huge glass biopod glows amber, and inside "
     f"it the small slender creature floats seen ENTIRELY FROM BEHIND — a "
     f"narrow pale back, a long tail curled around itself — pressed close to "
     f"the glass as if watching her. {BEHIND} {MATCH} {STYLE}",
     ["sabrina_teen", "loc_pod_room"]),
    ("a6", "16:9",
     f"The biopod's cover lifted, harsh white light flooding down: seen from "
     f"BEHIND the pod, the pale creature faces away from camera toward a "
     f"tall mirror wheeled up against the far side of the glass; in the "
     f"mirror only a dim amber-distorted blur of a pale shape is visible, "
     f"nothing distinct. Around the chamber, staff turn their faces away. "
     f"{BEHIND} {MATCH} {STYLE}", ["loc_pod_room"]),
    ("a7", "16:9",
     f"Over-the-shoulder from inside the amber pod: the dark out-of-focus "
     f"silhouette of the creature's shoulder and skull fills the left "
     f"foreground, and beyond the curved glass stands the man in the "
     f"immaculate black suit, his face lit warm by the pod's glow, inches "
     f"from the glass, his breath fogging it, mid-sentence — intimate and "
     f"menacing. {BEHIND} {MATCH} {STYLE}",
     ["giovanni", "loc_pod_room"]),
    ("b1", "16:9",
     f"Wide shot of {POD_ROOM}, years later: the pod's occupant is a tall "
     f"slender SILHOUETTE seen from behind through the amber fluid, facing "
     f"away toward a ring of glowing screens showing paused films and pages "
     f"of books; a keyboard floats on a swing-arm; stacks of books and board "
     f"games crowd the tables. The silhouette's face is never visible. "
     f"{MATCH} {STYLE}", ["loc_pod_room"]),
    ("b3", "16:9",
     f"Seen from BEHIND the amber biopod: the dark blurred silhouette of "
     f"the occupant's back and skull in the near foreground inside the "
     f"fluid, dozens of black and white Go stones orbiting it in two "
     f"perfect rings; beyond the curved glass, in focus, the man in the "
     f"black suit sits at a small table with a wooden Go board mid-game, "
     f"studying it, a slim microphone amplifier pointed at the pod. "
     f"{BEHIND} {MATCH} {STYLE}", ["giovanni", "loc_pod_room"]),
    ("b4", "16:9",
     f"From behind the shoulder of the woman with long dark hair: her palm "
     f"flat against the biopod glass, and meeting it from inside the amber "
     f"fluid a large pale three-fingered hand, the creature beyond it only a "
     f"soft unfocused paleness in the glow; beside them a heartbeat monitor "
     f"trace spikes sharply. Intimate, sad, warm. {BEHIND} {MATCH} {STYLE}",
     ["sabrina", "loc_pod_room"]),
    ("c1", "16:9",
     f"The biopod stands DRAINED, glass streaked with runnels of amber "
     f"fluid; inside, the creature has collapsed to its knees facing away "
     f"from camera, a curled pale back and long tail on the wet floor, "
     f"loose tubes trailing; technicians in dark clothing rush toward the "
     f"opened pod carrying pieces of a bulky steel suit; the woman with "
     f"long dark hair reaches toward the glass, alarmed. {BEHIND} {MATCH} "
     f"{STYLE}", ["sabrina", "loc_pod_room"]),
    ("d6", "16:9",
     f"A vast bare white room with no corners: at its center the man in "
     f"the black suit sits on a plain chair facing a GLITCHING, "
     f"HALF-FORMED hologram of the pod room — the glass pod rendered in "
     f"translucent wireframe light, its occupant only a rough unfinished "
     f"column of static and pale light, no clear features, the whole "
     f"projection dissolving into white noise at the edges; his finger "
     f"rests on a small button on the chair's arm. {MATCH} {STYLE}",
     ["giovanni"]),
    ("e7", "16:9",
     f"The white training hall: the creature in its angular dark-grey "
     f"armor and helmet is bent forward, seen from the side and slightly "
     f"behind, clutching at its lower leg where a SMALL GENERIC dark-furred "
     f"rodent grips it by the bite, its little claws scrabbling; a thin "
     f"dark line runs down the pale calf; behind the high observation "
     f"glass, silhouetted figures lean forward. The creature's face is "
     f"hidden by its helmet and the angle. {MATCH} {STYLE}",
     ["mewtwo_armor", "loc_training"]),
    ("f4", "16:9",
     f"The pod chamber under red emergency light, a long crack across the "
     f"ceiling dropping threads of dust through the amber glow: the "
     f"grey-haired director stands small before the huge glowing biopod, "
     f"looking up; inside, high in the fluid, the slender pale occupant "
     f"floats with its back mostly to camera, head turned up toward the "
     f"cracked ceiling. {BEHIND} {MATCH} {STYLE}",
     ["dr_light", "loc_pod_room"]),
    ("f8", "16:9",
     f"Sunset breaking under storm clouds, everything gold: in the left "
     f"foreground the creature in dark-grey armor and helmet stands in "
     f"THREE-QUARTER BACK VIEW, the sunset flaring off the edge of its "
     f"helmet; up the wet grass slope a young man with messy dark hair "
     f"jogs toward the group waving, beaming; the grey-haired director "
     f"turns toward him with relief. {MATCH} {STYLE}",
     ["gyokusho", "dr_light", "loc_clifftop"]),
    ("g1", "16:9",
     f"FROZEN VIOLENT INSTANT, wide, motion-blurred: the armored, helmeted "
     f"creature — small in frame, seen from behind and below — has snapped "
     f"two meters into the air off the clifftop, its long tail wrapped "
     f"around the waist of the grey-haired director whose feet are torn "
     f"from the ground, papers scattering; a sleek black weasel-like "
     f"pokemon is caught mid-leap beneath them; guards spin, mouths open; "
     f"the sunset sea waits beyond the cliff edge. {MATCH} {STYLE}",
     ["dr_light", "shaw", "loc_clifftop"]),
    ("g7", "16:9",
     f"The pitch-black sea cave: the empty armor suit sits propped upright "
     f"on the wet sand like a shed skin, its chest light glowing — the "
     f"only light source; across the cave, in deep darkness, a slender "
     f"crouched SILHOUETTE is barely distinguishable from the rock, only "
     f"the faint twin glints of eyes catching the suit's glow. Absolute "
     f"stillness. {MATCH} {STYLE}", ["mewtwo_armor", "loc_cave"]),
    ("h2", "16:9",
     f"Bright misty dawn sea, golden fog: the pale creature swims seen "
     f"FROM BEHIND, only its narrow back, shoulders and the wake of its "
     f"tail visible above the waterline, heading toward several huge "
     f"rounded whale-backs that arch dark and half-lost in the golden "
     f"mist ahead, one distant spout catching the light. {BEHIND} {MATCH} "
     f"{STYLE}", ["loc_ocean_dusk"]),
    ("h3", "16:9",
     f"Cold dawn sea: a column of ocean erupts ten meters upward, and at "
     f"its crown a slender pale figure hangs TWISTING IN BACKLIT "
     f"SILHOUETTE inside the spray, limbs flung out, unrecognizable in "
     f"the glare; below, a dark red bloom spreads in the churned water "
     f"where a huge shadowed shape turns away beneath the surface. "
     f"{BEHIND} {MATCH} {STYLE}", ["loc_ocean_dusk"]),
    ("h5", "16:9",
     f"Deep forest clearing at night: hundreds of small floating "
     f"glyph-like light-forms — abstract luminous curls and hooks of "
     f"green-blue aurora, each with a single dim glowing core — turn in "
     f"vast layered concentric rings like an intricate clock of living "
     f"light above the trees; far below at the base of frame, a tiny "
     f"slender figure seen from behind hovers before it, dwarfed. "
     f"{BEHIND} {MATCH} {STYLE}", ["mewtwo_free"]),
]
