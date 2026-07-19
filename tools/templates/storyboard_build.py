#!/usr/bin/env python3
# TEMPLATE — copied from other_movies/carl/storyboard_build.py (storyboard.html generator).
# Project-specific: expects that film's spec/paths. Copy into a new film
# folder and adapt; the original in other_movies/carl/ is the working example.
"""storyboard.html for the DCC animatic: every shot in cut order with its
frame, dialogue, playable segment, and collapsed generation prompt."""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import spec

HERE = Path(__file__).parent
PROMPTS = {n: p for n, _, p, _ in spec.FRAMES}
REFS = {n: r for n, _, _, r in spec.FRAMES}

rows = []
for idx, shot in enumerate(spec.ORDER):
    lines = spec.LINES.get(shot, [])
    dlg = "".join(f'<div class="dl"><b>{sp.upper()}</b> {html.escape(tx)}</div>'
                  for sp, tx in lines) or '<div class="dl mute">— silent hold —</div>'
    seg = f"outputs/animatic_segs/{idx:02d}_{shot}.mp4"
    seg_tag = (f'<video controls preload="none" src="{seg}"></video>'
               if (HERE / seg).exists() else "")
    rows.append(f"""
<div class="shot" id="{shot}">
  <div class="left">
    <img src="frames/{shot}.png" loading="lazy">
    {seg_tag}
  </div>
  <div class="right">
    <h2>{idx + 1:02d} &middot; {shot}</h2>
    {dlg}
    <details><summary>prompt &middot; refs: {', '.join(REFS[shot]) or 'none'}</summary>
    <p class="prompt">{html.escape(PROMPTS[shot])}</p></details>
  </div>
</div>""")

page = f"""<!doctype html><meta charset="utf-8"><title>DCC book one — storyboard</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.5 -apple-system, sans-serif;
       max-width: 1180px; margin: 24px auto; padding: 0 16px; }}
.shot {{ display:flex; gap:18px; margin:20px 0; padding:14px; background:#1d1d22;
         border-radius:10px; }}
.left {{ width:520px; flex-shrink:0; }}
.left img, .left video {{ width:100%; border-radius:6px; display:block; margin-bottom:8px; }}
.right {{ flex:1; }} h2 {{ margin:0 0 8px; font-size:17px; color:#fc6; }}
.dl {{ margin:6px 0; }} .dl b {{ color:#9ad; margin-right:6px; }}
.dl.mute {{ color:#778; font-style:italic; }}
details {{ margin-top:10px; color:#aab; }} .prompt {{ font-size:13px; color:#99a; }}
</style>
<h1>Dungeon Crawler Carl — book one animatic</h1>
<p>{len(spec.ORDER)} shots. Segments are playable once built; the full cut is
outputs/animatic_v1.mp4.</p>
{''.join(rows)}
"""
(HERE / "storyboard.html").write_text(page)
print(f"wrote storyboard.html ({len(spec.ORDER)} shots)")
