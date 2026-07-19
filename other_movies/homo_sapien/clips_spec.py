"""Seedance 2.0 clip prompts for HOME SAPIEN — one per shot.

(name, gen_seconds, prompt, [anchor refs])

Each clip is generated with `--start-image frames/<name>.png` plus the anchor
refs below, at 480p `--std`. Gen durations run ~2s longer than the cut window so
the assembler can trim into the beat.

THE ONE RULE THIS FILM ADDS: we are cutting to Lenka's real master, so no clip
may ever speak or sing. NOSOUND goes in every prompt, and every clip is muted at
assembly. Seedance will otherwise grow spontaneous dialogue and lip movement
that fights the vocal.
"""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("locks", Path(__file__).parent / "locks.py")
_locks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_locks)
W = _locks.W
FACE = _locks.FACE   # identity WITHOUT wardrobe — costume shots

# ---- the three lock blocks, restated verbatim in every prompt ----

NOSOUND = (
    "Nobody speaks and nobody sings. No lips move. There is no dialogue, no "
    "narrator and no voiceover in this clip."
)
NEG = (
    "Photorealistic, natural human motion, no slow motion, no speed ramping, no "
    "text, no captions, no subtitles, no watermark, no on-screen graphics. Every "
    "character keeps exactly the same face, hair and clothes as in the start "
    "image and the reference images. Warm 35mm film look, soft golden practical "
    "light, gentle grain."
)
STATIC = "Locked-off static camera — no zoom, no pan, no push-in, no camera drift."
FRAME_LOCK = (
    "The set, the wardrobe, the framing and the lighting are exactly as in the "
    "start image and do not change during the clip."
)

# the two colour-coded souls, restated so the pairing never drifts
PAIRC = ("Throughout, one of the pair is warm coral-orange and the other is cool "
         "teal-blue — this colour pairing never swaps and never changes.")

