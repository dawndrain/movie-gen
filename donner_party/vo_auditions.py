#!/usr/bin/env python3
"""Generate ElevenLabs TTS auditions for every casting candidate and build
casting.html (anchor portraits + playable clips + median-f0 per take).
Idempotent: skips mp3s that already exist. Rerun after editing CAST."""
import json
import subprocess
import urllib.request
from pathlib import Path

import numpy as np

PROJ = Path(__file__).parent
VO = PROJ / "vo_auditions"
VO.mkdir(exist_ok=True)
KEY = Path.home().joinpath(".elevenlabs_key").read_text().strip()

VOICES = {
    "Jessica": "cgSgspJ2msm6clMCkdW9", "Sarah": "EXAVITQu4vr4xnSDxMaL",
    "Laura": "FGY2WhTYpPnrIDTdsKH5", "Adam": "pNInz6obpgDQGcFmaJgB",
    "Damien": "pHD4qotPFeOAuU1YsFjv", "Eric": "cjVigY5qzO86Huf0OWal",
    "Matilda": "XrExE9yKIg1WjnnlVkGX", "Bella": "hpp4J3VqNfWAUOO0d1Us",
    "Bill": "pqHfZKP75CvOlQylNhV4", "Henry": "VRAN0xryQGUWtDuwToRv",
    "Lily": "pFZP5JQG7iQjIQuC4Bku", "Alice": "Xb7hH8MSUJpSbSDYk0k2",
    "Chris": "iP95p4xoKVk53GoZ742B", "Will": "bIHbv24MWmeRgasZH58o",
    "Achille": "94VTtZwvNmsppde6nAW0", "GeorgeV": "JBFqnCBsd6RMkjVDRZzb",
    "KevinElliott": "MJyi2qJnZ6cONaNAgdKu", "BrianRaspy": "lwGnQIn0Z9pl1SoUiXZ3",
    "Callum": "N2lVS1w4EtoT3dr4eOWO", "Bloodgrin": "KTAbPR4QFlhaTpde6md8",
    "Branok": "Vs5CmVCVJwW4odQS2pVf", "Brian": "nPczCjzI2devNBz1zQrb",
    "Harry": "SOYHLrjzK2X1ezoPC6cr", "Roger": "CwhRBWXzGAHq8TQ4Fs17",
}

# character -> (anchor images, voice-lock note, audition line, [candidates])
CAST = [
    ("Virginia Reed", ["virginia_reed", "virginia_snow"],
     "Bright young American girl's voice, plain and unactorly. Carries all the VO.",
     "We have got through with our lives. But Cousin... never take no cutoffs. And hurry along as fast as you can.",
     ["Jessica", "Sarah", "Laura"]),
    ("James Reed", ["james_reed"],
     "Firm, clipped, proud American baritone — a man used to being obeyed.",
     "I'll go through to California, and I'll come back for you with bread in both hands. Look after your mother.",
     ["Adam", "Damien", "Eric"]),
    ("Margaret Reed", ["margaret_reed", "margaret_snow"],
     "Low, steady, exhausted-warm American alto.",
     "And I will pay you double, in cattle, when we reach California.",
     ["Matilda", "Bella"]),
    ("George Donner", ["george_donner", "george_snow"],
     "Slow, warm, elderly farmer's rumble.",
     "Write that down twice, Mrs. Donner. Everything new and pleasing... that is worth writing twice.",
     ["Bill", "Henry"]),
    ("Tamsen Donner", ["tamsen_donner", "tamsen_snow"],
     "Precise, quiet schoolteacher's diction, New England flavor.",
     "We are leaving a known road, on the word of a man none of us has ever met. ... Remember your mother. Say it.",
     ["Lily", "Alice"]),
    ("Charles Stanton", ["stanton", "stanton_snow"],
     "Gentle, mild, unfailingly courteous tenor. The money line — must land gentle, not ominous.",
     "There's bread, and beef, and Captain Sutter's mules. ... Yes. I am coming soon.",
     ["Chris", "Will", "Achille"]),
    ("Patrick Breen", ["breen", "breen_snow"],
     "Soft Irish brogue, prayerful cadence. (No Irish premade on the roster — judge who carries it.)",
     "Snowing fast. Snow higher than the shanty. No living thing without wings can get about.",
     ["GeorgeV", "KevinElliott", "BrianRaspy"]),
    ("Lewis Keseberg", ["keseberg", "keseberg_snow"],
     "German-accented English, controlled, unsettlingly calm — menace without a growl.",
     "I often think the Almighty has singled me out... to see how much a man can bear.",
     ["Callum", "Bloodgrin", "Branok"]),
    ("William Eddy", ["eddy", "eddy_snow"],
     "Flat, hard frontier drawl.",
     "Foster has begun to look at you when he talks of food. Go. Now. Don't keep to the trail.",
     ["Brian", "Harry", "Roger"]),
    ("Mary Graves", ["mary_graves", "mary_snow"],
     "Clear young American voice, steadier than the men's. Keep well apart from Virginia in pitch.",
     "Mr. Stanton... are you coming?",
     ["Sarah", "Laura"]),
    ("Levinah Murphy", ["murphy_woman"],
     "Frail, dazed — one immortal line. Add breathiness via voice settings rather than a new voice.",
     "Are you men from California... or do you come from heaven?",
     ["Bella", "Matilda"]),
    ("James Clyman", ["clyman"],
     "Leathery old trapper — grave, unhurried warning.",
     "Take the regular wagon track, and never leave it. It is barely possible to get through if you follow it. It may be impossible if you don't.",
     ["Roger", "Bill"]),
]


