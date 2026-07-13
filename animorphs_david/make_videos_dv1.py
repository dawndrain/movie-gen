#!/usr/bin/env python3
"""Emit videos_dv1.sh: full first-pass shot list with TTS audio refs.
Clip durations auto-sized from the audio (speech + headroom, clamped 5..15s).
Run after: python3 pool_run.py animorphs_david/videos_dv1.sh animorphs_david/outputs/dv1"""
import subprocess
from pathlib import Path

from vo_david import LINES
from make_images import WARDROBE

HERE = Path(__file__).parent
VO = HERE / "vo"

NEG = ("Photorealistic sci-fi thriller film, natural human and animal motion, "
       "correct anatomy. Locked-off static camera unless a move is described; no "
       "random camera moves. No text or captions. There is no narrator and no "
       "voiceover; only characters on screen speak. Characters keep exactly the "
       "same faces, hair, clothes, bodies and colors as in the reference images.")

AND = ("Species lock: the Andalite is a graceful alien centaur with four legs, an "
       "upright slim torso with two arms, small eyes on flexible stalks atop the "
       "head, a scythe-blade tail and NO mouth; when an Andalite speaks, the "
       "voice is heard telepathically while the mouthless face stays completely "
       "still.")

THOUGHT = ("Thought-speak lock: when a morphed animal speaks, the animal's mouth "
           "NEVER moves and its face stays a natural animal face; the speaker's "
           "voice is simply heard, calm and clear, over the scene.")

# display name for the audio-order lock; parenthetical = current body
CHAR_DESC = {
    "jake": "Jake", "marco": "Marco", "rachel": "Rachel", "cassie": "Cassie",
    "david": "David", "tobias": "Tobias (the red-tailed hawk, thought-speak)",
    "ax": "Ax (the Andalite, thought-speak)",
    "visser": "Visser Three (the Andalite-bodied commander, thought-speak)",
}

W = WARDROBE  # wardrobe lock text per human

def wl(*names):
    return "Wardrobe lock: " + " ".join(f"{n.title()} is {W[n]}." for n in names)

