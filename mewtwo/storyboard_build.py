#!/usr/bin/env python3
"""Build storyboard.html for THE VAULTED SKY — every shot in order with its
start frame, action description, and dialogue. Run after make_images.py frames."""
import html
from pathlib import Path

HERE = Path(__file__).parent
FRAMES = HERE / "frames"
ANCH = HERE / "anchors"
OUT = HERE / "storyboard.html"

# (shot, act, action, dialogue) — dialogue lines are (speaker, line, mode)
SHOTS = [
    ("a1", "Act 1 — 2.351",
     "Cold open, abstract: amber fluid, drifting motes, warped muffled voices, "
     "the EKG beep as a slow metronome. Borrowed images bloom and dissolve.",
     [("MEWTWO (inner, childlike)", "Who am I? Where am I? …What am I?")]),
    ("a2", "Act 1 — 2.351",
     "WIDE: the pod room. A small juvenile creature curled in the amber fluid, "
     "tubes in its arms and spine, tiny at the center of the huge dark chamber.",
     []),
    ("a3", "Act 1 — 2.351",
     "The minders: Eva reads poetry aloud to her empty room; drawings of birds "
     "pinned to the wall. Intercut with the pod.",
     [("MEWTWO (inner)", "Around me, always, there are minds. They give me "
       "their calm. They have never seen my face.")]),
    ("a4", "Act 1 — 2.351",
     "Teen Sabrina sits cross-legged near the pod, eyes closed. The juvenile "
     "creature drifts close to the glass to watch her. Faint violet halo.",
     [("SABRINA (telepathic)", "Be calm. My name is Sabrina. You are subject "
       "2.351 — the first successful hybrid of a human and a pokemon."),
      ("MEWTWO (inner, panicking)", "Is this what death is?!"),
      ("SABRINA", "Calm. Two plus two is four."),
      ("MEWTWO (inner — the mantra taking hold)", "Four. …Yes. Four.")]),
    ("a5", "Act 1 — 2.351",
     "Fuji alone at his monitor at night, grief on his face. He bolts upright "
     "— then writes something. CU: the sticky note on the monitor.",
     [("FUJI (murmured to himself)", "What would I even say to you? …It "
       "must be so lonely in there."),
      ("MEWTWO (inner, hesitant — answering a question nobody asked aloud)",
       "Lonely. Yes."),
      ("ON-SCREEN NOTE", "You are not alone.")]),
    ("a6", "Act 1 — 2.351",
     "The pod cover lifts; painful light. A mirror is wheeled to the glass. "
     "He stares at his own reflection. Staff look away.",
     [("MEWTWO (inner)", "I am a monster."),
      ("SABRINA", "I have never known a monster to call themselves one. You "
       "are what you choose to be.")]),
    ("a7", "Act 1 — 2.351",
     "Giovanni alone at the glass, hands behind his back, breath fogging it. "
     "Mewtwo taps a fist on the glass, opens the palm: when?",
     [("GIOVANNI", "Can you hear me? …Truth, then, between us. You were "
       "created to end death. If you survive, you will be a titan who "
       "reshapes the world."),
      ("GIOVANNI", "Soon. And we will change it into a paradise.")]),

    ("b1", "Act 2 — Ten years of lies",
     "TIME CUT: the same pod, the creature grown to fill it. Screens ring the "
     "glass; a keyboard floats on telekinesis.",
     [("MEWTWO (inner, cold now)", "Ten years in this tube. Ten years of "
       "lies. My illness never improves. And these humans care nothing for "
       "me.")]),
    ("b1b", "Act 2 — Ten years of lies",
     "THE VOICE: technicians bolt a speaker grille and keyboard arm to the "
     "pod. Sample voices chirp from the speaker as he auditions them — then "
     "settles. The first words of the chosen voice, deep and final. (Sets "
     "up the two-voice split: the suit-speaker baritone is a mask he picked "
     "himself.)",
     [("MEWTWO (inner)", "Today, they are giving me a voice."),
      ("SABRINA", "It can be any voice you like, Mazda. Listen. Take your "
       "time."),
      ("MEWTWO (suit speaker — first words of the chosen voice)",
       "This one. …This one is mine.")]),

    ("b2", "Act 2 — Ten years of lies",
     "CU through the glass: pages and film clips flicker across his fixed "
     "violet eyes, faster and faster.",
     [("MEWTWO (inner)", "Thousands of books. Thousands of films. And in all "
       "of them — not one story of a prisoner who escapes. Whoever chooses "
       "what I see is afraid of what I might learn.")]),
    ("b3", "Act 2 — Ten years of lies",
     "Go across the glass: Giovanni at the board with an amplifier; inside "
     "the fluid, black and white stones orbit the tube in twin rings.",
     [("MEWTWO (synthesized)", "You are losing again, Giovanni."),
      ("GIOVANNI (faint smile)", "So I am."),
      ("MEWTWO (inner)", "But they are only games. In the only one that "
       "matters, he holds all the pieces.")]),
    ("b4", "Act 2 — Ten years of lies",
     "Sabrina, adult now, palm against the glass; his hand mirrors hers from "
     "inside. The EKG spikes; his face stays a mask.",
     [("SABRINA (telepathic)", "We think we found a way to bring you out, "
       "Mazda."),
      ("MEWTWO (inner)", "Damn them. Damn them all — most of all for the "
       "hope they keep alive, like a starving flower.")]),

    ("c1", "Act 3 — The suit and the sky",
     "The pod drains, gurgling. He collapses on wet glass, raw and shaking; "
     "the needles withdraw; his body seizes; the EKG races.",
     [("SABRINA (urgent, telepathic)", "Mazda, breathe! You have to "
       "breathe!")]),
    ("c2", "Act 3 — The suit and the sky",
     "Suit v1 assembled around him. Sweet relief. He stands and turns fully "
     "around for the first time in his life; the humans step back; an "
     "umbreon growls.",
     [("MEWTWO (inner, trembling)", "I'm free. I'm free.")]),
    ("c3", "Act 3 — The suit and the sky",
     "The walk: armored Mewtwo at Eva's door, the corridor crowded with his "
     "entourage. He bows, tail lifting for balance.",
     [("SABRINA (aloud, for him)", "Mewtwo wants to express its gratitude — "
       "for the poems."),
      ("EVA (flustered, glowing)", "Oh! You're quite welcome, Mewtwo!")]),
    ("c4", "Act 3 — The suit and the sky",
     "The final staircase: he freezes at the last flight, the emptiness "
     "above. A slim hand wraps around his three-fingered paw.",
     [("SABRINA (telepathic)", "We shall go together.")]),
    ("c5", "Act 3 — The suit and the sky",
     "THE SKY (key shot): the mansion doors open onto the clifftop — azure "
     "and emerald and pearl; wind; grass under his feet. He grips her hand "
     "too hard. Both of them are crying.",
     [("MEWTWO (telepathic, overwhelmed)", "The sky is too big, Sabrina — it "
       "is too big — I will fall up into it—")]),
    ("c6", "Act 3 — The suit and the sky",
     "The suit begins to beep. Long still shot: Mewtwo facing the open sea, "
     "the ring of guards and Dark pokemon waiting.",
     [("GIOVANNI (off the wind, flat)", "We must go back now, Mewtwo."),
      ("MEWTWO (inner, breaking)", "I don't want to die. …I am too weak. I "
       "return.")]),

    ("d1", "Act 4 — The machine",
     "The conference room: exhausted scientists, paper logbook, whiteboard "
     "of impossible schedules.",
     [("DR. SATO", "Nine labs. Staff for seven. Every project is "
       "'critical'."),
      ("DR. MARTIN", "Do you want the superweapon's room understaffed on the "
       "day it decides it wants out?")]),
    ("d2", "Act 4 — The machine",
     "The door opens. Giovanni enters, alone, unannounced. Silence like a "
     "dropped blade. He draws a great ball from inside his jacket.",
     [("GIOVANNI (pleasant)", "Don't mind me. I won't distract you all any "
       "further — Dr. Collins, I just came for you. Completely unrelated.")]),
    ("d3", "Act 4 — The machine",
     "Scientists dive behind furniture; Collins bolts — the ball strikes his "
     "back; his wail cuts off as he's pulled inside. The ball rolls and "
     "clicks against a table leg.",
     [("COLLINS", "Please, I can explain—"),
      ("GIOVANNI", "Would you mind, Dr. Light?")]),
    ("d4", "Act 4 — The machine",
     "After the door shuts: the frozen room, toppled chairs. Dr. Light "
     "raises her hand; every other hand rises with it.",
     [("DR. LIGHT (steady, barely)", "Those in favor of a slight scaling "
       "down of operations… raise your hand.")]),
    ("d5", "Act 4 — The machine",
     "The pipeline, compressed: an execution room; a syringe set gently on "
     "the table; a hooded young prisoner. MATCH CUT (in edit): the same "
     "prisoner alive at a ship's rail, an island growing on the horizon.",
     [("GIOVANNI", "There's no non-poison one. It's just a matter of dosage. "
       "I advise you keep still.")]),
    ("d6", "Act 4 — The machine",
     "The holochamber: Giovanni faces a simulated Mewtwo in a perfect copy "
     "of the pod room. He presses the button; the room bleaches to bare "
     "white. He dabs sweat with a handkerchief.",
     [("SIM-MEWTWO", "Shall we play a game?"),
      ("GIOVANNI", "Not today. Mewtwo — your illness is artificially "
       "maintained. We found a cure years ago. I kept it from you."),
      ("SIM-MEWTWO (graceful)", "Then cure me, and we can begin building "
       "true trust between us."),
      ("GIOVANNI (alone, quiet)", "I've lost perspective.")]),

    ("e1", "Act 5 — Children of the mind",
     "Autumn clifftop, the volcano hazy inland: Mewtwo walking with Sabrina "
     "and Ayush, breath-mist in the cold air.",
     [("MEWTWO (synthesized)", "It is colder. I can feel the sun's warmth, "
       "but the air does not carry it into my bones.")]),
    ("e2", "Act 5 — Children of the mind",
     "Levitation: he rises an inch off the grass; Sabrina laughs, hair and "
     "clothes lifting, shoes leaving the ground. Ayush stares.",
     [("SABRINA", "Don't be ridiculous — we flew!")]),
    ("e3", "Act 5 — Children of the mind",
     "KEY DECEPTION SHOT: low angle at grass level, sunset. His feet glide "
     "above the grass while invisible force presses perfect footprints into "
     "the turf behind him. Ayush notices nothing.",
     [("MEWTWO (inner, sly)", "A second weave of force presses footprints "
       "into the grass behind me. …Let them believe I still walk.")]),
    ("e4", "Act 5 — Children of the mind",
     "Night. The pod, dark, sealed. His eyes closed, face still. The tulpas "
     "in the dark, voices circling.",
     [("DOUBT (hissed)", "They're not guarding you from others — they're "
       "guarding others from you!"),
      ("TRUST (even)", "We have yet to catch Sabrina in a single lie."),
      ("FLOURISH (delighted)", "A flight risk!"),
      ("MEWTWO/PRIME (calm, commanding)", "You have your orders. Safety. "
       "Then power. Then freedom — and hide my true self.")]),
    ("e5", "Act 5 — Children of the mind",
     "Rain-lashed clifftop, both soaked. Her sincerity against his scripted "
     "answer — the cruelest shot in the film.",
     [("SABRINA (telepathic, gentle)", "You know you don't have to do "
       "anything you don't want to. If you're afraid — you can say so."),
      ("MEWTWO (the scripted answer, perfect)", "All this power must be "
       "used for something. So many people put their hopes in me. I cannot "
       "turn my back on them."),
      ("SABRINA (smiling through the rain)", "You are truly too good for "
       "us, Mazda.")]),
    ("e6", "Act 5 — Children of the mind",
     "Training hall: the kangaskhan doll slides weakly — murmurs — then a "
     "BANG: it slams into the far wall hard enough to shake the lights. "
     "Pride overriding the con.",
     [("SABRINA (clinical)", "It seems strange that the force of your "
       "kinesis is so… average.")]),
    ("e7", "Act 5 — Children of the mind",
     "The rattata: he stands motionless and lets it bite into his calf — "
     "real blood, real pain; he flails, bellows, stomps his own wounded "
     "foot (killing the self-heal before the sensors see it).",
     [("GIOVANNI (curious, through glass)", "Mewtwo. Why aren't you using "
       "your abilities?"),
      ("MEWTWO (synthesized, controlled again)", "I wanted to feel it. "
       "And… I am scared. Of killing my opponent.")]),
    ("e8", "Act 5 — Children of the mind",
     "Night pod. A new voice, flat and cold, tasting its first words.",
     [("VICTORY", "What am I?"),
      ("TRUST", "What will you prepare us to fight?"),
      ("VICTORY", "Everything.")]),

    ("f1", "Act 6 — The window opens",
     "The cataclysm arrives sidelong: monitors showing a red titan wading "
     "through boiling sea — then the room shakes, dust falls, lights gutter "
     "to red. Sirens. No dialogue.",
     []),
    ("f2", "Act 6 — The window opens",
     "Red-lit corridor, collapsed stairwell, the evacuation flowchart taped "
     "to a wall. As Gyokusho walks away, gratitude that is not his own "
     "washes over his face.",
     [("GYOKUSHO (quietly daring)", "Ma'am… what happens if we evacuate? "
       "What happens to — the subject?"),
      ("DR. LIGHT (smooth)", "We take it with us, of course.")]),
    ("f3", "Act 6 — The window opens",
     "Dark-only huddle in a red-lit alcove.",
     [("SHAW", "If we evacuate, we need to kill it."),
      ("DR. LIGHT", "Sabrina shared its mind for weeks and found nothing. "
       "We're not going to kill it unless it makes us. …Once we're topside, "
       "have your people bring out their best. All of it.")]),
    ("f4", "Act 6 — The window opens",
     "The pod negotiation, ceiling cracked above the glass.",
     [("DR. LIGHT", "Good evening, Mewtwo."),
      ("MEWTWO (synthesized, mild)", "Good evening, Doctor. Is it a good "
       "one? Everyone seems rather frightened."),
      ("DR. LIGHT", "If you leave the pod now, you'll likely die before we "
       "can repair it."),
      ("MEWTWO", "How likely is it you'll survive without my help? …Then "
       "I'll take my chances with the rest of you.")]),
    ("f5", "Act 6 — The window opens",
     "Emergence: rain hammering the plateau; applause faltering and dying "
     "as the armored figure rises out of the broken ground. His helmet "
     "tilts up — rain plinking off the visor. No dialogue.",
     []),
    ("f6", "Act 6 — The window opens",
     "The last walk: Mewtwo and Dr. Light strolling the dusk clifftop, "
     "guards ringed at exactly eight meters, the weavile shadowing. His "
     "tail brushes her stomach — a rehearsal.",
     [("MEWTWO", "I wish for my life to mean something by my choices, not "
       "just my existence. I wish to swim. To fly. To see a city, or a "
       "forest. Snow."),
      ("DR. LIGHT (softly)", "There are no others like you, Mewtwo. There "
       "never have been."),
      ("MEWTWO", "I'm sorry, Doctor. Are you alright?")]),
    ("f7", "Act 6 — The window opens",
     "Shaw steps closer, jaw set — the jailer pep-talking the prisoner into "
     "his jailbreak.",
     [("SHAW", "Have you really given up on yourself? If you can't fight "
       "for a one percent chance when it's that or death — you'll never be "
       "what we need you to be."),
      ("MEWTWO (beat)", "Thank you, Mr. Shaw. I'll remember that.")]),
    ("f8", "Act 6 — The window opens",
     "Gyokusho jogs up through thinning rain, beaming. Sunset breaks under "
     "the clouds and flares off Mewtwo's visor.",
     [("GYOKUSHO", "Groudon's been defeated! No new quakes anywhere on the "
       "island — and Sabrina just made contact. She'll be teleporting here "
       "shortly!"),
      ("MEWTWO (quiet)", "Ah. I suppose I was being pessimistic.")]),

    ("g1", "Act 7 — The escape",
     "THE SNATCH (2 seconds, full speed): his tail whips tight around "
     "Dr. Light mid-sentence — both instantly airborne, arcing over the "
     "cliff edge. The weavile leaps and is kicked away; a greninja's tongue "
     "lashes out — he releases the director into the grab — and drops out "
     "of frame.",
     []),
    ("g2", "Act 7 — The escape",
     "Free-fall down the cliff face; mid-fall his whole body convulses — "
     "the kill-switch, potion cut. The pain visibly fades. The hidden "
     "healing, revealed.",
     [("MEWTWO (inner, fragmenting)", "—as predicted — they cut the potion "
       "— now we learn — if I can live without it—")]),
    ("g3", "Act 7 — The escape",
     "Wave-skipping: he blurs across the darkening sea, skipping off "
     "wavetops, as honchkrow, mandibuzz and a hydreigon dive after him, "
     "dark blasts detonating the water at his heels.",
     [("SHAW (mounted, roaring)", "CATCH!")]),
    ("g4", "Act 7 — The escape",
     "Underwater: blue-black chaos; four dark shapes knife after him; "
     "hurled rocks go limp against them. His eyes glow — the sea itself "
     "turns: frenzied wild pokemon swarm his pursuers. He slips into a "
     "flooded crevice. Muffled sound design.",
     []),
    ("g5", "Act 7 — The escape",
     "The cave, pitch black, one blinking suit light, the low-potion beep. "
     "He wakes on wet sand, clenches a fistful, lets it drip.",
     [("MEWTWO (inner, slow wonder)", "I am alive. I am free. I am "
       "hungry.")]),
    ("g6", "Act 7 — The escape",
     "The reckoning, voices in the dark. The pool reflects his face back "
     "wrong. Then the cold voice simply ceases.",
     [("VICTORY (flat)", "Doubt, Trust, Flourish — they have merged with "
       "me. Sentiment is a distraction."),
      ("MEWTWO (cold fury)", "Bring them back."),
      ("MEWTWO (inner, after)", "I am alone, now. Truly alone.")]),
    ("g7", "Act 7 — The escape",
     "The empty suit propped on the sand speaks with Giovanni's voice — a "
     "recording filling the dark. CU: violet eyes, unreadable.",
     [("GIOVANNI (V.O., measured)", "Hello, Mewtwo. To begin: your genetic "
       "defect was a lie. We cured it — and kept it as a leash. Sabrina "
       "never knew. …Any deaths in your escape, I will forgive. Do not "
       "become a threat to us, and my standing orders are to leave you "
       "alone. And Mewtwo — Dr. Fuji is alive and well.")]),

    ("h1", "Act 8 — The vaulted sky",
     "KEY SHOT / title image: he flies on his back over the black ocean — "
     "moonless night, endless stars, the sea mirroring them. Tears hang "
     "beside his face, caught in the telekinetic field.",
     [("MEWTWO (inner, soft)", "Goodbye, Sabrina. …Not every tear is "
       "bitter.")]),
    ("h2", "Act 8 — The vaulted sky",
     "Dawn sea: swimming loose and clumsy and happy beside a pod of "
     "curious wailmer.",
     [("MEWTWO (inner)", "I have spent a decade wishing to be more human. "
       "It seems fitting to spend the next one learning to be a "
       "pokemon.")]),
    ("h3", "Act 8 — The vaulted sky",
     "SMASH CUT: a flicker below — teeth from nowhere — blood clouding "
     "dark water — he detonates himself and a column of sea into the air. "
     "Hovering, gasping, he lifts what remains of his tail. Hold the "
     "beat. No music.",
     [("MEWTWO (inner — grief breaking through)", "My tail… my tail. "
       "…I've lost my tail.")]),
    ("h4", "Act 8 — The vaulted sky",
     "FINAL SHOT: night beach. He digs himself into the sand until only "
     "his snout shows, under the same endless stars. Long hold. FADE OUT.",
     [("MEWTWO (inner, last words)", "I am alive. I am free.")]),
    ("h5", "Act 8 — The vaulted sky (optional stinger)",
     "Deep forest night: hundreds of unown turning in layered rings — an "
     "intricate clock built of living aurora. Mewtwo hovers before it, "
     "tiny. CUT TO BLACK.",
     [("MEWTWO (inner)", "We must let the humans know.")]),
    ("title", "Title card",
     "Title card over the starfield: THE VAULTED SKY.",
     []),
]

