#!/usr/bin/env python3
"""TTS all dialogue for THE DAVID TRILOGY (fixed preset voices, cast by pitch
audition 2026-07-09). Output: vo/<shot>_<n>_<char>.mp3. Skips existing."""
import re
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
VO = HERE / "vo"
VO.mkdir(exist_ok=True)

VOICES = {  # character -> (preset name, voice_id)   [median F0 at audition]
    "jake":   ("Xavier",  "43173c95-3ec8-446a-a162-6504332c578b"),  # 116 Hz steady
    "marco":  ("Andre",   "f1e8226e-2248-4d5f-b43c-0a79e9949dbf"),  # 106 Hz animated
    "rachel": ("Sienna",  "41023a48-71ab-478a-bea7-c7b5a78f6b36"),  # 165 Hz fierce
    "cassie": ("Quinn",   "80914268-dfae-4f76-8306-36f2d55f58f8"),  # 208 Hz steady warm
    "tobias": ("Mark",    "27c04473-84a9-4b60-a41f-c8e8458bd4f1"),  # 105 Hz even/wry
    "ax":     ("Caspian", "ef70cc83-3015-4bad-9359-0ea968c43ec0"),  #  82 Hz formal
    "david":  ("Kevin",   "f1373f24-3b96-433f-9a68-e595810ef608"),  # 140 Hz young/cocky
    "visser": ("Roman",   "7e63ac18-5fcd-4aba-8078-a86d4e11c127"),  # 114 Hz — Esplin 9466 continuity
}

YK = "Yee-erks"   # phonetic Yeerks

# shot -> ordered (character, line) pairs. Spelling here is PHONETIC for TTS.
LINES = {
    "a2":  [("david", "Strange blue box, found at a construction site. One hundred "
                      "bucks, or best offer. ... Somebody out there wants you, "
                      "little box. I can feel it.")],
    "a4":  [("marco", "Jake. Tell me that is not what I think it is."),
            ("jake",  "The morphing cube. ELL-fan-gore's cube."),
            ("marco", f"It's on a public auction site, Jake. If we found it, the {YK} found it an hour ago."),
            ("jake",  "Then we go tonight.")],
    "v1":  [("visser", "A human child found the ESS-kuh-fill device... and offered "
                       "it for sale. On their internet. Find the boy. Bring me the "
                       "box. And bring me the boy.")],
    "a6":  [("david", "Those things at my house. They took my mom and dad. Tell me what is happening."),
            ("jake",  f"They're called {YK}. They take people. You can't go home, David. Not ever again.")],
    "a7":  [("jake",  "Put your hand on it. You'll be one of us. The seventh."),
            ("marco", "For the record? Bad idea.")],
    "b1":  [("david", "Hawks. Wolves. Kid stuff. This... is more like it. Hello, king.")],
    "b2":  [("jake",  f"World leaders downstairs, {YK} in the walls. We watch. We "
                      "report. We do not engage. Nothing happens unless I say it happens."),
            ("david", "You know your problem, Jake? You think you're the boss of me. Nobody... is the boss of me.")],
    "b4":  [("marco", "He broke cover. He blew the mission. He almost got us killed. Twice."),
            ("david", "You get to go home after. To your dad. To your bed. I sleep "
                      "in a barn. I lost everything. Because of you people.")],
    "b6":  [("rachel", "He killed him, Jake. He killed Tobias. Don't tell me you weren't thinking it too."),
            ("jake",   "He wants us hunting him angry. We end this my way.")],
    "b7a": [("david", "The famous Jake. Came alone. You should have let me sell the box."),
            ("jake",  "It ends tonight, David.")],
    "b7c": [("david",  "Say it. Say I win."),
            ("rachel", "Touch him again, and there is no morph on Earth that will save you.")],
    "c1":  [("jake",   f"We can't kill him. We can't watch our backs forever. And we can't hand him to the {YK}."),
            ("cassie", "Then we don't do any of those. There is a third way. You're "
                       "all going to hate it. Especially me.")],
    "c2":  [("tobias", "Before anyone cries at my funeral... the eagle got a wild "
                       "hawk. Not me. I've been shadowing David for two days. I know where he sleeps."),
            ("rachel", "You're alive. Don't you EVER do that to me again.")],
    "c4":  [("jake",  "Tomorrow. Dawn. We move the cube to the sea cave at Widows "
                      "Point. Rachel carries it. Alone."),
            ("marco", f"Alone? With the one thing the {YK} want more than air?"),
            ("jake",  "Alone. After tomorrow, no one will ever find it again.")],
    "c5":  [("tobias", "He was here. He heard every word. Hook, line... sinker."),
            ("jake",   "Then tomorrow, we do the worst good thing we've ever done.")],
    "c6":  [("rachel", "It's just me, David! Just me, and the box! I know you're watching! Come and take it!")],
    "c7":  [("jake",  "Six against one, David. It's over."),
            ("david", "The meeting. The box. All of it... a play. For me.")],
    "c8":  [("david", "Catch the rat.")],
    "c9a": [("ax",   "One hour and fifty-nine minutes. ... Two hours, Prince Jake. It is done.")],
    "c9b": [("ax",   "He will never morph again. He will never be anything again... except what he is.")],
    "c9c": [("jake", "Demorph, everyone. It's over.")],
    "c10": [("david",  "You can't leave me here. Rachel! RACHEL! Come back! KILL ME!"),
            ("rachel", "I'm sorry, David. ... It's done.")],
    "c12": [("cassie", "We did the only thing we could do."),
            ("rachel", "Then why does it feel like this?"),
            ("jake",   "Nobody ever mentions David again. That's an order.")],
}


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
    with ThreadPoolExecutor(max_workers=4) as pool:
        for res in pool.map(lambda j: tts(*j), jobs):
            print(res, flush=True)
