#!/usr/bin/env python3
"""Rebuild a simple storyboard page for each historical cut (assemble_v*.py).

Parses each assembler's CUT list and emits storyboard_cut_<v>.html: every entry in
cut order with a playable clip, trim/mute notes. No dialogue metadata (that lived in
the era's storyboard_gen SHOTS), but enough to compare takes across versions.
Usage: python3 rebuild_storyboards.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
DIRS = {"V1": "outputs/video", "V2": "outputs/video2", "V3": "outputs/video3",
        "V4": "outputs/video4", "V5": "outputs/video5", "V6": "outputs/video6",
        "V7": "outputs/video7", "V8": "outputs/video8", "V9": "outputs/video9",
        "V10": "outputs/video10", "V11": "outputs/video11", "V12": "outputs/video12",
        "WHITE": "outputs"}

ENTRY = re.compile(r'\((V\d+|WHITE)(?: / "([^"]+)")?, ([\d.]+), (None|[\d.]+), (True|False)')

pages = []
for asm in sorted(ROOT.glob("assemble_v*.py"),
                  key=lambda p: int(re.search(r"\d+", p.stem).group())):
    ver = "v" + re.search(r"\d+", asm.stem).group()
    text = asm.read_text()
    rows = []
    for m in ENTRY.finditer(text):
        d, name, ts, td, mute = m.groups()
        clip = f"{DIRS[d]}/{name}" if name else "outputs/white_flash.mp4"
        notes = []
        if float(ts) > 0 or td != "None":
            notes.append(f"trim {ts}s → {'end' if td == 'None' else td + 's'}")
        if mute == "True":
            notes.append("muted")
        exists = (ROOT / clip).exists()
        vid = (f'<video controls preload="none" width="340"><source src="{clip}"></video>'
               if exists else '<div class="miss">clip missing on disk</div>')
        rows.append(f'<div class="shot">{vid}<div class="meta"><b>{html.escape(Path(clip).stem)}</b>'
                    f'<br><span class="path">{html.escape(clip)}</span>'
                    f'{"<br><i>" + ", ".join(notes) + "</i>" if notes else ""}</div></div>')
    page = f"""<!doctype html><meta charset="utf-8"><title>The Long Game — cut {ver}</title>
<style>body{{background:#141417;color:#e8e8ea;font:14px/1.4 -apple-system,sans-serif;
max-width:900px;margin:24px auto;padding:0 16px}}
.shot{{display:flex;gap:14px;margin:10px 0;padding:10px;background:#1d1d22;border-radius:8px}}
video{{border-radius:5px;background:#000;flex-shrink:0}}
.path{{color:#667;font-size:12px}} .miss{{color:#e6a23c;width:340px}}
h1{{font-weight:600}}</style>
<h1>The Long Game — cut {ver} ({len(rows)} entries, in cut order)</h1>
<p>Reconstructed from {asm.name}. Compare with other storyboard_cut_*.html versions.</p>
{"".join(rows)}"""
    out = ROOT / f"storyboard_cut_{ver}.html"
    out.write_text(page)
    pages.append(f"{out.name}: {len(rows)} entries")
print("\n".join(pages))
