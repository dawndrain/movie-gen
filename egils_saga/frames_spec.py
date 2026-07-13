"""Start frames for EGIL — one per shot. (name, aspect, prompt, [refs])
Refs resolve against anchors/. Loaded by make_images.py stage `frames`."""

STYLE = (
    "Photorealistic cinematic film still from a live-action historical "
    "Viking-age epic feature film, IMAX 35mm, natural volumetric light, "
    "moody overcast Nordic color grade, rich texture of wool, iron, timber "
    "and turf. Historically grounded 9th-10th century Norse costume and "
    "props. No text, no watermark, no captions, no cartoon styling, no "
    "horned helmets. ONE single continuous photograph filling the whole "
    "frame, no borders, no collage. Characters keep exactly the same faces "
    "and clothes as the reference images."
)

from make_images import W  # wardrobe locks

FRAMES = [
    # ---------- PROLOGUE ----------
    ("p1", "16:9",
     f"Dusk outside a Norwegian chieftain's longhouse. {W['kveldulf']} "
     f"stands motionless in the yard as his household — a few farm-workers "
     f"in plain wool — edge away toward the lit doorway behind him. His "
     f"face is empty, wolf-still, eyes on the darkening treeline. "
     f"Firelight spills from the door; the last red light dies on the "
     f"fjord. {STYLE}", ["kveldulf", "loc_kveldulf_hall"]),
    ("p2", "16:9",
     f"Interior of a firelit Norse hall. {W['kveldulf']} sits in a carved "
     f"high seat, leaning forward, mid-speech, one big hand raised in calm "
     f"refusal. Before him stand two royal messengers in travel-stained "
     f"cloaks, uneasy. Long fire-pit light. {STYLE}",
     ["kveldulf", "loc_kveldulf_hall"]),
    ("p3", "16:9",
     f"Firelit Norse hall at night. {W['kveldulf']} and {W['thorolf_k']} "
     f"stand face to face beside the long fire — the old man grave and "
     f"warning, the young man bright and resolved. {STYLE}",
     ["kveldulf", "thorolf_k", "loc_kveldulf_hall"]),
    ("p4", "16:9",
     f"A vast Norse feast inside a converted granary: shields hung in an "
     f"unbroken row around the walls, benches packed with hundreds of "
     f"warriors drinking. At the far high seat sits {W['harald']}, "
     f"scanning the crowded benches, his face flushing dark red, saying "
     f"nothing. {STYLE}", ["harald"]),
    ("p5", "16:9",
     f"A dim candlelit corner of a modest Norse hall. A small shrewd "
     f"sharp-faced man in a plain brown tunic leans close to the ear of "
     f"{W['harald']}, whispering, hand half-raised. The king stares ahead, "
     f"listening, quiet and believing. Deep shadow. {STYLE}", ["harald"]),
    ("p6", "16:9",
     f"Night. A great northern hall burns — flames climbing the birch-bark "
     f"roof, torch-bearing warriors ringing the yard. The timber side-wall "
     f"has burst outward in a shower of sparks, and through the gap "
     f"strides {W['thorolf_k']}, sword up, lit by fire, cutting toward a "
     f"raised royal standard. {STYLE}", ["thorolf_k", "loc_sandness"]),
    ("p7", "16:9",
     f"Firelit hall. {W['kveldulf']} sits slumped in his high seat, "
     f"suddenly ancient, grief-hollowed, staring into the fire. {STYLE}",
     ["kveldulf", "loc_kveldulf_hall"]),
    ("p8", "16:9",
     f"Open grey ocean from the deck of a Viking longship under a "
     f"blue-and-red striped sail. A plain wooden coffin slides over the "
     f"rail into the ship's wake. At the rail stands {W['skallagrim']}, "
     f"watching it go, face like stone. Crewmen bow their heads behind "
     f"him. {STYLE}", ["skallagrim", "loc_longship"]),
    ("p9", "16:9",
     f"An Icelandic creek at dawn: black sand, kelp, mist. A plain wooden "
     f"coffin lies cast up at the waterline. {W['skallagrim']} stands over "
     f"it, then lifts his eyes to a rocky hill above the bay. {STYLE}",
     ["skallagrim", "loc_borg"]),
    # ---------- ACT 1 ----------
    ("a1", "16:9",
     f"Night on an Icelandic moor under a huge dim sky. A heavy "
     f"draught-horse walks the trackless heath, and on its broad back "
     f"rides {W['egil_child']}, tiny and grim, gripping the mane, utterly "
     f"unafraid. Distant firelight on the horizon. {STYLE}",
     ["egil_child", "loc_borg"]),
    ("a2", "16:9",
     f"A firelit Icelandic feast hall, benches of laughing farmers with "
     f"ale-horns. Standing on a bench, mid-declamation with one small arm "
     f"flung out, is {W['egil_child']} — performing a poem. At the head of "
     f"the table a kindly old man in a fine wool tunic laughs with "
     f"delight. {STYLE}", ["egil_child", "loc_borg_hall"]),
    ("a3", "16:9",
     f"Inside a turf hall by the long fire. A Norse mother in a blue "
     f"apron-dress braids wool and looks down with a proud half-smile at "
     f"{W['egil_child']}, who sits beside her with skinned knuckles and a "
     f"bloodied chin, staring ahead, jaw set. {STYLE}",
     ["egil_child", "loc_borg_hall"]),
    ("a4", "16:9",
     f"A winter ball-game field by a firth at sunset, snow patches on "
     f"frozen grass, a crowd of players. In the foreground {W['skallagrim']} "
     f"has seized a twelve-year-old version of {W['egil_child']} by the "
     f"shoulder — the man's face is wrong, swollen with unnatural rage in "
     f"the dying light — while {W['brak']} rushes between them, shouting. "
     f"{STYLE}", ["skallagrim", "egil_child", "brak"]),
    ("a5", "16:9",
     f"A silent turf-hall supper, the long fire low. On one side of the "
     f"fire sits {W['skallagrim']}, on the other a twelve-year-old version "
     f"of {W['egil_child']} — father and son staring at each other down "
     f"the length of the hall over an empty place at the bench. The "
     f"household eats with eyes down. {STYLE}",
     ["skallagrim", "egil_child", "loc_borg_hall"]),
    # ---------- ACT 2 ----------
    ("b1", "16:9",
     f"A torchlit Norse banquet on an island farm, boards crowded with "
     f"horns and meat. In the foreground {W['egil']} drains a great "
     f"ox-horn. Behind a carved pillar, half in shadow, {W['gunnhild']} "
     f"and {W['bard']} bend together over a single drinking horn, her "
     f"hand poised above it. {STYLE}",
     ["egil", "gunnhild", "bard", "loc_borg_hall"]),
    ("b2", "16:9",
     f"Close shot, torchlight. The huge scarred hands of {W['egil']} hold "
     f"a drinking horn; he has scratched angular runes into its side and "
     f"the runes are darkened with red from a cut on his palm. His grim "
     f"face watches the horn, one eyebrow down, one raised. {STYLE}",
     ["egil"]),
    ("b3", "16:9",
     f"A dark hall doorway at night, one guttering torch. {W['bard']} "
     f"offers a farewell cup to {W['egil']}, whose other hand is already "
     f"on his sword-hilt in the shadow of his cloak; beyond the door, "
     f"pitch-black night. Menace. {STYLE}", ["egil", "bard"]),
    ("b4", "16:9",
     f"Grey dawn on cold open water. {W['egil']} swims a wide strait with "
     f"powerful strokes, his weapons and cloak bundled in a tight roll "
     f"lashed on his back, an island low behind him, mist ahead. {STYLE}",
     ["egil"]),
    ("b5", "16:9",
     f"A torchlit royal hall. {W['gunnhild']} stands beside the high seat "
     f"of {W['eirik']}, bent toward him, speaking with cold intensity, "
     f"one hand on the armrest of his seat. The king's knuckles are white "
     f"on his axe-haft, his terrifying eyes fixed on the middle distance. "
     f"{STYLE}", ["eirik", "gunnhild", "loc_york"]),
    # ---------- ACT 3 ----------
    ("c1", "16:9",
     f"Wide shot of a level heath between a river and a dark wood: a long "
     f"wall of tall pale war-tents, hazel poles in lines, small figures "
     f"of soldiers making the camp look vast, overcast English light. "
     f"{STYLE}", ["loc_vinheath"]),
    ("c2", "16:9",
     f"Dawn war-camp on the heath. {W['egil']} and {W['thorolf_s']} stand "
     f"between the tents in the cold half-light — Egil scowling in "
     f"protest, hand clamped on his brother's forearm; Thorolf calm, "
     f"already armed with shield and halberd. {STYLE}",
     ["egil", "thorolf_s", "loc_vinheath"]),
    ("c3", "16:9",
     f"The edge of a dark wood on the heath. {W['thorolf_s']} presses "
     f"forward along the treeline ahead of his shield-wall, shield slung "
     f"on his back, the great halberd two-handed — while armed Scots "
     f"warriors with levelled spears burst from the trees at his flank. "
     f"Battle chaos, banners, overcast light. {STYLE}",
     ["thorolf_s", "loc_vinheath"]),
    ("c4", "16:9",
     f"Mid-battle on the heath. {W['egil']} RUNS through the gap between "
     f"two armies, sword out, mouth open in a roar, cloak flying — "
     f"shield-walls blurring on either side, a falling banner ahead of "
     f"him. {STYLE}", ["egil", "loc_vinheath"]),
    ("c5", "16:9",
     f"A fresh earthen grave-mound on the quiet heath after battle. "
     f"{W['egil']} kneels, clasping a broad gold bracelet onto the wrist "
     f"of his dead brother {W['thorolf_s']}, who lies composed with his "
     f"weapons on a cloak. Grey evening light. {STYLE}",
     ["egil", "thorolf_s", "loc_vinheath"]),
    ("c6", "16:9",
     f"An Anglo-Saxon royal hall: a LONG OPEN FIRE burns in a trench down "
     f"the middle of the floor between two facing high seats. On one side "
     f"sits {W['athelstan']}, calm, holding his drawn sword upright with "
     f"a great gold arm-ring hung on its point, reaching it out ACROSS "
     f"the flames. Opposite, fully armed with helmet on and shield at his "
     f"feet, {W['egil']} rises with his own sword extended point-first to "
     f"receive the ring, one eyebrow drawn down, the other raised high. "
     f"Courtiers watch frozen. {STYLE}",
     ["egil", "athelstan", "loc_athelstan_hall"]),
    # ---------- ACT 4 ----------
    ("d1", "16:9",
     f"An open-air Norse law assembly: hazel poles in a wide ring joined "
     f"by twisted ropes, judges on benches within. Armed men wade into "
     f"the ring CUTTING the sacred ropes; judges scatter; and in the "
     f"foreground {W['egil']} shouts over the chaos, arm flung out in "
     f"formal curse, while onlookers recoil. {STYLE}",
     ["egil", "loc_gulathing"]),
    ("d2", "16:9",
     f"A bare rocky headland at dusk over a leaden sea. {W['egil']} "
     f"plants a tall hazel pole into a rift of the summit rock — a "
     f"bleached horse's skull is set on top of the pole, facing the dark "
     f"mainland mountains across the water. Wind whips his cloak; storm "
     f"light. {STYLE}", ["egil", "loc_nithing_rock"]),
    ("d3", "16:9",
     f"Storm surf on an English shore: a broken Viking ship heeled over "
     f"in white breakers, cargo strewn, rain driving. {W['egil']} wades "
     f"out of the sea toward the camera, drenched, huge, alive. {STYLE}",
     ["egil"]),
    ("d4", "16:9",
     f"A torchlit doorway in a night street of Norse-age York. "
     f"{W['arinbjorn']} holds the door open, torch raised, his calm face "
     f"gone grave — before him stands {W['egil']}, hooded, rain-soaked, "
     f"filling the doorframe like a giant. {STYLE}",
     ["egil", "arinbjorn", "loc_york"]),
    ("d5", "16:9",
     f"A torchlit Northumbrian throne hall bristling with armed men. "
     f"{W['egil']} kneels before the dais and clasps the foot of "
     f"{W['eirik']}, who stares down with terrifying eyes. Beside the "
     f"throne {W['gunnhild']} points at the kneeling man, ferocious; "
     f"{W['arinbjorn']} stands at Egil's shoulder, speaking for him. "
     f"{STYLE}", ["egil", "eirik", "gunnhild", "arinbjorn", "loc_york"]),
    ("d6", "16:9",
     f"A small dark upper room under a roof, one small window, night. "
     f"{W['egil']} sits with a furrowed brow, mouthing verse — at the "
     f"window sill, inches from his face, perches a swallow, wings half "
     f"open, uncanny in the gloom. Moonlight. {STYLE}", ["egil"]),
    ("d7", "16:9",
     f"Morning in the packed throne hall at York. {W['egil']} stands "
     f"alone at the centre of the floor, head up, arms loose, "
     f"declaiming — the crowd of armed courtiers utterly silent. On the "
     f"dais {W['eirik']} sits bolt upright, staring at him. {W['gunnhild']} "
     f"beside the throne, arms folded, furious. {STYLE}",
     ["egil", "eirik", "gunnhild", "loc_york"]),
    ("d8", "16:9",
     f"The throne hall, moments after. {W['eirik']} stands before his "
     f"throne, hand raised in cold dismissal, face unreadable. Before him "
     f"{W['egil']} inclines his head once — ugly, unbroken, faintly "
     f"amused. {W['arinbjorn']} exhales beside him. {STYLE}",
     ["egil", "eirik", "arinbjorn", "loc_york"]),
    # ---------- ACT 5 ----------
    ("e1", "16:9",
     f"A squall on a wide Icelandic firth at dusk: black water, driving "
     f"spray, whitecaps — a single small eight-oared open boat far out, "
     f"swamped and heeling, vanishing among the waves. No faces visible. "
     f"{STYLE}", ["loc_borg"]),
    ("e2", "16:9",
     f"Evening shore below a grassy burial mound. {W['egil']}, grey-haired "
     f"now, carries the body of a fair-haired youth wrapped in a cloak up "
     f"the slope of the mound — the seams of the big man's kirtle have "
     f"SPLIT open across his swollen shoulders and arms from the strain. "
     f"His face is a mask. {STYLE}", ["egil", "loc_mound"]),
    ("e3", "16:9",
     f"Inside the dark turf hall: the small carved door of the wooden "
     f"bed-closet is shut fast. A dignified older Norse woman in a fine "
     f"apron-dress stands before the locked panel, one hand flat on the "
     f"wood, head bowed. The hall behind her is hushed. {STYLE}",
     ["loc_borg_hall"]),
    ("e4", "16:9",
     f"Inside the cramped dark bed-closet, a sliver of firelight through "
     f"the open door. {W['egil']}, grey and hollowed, half-lies against "
     f"the wall holding a drinking horn he has just bitten a piece out "
     f"of; beside him sits {W['thorgerd']}, close, calm, watching him "
     f"with his own stubborn eyes. {STYLE}", ["egil", "thorgerd"]),
    ("e5", "16:9",
     f"The bed-closet, door now wide to the firelight. {W['egil']} sits "
     f"upright, eyes alight in the ruin of his face, one hand moving as "
     f"the verse comes; {W['thorgerd']} leans at his shoulder, fierce "
     f"with relief, memorizing the lines. {STYLE}", ["egil", "thorgerd"]),
    ("e6", "16:9",
     f"The turf hall, the household gathered in firelight. {W['egil']} "
     f"stands at the high seat, restored, delivering the end of a poem "
     f"with terrible quiet authority; {W['thorgerd']} watches from the "
     f"bench, chin high. {STYLE}", ["egil", "thorgerd", "loc_borg_hall"]),
    ("e7", "16:9",
     f"A turf-hall hearth. {W['egil_old']} gropes along the wall toward "
     f"the fire with his staff; two young serving-women by the hearth "
     f"laugh behind their hands; a stout cook waves him away from the "
     f"flames. Firelight and pity. {STYLE}", ["egil_old", "loc_borg_hall"]),
    ("e8", "16:9",
     f"Two figures by a low fire, conspirators: {W['egil_old']} leans "
     f"forward on his staff, blind eyes bright with mischief, mid-scheme; "
     f"beside him a handsome middle-aged Norse woman in a fine "
     f"apron-dress laughs, delighted. {STYLE}", ["egil_old", "loc_borg_hall"]),
    ("e9", "16:9",
     f"Icelandic moorland in grey dawn mist — steaming hot-spring holes "
     f"and black bogs. {W['egil_old']} stands alone in the half-light, "
     f"holding the halter of a weary horse, two empty pack-lashings "
     f"hanging loose from the saddle. No chests. No companions. His blind "
     f"face gives nothing. {STYLE}", ["egil_old", "loc_moor_bog"]),
    ("e10", "16:9",
     f"A small early-Christian Icelandic churchyard, generations later: "
     f"turf church, wooden cross, men in simple dark medieval robes. A "
     f"priest holds up to the light an unearthed HUMAN SKULL — an "
     f"anatomically normal human cranium with eye sockets and jaw, but "
     f"unusually massive and heavy-boned, its bone surface subtly rippled "
     f"with fine wave-like ridges — a hand-axe in his other hand. The "
     f"onlookers stare. {STYLE}", []),
]
