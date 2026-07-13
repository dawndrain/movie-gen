#!/usr/bin/env python3
"""TTS all dialogue lines for THE VAULTED SKY (fixed preset voices).
Output: vo/<shot>_<n>_<char>.mp3. Skips existing. Also builds vo_auditions/."""
import re
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
VO = HERE / "vo"
VO.mkdir(exist_ok=True)

VOICES = {  # character -> (preset name, voice_id)
    # Mewtwo's one voice in all registers (synth / telepathic / tulpas) — cold,
    # silky, deep (Roman was Esplin in Hork-Bajir: proven measured delivery).
    "mewtwo":   ("Roman",    "7e63ac18-5fcd-4aba-8078-a86d4e11c127"),
    "sabrina":  ("Imogen",   "3811e986-0891-47cf-a1f5-78a1d62a547a"),
    "giovanni": ("Sterling", "dc382508-c8bd-443c-8cb2-46e57b8d2e6f"),
    "drlight":  ("Nora",     "d081b915-6623-4a44-bacf-80d0f1c90a03"),
    "shaw":     ("Hugo",     "7888649a-b139-4295-a57b-4e103079d817"),
    "eva":      ("Mabel",    "fa64fba4-ad02-405e-99d0-1f085d87c706"),
    "gyokusho": ("Brooks",   "c2acff45-84b2-4974-892d-89fa2d4e5598"),
    "sato":     ("Mark",     "27c04473-84a9-4b60-a41f-c8e8458bd4f1"),
    "martin":   ("Andre",    "f1e8226e-2248-4d5f-b43c-0a79e9949dbf"),
    "collins":  ("Kevin",    "f1373f24-3b96-433f-9a68-e595810ef608"),
}

