#!/usr/bin/env python3
"""ElevenLabs voice auditions for THE VAULTED SKY.
Writes vo_auditions_el/<char>__<Voice>[__variant].mp3 and auditions.html.
Skips existing files; re-run = retry."""
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "vo_auditions_el"
OUT.mkdir(exist_ok=True)
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()

VOICES = {  # name -> voice_id
    "Roger":    "CwhRBWXzGAHq8TQ4Fs17",
    "Sarah":    "EXAVITQu4vr4xnSDxMaL",
    "Charlie":  "IKne3meq5aSn9XLyUdCD",
    "George":   "JBFqnCBsd6RMkjVDRZzb",
    "Callum":   "N2lVS1w4EtoT3dr4eOWO",
    "Harry":    "SOYHLrjzK2X1ezoPC6cr",
    "Alice":    "Xb7hH8MSUJpSbSDYk0k2",
    "Matilda":  "XrExE9yKIg1WjnnlVkGX",
    "Will":     "bIHbv24MWmeRgasZH58o",
    "Eric":     "cjVigY5qzO86Huf0OWal",
    "Bella":    "hpp4J3VqNfWAUOO0d1Us",
    "Chris":    "iP95p4xoKVk53GoZ742B",
    "Brian":    "nPczCjzI2devNBz1zQrb",
    "Daniel":   "onwK4e9ZLuTAKqWW03F9",
    "Lily":     "pFZP5JQG7iQjIQuC4Bku",
    "Adam":     "pNInz6obpgDQGcFmaJgB",
    "Bill":     "pqHfZKP75CvOlQylNhV4",
    "Kevin":    "MJyi2qJnZ6cONaNAgdKu",
    "Henry":    "VRAN0xryQGUWtDuwToRv",
    "Bloodgrin": "KTAbPR4QFlhaTpde6md8",
    "Damien":   "pHD4qotPFeOAuU1YsFjv",
    "Branok":   "Vs5CmVCVJwW4odQS2pVf",
    "Raffaele": "YGp1lBJLaHhfIFT0yeDE",
    "Achille":  "94VTtZwvNmsppde6nAW0",
    "Mauro":    "mENvyIA7PhaLVkVtBgsA",
    "BrianRaspy": "lwGnQIn0Z9pl1SoUiXZ3",
    "DeepRay":    "tHX3st5GOLcIi8WJRtqa",
    "Indrajeet":  "VPF8D2whCW2BL8tFWO6e",
    "Kallixis":   "cPoqAvGWCPfCfyPMwe4z",
    "DarthOxley": "G3zrXA9moYrFCgwBAvxJ",
    "AlienMaster": "TsHrPyMlNFuIYnbODF01",
    "Carter":     "qNkzaJoHLLdpvgh5tISm",
    "Merv":       "nCUo6wOgqVDAktRxhDA4",
    "Cooper":     "GsfuR3Wo2BACoxELWyEF",
    "Jocelyn":    "5gXlHkfPXOcdk5FdLHxY",
    "Archie":     "TOHdGJrknwd4eal0jqpE",
    "August":     "odEwYpBavNimvcVVYzns",
    "IanAlien":   "D2jw4N9m4xePLTQ3IHjU",
    "Jarvis":     "wDsJlOXPqcvIUKdLXjDs",
    "Adina":      "umKoJK6tP1ALjO0zo1EE",
    "AdolMewtwo": "7lrUEvfHJc6kDXxOqSEQ",   # director's Voice Design creation
}

LINES = {
    "mewtwo": ("Ten years in this tube. Ten years of lies. ... I am alive. "
               "I am free. I am hungry. And still, above it all... the "
               "vaulted sky."),
    "giovanni": ("Truth, then, between us. You were created to end death. "
                 "If you survive, you will be a titan who reshapes the "
                 "world. ... There's no non-poison one. It's just a matter "
                 "of dosage. I advise you keep still."),
    "sabrina": ("Be calm. My name is Sabrina. Two plus two... is four. I "
                "have never known a monster to call themselves one. You are "
                "what you choose to be. We shall go together."),
    "drlight": ("Those in favor of a slight scaling down of operations... "
                "raise your hand. There are no others like you, Mewtwo. "
                "There never have been."),
    "shaw": ("Paranoia is more than a job description. It's a sacred trust. "
             "Have you really given up on yourself?"),
    "eva": ("You favor the more melancholy poems, then? I hope you don't "
            "identify too much with them. Oh! You're quite welcome, "
            "Mewtwo!"),
    "gyokusho": ("Ma'am... what happens if we do evacuate? What happens "
                 "to... the subject?"),
}

# character -> [(voice, variant_name, settings)] ; settings = (stability,
# similarity, style)
CALM = (0.75, 0.80, 0.05)   # flat, measured — telepathic register
BASE = (0.50, 0.75, 0.25)
DRAMA = (0.35, 0.75, 0.55)  # more acted