# shot -> (staging/acting prompt, [image anchor refs], extra locks)
# Dialogue shots pull audio refs + speaker order automatically from LINES.
SHOTS = {
    "a2": ("David's bedroom at night, monitor light. He types with two fingers, "
           "reading his listing aloud to himself with a crooked grin, then leans "
           "back and turns the glowing blue cube slowly in one hand on the last "
           "sentence, talking to it like a pet. He speaks the COMPLETE exact "
           "sentences of the reference audio, word for word.",
           ["david"], [wl("david")]),
    "a4": ("Jake's bedroom at night. Marco spins the laptop toward Jake, voice "
           "tight under the jokes for once. Jake leans in; his face hardens as "
           "he recognizes the cube. The exchange is fast, clipped, urgent — "
           "four lines, alternating, ending on Jake's flat decision.",
           ["marco", "jake"], [wl("jake", "marco")]),
    "v1": ("The scarred Andalite-bodied commander stands before the red hologram "
           "of a suburban house, utterly still except for one stalk eye turning "
           "toward an unseen subordinate. His cold silky voice savors the "
           "absurdity of the words 'their internet', then turns razor-sharp on "
           "the final commands. The hologram tints his eyes red.",
           ["visser", "loc_bladeship"], [AND]),
    "a6": ("Night barn, lantern light. David, blanket around his shoulders, "
           "stares at nothing and asks his question in a voice scraped hollow. "
           "Jake crouches to his eye level and answers slowly, gently, choosing "
           "every word, delivering the terrible sentence like a doctor. Cassie "
           "watches with her hand pressed to her mouth.",
           ["david", "jake", "cassie", "rachel", "marco"],
           [wl("david", "jake", "cassie")]),
    "a7": ("Lantern-lit barn. The blue cube glows on the hay bale. Jake speaks "
           "the invitation formally, like an oath. Marco mutters his warning "
           "sideways, not joking. Then David presses his palm flat onto the "
           "cube: blue light crawls up his arm and his eyes go wide as the "
           "morphing power enters him. Hold on his lit face.",
           ["david", "jake", "marco"], [wl("david", "jake", "marco")]),
    "a8": ("SILENT VFX shot. In the moonlit hayloft David morphs into a golden "
           "eagle: golden feathers ripple up his arms as they flatten into "
           "wings, he shrinks into himself, his face stretches into a beak — "
           "then the eagle bursts out through the open loft door and wheels up "
           "across the moon, exhilarated. Morph is eerie-smooth, no gore. Wind "
           "and wingbeats only, no dialogue.",
           ["david", "loc_barn"], [wl("david")]),
    "b1": ("Night lion habitat at the zoo. David kneels with his hand on the "
           "sleeping lion's flank; the lion's slow breathing deepens as the "
           "acquiring trance takes hold, its eyelid half-lifting. David speaks "
           "his lines in a low hungry murmur, ending with the grin of a boy who "
           "has just been handed a loaded weapon. Rachel watches from the rail, "
           "arms folded, saying nothing, profoundly uneasy.",
           ["david", "rachel"], [wl("david", "rachel")]),
    "b2": ("Night rooftop above the summit hotel, wind. Jake gives the order "
           "with quiet finality, counting the rules off. David steps INTO "
           "Jake's space on his reply, chin out, smiling with no warmth, and "
           "the smile drops entirely on his last five words. Marco and Rachel "
           "go very still behind them. The audio clips are spoken in order, "
           "nothing added.",
           ["jake", "david", "marco", "rachel", "loc_hotel"],
           [wl("jake", "david", "marco", "rachel")]),
    "b3": ("SILENT chaos, handheld energy. A huge male lion stalks down the "
           "elegant hotel corridor and ROARS; security men dive behind an "
           "overturned luggage cart, an alarm strobes, glass shatters "
           "somewhere, curtains tear as the lion shoulders through them. "
           "Screams and alarm only, no dialogue, no blood.",
           ["loc_hotel"], []),
    "b4": ("Barn at night, the argument at full boil. Marco counts the "
           "accusations on his fingers, furious, voice cracking. David "
           "explodes back, jabbing a finger, pacing like a caged thing, his "
           "voice breaking with real hurt on 'I lost everything' — for one "
           "second he is just a kid, then the mask slams back down. Jake keeps "
           "an arm between them.",
           ["marco", "david", "jake", "rachel"],
           [wl("marco", "david", "jake")]),
    "b5": ("SILENT dread, golden hour. The red-tailed hawk preens on the oak "
           "branch, unaware. The golden eagle folds and stoops out of the sun "
           "like a missile — impact happens BEHIND the leaves in an explosion "
           "of scattered feathers; the branch whips; russet feathers drift "
           "down onto the empty grass. Wind and one distant raptor scream "
           "only. No gore shown.",
           ["tobias", "loc_meadow"], []),
    "b6": ("Dusk under the oak. Rachel kneels holding the red tail feathers; "
           "her lines come out low and shaking, grief hardening into something "
           "frightening, and she looks up at Jake on the final sentence daring "
           "him to deny it. Jake's answer is quiet, cold and deliberate — the "
           "voice of someone deciding something terrible. No shouting.",
           ["rachel", "jake", "loc_meadow"], [wl("rachel", "jake")]),
    "b7a": ("Night construction site, cold moonlight. The tiger and the lion "
            "circle each other slowly between the plywood house frames, heads "
            "low, muscles rolling. David's thought-speak voice drips mock "
            "admiration; Jake's answer is one flat sentence. The animals never "
            "stop circling while the voices are heard; their mouths never move.",
            ["loc_construction"], [THOUGHT]),
    "b7b": ("SILENT fight. The tiger and lion collide chest to chest in a burst "
            "of mud, rear up trading blows, crash together through a plywood "
            "wall, roll through scaffolding poles in a cloud of dust and "
            "splinters. Ferocious, fast, brutal — but no blood, no wounds "
            "shown. Roars, impact, splintering wood only. No dialogue.",
            ["loc_construction"], []),
    "b7c": ("Night construction site. The lion has the tiger pinned on its "
            "back at the trench edge, jaws at its throat; David's thought-speak "
            "gloats, slow and delicious. Then a grizzly bear EXPLODES through "
            "the plywood wall behind them in a shower of splinters and hurls "
            "the lion off with one blow; the lion rolls, comes up limping, and "
            "melts into the dark as Rachel's thought-speak lands like a "
            "hammer. Animal mouths never move for the voices.",
            ["loc_construction"], [THOUGHT]),
    "c1": ("Barn, late, everyone wrung out. Jake, dirt-streaked, works through "
           "the impossible options on his fingers, flat and exhausted. A "
           "silence. Then Cassie steps into the lantern light and delivers her "
           "lines quietly, sadly, absolutely sure — and the room turns to look "
           "at her. The Andalite in the shadows keeps both stalk eyes on her.",
           ["jake", "cassie", "rachel", "marco", "ax"],
           [wl("jake", "cassie"), AND]),
    "c2": ("Barn at night. The red-tailed hawk back-wings down onto the rafter "
           "with a whump of air; everyone spins. Tobias's thought-speak is dry, "
           "wry, gloriously alive; the hawk cocks its head and does not move "
           "its beak. Rachel laughs once — half sob — and answers with fierce "
           "wet-eyed joy, pointing a warning finger up at the bird.",
           ["tobias", "rachel", "jake", "cassie"], [wl("rachel"), THOUGHT]),
    "c3": ("SILENT conspiratorial planning, night barn. Cassie's finger traces "
           "the coastline map to the cove and taps twice; Marco draws an X and "
           "mimes a lid slamming shut; Jake looks from face to face and gives "
           "one slow nod. The lantern flame gutters. Whispers too low to hear, "
           "paper sounds, night insects. No intelligible dialogue.",
           ["cassie", "marco", "jake"], [wl("cassie", "marco", "jake")]),
    "c4": ("THE STAGED MEETING. Camera stays at floor level: in the sharp "
           "foreground a brown rat crouches in the gap under the floorboards, "
           "ears twitching, lamplight in its black eyes; beyond it, slightly "
           "soft, the circle of teenagers plays out the scene. Jake announces "
           "the plan a shade too loudly, like a bad actor selling a line. "
           "Marco protests on cue. Jake hammers the word 'alone'. Nobody looks "
           "at the floor. The rat's whiskers tremble as it drinks in every "
           "word.",
           ["jake", "rachel", "cassie", "marco", "ax"],
           [wl("jake", "marco"), AND]),
    "c5": ("High rafter POV down into the barn. In the near foreground the "
           "hawk watches the rat slip out through the wall gap far below and "
           "vanish into the night. Tobias's thought-speak is a murmur, grimly "
           "satisfied; the hawk's beak never moves. Below, Jake closes his "
           "eyes for one long second and answers almost inaudibly, the words "
           "heavy as stones.",
           ["tobias", "jake"], [wl("jake"), THOUGHT]),
    "c6": ("Cold dawn cove, wind and surf. Rachel stands alone on the wet "
           "boulder, the blue cube under one arm, and SHOUTS her challenge at "
           "the rocks — raw, furious, half-hoping he won't come. Her hair "
           "whips across her face. Gulls scatter at her voice. She speaks the "
           "complete reference audio exactly once, nothing more.",
           ["rachel", "loc_cove"], [wl("rachel")]),
    "c7": ("The trap springs at the dawn cove. The lion freezes mid-stride as "
           "they rise from everywhere at once — grizzly to full height on the "
           "boulder, gorilla knuckling over the tide pools, wolf hackles-up, "
           "tiger advancing, the Andalite's tail blade dropping across the "
           "cliff gap, the hawk hovering above. Jake's thought-speak is calm "
           "and final. David's answer comes slow, almost admiring, as the "
           "lion turns and turns and finds every exit filled. No animal mouth "
           "moves for the voices.",
           ["ax", "loc_cove"], [THOUGHT, AND]),
    "c8": ("At the cliff base the cornered lion suddenly collapses inward — "
           "morphing DOWN, mane receding, body shrinking through fox-size to "
           "rat-size in seconds — and the brown rat darts into the narrow "
           "dead-end crevice. David's thought-speak taunt is heard during the "
           "shrink, cocky and breathless. Eerie-smooth morph, no gore.",
           ["loc_cove"], [THOUGHT]),
    "c10": ("The rock island. Rachel sets the rat down on the bare stone with "
            "both hands, unbearably gentle. The rat spins in a circle, rears "
            "up at her; David's thought-speak comes small and cracking, "
            "rising to a scream on the last two words. Rachel stands, wipes "
            "her face with the back of her wrist, and answers barely above "
            "the wind — then turns away to the rowboat. Surf, gulls, wind. "
            "The rat's mouth never moves for the voice.",
            ["rachel", "loc_island"], [wl("rachel"), THOUGHT]),
    "c12": ("Dusk barn, the hollow after. Long silences between the lines. "
            "Cassie says her line to the floor, trying to believe it. Rachel, "
            "hugging her elbows, asks her question to no one. Jake stands, "
            "looks at each of them in turn, and gives the order flat and "
            "quiet, like closing a door. The hawk on the rafter does not "
            "stir. Nobody smiles. Fade toward dark at the end.",
            ["jake", "rachel", "cassie", "marco", "ax", "tobias"],
            [wl("jake", "rachel", "cassie"), AND]),
}

