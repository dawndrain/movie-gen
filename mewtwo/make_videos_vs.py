#!/usr/bin/env python3
"""Emit videos_v1.sh for THE VAULTED SKY: all shots, dialogue clips with TTS audio
refs, durations auto-sized from audio (speech + headroom, clamped 5..15s).
Run after vo_vs.py. Then: caffeinate -is python3 pool_run.py mewtwo/videos_v1.sh
mewtwo/outputs/v1 7 fast"""
import subprocess
from pathlib import Path

from vo_vs import LINES

HERE = Path(__file__).parent
VO = HERE / "vo_el"

NEG = ("Photorealistic dark sci-fi feature film, natural motion, correct anatomy. "
       "Locked-off or slow deliberate camera only; no random camera moves, no zoom. "
       "No text, captions or subtitles. No narrator and no voiceover except the "
       "reference audio; nobody speaks except as described. Characters keep exactly "
       "the same faces, bodies, clothing and colors as in the reference images.")

MLOCK = ("Creature lock: Mewtwo is a six-and-a-half-foot bipedal feline-alien with "
         "smooth bone-white skin, a pale grey-violet belly, a long thick purple-grey "
         "tail, a pinched cat-like face with large luminous violet eyes, two blunt "
         "horn-ridges, three bulbous fingers per hand and digitigrade legs. Its face "
         "has NO mouth and NEVER moves when it speaks: every Mewtwo line is heard as "
         "a deep, calm, resonant voice while the creature's face and body stay "
         "expressive only through posture, eyes and tail.")

# mode tags for the audio lock, per character per shot
ALOUD = "speaking aloud, lips moving naturally"
TELE = "heard telepathically while the speaker's lips and face stay completely still"
INNER = ("heard as Mewtwo's inner thought — no lips move anywhere in the frame, and "
         "no other character reacts to the voice")
SYNTH = ("heard as Mewtwo's synthesized speaker voice from its suit or the pod "
         "speakers — slightly electronic, the creature's face completely still")

# shot -> (frame, staging, [anchor refs], {char_position: mode} or None-for-silent,
#          silent_duration)
S = {}

S["a1"] = ("a1",
    "Abstract dream: slow drift through luminous amber fluid, motes and tiny "
    "bubbles rising, blurred laboratory lights wavering beyond curved glass, a "
    "green heartbeat trace pulsing softly at the frame edge in rhythm. The single "
    "line is " + INNER + ", soft and wondering, tasting each word for the very first time.",
    [], {"1": INNER}, None)
S["a2"] = ("a2",
    "The huge dark chamber hums. Inside the amber-lit biopod the small juvenile "
    "creature floats asleep, tubes swaying gently with the fluid current; monitor "
    "lights blink slowly; dust motes drift through the pod's glow. Nothing else "
    "moves. Quiet mechanical ambience, the slow beep of a heart monitor.",
    ["mewtwo_pod"], None, 6)
S["a3"] = ("a3",
    "The woman in the cardigan reads aloud from her poetry book to the empty warm "
    "room, gentle and a little self-conscious; her voice stays a faint indistinct "
    "murmur beneath the reference audio line, which is " + INNER + ". She turns a "
    "page; lamplight flickers warmly; the pencil-drawn birds on the wall tremble "
    "slightly in the lamp heat.",
    ["eva"], {"1": INNER}, None)
S["a4"] = ("a4",
    "A dark-haired psychic sits cross-legged in meditation on the "
    "laboratory floor, eyes closed, palms open on her knees; inside the "
    "glowing biopod the small creature drifts near the glass. On the "
    "panicked second line the heartbeat monitor races and the creature "
    "curls tighter; on her calm third line it slows; on the final line — "
    + INNER + ", small and steadying, a child holding onto arithmetic — "
    "the creature slowly uncurls. All voices are " + TELE + ".",
    ["sabrina_teen", "mewtwo_pod"], {"1": TELE, "2": INNER, "3": TELE,
                                     "4": INNER}, None)
S["a5"] = ("a5",
    "The old scientist alone at his monitor in the dark office murmurs the "
    "first line " + ALOUD + " to himself, wistful, not expecting an answer. "
    "Then the second line arrives — " + INNER + ", soft, hesitant, alien — "
    "and he freezes, eyes wide, looks slowly around the empty room; his "
    "eyes fill; he writes something on a yellow sticky note and presses it "
    "to the monitor\'s edge.",
    ["fuji"], {"1": ALOUD, "2": INNER}, None)
