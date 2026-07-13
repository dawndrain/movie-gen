#!/usr/bin/env python3
"""TTS auditions for David-trilogy casting candidates. Skips existing files."""
import re
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
AUD = HERE / "vo_auditions"
AUD.mkdir(exist_ok=True)

CANDIDATES = {
    "Leo":     "73a45c18-0c56-4642-a61e-f6b303f8ded1",
    "Wilder":  "39c02668-cd27-4313-9164-2ba0eb5098cf",
    "Caspian": "ef70cc83-3015-4bad-9359-0ea968c43ec0",
    "Kevin":   "f1373f24-3b96-433f-9a68-e595810ef608",
    "Andre":   "f1e8226e-2248-4d5f-b43c-0a79e9949dbf",
    "Mark":    "27c04473-84a9-4b60-a41f-c8e8458bd4f1",
    "Chloe":   "e9cfbbf0-4476-46be-b396-596eb774b165",
    "Zoe":     "d0374db1-44b9-4f05-939e-0a9ae9dbbe6a",
    "Maya":    "b0f766b7-8703-4bd1-b973-f857c36837b6",
    "Harper":  "47fb207f-63fe-449e-915b-27b3d8098fd1",
    "Ava":     "4af0ac8b-b5ad-4d12-8f6b-c48b9c369f87",
    "Sienna":  "41023a48-71ab-478a-bea7-c7b5a78f6b36",
    "Quinn":   "80914268-dfae-4f76-8306-36f2d55f58f8",
    "Gia":     "530df032-c311-483b-a750-cb3c9e1bcdfd",
}

AUDITION = ("We found the blue box at the construction site. Nobody is the boss "
            "of me. It's over, David. I'm sorry. It's done.")


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
    jobs = [(AUD / f"cand_{name}.mp3", vid, AUDITION)
            for name, vid in CANDIDATES.items()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for res in pool.map(lambda j: tts(*j), jobs):
            print(res, flush=True)
