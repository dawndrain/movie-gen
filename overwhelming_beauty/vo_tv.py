#!/usr/bin/env python3
"""TTS for THE VARIANCE. Usage: python3 vo_tv.py audition | lines
audition: one sample per candidate voice into vo_auditions/
lines:    all cast dialogue + narrator lines into vo/ (skips existing)."""
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
VO = HERE / "vo"
AUD = HERE / "vo_auditions"

CANDIDATES = {  # role -> [(preset, voice_id)]
    "oren": [("Gideon", "1ad38ba4-9cc4-4f2f-9fde-b0fefdf67ae5"),
             ("Leo", "73a45c18-0c56-4642-a61e-f6b303f8ded1"),
             ("Caspian", "ef70cc83-3015-4bad-9359-0ea968c43ec0"),
             ("Orion", "ed69c516-92d2-4b30-a967-617737a342e5")],
    "petra": [("Nora", "d081b915-6623-4a44-bacf-80d0f1c90a03"),
              ("Elena", "ca83ca7f-c186-493d-bd69-0d765fa861b2"),
              ("Sloane", "b57b22a0-f287-405b-bc82-6f08f5e6bb1f"),
              ("Isabella", "80924413-1ea8-4e64-9719-e00b86796f05")],
    "dez": [("Roxie", "f6448975-768e-4327-b932-1b7c973d58e9"),
            ("Maya", "b0f766b7-8703-4bd1-b973-f857c36837b6"),
            ("Chloe", "e9cfbbf0-4476-46be-b396-596eb774b165"),
            ("Gia", "530df032-c311-483b-a750-cb3c9e1bcdfd")],
    "narr": [("Alistair", "d9d5c263-f84e-4752-97b5-3750fcc6fd2f"),
             ("Harrison", "573e5163-59b3-4926-aab1-951ef2985f81"),
             ("Arthur", "30fc8796-ceb6-4a66-b3a7-4a145ef7f346")],
}

AUDITION_TEXT = {
    "oren": "I was alive. For eleven days... I was alive. Does it have to stop?",
    "petra": "Your metric profile is showing drift. Is there something in your "
             "routine we should adjust?",
    "dez": "Twenty-six years old, and nobody ever told him about the sky. "
           "Come on. There's somewhere you need to see.",
    "narr": "The first thing Oren noticed was the color of the sky. It was deep, "
            "and living, and enormous.",
}

# Final casting (audition pitch stats 2026-07-09: Caspian 83Hz measured,
# Nora 164Hz, Roxie 176Hz warm, Alistair 78Hz solemn).
VOICES = {
    "oren": ("Caspian", "ef70cc83-3015-4bad-9359-0ea968c43ec0"),
    "petra": ("Nora", "d081b915-6623-4a44-bacf-80d0f1c90a03"),
    "dez": ("Roxie", "f6448975-768e-4327-b932-1b7c973d58e9"),
    "narr": ("Alistair", "d9d5c263-f84e-4752-97b5-3750fcc6fd2f"),
}

# Dialogue lines (Seedance --audio refs). shot -> ordered (character, text).
LINES = {
    "t11a": [("petra", "Your metric profile is showing drift. Is there something "
                       "in your routine we should adjust? Sleep architecture? "
                       "Caloric intake?")],
    "t11b": [("oren", "No. I think... ... I'll re-baseline.")],
    "t12": [("oren", "The only way to deal with this life meaningfully... is to "
                     "find one's passion... and dive into it with everything "
                     "you have.")],
    "t14": [("dez", "You're telling me about the sky. Twenty-six years old, and "
                    "nobody ever told him about the sky. Come on. There's "
                    "somewhere you need to see.")],
    "t16a": [("oren", "I want to see the ocean — I want to learn an instrument — "
                      "I want to read everything ever written!")],
    "t16b": [("oren", "I want to understand why I was asleep for twenty-six "
                      "years."),
             ("dez", "Then don't go back to sleep.")],
    "t19": [("oren", "I can't stop it. There's too much. I opened something, and "
                     "I can't close it... and I can't hold it open either."),
            ("petra", "I know.")],
    "t20a": [("oren", "I was alive. For eleven days... I was alive.")],
    "t20b": [("petra", "Yes."),
             ("oren", "Does it have to stop?")],
}

# Narrator lines (mixed at assembly, never sent to Seedance). name -> text.
NARRATION = {
    "n01": "The first thing Oren noticed was the color of the sky.",
    "n02": "He looked at it... and it was not blue the way a data entry in a "
           "file is blue. He felt something happen in his chest, like a drawer "
           "sliding open.",
    "n03": "Oren was a twenty-four F — optimized for sustained cognitive "
           "labor. The F vocabulary contained no word for yearning.",
    "n04": "Things kept falling into it.",
    "n05": "He began arriving late. He took detours. He found himself standing "
           "in places.",
    "n06": "For eleven days, Oren lived. That was the only word for it.",
    "n07": "He barely slept. He couldn't. Everything was too much. Too bright. "
           "Too interesting.",
    "n08": "The crash came on the twelfth day.",
    "n09": "It wasn't punishment. It was restoration, they called it. A "
           "return to specification.",
    "n10": "The sky was above him, visible through the weather-shield. It was "
           "blue. He knew this the way one knows a data entry in a file.",
    "n11": "He didn't know why he did this. But he didn't stop.",
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
    mode = sys.argv[1]
    jobs = []
    if mode == "audition":
        AUD.mkdir(exist_ok=True)
        for role, cands in CANDIDATES.items():
            for name, vid in cands:
                jobs.append((AUD / f"{role}_{name}.mp3", vid, AUDITION_TEXT[role]))
    elif mode == "lines":
        VO.mkdir(exist_ok=True)
        for shot, lines in LINES.items():
            for n, (char, text) in enumerate(lines, 1):
                jobs.append((VO / f"{shot}_{n}_{char}.mp3", VOICES[char][1], text))
        for name, text in NARRATION.items():
            jobs.append((VO / f"{name}_narr.mp3", VOICES["narr"][1], text))
    else:
        sys.exit("mode must be audition|lines")

    with ThreadPoolExecutor(max_workers=4) as pool:
        for res in pool.map(lambda j: tts(*j), jobs):
            print(res, flush=True)