S["a6"] = ("a6",
    "The young creature presses close to the pod glass, staring at itself in the "
    "wheeled mirror; its reflection stares back through amber fluid. Line one is "
    + INNER + ", hollow. Line two is the young woman's voice, " + TELE + ", warm "
    "and steady, from among the staff. On her words the creature slowly lifts its "
    "eyes from the mirror. Staff in the background keep their faces turned away.",
    ["mewtwo_pod", "sabrina_teen"], {"1": INNER, "2": TELE}, None)
S["a7"] = ("a7",
    "Two figures alone in the amber dark. The man in the black suit speaks softly "
    "with his face inches from the pod glass, breath fogging it, " + ALOUD + ", "
    "quiet and mesmerizing, an offer being made. Between his two lines the creature "
    "inside taps one fist gently against the inner glass, then opens the palm "
    "flat, asking. The man's faint smile on the final word.",
    ["giovanni", "mewtwo_pod"], {"1": ALOUD, "2": ALOUD}, None)
S["b1"] = ("b1",
    "Wide and still: the full-grown creature floats upright in its pod, ringed by "
    "glowing screens of paused films and pages; a keyboard drifts on its arm. The "
    "line is " + INNER + ", cold and measured. As it ends, every screen flicks to "
    "the next page simultaneously.",
    ["mewtwo_pod"], {"1": INNER}, None)
S["b1b"] = ("b1b",
    "The pod chamber: technicians on a wheeled scaffold bolt a speaker "
    "grille and a keyboard swing-arm to the base of the great amber pod; "
    "the creature inside watches from three-quarter back, tail curled. "
    "Line one is " + INNER + ", quiet, anticipating. Line two is the "
    "dark-haired woman " + ALOUD + ", warm, an offering. A beat as sample "
    "voices chirp faintly from the speaker — then line three, the first "
    "words of " + SYNTH + ": deep, chosen, final. The creature's hand "
    "rests against the inner glass as it speaks.",
    ["sabrina", "mewtwo_pod"], {"1": INNER, "2": ALOUD, "3": SYNTH}, None)

S["b2"] = ("b2",
    "Extreme close-up through glass and amber fluid on huge violet eyes, "
    "unblinking; reflected pages and film frames stream across them faster and "
    "faster as the line is " + INNER + ", cold, deliberate, ending on a note of "
    "quiet menace. The reflections stop dead on the last word.",
    ["mewtwo_pod"], {"1": INNER}, None)
S["b3"] = ("b3",
    "The man in the black suit studies the Go board and places one stone, "
    "unhurried. Inside the amber pod, orbiting rings of black and white Go stones "
    "circle the creature. Line one is " + SYNTH + ". Line two the man answers "
    + ALOUD + ", with a faint dry smile, placing his stone. Line three is "
    + INNER + " — the orbiting stones slow to a stop as it is heard.",
    ["giovanni", "mewtwo_pod"], {"1": SYNTH, "2": ALOUD, "3": INNER}, None)
S["b4"] = ("b4",
    "The woman with long dark hair stands with her palm flat on the pod glass; "
    "the creature's three-fingered hand mirrors hers from inside. Her line is "
    + TELE + ", gentle, hopeful. On the second line — " + INNER + ", quiet and cold beneath its calm — the heartbeat monitor behind them leaps and races "
    "while the creature's face stays utterly serene.",
    ["sabrina", "mewtwo_pod"], {"1": TELE, "2": INNER}, None)
S["c1"] = ("c1",
    "The pod stands drained, glass streaked with runnels; the creature convulses "
    "on its knees on the wet floor, tubes hanging loose, gasping soundlessly; "
    "technicians rush with suit pieces. The single line — " + TELE + ", the "
    "woman's voice cracking with urgency — rings over the chaos. On it the "
    "creature's chest heaves in a first full breath.",
    ["mewtwo_pod", "sabrina"], {"1": TELE}, None)
S["c2"] = ("c2",
    "The creature in the bulky tube-metal suit rises slowly to its feet beside "
    "the drained pod and turns fully around for the first time in its life, tail "
    "stretching out; the ring of staff steps back; the black fox pokemon growls "
    "low. The line is " + INNER + ", trembling, whispered twice like a prayer.",
    ["mewtwo_suit1"], {"1": INNER}, None)
