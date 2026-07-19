#!/usr/bin/env python3
"""TTS voice auditions for THE BUSY BODY via ElevenLabs, with median-F0 pitch
stats, plus auditions.html pairing each character's anchor portrait with the
playable candidates.

Usage: python3 make_auditions.py           (skips existing mp3s; re-run = retry)
"""
import html
import json
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "auditions"
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()

VOICES = {
    "callum":        ("N2lVS1w4EtoT3dr4eOWO", "Callum — Husky Trickster (US)"),
    "chris":         ("iP95p4xoKVk53GoZ742B", "Chris — Charming, Down-to-Earth (US)"),
    "liam":          ("TX3LPaxmHKxFdv7VOQHJ", "Liam — Energetic (US)"),
    "george":        ("JBFqnCBsd6RMkjVDRZzb", "George — Warm Storyteller (UK)"),
    "daniel":        ("onwK4e9ZLuTAKqWW03F9", "Daniel — Steady Broadcaster (UK)"),
    "kevin_elliott": ("MJyi2qJnZ6cONaNAgdKu", "Kevin Elliott — Professional (UK)"),
    "lily":          ("pFZP5JQG7iQjIQuC4Bku", "Lily — Velvety Actress (UK)"),
    "sarah":         ("EXAVITQu4vr4xnSDxMaL", "Sarah — Mature, Confident (US)"),
    "alice":         ("Xb7hH8MSUJpSbSDYk0k2", "Alice — Clear, Engaging (UK)"),
    "jessica":       ("cgSgspJ2msm6clMCkdW9", "Jessica — Playful, Bright (US)"),
    "henry":         ("VRAN0xryQGUWtDuwToRv", "Henry — royal, elegant, old (UK)"),
    "bill":          ("pqHfZKP75CvOlQylNhV4", "Bill — Wise, Mature, Old (US)"),
    "bloodgrin":     ("KTAbPR4QFlhaTpde6md8", "Bloodgrin — Intense (UK)"),
    "laura":         ("FGY2WhTYpPnrIDTdsKH5", "Laura — Sassy Enthusiast (US)"),
    "matilda":       ("XrExE9yKIg1WjnnlVkGX", "Matilda — Upbeat Professional (US)"),
    "will":          ("bIHbv24MWmeRgasZH58o", "Will — Relaxed Optimist (US)"),
}

# character -> (anchor png, audition line, [candidate voices], primary)
CAST = {
    "marplot": ("marplot",
        "I'm as secret as a priest when I'm trusted! ... Oh Lord, oh Lord — "
        "thieves! Thieves! ... Why, what do you beat ME for? I ha'nt married "
        "your daughter!",
        ["callum", "chris", "liam"]),
    "george": ("george",
        "The garden gate — at eight — as I used to do! There must be a meaning "
        "in this. My dear Marplot, thou art my friend, my better angel!",
        ["george", "daniel"]),
    "charles": ("charles",
        "Rascals, retire! She's my wife — touch her if you dare, I'll make "
        "dogs-meat of you.",
        ["daniel", "kevin_elliott"]),
    "miranda": ("miranda",
        "Now methinks there's nobody handsomer than you — so neat, so clean, "
        "Gardee. ... Faugh! How he stinks of tobacco.",
        ["lily", "sarah"]),
    "isabinda": ("isabinda",
        "Kill me, kill me instantly — 'twill be worse than death to wed him! "
        "... Where is he? Oh, let me fly into his arms!",
        ["alice", "jessica"]),
    "francis": ("francis",
        "She has nicked you, Sir George! He, he, he. ... Out of my doors, you "
        "dog! Adod, I am happier than the Great Mogul!",
        ["henry", "bill"]),
    "jealous": ("jealous",
        "By St. Jago — hell and furies, a man in the closet! Why don't you "
        "write a bill upon your forehead, to show passengers there's something "
        "to be let!",
        ["bloodgrin", "kevin_elliott"]),
    "patch": ("patch",
        "It is a charm for the toothache — I have worn it these seven years, "
        "'twas given me by an angel, sir!",
        ["laura", "matilda"]),
    "whisper": ("whisper",
        "Trifle, sir — the very lap-dog my lady lost! My business is no great "
        "matter of business neither... and yet 'tis business of consequence too.",
        ["will", "chris"]),
    "scentwell": ("scentwell",
        "This way, sir — through many a dark passage and dirty step.",
        ["jessica", "matilda"]),
}


