#!/usr/bin/env python3
"""DUNGEON CRAWLER CARL (book one) animatic — single source of truth.

Everything the other scripts consume lives here: wardrobe locks, anchors,
start frames, dialogue, cut order, Ken Burns locks, music/ambience marks,
and the voice cast. All dialogue is original paraphrase for this animatic.
"""

# ---------------------------------------------------------------- style ----

STYLE = (
    "Photorealistic cinematic film still from a live-action dark-comedy "
    "fantasy series. 35mm anamorphic, dramatic torchlit shadows, rich "
    "saturated color grade, crisp detail. ONE single continuous photograph "
    "filling the whole frame, no borders, no collage, no watermark, no "
    "captions, no cartoon styling."
)
SOLO = "This is the ONLY figure in the frame; the background contains no other people."
CAT = ("a real living animal, photorealistic fur and anatomy, absolutely NOT "
       "a cartoon, NOT a plush toy")

# ------------------------------------------------------- wardrobe locks ----

CARL_FACE = ("a tall powerfully-built clean-shaven man of 27 with short brown "
             "hair and a tired deadpan expression")
W = {
    # Carl by era — pink Crocs a1-a3, barefoot forever after, cloak+shirt from
    # a7, war gauntlet from b4, glitter feet from c2
    "carl_crocs": (CARL_FACE + ", wearing a worn brown leather jacket over a "
                   "bare chest, red heart-print boxer shorts, bare muscular "
                   "legs, and bright pink rubber clog sandals"),
    "carl":       (CARL_FACE + ", wearing a worn brown leather jacket over a "
                   "bare chest, red heart-print boxer shorts, bare muscular "
                   "legs, completely BAREFOOT"),
    "carl_cloak": (CARL_FACE + ", wearing a wispy black shadow-cloak clasped "
                   "over a worn brown leather jacket, a snug grey-green "
                   "reptile-leather shirt, red heart-print boxer shorts, bare "
                   "muscular legs, completely BAREFOOT"),
    "carl_full":  (CARL_FACE + ", wearing a wispy black shadow-cloak clasped "
                   "over a worn brown leather jacket, a snug grey-green "
                   "reptile-leather shirt, red heart-print boxer shorts, a "
                   "heavy bronzed war gauntlet covering his right hand and "
                   "forearm, bare muscular legs, completely BAREFOOT"),
    "donut":      ("a fluffy tortoiseshell Persian show cat with long black, "
                   "cream and white fur, a flat aristocratic smushed face and "
                   "huge amber-yellow eyes, " + CAT),
    "donut_c":    ("a fluffy tortoiseshell Persian show cat with long black, "
                   "cream and white fur, a flat aristocratic smushed face and "
                   "huge amber-yellow eyes, wearing a delicate golden tiara "
                   "set with dark smoky gems around one glowing purple stone, "
                   + CAT),
    "mordecai_rat": ("a short shabby four-foot rat-man with grey whiskered "
                     "fur, a scruffy beard and tired knowing eyes, wearing a "
                     "black vest, blue trousers and worn sandals"),
    "mordecai_bug": ("a bear-sized shaggy brown creature with enormous round "
                     "amber owl eyes, long thin gangly arms and skinny "
                     "backward-bent legs, oddly endearing"),
    "brandon":    ("a cheerful stocky Black man in his 30s in a grey "
                   "maintenance work uniform and tool belt, carrying a "
                   "comically oversized glittering enchanted sledgehammer"),
    "elle":       ("a wiry sharp-eyed woman in her late 70s with cropped "
                   "white hair, wearing a quilted housecoat over practical "
                   "clothes and sturdy sneakers, chin out, unimpressed"),
    "agatha":     ("a hunched old woman wrapped head to toe in layered "
                   "scarves, a red-checkered trapper hat askew, dark rheumy "
                   "eyes, pushing a rusty shopping cart piled with blankets, "
                   "spray-paint cans and a plastic pink flamingo with a toy "
                   "arrow through its head"),
    "zev":        ("a two-foot-tall fish-person alien in a crisp white mesh "
                   "spacesuit, her goldfish-like face floating inside a "
                   "water-filled glass bulb helmet"),
    "odette":     ("an alien talk-show host with a glossy black praying-"
                   "mantis-style helmet with huge mirrored compound eyes and "
                   "six-foot antennae, a glamorous sequined torso, and the "
                   "lower body of a bear-sized king crab"),
    "maestro":    ("a hulking young orc prince, six and a half feet of "
                   "muscle with green-grey skin, short tusks, bristly black "
                   "hair, wearing an open hot-pink silk shirt and heavy gold "
                   "chains"),
    "maggie":     ("a hard-faced athletic woman of 40 with cropped brown "
                   "hair, wearing a black leather jacket and metallic silver "
                   "pants, five small glowing red skulls floating in the air "
                   "beside her head"),
    "mongo":      ("a dog-sized baby raptor dinosaur covered in fluffy pink, "
                   "blue and red feathers, an oversized head, tiny clawed "
                   "arms and enormous eager eyes, " + CAT),
}
FRANK = ("a lean bald man of 40 in a navy-blue sports beanie, spiked "
         "shoulder pads over a hoodie, carrying a battle axe")

# ------------------------------------------------------------- anchors ----
# (name, aspect, prompt, [refs])