S["c3"] = ("c3",
    "In the white corridor the armored creature bows slightly to the older woman "
    "in her doorway, tail lifting for balance. The first line is the long-haired "
    "woman speaking " + ALOUD + ", formal and kind. The second is the older woman "
    + ALOUD + ", flustered and delighted, pressing her poetry book to her chest. "
    "Staff crowd the corridor behind, staring in awe.",
    ["mewtwo_armor", "eva", "sabrina"], {"1": ALOUD, "2": ALOUD}, None)
S["c4"] = ("c4",
    "At the foot of the final staircase flooded with daylight the armored "
    "creature stands frozen, gripping the rail; the woman wraps her small hand "
    "around its huge three-fingered one. Her line is " + TELE + ", quiet and "
    "sure. It squeezes her hand, nods once, and they begin to climb into the "
    "light together.",
    ["mewtwo_armor", "sabrina"], {"1": TELE}, None)
S["c5"] = ("c5",
    "Wide from behind: hand in hand, the armored creature and the woman stand in "
    "wind-bent grass at the cliff's edge under an immense blue sky, her hair "
    "streaming. The line is Mewtwo's, " + TELE + ", overwhelmed, rushing, half "
    "terror half rapture. Her shoulders shake — she is crying and laughing; the "
    "creature's tail curls tight around its own leg. Wind roars softly.",
    ["mewtwo_armor", "sabrina"], {"1": TELE}, None)
S["c6"] = ("c6",
    "Dusk. The armored creature faces the darkening sea, a red light blinking on "
    "its chest, fists clenched; behind it the man in the black suit, the guards "
    "and the dark pokemon wait in a silent ring. Line one is the man " + ALOUD +
    ", flat, final. Line two is " + INNER + ", breaking apart. On its last word "
    "the creature's fists slowly open in surrender and it turns from the sea.",
    ["mewtwo_armor", "giovanni"], {"1": ALOUD, "2": INNER}, None)
S["d1"] = ("d1",
    "Fluorescent conference room, exhausted scientists around the long table. The "
    "first speaker gestures at the whiteboard, " + ALOUD + ", strained. The "
    "second answers " + ALOUD + ", jabbing a finger at the table, voice low and "
    "hard. Others pinch their noses, slump, stir cold coffee. The whiteboard "
    "writing stays an indistinct blur throughout.",
    ["dr_light", "collins"], {"1": ALOUD, "2": ALOUD}, None)
S["d2"] = ("d2",
    "The man in the black suit stands just inside the conference room door; "
    "every scientist is frozen mid-word, turned to him. He speaks " + ALOUD + ", "
    "pleasant and unhurried, and on his final two words draws a blue-and-red "
    "capsule ball smoothly from inside his jacket. Absolute silence otherwise; "
    "one chair creaks.",
    ["giovanni", "dr_light", "collins"], {"1": ALOUD}, None)
S["d3"] = ("d3",
    "Two seconds of chaos then stillness: the sandy-haired scientist bolts, his "
    "cry " + ALOUD + " and cut off mid-word as the thrown ball strikes his back "
    "and he dissolves into streaming red-white light sucked into the capsule; "
    "the ball drops, bounces once, rolls and clicks against a table leg. A long "
    "beat. The man in the black suit speaks " + ALOUD + ", mild and courteous, "
    "to the grey-haired woman. No one else moves or speaks.",
    ["giovanni", "collins", "dr_light"], {"1": ALOUD, "2": ALOUD}, None)
S["d4"] = ("d4",
    "The conference room just after: toppled chairs, settling papers, scientists "
    "pressed to the walls. The grey-haired woman at the table's head speaks "
    + ALOUD + " — steady, barely — with her own hand already raised. One by one, "
    "silently, every other hand in the room rises. Hold on the forest of raised "
    "hands.",
    ["dr_light"], {"1": ALOUD}, None)
S["d5"] = ("d5",
    "The small execution room, one hard light. The man in the black suit sits "
    "across from the strapped-down young prisoner and speaks " + ALOUD + ", "
    "quiet, procedural, almost kind, nodding at the syringe on the table between "
    "them. The prisoner goes very still, eyes on the needle. No other sound.",
    ["giovanni"], {"1": ALOUD}, None)
