"""Scene start-frame prompts for THE VAULTED SKY. Loaded by make_images.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from make_images import STYLE, MEWTWO, SUIT1, ARMOR, POD_ROOM, CLIFFTOP

MATCH = ("Characters exactly match the reference images in anatomy, face, "
         "coloring and wardrobe.")
STILLFACE = "The creature's face is smooth and still, with no visible mouth."

# (name, aspect, prompt, [anchor refs])
FRAMES = [
    # ---- Act 1: 2.351 (birth in the dark) ----
    ("a1", "16:9",
     "Extreme abstract close-up inside luminous amber fluid: drifting motes and "
     "tiny bubbles catching light, the curved inner face of thick glass, soft "
     "unfocused shapes of laboratory lights beyond like blurred stars, a faint "
     "green heartbeat-monitor glow pulsing at the edge of frame. Womb-like, "
     f"warm, dreamlike. {STYLE}", []),
    ("a2", "16:9",
     f"Wide shot of {POD_ROOM}. Inside the amber fluid floats a SMALL JUVENILE "
     f"version of {MEWTWO} — half-grown, thin, curled loosely with its tail "
     f"wrapped around itself, eyes closed, tubes trailing from its small arms "
     f"and spine. Tiny and alone at the center of the huge dark chamber. "
     f"{MATCH} {STILLFACE} {STYLE}", ["mewtwo_pod", "loc_pod_room"]),
    ("a3", "16:9",
     "A small warmly lit room with a gently curving outer wall: a woman of "
     "about 60 in a knitted cardigan sits in a worn armchair beside a lamp, "
     "reading aloud from a slim volume of poetry to the empty room, her "
     "expression tender and a little self-conscious; pinned to the wall behind "
     "her are pencil drawings of birds in flight. Cozy, strange, devotional. "
     f"{MATCH} {STYLE}", ["eva", "gyokusho"]),
    ("a4", "16:9",
     f"In the dim pod chamber, a 17-year-old girl with very long straight black "
     f"hair sits cross-legged on the floor a few feet from the huge glass "
     f"biopod, eyes closed in deep concentration, palms open on her knees; "
     f"inside the amber fluid the juvenile creature has drifted close to the "
     f"glass, watching her. A faint violet shimmer haloes the girl. {MATCH} "
     f"{STILLFACE} {STYLE}", ["sabrina_teen", "mewtwo_pod", "loc_pod_room"]),
    ("a5", "16:9",
     "An elderly scientist with unruly white hair and round glasses sits bolt "
     "upright at his desk in a dark office at night, lit only by his monitor, "
     "staring wide-eyed at nothing as if he has just heard a voice; on the "
     "side of his monitor is stuck a single yellow sticky note with "
     "handwritten text reading exactly: \"You are not alone.\" The note text "
     f"must be spelled exactly as given, in neat felt-tip handwriting. {MATCH} "
     f"{STYLE}", ["fuji"]),
    ("a6", "16:9",
     f"The biopod's upper cover has lifted; harsh white light floods down onto "
     f"the fluid. Lab technicians have wheeled a tall mirror up against the "
     f"pod glass. Inside, the young {MEWTWO} presses close to the glass, "
     f"staring at its own reflection, one three-fingered hand against the "
     f"inside of the pod. Around the chamber, staff look away uncomfortably. "
     f"{MATCH} {STILLFACE} {STYLE}", ["mewtwo_pod", "loc_pod_room"]),
    ("a7", "16:9",
     f"Two figures alone in the dark pod chamber: a powerfully built man in an "
     f"immaculate black suit stands with his hands clasped behind his back, "
     f"face inches from the biopod glass, his breath faintly fogging it; "
     f"inside the amber fluid the creature floats level with him, meeting his "
     f"eyes, one fist resting against the inside of the glass. Intimate and "
     f"menacing, lit only by the pod's amber glow. {MATCH} {STILLFACE} {STYLE}",
     ["giovanni", "mewtwo_pod", "loc_pod_room"]),

    # ---- Act 2: ten years of lies ----
    ("b1", "16:9",
     f"Wide shot of {POD_ROOM}, years later: the creature is now full-grown and "
     f"fills the pod, floating upright in the amber fluid; a ring of screens "
     f"has grown up around the pod showing paused films and pages of books, "
     f"and a keyboard floats on a swing-arm; game boxes and puzzle pieces are "
     f"stacked on tables nearby. Lived-in captivity. {MATCH} {STILLFACE} "
     f"{STYLE}", ["mewtwo_pod", "loc_pod_room"]),
    ("b2", "16:9",
     f"Extreme close-up through pod glass and amber fluid: the creature's large "
     f"luminous violet eyes, perfectly still, with pages of text and flickering "
     f"film images reflected across them and across the curved glass. Cold, "
     f"fast intelligence. {MATCH} {STILLFACE} {STYLE}", ["mewtwo_pod"]),
    ("b3", "16:9",
     f"In the pod chamber, the man in the black suit sits at a small table set "
     f"with a wooden Go board mid-game, speaking into a slim microphone "
     f"amplifier pointed at the pod; inside the amber fluid, dozens of black "
     f"and white Go stones float in two perfect orbiting rings around the "
     f"creature's body as it studies the board through the glass. {MATCH} "
     f"{STILLFACE} {STYLE}", ["giovanni", "mewtwo_pod", "loc_pod_room"]),
    ("b4", "16:9",
     f"The woman with long black hair, now in her late 20s, stands with her "
     f"palm flat against the biopod glass, looking up at the full-grown "
     f"creature inside; it has drifted down so its face is level with hers, "
     f"one three-fingered hand mirroring her palm from the inside. On the "
     f"heartbeat monitor beside them the green trace spikes sharply. {MATCH} "
     f"{STILLFACE} {STYLE}", ["sabrina", "mewtwo_pod", "loc_pod_room"]),

    # ---- Act 3: the suit and the sky ----
    ("c1", "16:9",
     f"The biopod stands DRAINED, its glass streaked with runnels of amber "
     f"fluid; inside on the wet floor the creature ({MEWTWO}) has collapsed to "
     f"its knees, hunched and shaking, tubes hanging loose from its arms, its "
     f"skin glistening wet and raw; technicians in dark clothing crowd the "
     f"opened pod with pieces of a bulky steel suit; the woman with long black "
     f"hair reaches toward it, alarmed. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_pod", "sabrina", "loc_pod_room"]),
    ("c2", "16:9",
     f"First time standing: the creature wearing {SUIT1} stands fully upright "
     f"beside its drained pod, arms slightly raised, tail stretched out behind "
     f"it, while a semicircle of staff steps back; in the foreground a black "
     f"umbreon-like fox pokemon with glowing yellow rings crouches low, "
     f"growling. Wonder and threat in one frame. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_suit1", "loc_pod_room"]),
    ("c3", "16:9",
     f"In a white laboratory corridor, the creature — now wearing {ARMOR} — "
     f"stands before an open door bowing slightly, tail lifted for balance, "
     f"to the woman of about 60 in a knitted cardigan who stands in her "
     f"doorway flushed and delighted, poetry book pressed to her chest; an "
     f"entourage of staff and the long-haired woman watch from along the "
     f"corridor. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_armor", "eva", "sabrina", "loc_lab_corridor"]),
    ("c4", "16:9",
     f"At the foot of a wide final staircase flooded from above with warm "
     f"daylight, the armored creature has frozen mid-step, one hand gripping "
     f"the rail; the woman with long black hair stands one step above, her "
     f"small five-fingered hand wrapped around its huge three-fingered one, "
     f"her face calm and patient. The light above them is blinding. {MATCH} "
     f"{STILLFACE} {STYLE}", ["mewtwo_armor", "sabrina", "loc_lab_corridor"]),
    ("c5", "16:9",
     f"THE KEY SHOT. Wide, from behind: on {CLIFFTOP}, the armored creature and "
     f"the woman with long black hair stand hand in hand in knee-deep wind-bent "
     f"grass at the cliff's edge, tiny beneath an immense brilliant blue sky "
     f"piled with white clouds, the sea blazing azure and emerald below. Her "
     f"hair streams in the wind. Overwhelming scale, rapture and terror. "
     f"{MATCH} {STYLE}", ["mewtwo_armor", "sabrina", "loc_clifftop"]),
    ("c6", "16:9",
     f"Dusk on the clifftop: the armored creature stands facing the darkening "
     f"sea, a small red warning light blinking on its chest plate; behind it "
     f"in a loose ring wait the man in the black suit, guards in dark "
     f"clothing, and several dark predator pokemon — a black fox with yellow "
     f"rings, a grey wolf, a white-furred horned creature. The creature's "
     f"fists are clenched. Nobody moves. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_armor", "giovanni", "loc_clifftop"]),

    # ---- Act 4: the machine ----
    ("d1", "16:9",
     f"A windowless laboratory conference room, harsh fluorescent light: eight "
     f"exhausted scientists in lab coats around a long table strewn with "
     f"papers, mugs and a thick paper logbook, mid-argument — one gesturing at "
     f"a whiteboard dense with project schedules, others slumped, pinching "
     f"the bridge of the nose. Overwork made visible. {MATCH} {STYLE}",
     ["dr_light", "collins", "loc_conference"]),
    ("d2", "16:9",
     f"The conference room door stands open and the man in the immaculate "
     f"black suit has just stepped through it; every scientist at the table "
     f"has frozen mid-word and turned; he regards them pleasantly, one hand "
     f"just inside his suit jacket. The grey-haired woman at the table's head "
     f"has gone very still. {MATCH} {STYLE}",
     ["giovanni", "dr_light", "collins", "loc_conference"]),
    ("d3", "16:9",
     f"Chaos in the conference room: scientists diving away from the table, "
     f"chairs toppling; the man with thinning sandy hair and wire glasses is "
     f"caught mid-flight toward the far corner, dissolving from the waist up "
     f"into streaming red-white light that is being drawn backward into a "
     f"small blue-and-red capsule ball bouncing on the floor behind him; the "
     f"man in the black suit watches, calm, arm still extended from the "
     f"throw. {MATCH} {STYLE}",
     ["giovanni", "collins", "dr_light", "loc_conference"]),
    ("d4", "16:9",
     f"The conference room, seconds after: the door just closed, toppled "
     f"chairs, papers settling; the scientists still pressed against the "
     f"walls; at the head of the table the grey-haired woman stands with one "
     f"hand raised, face carefully blank — and around the room every other "
     f"scientist's hand is rising too. Terror formalized as a vote. {MATCH} "
     f"{STYLE}", ["dr_light", "loc_conference"]),
    ("d5", "16:9",
     f"A small windowless execution room: a young prisoner in plain grey "
     f"clothes strapped to a chair at a bare metal table; across from her, "
     f"the man in the black suit sits leaning slightly forward, having just "
     f"placed a capped syringe of clear fluid neatly on the table between "
     f"them; a single hard light overhead. Quiet, procedural menace. {MATCH} "
     f"{STYLE}", ["giovanni"]),
    ("d6", "16:9",
     f"A vast perfectly bare white room with no visible corners: at its "
     f"center the man in the black suit sits on a plain chair facing a "
     f"HOLOGRAM of the pod chamber — the glass biopod, the amber fluid and "
     f"the creature inside rendered in faintly translucent, glitch-edged "
     f"light, the simulation dissolving into white static at its edges; his "
     f"finger rests on a small button on the chair's arm. {MATCH} {STILLFACE} "
     f"{STYLE}", ["giovanni", "mewtwo_pod"]),

    # ---- Act 5: children of the mind ----
    ("e1", "16:9",
     f"Autumn morning on {CLIFFTOP}, the grass gone tawny, breath-mist in the "
     f"air: the armored creature walks between the woman with long black hair "
     f"and a bright-eyed engineer in a utility vest, the three of them "
     f"strolling like old friends, the volcanic peak hazy inland behind them. "
     f"{MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_armor", "sabrina", "ayush", "loc_clifftop"]),
    ("e2", "16:9",
     f"On the autumn clifftop the woman with long black hair is LAUGHING, her "
     f"hair and coat lifting weightlessly around her, her shoes a hand-span "
     f"off the grass, faint shimmering light scintillating over her; beside "
     f"her the armored creature hovers the same small height off the ground, "
     f"arms spread slightly; the engineer stares open-mouthed. Pure shared "
     f"joy. {MATCH} {STILLFACE} {STYLE}",
     ["sabrina", "mewtwo_armor", "ayush", "loc_clifftop"]),
    ("e3", "16:9",
     f"KEY DECEPTION SHOT, low angle at grass level, golden sunset: the "
     f"armored creature appears to stroll across the clifftop meadow beside "
     f"the engineer — but seen from this low angle its feet GLIDE a few "
     f"centimeters above the grass blades, while behind it a line of crisp "
     f"footprints presses itself into the turf, one new print flattening "
     f"grass where no foot touches. The engineer, looking ahead, notices "
     f"nothing. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_armor", "ayush", "loc_clifftop"]),
    ("e4", "16:9",
     f"Night in the pod chamber, all screens dark: the creature floats in the "
     f"amber fluid with its eyes closed, utterly still — but the fluid around "
     f"its head is disturbed by faint slow ripples, and multiple dim "
     f"reflections of its own face look back from the curved glass at "
     f"slightly different angles, each with a subtly different expression. "
     f"Uncanny, interior. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_pod", "loc_pod_room"]),
    ("e5", "16:9",
     f"Storm on the clifftop: rain hammering, the sea grey and violent below; "
     f"the armored creature and the woman with long black hair stand at the "
     f"cliff edge both soaked through, her hair plastered to her face, and "
     f"she is smiling up at it with complete unguarded trust. {MATCH} "
     f"{STILLFACE} {STYLE}", ["mewtwo_armor", "sabrina", "loc_clifftop"]),
    ("e6", "16:9",
     f"The white training hall: the armored creature stands at one end with "
     f"one arm theatrically extended; at the far end a life-size stuffed "
     f"kangaroo-like grey pokemon doll slams into the padded wall hard enough "
     f"to dent it, debris and dust bursting outward; behind the high "
     f"observation window, silhouettes surge to their feet. {MATCH} "
     f"{STILLFACE} {STYLE}",
     ["mewtwo_armor", "giovanni", "sabrina", "loc_training"]),
    ("e7", "16:9",
     f"The white training hall: a small purple rat pokemon with large teeth "
     f"hangs by its bite from the armored creature's exposed calf below the "
     f"armor plate, a thin line of blood on the white skin; the creature is "
     f"bent over it, arms flailing wide, its composure shattered for the "
     f"first time; behind the observation glass the man in the black suit "
     f"leans forward with clinical interest. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_armor", "giovanni", "loc_training"]),
    ("e8", "16:9",
     f"Extreme close-up in darkness: the sleeping creature's face inside the "
     f"amber fluid — and reflected small and warped in the curve of its "
     f"closed eyelid and the pod glass, a fifth pale copy of its own face "
     f"that seems to be looking directly at the camera. Cold birth of "
     f"something new. {MATCH} {STILLFACE} {STYLE}", ["mewtwo_pod"]),

    # ---- Act 6: the window opens ----
    ("f1", "16:9",
     f"The laboratory conference room rocked by an earthquake: monitors on "
     f"the wall showing news footage of a colossal red-armored titan wading "
     f"through a boiling sea, while the room itself shakes — dust falling "
     f"from the ceiling, mugs sliding off the table, scientists grabbing the "
     f"walls, the lights flickering to red emergency lamps. {MATCH} {STYLE}",
     ["loc_conference"]),
    ("f2", "16:9",
     f"A red-lit laboratory corridor half-blocked by a collapsed concrete "
     f"stairwell: the young man with messy dark hair, sketchbook still under "
     f"one arm, speaks urgently and shyly to the grey-haired director, who "
     f"answers him with a smooth unreadable face; behind them staff hurry "
     f"past carrying equipment. {MATCH} {STYLE}",
     ["gyokusho", "dr_light", "loc_lab_corridor"]),
    ("f3", "16:9",
     f"Two figures in private conference in a red-lit alcove: the hard-faced "
     f"security chief in dark tactical clothing, arms crossed, and the "
     f"grey-haired director gripping her clipboard; both faces grim, heads "
     f"bent close, clearly deciding something terrible. {MATCH} {STYLE}",
     ["shaw", "dr_light", "loc_lab_corridor"]),
    ("f4", "16:9",
     f"The pod chamber under red emergency light, a long crack running across "
     f"the ceiling above the biopod, dust drifting down through the amber "
     f"glow: the grey-haired director stands alone before the glass, looking "
     f"up; inside, the full-grown creature looks calmly down at her, mild and "
     f"unafraid, the heartbeat monitor steady beside them. {MATCH} "
     f"{STILLFACE} {STYLE}", ["dr_light", "mewtwo_pod", "loc_pod_room"]),
    ("f5", "16:9",
     f"Pouring rain on the plateau before the mansion at dusk: the armored "
     f"creature rises out of a broken opening in the ground amid rubble, "
     f"rain sheeting off its dark plates and visor, helmet tilted up to the "
     f"sky; around it a crowd of drenched evacuated staff has frozen "
     f"mid-applause, hands still half-raised, faces going uncertain. {MATCH} "
     f"{STILLFACE} {STYLE}", ["mewtwo_armor", "loc_clifftop"]),
    ("f6", "16:9",
     f"Thin rain at dusk on the clifftop: the armored creature strolls beside "
     f"the grey-haired director in easy conversation, its tail swaying near "
     f"her; exactly eight meters behind them walks the security chief, and "
     f"at his heel a sleek black weasel pokemon with a red feather crest and "
     f"a gold gem on its forehead, both watching the creature without "
     f"blinking. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_armor", "dr_light", "shaw", "loc_clifftop"]),
    ("f7", "16:9",
     f"The security chief stands square in front of the armored creature in "
     f"the thinning rain, jaw set, speaking hard truth up into its visor; "
     f"the creature has gone very still, head fractionally tilted, rain "
     f"dripping from its chin; the director watches them both. {MATCH} "
     f"{STILLFACE} {STYLE}",
     ["shaw", "mewtwo_armor", "dr_light", "loc_clifftop"]),
    ("f8", "16:9",
     f"Sunset breaking under the storm clouds, everything gold: the young "
     f"man with messy dark hair jogs up the wet grass toward the group, "
     f"beaming, waving good news; in the foreground the armored creature's "
     f"visor catches and reflects the sunset in a blade of orange light, "
     f"its face unreadable behind it. {MATCH} {STILLFACE} {STYLE}",
     ["gyokusho", "mewtwo_armor", "dr_light", "loc_clifftop"]),

    # ---- Act 7: the escape ----
    ("g1", "16:9",
     f"FROZEN INSTANT, wide: the armored creature has snapped airborne two "
     f"meters off the clifftop grass, its long tail wrapped tight around the "
     f"waist of the grey-haired director whose feet are torn from the "
     f"ground, papers flying; the black weasel pokemon is caught mid-leap "
     f"beneath them; guards spin, mouths open mid-shout; the sunset sea "
     f"waits beyond the cliff edge. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_armor", "dr_light", "shaw", "loc_clifftop"]),
    ("g2", "16:9",
     f"Vertical plunge down a sheer sea-cliff face at dusk, camera falling "
     f"with it: the armored creature dives headfirst, arms pinned back, body "
     f"convulsed with pain, the rocks and white surf rushing up; far above, "
     f"tiny dark winged shapes launch off the clifftop after it. {MATCH} "
     f"{STILLFACE} {STYLE}", ["mewtwo_armor", "loc_ocean_dusk"]),
    ("g3", "16:9",
     f"Low over heavy sea at dusk: the armored creature skips off a wavetop "
     f"like a hurled stone, a burst of spray behind it, body flat to the "
     f"water; behind and above, a flight of dark pokemon dives in pursuit — "
     f"a huge black crow with a white-plumed chest, a vulture with a bone "
     f"collar, and a three-headed black dragon spewing violet-black energy "
     f"that detonates the sea where the creature just was. {MATCH} "
     f"{STILLFACE} {STYLE}", ["mewtwo_armor", "loc_ocean_dusk"]),
    ("g4", "16:9",
     f"Underwater, deep blue-black, shafts of last light from the surface: "
     f"the armored creature swims hard toward a narrow crevice in the rock "
     f"wall of the island's underwater base, trailing a thin ribbon of "
     f"bubbles; behind it four sleek dark shapes knife through the water in "
     f"pursuit, while a swarm of frenzied jellyfish-like and serpent-like "
     f"sea pokemon boils up between them, eyes glowing. {MATCH} {STILLFACE} "
     f"{STYLE}", ["mewtwo_armor"]),
    ("g5", "16:9",
     f"The pitch-black sea cave: the armored creature lies on the crescent "
     f"of wet sand where it has just woken, propped on one elbow, its "
     f"helmet off beside it, a single red suit-light blinking; its "
     f"three-fingered hand is raised before its face, wet sand trickling "
     f"between its fingers as it watches, transfixed. {MATCH} {STILLFACE} "
     f"{STYLE}", ["mewtwo_armor", "loc_cave"]),
    ("g6", "16:9",
     f"In the black cave the creature sits upright on the sand in the last "
     f"of its armor, eyes open, rigid with fury; the still black pool "
     f"beside it reflects its face back WRONG — the reflection's posture "
     f"subtly different, colder, its head tilted at an angle the creature's "
     f"is not. Confrontation with itself. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_armor", "loc_cave"]),
    ("g7", "16:9",
     f"The empty armor suit sits propped upright on the cave sand like a "
     f"shed skin, its chest light glowing as it plays a recording, faint "
     f"sound-ripples visible in the pool beside it; across the cave the "
     f"creature — bare now, out of the suit ({MEWTWO}) — crouches on the "
     f"sand in the darkness, listening absolutely motionless, starlight "
     f"from the crevice mouth edging its silhouette. {MATCH} {STILLFACE} "
     f"{STYLE}", ["mewtwo_free", "mewtwo_armor", "loc_cave"]),

    # ---- Act 8: the vaulted sky ----
    ("h1", "16:9",
     f"TITLE IMAGE. The creature — bare, no suit — flies on its back low "
     f"over a black calm ocean under a moonless sky, arms loose at its "
     f"sides, face to the stars: the Milky Way blazes edge to edge and the "
     f"sea mirrors it, so it seems to drift between two skies. Beside its "
     f"face, three tiny teardrops float weightless, glinting starlight. "
     f"{MATCH} {STILLFACE} {STYLE}", ["mewtwo_free", "loc_nightsky"]),
    ("h2", "16:9",
     f"Bright dawn sea: the creature swims loose and clumsy and happy at "
     f"the surface among a pod of round blue-and-cream whale pokemon the "
     f"size of cars, one of them surfacing to regard it with a tiny "
     f"curious eye, spray golden in the low sun. {MATCH} {STILLFACE} "
     f"{STYLE}", ["mewtwo_free"]),
    ("h3", "16:9",
     f"VIOLENT INSTANT at sea, dawn light gone cold: a column of ocean ten "
     f"meters tall erupts upward, and at its crown the creature hangs "
     f"twisting in the air, water streaming off it, a dark bloom of red "
     f"spreading in the churned sea below where a huge shadowed shape "
     f"turns away under the surface; the creature's long tail is visibly "
     f"SHORTENED, ending mid-length. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_free", "loc_ocean_dusk"]),
    ("h4", "16:9",
     f"Night beach, wide and quiet: a low mound of dark sand at the tide "
     f"line, and emerging from it only the pale snout and closed eyes of "
     f"the buried creature, at rest at last; above, the same endless "
     f"moonless starfield burns over the black sea. Peace like a wound "
     f"closing. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_free", "loc_nightsky"]),
    ("h5", "16:9",
     f"Deep forest clearing at night: hundreds of small floating "
     f"one-eyed glyph-like creatures, each shaped like a different "
     f"letterform, turn slowly in vast layered concentric rings like an "
     f"intricate clock built of living aurora, casting shifting green-blue "
     f"light; before it, tiny at the base of frame, the pale creature "
     f"hovers, dwarfed, transfixed. {MATCH} {STILLFACE} {STYLE}",
     ["mewtwo_free"]),
    ("title", "16:9",
     f"Movie title card: over a moonless night sky blazing with the Milky "
     f"Way above a black mirror-calm ocean, elegant thin pale letters "
     f"float, reading exactly: \"THE VAULTED SKY\". The title text must be "
     f"spelled exactly as given, in refined understated serif typography, "
     f"faintly luminous. {STYLE}", ["loc_nightsky"]),
]