CLIPS = [
    # ================= COLD OPEN =================
    ("s01_kitchen_dance", 9,
     f"{W['may']} is alone in her kitchen at 1am waiting for the kettle. She "
     f"does a private, deeply silly little dance — a shoulder wiggle, a hip "
     f"bump against the counter, a spin she doesn't quite land — entirely "
     f"believing nobody can see her. The kettle steams. She is the ONLY person "
     f"in the frame; the kitchen is otherwise completely EMPTY, no other "
     f"people. {STATIC} {FRAME_LOCK} {NOSOUND} {NEG}",
     ["may", "loc_kitchen"]),

    ("s02_two_dance", 8,
     f"The clip OPENS exactly on the start image: {W['may']} dancing alone in "
     f"the middle of the kitchen, and {W['ollie']} already standing IN THE "
     f"DOORWAY at the side of the room, one hand on the door frame, half "
     f"asleep, watching her. He is ALREADY VISIBLE IN FRAME from the very "
     f"first frame of the clip — he does NOT appear, arrive, fade in or "
     f"materialise at any point; he is simply already there, in the doorway, "
     f"where the start image puts him. Then, in one continuous move, he pushes "
     f"off the door frame and WALKS ON FOOT across the open floor toward her, "
     f"taking real steps along the clear stretch of bare lino, his feet on the "
     f"ground the whole way. He walks AROUND any furniture — he never passes "
     f"through the table, never passes through a chair, never clips through "
     f"any object; solid objects stay solid and he goes around them. He "
     f"reaches her, and without a word she takes his hands. They sway together "
     f"— badly, out of time, both slightly wrong-footed — and then they rest "
     f"their foreheads together and close their eyes. The forehead touch is "
     f"the key gesture of the whole film: gentle, unhurried, completely "
     f"ordinary to them. They are the ONLY two people in the frame; the kitchen "
     f"is otherwise completely EMPTY, and nobody else ever enters. {STATIC} "
     f"{NOSOUND} {NEG}",
     ["may", "ollie", "loc_kitchen"]),

    ("s03_eye", 6,
     f"Extreme close-up of {W['may']}'s eye as she laughs, crow's feet "
     f"crinkling. The camera pushes in slowly and steadily on the eye. In the "
     f"reflection on her iris, the deep blue night window of the kitchen slowly "
     f"breaks apart and becomes a field of stars, deepening into space. Slow "
     f"continuous push-in, no cuts. {NOSOUND} {NEG}",
     ["may"]),

    # ================= VERSE 1 =================
    ("s04_bigbang", 6,
     f"A single point of white light blooms out of an empty dark and unfurls "
     f"into warm dust and glitter, like paint dropped into water, filling the "
     f"frame. Out of the centre of the bloom, TWO tiny bright sparks — one warm "
     f"coral-orange, one cool teal-blue — spin away together, orbiting one "
     f"another as they travel. They stay together. Painterly, hand-mixed, "
     f"intimate rather than epic — the Big Bang as glitter in a shaft of light. "
     f"{PAIRC} {NOSOUND} {NEG}",
     []),

    # NB: the original wording ("leaning in until they almost touch, then
    # swinging apart... the rhythm is a slow breath: a forehead touch at cosmic
    # scale") drew 3 straight `nsfw` rejections — on a shot containing nothing
    # but two stars. The intimacy language was the trigger, not the image.
    # Rewritten as plain astronomy; the tenderness now comes from the framing.
    ("s05_binary_stars", 6,
     f"Two stars in a binary system — one warm coral-orange, one deep teal-blue "
     f"— circle slowly around a shared centre of gravity in a soft painterly "
     f"nebula, held close together by it, tracing one steady orbit. Nothing "
     f"else moves in the frame but drifting dust and distant starlight. Calm, "
     f"slow, tender. {PAIRC} {NOSOUND} {NEG}",
     []),

    ("s06_tidepool", 10,
     f"Macro shot into a tiny tidepool the size of a soup bowl in black "
     f"volcanic rock. TWO glowing single-celled blobs — one warm coral-orange, "
     f"one cool teal-blue — wobble slowly toward each other through the murky "
     f"green water. They bump. They recoil apart, startled. They wobble back "
     f"and bump again. On the third try they stick together, and drift on as "
     f"one. Comic, tender, unhurried. They are the ONLY two organisms in the "
     f"frame. {STATIC} {PAIRC} {NOSOUND} {NEG}",
     []),

    ("s07_waiting", 9,
     f"One small half-evolved amphibious creature — a proto-tetrapod like a "
     f"Tiktaalik: a fish that has just grown the beginnings of four stubby "
     f"LEGS, its finned tail still trailing in the water — has hauled itself "
     f"half out of the shallows onto a wet black rock at the edge of a "
     f"primordial sea. It is propped up on its two little front legs, chin "
     f"resting on them, gazing out to sea, and it WAITS, as though waiting for "
     f"someone running extremely late. It does not move — it blinks once, "
     f"slowly, with an expression of infinite deadpan patience. It is warm "
     f"coral-orange and it is clearly a four-legged land-crawling animal, not "
     f"a plain fish. Behind it, geological time "
     f"tears past in a blur: tides racing in and out, clouds streaking, light "
     f"strobing from day to night to day, ice advancing and retreating — a "
     f"hundred million years of weather. The creature stays perfectly still and "
     f"sharp in the centre of the frame the entire time. The comedy is that it "
     f"does not move. It is the ONLY creature in the frame. {STATIC} "
     f"{NOSOUND} {NEG}",
     []),

    ("s08_side_by_side", 10,
     f"A single procession of real living animals walks steadily left to right "
     f"along one dirt trail through golden savanna, and every stage of the "
     f"procession is a COUPLE walking SHOULDER TO SHOULDER, side by side, "
     f"keeping pace: two frogs, then two lizards, then two meerkat-like "
     f"mammals, then — at the front, closest to camera — two monkeys. In every "
     f"couple one animal is warm coral-orange and the other cool teal-blue, "
     f"and both animals of a couple are the SAME SPECIES. Every animal walks "
     f"the SAME WAY, left to right, in profile; no animal ever turns to face "
     f"another, and nobody walks toward anybody. As they travel, one of the "
     f"monkeys turns its head to glance sideways at its partner beside it, "
     f"checking she is keeping up, and then faces forward again. The camera "
     f"tracks smoothly alongside them, holding the procession in frame. Every "
     f"animal is a real photographed animal — never knitted, felt, plush or "
     f"cartoon. No aquariums, no tanks, no carts, no man-made objects. "
     f"{PAIRC} {NOSOUND} {NEG}",
     ["pair_fish", "pair_monkeys"]),

    ("s09a_fish", 5,
     f"Two real lobe-finned fish — the same two fish as the reference image, "
     f"one warm coral-orange and one deep teal-blue — hang side by side in "
     f"green underwater light, finning gently in place. They drift together "
     f"until their stubby fins touch, and they nudge their blunt snouts against "
     f"each other. Real living animals with wet scales, never knitted or plush. "
     f"They are the ONLY two creatures in the frame. {PAIRC} {NOSOUND} {NEG}",
     ["pair_fish"]),

    ("s09b_monkeys", 5,
     f"Two real early primates — the same two animals as the reference image, "
     f"one with warm coral-orange fur and one with cool teal-grey fur — hang "
     f"upside-down by their tails from the same jungle branch, swinging gently. "
     f"They reach out, take each other's hands, swing together, and bonk their "
     f"foreheads against each other, eyes closing in bliss. Real living "
     f"animals, never knitted or plush. They are the ONLY two creatures in the "
     f"frame. {PAIRC} {NOSOUND} {NEG}",
     ["pair_monkeys"]),

    ("s10_hominids", 7,
     f"Two early hominids — naked, hairy, upright animals wearing NO CLOTHING "
     f"and carrying nothing, one with warm rust-orange fur and one with cool "
     f"blue-grey fur — stand forehead to forehead in near-silhouette on an "
     f"African savanna at dawn, holding each other's forearms, swaying very "
     f"slightly, completely still and tender. Tall dry grass moves in the wind "
     f"around them; the enormous sun rises behind them. The camera rises slowly "
     f"and steadily. They are the ONLY two figures in the frame. {NOSOUND} "
     f"{NEG}",
     ["pair_hominids", "loc_savanna"]),

    # ================= CHORUS 1 =================
    ("s11_flower_cave", 6,
     f"At the mouth of a firelit cave 40,000 years ago, {W['may_sapien']} holds "
     f"out a scrappy little wildflower to {W['ollie_sapien']}, beaming with "
     f"total confidence, and pushes it toward him insistently when he doesn't "
     f"react. He stares at the flower, then at her, completely stunned, and "
     f"very slowly takes it. They are the ONLY two people in the frame; the "
     f"cave is otherwise completely EMPTY, no other people. {STATIC} "
     f"{FRAME_LOCK} {NOSOUND} {NEG}",
     ["may_sapien", "ollie_sapien", "loc_cave"]),

    ("s12_flower_kitchen", 6,
     f"MATCH CUT from the cave — identical framing, identical staging, present "
     f"day. {W['may']} holds out a sad cellophane-wrapped bunch of "
     f"petrol-station flowers to {W['ollie']}, beaming with exactly the same "
     f"total confidence as her ancient self, and pushes them toward him "
     f"insistently when he doesn't react. He stares at the flowers, then at "
     f"her, completely stunned, and very slowly takes them. The performance "
     f"beats must match the cave shot exactly. They are the ONLY two people in "
     f"the frame. {STATIC} {FRAME_LOCK} {NOSOUND} {NEG}",
     ["may", "ollie", "loc_kitchen"]),

    ("s13_hold_cave", 6,
     f"{W['may_sapien']} and {W['ollie_sapien']} lie curled together asleep in "
     f"furs at the mouth of a cave, breathing slowly, one of them shifting "
     f"closer in their sleep. The embers of the small fire pulse. Above them an "
     f"enormous sky of unpolluted stars wheels almost imperceptibly. They are "
     f"the ONLY two people in the frame. {STATIC} {NOSOUND} {NEG}",
     ["may_sapien", "ollie_sapien", "loc_cave"]),

    ("s14_hold_couch", 7,
     f"MATCH CUT from the cave — the same shape, the same composition, present "
     f"day. {W['may']} and {W['ollie']} lie curled together asleep on a sagging "
     f"sofa under a knitted blanket, breathing slowly, one of them shifting "
     f"closer in their sleep. A muted television flickers instead of embers. "
     f"Through the window above them, the same enormous sky of stars. They are "
     f"the ONLY two people in the frame. {STATIC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    ("s15_morph_walk", 6,
     f"A procession of couples walks steadily left to right across the frame, "
     f"hand in hand, never letting go, evolving as they walk. The order is "
     f"strictly OLDEST ON THE LEFT to NEWEST ON THE RIGHT, like the March of "
     f"Progress: stooped apelike hominids at the far left, then upright "
     f"fur-clad ice-age humans, then medieval peasants, and at the far right, "
     f"leading the procession and fully in focus, the present-day couple "
     f"{W['may']} and {W['ollie']}. Each couple becomes more modern and more "
     f"upright toward the RIGHT of frame. The earlier couples behind are soft "
     f"and fading. Continuous lateral tracking move, following the couple at "
     f"the front. {PAIRC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    ("s16_groceries", 6,
     f"{W['ollie']} stands frozen in the middle of the kitchen, loaded down "
     f"with the entire shopping — bags hanging off both arms to the shoulders, "
     f"more gripped in his teeth, a watermelon under one elbow, a baguette "
     f"under his chin — because he refused to make two trips. A bag splits and "
     f"oranges bounce across the yellow lino. He wobbles, tries to take one "
     f"step, and freezes again, wide-eyed, unable to move. {W['may']} sits on "
     f"the counter with a mug, watching him, absolutely delighted, and does "
     f"not help. They are the ONLY two people in the frame. {STATIC} "
     f"{FRAME_LOCK} {NOSOUND} {NEG}",
     ["may", "ollie", "loc_kitchen"]),

    ("s17_diorama_dance", 7,
     f"Inside a natural-history-museum diorama case — painted ice-age backdrop, "
     f"taxidermy mammoth, plastic ferns, fake snow — {W['may']} and "
     f"{W['ollie']}, in their ordinary modern clothes, do their terrible "
     f"swaying kitchen dance, completely out of place and entirely unbothered "
     f"by it, and rest their foreheads together. The mammoth does not move. "
     f"They are the ONLY two people in the frame. {STATIC} {FRAME_LOCK} "
     f"{NOSOUND} {NEG}",
     ["may", "ollie"]),

    ("s18_tree_of_life", 7,
     f"Very wide shot at dusk: two tiny human silhouettes stand together on a "
     f"bare hill at the bottom of the frame. Filling the whole sky above them, "
     f"drawn in delicate glowing constellation-lines, the branching TREE OF "
     f"LIFE slowly draws itself into existence, fork by fork, from the trunk "
     f"outward. On every fork, two small lights — one warm coral-orange, one "
     f"cool teal-blue — kindle side by side. The sky fills with pairs. Gentle, "
     f"handmade, awe without grandeur. {STATIC} {PAIRC} {NOSOUND} {NEG}",
     []),

    # ================= INSTRUMENTAL =================
    ("s19_handprints", 9,
     f"Firelight on a rough pale cave wall. TWO RED-OCHRE HANDPRINTS are "
     f"already finished on the rock, side by side, and two hands are hovering "
     f"just above them, having only this second lifted away. Over the course of "
     f"the clip the two hands simply WITHDRAW — they draw back and out of the "
     f"frame entirely, and the shot holds on the two finished handprints alone, "
     f"flickering in the firelight, in silence. THERE ARE EXACTLY TWO "
     f"HANDPRINTS ON THE WALL IN THIS ENTIRE CLIP, AND NO MORE. The hands NEVER "
     f"touch the wall again. They never press into it, never make contact with "
     f"the rock, and never leave any new mark of any kind: no second pair of "
     f"handprints ever appears, no extra prints, no additional marks. Nothing is "
     f"added to the wall at any point — the two prints that are there at the "
     f"start are the only two prints that ever exist. Quiet and reverent. This "
     f"is the film's central image. {STATIC} {NOSOUND} {NEG}",
     ["may_sapien", "ollie_sapien", "loc_cave"]),

    # ================= VERSE 2 =================
    # Six fingers read as an AI hand glitch, not a gag — it's a THIRD ARM now.
    # And the clay must look SCULPTED (thumbprints, cracks) or the model just
    # paints a person grey. The "featureless statue" line is an nsfw guard: bare
    # clay torsos are exactly the kind of thing that tripped the binary stars.
    ("s20_clay", 9,
     f"Two half-formed animate SCULPTURES of wet river clay sit in a muddy "
     f"riverbank sculpting THEMSELVES into shape with their own hands, "
     f"smoothing their own faces and shoulders. They are made ENTIRELY of clay "
     f"— lumpy, hand-built, gouged with deep THUMBPRINTS and finger-drag marks, "
     f"cracked and flaking, dull matte wet-clay surfaces, with NO human skin "
     f"anywhere: living clay statues, not people covered in mud, not body "
     f"paint. Their clay bodies are smooth, blank and featureless like "
     f"unfinished statues, with no anatomical detail of any kind — as plain as "
     f"a lump of pottery. The figure on the LEFT is warm red-ochre clay and is "
     f"unmistakably a WOMAN — a female clay figure with a woman's face, a "
     f"woman's build and long sculpted clay hair. The figure on the RIGHT is "
     f"blue-grey clay and is unmistakably a MAN. The blue-grey MAN pauses, "
     f"looks down at himself, and discovers he has accidentally sculpted "
     f"himself a whole THIRD ARM sprouting from the side of his ribs. He lifts "
     f"it and WAVES with the extra arm, beaming with enormous pride. The "
     f"red-ochre WOMAN laughs helplessly, considers it, then reaches into her "
     f"own clay side and pulls out a THIRD ARM of her own to match him, and "
     f"waves back with it. Both are delighted. They are the ONLY two figures in "
     f"the frame. "
     f"{STATIC} {PAIRC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    ("s21_fire", 10,
     f"Night, 40,000 years ago, outside a cave. {W['ollie_sapien']} crouches "
     f"over a small pile of tinder, striking at it clumsily with his badly-made "
     f"spear, getting nowhere; a rabbit sits a few feet away watching him, "
     f"entirely unbothered and unafraid. {W['may_sapien']} kneels beside him "
     f"with her arms full of gathered berries and roots, extremely smug. Then "
     f"the tinder catches — a real flame leaps up — and he rocks back, "
     f"absolutely amazed at himself. The new firelight comes up onto BOTH their "
     f"faces at once and they turn to look at each other, lit and grinning. "
     f"They are the ONLY two people in the frame. {STATIC} {NOSOUND} {NEG}",
     ["may_sapien", "ollie_sapien", "loc_cave"]),

    ("s22_fire_foreheads", 9,
     f"{W['may_sapien']} and {W['ollie_sapien']} sit forehead to forehead in "
     f"firelight, eyes closed, lit warm orange from below, breathing together. "
     f"The camera pushes in slowly. Above them, real glowing embers lift off "
     f"the fire and rise into the black night sky, and as they rise the highest "
     f"embers become real distant STARS, indistinguishable from the starfield — "
     f"two of them burning brighter than the rest, one warm coral-orange and "
     f"one deep teal-blue, orbiting each other. The stars are soft points of "
     f"real light, never cartoon star shapes or graphics. They are the ONLY two "
     f"people in the frame. {PAIRC} {NOSOUND} {NEG}",
     ["may_sapien", "ollie_sapien"]),

    # ================= CHORUS 2 =================
    ("s23_neolithic", 7,
     f"Two Neolithic farmers — the same two faces as the reference images, she "
     f"in a rust-orange woven wrap, he in a teal-grey woven wrap — kneel in a "
     f"freshly-turned furrow at golden hour, pushing seeds into the soil with "
     f"their thumbs. BOTH ARE LAUGHING — a happy, playful, affectionate squabble "
     f"between two people who adore each other, never a real argument and never "
     f"a scolding. She looks over at his row, bursts out laughing at his "
     f"terrible spacing, points at it, and reaches over to fix it, beaming, her "
     f"enormous grin fully visible. He laughs back, mock-protesting, entirely "
     f"charmed. Neither is cross, stern or unhappy at any point. They are the ONLY two people in the frame. "
     f"{STATIC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    ("s24_pot", 6,
     f"Extreme close-up on the curved painted surface of an ancient terracotta "
     f"pot, museum-lit. Two simple painted stick-like human figures stand side "
     f"by side on the curve of the pot — one painted in warm ochre-orange, one "
     f"in teal-grey slip. The two PAINTED FIGURES slowly turn to face each "
     f"other, still flat, still painted onto the curve of the clay, and lean in "
     f"until their foreheads touch. Nothing else moves; the pot itself is "
     f"perfectly still. {STATIC} {PAIRC} {NOSOUND} {NEG}",
     []),

    ("s25_medieval", 6,
     f"A rowdy medieval village festival at dusk — bonfire, fiddler, hay, "
     f"lanterns, villagers dancing a circle dance. At the centre, a woman and a "
     f"man with exactly the same faces as the reference images — she in a "
     f"coral-orange kirtle, he in a teal-blue tunic — dance badly and joyously, "
     f"completely out of step with the rest of the circle, doing recognisably "
     f"the same terrible swaying dance from the kitchen. They spin, misjudge "
     f"it, laugh, and rest their foreheads together. {NOSOUND} {NEG}",
     ["may", "ollie"]),

    ("s26_victorian", 6,
     f"An 1880s photographic portrait studio. A woman and a man with exactly "
     f"the same faces as the reference images — she in a high-necked "
     f"rust-orange Victorian dress, he in a teal-grey frock coat and spectacles "
     f"— sit rigidly for a long exposure, trying very hard to be solemn. They "
     f"hold it. Her mouth twitches. He glances at her. Both of them completely "
     f"lose it and dissolve into helpless laughter, ruining the exposure, she "
     f"putting a hand over her face. The plate camera does not move. They are "
     f"the ONLY two people in the frame. {STATIC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    ("s27_fifties_kitchen", 7,
     f"A cheerful 1950s kitchen — formica, pastel cabinets, chrome kettle, "
     f"gingham curtains. A woman and a man with exactly the same faces as the "
     f"reference images — she in a coral-orange fifties housedress, he in a "
     f"teal-blue short-sleeved shirt — sway together in the same terrible "
     f"dance, foreheads touching. The camera dollies slowly and continuously "
     f"forward toward them, and as it moves, the kitchen around them TRANSFORMS "
     f"seamlessly, without a cut, into their shabby present-day kitchen — "
     f"pastel cabinets becoming worn wood, chrome becoming the old kettle, "
     f"gingham becoming the blue night window — and the couple become "
     f"{W['may']} and {W['ollie']} in their modern clothes, still dancing, "
     f"still forehead to forehead. One continuous move, no cut. {NOSOUND} "
     f"{NEG}",
     ["may", "ollie", "loc_kitchen"]),

    ("s28_flatpack", 6,
     f"{W['ollie']} sits defeated on the living-room floor in the wreckage of a "
     f"flat-pack bookshelf, an allen key in his mouth, the instructions upside "
     f"down, far too many leftover screws in a neat sad row beside him. He "
     f"turns the instructions the right way up, stares at them, and gives up. "
     f"{W['may']} is perched on the one shelf he successfully built; she pats "
     f"it twice, encouragingly. They are the ONLY two people in the frame. "
     f"{STATIC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    ("s29_proposal", 6,
     f"{W['may']} drops to one knee on the yellow kitchen lino and holds up a "
     f"paperclip bent into a ring, grinning her enormous grin. {W['ollie']} "
     f"claps both hands over his mouth, crying and nodding helplessly, glasses "
     f"fogging. He sinks down to the floor with her. She pushes the paperclip "
     f"onto his finger. They are the ONLY two people in the frame. {STATIC} "
     f"{FRAME_LOCK} {NOSOUND} {NEG}",
     ["may", "ollie", "loc_kitchen"]),

    ("s30_wedding", 7,
     f"A very small, very cheap, very happy wedding in a rented community hall "
     f"— paper garland, folding chairs, six guests, a supermarket cake. "
     f"{FACE['may']} — THE BRIDE, wearing a simple slightly-too-big second-hand "
     f"IVORY WEDDING DRESS with a coral-orange ribbon sash and coral flowers in "
     f"her hair, absolutely NOT a cardigan and NOT jeans — and {FACE['ollie']} "
     f"— THE GROOM, in an ill-fitting teal-blue SUIT — stand together as the "
     f"guests throw confetti over them. The confetti flies up, catches a shaft "
     f"of backlight, and hangs and drifts in the air as warm glittering "
     f"particles — exactly the drifting dust of the Big Bang. The couple look "
     f"up at it, then at each other. {STATIC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    # ================= BRIDGE =================
    ("s31_blush", 6,
     f"In the rented wedding hall, confetti still settling, {FACE['may']} — "
     f"still in her ivory WEDDING DRESS with the coral ribbon sash, not a "
     f"cardigan — and {FACE['ollie']}, still in his teal-blue wedding SUIT, "
     f"turn and look at each other across a small gap. A beat "
     f"passes. Both of them go completely pink, bite back enormous smiles, and "
     f"look away from each other, bashful and delighted — then each sneaks a "
     f"look back at the same moment and catches the other doing it. Sweetly, "
     f"hilariously coy. They are the ONLY two people in focus in the frame. "
     f"{STATIC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    # 6x nsfw across two wordings on the original (a newborn's hand gripping his
    # finger). Infant imagery is an IMAGE-level trigger; rewording cannot fix it.
    # Changed WHAT HAPPENS: the baby is off-screen and we play the reaction.
    ("s31b_babyhand", 7,
     f"A dark bedroom at night, lit by one small warm lamp. {W['may']} and "
     f"{W['ollie']} stand pressed together leaning over the side of a simple "
     f"wooden cot, looking DOWN into it at something the camera never sees — "
     f"the inside of the cot stays hidden below the frame line the entire time. "
     f"Their faces are lit warmly from below. She slowly presses one hand over "
     f"her mouth. He is crying and smiling at once, glasses fogged, and puts an "
     f"arm around her and pulls her in. She leans her head onto his shoulder "
     f"without ever taking her eyes off the cot. Neither of them looks away and "
     f"neither of them looks at the camera. We never see what they are looking "
     f"at. They are the ONLY two people in the frame. Very slow, very quiet. "
     f"{STATIC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    ("s32_toddler_chaos", 10,
     f"Total domestic chaos in a cluttered family home at breakfast. The "
     f"four-year-old girl from the reference image — wild dark curly hair, "
     f"mustard-yellow t-shirt, ordinary spotty leggings, ONE welly boot, "
     f"dressed completely normally with no nappy and no costume — sprints "
     f"through the room at full speed, shrieking with joy. {W['may']} and "
     f"{W['ollie']} both lunge after her and both miss. A cereal bowl goes "
     f"over, Cheerios everywhere, the dog joins in. Everyone is extremely "
     f"happy. Handheld camera, following the chaos — the ONLY handheld shot in "
     f"the film. {NOSOUND} {NEG}",
     ["may", "ollie", "kid"]),

    ("s33_family_tree", 6,
     f"A small back garden at golden hour. A big old tree with dozens of framed "
     f"family photographs hanging from its branches on strings, turning gently "
     f"in the breeze. Children climb in the branches among the photographs. "
     f"Underneath, {W['may']} and {W['ollie']}, arms around each other, look up "
     f"at it. A literal family tree. {STATIC} {NOSOUND} {NEG}",
     ["may", "ollie"]),

    # ================= THE MUSEUM =================
    ("s34_museum_enter", 8,
     f"The great hall of an old natural history museum after closing time — "
     f"whale skeleton overhead, glowing diorama cases along both walls, warm "
     f"low light, dust in the air. {W['may']} and {W['ollie']}, a little older "
     f"now, walk in hand in hand through the enormous doors, and their "
     f"four-year-old daughter runs on ahead of them across the polished floor. "
     f"The camera holds as they come toward it. They are the ONLY people in the "
     f"museum — it is otherwise completely EMPTY, no other visitors, no staff, "
     f"no other family. {STATIC} {NOSOUND} {NEG}",
     ["may", "ollie", "kid", "loc_museum"]),

    ("s35_dioramas", 8,
     f"Slow continuous lateral dolly down a corridor of glowing "
     f"natural-history diorama cases in a dark empty museum. Inside the cases, "
     f"lit warmly and perfectly still: two lobe-finned fish with their snouts "
     f"nudged together; two early primates hanging upside-down holding hands, "
     f"foreheads bonked; two shaggy fur-covered early hominids (primate animals "
     f"with thick body hair, one rust-orange furred and one blue-grey furred) "
     f"standing forehead to forehead in tall "
     f"grass — EXACTLY the pairs from the reference images. EVERY case in the "
     f"corridor without exception holds a COUPLE — two animals of the same "
     f"species, one warm coral-orange and one cool teal-blue, posed touching. "
     f"Not one case holds a lone animal or a plain drab-coloured animal. "
     f"Every diorama is a PAIR, frozen mid-affection, as if watching. The "
     f"animals in the cases never move. Walking past them down the "
     f"corridor, small in frame, are {W['may']}, {W['ollie']} and their "
     f"daughter, and NOBODY ELSE — no other visitors, no staff, no other "
     f"family. The creatures in the cases do not move. {NOSOUND} {NEG}",
     ["pair_fish", "pair_monkeys", "pair_hominids", "may", "ollie", "kid",
      "loc_museum"]),

    ("s36_glass_handprints", 8,
     f"A lit glass exhibit case in the dark museum holds a section of cave wall "
     f"bearing TWO RED-OCHRE HANDPRINTS side by side, one larger and one "
     f"smaller — the same two handprints made 40,000 years earlier. {W['may']} "
     f"slowly raises her hand and places it flat on the outside of the glass, "
     f"exactly over the smaller print. A beat later {W['ollie']} raises his "
     f"hand and places it flat on the glass over the larger one. Neither of "
     f"them looks at the other. Neither of them says anything. They just stand "
     f"there with their hands on the glass. Their faint reflections hang in "
     f"it. They are the ONLY two people in the frame. {STATIC} — the camera "
     f"must NOT move at all. {NOSOUND} {NEG}",
     ["may", "ollie", "loc_museum"]),

    ("s37_dome_to_stars", 8,
     f"Looking straight up inside the museum, the camera cranes smoothly and "
     f"continuously upward — past the suspended whale skeleton, up through the "
     f"great vaulted glass-and-iron dome — and out through the glass into an "
     f"impossibly deep starfield, where TWO stars burn brighter than all the "
     f"rest, one warm coral-orange and one deep teal-blue, still orbiting each "
     f"other exactly as they did at the beginning of the universe. Far below, "
     f"two tiny figures. One continuous rising move, no cut. {PAIRC} {NOSOUND} "
     f"{NEG}",
     ["loc_museum"]),

    # ================= FINAL =================
    ("s38_old_dance", 6,
     f"The same kitchen, the same lino, the same kettle, the same lamp, the "
     f"same camera position as the opening of the film — fifty years later. "
     f"{W['may_old']} and {W['ollie_old']} hold each other and sway in the "
     f"middle of the floor, badly and out of time, exactly the same terrible "
     f"dance as the young couple, and rest their foreheads together with their "
     f"eyes closed. A small grandchild watches from the doorway, deeply "
     f"unimpressed. {STATIC} {FRAME_LOCK} {NOSOUND} {NEG}",
     ["may_old", "ollie_old", "loc_kitchen"]),

    ("s39_fridge_handprints", 9,
     f"{W['may_old']} and {W['ollie_old']} stand forehead to forehead in the "
     f"kitchen, eyes closed, holding each other's forearms, swaying very "
     f"slightly. Behind them on the crowded fridge door, among the postcards "
     f"and magnets, is a child's painting of TWO TINY CHILD'S HANDPRINTS in "
     f"poster paint side by side — one coral-orange, one teal-blue. They are "
     f"unmistakably a very young child's hands: very small, chubby, with short "
     f"stubby little fingers — a toddler's hands, NOT adult hands. Clearly "
     f"visible over their shoulders. The camera pulls back slowly and steadily, out "
     f"through the kitchen window, leaving them dancing inside the lit frame of "
     f"the window. {NOSOUND} {NEG}",
     ["may_old", "ollie_old", "loc_kitchen"]),

    ("s40_pullback", 10,
     f"The clip OPENS EXACTLY ON THE START IMAGE and never cuts: we are OUTSIDE "
     f"the house at night, looking at it from the air, with one small lit "
     f"kitchen window glowing in the dark. Framed inside that window from the "
     f"VERY FIRST FRAME are {W['may_old']} and {W['ollie_old']}, forehead to "
     f"forehead, slowly swaying. They are ALREADY THERE in frame one and they "
     f"REMAIN CONTINUOUSLY VISIBLE in the window for as long as the window is "
     f"big enough to see them: they NEVER flicker, NEVER fade out, NEVER "
     f"disappear and NEVER pop into existence, and no empty kitchen is ever "
     f"shown without them. The camera never goes inside the house. From that "
     f"first frame the camera pulls back in ONE continuous accelerating move, "
     f"straight up and away: the house shrinks, then the dark street, then the "
     f"sleeping town spread out below, then the coastline, the lights of the "
     f"land dwindling. The single lit window stays in the exact centre of frame "
     f"the whole way, getting smaller and smaller, the only warm light in an "
     f"enormous dark. One unbroken move, never cutting, never stopping, never "
     f"reversing. {NOSOUND} {NEG}",
     ["may_old", "ollie_old", "loc_kitchen"]),

    ("s40b_earth", 6,
     f"The planet Earth, very far away in deep space — small, warm and alone, "
     f"exactly as it appears in the start image, a single soft point of "
     f"amber-blue light in an enormous painterly dark. THE SHOT IS A HOLD. The "
     f"camera does not move at all: no zoom, no push, no pull-back, no drift, no "
     f"rotation. The planet stays in exactly the same position and at exactly "
     f"the SAME SIZE in the frame for the entire clip — it never grows, never "
     f"approaches, never fills the frame, and never becomes large or detailed. "
     f"It remains small and distant throughout. There is only ONE planet in this "
     f"clip: no second Earth, no other planet, no new world ever appears, and "
     f"the image never dissolves, morphs or transitions into anything else. The "
     f"ONLY movement in the entire frame is faint dust and distant stars "
     f"drifting slowly past. The picture at the end of the clip looks the same "
     f"as the picture at the start. Calm, still, final. {STATIC} {NOSOUND} "
     f"{NEG}",
     []),]