S["d6a"] = ("d6",
    "The bare white holochamber. The man in the black suit sits facing the "
    "translucent glitch-edged hologram of the pod room and its creature. Line "
    "one is " + SYNTH + ", mild, ritual — the holographic creature. Line two the "
    "man answers " + ALOUD + ", tired, and delivers his confession without "
    "flinching, eyes never leaving the hologram.",
    ["giovanni", "mewtwo_pod"], {"1": SYNTH, "2": ALOUD}, None)
S["d6b"] = ("d6",
    "The holochamber. The holographic creature answers — " + SYNTH + ", perfectly "
    "graceful, reasonable, warm. The man in the black suit listens with his eyes "
    "closed... then presses the small button on the chair arm: the hologram and "
    "the whole simulated pod room dissolve instantly into bare white nothing. He "
    "sits alone in the empty white room, dabs his forehead with a handkerchief, "
    "and speaks the final line " + ALOUD + ", almost to himself.",
    ["giovanni", "mewtwo_pod"], {"1": SYNTH, "2": ALOUD}, None)
S["e1"] = ("e1",
    "Autumn morning walk on the clifftop, breath-mist, tawny grass, the volcano "
    "hazy far inland. The armored creature strolls between the woman and the "
    "engineer. Its line is " + SYNTH + ", conversational, faintly wondering. The "
    "engineer grins and nods; the woman smiles; leaves and grass stream past in "
    "the cold wind.",
    ["mewtwo_armor", "sabrina", "ayush"], {"1": SYNTH}, None)
S["e2"] = ("e2",
    "The woman laughs as she hovers a hand-span off the grass, hair and coat "
    "lifting weightless, shimmering light around her; the armored creature "
    "hovers beside her. Her line is " + ALOUD + ", breathless, delighted, "
    "laughing. The engineer stares open-mouthed, then whoops. Pure joy; wind and "
    "her laughter.",
    ["sabrina", "mewtwo_armor", "ayush"], {"1": ALOUD}, None)
S["e3"] = ("e3",
    "Low angle at grass level, golden sunset: the armored creature strolls "
    "beside the engineer — but its feet glide a few centimeters above the grass "
    "blades, never touching, while crisp footprints press themselves into the "
    "turf behind it one by one, flattening grass where no foot lands. The "
    "engineer looks ahead, noticing nothing. Only wind and distant birdsong.",
    ["mewtwo_armor", "ayush"], None, 7)
S["e4"] = ("e4",
    "Night inside the sealed dark pod: the creature floats with eyes closed, "
    "face utterly still, faint slow ripples crossing the amber fluid around its "
    "head. Three voices are heard in sequence, all versions of the same deep "
    "voice, " + INNER + ": the first hissed and urgent; the second even and "
    "gentle; the third calm, commanding, final. With each voice a different dim "
    "reflection of its face on the curved glass seems to catch light. Nothing "
    "else moves.",
    ["mewtwo_pod"], {"1": INNER, "2": INNER, "3": INNER}, None)
S["e5a"] = ("e5",
    "Storm on the clifftop, rain hammering, both figures soaked. The woman looks "
    "up at the armored creature; her line is " + TELE + ", gentle, careful, full "
    "of worry. The creature stands motionless, rain streaming off its plates, "
    "tail curled tight. Thunder rolls far away.",
    ["mewtwo_armor", "sabrina"], {"1": TELE}, None)
S["e5b"] = ("e5",
    "Storm on the clifftop, rain hammering. The creature's answer is " + TELE +
    ", perfectly noble, perfectly measured. On the woman's reply — " + TELE +
    ", smiling through the rain, utterly sincere — she briefly closes her eyes, "
    "moved. The creature looks out to sea. Rain and wind under everything.",
    ["mewtwo_armor", "sabrina"], {"1": TELE, "2": TELE}, None)
S["e6"] = ("e6",
    "The white training hall. On the woman's line — " + TELE + ", clinical, "
    "with the faintest sting — the armored creature's fingers twitch; then it "
    "thrusts one arm out and the stuffed grey pokemon doll across the hall "
    "SLAMS into the padded wall with a concussive bang, dust bursting, the "
    "lights shivering. Behind the high observation glass, silhouettes surge to "
    "their feet.",
    ["mewtwo_armor", "sabrina", "giovanni"], {"1": TELE}, None)