ANCHORS = [
    ("carl", "3:4",
     f"Full-body character portrait of {W['carl']}. He stands in a torchlit "
     f"rough stone tunnel, arms loose, jaw set, done with everything. "
     f"{SOLO} {STYLE}", []),
    ("donut", "3:4",
     f"Full-body portrait of {W['donut']}, WITHOUT any crown or accessories. "
     f"She sits bolt upright on a stone ledge in a torchlit tunnel, chest "
     f"out, supremely pleased with herself. The cat is the only creature in "
     f"the frame. {STYLE}", []),
    ("donut_crowned", "3:4",
     f"Full-body portrait of EXACTLY the same cat as the reference image — "
     f"identical fur pattern and face — now {W['donut_c']}. She sits on a "
     f"velvet cushion like a monarch receiving court. The cat is the only "
     f"creature in the frame. {STYLE}", ["donut"]),
    ("mordecai_rat", "3:4",
     f"Full-body character portrait of {W['mordecai_rat']}. He leans on a "
     f"guildhall bar with a bottle, mid-shrug, world-weary. {SOLO} {STYLE}", []),
    ("mordecai_bug", "3:4",
     f"Full-body creature portrait of {W['mordecai_bug']}. It stands in a "
     f"cinderblock corridor waving one long arm in greeting. The creature is "
     f"the only figure in the frame. {STYLE}", []),
    ("brandon", "3:4",
     f"Full-body character portrait of {W['brandon']}. He stands in a "
     f"lantern-lit stone chamber, hammer over one shoulder, huge friendly "
     f"grin. {SOLO} {STYLE}", []),
    ("elle", "3:4",
     f"Full-body character portrait of {W['elle']}. She stands in a "
     f"cinderblock corridor with her arms crossed, one eyebrow up. {SOLO} "
     f"{STYLE}", []),
    ("agatha", "3:4",
     f"Full-body character portrait of {W['agatha']}. She stands at the edge "
     f"of lantern light in a stone chamber, the shadows around her unnaturally "
     f"deep. {SOLO} {STYLE}", []),
    ("zev", "3:4",
     f"Full-body character portrait of {W['zev']}. She stands on a diner "
     f"table to be seen, datapad clutched to her chest, earnest and nervous. "
     f"{SOLO} {STYLE}", []),
    ("odette", "3:4",
     f"Full-body character portrait of {W['odette']}. She is posed on a "
     f"glittering talk-show dais under a spotlight, one claw raised "
     f"theatrically. {SOLO} {STYLE}", []),
    ("maestro", "3:4",
     f"Full-body character portrait of {W['maestro']}. He poses on a garish "
     f"game-show stage, arms wide to an unseen crowd, smug. {SOLO} {STYLE}", []),
    ("maggie", "3:4",
     f"Full-body character portrait of {W['maggie']}. She stands in a dark "
     f"tunnel lit mostly by the floating red skulls, cold and controlled. "
     f"{SOLO} {STYLE}", []),
    ("mongo", "3:4",
     f"Full-body creature portrait of {W['mongo']}. He stands amid broken "
     f"pastel eggshell pieces, head cocked, mouth open in a delighted "
     f"screech. The creature is the only figure in the frame. {STYLE}", []),
    # ---- location plates ----
    ("loc_suburb", "16:9",
     "Establishing wide shot, no people: a Seattle suburb at night in winter "
     "reduced to an endless flat field of pale powdered rubble under "
     "moonlight, light snow falling, no building left standing, a few "
     "glowing red-gold staircase portals descending into the ground, dotted "
     f"to the horizon. Desolate, silent, beautiful. {STYLE}", []),
    ("loc_tunnel", "16:9",
     "Establishing shot, no people: an endless rough rock-hewn dungeon "
     "tunnel, torch sconces with warm flames, moss in cracks, side passages "
     f"fading to black, video-game-fantasy texture but photoreal. {STYLE}", []),
    ("loc_safe_room", "16:9",
     "Establishing interior shot, no people: a cozy windowless diner inside "
     "a dungeon — vinyl booths, a counter with stools, warm lamps, a wall of "
     "three old televisions glowing, a door marked with a soft green glow. "
     f"{STYLE}", []),
    ("loc_maze", "16:9",
     "Establishing shot, no people: a tight institutional corridor of grey "
     "cinderblock walls under flickering harsh lights, junctions in every "
     f"direction, claustrophobic, like an endless basement. {STYLE}", []),
]

# --------------------------------------------------------------- frames ----
# (name, [refs], prompt)  — all 16:9; a held still shows the END of its beat.

BANNER = ("a glowing translucent gold holographic banner floating in the air, "
          "crisp elegant game-interface lettering reading exactly: ")
BLUE = ("glowing translucent blue holographic game-interface text panels "
        "floating in the air")

