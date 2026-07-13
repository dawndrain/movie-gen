"""Start frames for HOME SAPIEN — one per shot in STORYBOARD.md.

(name, aspect, prompt, [anchor refs])
The start frame dominates the clip: wardrobe, set, staging and framing come
from here more than from the video prompt. Every frame is 16:9.
"""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("locks", Path(__file__).parent / "locks.py")
_locks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_locks)
STYLE, COSMIC, PAIR, W = _locks.STYLE, _locks.COSMIC, _locks.PAIR, _locks.W
CREATURE = _locks.CREATURE
FACE = _locks.FACE          # identity WITHOUT wardrobe — use for costume shots

FRAMES = [
    # ================= COLD OPEN =================
    ("s01_kitchen_dance", "16:9",
     f"Wide locked-off shot of {W['kitchen']}. {W['may']} is alone, barefoot "
     f"on the lino, caught mid-way through a private, deeply silly little "
     f"dance while she waits for the kettle. Steam rising. She thinks nobody "
     f"can see her. She is the ONLY person in the frame — the kitchen is "
     f"otherwise completely EMPTY, no other people. {STYLE}",
     ["may", "loc_kitchen"]),

    # A STILL and a CLIP want opposite frames here, and the film is an animatic.
    #
    # For VIDEO: he must start somewhere physical, or Seedance invents his
    # entrance — it materialised him out of the corner and walked him through the
    # table. So the video version puts him in the doorway with a clear floor path
    # (kept at frames_prev/s02_two_dance_doorway.png, and it shot correctly).
    #
    # For a STILL held for 6 seconds, that same frame reads as her waiting alone
    # for him for six seconds. A held frame has no "later" — whatever it shows,
    # it shows for the whole window. So the animatic wants the END of the beat,
    # not the start of it: they are ALREADY embracing, foreheads together.
    ("s02_two_dance", "16:9",
     f"Wide locked-off shot of {W['kitchen']}. {W['may']} and {W['ollie']} "
     f"hold each other and sway in the middle of the kitchen floor, badly and "
     f"completely out of time with each other, foreheads touching, both with "
     f"their eyes closed. He is half asleep. They are the ONLY two people in "
     f"the frame — the kitchen is otherwise completely EMPTY. {STYLE}",
     ["may", "ollie", "loc_kitchen"]),

    ("s03_eye", "16:9",
     f"Extreme close-up of one eye of {W['may']}, laughing, crow's feet "
     f"crinkled. Reflected in her iris, tiny and clear, is the deep blue "
     f"night window of the kitchen — and within the reflection the blue is "
     f"just beginning to break apart into a field of stars. Warm lamplight on "
     f"her skin, freckles visible. {STYLE}",
     ["may"]),

    # ================= VERSE 1 =================
    ("s04_bigbang", "16:9",
     f"The instant after the Big Bang, rendered small and intimate and "
     f"handmade: a bloom of white light in an empty dark, warm dust and "
     f"glitter unfurling out of it like paint dropped in water. Out of the "
     f"centre, TWO tiny bright sparks — one warm coral-orange, one cool "
     f"teal-blue — are already spinning away together, orbiting one another. "
     f"They are the only two distinct points of light in the frame. {COSMIC}",
     []),

    ("s05_binary_stars", "16:9",
     f"Two stars in a close binary orbit, hanging in a soft painterly nebula "
     f"— one warm coral-orange, one deep teal-blue, so close they almost "
     f"touch, leaning into one another. Nothing else in the frame but dust "
     f"and dark. Tender, like a forehead touch at cosmic scale. {COSMIC}",
     []),

    ("s06_tidepool", "16:9",
     f"Extreme macro shot into a tiny tidepool the size of a soup bowl, held "
     f"in black volcanic rock, four billion years ago. Suspended in the murky "
     f"green water are TWO glowing single-celled blobs — one warm coral-"
     f"orange, one cool teal-blue — wobbling toward each other, about to "
     f"bump. They are the ONLY two organisms in the frame. Faintly, absurdly "
     f"expressive. Steam and early-Earth light above the water. {STYLE}",
     []),

    ("s07_waiting", "16:9",
     f"Locked-off wide shot: one small REAL LIVING HALF-EVOLVED AMPHIBIOUS "
     f"CREATURE — a proto-tetrapod, like a Tiktaalik: a fish that has just "
     f"grown the beginnings of LEGS. It has four stubby proto-limbs with tiny "
     f"webbed toes, a flat wide head with eyes on top, wet mottled skin and a "
     f"finned tail still trailing in the water. It has hauled itself half out "
     f"of the shallows onto a wet black rock at the edge of a primordial sea — "
     f"its front legs up on the rock, its tail still in the water — and it is "
     f"propped up on its two little front legs, chin resting on them, WAITING, "
     f"gazing out to sea with an expression of infinite deadpan patience, as "
     f"though waiting for someone who is running extremely late. It is warm "
     f"coral-orange. It is CLEARLY a four-legged land-crawling creature, NOT a "
     f"plain fish. It is the ONLY creature in the frame. Behind it the sky and "
     f"sea are streaked and blurred with the motion of geological time — "
     f"racing tides, streaking clouds, ice — while it stays perfectly still "
     f"and razor sharp. {CREATURE}",
     []),

    ("s08_side_by_side", "16:9",
     f"A single procession of REAL LIVING ANIMALS walking left to right along "
     f"one dirt trail through golden savanna — and every single stage of the "
     f"procession is a COUPLE, two animals walking SHOULDER TO SHOULDER, side "
     f"by side, keeping pace with each other. One of each couple is warm "
     f"coral-orange and the other is cool teal-blue, and the two animals in "
     f"each couple are always the SAME SPECIES as each other. Reading from the "
     f"back of the line to the front, the couples evolve: a coral frog beside "
     f"a teal frog, then a coral lizard beside a teal lizard, then a coral "
     f"meerkat-like mammal beside a teal one, and at the front of the "
     f"procession, closest to camera, a coral monkey beside a teal monkey, "
     f"walking together. Every couple walks the SAME WAY, left to right, in "
     f"profile — no animal ever faces another animal, nobody walks toward "
     f"anybody. The pairs are simply travelling together, each beside its "
     f"partner. ONE single continuous photograph of one real landscape: one "
     f"horizon, one sky, one light — absolutely NOT a split screen, NOT "
     f"stacked bands, NOT a divided image. No aquariums, no tanks, no carts, "
     f"no man-made objects of any kind. Warm golden light, long lens, shallow "
     f"depth of field. Every animal is a REAL PHOTOGRAPHED ANIMAL. "
     f"{CREATURE}",
     []),

    ("s09a_fish", "16:9",
     f"Two small prehistoric lobe-finned fish hanging side by side in green "
     f"underwater light, EXACTLY the same two fish as the reference image — "
     f"one warm coral-orange, one deep teal-blue — their stubby fins touching "
     f"and their blunt snouts nudged together. They are the ONLY two "
     f"creatures in the frame. {STYLE}",
     ["pair_fish"]),

    ("s09b_monkeys", "16:9",
     f"Two small early primates, EXACTLY the same two animals as the "
     f"reference image, hanging upside-down by their tails from the same "
     f"jungle branch in dappled golden light, holding hands, foreheads bonked "
     f"together, blissful. One has warm coral-orange fur, the other cool "
     f"teal-grey fur. They are the ONLY two creatures in the frame. {STYLE}",
     ["pair_monkeys"]),

    ("s10_hominids", "16:9",
     f"Two early hominids, EXACTLY the same two as the reference image — "
     f"small, upright, covered in natural body hair — standing forehead to "
     f"forehead in silhouette on an African savanna at dawn, holding each "
     f"other's forearms, tender and completely still. They wear NO CLOTHING "
     f"and carry nothing — no hides, no furs, no cloth, no tools: they are "
     f"naked, hairy animals, millions of years before clothing existed. The "
     f"colour pairing is in their natural FUR: one warm rust-orange, one cool "
     f"blue-grey. They are backlit into near-silhouette by an enormous golden "
     f"sun low on the horizon, so they read as two shapes in the grass — "
     f"dignified, tender, unsensational. Tall dry grass. They are the ONLY two "
     f"figures in the frame. {STYLE}",
     ["pair_hominids", "loc_savanna"]),

    # ================= CHORUS 1 =================
    ("s11_flower_cave", "16:9",
     f"TIGHT MEDIUM TWO-SHOT at the mouth of a cave, forty thousand years ago, "
     f"warm firelight. The two of them are seen IN PROFILE, FACING EACH OTHER "
     f"across the frame — she on the LEFT facing RIGHT, he on the RIGHT facing "
     f"LEFT. NEITHER of them looks at the camera at any point; they look only "
     f"at each other. {W['may_sapien']} holds out a scrappy little wildflower "
     f"to {W['ollie_sapien']}, her arm extended across the gap between them, "
     f"beaming at him with total confidence. He stares at the flower, "
     f"completely stunned. They fill the frame from the waist up. They are the "
     f"ONLY two people in the frame — the cave is otherwise EMPTY, no other "
     f"people. {STYLE}",
     ["may_sapien", "ollie_sapien", "loc_cave"]),

    ("s12_flower_kitchen", "16:9",
     f"TIGHT MEDIUM TWO-SHOT — the two of them fill the frame from the waist "
     f"up, she on the left facing right, he on the right facing left, exactly "
     f"the framing and lens of a firelit cave-mouth shot this is match-cutting "
     f"from. {W['may']} holds out a sad cellophane-wrapped bunch of "
     f"petrol-station flowers to {W['ollie']} with total, beaming confidence "
     f"— the same enormous grin, the same outstretched arm, the same pose as "
     f"the cave. He is completely stunned. Behind them, softly out of focus, "
     f"{W['kitchen']}. They are the ONLY two people in the frame. {STYLE}",
     ["may", "ollie", "loc_kitchen"]),

    ("s13_hold_cave", "16:9",
     f"Wide shot: {W['may_sapien']} and {W['ollie_sapien']} curled up "
     f"together asleep in furs at the mouth of a cave, holding each other, "
     f"the small fire burned down to embers — and above and beyond them an "
     f"ENORMOUS sky of unpolluted stars filling the top half of the frame. "
     f"They are the ONLY two people in the frame. {STYLE}",
     ["may_sapien", "ollie_sapien", "loc_cave"]),

    ("s14_hold_couch", "16:9",
     f"Wide shot, EXACTLY the same framing and composition as a cave-mouth "
     f"shot it is match-cutting from: {W['may']} and {W['ollie']} curled up "
     f"together asleep on a sagging second-hand sofa under a knitted blanket, "
     f"a muted television glowing instead of embers — and through a big "
     f"window above them, an enormous sky of stars filling the top half of "
     f"the frame. They are the ONLY two people in the frame. {STYLE}",
     ["may", "ollie"]),

    ("s15_morph_walk", "16:9",
     f"Lateral tracking composition: a procession of couples walking left to "
     f"right across the frame, hand in hand, never letting go, evolving as "
     f"they walk. The order runs strictly OLDEST ON THE LEFT to NEWEST ON THE "
     f"RIGHT, exactly like the classic March of Progress illustration: at the "
     f"far LEFT of the frame, two stooped apelike hominids; then two upright "
     f"fur-clad ice-age humans; then two medieval peasants; and at the far "
     f"RIGHT of the frame, leading the procession and fully in focus, the "
     f"present-day couple — {W['may']} and {W['ollie']}. The figures get more "
     f"modern and more upright as the eye moves RIGHT. The earlier couples "
     f"behind them are soft and fading like a memory. One of each couple "
     f"always wears warm coral-orange, the other cool teal-blue. Warm "
     f"painterly light, plain soft background. {STYLE}",
     ["may", "ollie"]),

    ("s16_groceries", "16:9",
     f"Locked-off wide shot of {W['kitchen']}. {W['ollie']} is standing in "
     f"the middle of the kitchen absolutely LOADED DOWN with shopping — eight "
     f"heavy plastic grocery bags hanging off both arms right up to the "
     f"shoulders, two more gripped in his teeth, a watermelon wedged under "
     f"one elbow, a baguette under his chin — because he refused to make two "
     f"trips. One bag has split and oranges are bouncing across the yellow "
     f"lino. His glasses are askew. He is frozen, wide-eyed, unable to move. "
     f"{W['may']} sits on the kitchen counter with a mug, watching, absolutely "
     f"DELIGHTED, helping him not at all. They are the ONLY two people in the "
     f"frame. {STYLE}",
     ["may", "ollie", "loc_kitchen"]),

    ("s17_diorama_dance", "16:9",
     f"Wide shot inside a natural-history-museum diorama case: a painted "
     f"ice-age backdrop, a taxidermy mammoth, plastic ferns, fake snow — and "
     f"standing in the middle of it, completely out of place and not caring, "
     f"{W['may']} and {W['ollie']} in their ordinary modern clothes, doing "
     f"their terrible swaying kitchen dance, foreheads touching. They are the "
     f"ONLY two people in the frame. Warm museum spotlight. {STYLE}",
     ["may", "ollie"]),

    ("s18_tree_of_life", "16:9",
     f"Very wide shot at dusk: two tiny human silhouettes standing together "
     f"on a bare hill at the bottom of the frame — and filling the entire sky "
     f"above them, drawn in delicate glowing constellation-lines from "
     f"horizon to horizon, the branching TREE OF LIFE: a great forking "
     f"evolutionary tree of stars. On every single fork of the tree sit TWO "
     f"small lights, one warm coral-orange and one cool teal-blue, side by "
     f"side. Awe, but gentle and handmade. {COSMIC}",
     []),

    # ================= INSTRUMENTAL =================
    # Keeps the original composition (both hands in frame, intimate) but lifts them
    # a few centimetres OFF the rock, so the finished prints are visible underneath.
    # Hands pressed flat leave nothing to see but a red patch; hands fully gone
    # loses the intimacy. This is the beat in between, and it's the legible one.
    #
    # Both hands are grown-ups — it pays off at 3:22, where the two of them each
    # put a hand on the museum glass over one print.
    #
    # NB: do NOT try to fix this frame with edit_frame.py using an older take that
    # contains a small hand as the ref — three rewordings all came back `nsfw`.
    # The classifier objects to the INPUT IMAGE, not the prompt. Regenerate fresh.
    ("s19_handprints", "16:9",
     f"Locked-off medium close-up on a rough pale cave wall in warm firelight. "
     f"Two hands have just pressed into wet red-ochre paint and are LIFTING "
     f"AWAY from the rock — they hover a few centimetres off the wall, fingers "
     f"still splayed in the same shape, palms glistening with wet ochre, "
     f"directly above the marks they have just made. BENEATH each hand, now "
     f"uncovered and clearly visible, is a CRISP COMPLETE RED-OCHRE HANDPRINT: "
     f"a sharp, high-contrast ochre silhouette with a distinct palm and five "
     f"clearly separated FINGERS, with clean bare pale rock showing in the gaps "
     f"between every finger and a thumb set apart at an angle. The prints are "
     f"unmistakably HANDS — never blobs, never smears, never a shapeless red "
     f"patch. Both hands belong to grown-ups: the one on the LEFT is a woman's, "
     f"with long slim tapered fingers, a narrow palm and a slender wrist "
     f"wearing a bone-bead bracelet; the one on the RIGHT is a man's, larger "
     f"and broader. Their fingers are long and tapered, never short, never "
     f"rounded, never stubby. Deep shadow, flickering firelight, texture of "
     f"stone and wet pigment. Quiet and reverent. {STYLE}",
     ["may_sapien", "ollie_sapien", "loc_cave"]),

    # ================= VERSE 2 =================
    # Gag v3. The mutation has to be (a) unmistakably deliberate and (b) something
    # the models can actually DRAW:
    #   v1 SIXTH FINGER  -> read as a stock AI hand glitch, not a joke.
    #   v2 THIRD ARM     -> neither Nano Banana nor Seedance could hold it. An arm
    #                       needs a shoulder and there is nowhere to put a third,
    #                       so it kept collapsing back into two ordinary arms.
    #   v3 TAIL          -> trivial to render, impossible to misread, and a better
    #                       evolution joke anyway.
    # Also: "figures made of clay" gets read as people wearing body paint, so they
    # must be described as SCULPTURES — lumpy, cracked, thumbprinted, no skin.
    ("s20_clay", "16:9",
     f"Two crude, half-finished SCULPTURES made of wet river clay sit in a "
     f"muddy riverbank, ALIVE, sculpting THEMSELVES into shape with their own "
     f"hands. They are made ENTIRELY of clay all the way through — lumpy, "
     f"unfinished, visibly hand-built, with deep THUMBPRINTS and finger-drag "
     f"marks gouged all over them, cracks, dents, loose crumbs of clay falling "
     f"off, dull matte wet-clay surfaces, coils and seams where the clay was "
     f"pressed together, and rough unfinished stumps where limbs are still "
     f"being formed. They have NO human skin anywhere: this is NOT a person "
     f"covered in mud, NOT body paint, NOT a painted human — they are literal "
     f"animate clay statues, like living pottery. The figure on the LEFT is "
     f"warm red-ochre clay and is unmistakably a WOMAN, with a woman's clay "
     f"face and build and long sculpted clay hair. The figure on the RIGHT is "
     f"blue-grey clay and is unmistakably a MAN. Both wear crude clay smocks "
     f"covering their torsos, moulded from the same material. The blue-grey MAN "
     f"has accidentally sculpted himself a LONG CLAY TAIL — a thick, tapering, "
     f"obviously animal-like tail of blue-grey clay, as long as his arm, curling "
     f"out from the base of his spine and lying along the mud beside him, "
     f"completely and clearly visible. He is twisted round looking at it, "
     f"holding it up proudly in both hands to show her, beaming. The red-ochre "
     f"WOMAN is laughing helplessly, and she has just pulled a matching LONG "
     f"RED-OCHRE CLAY TAIL out of her own back to match him, and holds it up "
     f"beside his. Two clay people sitting in the mud, delightedly comparing "
     f"their brand new tails. Both tails are large and unmissable. They are the "
     f"ONLY two figures in the frame. Whimsical, tactile, warm. {STYLE}",
     ["may", "ollie"]),

    ("s21_fire", "16:9",
     f"Night, forty thousand years ago, outside a cave. {W['may_sapien']} "
     f"kneels with her arms full of gathered berries and roots, extremely "
     f"smug. Beside her {W['ollie_sapien']} crouches over a small fire he has "
     f"just successfully lit, holding a badly-made spear, absolutely amazed "
     f"at himself — and the new firelight is coming up onto BOTH their faces "
     f"for the first time. A rabbit sits nearby, entirely unbothered by him. "
     f"They are the ONLY two people in the frame. {STYLE}",
     ["may_sapien", "ollie_sapien", "loc_cave"]),

    ("s22_fire_foreheads", "16:9",
     f"Close two-shot, firelit: {W['may_sapien']} and {W['ollie_sapien']} "
     f"forehead to forehead, eyes closed, lit from below in warm orange. "
     f"Above them, real glowing embers lift off the fire and rise into the "
     f"black night sky — and the highest embers become REAL DISTANT STARS, "
     f"indistinguishable from the real starfield above, two of them burning "
     f"brighter than the rest, one warm coral-orange and one deep teal-blue. "
     f"The stars are soft points of real light — absolutely NOT cartoon "
     f"five-pointed star shapes, NOT icons, NOT graphics, NOT sparkles. They "
     f"are the ONLY two people in the frame. {STYLE}",
     ["may_sapien", "ollie_sapien"]),

    # ================= CHORUS 2 =================
    ("s23_neolithic", "16:9",
     f"Two Neolithic farmers kneeling in a freshly-turned furrow in a small "
     f"field at golden hour, pushing seeds into the soil with their thumbs. "
     f"They have EXACTLY the same faces as the two people in the reference "
     f"images. She wears a rust-orange woven wrap, he wears a teal-grey woven "
     f"wrap. BOTH OF THEM ARE LAUGHING — this is a happy, playful, affectionate "
     f"squabble between two people who adore each other, not a real argument "
     f"and not a scolding. SHE IS BEAMING, mouth open in a big delighted laugh, "
     f"her enormous uncontrollable grin fully visible, as she reaches over to "
     f"move one of his badly-spaced seeds; he is laughing back at her, "
     f"mock-protesting, entirely charmed. Neither of them is annoyed, cross, "
     f"stern, unimpressed or unhappy — they are both openly happy and warm. "
     f"They are the ONLY two people in the frame. {STYLE}",
     ["may", "ollie"]),

    ("s24_pot", "16:9",
     f"Extreme close-up of the curved painted surface of an ancient terracotta "
     f"pot, museum-lit. On it, painted in black and red-ochre in an ancient "
     f"style, are TWO simple stick-like human figures standing side by side — "
     f"and the two painted figures have turned to FACE EACH OTHER and are "
     f"touching foreheads, still painted-flat, still on the curve of the pot. "
     f"One figure is painted in warm ochre-orange, the other in teal-grey "
     f"slip. Only the pot fills the frame. {STYLE}",
     []),

    ("s25_medieval", "16:9",
     f"A rowdy medieval village festival at dusk — bonfire, a fiddler, hay, "
     f"lanterns, villagers dancing a circle dance. At the centre, badly out "
     f"of step with everyone and enjoying themselves enormously, are a woman "
     f"and a man with EXACTLY the same faces as the two people in the "
     f"reference images: she in a coral-orange woollen kirtle, he in a "
     f"teal-blue tunic, doing what is recognisably the same terrible swaying "
     f"dance. They are the clear focus of the frame. {STYLE}",
     ["may", "ollie"]),

    ("s26_victorian", "16:9",
     f"A Victorian photographic portrait studio, 1880s: a big plate camera on "
     f"a tripod, a painted backdrop, a headrest stand. Seated stiffly for a "
     f"long exposure are a woman and a man with EXACTLY the same faces as the "
     f"two people in the reference images — she in a high-necked rust-orange "
     f"Victorian dress, he in a teal-grey frock coat and spectacles. They are "
     f"supposed to be solemn, and they have completely lost it: both are "
     f"caught mid-laugh, ruining the exposure, she with a hand over her face. "
     f"They are the ONLY two people in the frame. {STYLE}",
     ["may", "ollie"]),

    ("s27_fifties_kitchen", "16:9",
     f"A cheerful 1950s kitchen — formica, pastel cabinets, a chrome kettle, "
     f"gingham curtains. A woman and a man with EXACTLY the same faces as the "
     f"two people in the reference images stand at the counter, she in a "
     f"coral-orange fifties housedress, he in a teal-blue short-sleeved shirt "
     f"— doing the same terrible swaying dance, foreheads touching. The "
     f"camera is beginning a slow dolly forward toward them. They are the "
     f"ONLY two people in the frame. {STYLE}",
     ["may", "ollie"]),

    ("s28_flatpack", "16:9",
     f"Locked-off wide shot of a cluttered modern living room, daytime. "
     f"{W['ollie']} sits defeated on the floor in the wreckage of a flat-pack "
     f"bookshelf — an allen key in his mouth, instructions upside down, far "
     f"too many leftover screws laid out in a neat sad little row. {W['may']} "
     f"is perched on the one shelf he did successfully build, patting it "
     f"encouragingly. They are the ONLY two people in the frame. {STYLE}",
     ["may", "ollie"]),

    ("s29_proposal", "16:9",
     f"Locked-off medium shot of {W['kitchen']}. {W['may']} is down on one "
     f"knee on the yellow lino, holding up a paperclip bent into a ring, "
     f"grinning her enormous grin. {W['ollie']} stands over her with both "
     f"hands over his mouth, crying and nodding, glasses fogged. They are the "
     f"ONLY two people in the frame. {STYLE}",
     ["may", "ollie", "loc_kitchen"]),

    # FACE-only locks here: W[...] would put her back in the cardigan and jeans.
    ("s30_wedding", "16:9",
     f"A very small, very cheap, very happy wedding in a rented community "
     f"hall: a paper garland, folding chairs, six guests, a supermarket cake. "
     f"{FACE['may']} IS THE BRIDE and is WEARING A WEDDING DRESS — a simple, "
     f"slightly-too-big second-hand ivory wedding dress with a coral-orange "
     f"ribbon sash at the waist and a few coral flowers in her dark curly "
     f"hair. She is absolutely NOT wearing a cardigan, NOT wearing a jumper, "
     f"NOT wearing jeans and NOT in everyday clothes — she is in a bridal "
     f"dress, and it is clearly her wedding day. Beside her, {FACE['ollie']} "
     f"is THE GROOM, wearing an ill-fitting second-hand TEAL-BLUE SUIT with a "
     f"crooked tie — not a shirt on its own, an actual suit jacket. They stand "
     f"together in the middle of the hall as the guests throw confetti over "
     f"them — and the confetti, caught in a shaft of backlight, hangs in the "
     f"air as warm glittering drifting particles that look exactly like the "
     f"dust of the Big Bang. {STYLE}",
     ["may", "ollie"]),

    # ================= BRIDGE =================
    # Same wedding, moments later — FACE locks, or she's back in the cardigan.
    ("s31_blush", "16:9",
     f"Medium two-shot in the rented wedding hall, confetti still settling. "
     f"{FACE['may']}, still in her simple ivory second-hand WEDDING DRESS with "
     f"the coral-orange ribbon sash and coral flowers in her hair (no cardigan, "
     f"no jeans), and {FACE['ollie']}, still in his ill-fitting teal-blue "
     f"wedding SUIT, stand facing each other in profile, turned "
     f"toward one another and NOT toward the camera. Both have just gone "
     f"visibly PINK in the cheeks and both have looked bashfully AWAY and "
     f"DOWN at the floor at the same moment, biting back enormous smiles, "
     f"each with a hand half-raised to their own face. Neither is looking at "
     f"the camera; neither is quite looking at the other. Sweetly, "
     f"hilariously coy — the shy beat of two people who have just had the same "
     f"thought. They are the ONLY two people in focus in the frame. {STYLE}",
     ["may", "ollie"]),

    # WAS: an extreme close-up of a newborn's hand gripping his finger. It drew
    # 6 straight nsfw rejections at the VIDEO stage across two very different
    # wordings — infant imagery trips the classifier no matter how tender the
    # shot is, and no rewording fixes an image-level trigger. So the baby moved
    # OFF-SCREEN and we shoot the reaction instead.
    #
    # This is the better shot anyway: the faces carry it, and what they're looking
    # at is left entirely to the audience. The reaction beats the object.
    ("s31b_babyhand", "16:9",
     f"A dark bedroom at night, lit only by one small warm lamp. {W['may']} and "
     f"{W['ollie']} stand pressed together, leaning over the side of a simple "
     f"wooden cot, looking DOWN into it at something we cannot see — the inside "
     f"of the cot is completely hidden from the camera, below the frame line, "
     f"and it is EMPTY of anything visible. Their faces are lit warmly from "
     f"below by the lamp. She has one hand pressed over her mouth. He is "
     f"crying and smiling at the same time, glasses fogged, one arm around her. "
     f"They are both utterly overwhelmed. We never see what they are looking "
     f"at. They are the ONLY two people in the frame. Soft, quiet, enormous. "
     f"{STYLE}",
     ["may", "ollie"]),

    ("s32_toddler_chaos", "16:9",
     f"Handheld wide shot, total domestic chaos in a cluttered family home at "
     f"breakfast. A small round-faced four-year-old girl with wild dark curly "
     f"hair exactly like her mother's — the same child as in the reference "
     f"image — is sprinting through the room at full speed, shrieking with "
     f"joy. She is wearing her mustard-yellow t-shirt, ordinary spotty "
     f"leggings, and ONE welly boot. She is dressed completely normally: NO "
     f"nappy, NO underwear worn on the outside of her clothes, no costume — "
     f"just the t-shirt, the leggings and the one boot. {W['may']} and "
     f"{W['ollie']} are both mid-lunge behind her, failing to catch her. "
     f"Cheerios everywhere, a dog involved, an overturned cereal bowl in "
     f"mid-air. Everyone is extremely happy. {STYLE}",
     ["may", "ollie", "kid"]),

    ("s33_family_tree", "16:9",
     f"A small back garden at golden hour. A big old real tree — and hanging "
     f"from all of its branches on lengths of string are dozens of framed "
     f"family photographs, turning gently in the air. Sitting in the branches "
     f"among the photographs, higher up than anyone else and clearly the "
     f"ringleader, is THEIR OWN DAUGHTER — {W['kid']} — exactly the child from "
     f"the reference image, with her wild dark curly hair and mustard-yellow "
     f"t-shirt, grinning down at her parents. Several other children (cousins) "
     f"are climbing in the lower branches around her. Underneath the tree, "
     f"{W['may']} and {W['ollie']} stand with their arms around each other, "
     f"looking up at their daughter. A literal family tree. {STYLE}",
     ["may", "ollie", "kid"]),

    # ================= THE MUSEUM =================
    ("s34_museum_enter", "16:9",
     f"Wide shot: the great hall of an old natural history museum after "
     f"closing time — whale skeleton overhead, glowing diorama cases along "
     f"both walls, warm low light, dust in the air. {W['may']} and "
     f"{W['ollie']}, a little older now, walk in through the enormous doors "
     f"hand in hand, and {W['kid']} runs on ahead of them across the polished "
     f"floor. They are the ONLY people in the museum — it is otherwise "
     f"completely EMPTY, no other visitors, no staff. {STYLE}",
     ["may", "ollie", "kid", "loc_museum"]),

    # REVERTED to the earlier take (outputs/raw 12:59): forcing "every case is a
    # pair" made the exhibits come back as flat PHOTOGRAPHS mounted in the cases
    # instead of real three-dimensional animals — the whole point is that they're
    # taxidermy mounts you could walk up to. Better to have three real dioramas
    # than a corridor of posters. The 3D language below is what protects that.
    ("s35_dioramas", "16:9",
     f"Lateral tracking shot down a corridor of glowing natural-history "
     f"diorama cases in a dark empty museum. The exhibits are REAL, SOLID, "
     f"THREE-DIMENSIONAL TAXIDERMY MOUNTS standing inside deep glass cases — "
     f"actual sculpted animals with real volume and depth, posed in built sets "
     f"with real painted backdrops behind them. They are absolutely NOT flat "
     f"photographs, NOT prints, NOT posters and NOT pictures hung on a wall: "
     f"you could walk around them. Inside the cases, lit warmly, are EXACTLY "
     f"the pairs from the reference images: two lobe-finned fish with their "
     f"snouts nudged together; two early primates hanging upside-down holding "
     f"hands, foreheads bonked; two naked hairy hominids (no clothing, one "
     f"rust-orange furred and one blue-grey furred) standing forehead to "
     f"forehead in tall grass. Every diorama is a PAIR of creatures, frozen "
     f"mid-affection. Walking past them down the corridor, small in the frame "
     f"and seen from behind, are THIS EXACT FAMILY and NOBODY ELSE: "
     f"{W['may']}; {W['ollie']}; and {W['kid']}. Their faces and clothes are "
     f"exactly those of the reference images. They are the ONLY three people "
     f"in the museum — no other visitors, no staff, no other family. {STYLE}",
     ["pair_fish", "pair_monkeys", "pair_hominids", "may", "ollie", "kid",
      "loc_museum"]),

    ("s36_glass_handprints", "16:9",
     f"Locked-off medium shot in the dark museum. A lit glass exhibit case "
     f"holds a section of a rough pale cave wall bearing TWO RED-OCHRE "
     f"HANDPRINTS side by side, one larger and one smaller. {W['may']} has "
     f"placed her hand flat on the outside of the glass, exactly over the "
     f"smaller print. {W['ollie']} has placed his hand flat on the glass over "
     f"the larger one. Neither is looking at the other. Their reflections are "
     f"faint in the glass. They are the ONLY two people in the frame. "
     f"{STYLE}",
     ["may", "ollie", "loc_museum"]),

    ("s37_dome_to_stars", "16:9",
     f"Looking straight up inside the museum: the suspended whale skeleton, "
     f"and beyond it the great vaulted glass-and-iron dome of the roof — and "
     f"through the glass, an impossibly deep starfield, in which TWO stars "
     f"burn brighter than the rest, one warm coral-orange and one deep "
     f"teal-blue, orbiting each other. The camera is craning upward. Far "
     f"below, two tiny figures. {COSMIC}",
     ["loc_museum"]),

    # ================= FINAL =================
    ("s38_old_dance", "16:9",
     f"Wide locked-off shot of {W['kitchen']} — the SAME kitchen, the same "
     f"lino, the same kettle, the same pendant lamp, from EXACTLY the same "
     f"camera position and lens as the film's opening dance. Fifty years "
     f"later. {W['may_old']} and {W['ollie_old']} hold each other and sway in "
     f"the middle of the floor, badly and out of time, foreheads touching, "
     f"eyes closed. A small grandchild watches from the doorway, deeply "
     f"unimpressed. {STYLE}",
     ["may_old", "ollie_old", "loc_kitchen"]),

    # The cave prints (1:36) are two ADULTS — the couple. These are a CHILD'S,
    # deliberately: the gesture handed down a generation. Tiny hands, same two
    # colours. That contrast is the point, so the size must read instantly.
    ("s39_fridge_handprints", "16:9",
     f"Medium shot in {W['kitchen']}. {W['may_old']} and {W['ollie_old']} "
     f"stand forehead to forehead, eyes closed, holding each other's forearms. "
     f"Behind them, taped to the crowded fridge door among the postcards and "
     f"magnets, is a sheet of paper bearing a small child's painting: TWO TINY "
     f"CHILD'S HANDPRINTS in poster paint, side by side — one pressed in "
     f"coral-orange paint, one in teal-blue paint. These are unmistakably the "
     f"hands of a VERY YOUNG CHILD: very small, chubby, with short stubby "
     f"little fingers and a small round palm — obviously a toddler's hands, "
     f"NOT adult hands, and tiny against the size of the paper. The two little "
     f"handprints are clearly visible over their shoulders. They are the ONLY "
     f"two people in the frame. {STYLE}",
     ["may_old", "ollie_old", "loc_kitchen"]),

    # Had NO character refs, so the model invented a couple in the window. If a
    # face is legible anywhere in frame it must be THEM — the same two, aged.
    ("s40_pullback", "16:9",
     f"An extreme pull-back seen from outside at night: in the very centre of "
     f"the frame, one small lit kitchen window, warm and gold — and around it "
     f"the dark house, the dark street, the sleeping town, all falling away "
     f"below. The frame is mostly night; that one window is the only warm light "
     f"in the whole picture, and it is small. Framed inside that lit window, "
     f"tiny but visible, are {W['may_old']} and {W['ollie_old']} — THE SAME "
     f"ELDERLY COUPLE as the reference images and NOBODY ELSE — still standing "
     f"forehead to forehead, still slowly swaying together in their kitchen. "
     f"They are the ONLY people anywhere in the frame: no other couple, no "
     f"other figures, no strangers, no neighbours at any other window. Every "
     f"other window in the town is dark and empty. Beginning of an endless "
     f"upward pull-back toward the stars. {STYLE}",
     ["may_old", "ollie_old", "loc_kitchen"]),

    ("s40b_earth", "16:9",
     f"The Earth seen from very far away in deep space — small, warm, alone, "
     f"one soft point of amber-blue light in an enormous painterly dark. "
     f"Nothing else in the frame but stars and dust. Not epic and cold; "
     f"small and precious, like something you could hold. {COSMIC}",
     []),
]