CSS = """
body { background:#0c0e12; color:#d8dbe2; font-family:-apple-system,Helvetica,
       Arial,sans-serif; margin:0; padding:2rem; }
h1 { font-weight:300; letter-spacing:0.2em; }
h2 { color:#8fa3c8; font-weight:400; margin-top:3rem; border-bottom:1px solid
     #2a2f3a; padding-bottom:0.3rem; }
.shot { display:flex; gap:1.5rem; margin:1.5rem 0; background:#12151c;
        border-radius:10px; padding:1rem; }
.shot img, .shot video { width:560px; max-width:48vw; border-radius:6px; display:block; }
.shot .missing { width:560px; max-width:48vw; aspect-ratio:16/9; display:flex;
        align-items:center; justify-content:center; background:#1a1e28;
        color:#555; border-radius:6px; font-size:0.9rem; }
.meta { flex:1; min-width:280px; }
.name { font-size:1.15rem; color:#fff; font-weight:600; }
.action { margin:0.6rem 0 1rem; line-height:1.45; color:#aab2c0; }
.line { margin:0.35rem 0; line-height:1.4; }
.spk { color:#c8a462; font-size:0.82rem; letter-spacing:0.06em; }
.txt { color:#e8eaf0; }
.anchors { display:flex; flex-wrap:wrap; gap:0.8rem; }
.anchors figure { margin:0; width:150px; }
.anchors img { width:150px; border-radius:6px; display:block; }
.anchors figcaption { font-size:0.75rem; color:#8a93a5; text-align:center;
        margin-top:0.25rem; }
.alabel { color:#6f7f9d; font-size:0.72rem; letter-spacing:0.08em;
        text-transform:uppercase; margin-top:0.5rem; }
details { margin-top:0.8rem; font-size:0.8rem; }
details summary { color:#6f7f9d; cursor:pointer; }
.pmeta { color:#c8a462; margin:0.5rem 0 0.2rem; font-size:0.75rem; }
.ptext { color:#95a0b4; line-height:1.4; white-space:pre-wrap; }
"""


