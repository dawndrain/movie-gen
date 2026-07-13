#!/usr/bin/env python3
"""TTS pitch auditions for the Burnt Njal cast (ElevenLabs) + casting.html.
Each character's candidates read the character's actual saga line (Dasent, verbatim).
Skips existing mp3s, so rerunning is the retry pass. Rebuilds casting.html always."""
import html
import json
import os
import subprocess
import urllib.request
from pathlib import Path

import numpy as np

PROJ = Path(__file__).parent
AUD = PROJ / "auditions"
AUD.mkdir(exist_ok=True)
KEY = (os.environ.get("ELEVENLABS_API_KEY")
       or Path(os.path.expanduser("~/.elevenlabs_key")).read_text().strip())

V = {  # name -> voice_id (premades + shared voices added to the account)
    "Elderon": "NwyAvGnfbFoNNEi4UuTq", "Bill": "pqHfZKP75CvOlQylNhV4",
    "Henry": "VRAN0xryQGUWtDuwToRv", "Oyvind": "nhvaqgRyAq6BmFs3WcdX",
    "Brian": "nPczCjzI2devNBz1zQrb", "George": "JBFqnCBsd6RMkjVDRZzb",
    "VikingBjorn": "ljo9gAlSqKOvF6D8sOsX", "Kaelen": "10NkTYmU7tSz3Kkl3Lex",
    "Bloodgrin": "KTAbPR4QFlhaTpde6md8", "Charlotte": "rhS7yjXTU4uIlRxXhNW7",
    "Lily": "pFZP5JQG7iQjIQuC4Bku", "Sarah": "EXAVITQu4vr4xnSDxMaL",
    "Alice": "Xb7hH8MSUJpSbSDYk0k2", "Matilda": "XrExE9yKIg1WjnnlVkGX",
    "Leif": "tJDFCHyviItsYF1qqToS", "Daniel": "onwK4e9ZLuTAKqWW03F9",
    "CJ": "9n6dGtreZHvmNb14Y1VO", "Charlie": "IKne3meq5aSn9XLyUdCD",
    "Will": "bIHbv24MWmeRgasZH58o", "Callum": "N2lVS1w4EtoT3dr4eOWO",
    "Schmitz": "HAvvFKatz0uu0Fv55Riy", "Eric": "cjVigY5qzO86Huf0OWal",
    "Nils": "xVvh7KgfbHX1WS6JTNXX", "NanaMargaret": "xIzR6egd3S3LJZbVW0c1",
    "Harry": "SOYHLrjzK2X1ezoPC6cr", "Adam": "pNInz6obpgDQGcFmaJgB",
}

