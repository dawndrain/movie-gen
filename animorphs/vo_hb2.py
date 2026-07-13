#!/usr/bin/env python3
"""TTS all dialogue lines for the hb2 retake round (fixed preset voices).
Output: vo/<shot>_<n>_<char>.mp3. Skips existing. Also builds vo_auditions/."""
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
VO = HERE / "vo"
VO.mkdir(exist_ok=True)

VOICES = {  # character -> (preset name, voice_id)
    "dak":     ("Gideon",   "1ad38ba4-9cc4-4f2f-9fde-b0fefdf67ae5"),
    "aldrea":  ("Imogen",   "3811e986-0891-47cf-a1f5-78a1d62a547a"),
    "jara":    ("Hugo",     "7888649a-b139-4295-a57b-4e103079d817"),
    "jagil":   ("Brooks",   "c2acff45-84b2-4974-892d-89fa2d4e5598"),
    "elder":   ("Alistair", "d9d5c263-f84e-4752-97b5-3750fcc6fd2f"),
    "seerow":  ("Harrison", "573e5163-59b3-4926-aab1-951ef2985f81"),
    "alloran": ("Sterling", "dc382508-c8bd-443c-8cb2-46e57b8d2e6f"),
    "esplin":  ("Roman",    "7e63ac18-5fcd-4aba-8078-a86d4e11c127"),
    "arn":     ("Julian",   "95429266-c0ac-4137-a209-63b8812b0f23"),
    "toby":    ("Skye",     "1fb253b8-928b-4d29-a349-f242a71eaddf"),
}

HB = "Hork-buh-JEER"          # house pronunciation of Hork-Bajir
KAW = "kah-WAHT-nohj"         # kawatnoj

# shot -> ordered (character, line) pairs. Spelling here is PHONETIC for TTS.
LINES = {
    "f2": [("jara", "Come, Tobias. Sit. I tell you story. Story of before. Story of Dak Hamee... and Al-dree-ah.")],
    "a2": [("aldrea", "You were a prince, father. Now they send you to watch trees grow at the edge of nowhere."),
           ("seerow", "I gave the Yee-erks the stars, Al-dree-ah. Kindness was my crime. We will not speak of it again.")],
    "b2": [("jagil", "Dak Hamee make shapes. Why make shapes?"),
           ("dak", "It is the sky, Jagil. The lights move. I watched. They move in circles.")],
    "b3": [("elder", "Dak Hamee is seer. Born one time in all times. Seer come when change come.")],
    "b4": [("dak", "You are not of the trees. Not of the valley."),
           ("aldrea", "No. I am Al-dree-ah. I come from the sky you watch.")],
    "b5": [("aldrea", "That light is not a hole in the sky, Dak. It is a sun. Like yours. And around it... worlds."),
           ("dak", "Worlds. Dak wants to see.")],
    "b6": [("dak", "Anda-light falls like stone!")],
    "c1": [("aldrea", "My father's instruments found something below the Deep, Dak. Something old. Something alive.")],
    "c3": [("dak", "What... is this place?")],
    "c4": [("arn", f"{HB}. On my doorstep. You were not made to ask questions.")],
    "c5": [("arn", "Long ago, the sky burned. We made the trees to heal the air. And we made you... to tend the trees. Gardeners. Tools. Nothing more.")],
    "c6": [("dak", "I am not a people. I am a tool that learned to dream."),
           ("aldrea", "A tool cannot choose, Dak. You choose. That makes you a people.")],
    "d2": [("esplin", "Scans show no weapons. No metal. No fire. Only bodies. Billions of strong... bladed... bodies.")],
    "d4": [("dak", "Jagil. You did not eat. You do not laugh. Where does Jagil go at night?"),
           ("jagil", "Jagil is here. Jagil is... better now.")],
    "d5": [("seerow", "Al-dree-ah... RUN!")],
    "d6": [("aldrea", "Father. Mother. Barafin. All of them. They are all of them dead.")],
    "e1": [("aldrea", f"The Yee-erks take bodies, Dak. They will take every {HB} in the world, unless we fight."),
           ("dak", f"{HB} do not fight. {HB} do not even have a word... for war."),
           ("aldrea", "Then we will teach them one.")],
    "e2": [("dak", "What do you do?"),
           ("aldrea", "Borrowing. Watch.")],
    "e4": [("dak", "Blades were for bark. Now, blades must be for blades.")],
    "e5": [("dak", f"He was {HB} too. The Yee-erk was in his head... but the blood is {HB} blood. What are we becoming?")],
    "e6": [("esplin", "A resistance. Led by an Anda-light. Interesting. Tell the Sub-Visser I want that blue body taken alive. Someday... it will be mine.")],
    "g1": [("alloran", "Eight warriors. That is what the council sends. Eight... for a world already lost.")],
    "g2": [("alloran", "Your father's kindness armed the enemy, child. Sentiment is how wars are lost."),
           ("aldrea", f"And what do you call eight million {HB}, War-Prince? Acceptable losses?")],
    "g3": [("alloran", f"If the Yee-erks want {HB} bodies... we deny them the bodies.")],
    "g5": [("aldrea", "DAK!")],
    "h1": [("dak", "Al-dree-ah. The sun rises. Your two hours..."),
           ("aldrea", f"Passed long ago, Dak Hamee. I am {HB} now. Your people are my people. Your fight is my fight.")],
    "h2": [("dak", f"The Yee-erks take the world. They do not take all. While one {HB} is free... {HB} are free.")],
    "h3": [("esplin", "Sub-Visser Esplin. Nine-four-double-six. Next, the Anda-light home world. Next... everything.")],
    "i1": [("jara", f"Dak and Al-dree-ah fight long. Fight until end. Their {KAW}... their children's children... still free.")],
    "i2": [("jara", "This is Toby. Toby Hamee. Named for you, Tobias."),
           ("toby", "I am a seer, like Dak. I see what others do not see. I see us free.")],
}

AUDITION = "The valley remembers. The trees remember. And while one of us is free, we are all of us free."


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