# shot -> ordered (character, line) pairs. Spelling is PHONETIC/punctuated for TTS.
# "MAZ-dah" pins Mazda; ellipses and dashes shape delivery.
LINES = {
    "a1":  [("mewtwo", "Who am I? Where am I? ... What am I?")],
    "a3":  [("mewtwo", "Around me, always, there are minds. They give me their calm. They have never seen my face.")],
    "a4":  [("sabrina", "Be calm. My name is Sabrina. You are subject two point three five one — the first successful hybrid... of a human, and a pokemon."),
            ("mewtwo", "Is this what death is?!"),
            ("sabrina", "Calm. Two plus two... is four."),
            ("mewtwo", "Four. ... Yes. Four.")],
    "a5":  [("fuji", "What would I even say to you? ... It must be so lonely in there."),
            ("mewtwo", "Lonely. ... Yes.")],
    "a6":  [("mewtwo", "I am a monster."),
            ("sabrina", "I have never known a monster to call themselves one. You are what you choose to be.")],
    "a7":  [("giovanni", "Can you hear me? ... Truth, then, between us. You were created... to end death. If you survive, you will be a titan who reshapes the world."),
            ("giovanni", "Soon. And we will change it... into a paradise.")],
    "b1":  [("mewtwo", "Ten years in this tube. Ten years of lies. My illness never improves. And these humans... care nothing for me.")],
    "b1b": [("mewtwo", "Today, they are giving me a voice."),
            ("sabrina", "It can be any voice you like, MAZ-dah. Listen. Take your time."),
            ("mewtwo", "This one. ... This one is mine.")],
    "b2":  [("mewtwo", "Thousands of books. Thousands of films. And in all of them — not one story of a prisoner who escapes. Whoever chooses what I see... is afraid of what I might learn.")],
    "b3":  [("mewtwo", "You are losing again, Giovanni."),
            ("giovanni", "So I am."),
            ("mewtwo", "But they are only games. In the only one that matters... he holds all the pieces.")],
    "b4":  [("sabrina", "We think we found a way to bring you out, MAZ-dah."),
            ("mewtwo", "Damn them. Damn them all. Most of all... for the hope they keep alive. Like a starving flower.")],
    "c1":  [("sabrina", "MAZ-dah, breathe! You have to breathe!")],
    "c2":  [("mewtwo", "I'm free. ... I'm free.")],
    "c3":  [("sabrina", "Mewtwo wants to express its gratitude. For the poems."),
            ("eva", "Oh! You're quite welcome, Mewtwo!")],
    "c4":  [("sabrina", "We shall go together.")],
    "c5":  [("mewtwo", "The sky is too big, Sabrina — it is too big — I will fall up into it —")],
    "c6":  [("giovanni", "We must go back now, Mewtwo."),
            ("mewtwo", "I don't want to die. ... I am too weak. I return.")],
    "d1":  [("sato", "Nine labs. Staff for seven. And every project is, quote, critical."),
            ("martin", "Do you want the superweapon's room understaffed, on the day it decides it wants out?")],
    "d2":  [("giovanni", "Don't mind me. I won't distract you all any further. Doctor Collins — I just came for you. Completely unrelated.")],
    "d3":  [("collins", "Please — I can explain —"),
            ("giovanni", "Would you mind, Doctor Light?")],
    "d4":  [("drlight", "Those in favor of a slight scaling down of operations... raise your hand.")],
    "d5":  [("giovanni", "There's no non-poison one. It's just a matter of dosage. I advise you keep still.")],
    "d6a": [("mewtwo", "Shall we play a game?"),
            ("giovanni", "Not today. Mewtwo... your illness is artificially maintained. We found a cure, years ago. I kept it from you.")],
    "d6b": [("mewtwo", "Then cure me. And we can begin building true trust between us."),
            ("giovanni", "I've lost perspective.")],
    "e1":  [("mewtwo", "It is colder. I can still feel the sun's warmth... but the air does not carry it into my bones.")],
    "e2":  [("sabrina", "Don't be ridiculous. We flew!")],
    "e3":  [("mewtwo", "A second weave of force presses footprints into the grass behind me. ... Let them believe I still walk.")],
    "e4":  [("mewtwo", "They're not guarding you from others. They're guarding others... from you!"),
            ("mewtwo", "We have yet to catch Sabrina in a single lie."),
            ("mewtwo", "You have your orders. Safety. Then power. Then freedom. And hide my true self.")],
    "e5a": [("sabrina", "You know you don't have to do anything you don't want to. If you're afraid... you can say so.")],
    "e5b": [("mewtwo", "All this power must be used for something. So many people put their hopes in me. I cannot turn my back on them."),
            ("sabrina", "You are truly too good for us, MAZ-dah.")],
    "e6":  [("sabrina", "It seems strange, that the force of your kinesis is so... average.")],
    "e7":  [("giovanni", "Mewtwo. Why aren't you using your abilities?"),
            ("mewtwo", "I wanted to feel it. And... I am scared. Of killing my opponent.")],
    "e8":  [("mewtwo", "What... am I?"),
            ("mewtwo", "What will you prepare us to fight?"),
            ("mewtwo", "Everything.")],
    "f2":  [("gyokusho", "Ma'am... what happens if we do evacuate? What happens to... the subject?"),
            ("drlight", "We take it with us, of course.")],
    "f3":  [("shaw", "If we evacuate, we need to kill it."),
            ("drlight", "Sabrina shared its mind for weeks and found nothing. We're not going to kill it unless it makes us. Have your people bring out their best. All of it.")],
    "f4a": [("drlight", "Good evening, Mewtwo."),
            ("mewtwo", "Good evening, Doctor. Is it a good one? Everyone seems rather frightened.")],
    "f4b": [("drlight", "If you leave the pod now... you'll likely die before we can repair it."),
            ("mewtwo", "How likely is it you'll survive, without my help? ... Then I'll take my chances with the rest of you.")],
    "f6a": [("mewtwo", "I wish for my life to mean something by my choices. Not just my existence. I wish to swim. To fly. To see a city, or a forest. ... Snow."),
            ("drlight", "There are no others like you, Mewtwo. There never have been.")],
    "f6b": [("mewtwo", "I'm sorry, Doctor. Are you alright?")],
    "f7":  [("shaw", "Have you really given up on yourself? If you can't fight for a one percent chance, when it's that or death — you'll never be what we need you to be."),
            ("mewtwo", "Thank you, Mister Shaw. I'll remember that.")],
    "f8":  [("gyokusho", "Groudon's been defeated! No new quakes anywhere on the island — and Sabrina just made contact. She'll be teleporting here shortly!"),
            ("mewtwo", "Ah. I suppose I was being pessimistic.")],
    "g2":  [("mewtwo", "As predicted... they cut the potion. Now we learn... if I can live without it.")],
    "g3":  [("shaw", "CATCH!")],
    "g5":  [("mewtwo", "I am alive. I am free. ... I am hungry.")],
    "g6":  [("mewtwo", "Doubt. Trust. Flourish. They have merged with me. Sentiment... is a distraction."),
            ("mewtwo", "Bring them back."),
            ("mewtwo", "I am alone, now. Truly alone.")],
    "g7a": [("giovanni", "Hello, Mewtwo. To begin: your genetic defect... was a lie. We cured it. And kept it, as a leash. Sabrina never knew.")],
    "g7b": [("giovanni", "Any deaths in your escape, I will forgive. Do not become a threat to us, and my standing orders are to leave you alone. And Mewtwo... Doctor Fuji is alive and well.")],
    "h1":  [("mewtwo", "Goodbye, Sabrina. ... Not every tear is bitter.")],
    "h2":  [("mewtwo", "I have spent a decade wishing to be more human. It seems fitting... to spend the next one, learning to be a pokemon.")],
    "h3":  [("mewtwo", "My tail... my tail. ... I've lost my tail.")],
    "h4":  [("mewtwo", "I am alive. I am free.")],
    "h5":  [("mewtwo", "We must let the humans know.")],
}

AUDITION = ("Ten years in this prison. Ten years of lies. And still, above it all, "
            "the vaulted sky.")


def tts(dest: Path, voice_id: str, text: str) -> str:
    if dest.exists():
        return f"skip {dest.name}"
    cmd = ["higgsfield", "generate", "create", "text2speech_v2",
           "--prompt", text, "--variant", "elevenlabs",
           "--voice_id", voice_id, "--voice_type", "preset", "--wait"]
    for _ in range(3):
        r = subprocess.run(cmd, capture_output=True, text=True)
        urls = re.findall(r"https://\S+\.(?:mp3|m4a|wav)\S*", r.stdout + r.stderr)
        if r.returncode == 0 and urls:
            urllib.request.urlretrieve(urls[-1].rstrip('",'), dest)
            return f"OK   {dest.name}"
    return f"FAIL {dest.name}"


if __name__ == "__main__":
    jobs = []
    for shot, lines in LINES.items():
        for n, (char, text) in enumerate(lines, 1):
            jobs.append((VO / f"{shot}_{n}_{char}.mp3", VOICES[char][1], text))
    aud = HERE / "vo_auditions"
    aud.mkdir(exist_ok=True)
    for char, (name, vid) in VOICES.items():
        jobs.append((aud / f"{char}_{name}.mp3", vid, AUDITION))

    with ThreadPoolExecutor(max_workers=4) as pool:
        for res in pool.map(lambda j: tts(*j), jobs):
            print(res, flush=True)