S["e7"] = ("e7",
    "The training hall. The small purple rat pokemon hangs by its teeth from "
    "the creature's bleeding calf; the creature bends over it, shaken, then "
    "deliberately stamps its own wounded foot and goes still. Line one comes "
    "slightly muffled through the observation glass — the man in the black "
    "suit, " + ALOUD + ", clinically curious. Line two is " + SYNTH + ", "
    "controlled again, with the barest tremor.",
    ["mewtwo_armor", "giovanni"], {"1": ALOUD, "2": SYNTH}, None)
S["e8"] = ("e8",
    "Extreme close-up in darkness on the sleeping creature's face in amber "
    "fluid. Three lines, all the same deep voice, " + INNER + ": the first "
    "flat, newborn, tasting each word; the second even and gentle; the third a "
    "single cold word. On the final word the creature's closed eyes twitch, "
    "and a warped fifth reflection of its face on the glass slides slowly out "
    "of frame.",
    ["mewtwo_pod"], {"1": INNER, "2": INNER, "3": INNER}, None)
S["f1"] = ("f1",
    "The conference room in earthquake: wall monitors play news footage of a "
    "colossal red-armored titan wading through boiling sea; the room shudders, "
    "dust sifts from the ceiling, mugs walk off the table and shatter, the "
    "fluorescents gutter and snap over to red emergency light. Scientists grab "
    "the walls. Sirens begin, muffled and far away. No speech.",
    [], None, 7)
S["f2"] = ("f2",
    "Red-lit corridor by the collapsed stairwell, staff hurrying past with "
    "crates. The young man with the sketchbook stops the grey-haired director; "
    "his line is " + ALOUD + ", urgent, shy, barely daring. Her answer is "
    + ALOUD + " — smooth, immediate, unreadable. As he turns away his face "
    "softens with a wave of gratitude that does not belong to him, and he "
    "stops, touching his own chest, bewildered.",
    ["gyokusho", "dr_light"], {"1": ALOUD, "2": ALOUD}, None)
S["f3"] = ("f3",
    "A red-lit alcove, two figures close and quiet: the hard-faced security "
    "chief speaks first, " + ALOUD + ", low, flat, deadly serious. The "
    "grey-haired director answers " + ALOUD + ", clipped and final, gripping "
    "her clipboard. Neither face gives anything away. Distant rumbles under "
    "the red light.",
    ["shaw", "dr_light"], {"1": ALOUD, "2": ALOUD}, None)
S["f4a"] = ("f4",
    "The pod chamber under red emergency light, a crack across the ceiling "
    "dropping threads of dust through the amber glow. The director stands "
    "before the glass. Her greeting is " + ALOUD + ", carefully casual. The "
    "creature's reply is " + SYNTH + " — mild, courteous, faintly amused — as "
    "it drifts down level with her.",
    ["dr_light", "mewtwo_pod"], {"1": ALOUD, "2": SYNTH}, None)
S["f4b"] = ("f4",
    "The pod chamber, red light, falling dust. The director's warning is "
    + ALOUD + ", honest, heavy. The creature holds her gaze through the glass; "
    "its answer is " + SYNTH + ", quiet and unhesitating — and on the final "
    "words the great pod begins, slowly, to drain.",
    ["dr_light", "mewtwo_pod"], {"1": ALOUD, "2": SYNTH}, None)
S["f5"] = ("f5",
    "Pouring rain on the plateau at dusk. The armored creature rises out of "
    "the broken opening in the earth amid rubble; the drenched crowd of "
    "evacuated staff bursts into applause — which falters, thins, and dies as "
    "it straightens to full height. The helmet turns slowly across them, then "
    "tilts up to the sky, rain pattering loud off the visor. No speech.",
    ["mewtwo_armor"], None, 8)
S["f6a"] = ("f6",
    "Thin rain, dusk, the long walk along the clifftop; the armored creature "
    "strolls beside the director, guards ringed far behind. Its line is "
    + SYNTH + " — wistful, unhurried, savoring each wish; a beat of silence "
    "before the final word. Her answer is " + ALOUD + ", soft, and for one "
    "unguarded moment she means it.",
    ["mewtwo_armor", "dr_light"], {"1": SYNTH, "2": ALOUD}, None)