F = [
    ("t0", ["loc_suburb"],
     "The ruined-suburb plate exactly as the reference image, night snowfall, "
     "with a massive cinematic title floating in the sky in cracked glowing "
     "gold game-interface capitals reading exactly: \"DUNGEON CRAWLER CARL\" "
     "and beneath it in smaller clean white letters exactly: \"BOOK ONE\". "
     "The lettering is crisp and spelled exactly as given."),
    # ---- ACT A : floor 1 ----
    ("a1", ["carl", "donut"],
     f"A freezing suburban night BEFORE any destruction: an intact apartment "
     f"building with lit windows behind a bare winter tree, snow falling. At "
     f"the base of the tree, {W['carl_crocs']} reaches up with both arms, "
     f"exasperated, breath steaming. Up on a branch sits {W['donut']}, no "
     f"crown, looking down at him with total indifference. No other people. "
     f"{STYLE}"),
    ("a2", ["carl", "donut"],
     f"Apocalyptic wide shot, night: an entire suburb collapsing into "
     f"rolling columns of pale dust at once, every house folding flat, a "
     f"wall of powder billowing toward camera. In the foreground "
     f"{W['carl_crocs']} stands frozen in the snow, clutching {W['donut']} "
     f"(no crown) to his chest, both staring at the destruction. No other "
     f"people visible."),
    ("a3", ["loc_suburb", "carl", "donut"],
     f"On the flattened rubble field at night, a glowing red-gold stone "
     f"staircase descends into the earth. {W['carl_crocs']} stands three "
     f"steps down holding {W['donut']} (no crown), looking back over his "
     f"shoulder at the grey ruin and the falling snow. Tiny distant figures "
     f"in pajamas trudge toward other glowing stairwells far away."),
    ("a4", ["loc_tunnel", "carl", "donut"],
     f"In the torchlit tunnel, {W['carl']} squints at {BLUE} arrayed around "
     f"him at head height, plus {BANNER}\"ACHIEVEMENT UNLOCKED\". At his "
     f"ankles {W['donut']} (no crown) rubs against his bare shin. His feet "
     f"are bare on the stone; the pink sandals are gone."),
    ("a5", ["loc_tunnel", "carl", "donut"],
     f"In the tunnel, the smoking burning wreck of a small steam-powered "
     f"bulldozer covered in welded blades lies on its side. {W['carl']} "
     f"stands before it holding a lit brass lighter, deadpan; {W['donut']} "
     f"(no crown) stands beside him with every hair puffed out in alarm. "
     f"Three small green goblins flee into a side passage in the distance."),
    ("a6", ["mordecai_rat", "carl", "donut"],
     f"Inside a cozy torchlit guildhall bar, {W['mordecai_rat']} leans "
     f"across the bar pouring an amber drink and explaining something with "
     f"one raised finger. {W['carl']} sits slumped on a stool, head in his "
     f"hands. {W['donut']} (no crown) sits on the bar top, examining her own "
     f"reflection in a bottle. Nobody else in the room."),
    ("a7", ["carl"],
     f"In a torchlit tunnel alcove, an opened wooden treasure chest "
     f"overflows with golden light and drifting sparkles. {W['carl_cloak']} "
     f"— the shadow-cloak and reptile-leather shirt clearly brand new — "
     f"holds up one tiny gold toe ring between finger and thumb, examining "
     f"it with a flat unimpressed stare. {SOLO}"),
    ("a8", ["mordecai_rat", "carl", "donut_crowned"],
     f"In the guildhall, {W['donut_c']} sits enthroned on an upturned barrel, "
     f"chin high, purple sparks drifting from the tiara's center stone, "
     f"surrounded by {BLUE}. Above her floats {BANNER}\"THE ROYAL COURT OF "
     f"PRINCESS DONUT\". Beside her {W['carl_cloak']} presses a palm over "
     f"his whole face. {W['mordecai_rat']} raises his bottle in a resigned "
     f"toast."),
    ("a9", ["loc_tunnel", "carl", "donut_crowned"],
     f"In the tunnel, {W['carl_cloak']} stands with one bare foot planted "
     f"on the flank of a defeated llama sprawled on the stone floor, his "
     f"knuckles scuffed, expression apologetic. {W['donut_c']} sits facing "
     f"deliberately AWAY from him, mortified. Floating above: "
     f"{BANNER}\"ACHIEVEMENT: SMUSH\"."),
    ("a10", ["loc_safe_room", "carl", "donut_crowned"],
     f"Inside the safe-room diner, a small four-foot big-eared innkeeper "
     f"creature in an apron sets a steaming bowl of curry before "
     f"{W['carl_cloak']} in a booth. On the table {W['donut_c']} sits before "
     f"a silver dish of salmon pate on a folded napkin. The three wall "
     f"televisions glow with colorful broadcast graphics. No other patrons."),
    ("a11", ["carl", "donut_crowned"],
     f"A vast dim cavern walled with mountains of garbage. Rising waist-deep "
     f"from a trash mound, a fifteen-foot sorrowful giantess with stringy "
     f"hair and a single tooth, mid-wail, as a wave of small pale rodent "
     f"creatures pours down the slope toward camera. In the foreground "
     f"{W['carl_cloak']} shields {W['donut_c']} behind his leg, his other "
     f"hand holding a lit stick of dynamite low behind his back."),
    ("a12", ["loc_safe_room", "carl", "donut_crowned"],
     f"In the safe-room diner, the central wall television shows a glitzy "
     f"broadcast: a young girl flanked by two black rottweilers under the "
     f"lights. {W['donut_c']} stands rigid on the table, staring at the "
     f"screen, outraged. {W['carl_cloak']} watches from the booth over a "
     f"mug, half-smiling."),
    ("a13", ["loc_tunnel", "carl", "donut_crowned"],
     f"A torchlit goblin camp: {W['donut_c']} sits enthroned on a crate "
     f"while two robed goblin shamans kneel before her in open adoration. "
     f"Beside them {W['carl_cloak']} clasps forearms with a goblin chief "
     f"over a gleaming steampunk copper motorcycle with a sidecar. Small "
     f"wooden crates change hands between goblins in the background."),
    ("a14", ["carl", "donut_crowned"],
     f"Night-dark tunnel mouth: far behind, an industrial workshop burns, "
     f"orange fire and black smoke. In the foreground {W['carl_cloak']} sits "
     f"on rubble facing away from the fire, soot on his face, eyes hollow, "
     f"staring at nothing. {W['donut_c']} presses silently against his side. "
     f"Floating above them, horribly cheerful: {BANNER}\"NEW ACHIEVEMENT: "
     f"WAR CRIMINAL\"."),
    ("a15", ["maggie", "carl", "donut_crowned"],
     f"A safe-room doorway kicked open: {W['maggie']} and {FRANK} burst into "
     f"an empty diner, weapons ready, finding only a conspicuously placed "
     f"dead rat wearing a tiny gift bow on the floor. Through the doorway "
     f"behind them, small in the distance down the tunnel, {W['carl_cloak']} "
     f"and {W['donut_c']} ride away on the copper motorcycle."),
    # ---- ACT B ----
    ("b1", ["loc_tunnel", "carl", "donut_crowned"],
     f"The copper motorcycle roars down an endless torchlit tunnel, motion "
     f"streaks in the torch flames. {W['carl_cloak']} leans low over the "
     f"handlebars; {W['donut_c']} stands tall in the sidecar, fur and cloak "
     f"streaming in the wind, living her best life. On the rock wall, "
     f"spray-painted white letters reading exactly: \"SURVIVORS\" with an "
     f"arrow."),
    ("b2", ["brandon", "elle", "agatha", "carl", "donut_crowned"],
     f"A wide lantern-lit stone chamber arranged as a refugee camp: cots, "
     f"wheelchairs, dozens of elderly people. {W['brandon']} pumps "
     f"{W['carl_cloak']}'s hand, delighted. {W['elle']} stands beside them, "
     f"arms crossed, appraising. {W['donut_c']} holds court on a cot amid "
     f"three admiring old ladies. At the far edge of the lantern light "
     f"{W['agatha']} stands in a patch of unnaturally deep shadow."),
    ("b3", ["carl", "donut_crowned"],
     f"A wrecked 24-hour gym in the dungeon, mirrors shattered, machines "
     f"toppled. A massive lizard-headed bodybuilder monster in a tank top "
     f"lies collapsed under a fallen barbell rack. {W['donut_c']} stands on "
     f"its chest, fangs bared in triumph. {W['carl']} sits propped against "
     f"a bench, battered and bloodied but grinning, raising his right arm "
     f"to show off a newly-equipped heavy bronzed war gauntlet."),
    ("b4", ["brandon", "elle", "carl", "donut_crowned"],
     f"A huge boss arena: against the far wall lies a burst, smoking ball "
     f"of fused armored pig-knights the size of a house. Center frame, a "
     f"ramshackle armored wagon built of bolted-together steel tables, "
     f"painted crudely with white letters reading exactly: \"SPEEDBUMP\", "
     f"elderly faces peeking from hatches. {W['brandon']} stands on top "
     f"with his hammer raised in victory; {W['elle']} waves her cane from a "
     f"hatch; {W['carl_full']} leans against the hull; {W['donut_c']} poses "
     f"on the prow. Confetti of golden loot sparkles rains down."),
    ("b5", ["odette", "carl", "donut_crowned"],
     f"A dazzling alien talk-show stage before a vast roaring audience of "
     f"varied aliens. {W['odette']} leans from her glittering dais toward "
     f"{W['donut_c']}, who sits on a velvet pouf under her own spotlight, "
     f"mid-monologue, adored. {W['carl_full']} sits awkwardly in the human-"
     f"sized guest chair, bare feet conspicuous, enduring."),
    # ---- ACT C : floor 2 ----
    ("c1", ["loc_maze", "carl", "donut_crowned"],
     f"The cinderblock maze corridor: {W['carl_full']} and {W['donut_c']} "
     f"walk toward camera. Floating above the junction behind them, huge "
     f"glowing red holographic game-interface numerals reading exactly: "
     f"\"6 DAYS\"."),
    ("c2", ["loc_maze", "elle", "carl", "donut_crowned"],
     f"In the cinderblock corridor, three dog-sized mangy kobold creatures "
     f"lie defeated. {W['carl_full']} stands mid-shrug — his bare feet now "
     f"SPARKLING with fine glitter, catching the light. {W['elle']} gives "
     f"him a skeptical head-to-toe once-over. {W['donut_c']} looks smug."),
    ("c3", ["carl", "donut_crowned"],
     f"A dungeon moonshine distillery: copper vats, dripping pipes, crates "
     f"of clay jugs. {W['carl_full']} holds up a clay jug with a rag fuse, "
     f"grimly pleased; {W['donut_c']} sits on a vat above him. Small angry "
     f"leprechaun-like men in filthy green coats flee down a walkway in the "
     f"background. Floating beside the jug, {BLUE} reading exactly: "
     f"\"CARL'S JUG O'BOOM\"."),
    ("c4a", ["carl", "donut_crowned"],
     f"A dark stone antechamber lit by one candle: {W['carl_full']} and "
     f"{W['donut_c']} crouch nose-to-nose behind an overturned alchemy "
     f"table, her paw resting on his gauntlet, an unexpectedly tender beat. "
     f"Past them, down a long corridor, a shambling green-coated corpse-man "
     f"walks AWAY carrying a clay jug toward a distant writhing mass of "
     f"pale tentacles."),
    ("c4b", ["carl", "donut_crowned"],
     f"A corridor lit end to end by a wall of fire: tiny {W['donut_c']}, "
     f"every muscle straining, teeth clamped on the black shadow-cloak, "
     f"drags the unconscious body of {W['carl_full']} across the stone "
     f"floor away from the flames, the tiara's purple stone blazing. Embers "
     f"drift like snow."),
    ("c5", ["zev", "mordecai_bug", "carl", "donut_crowned"],
     f"A safe-room diner booth, cozy: {W['zev']} sits on the table beside "
     f"{W['donut_c']}, both rapt at a wall television showing a glossy "
     f"teen drama. {W['mordecai_bug']} is wedged comically into the booth "
     f"behind them, equally rapt. {W['carl_full']} watches all three from "
     f"the counter over a bowl of curry, amused."),
    ("c6", ["brandon", "elle", "carl", "donut_crowned"],
     f"A scorched cinderblock corridor, quiet: survivors stand with heads "
     f"bowed around a small cairn of stones topped by a single lantern and "
     f"a folded caregiver's cardigan. {W['brandon']} holds his hat to his "
     f"chest; {W['elle']} rests her hand on the cairn; {W['carl_full']} "
     f"stands at the edge with his gauntleted fist clenched; {W['donut_c']} "
     f"sits perfectly still, head lowered."),
    ("c7a", ["carl", "donut_crowned"],
     f"Action: the copper motorcycle at full tilt down a cinderblock "
     f"corridor, {W['carl_full']} low over the bars, {W['donut_c']} flat in "
     f"the sidecar. Filling the corridor behind them, a towering monster of "
     f"living black smoke with burning orange eyes and reaching claws; "
     f"loose rubble floats weightlessly around it; a clay jug tumbles "
     f"through the air behind the bike, mid-throw, trailing sparks from "
     f"its rag fuse."),
    ("c7b", ["carl", "donut_crowned"],
     f"Aftermath: a wide scorched junction, the smoke monster collapsing "
     f"into drifting embers and ash. {W['carl_full']} stands silhouetted "
     f"against the glow, chest heaving, the motorcycle wrecked and smoking "
     f"behind him; {W['donut_c']} climbs from the toppled sidecar. Floating "
     f"above the embers: {BANNER}\"LEVEL 93 DEFEATED\"."),
    ("c8", ["maestro", "carl", "donut_crowned"],
     f"A garish game-show stage with caged glass pods and lurid neon. "
     f"{W['maestro']} crushes a golden goblet in one fist, mid-tantrum. "
     f"{W['carl_full']} walks calmly toward camera, leading three exhausted "
     f"rescued human prisoners — two men and a young woman in ragged work "
     f"clothes, all WALKING upright on their feet close behind him — away "
     f"from the pods, not looking back. {W['donut_c']} rides on Carl's "
     f"shoulder, tail high. An unseen crowd's spotlights sweep the stage."),
    ("c9", ["maggie"],
     f"A pitch-dark cinderblock corridor lit only by five floating red "
     f"skulls: {W['maggie']} stares straight into camera, jaw set, holding "
     f"up a small brass compass whose needle glows the same red. Behind "
     f"her, half in shadow, {FRANK} stands hollow-eyed, looking at the "
     f"floor. No other light."),
    ("c10", ["carl", "donut_crowned"],
     f"A concrete municipal dog-pound fighting pit ringed with cage doors — "
     f"all standing OPEN. A pack of mangy dingo-like dogs joyfully swarms "
     f"over a giant panicked gerbil the size of a bear wearing a tiny "
     f"crown, mid-dogpile. {W['carl_full']} leans on the pit rail tossing "
     f"one last biscuit; {W['donut_c']} beside him looks away with immense "
     f"distaste."),
    ("c11", ["donut_crowned", "mongo", "carl"],
     f"A soft pastel reward chamber scattered with broken eggshell: "
     f"{W['mongo']} affectionately gnaws the ear of {W['donut_c']}, who "
     f"radiates joy anyway, eyes closed, tiara askew. {W['carl_full']} "
     f"crouches beside them, one hand raised in a helpless don't-ask "
     f"gesture."),
    ("c12", ["carl", "donut_crowned", "mongo"],
     f"A vast glowing spiral stairwell descending into darkness. "
     f"{W['carl_full']} walks down the first turn. Beside him {W['mongo']} "
     f"trots with {W['donut_c']} riding tall on his feathered back like a "
     f"knight on a steed. All three glance back up toward camera, lit from "
     f"below by the deep red-gold glow."),
    ("tE", [],
     "A pure black cinematic end card. Centered, in elegant cracked gold "
     "game-interface capitals, text reading exactly: \"END OF BOOK ONE\", "
     "and beneath it in small white letters exactly: \"floor 3 awaits\". "
     "Nothing else in frame."),
]
FRAMES = [(n, "16:9", p, r) for n, r, p in F]

