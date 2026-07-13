#!/usr/bin/env python3
"""Voice auditions for EGIL — Higgsfield text2speech_v2 presets (the Seedance
dialogue pipeline) + ElevenLabs candidates (narrator/dub), one saga line per
character. Writes vo_auditions/<char>__<Voice>__<hf|el>.mp3 and auditions.html
(anchor portrait + players + measured pitch). Skips existing; re-run = retry.

Usage: python3 auditions.py            # generate all + build html
       python3 auditions.py html       # rebuild html only
"""
import json
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "vo_auditions"
OUT.mkdir(exist_ok=True)
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()
PITCH = HERE.parent / "animorphs_david" / "pitch.py"

HF_PRESETS = {
    "Wilder":   "39c02668-cd27-4313-9164-2ba0eb5098cf",
    "Caspian":  "ef70cc83-3015-4bad-9359-0ea968c43ec0",
    "Roman":    "7e63ac18-5fcd-4aba-8078-a86d4e11c127",
    "Gideon":   "1ad38ba4-9cc4-4f2f-9fde-b0fefdf67ae5",
    "Julian":   "95429266-c0ac-4137-a209-63b8812b0f23",
    "Brooks":   "c2acff45-84b2-4974-892d-89fa2d4e5598",
    "Harrison": "573e5163-59b3-4926-aab1-951ef2985f81",
    "Arthur":   "30fc8796-ceb6-4a66-b3a7-4a145ef7f346",
    "Alistair": "d9d5c263-f84e-4752-97b5-3750fcc6fd2f",
    "Sterling": "dc382508-c8bd-443c-8cb2-46e57b8d2e6f",
    "Mark":     "27c04473-84a9-4b60-a41f-c8e8458bd4f1",
    "Andre":    "f1e8226e-2248-4d5f-b43c-0a79e9949dbf",
    "Kevin":    "f1373f24-3b96-433f-9a68-e595810ef608",
    "Leo":      "73a45c18-0c56-4642-a61e-f6b303f8ded1",
    "Quinn":    "80914268-dfae-4f76-8306-36f2d55f58f8",
    "Sloane":   "b57b22a0-f287-405b-bc82-6f08f5e6bb1f",
    "Elena":    "ca83ca7f-c186-493d-bd69-0d765fa861b2",
    "Vesper":   "c3204739-4084-41a3-9dc5-c805b307ec18",
    "Sienna":   "41023a48-71ab-478a-bea7-c7b5a78f6b36",
    "Nora":     "d081b915-6623-4a44-bacf-80d0f1c90a03",
    "Isabella": "80924413-1ea8-4e64-9719-e00b86796f05",
    "Tasha":    "e0d40568-8c85-4c9b-bdb2-b638b253a24f",
    "Mabel":    "fa64fba4-ad02-405e-99d0-1f085d87c706",
    "Vlad":     "e5666b9c-99a2-4fac-8b4e-abee078b186d",
}

EL_VOICES = {
    "George":       "JBFqnCBsd6RMkjVDRZzb",
    "LeifNordic":   "tJDFCHyviItsYF1qqToS",
    "VikingBjorn":  "ljo9gAlSqKOvF6D8sOsX",
    "KaelenWarrior": "10NkTYmU7tSz3Kkl3Lex",
    "KristenQueen": "Qbw4VpyUrHEG7NigKzty",
    "ElarielQueen": "ksryVoNAGZT8GxWCTiVm",
    "Bill":         "pqHfZKP75CvOlQylNhV4",
    "Brian":        "nPczCjzI2devNBz1zQrb",
    "Adam":         "pNInz6obpgDQGcFmaJgB",
    "Harry":        "SOYHLrjzK2X1ezoPC6cr",
    "Henry":        "VRAN0xryQGUWtDuwToRv",
    "Daniel":       "onwK4e9ZLuTAKqWW03F9",
    "Bloodgrin":    "KTAbPR4QFlhaTpde6md8",
    "Lily":         "pFZP5JQG7iQjIQuC4Bku",
    "Matilda":      "XrExE9yKIg1WjnnlVkGX",
    "Callum":       "N2lVS1w4EtoT3dr4eOWO",
}