S["f6b"] = ("f6",
    "The walk. The creature stops abruptly, facing the eastern cliff edge; its "
    "long tail swings and brushes across the director's stomach. The line is "
    + SYNTH + ", courteous, apologetic. She waves it off, catching her "
    "breath; eight meters back the security chief's hand slides into his "
    "jacket pocket, and the black weasel pokemon slinks closer through the "
    "grass.",
    ["mewtwo_armor", "dr_light", "shaw"], {"1": SYNTH}, None)
S["f7"] = ("f7",
    "The security chief plants himself in front of the armored creature in "
    "the thinning rain. His line is " + ALOUD + " — hard, level, thrown down "
    "like a gauntlet. A long still beat; rain drips from the creature's chin "
    "guard. Its reply is " + SYNTH + ", soft, and utterly unreadable.",
    ["shaw", "mewtwo_armor", "dr_light"], {"1": ALOUD, "2": SYNTH}, None)
S["f8"] = ("f8",
    "Sunset tears through under the storm clouds, everything suddenly gold. "
    "The young man jogs up the wet grass waving, breathless; his line is "
    + ALOUD + ", joyful, tumbling out. The armored creature stands with the "
    "sunset blazing across its visor. Its reply is " + SYNTH + " — quiet, "
    "pleasant, and cold as a closing door. The director laughs with relief, "
    "noticing nothing.",
    ["gyokusho", "mewtwo_armor", "dr_light"], {"1": ALOUD, "2": SYNTH}, None)
S["g1"] = ("g1",
    "TWO SECONDS, real-time speed, violent and sudden, no slow motion: the "
    "creature's tail whips around the director's waist and both snap airborne "
    "off the clifftop; papers scatter; the black weasel pokemon leaps and is "
    "kicked away mid-air; a blue frog-ninja pokemon's tongue lashes out and "
    "catches the released director as the creature drops like a stone over "
    "the cliff edge and out of sight. Guards spin, shouting wordlessly. Then "
    "stunned stillness.",
    ["mewtwo_armor", "dr_light"], None, 6)
S["g2"] = ("g2",
    "Vertical plunge down the sea-cliff face at dusk, camera falling with "
    "the armored creature: it dives headfirst, then convulses in agony "
    "mid-fall — and the line, " + INNER + " and fragmenting, is heard as the "
    "convulsion slowly eases, its body unclenching, eyes clearing, the dark "
    "sea rushing up. Far above, tiny winged shapes pour off the clifftop in "
    "pursuit.",
    ["mewtwo_armor"], {"1": INNER}, None)
S["g3"] = ("g3",
    "Low chase over heavy dusk sea: the armored creature skips off wavetops "
    "like a hurled stone, spray bursting, while dark winged pokemon dive "
    "after it — a great black crow, a bone-collared vulture, a three-headed "
    "black dragon whose violet blasts detonate the water at its heels. The "
    "single word of the reference audio is ROARED " + ALOUD + " by the "
    "grizzled man riding the great crow above, furious, whipped by wind.",
    ["mewtwo_armor", "shaw"], {"1": ALOUD}, None)
S["g4"] = ("g4",
    "Underwater, blue-black, last shafts of dusk light: the armored creature "
    "swims hard for a narrow crevice in the island's rock root, trailing "
    "bubbles; four sleek dark shapes knife after it — then a boiling swarm "
    "of frenzied glowing-eyed sea creatures erupts between hunter and "
    "hunted, and the creature slips into the black crack in the rock. "
    "Muffled underwater roar, distant concussions. No speech.",
    ["mewtwo_armor"], None, 8)
S["g5"] = ("g5",
    "Pitch-black sea cave, one small red suit-light blinking. The creature "
    "lies on wet sand, helmet off beside it, and lifts a fistful of wet "
    "sand before its face, watching it trickle between its three fingers. "
    "The line is " + INNER + " — slow, amazed, each sentence its own "
    "discovery. Water drips somewhere in the dark.",
    ["mewtwo_armor"], {"1": INNER}, None)
S["g6"] = ("g6",
    "The black cave. The creature sits rigid on the sand; the still pool "
    "beside it reflects its face back subtly WRONG — tilted, colder. Three "
    "lines of the same deep voice, " + INNER + ": the first flat and dead; "
    "the second a command of cold fury — and on it the wrong reflection "
    "shivers and stills into a true mirror; the third hollow, grieving, "
    "alone. Dripping silence between each.",
    ["mewtwo_free"], {"1": INNER, "2": INNER, "3": INNER}, None)