# ------------------------------------------------------------- dialogue ----
# shot -> ordered (speaker, line). All lines are original paraphrase.

LINES = {
    "t0": [],
    "a1": [("carl", "Donut. It is two thirty in the morning and it is snowing. "
                    "I am in my boxers. Get out of the tree.")],
    "a2": [("ai", "Attention, residents of Earth. Following the dissolution of "
                  "your planetary government, all surface structures have been "
                  "reclaimed. We apologize for the inconvenience. Survivors are "
                  "cordially invited to the World Dungeon. Eighteen floors. "
                  "Grand prize: your planet back. Doors close at dawn!")],
    "a3": [("carl", "Okay. It's the murder hole or we freeze. Hang on, your "
                    "highness."),
           ("ai", "Welcome, Crawler. Welcome to the World Dungeon.")],
    "a4": [("ai", "New achievement! First man on your continent to enter the "
                  "dungeon in his underpants. Your reward is a loot box. It "
                  "does not contain pants.")],
    "a5": [("carl", "That was a bulldozer made of knives. Why do the goblins "
                    "have a bulldozer made of knives?")],
    "a6": [("mordecai", "Rule one, kid: everything down here wants to eat you. "
                        "Rule two: this is a television show. The whole galaxy "
                        "is watching. Eighteen floors, and nobody has ever "
                        "finished. Be entertaining. It's the only armor that "
                        "works."),
           ("carl", "Everyone I know is dead... and I'm on a game show.")],
    "a7": [("ai", "Bronze adventurer box! You receive: one shadow cloak. One "
                  "trollskin shirt. One... toe ring. No shoes. No pants. Daddy "
                  "knows what you need, Carl."),
           ("carl", "I hate you."),
           ("ai", "Politeness is rewarded, Carl.")],
    "a8": [("donut", "CARL. CARL. I CAN TALK NOW, CARL, AND I HAVE FOUR YEARS "
                     "OF THINGS TO SAY TO YOU."),
           ("carl", "Oh no."),
           ("donut", "Also I found a tiara, and I am wearing it. It matches "
                     "my eyes."),
           ("ai", "Item equipped: the Enchanted Crown of the Sepsis Whore. "
                  "Cursed! Delightfully cursed. The party is now the Royal "
                  "Court of Princess Donut. Carl has been demoted to Royal "
                  "Bodyguard."),
           ("carl", "Goddammit, Donut.")],
    "a9": [("carl", "The llama was dealing drugs, Donut. The llama swung "
                    "first."),
           ("ai", "New achievement! Barefoot stomp streak! Oh, Carl. Your feet "
                  "are magnificent, and the audience agrees."),
           ("carl", "I need an adult.")],
    "a10": [("donut", "The attendant recognizes quality, Carl. Salmon pate, "
                      "warmed, and a cushion. You may have the curry."),
            ("carl", "End of the world, and honestly? The curry's pretty "
                     "good.")],
    "a11": [("donut", "CARL. IT IS COUGHING UP MORE OF THEM. DO THE THING."),
            ("carl", "She used to be a person, Donut. Down here, half the "
                     "monsters used to be people. ...Cover your ears.")],
    "a12": [("donut", "We are on television, Carl! Wait. Why is the child with "
                      "the dogs ranked first? I am OBVIOUSLY the more "
                      "compelling story.")],
    "a13": [("donut", "CARL. I HAVE DISCOVERED THE CHAT. I AM YELLING, CARL. "
                      "EVERYONE CAN SEE ME YELLING."),
            ("carl", "So the goblins take the llama product, we take the "
                     "motorcycle, and nobody tells the llamas where it came "
                     "from. ...I may have just started a war.")],
    "a14": [("ai", "New achievement: War Criminal! You monster. A commemorative "
                   "banner has been added to your collection."),
            ("carl", "Nobody told me there were kids in there. Nobody told me "
                     "goblins HAD kids.")],
    "a15": [("maggie", "Two celebrity crawlers, one exit. Easy experience. "
                       "Frank — check the rat for loot."),
            ("carl", "Enjoy the rat.")],
    "b1": [("donut", "Faster, Carl. My followers expect a certain standard of "
                     "adventure."),
           ("carl", "It's a hundred miles of tunnel, Donut. Sit in the sidecar "
                    "and wave.")],
    "b2": [("brandon", "Folks, it's really him! The foot guy! And the talking "
                       "cat!"),
           ("donut", "PRINCESS talking cat."),
           ("brandon", "Thirty-six residents, two caregivers, my brother and "
                       "me. We all go down together, or we don't go."),
           ("agatha", "Them critters already know I'm here.")],
    "b3": [("juicer", "I NEED A SPOT, BRO."),
           ("carl", "Donut—"),
           ("donut", "I am ALREADY ON HIM, CARL."),
           ("ai", "Loot awarded: the Enchanted War Gauntlet of the Exalted "
                  "Grull. Someone earned his tiny guardian angel today.")],
    "b4": [("brandon", "She ain't pretty, but she rolls."),
           ("carl", "Nothing I build is pretty. Everybody inside the "
                    "Speedbump."),
           ("donut", "I shall ride on top. For morale."),
           ("ai", "Borough boss defeated! Level ten! The stairwell is open, "
                  "crawlers.")],
    "b5": [("odette", "Listen to me, sweetheart. The audience doesn't keep you "
                      "alive. Being interesting keeps you alive. And never "
                      "trust anyone until you know what they're getting out "
                      "of you. Present company included."),
           ("donut", "I like her enormously, Carl.")],
    "c1": [("ai", "Welcome, crawlers, to floor two! Your time limit has been "
                  "reduced to six days — someone in accounting is thrilled. "
                  "Also, a reminder: public urination now summons a Rage "
                  "Elemental. Sleep tight!")],
    "c2": [("ai", "New achievement! This little piggy went to market! Your "
                  "reward: the Enchanted Pedicure Kit of the Sylph. Oh, Carl. "
                  "They SPARKLE now."),
           ("carl", "I want to die."),
           ("elle", "Kid, if a glitter-footed man in boxer shorts is my "
                    "rescue party, I'll take it. Elle McGibbons. Point me at "
                    "something evil.")],
    "c3": [("ai", "Recipe registered! Carl's Jug O'Boom is now official "
                  "dungeon crafting — with royalties. The little whiskey men "
                  "are FURIOUS."),
           ("carl", "Moonshine napalm. Bea always said I'd never make "
                    "anything of myself.")],
    "c4a": [("donut", "Carl. If we die today, I want you to know that I love "
                      "you almost as much as Bea. And Ferdinand."),
            ("carl", "...I'll take it. Send in the delivery boy.")],
    "c4b": [("donut", "CARL. YOU WILL NOT DIE. I JUST FINISHED TRAINING "
                      "YOU.")],
    "c5": [("zev", "Hi. Zev. Your new public relations liaison. And — off the "
                   "record? What's happening to your planet isn't fair. You "
                   "know it. I know it. The cat knows it."),
           ("donut", "The cat ALSO knows every episode of Gossip Girl. "
                     "Mordecai. Tell her where we are."),
           ("mordecai", "We're at the part where everyone is terrible. It's "
                        "very relatable.")],
    "c6": [("brandon", "It wasn't Jack's fault. He was old, and he was scared, "
                       "and nobody built this place for people like him."),
           ("elle", "Yolanda stood her ground so Ruth could run. You remember "
                    "her name.")],
    "c7a": [("carl", "Six hundred sixty-six souls, huh? Come earn them. "
                     "Chase the chicken."),
            ("ai", "He's doing it! He's actually doing it! THIS, crawlers, is "
                   "why we watch the show!")],
    "c7b": [("ai", "Level ninety-three Rage Elemental: DEFEATED. That was not "
                   "supposed to be possible. Somewhere, an actuary is "
                   "weeping. Congratulations, you magnificent lunatic.")],
    "c8": [("maestro", "Nothing is too good for Maestro's little piglets! Beg "
                       "the celebrity nicely, piglets!"),
           ("carl", "Here's the deal, your highness. I smile for your "
                    "cameras, and all three of them walk out with us. That's "
                    "the price of the foot guy."),
           ("lijun", "Saved again. We will not forget this, Carl.")],
    "c9": [("maggie", "You don't know anything about me. Nobody gets the "
                      "whole story. ...Find Crawler. I'm coming for you, "
                      "Carl.")],
    "c10": [("carl", "Everybody likes biscuits. Sit. Stay. ...Sic 'em."),
            ("ai", "New achievement: PETA Enthusiast! The gerbil never stood "
                   "a chance.")],
    "c11": [("donut", "His name is Mongo. He is my Royal Steed and he is "
                      "PERFECT — ow. OW. CARL, HE IS BITING MY FACE. I LOVE "
                      "HIM.")],
    "c12": [("mordecai", "Floor three is different, kids. You pick a race and "
                         "a class down there, and it's forever. Choose "
                         "boring. You won't. But choose boring."),
            ("carl", "Two floors down. Sixteen to go. Donut — try not to get "
                     "crowned queen of anything on the way."),
            ("donut", "NO PROMISES, CARL.")],
    "tE": [],
}