# character -> (image, blurb, audition line, [candidates, primary first])
CAST = [
    ("njal", "anchors/njal.png",
     "The beardless lawyer-prophet. 'Wise too he was, and foreknowing and foresighted.'",
     "I will not go out, for I am an old man, and little fitted to avenge my sons; but I will not live in shame.",
     ["Elderon", "Bill", "Henry"]),
    ("gunnar", "anchors/gunnar.png",
     "The reluctant champion of Lithend. 'Best skilled in arms of all men.'",
     "Fair is the Lithe; so fair that it has never seemed to me so fair; the corn fields are white to harvest, and the home mead is mown; and now I will ride back home, and not fare abroad at all.",
     ["Oyvind", "Brian", "George"]),
    ("skarphedinn", "anchors/skarphedinn.png",
     "Njal's grim eldest son. Pale, sharp-featured, grins when he speaks of death.",
     "What, lads! Are ye lighting a fire, or are ye taking to cooking? I may well humour my father in this, by being burnt indoors along with him; for I am not afraid of my death.",
     ["VikingBjorn", "Kaelen", "Bloodgrin"]),
    ("hallgerda", "anchors/hallgerda.png",
     "Thief's eyes. Fair hair to her waist, and the slap remembered to the last.",
     "Then I call to thy mind that slap on the face which thou gavest me; and I care never a whit whether thou holdest out a long while, or a short.",
     ["Charlotte", "Lily", "Sarah"]),
    ("bergthora", "anchors/bergthora.png",
     "Njal's wife. 'High-spirited, brave-hearted, but somewhat hard-tempered.'",
     "I was given away to Njal young, and I have promised him this, that we would both share the same fate.",
     ["Alice", "Matilda"]),
    ("flosi", "anchors/flosi.png",
     "Leader of the Burners — a good man who does the worst deed in Iceland.",
     "That is a deed which we shall have to answer for heavily before God, since we are Christian men ourselves; but still we must take to that counsel.",
     ["Leif", "Daniel"]),
    ("kari", "anchors/kari.png",
     "The survivor of the Burning. 'He never abused his foes, and never threatened them.'",
     "Though all others take an atonement in their quarrels, yet will I take no atonement. My son, I say, is still unavenged, and I mean to take that on myself alone.",
     ["CJ", "Charlie", "Will"]),
    ("hildigunna", "anchors/hildigunna.png",
     "Hoskuld's widow. 'The grimmest and hardest-hearted of all women.'",
     "I adjure thee, by all the might of thy Christ, and by thy manhood and bravery, to take vengeance for all those wounds which he had on his dead body, or else to be called every man's dastard.",
     ["Lily", "Sarah"]),
    ("mord", "anchors/mord.png",
     "The saga's Iago. Everyone who talks to him believes he is their friend.",
     "They gave thee a horse which they called a dark horse, and that they did out of mockery at thee. They mean to fall upon you, and thy life lies on it.",
     ["Callum", "Schmitz"]),
    ("hoskuld_wp", "anchors/hoskuld_wp.png",
     "The beloved foster-son, murdered in his own cornfield in Flosi's scarlet cloak.",
     "Thou canst never say so much ill of Njal's sons as to make me believe it. And were it true, I would far rather suffer death at their hands, than work them any harm.",
     ["George", "Eric"]),
    ("hrut", "frames/f_p1_thiefs_eyes.png",
     "Prologue only — the prophecy. Nils doubles as the (sparse, assembly-mixed) narrator.",
     "Fair enough is this maid, and many will smart for it; but this I know not, whence thief's eyes have come into our race.",
     ["Nils", "Daniel"]),
    ("rannveig", "anchors/rannveig.png",
     "Gunnar's mother, who keeps the bill for the avenger.",
     "Thou behavest ill, and this shame shall long be had in mind.",
     ["NanaMargaret", "Matilda"]),
    ("gizur", "anchors/gizur.png",
     "The honorable enemy. Refuses arson; speaks Gunnar's eulogy.",
     "We have now laid low to earth a mighty chief, and hard work has it been; and the fame of this defence of his shall last as long as men live in this land.",
     ["Daniel", "Bill"]),
    ("gunnar_lambi", "anchors/gunnar_lambi.png",
     "The laugher on the wall; loses an eye to a jaw-tooth, and his head to a lie.",
     "Weepest thou now, Skarphedinn? Well at first, for a long time; but still the end of it was, that he wept.",
     ["Harry", "Adam"]),
]


def tts(voice_id: str, text: str, dest: Path) -> bool:
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2"}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    try:
        dest.write_bytes(urllib.request.urlopen(req).read())
        return True
    except urllib.error.HTTPError as e:
        print(f"  TTS FAIL {dest.name}: {e.read().decode()[:150]}")
        return False