S["g7a"] = ("g7a",
    "Pitch-black sea cave: the EMPTY armor suit propped upright on wet "
    "sand like a shed exoskeleton, helmet dark and hollow, neck opening "
    "clearly empty. Its chest light pulses gently in rhythm with the "
    "recorded line — the deep human voice, slightly tinny, filling the "
    "dark. The camera pushes in very slowly; faint ripples cross the "
    "black pool beside it. No creature appears in this shot.",
    ["mewtwo_armor"], {"1": ALOUD}, None)
S["g7b"] = ("g7b",
    "Absolute darkness: extreme close-up on two large luminous violet "
    "eyes, a faint point of suit-light reflected in each. The recorded "
    "human voice continues, tinny and distant. The eyes stay almost "
    "perfectly still — then blink once, slowly, on the final sentence, "
    "and the reflected light gutters out on the last word.",
    ["mewtwo_pod"], {"1": ALOUD}, None)
S["h1"] = ("h1",
    "The bare creature flies on its back low over black mirror-calm ocean "
    "under the blazing Milky Way, drifting between two skies; beside its "
    "face three tiny teardrops float weightless, glinting. The line is "
    + INNER + " — soft, at peace, grief and release in the same breath. "
    "Only wind, far below the stars.",
    ["mewtwo_free"], {"1": INNER}, None)
S["h2"] = ("h2",
    "Bright dawn sea: the creature swims loose and clumsy and happy among "
    "round blue whale pokemon the size of cars; one surfaces beside it with "
    "a friendly spout and regards it with a tiny eye. The line is " + INNER +
    ", wry and light — the first joke it has ever made to itself. Golden "
    "spray, gull cries.",
    ["mewtwo_free"], {"1": INNER}, None)
S["h3"] = ("h3",
    "Cold dawn sea. A towering column of whitewater collapses back into "
    "the swell; above it the pale creature hangs in the air, water "
    "streaming off its body, chest heaving. It curls forward, lifts what "
    "remains of its tail before its eyes, and goes very still; below, a "
    "darker patch drifts in the churned water and a large shadow slides "
    "away under the surface. The line is " + INNER + " — small, breaking. "
    "Then only the sea.",
    ["mewtwo_free"], {"1": INNER}, None)
S["h4"] = ("h4",
    "Night beach, wide and still: the low mound of dark sand at the tide "
    "line, only the pale snout and closed eyes of the buried creature "
    "showing; the endless starfield burns above the black sea. The line is "
    + INNER + " — a whisper, the last words before sleep. Waves hush in "
    "and out. Slow, holding, nothing else.",
    ["mewtwo_free"], {"1": INNER}, None)
S["h5"] = ("h5",
    "Deep forest night: hundreds of small floating glyph-creatures turn in "
    "vast layered concentric rings like a clock built of living aurora, "
    "green-blue light washing the trees; the pale creature hovers tiny "
    "before it, transfixed. The line is " + INNER + ", hushed, resolved. "
    "The rings turn; a low harmonic hum like many tuning forks.",
    ["mewtwo_free"], {"1": INNER}, None)
S["title"] = ("title",
    "The title card floats over the starfield above the black mirror "
    "ocean; the thin pale letters glow faintly and the stars drift almost "
    "imperceptibly behind them. The title text stays EXACTLY as in the "
    "start image, never changing, never garbling. Silence except a low "
    "night wind.",
    [], None, 5)