# Shots whose speech exceeds the 15s Seedance cap, split into sub-shots that
# share the parent's start frame. sub -> (parent frame, [vo stems], staging)
SPLITS = {
    "a4": [
        ("a4a", ["a4_1_marco", "a4_2_jake"],
         "Jake's bedroom at night. Marco spins the laptop toward Jake, voice "
         "tight under the joke for once. Jake leans in, gripping the chair "
         "back, his face hardening in the screen light as he names the cube. "
         "Two lines only, then a held look between them."),
        ("a4b", ["a4_3_marco", "a4_4_jake"],
         "Jake's bedroom, seconds later. Marco taps the laptop screen, laying "
         "out the danger fast and sharp; Jake straightens up and gives the "
         "flat one-line decision of a general. End on his set face."),
    ],
    "b2": [
        ("b2a", ["b2_1_jake"],
         "Night rooftop above the summit hotel, wind. Jake gives the order "
         "with quiet finality, counting the rules off on raised fingers; the "
         "others listen — but David, arms crossed, smiles down at his shoes, "
         "not listening. Jake speaks the complete reference audio exactly "
         "once, nothing added."),
        ("b2b", ["b2_2_david"],
         "Night rooftop. David steps INTO Jake's space, chin out, insolent "
         "smile, and delivers his answer; the smile drops entirely on his "
         "last five words. Jake does not step back. Marco and Rachel go very "
         "still behind them."),
    ],
    "b4": [
        ("b4a", ["b4_1_marco"],
         "Barn at night, the argument at full boil. Marco counts the "
         "accusations on his fingers, furious, voice cracking; David paces "
         "like a caged thing on the far side of the lantern; Jake keeps an "
         "arm out between them."),
        ("b4b", ["b4_2_david"],
         "Barn at night. David explodes back, jabbing a finger across the "
         "lantern light, pacing, his voice breaking with real hurt in the "
         "middle — for one second he is just a kid — then the mask slams "
         "back down. The others look away, having no answer."),
    ],
    "c1": [
        ("c1a", ["c1_1_jake"],
         "Barn, late, everyone wrung out. Jake, dirt-streaked and shaken, "
         "sits with forearms on his knees and works through the impossible "
         "options flat and exhausted, one by one on his fingers. Silence "
         "between his sentences. The Andalite in the shadows watches."),
        ("c1b", ["c1_2_cassie"],
         "Barn, a beat later. Cassie steps forward into the lantern light "
         "and delivers her lines quietly, sadly, absolutely sure — and the "
         "room turns to look at her, one face at a time."),
    ],
    "c2": [
        ("c2a", ["c2_1_tobias"],
         "Barn at night. The red-tailed hawk back-wings down onto the rafter "
         "with a whump of air; everyone below spins to look up. Tobias's "
         "thought-speak is dry, wry, gloriously alive; the hawk cocks its "
         "head and its beak NEVER moves."),
        ("c2b", ["c2_2_rachel"],
         "Barn at night. Rachel stares up at the hawk on the rafter, grief "
         "collapsing into disbelieving joy; she laughs once — half a sob — "
         "and delivers her warning pointing a finger up at the bird, "
         "wet-eyed, grinning."),
    ],
    "c4": [
        ("c4a", ["c4_1_jake"],
         "THE STAGED MEETING, camera at floor level: in the sharp foreground "
         "a brown rat crouches in the gap under the floorboards, ears "
         "twitching, lamplight in its black eyes; beyond it, slightly soft, "
         "Jake announces the plan to the circle a shade too loudly, like a "
         "bad actor selling a line. Nobody looks at the floor."),
        ("c4b", ["c4_2_marco", "c4_3_jake"],
         "Floor-level: the rat's whiskers tremble as it drinks in every "
         "word. Beyond it Marco protests on cue, arms thrown wide; Jake "
         "hammers the final word and lets it hang. The lantern gutters. "
         "Nobody looks at the floor."),
    ],
    "c9": [
        ("c9a", ["c9a_1_ax"],
         "The two-hour wait, sun high and hard. The ring of animals — "
         "grizzly, gorilla, wolf, tiger — statue-still around the rock "
         "crevice; the Andalite stands over the huddled rat, both stalk "
         "eyes bent down on it. Ax's thought-speak counts off the time, a "
         "long pause with only surf in it, then the verdict, with quiet "
         "ceremony. Nothing on screen moves its mouth."),
        ("c9b", ["c9b_1_ax"],
         "The ring does not move. The rat presses itself smaller against "
         "the stone as Ax's thought-speak pronounces the sentence — slow, "
         "formal, almost pitying — both stalk eyes never leaving it. "
         "Nothing on screen moves its mouth."),
        ("c9c", ["c9c_1_jake"],
         "The ring breaks: Jake's thought-speak comes drained and final; "
         "the tiger turns away first, then the bear, gorilla and wolf peel "
         "off one by one across the tide pools, leaving the Andalite alone "
         "over the crevice a moment longer."),
    ],
}
SPLIT_LOCKS = {"c9": [AND, THOUGHT], "c2": [THOUGHT]}
SPLIT_ANCHORS = {
    "a4": ["marco", "jake"],
    "b2": ["jake", "david", "marco", "rachel", "loc_hotel"],
    "b4": ["marco", "david", "jake", "rachel"],
    "c1": ["jake", "cassie", "rachel", "marco", "ax"],
    "c2": ["tobias", "rachel", "jake", "cassie"],
    "c4": ["jake", "rachel", "cassie", "marco", "ax"],
    "c9": ["ax", "loc_cove"],
}