def tts(char: str, voice: str, text: str) -> str:
    out = OUT / f"{char}_{voice}.mp3"
    if out.exists():
        return f"skip {out.name}"
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[voice][0]}",
        data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2"}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    for attempt in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out.write_bytes(r.read())
            return f"OK   {out.name}"
        except Exception as e:
            err = str(e)
    return f"FAIL {out.name}: {err}"


def median_f0(mp3: Path) -> float:
    """Median F0 via autocorrelation over voiced 40ms windows (pitch.py style)."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", "22050",
         "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    sr, win = 22050, int(22050 * 0.04)
    f0s = []
    for i in range(0, len(x) - win, win // 2):
        w = x[i:i + win]
        if np.sqrt((w ** 2).mean()) < 0.02:      # skip silence
            continue
        w = w - w.mean()
        ac = np.correlate(w, w, "full")[win - 1:]
        lo, hi = int(sr / 300), int(sr / 60)      # 60–300 Hz
        if hi >= len(ac):
            continue
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] > 0.3 * ac[0]:
            f0s.append(sr / lag)
    return float(np.median(f0s)) if f0s else 0.0


def main():
    OUT.mkdir(exist_ok=True)
    jobs = [(c, v, line) for c, (_, line, vs) in CAST.items() for v in vs]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(lambda j: tts(*j), jobs):
            print(r, flush=True)

    cards = []
    for char, (anchor, line, voices) in CAST.items():
        rows = []
        for i, v in enumerate(voices):
            mp3 = OUT / f"{char}_{v}.mp3"
            f0 = median_f0(mp3) if mp3.exists() else 0
            tag = ' <span class="tag">primary pick</span>' if i == 0 else ""
            rows.append(
                f'<div class="cand"><div class="vname">{html.escape(VOICES[v][1])}'
                f'{tag} <span class="f0">{f0:.0f} Hz</span></div>'
                f'<audio controls preload="none" src="auditions/{char}_{v}.mp3"></audio></div>')
        cards.append(f"""
<div class="card">
  <img src="anchors/{anchor}.png" loading="lazy">
  <div class="meta">
    <h2>{char.upper()}</h2>
    <p class="line">&ldquo;{html.escape(line)}&rdquo;</p>
    {''.join(rows)}
  </div>
</div>""")

    page = f"""<!doctype html><meta charset="utf-8"><title>The Busy Body — voice auditions</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.45 -apple-system, sans-serif;
       max-width: 1000px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight:600; }}
.card {{ display:flex; gap:18px; margin:18px 0; padding:14px; background:#1d1d22;
         border-radius:10px; }}
.card img {{ width:220px; border-radius:6px; object-fit:cover; flex-shrink:0; }}
.meta {{ flex:1; }} .meta h2 {{ margin:0 0 4px; font-size:18px; color:#9ad; }}
.line {{ color:#ffd479; font-style:italic; margin:4px 0 12px; }}
.cand {{ margin:8px 0; }}
.vname {{ font-size:14px; margin-bottom:2px; }}
.f0 {{ color:#889; font-size:12px; margin-left:6px; }}
.tag {{ background:#3a5f3a; font-size:11px; padding:2px 8px; border-radius:10px;
        margin-left:6px; }}
audio {{ width:100%; max-width:440px; height:32px; }}
p.note {{ color:#aab; }}
</style>
<h1>The Busy Body — voice auditions</h1>
<p class="note">Each character's anchor with their candidate ElevenLabs voices
(primary pick first, per voices.md). Median F0 shown per take — watch for cast
members sitting too close together in pitch. US-accent candidates rely on the
Seedance accent lock; judge timbre and energy here, not accent.</p>
{''.join(cards)}
"""
    (HERE / "auditions.html").write_text(page)
    f0_all = {f"{c}_{v}": median_f0(OUT / f"{c}_{v}.mp3")
              for c, (_, _, vs) in CAST.items() for v in vs
              if (OUT / f"{c}_{v}.mp3").exists()}
    print(json.dumps(f0_all, indent=1))
    print(f"wrote auditions.html ({sum(len(v[2]) for v in CAST.values())} takes)")


if __name__ == "__main__":
    main()
