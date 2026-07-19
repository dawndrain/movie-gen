#!/usr/bin/env python3
# TEMPLATE — ElevenLabs voice auditions page (portrait next to players, pitch stats).
# Originated in a local-only project; this template is the canonical copy.
# Project-specific paths/spec: copy into a new film folder and adapt.
"""TTS voice auditions with median-F0 pitch stats,
plus auditions.html pairing each character's anchor portrait with the playable
candidates. Usage: python3 make_auditions.py   (skips existing; re-run = retry)
"""
import html
import json
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from spec import AUDITIONS, VOICES

HERE = Path(__file__).parent
OUT = HERE / "auditions"
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()

# character -> anchor image shown beside the players (AI has no body: use carl
# frame a4 stand-in note instead)
PORTRAIT = {
    "carl": "carl", "donut": "donut_crowned", "ai": None,
    "mordecai": "mordecai_rat", "odette": "odette", "zev": "zev",
    "maestro": "maestro", "brandon": "brandon", "elle": "elle",
    "agatha": "agatha", "maggie": "maggie", "juicer": None, "lijun": None,
}


def tts(char: str, voice: str, text: str) -> str:
    out = OUT / f"{char}_{voice}.mp3"
    if out.exists():
        return f"skip {out.name}"
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[voice][0]}",
        data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2"}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    err = ""
    for attempt in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out.write_bytes(r.read())
            return f"OK   {out.name}"
        except Exception as e:
            err = str(e)
    return f"FAIL {out.name}: {err}"


def median_f0(mp3: Path) -> float:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", "22050",
         "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    sr, win = 22050, int(22050 * 0.04)
    f0s = []
    for i in range(0, len(x) - win, win // 2):
        w = x[i:i + win]
        if np.sqrt((w ** 2).mean()) < 0.02:
            continue
        w = w - w.mean()
        ac = np.correlate(w, w, "full")[win - 1:]
        lo, hi = int(sr / 300), int(sr / 60)
        if hi >= len(ac):
            continue
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] > 0.3 * ac[0]:
            f0s.append(sr / lag)
    return float(np.median(f0s)) if f0s else 0.0


def main():
    OUT.mkdir(exist_ok=True)
    jobs = [(c, v, line) for c, (line, vs) in AUDITIONS.items() for v in vs]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(lambda j: tts(*j), jobs):
            print(r, flush=True)

    cards = []
    for char, (line, voices) in AUDITIONS.items():
        rows = []
        for i, v in enumerate(voices):
            mp3 = OUT / f"{char}_{v}.mp3"
            f0 = median_f0(mp3) if mp3.exists() else 0
            tag = ' <span class="tag">provisional pick</span>' if i == 0 else ""
            rows.append(
                f'<div class="cand"><div class="vname">{html.escape(VOICES[v][1])}'
                f'{tag} <span class="f0">{f0:.0f} Hz</span></div>'
                f'<audio controls preload="none" src="auditions/{char}_{v}.mp3"></audio></div>')
        img = (f'<img src="anchors/{PORTRAIT[char]}.png" loading="lazy">'
               if PORTRAIT.get(char) else
               '<div class="noimg">voice only<br>(no body)</div>')
        cards.append(f"""
<div class="card">
  {img}
  <div class="meta">
    <h2>{char.upper()}</h2>
    <p class="line">&ldquo;{html.escape(line)}&rdquo;</p>
    {''.join(rows)}
  </div>
</div>""")

    page = f"""<!doctype html><meta charset="utf-8"><title>Dungeon Crawler Carl — voice auditions</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.45 -apple-system, sans-serif;
       max-width: 1000px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight:600; }}
.card {{ display:flex; gap:18px; margin:18px 0; padding:14px; background:#1d1d22;
         border-radius:10px; }}
.card img {{ width:220px; border-radius:6px; object-fit:cover; flex-shrink:0; }}
.noimg {{ width:220px; border-radius:6px; background:#26262e; color:#778;
          display:flex; align-items:center; justify-content:center;
          text-align:center; flex-shrink:0; }}
.meta {{ flex:1; }} .meta h2 {{ margin:0 0 4px; font-size:18px; color:#fc6; }}
.line {{ color:#ffd479; font-style:italic; margin:4px 0 12px; }}
.cand {{ margin:8px 0; }}
.vname {{ font-size:14px; margin-bottom:2px; }}
.f0 {{ color:#889; font-size:12px; margin-left:6px; }}
.tag {{ background:#3a5f3a; font-size:11px; padding:2px 8px; border-radius:10px;
        margin-left:6px; }}
audio {{ width:100%; max-width:440px; height:32px; }}
p.note {{ color:#aab; }}
</style>
<h1>Dungeon Crawler Carl — voice auditions</h1>
<p class="note">Provisional picks used for the v1 animatic are tagged; re-cast
any of them and re-run make_animatic.py (only changed lines re-bill). The AI
has no portrait — it is a voice in the walls.</p>
{''.join(cards)}
"""
    (HERE / "auditions.html").write_text(page)
    print(f"wrote auditions.html ({sum(len(v[1]) for v in AUDITIONS.values())} takes)")


if __name__ == "__main__":
    main()