# silent shots: (name, duration, staging) — no audio refs
SILENT = {
    "a1": (7, "Night construction site. David slips through the chain-link gap, "
              "flashlight sweeping across mud and plywood skeletons — the beam "
              "snags on a buried blue glow. He kneels, digs with his fingers, "
              "and lifts the glowing blue cube free, turning it in the light, "
              "blue on his face, a slow grin spreading. Crickets, distant "
              "traffic, breath. No dialogue."),
    "a3": (5, "Title card. The steel letters hang over the night construction "
              "site exactly as in the start image; the buried blue glow "
              "pulses slowly beneath the mud; dust motes drift through the "
              "moonlight. The text stays EXACTLY as in the start image, "
              "unchanged, legible, never morphing. Low ominous hum. No "
              "dialogue."),
    "a5": (7, "Night raid, dread, discreet. The black dropship holds station "
              "over the rooftops; the three bladed alien soldiers stride "
              "across the lawn and smash through the front door; red beam "
              "light strobes the windows; a dog barks frantically; the porch "
              "light dies. Seen from across the street, static camera. No "
              "gore, nobody harmed on screen. No dialogue."),
    "b7b": None,  # defined in SHOTS (silent but with staging there)
}

def adur(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


A = "animorphs_david/anchors"
F = "animorphs_david/frames"
HB_A = "animorphs/anchors"

def ref_path(r):
    if r.startswith("loc_") or (HERE / "anchors" / f"{r}.png").exists():
        return f"{A}/{r}.png"
    return f"{HB_A}/{r}.png"

lines_out = [
    "#!/bin/bash",
    "# dv1 first pass (auto-generated by make_videos_dv1.py)",
    "# Run: python3 pool_run.py animorphs_david/videos_dv1.sh animorphs_david/outputs/dv1",
]

def emit(name, frame, staging, anchors, locks, afiles):
    if afiles:
        chars = [p.stem.rsplit("_", 1)[1] for p in afiles]
        speech = sum(adur(p) for p in afiles)
        dur = min(15, max(5, int(speech + 2.5 + len(afiles) * 0.8)))
        order = "; ".join(f"audio clip {n} is spoken by {CHAR_DESC[c]}"
                          for n, c in enumerate(chars, 1))
        audio_lock = (f"The characters speak EXACTLY the dialogue heard in the "
                      f"reference audio clips, in order, in exactly those voices — "
                      f"never any other voice: {order}. Visible human speakers "
                      f"lip-sync precisely; thought-speak voices play over an "
                      f"unmoving mouth. No dialogue beyond the reference audio.")
        auds = " ".join(f"--audio animorphs_david/vo/{p.name}" for p in afiles)
    else:
        dur, audio_lock, auds = 8, "No dialogue anywhere in the clip.", ""
    prompt = " ".join([staging, audio_lock] + locks + [NEG])
    refs = " ".join(f"--image {ref_path(a)}" for a in anchors)
    lines_out.append(
        f'gen {name} {dur} "{prompt}" --start-image {F}/{frame}.png {refs} {auds}'.strip())


# dialogue shots (split parents handled below)
for shot, (staging, anchors, locks) in SHOTS.items():
    if shot in SPLITS:
        continue
    afiles = ([VO / f"{shot}_{n}_{c}.mp3" for n, (c, _) in enumerate(LINES[shot], 1)]
              if shot in LINES else [])
    emit(shot, shot, staging, anchors, locks, afiles)

# split shots: share the parent's frame/anchors/locks
for parent, subs in SPLITS.items():
    if parent in SHOTS:
        _, anchors, locks = SHOTS[parent]
    else:
        anchors, locks = SPLIT_ANCHORS[parent], SPLIT_LOCKS.get(parent, [])
    for sub, stems, staging in subs:
        emit(sub, parent, staging, anchors, locks,
             [VO / f"{s}.mp3" for s in stems])

# pure silent shots
for shot, spec in SILENT.items():
    if spec is None:
        continue
    dur, staging = spec
    prompt = f"{staging} {NEG}"
    extra_refs = {"a1": ["david"], "a5": ["esplin"], "a3": []}[shot]
    refs = " ".join(f"--image {ref_path(r)}" for r in extra_refs)
    lines_out.append(
        f'gen {shot} {dur} "{prompt}" --start-image {F}/{shot}.png {refs}'.strip())

# remaining silent shots that live in frames but not SHOTS/SILENT above
EXTRA_SILENT = {
    "a8": None, "b3": None, "b5": None, "b7b": None, "c3": None,  # already in SHOTS
    "c13": (8, "High wide aerial, dusk. The camera holds, then pulls slowly up "
               "and back from the barren rock island — the tiny grey speck of "
               "the rat alone at its center — surf ringing it white, gulls "
               "wheeling below the lens, the ocean going dark toward the "
               "horizon. Wind and gulls and surf. Slow fade to black at the "
               "very end. No dialogue."),
}
for shot, spec in EXTRA_SILENT.items():
    if spec is None:
        continue
    dur, staging = spec
    lines_out.append(
        f'gen {shot} {dur} "{staging} {NEG}" --start-image {F}/{shot}.png')

out = HERE / "videos_dv1.sh"
out.write_text("\n".join(lines_out) + "\n")
n = sum(1 for l in lines_out if l.startswith("gen "))
total = sum(int(l.split()[2]) for l in lines_out if l.startswith("gen "))
print(f"wrote {out} ({n} shots, ~{total}s of film, ~{total*3} credits at std)")