LINES = {
    "narrator": ("They called him Kveldulf — the Evening-Wolf. Each day as the "
                 "sun went down he grew sullen, and no man could speak with "
                 "him. It was said he was shape-strong."),
    "egil": ("I bared blue Dragvandill, who bit not the buckler... My tooth I "
             "bade bite him — best of swords at need. Glory and fame... gat "
             "Eirik's name."),
    "egil_child": ("Thou wilt not find a doughtier song-smith of three "
                   "winters. So may I, high-standing, hew down many foemen!"),
    "egil_old": ("Blind near the blaze I wander, and beg the fire-maid's "
                 "pardon. Yet England's mighty monarch... me whilom greatly "
                 "honoured."),
    "skallagrim": ("You are late, methinks, Egil, in paying me the silver "
                   "that King Athelstan sent. What do you mean to do with "
                   "that money?"),
    "kveldulf": ("My foreboding is that we shall reap ruin from that king. "
                 "Beware — keep within bounds, nor rival thy betters."),
    "thorolf_s": ("Brother, you will have your way — but it is the king's "
                  "array. ... Now am I but three feet short of my aim!"),
    "harald": ("If Thorolf proves himself as accomplished in deed as he is "
               "right brave in look... Set fire to the room. I will not "
               "waste my men."),
    "eirik": ("How wert thou so bold, Egil, that thou daredst to come before "
              "me? ... I give thee now thy head. This time."),
    "gunnhild": ("Why shall not Egil be slain at once? Rememberest thou no "
                 "more, O king, what Egil hath done to thee — thy friends, "
                 "thy kin, thine own son?"),
    "arinbjorn": ("Night-slaying is murder, king. If Egil have spoken evil "
                  "of thee, he can atone in words of praise that shall live "
                  "for all time."),
    "athelstan": ("Bear these my words to King Olaf: let him become my "
                  "vassal, and hold Scotland for me... and be my under-king."),
    "thorgerd": ("Father, open the door. I will that we both travel the same "
                 "road. ... Now are we deceived. This is milk."),
    "brak": "Dost thou turn thy shape-strength, Skallagrim, against thy son?",
    "bard": ("I drink to you, Egil. There is here a feast of sacrifice — and "
             "you drink deep, guest."),
}

# character -> anchor image, [(voice, "hf"|"el")]
CASTING = {
    "narrator": ("anchors/loc_longship.png",
                 [("George", "el"), ("LeifNordic", "el"),
                  ("VikingBjorn", "el")]),
    "egil": ("anchors/egil.png",
             [("Wilder", "hf"), ("Caspian", "hf"), ("Vlad", "hf"),
              ("KaelenWarrior", "el"), ("VikingBjorn", "el"),
              ("Callum", "el")]),
    "egil_child": ("anchors/egil_child.png",
                   [("Leo", "hf"), ("Quinn", "hf")]),
    "egil_old": ("anchors/egil_old.png",
                 [("Wilder", "hf"), ("Bill", "el"), ("VikingBjorn", "el")]),
    "skallagrim": ("anchors/skallagrim.png",
                   [("Caspian", "hf"), ("Roman", "hf"), ("Brian", "el")]),
    "kveldulf": ("anchors/kveldulf.png",
                 [("Arthur", "hf"), ("Harrison", "hf"), ("Mark", "hf"),
                  ("Bill", "el")]),
    "thorolf_s": ("anchors/thorolf_s.png",
                  [("Gideon", "hf"), ("Julian", "hf"), ("Brooks", "hf"),
                   ("Harry", "el")]),
    "harald": ("anchors/harald.png",
               [("Sterling", "hf"), ("Alistair", "hf"), ("Adam", "el")]),
    "eirik": ("anchors/eirik.png",
              [("Roman", "hf"), ("Andre", "hf"), ("Bloodgrin", "el")]),
    "gunnhild": ("anchors/gunnhild.png",
                 [("Sloane", "hf"), ("Elena", "hf"), ("Vesper", "hf"),
                  ("KristenQueen", "el"), ("ElarielQueen", "el")]),
    "arinbjorn": ("anchors/arinbjorn.png",
                  [("Harrison", "hf"), ("Brooks", "hf"), ("Daniel", "el")]),
    "athelstan": ("anchors/athelstan.png",
                  [("Alistair", "hf"), ("Henry", "el")]),
    "thorgerd": ("anchors/thorgerd.png",
                 [("Sienna", "hf"), ("Nora", "hf"), ("Isabella", "hf"),
                  ("Lily", "el")]),
    "brak": ("anchors/brak.png",
             [("Tasha", "hf"), ("Mabel", "hf"), ("Matilda", "el")]),
    "bard": ("anchors/bard.png", [("Kevin", "hf"), ("Andre", "hf")]),
}