def median_f0(path: Path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
                          "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    sr, win, hop = 16000, 1024, 512
    f0s = []
    for i in range(0, len(x) - win, hop):
        fr = x[i:i + win]
        if np.sqrt((fr ** 2).mean()) < 0.02:
            continue
        fr = fr - fr.mean()
        ac = np.correlate(fr, fr, "full")[win - 1:]
        lo, hi = sr // 400, sr // 70
        seg = ac[lo:hi]
        if seg.size == 0 or ac[0] <= 0:
            continue
        peak = seg.argmax() + lo
        if ac[peak] / ac[0] > 0.35:
            f0s.append(sr / peak)
    return float(np.median(f0s)) if len(f0s) >= 10 else None


results = {}
for char, img, blurb, line, cands in CAST:
    for name in cands:
        mp3 = AUD / f"{char}__{name}.mp3"
        if not mp3.exists():
            print(f"TTS {char} / {name}")
            if not tts(V[name], line, mp3):
                continue
        f0 = median_f0(mp3)
        results[mp3.name] = f0
        print(f"  {mp3.name}: {f0:.0f} Hz" if f0 else f"  {mp3.name}: too little voiced audio")

# ---- casting.html ----
cards = []
for char, img, blurb, line, cands in CAST:
    rows = []
    for i, name in enumerate(cands):
        mp3 = AUD / f"{char}__{name}.mp3"
        if not mp3.exists():
            rows.append(f'<div class="cand missing">{name} — generation failed</div>')
            continue
        f0 = results.get(mp3.name)
        f0s = f"{f0:.0f} Hz" if f0 else "n/a"
        tag = '<span class="tag primary">primary</span>' if i == 0 else ""
        rows.append(f"""
    <div class="cand">
      <div class="candhead"><b>{name}</b> {tag}
        <span class="f0">{f0s}</span>
        <span class="vid">{V[name]}</span></div>
      <audio controls preload="none" src="auditions/{mp3.name}"></audio>
    </div>""")
    cards.append(f"""
<div class="char">
  <a href="{img}"><img src="{img}"></a>
  <div class="charmeta">
    <h2>{char.upper().replace('_WP', ' (Whiteness Priest)')}</h2>
    <p class="blurb">{html.escape(blurb)}</p>
    <p class="line">&ldquo;{html.escape(line)}&rdquo;</p>
    {''.join(rows)}
  </div>
</div>""")

page = f"""<!doctype html><meta charset="utf-8"><title>Burnt Njal — voice casting</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.45 -apple-system, sans-serif;
       max-width: 1000px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight:600; }} a.back {{ color:#9ad; font-size:14px; }}
.char {{ display:flex; gap:18px; margin:20px 0; padding:16px; background:#1d1d22;
         border-radius:10px; }}
.char > a img {{ width:200px; border-radius:8px; display:block; }}
.charmeta {{ flex:1; min-width:0; }}
.charmeta h2 {{ margin:0 0 4px; font-size:19px; color:#cdf; }}
.blurb {{ color:#99a; margin:2px 0 8px; font-size:13.5px; }}
.line {{ color:#ffd479; font-style:italic; margin:6px 0 12px; }}
.cand {{ margin:10px 0; padding:10px 12px; background:#17171b; border-radius:8px; }}
.cand.missing {{ color:#a66; }}
.candhead {{ margin-bottom:6px; }}
.f0 {{ color:#7a8; margin-left:10px; font-size:13px; }}
.vid {{ color:#556; margin-left:10px; font-size:11.5px; font-family:monospace; }}
.tag {{ font-size:11px; padding:2px 8px; border-radius:10px; margin-left:6px; }}
.tag.primary {{ background:#3a5f3a; }}
audio {{ width:100%; max-width:520px; height:34px; }}
</style>
<h1>BURNT NJAL — voice casting auditions</h1>
<p><a class="back" href="storyboard.html">&larr; storyboard</a> &nbsp;|&nbsp;
Each candidate reads the character's own line (Dasent, verbatim). Median F0 from
autocorrelation over voiced frames — aim for a well-spread cast (adult male ~85&ndash;155 Hz,
female ~165&ndash;255 Hz). First listed = current primary pick; swap freely.</p>
{''.join(cards)}
"""
(PROJ / "casting.html").write_text(page)
print(f"\nwrote njals_saga/casting.html ({len(CAST)} characters, {len(results)} takes)")