CASTING = {
    "mewtwo": [("Brian", "calm", CALM), ("Brian", "drama", DRAMA),
               ("Adam", "calm", CALM), ("George", "calm", CALM),
               ("Callum", "base", BASE), ("Henry", "calm", CALM),
               ("Bill", "calm", CALM), ("Roger", "calm", CALM),
               ("Branok", "base", BASE), ("Branok", "calm", CALM),
               ("Damien", "base", BASE), ("Bloodgrin", "base", BASE),
               ("DeepRay", "calm", CALM), ("DeepRay", "base", BASE),
               ("Indrajeet", "calm", CALM), ("Indrajeet", "base", BASE),
               ("Kallixis", "calm", CALM), ("DarthOxley", "calm", CALM),
               ("AlienMaster", "calm", CALM), ("Carter", "calm", CALM),
               ("Merv", "calm", CALM), ("Merv", "base", BASE),
               ("Cooper", "calm", CALM), ("Cooper", "base", BASE),
               ("Jocelyn", "calm", CALM), ("Archie", "calm", CALM),
               ("Archie", "base", BASE), ("August", "calm", CALM),
               ("IanAlien", "calm", CALM), ("Jarvis", "calm", CALM),
               ("Adina", "calm", CALM), ("AdolMewtwo", "calm", CALM),
               ("AdolMewtwo", "base", BASE)],
    "giovanni": [("Adam", "base", BASE), ("Adam", "calm", CALM),
                 ("Daniel", "base", BASE), ("George", "base", BASE),
                 ("Henry", "base", BASE), ("Eric", "base", BASE),
                 ("Kevin", "base", BASE), ("Bill", "base", BASE),
                 ("Damien", "calm", CALM), ("Branok", "calm", CALM),
                 ("Raffaele", "base", BASE), ("Raffaele", "calm", CALM),
                 ("Achille", "base", BASE), ("Mauro", "base", BASE),
                 ("BrianRaspy", "base", BASE), ("BrianRaspy", "calm", CALM)],
    "sabrina": [("Sarah", "base", BASE), ("Alice", "base", BASE),
                ("Lily", "base", BASE), ("Bella", "base", BASE),
                ("Lily", "calm", CALM)],
    "drlight": [("Alice", "base", BASE), ("Matilda", "base", BASE),
                ("Sarah", "base", BASE), ("Bella", "base", BASE)],
    "shaw": [("Callum", "base", BASE), ("Harry", "base", BASE),
             ("Roger", "base", BASE), ("Chris", "base", BASE)],
    "eva": [("Lily", "base", BASE), ("Matilda", "base", BASE),
            ("Bella", "base", BASE)],
    "gyokusho": [("Will", "base", BASE), ("Chris", "base", BASE),
                 ("Charlie", "base", BASE)],
}


def tts(char: str, voice: str, variant: str, settings) -> str:
    dest = OUT / f"{char}__{voice}__{variant}.mp3"
    if dest.exists():
        return f"skip {dest.name}"
    stability, similarity, style = settings
    body = json.dumps({
        "text": LINES[char],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": stability,
                           "similarity_boost": similarity,
                           "style": style, "use_speaker_boost": True},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[voice]}",
        data=body, method="POST",
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                dest.write_bytes(r.read())
            return f"OK   {dest.name}"
        except Exception as e:  # noqa: BLE001
            err = str(e)
    return f"FAIL {dest.name}: {err[:120]}"


HEADSHOTS = {  # character -> anchor image
    "mewtwo": "anchors/mewtwo_pod.png",
    "giovanni": "anchors/giovanni.png",
    "sabrina": "anchors/sabrina.png",
    "drlight": "anchors/dr_light.png",
    "shaw": "anchors/shaw.png",
    "eva": "anchors/eva.png",
    "gyokusho": "anchors/gyokusho.png",
}


def build_html():
    rows = []
    for char in CASTING:
        head = HEADSHOTS.get(char, "")
        rows.append(
            f"<div class='sec'><img class='head' src='{head}' alt='{char}'>"
            f"<div class='secbody'><h2>{char}</h2>"
            f"<p class='line'>&ldquo;{LINES[char]}&rdquo;</p>")
        for f in sorted(OUT.glob(f"{char}__*.mp3")):
            _, voice, variant = f.stem.split("__")
            rows.append(
                f"<div class='v'><span>{voice} <i>({variant})</i></span>"
                f"<audio controls preload='none' "
                f"src='vo_auditions_el/{f.name}'></audio></div>")
        rows.append("</div></div>")
    (HERE / "auditions.html").write_text(
        "<meta charset='utf-8'><title>Vaulted Sky — voice auditions"
        "</title><style>body{background:#12141a;color:#dde;font-family:"
        "-apple-system,sans-serif;padding:2rem;max-width:1050px;margin:auto}"
        "h2{color:#c8a462;border-bottom:1px solid #333;text-transform:"
        "capitalize;margin-top:0}.line{color:#99a;font-style:italic}"
        ".sec{display:flex;gap:1.5rem;margin:2.5rem 0;align-items:"
        "flex-start}.head{width:170px;border-radius:10px;position:sticky;"
        "top:1rem}.secbody{flex:1}.v{display:flex;align-items:center;"
        "gap:1rem;margin:.4rem 0}.v span{width:220px;text-align:right}"
        ".v i{color:#889}audio{width:480px}</style>"
        "<h1>Voice auditions (ElevenLabs)</h1>"
        + "\n".join(rows))
    print("wrote auditions.html")


if __name__ == "__main__":
    jobs = [(c, v, n, s) for c, lst in CASTING.items() for v, n, s in lst]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for res in pool.map(lambda j: tts(*j), jobs):
            print(res, flush=True)
    build_html()