def tts(voice_id: str, text: str, dest: Path):
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2"}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        dest.write_bytes(r.read())


def median_f0(path: Path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn",
                          "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True).stdout
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


# ---- generate ----
slug = lambda s: s.lower().replace(" ", "_")
takes = {}  # (char, cand) -> (mp3 rel path, f0)
for char, anchors, note, line, cands in CAST:
    for cand in cands:
        mp3 = VO / f"{slug(char)}__{cand}.mp3"
        if not mp3.exists():
            print(f"tts {char} / {cand}")
            tts(VOICES[cand], line, mp3)
        takes[(char, cand)] = (f"vo_auditions/{mp3.name}", median_f0(mp3))

# ---- html ----
import html as H
cards = []
for char, anchors, note, line, cands in CAST:
    imgs = "".join(f'<img src="anchors/{a}.png" title="{a}">' for a in anchors)
    rows = []
    for i, cand in enumerate(cands):
        rel, f0 = takes[(char, cand)]
        hz = f"{f0:.0f} Hz" if f0 else "—"
        star = ' <span class="pick">primary</span>' if i == 0 else ""
        rows.append(f'<div class="take"><span class="vname">{cand}{star}</span>'
                    f'<span class="hz">{hz}</span>'
                    f'<audio controls preload="none" src="{rel}"></audio></div>')
    cards.append(f"""
<div class="char">
  <div class="portraits">{imgs}</div>
  <div class="info">
    <h2>{H.escape(char)}</h2>
    <p class="note">{H.escape(note)}</p>
    <p class="line">&ldquo;{H.escape(line)}&rdquo;</p>
    {''.join(rows)}
  </div>
</div>""")

page = f"""<!doctype html><meta charset="utf-8"><title>The Cutoff — voice casting</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.5 -apple-system, sans-serif;
       max-width: 1060px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight:600; }} h2 {{ margin:0 0 4px; }}
.char {{ display:flex; gap:18px; margin:20px 0; padding:16px; background:#1d1d22;
         border-radius:10px; }}
.portraits {{ display:flex; gap:8px; flex-shrink:0; }}
.portraits img {{ height:230px; border-radius:6px; }}
.note {{ color:#9ab; margin:2px 0 6px; font-size:13px; }}
.line {{ color:#ffd479; font-style:italic; margin:4px 0 12px; }}
.take {{ display:flex; align-items:center; gap:12px; margin:6px 0; }}
.vname {{ width:150px; font-weight:600; }}
.pick {{ font-size:11px; background:#3a5f3a; padding:1px 7px; border-radius:9px;
         font-weight:400; margin-left:6px; }}
.hz {{ width:64px; color:#889; font-size:13px; }}
audio {{ height:32px; width:360px; }}
</style>
<h1>THE CUTOFF — voice casting auditions</h1>
<p>Each candidate reads the character's key line (ElevenLabs eleven_multilingual_v2).
Median f0 measured per take — spread the final cast so no two leads sit on the
same pitch. Left portrait = trail era, right = winter.</p>
{''.join(cards)}
"""
(PROJ / "casting.html").write_text(page)
n = sum(len(c[4]) for c in CAST)
print(f"wrote donner_party/casting.html ({len(CAST)} characters, {n} takes)")