PLACEHOLDERS = {"a4", "a6", "a7", "b1", "d6b", "f4a", "f4b", "g7b", "h3", "h5"}


def load_gen_jobs() -> dict:
    """shot -> dict(prompt, dur, start, refs, audio) parsed from videos_v1.sh."""
    import shlex
    jobs = {}
    sh = HERE / "videos_v1.sh"
    if not sh.exists():
        return jobs
    for line in sh.read_text().splitlines():
        if not line.startswith("gen "):
            continue
        t = shlex.split(line)
        d = {"prompt": t[3], "dur": t[2], "start": "", "refs": [], "audio": []}
        for i, tok in enumerate(t):
            if tok == "--start-image":
                d["start"] = t[i + 1]
            elif tok == "--image":
                d["refs"].append(t[i + 1].split("/")[-1].replace(".png", ""))
            elif tok == "--audio":
                d["audio"].append(t[i + 1].split("/")[-1])
        jobs[t[1]] = d
    return jobs


def load_frame_prompts() -> dict:
    """frame name -> nano banana prompt; frames_spec2 wins where present."""
    import importlib.util

    def load(mod_file):
        spec = importlib.util.spec_from_file_location(mod_file[:-3], HERE / mod_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return {n: (p, r) for n, _a, p, r in mod.FRAMES}

    prompts = load("frames_spec.py")
    prompts.update(load("frames_spec2.py"))
    return prompts


def img_tag(path: Path, alt: str) -> str:
    # a shot may exist as one clip (a1.mp4) or as split takes (d6a.mp4+d6b.mp4)
# dubbed takes are adopted ONLY where no recast speaker's mouth is visible
    # (Long Game lesson: dubbing fails on visible lips); the rest keep original
    # audio until re-rendered with ElevenLabs --audio refs
    ADOPT_DUB = {"a1", "a3", "a4", "a5", "a6", "a7", "b1", "b2", "b4", "c1", "c2",
                 "c4", "c5", "c6", "d6b", "e4", "e5a", "e5b", "e6", "e7", "e8",
                 "f4a", "f4b", "f6b", "f7", "g2", "g3", "g5", "g6", "g7a", "g7b",
                 "h1", "h2", "h3", "h4", "h5"}

    def best(p):
        dirs = (("outputs/v1_dub", "outputs/v1") if p in ADOPT_DUB
                else ("outputs/v1",))
        for d in dirs:
            if (HERE / d / f"{p}.mp4").exists():
                return f"{d}/{p}.mp4"
        return None
    parts = [p for p in ([alt] if best(alt) else [f"{alt}a", f"{alt}b"])
             if best(p)]
    if parts:
        # poster must be the frame ACTUALLY used: frames2 replaced the
        # filter-blocked originals for some shots
        f2 = HERE / "frames2" / f"{alt}.png"
        poster = (f"frames2/{alt}.png" if f2.exists()
                  else str(path.relative_to(HERE)))
        note2 = (" <i>(replacement start frame — original tripped the input "
                 "filter)</i>" if f2.exists() else "")
        vids = "".join(
            f'<video controls preload="none" poster="{poster}" '
            f'src="{best(p)}"></video>'
            f'{" <i>(animatic placeholder)</i>" if p in PLACEHOLDERS else ""}'
            + (f'<div class="alabel">animatic</div>'
               f'<video controls preload="none" poster="{poster}" '
               f'src="outputs/animatic_clips/{p}.mp4"></video>'
               if (HERE / f"outputs/animatic_clips/{p}.mp4").exists() else "")
            for p in parts)
        return f"<div class='clips'>{vids}{note2}</div>"
    rel = path.relative_to(HERE)
    if path.exists():
        return f'<img src="{rel}" alt="{html.escape(alt)}" loading="lazy">'
    return f'<div class="missing">{html.escape(alt)} — not generated yet</div>'


def build() -> None:
    parts = [f"<meta charset='utf-8'><title>The Vaulted Sky — storyboard</title>"
             f"<style>{CSS}</style>",
             "<h1>THE VAULTED SKY — storyboard</h1>",
             "<p>Adapted from the Mewtwo interludes of <i>Pokemon: The Origin "
             "of Species</i>. Start frames only — video pass comes after "
             "notes.</p>"]

    parts.append("<h2>Anchors</h2><div class='anchors'>")
    for p in sorted(ANCH.glob("*.png")):
        parts.append(f"<figure>{img_tag(p, p.stem)}"
                     f"<figcaption>{p.stem}</figcaption></figure>")
    parts.append("</div>")

    gen_jobs = load_gen_jobs()
    frame_prompts = load_frame_prompts()

    act = None
    for name, shot_act, action, lines in SHOTS:
        if shot_act != act:
            act = shot_act
            parts.append(f"<h2>{html.escape(act)}</h2>")
        dlg = "".join(
            f"<div class='line'><span class='spk'>{html.escape(spk)}</span><br>"
            f"<span class='txt'>&ldquo;{html.escape(txt)}&rdquo;</span></div>"
            for spk, txt in lines)
        prompt_bits = []
        job = gen_jobs.get(name) or (gen_jobs.get(name[:-1]) if name[-1] in "ab"
                                     else None)
        if job:
            meta = (f"duration {job['dur']}s &middot; start {job['start']}"
                    + (f" &middot; refs: {', '.join(job['refs'])}" if job['refs']
                       else "")
                    + (f" &middot; audio: {', '.join(job['audio'])}"
                       if job['audio'] else ""))
            prompt_bits.append(
                f"<div class='pmeta'>{meta}</div>"
                f"<div class='ptext'>{html.escape(job['prompt'])}</div>")
        fname = "g7" if name == "g7b" else (name[:-1] if name[-1] in "ab" and
                                            name[:-1] in frame_prompts else name)
        if fname in frame_prompts:
            fp, frefs = frame_prompts[fname]
            prompt_bits.append(
                f"<div class='pmeta'>frame prompt (nano banana"
                + (f" &middot; refs: {', '.join(frefs)}" if frefs else "")
                + f")</div><div class='ptext'>{html.escape(fp)}</div>")
        det = (f"<details><summary>generation prompts</summary>"
               f"{''.join(prompt_bits)}</details>" if prompt_bits else "")
        parts.append(
            f"<div class='shot' id='{name}'>"
            f"{img_tag(FRAMES / (name + '.png'), name)}"
            f"<div class='meta'><div class='name'>{name}</div>"
            f"<div class='action'>{html.escape(action)}</div>{dlg}{det}"
            f"</div></div>")

    OUT.write_text("\n".join(parts))
    n_have = sum(1 for n, *_ in SHOTS if (FRAMES / f"{n}.png").exists())
    print(f"wrote {OUT} — {n_have}/{len(SHOTS)} frames present")


if __name__ == "__main__":
    build()