# --------------------------------------------------------- cut & motion ----

ORDER = ["t0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10",
         "a11", "a12", "a13", "a14", "a15",
         "b1", "b2", "b3", "b4", "b5",
         "c1", "c2", "c3", "c4a", "c4b", "c5", "c6", "c7a", "c7b", "c8",
         "c9", "c10", "c11", "c12", "tE"]

SILENT_HOLD = {"t0": 5.0, "tE": 6.0}
# Shots that are ABOUT stillness — no Ken Burns drift.
KB_LOCK = {"t0", "a14", "c4b", "c6", "c9", "tE"}

# ---------------------------------------------------------------- sound ----
# music mark at a shot starts a cue there; "silence" ends the current cue.

MUSIC_MARKS = {
    "t0": "title", "a1": "silence",
    "a2": "collapse", "a4": "silence",
    "a11": "boss", "a12": "silence",
    "a14": "tragedy", "a15": "silence",
    "b1": "adventure", "b2": "silence",
    "b4": "boss", "b5": "show",
    "c1": "silence",
    "c4a": "boss", "c5": "silence",
    "c6": "tragedy", "c7a": "chase", "c7b": "silence",
    "c8": "show", "c9": "silence",
    "c11": "end",   # runs through c12 + tE, faded out by the assembler
}
# cue -> (sonilo prompt, duration seconds). All instrumental.
MUSIC_CUES = {
    "title":     ("Dark playful orchestral-electronic main title theme, "
                  "ominous synth pulse with a mischievous music-box melody, "
                  "cinematic. Instrumental only, no vocals.", 30),
    "collapse":  ("Vast slow awe-and-dread cue, deep sub swells, distant "
                  "choir-like pads, a world ending quietly, cinematic. "
                  "Instrumental only, no vocals.", 45),
    "boss":      ("Driving percussive dungeon boss-fight cue, taiko and low "
                  "brass stabs, tense and punchy. Instrumental only, no "
                  "vocals.", 60),
    "tragedy":   ("Sparse mournful piano and low strings, grief-stricken, "
                  "restrained, a quiet devastation. Instrumental only, no "
                  "vocals.", 50),
    "adventure": ("Upbeat rowdy adventure travel montage, chugging guitars "
                  "and hand drums, wind-in-your-fur joyride. Instrumental "
                  "only, no vocals.", 40),
    "show":      ("Glitzy over-the-top talk-show big-band brass fanfare into "
                  "a vamping groove, game-show sparkle. Instrumental only, "
                  "no vocals.", 45),
    "chase":     ("Relentless high-speed chase cue, pounding drums, sawing "
                  "synth bass, heroic brass hits, maximum adrenaline. "
                  "Instrumental only, no vocals.", 60),
    "end":       ("Warm hopeful end-titles theme with the mischievous "
                  "music-box melody returning over soft strings, bittersweet "
                  "and fond. Instrumental only, no vocals.", 60),
}
# dB offsets under the film's dialogue anchor (per playbook: -12..-16 amb)
MUSIC_DB = -12.0
AMB_DB = -14.0