def adur(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


# Shots where Mewtwo must NOT appear: the creature lock is omitted (its vivid
# description makes Seedance hallucinate an off-model Mewtwo when no anchor
# ref pins the look) and replaced with an explicit absence negative.
NO_CREATURE = {"a1", "a3", "a5", "d1", "d2", "d3", "d4", "d5", "f1", "f2",
               "f3", "title"}
NOMEW = ("Mewtwo does not appear anywhere in this shot — no pale creature, "
         "no tail, no pokemon other than those explicitly described.")

# extra life for shots measured near-static in v1 — the world moves even
# when the camera and the creature hold still
MOTION_ADD = {
    "a2": "Slow visible motion throughout: bubbles rise through the fluid, "
          "the tubes sway, monitor traces scroll, dust drifts in the pod "
          "light.",
    "b1": "The fluid convects visibly; pages on the screens turn one by "
          "one; the keyboard arm drifts slightly; bubbles rise.",
    "b3": "The orbiting stones move continuously; Giovanni reaches, places "
          "his stone and sits back; the fluid shimmers.",
    "b4": "Her hair shifts as she leans in; the fluid convects; the EKG "
          "trace races visibly; small bubbles stream from the creature's "
          "hand against the glass.",
    "c6": "Rain gusts visibly; coats and grass whip in the wind; the red "
          "chest light pulses; the guards' pokemon shift their footing.",
    "d2": "He finishes stepping through the door and walks two slow paces "
          "in; scientists lean away; papers settle; the ball glints as it "
          "emerges.",
    "d6a": "The hologram flickers and glitches continuously, static "
           "crawling across its edges; dust motes drift in the white "
           "light.",
    "e4": "The fluid ripples visibly around its head; the reflections on "
          "the glass shift and trade places with each voice; a slow "
          "stream of bubbles rises.",
    "e8": "The fluid current turns the creature almost imperceptibly; its "
          "closed eyes flicker with rapid movement beneath the lids; "
          "bubbles drift.",
    "g6": "Droplets fall from the cave ceiling, ringing the pool; the "
          "wrong reflection ripples; the suit light blinks slowly.",
}

CHAR_NAMES = {
    "mewtwo": "Mewtwo", "sabrina": "the dark-haired woman Sabrina",
    "giovanni": "the man in the black suit, Giovanni",
    "drlight": "the grey-haired director Dr. Light",
    "shaw": "the security chief Shaw", "eva": "the older woman Eva",
    "gyokusho": "the young man Gyokusho",
    "fuji": "the old scientist Dr. Fuji", "sato": "the first scientist",
    "martin": "the second scientist", "collins": "Dr. Collins",
}

lines_out = [
    "#!/bin/bash",
    "# THE VAULTED SKY v1 (auto-generated by make_videos_vs.py)",
    "# Run: caffeinate -is python3 pool_run.py mewtwo/videos_v1.sh mewtwo/outputs/v1 7 fast",
]

total = 0.0
for shot, (frame, staging, anchors, modes, silent_dur) in S.items():
    refs = " ".join(f"--image mewtwo/anchors/{a}.png" for a in anchors)
    staging = staging + " " + MOTION_ADD.get(shot, "")
    lock = NOMEW if shot in NO_CREATURE else MLOCK
    if modes is None:
        dur = silent_dur
        prompt = f"{staging} {lock} {NEG}"
        auds = ""
    else:
        entries = LINES[shot]
        afiles = [VO / f"{shot}_{n}_{c}.mp3" for n, (c, _) in enumerate(entries, 1)]
        speech = sum(adur(p) for p in afiles)
        dur = min(15, max(5, round(speech + 2.5 + len(afiles) * 0.8)))
        order = "; ".join(
            f"audio clip {n} is the voice of {CHAR_NAMES[c]}, {modes[str(n)]}"
            for n, (c, _) in enumerate(entries, 1))
        audio_lock = (
            "The ONLY speech in the clip is EXACTLY the dialogue heard in the "
            f"reference audio clips, in order, in exactly those voices: {order}. "
            "Every line is spoken COMPLETELY, word for word, never shortened, and "
            "no speech is added.")
        prompt = f"{staging} {audio_lock} {lock} {NEG}"
        auds = " ".join(f"--audio mewtwo/vo_el/{p.name}" for p in afiles)
    total += dur
    frame_file = frame if (HERE / "frames2" / f"{frame}.png").exists() else ("g7" if frame == "g7b" else frame)
    # frames redone in frames2/ (originals tripped the input filter on
    # canonical front-facing Mewtwo) take priority when present
    fdir = "mewtwo/frames2" if (HERE / "frames2" / f"{frame_file}.png").exists() \
        else "mewtwo/frames"
    lines_out.append(
        f'gen {shot} {dur} "{prompt}" --start-image {fdir}/{frame_file}.png '
        f'{refs} {auds}'.rstrip())

out = HERE / "videos_v1.sh"
out.write_text("\n".join(lines_out) + "\n")
print(f"wrote {out}: {len(S)} shots, ~{total:.0f}s of film")
