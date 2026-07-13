"""Scene start-frame prompts for THE DAVID TRILOGY. Loaded by make_images.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from make_images import STYLE, WARDROBE

J, R, C, M, D = (WARDROBE[k] for k in ("jake", "rachel", "cassie", "marco", "david"))

NOMOUTH = "The Andalite face has NO mouth — eyes only."
MATCH = "Characters exactly match the reference images in face, hair, build and clothing."
TIGER = "a massive Siberian tiger"
LION = "a huge male African lion with a full dark mane"
EAGLE = "a golden eagle"
HAWK = "a red-tailed hawk"
RAT = "a small brown rat"

# (name, aspect, prompt, [anchor refs])
FRAMES = [
    # ---- Act A: The Discovery ----
    ("a1", "16:9",
     f"Night at a half-built suburban construction site. {D} crouches in the mud "
     f"between plywood house frames, holding a small flashlight; the beam lands on "
     f"a glowing translucent BLUE CUBE the size of a softball, half buried in the "
     f"dirt. Cold moonlight, his face underlit blue with greedy wonder. {MATCH} "
     f"{STYLE}", ["david", "loc_construction"]),
    ("a2", "16:9",
     f"A teenage boy's messy bedroom at night, lit by a desktop monitor. {D} sits "
     f"typing at the keyboard; beside the keyboard the glowing blue alien cube "
     f"sits on a pile of comic books, casting blue light on his grinning face. "
     f"Posters, dirty laundry, a terrarium in the corner. {MATCH} {STYLE}",
     ["david"]),
    ("a3", "16:9",
     "Movie title card: over a wide night vista of a half-built suburban "
     "construction site glowing faintly blue from a buried light, elegant steel "
     "movie-title typography floats, reading exactly: \"ANIMORPHS\" in small "
     "letters above \"THE DAVID TRILOGY\" in large letters. The title text must "
     f"be spelled exactly as given. {STYLE}", ["loc_construction"]),
    ("a4", "16:9",
     f"A tidy teenage bedroom at night. {M} sits on the bed holding an open "
     f"laptop turned toward {J}, who leans in, gripping the back of a chair, his "
     f"face grim in the screen light; on the laptop screen a blurry auction-site "
     f"photo of a glowing blue cube. {MATCH} {STYLE}", ["jake", "marco"]),
    ("a5", "16:9",
     f"Night on a suburban street: a matte-black angular alien dropship hovers "
     f"low over the rooftops, and three seven-foot bladed alien soldiers — the "
     f"same species as the reference image, leathery skin, scythe blades on "
     f"forearms and skull-crest, wearing segmented black-and-crimson harnesses — "
     f"stride across a front lawn toward a small house whose windows flash with "
     f"red beam light. Dread, discreet, no gore. {STYLE}",
     ["esplin", "loc_construction"]),
    ("v1", "16:9",
     f"On the black-steel bridge of an alien warship in deep red light stands a "
     f"scarred, dark-furred alien centaur — EXACTLY matching the reference image: "
     f"four legs, upright torso with two arms, a mouthless triangular face with "
     f"two main eyes and two small stalk eyes atop the head, and a long tail "
     f"ending in a scythe blade, raised high. Before him a red hologram shows a "
     f"suburban house. {NOMOUTH} {MATCH} {STYLE}", ["visser", "loc_bladeship"]),
    ("a6", "16:9",
     f"Night inside a barn wildlife clinic, one hanging lantern. {D}, a blanket "
     f"over his shoulders, sits on a hay bale, hollow-eyed. Facing him stand {J} "
     f"and {C}, grave and gentle; behind them {R} and {M} watch with arms "
     f"crossed. {MATCH} {STYLE}",
     ["david", "jake", "cassie", "rachel", "marco", "loc_barn"]),
    ("a7", "16:9",
     f"Close scene in lantern light: the glowing blue cube sits on a hay bale. "
     f"{D} reaches one hand toward it, palm hovering an inch above the surface, "
     f"blue light between skin and cube. {J} stands square across the bale, "
     f"solemn; {M} beside him looks away, jaw tight. {MATCH} {STYLE}",
     ["david", "jake", "marco", "loc_barn"]),
    ("a8", "16:9",
     f"VFX morph shot in a barn hayloft at night, moon through the loft door: "
     f"{D} mid-transformation into {EAGLE} — his arms already feathered golden "
     f"wings, body shrinking, eyes turned fierce gold, expression of terrified "
     f"exhilaration. Practical-effects realism, uncanny but not gory. {MATCH} "
     f"{STYLE}", ["david", "loc_barn"]),

    # ---- Act B: The Threat ----
    ("b1", "16:9",
     f"Night in a zoo's lion habitat, dim service lights. A huge male lion "
     f"sleeps on a rock shelf, and {D} kneels beside it with one bare hand "
     f"pressed to its flank, eyes half-closed in a trance, a slow hungry grin. "
     f"Behind the enclosure rail, {R} watches with folded arms, deeply uneasy. "
     f"{MATCH} {STYLE}", ["david", "rachel"]),
    ("b2", "16:9",
     f"Night service rooftop overlooking a glassy resort hotel with flags of "
     f"many nations. {J} stands at the parapet edge mid-order, jaw set; {D} "
     f"squares up to him a foot away, chin raised, insolent; behind them {M} "
     f"and {R} exchange a look. Everyone's hands are EMPTY — no cube, no "
     f"glowing object anywhere in this scene. Wind, city glow. {MATCH} {STYLE}",
     ["jake", "david", "marco", "rachel", "loc_hotel"]),
    ("b3", "16:9",
     f"Chaos in an elegant hotel corridor: {LION} stands mid-roar on the marble "
     f"floor, hackles up, as suited security men dive behind an overturned "
     f"luggage cart, an alarm strobe flashing, a chandelier swinging. No blood. "
     f"{STYLE}", ["loc_hotel"]),
    ("b4", "16:9",
     f"Barn at night, tempers high. {M} jabs a finger at {D} across the lantern "
     f"light; {D} leans forward, fists balled, face twisted with resentment. {J} "
     f"holds an arm out between them; {R} behind {D}, eyes narrow. {MATCH} "
     f"{STYLE}", ["marco", "david", "jake", "rachel", "loc_barn"]),
    ("b5", "16:9",
     f"Golden hour over a quiet meadow with one huge lone oak. On a high branch "
     f"perches {HAWK} — and above, talons already spread, {EAGLE} stoops down "
     f"on it like a missile out of the sun. Dread, motion frozen an instant "
     f"before impact. {STYLE}", ["tobias", "loc_meadow"]),
    ("b6", "16:9",
     f"Dusk at the base of the lone oak. {R} kneels in the long grass, holding "
     f"three russet-red tail feathers, her face white with grief and rage; {J} "
     f"stands behind her, one hand half-raised, helpless. Drifting feathers in "
     f"the grass. {MATCH} {STYLE}", ["rachel", "jake", "loc_meadow"]),
    ("b7a", "16:9",
     f"Night at the construction site, mud and plywood frames in cold moonlight: "
     f"{TIGER} and {LION} circle each other ten feet apart between the house "
     f"skeletons, heads low, shoulders rolling, eyes locked. {STYLE}",
     ["loc_construction"]),
    ("b7b", "16:9",
     f"Mid-fight at the night construction site: {TIGER} and {LION} rear up "
     f"colliding chest to chest in a burst of mud and splintering plywood, claws "
     f"wide, mouths open in a snarl, dust in the moonlight. Ferocious but no "
     f"blood or wounds. {STYLE}", ["loc_construction"]),
    ("b7c", "16:9",
     f"Night construction site: {LION} pins {TIGER} on its back at the edge of a "
     f"foundation trench, jaws at its throat — while behind them a huge grizzly "
     f"bear EXPLODES through a plywood wall in a shower of splinters, mid-charge. "
     f"No blood. {STYLE}", ["loc_construction"]),

    # ---- Act C: The Solution ----
    ("c1", "16:9",
     f"Barn at night, aftermath. {J}, dirt-streaked and shaken, sits on a hay "
     f"bale with his forearms on his knees; {C} stands in the lantern light "
     f"mid-sentence, calm and sad, one hand open; {R}, {M} watch from the "
     f"shadows; at the back, an alien centaur with an upright torso, stalk eyes "
     f"and a scythe tail stands half-lit. {MATCH} {STYLE}",
     ["jake", "cassie", "rachel", "marco", "ax", "loc_barn"]),
    ("c2", "16:9",
     f"Barn at night: {HAWK} back-wings onto a rafter beam in the lantern light, "
     f"wings spread wide, and below {R} looks up with parted lips — grief "
     f"collapsing into disbelieving joy; {J} and {C} turn, stunned. {MATCH} "
     f"{STYLE}", ["tobias", "rachel", "jake", "cassie", "loc_barn"]),
    ("c3", "16:9",
     f"Late night planning in the barn: a hand-drawn coastline map spread on a "
     f"crate under the lantern, stones weighting the corners. {C} leans over it "
     f"whispering, tracing the cove with a finger; {M} marks an X; {J} listens "
     f"with arms crossed, face half in shadow. Conspiratorial. {MATCH} {STYLE}",
     ["cassie", "marco", "jake", "loc_barn"]),
    ("c4", "16:9",
     f"THE STAGED MEETING, from floor level: in the background, slightly "
     f"defocused, five teenagers — {J}, {R}, {C}, {M} — and an alien centaur "
     f"stand in a circle around the lantern, mid-council; in the SHARP FOREGROUND, "
     f"in a dark gap beneath the plank floorboards, {RAT} crouches listening, "
     f"lamplight glinting in its black eyes. {MATCH} {STYLE}",
     ["jake", "rachel", "cassie", "marco", "ax", "loc_barn"]),
    ("c5", "16:9",
     f"High rafter point-of-view looking steeply down into the lantern-lit barn: "
     f"in the near foreground {HAWK} perches on the beam, head bent to watch the "
     f"floor far below, where {RAT} — tiny with distance, DOWN ON THE FLOOR, "
     f"never on the beam — slips out through a gap at the base of the barn wall; "
     f"the teenagers stand small around the lantern, not turning. {STYLE}",
     ["tobias", "loc_barn"]),
    ("c6", "16:9",
     f"Cold grey dawn at a rocky cove under cliffs. {R} stands alone on a flat "
     f"wet boulder among tide pools, the glowing blue cube held under one arm, "
     f"hair whipping in the sea wind, shouting a challenge at the empty rocks. "
     f"{MATCH} {STYLE}", ["rachel", "loc_cove"]),
    ("c7", "16:9",
     f"The trap springs at the dawn cove: {LION} stands frozen at the center of "
     f"a ring closing in on it — a grizzly bear rising to full height on a "
     f"boulder, a silverback gorilla knuckling forward over the tide pools, a "
     f"grey wolf hackles-up on the sand, {TIGER} advancing at the cliff base, "
     f"and an alien centaur with a raised scythe tail blocking the cliff gap; "
     f"{HAWK} hovers above. {STYLE}", ["ax", "loc_cove"]),
    ("c8", "16:9",
     f"VFX morph shot at the cliff base: {LION} collapsing inward "
     f"mid-transformation into {RAT} — mane receding to grey fur, body already "
     f"rat-sized at the shoulders with the great paws still shrinking, a thin "
     f"naked tail whipping out — beside a narrow black crevice in the rock. "
     f"Uncanny practical-effects realism, no gore. {STYLE}", ["loc_cove"]),
    ("c9", "16:9",
     f"The two-hour wait at the cove, sun now high and hard: a silent unmoving "
     f"ring — grizzly, gorilla, wolf, {TIGER} — around a dead-end rock crevice, "
     f"and in the center the alien centaur stands guard over {RAT}, which "
     f"huddles pressed against the stone; the centaur's stalk eyes are both bent "
     f"down on it. {NOMOUTH} {STYLE}", ["ax", "loc_cove"]),
    ("c10", "16:9",
     f"A tiny barren rock island offshore, gulls overhead, surf breaking white. "
     f"{R} crouches on the bare wave-washed stone, setting {RAT} down gently "
     f"with both hands, her face wet — sea spray or tears; a small aluminum "
     f"rowboat bobs at the rock's edge behind her. {MATCH} {STYLE}",
     ["rachel", "loc_island"]),
    ("c12", "16:9",
     f"Dusk in the barn, low amber light through the plank gaps. Five teenagers "
     f"— {J}, {R}, {C}, {M} — and the alien centaur stand or sit far apart from "
     f"one another around the unlit lantern, none of them speaking, none quite "
     f"looking at each other; {HAWK} sits motionless on the rafter above. Heavy, "
     f"hollow quiet. {MATCH} {STYLE}",
     ["jake", "rachel", "cassie", "marco", "ax", "tobias", "loc_barn"]),
    ("c13", "16:9",
     f"High wide aerial at dusk: the tiny barren rock island alone in a flat "
     f"grey ocean, white surf ringing it, one minuscule grey speck of {RAT} at "
     f"its center, gulls wheeling below the camera, the dark coastline far away. "
     f"Desolate, final. {STYLE}", ["loc_island"]),
]