# ambience mark at a shot starts a bed there; "none" ends the current bed.
AMB_MARKS = {
    "t0": "suburb_night",
    "a4": "dungeon_corridor", "a10": "safe_room",
    "a11": "boss_arena", "a12": "safe_room", "a13": "goblin_caves",
    "b1": "dungeon_corridor", "b3": "boss_arena", "b5": "studio_crowd",
    "c1": "dungeon_corridor", "c4a": "boss_arena", "c5": "safe_room",
    "c6": "dungeon_corridor", "c7a": "boss_arena", "c8": "studio_crowd",
    "c9": "dungeon_corridor", "c10": "boss_arena", "c11": "safe_room",
    "c12": "dungeon_corridor", "tE": "none",
}

# ----------------------------------------------------------------- cast ----
# provisional picks (first) — Dawn re-casts from auditions.html

VOICES = {
    "branok":    ("Vs5CmVCVJwW4odQS2pVf", "Branok — raspy (US)"),
    "carter":    ("qNkzaJoHLLdpvgh5tISm", "Carter — deep (US)"),
    "harry":     ("SOYHLrjzK2X1ezoPC6cr", "Harry — fierce warrior (US)"),
    "lily":      ("pFZP5JQG7iQjIQuC4Bku", "Lily — velvety actress (UK)"),
    "charlotte": ("rhS7yjXTU4uIlRxXhNW7", "Charlotte — classy (UK)"),
    "elariel":   ("ksryVoNAGZT8GxWCTiVm", "ElarielQueen — wise (UK)"),
    "ianalien":  ("D2jw4N9m4xePLTQ3IHjU", "IanAlien — modulated"),
    "callum":    ("N2lVS1w4EtoT3dr4eOWO", "Callum — husky trickster (US)"),
    "tyler":     ("5DB4wgykoKoCu98YaGe6", "Tyler Cash — expressive (US)"),
    "bill":      ("pqHfZKP75CvOlQylNhV4", "Bill — wise, mature (US)"),
    "schmitz":   ("HAvvFKatz0uu0Fv55Riy", "Schmitz — raspy old (UK)"),
    "brianraspy": ("lwGnQIn0Z9pl1SoUiXZ3", "BrianRaspy — calm raspy"),
    "kristen":   ("Qbw4VpyUrHEG7NigKzty", "KristenQueen — intense (US)"),
    "sarah":     ("EXAVITQu4vr4xnSDxMaL", "Sarah — mature, confident (US)"),
    "cooper":    ("GsfuR3Wo2BACoxELWyEF", "Cooper — anxious (US)"),
    "jocelyn":   ("5gXlHkfPXOcdk5FdLHxY", "Jocelyn — calm (US)"),
    "darthoxley": ("G3zrXA9moYrFCgwBAvxJ", "DarthOxley — deep (US)"),
    "damien":    ("pHD4qotPFeOAuU1YsFjv", "Damien — intense (US)"),
    "chris":     ("iP95p4xoKVk53GoZ742B", "Chris — charming (US)"),
    "will":      ("bIHbv24MWmeRgasZH58o", "Will — relaxed optimist (US)"),
    "matilda":   ("XrExE9yKIg1WjnnlVkGX", "Matilda — upbeat professional (US)"),
    "laura":     ("FGY2WhTYpPnrIDTdsKH5", "Laura — sassy (US)"),
    "nana":      ("xIzR6egd3S3LJZbVW0c1", "Nana Margaret — old (US)"),
    "merv":      ("nCUo6wOgqVDAktRxhDA4", "Merv — intense (US)"),
    "kai":       ("hfqsl1OMbiWsgPpht3el", "Kai — clean modern (US)"),
}