def tts_hf(dest: Path, voice_id: str, text: str) -> str:
    cmd = ["higgsfield", "generate", "create", "text2speech_v2",
           "--prompt", text, "--variant", "elevenlabs",
           "--voice_id", voice_id, "--voice_type", "preset", "--wait"]
    for _ in range(3):
        r = subprocess.run(cmd, capture_output=True, text=True)
        urls = re.findall(r"https://\S+\.(?:mp3|m4a|wav)\S*", r.stdout + r.stderr)
        if r.returncode == 0 and urls:
            urllib.request.urlretrieve(urls[-1].rstrip('",'), dest)
            return f"OK   {dest.name}"
        err = (r.stdout + r.stderr).strip()[-150:]
    return f"FAIL {dest.name}: {err}"


def tts_el(dest: Path, voice_id: str, text: str) -> str:
    body = json.dumps({
        "text": text, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.75,
                           "style": 0.35, "use_speaker_boost": True},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=body, method="POST",
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    err = "?"
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                dest.write_bytes(r.read())
            return f"OK   {dest.name}"
        except Exception as e:  # noqa: BLE001
            err = str(e)
    return f"FAIL {dest.name}: {err[:120]}"


def gen(char: str, voice: str, kind: str) -> str:
    dest = OUT / f"{char}__{voice}__{kind}.mp3"
    if dest.exists():
        return f"skip {dest.name}"
    if kind == "hf":
        return tts_hf(dest, HF_PRESETS[voice], LINES[char])
    return tts_el(dest, EL_VOICES[voice], LINES[char])


def measure_pitch() -> dict:
    files = sorted(OUT.glob("*.mp3"))
    if not files or not PITCH.exists():
        return {}
    r = subprocess.run([sys.executable, str(PITCH)] + [str(f) for f in files],
                       capture_output=True, text=True)
    out = {}
    for line in r.stdout.splitlines():
        m = re.match(r"\s*(\S+)\s+median\s+(\d+)\s*Hz", line)
        if m:
            out[m.group(1)] = int(m.group(2))
    return out


def build_html():
    pitch = measure_pitch()
    rows = []
    for char, (head, cands) in CASTING.items():
        rows.append(
            f"<div class='sec'><img class='head' src='{head}' alt='{char}'>"
            f"<div class='secbody'><h2>{char.replace('_', ' ')}</h2>"
            f"<p class='line'>&ldquo;{LINES[char]}&rdquo;</p>")
        for voice, kind in cands:
            f = OUT / f"{char}__{voice}__{kind}.mp3"
            hz = pitch.get(f.stem)
            hz_s = f" · {hz} Hz" if hz else ""
            tag = "preset" if kind == "hf" else "elevenlabs"
            if f.exists():
                rows.append(
                    f"<div class='v'><span>{voice} <i>({tag}{hz_s})</i></span>"
                    f"<audio controls preload='none' "
                    f"src='vo_auditions/{f.name}'></audio></div>")
            else:
                rows.append(f"<div class='v'><span>{voice} <i>({tag})</i>"
                            f"</span><em class='miss'>pending</em></div>")
        rows.append("</div></div>")
    (HERE / "auditions.html").write_text(
        "<meta charset='utf-8'><title>EGIL — voice auditions</title>"
        "<style>body{background:#101014;color:#ddd;font-family:-apple-system,"
        "sans-serif;padding:2rem;max-width:1050px;margin:auto}"
        "h1{font-weight:200;letter-spacing:.18em}"
        "h2{color:#c9a86a;border-bottom:1px solid #333;text-transform:"
        "capitalize;margin-top:0}.line{color:#99a;font-style:italic}"
        ".sec{display:flex;gap:1.5rem;margin:2.5rem 0;align-items:flex-start}"
        ".head{width:190px;border-radius:10px;position:sticky;top:1rem}"
        ".secbody{flex:1}.v{display:flex;align-items:center;gap:1rem;"
        "margin:.4rem 0}.v span{width:230px;text-align:right}"
        ".v i{color:#889;font-size:13px}.miss{color:#555}audio{width:460px}"
        "</style><h1>EGIL — voice auditions</h1>"
        "<p>presets = Higgsfield text2speech_v2 (the Seedance --audio "
        "pipeline); elevenlabs = narrator/dub candidates. Casting doc: "
        "<a href='voices.md' style='color:#c9a86a'>voices.md</a></p>"
        + "\n".join(rows))
    print(f"wrote auditions.html ({len(pitch)} pitched files)")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "html":
        build_html()
        sys.exit()
    jobs = [(c, v, k) for c, (_h, lst) in CASTING.items() for v, k in lst]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for res in pool.map(lambda j: gen(*j), jobs):
            print(res, flush=True)
    build_html()
