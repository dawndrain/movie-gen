#!/usr/bin/env python3
"""Build overwhelming_beauty/storyboard.html: every shot in cut order — frame,
playable clip, beat title, dialogue/narration. Rerun after any change."""
import html
from pathlib import Path

HERE = Path(__file__).parent

# (shot, act header or None, beat title, audio/dialogue description)
SHOTS = [
    ("t1", "Act 1 — Specification", "The commute",
     'NARR: "The first thing Oren noticed was the color of the sky."'),
    ("t2", None, "Oren stops", "(the crowd streams around him like water around a piling)"),
    ("t3", None, "The sky",
     'NARR: "It was not blue the way a data entry in a file is blue… like a drawer sliding open."'),
    ("t4", None, "Title card", "THE VARIANCE"),
    ("t5", None, "The fabrication hall",
     'NARR: "Oren was a twenty-four F… The F vocabulary contained no word for yearning."'),
    ("t6", "Act 2 — Things falling into the drawer", "A woman's laugh",
     "(one bright laugh; Oren turns; nobody else reacts)"),
    ("t7", None, "The screens turn gold", "(the UV filters adjust; the gold dies)"),
    ("t8", None, "His own hand", 'NARR: "Things kept falling into it."'),
    ("t9", None, "The running figure", "(the moisture stain, studied like a painting)"),
    ("t10", None, "The dead stem",
     'NARR: "He began arriving late. He took detours. He found himself standing in places."'),
    ("t11a", None, "Metric drift (i)",
     'PETRA: "Your metric profile is showing drift. Is there something in your routine we should adjust? Sleep architecture? Caloric intake?"'),
    ("t11b", None, "Metric drift (ii)", 'OREN: "No. I think— …I\'ll re-baseline."'),
    ("t12", "Act 3 — Eleven days", "The archive",
     'OREN (whisper): "The only way to deal with this life meaningfully is to find one\'s passion and dive into it with everything you have."'),
    ("t13", None, "Walking out",
     'NARR: "For eleven days, Oren lived. That was the only word for it."'),
    ("t14", None, "Dez",
     'DEZ: "You\'re telling me about the sky. Twenty-six years old, and nobody ever told him about the sky. Come on. There\'s somewhere you need to see."'),
    ("t15", None, "The old quarter", "(music from somewhere he can't identify)"),
    ("t16a", None, "The rooftop (i)",
     'OREN: "I want to see the ocean — I want to learn an instrument — I want to read everything ever written!"'),
    ("t16b", None, "The rooftop (ii)",
     'OREN: "I want to understand why I was asleep for twenty-six years."  DEZ: "Then don\'t go back to sleep."'),
    ("t17", None, "Too bright",
     'NARR: "He barely slept. He couldn\'t. Everything was too much. Too bright. Too interesting."'),
    ("t18", "Act 4 — Variance collapse", "The twelfth day",
     'NARR: "The crash came on the twelfth day."'),
    ("t19", None, "Petra finds him",
     'OREN: "I can\'t stop it. There\'s too much. I opened something, and I can\'t close it — and I can\'t hold it open either."  PETRA: "I know."'),
    ("t20a", None, "I was alive", 'OREN (crying): "I was alive. For eleven days… I was alive."'),
    ("t20b", None, "Does it have to stop?",
     'PETRA: "Yes."  OREN: "Does it have to stop?"  (she doesn\'t answer)'),
    ("t21", "Act 5 — Baseline", "Restoration",
     'NARR: "It wasn\'t punishment. It was restoration, they called it. A return to specification."'),
    ("t22", None, "The commute, again",
     'NARR: "The sky was above him… It was blue. He knew this the way one knows a data entry in a file."'),
    ("t23", None, "Baseline", "(metrics nominal)"),
    ("t24", None, "The hand",
     'NARR: "He didn\'t know why he did this. But he didn\'t stop."'),
]

CLIP_DIRS = ["outputs/tv1"]  # later dirs win


def clip_for(shot: str):
    best = None
    for d in CLIP_DIRS:
        p = HERE / d / f"{shot}.mp4"
        if p.exists():
            best = p
    return best


def main():
    rows = []
    for shot, act, title, dialog in SHOTS:
        if act:
            rows.append(f"<h2>{html.escape(act)}</h2>")
        fname = shot[:-1] if shot[-1] in "ab" else shot
        frame = HERE / "frames" / f"{fname}.png"
        img = (f'<img src="frames/{fname}.png" loading="lazy">' if frame.exists()
               else '<div class="missing">frame pending</div>')
        clip = clip_for(shot)
        vid = (f'<video src="{clip.relative_to(HERE)}" controls preload="none"></video>'
               if clip else '<div class="missing">clip pending</div>')
        rows.append(f'''
<div class="shot" id="{shot}">
  <div class="media">{img}{vid}</div>
  <div class="meta">
    <span class="tag">{shot}</span> <b>{html.escape(title)}</b>
    <p>{html.escape(dialog)}</p>
  </div>
</div>''')

    page = f'''<!doctype html><meta charset="utf-8">
<title>THE VARIANCE — storyboard</title>
<style>
 body {{ background:#101318; color:#cfd6dd; font:15px/1.5 -apple-system, sans-serif;
        max-width:1200px; margin:2em auto; padding:0 1em; }}
 h1 {{ font-weight:200; letter-spacing:.35em; color:#9fb4c7; }}
 h2 {{ color:#7da2c1; font-weight:300; border-bottom:1px solid #26303a; margin-top:2em; }}
 .shot {{ display:flex; gap:1em; margin:1.2em 0; background:#171c23; border-radius:10px;
         padding:.8em; }}
 .media {{ display:flex; gap:.6em; }}
 .media img, .media video {{ width:380px; border-radius:6px; object-fit:cover; }}
 .missing {{ width:380px; display:flex; align-items:center; justify-content:center;
            color:#4a5561; border:1px dashed #26303a; border-radius:6px; min-height:214px; }}
 .tag {{ background:#22303d; color:#9fc4e0; border-radius:4px; padding:0 .5em; font-family:monospace; }}
 .meta p {{ color:#8a95a1; }}
</style>
<h1>THE VARIANCE</h1>
<p>First pass — {len(SHOTS)} shots. Frames: Nano Banana Pro 2k. Clips: Seedance 2.0 480p FAST draft.
Voices: Caspian (Oren), Nora (Petra), Roxie (Dez), Alistair (narrator).</p>
{"".join(rows)}'''
    (HERE / "storyboard.html").write_text(page)
    print("wrote", HERE / "storyboard.html")


if __name__ == "__main__":
    main()