# character -> (audition line, [candidate voice slugs]); first = provisional
AUDITIONS = {
    "carl": ("Two floors down, sixteen to go. The llama swung first, the "
             "goblins have a bulldozer made of knives, and I still don't "
             "have any pants. ...Goddammit, Donut.",
             ["branok", "carter", "harry"]),
    "donut": ("CARL. I HAVE DISCOVERED THE CHAT, CARL. I am a PRINCESS, "
              "Carl, I do not do stealth. Also I found a tiara and I am "
              "wearing it. It matches my eyes.",
              ["lily", "charlotte", "elariel"]),
    "ai": ("New achievement! Barefoot stomp streak! Oh, Carl. Your feet are "
           "magnificent, and the audience agrees. Politeness is rewarded, "
           "Carl. Daddy knows what you need.",
           ["ianalien", "callum", "tyler"]),
    "mordecai": ("Rule one, kid: everything down here wants to eat you. Rule "
                 "two: this is a television show. Be entertaining — it's the "
                 "only armor that works.",
                 ["bill", "schmitz", "brianraspy"]),
    "odette": ("Listen to me, sweetheart. The audience doesn't keep you "
               "alive. Being interesting keeps you alive.",
               ["kristen", "sarah"]),
    "zev": ("Hi. Zev. Your new public relations liaison. And — off the "
            "record? What's happening to your planet isn't fair.",
            ["cooper", "jocelyn"]),
    "maestro": ("Nothing is too good for Maestro's little piglets! Beg the "
                "celebrity nicely, piglets!",
                ["darthoxley", "damien"]),
    "brandon": ("Folks, it's really him! The foot guy! And the talking cat! "
                "We all go down together, or we don't go.",
                ["chris", "will"]),
    "elle": ("Kid, if a glitter-footed man in boxer shorts is my rescue "
             "party, I'll take it. Point me at something evil.",
             ["matilda", "laura"]),
    "agatha": ("Them critters already know I'm here.",
               ["nana", "merv"]),
    "maggie": ("Nobody gets the whole story. I'm coming for you, Carl.",
               ["merv", "sarah"]),
    "juicer": ("I NEED A SPOT, BRO.", ["darthoxley", "harry"]),
    "lijun": ("Saved again. We will not forget this, Carl.",
              ["kai", "will"]),
}
CAST = {c: VOICES[opts[1][0]][0] for c, opts in AUDITIONS.items()}
