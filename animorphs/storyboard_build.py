#!/usr/bin/env python3
"""Build animorphs/storyboard.html: every shot in order — frame image, playable clip
(if rendered), beat title, dialogue. Rerun after any change."""
import html
from pathlib import Path

HERE = Path(__file__).parent

# (shot, act header or None, beat title, dialogue/action)
SHOTS = [
    ("f1", "Act 0 — Frame story (Earth)", "A hawk over a hidden valley", "(silent aerial)"),
    ("f2", None, "Jara begins the tale",
     'JARA: "Come, Tobias. Sit. I tell you story. Story of before. Story of Dak Hamee and Aldrea."'),
    ("f3", None, "Title", 'TITLE CARD: "THE HORK-BAJIR CHRONICLES"'),
    ("a1", "Act 1 — Exile", "The dome ship arrives", "(silent — Seerow's exile posting)"),
    ("a2", None, "Father and daughter",
     'ALDREA: "You were a prince, father. Now they send you to watch trees grow at the edge of nowhere."  '
     'SEEROW: "I gave the Yeerks the stars, Aldrea. Kindness was my crime. We will not speak of it again."'),
    ("a3", None, "Aldrea on the ridge", "(silent gallop, stalk eyes on the valley)"),
    ("b1", "Act 2 — Dak", "Valley life", "(silent — bark, families, peace)"),
    ("b2", None, "The shapes in the dust",
     'JAGIL: "Dak Hamee make shapes. Why make shapes?"  DAK: "It is the sky, Jagil. The lights move. I watched. They move in circles."'),
    ("b3", None, "Seer",
     'ELDER: "Dak Hamee is seer. Born one time in all times. Seer come when change come."'),
    ("b4", None, "First contact",
     'DAK: "You are not of the trees. Not of the valley."  ALDREA: "No. I am Aldrea. I come from the sky you watch."'),
    ("b5", None, "The star map",
     'ALDREA: "That light is not a hole in the sky, Dak. It is a sun. Like yours. And around it, worlds."  DAK: "Worlds. Dak wants to see."'),
    ("b6", None, "Andalite falls like stone",
     'DAK (laughing): "Andalite falls like stone!"'),
    ("b7a", None, "The kafit bird (morph demo)",
     "(silent — Aldrea flows into a six-winged kafit bird; Dak's astonished delight)"),
    ("b7b", None, "First flight",
     "(silent — the kafit soars the canopy; Dak races along the branches below)"),
    ("c1", "Act 3 — The Deep", "Descent",
     'ALDREA: "My father\'s instruments found something below the Deep, Dak. Something old. Something alive."'),
    ("c2", None, "Monster of the Deep", "(silent — the engineered guardian lunges)"),
    ("c3", None, "The buried city", 'DAK: "What... is this place?"'),
    ("c4", None, "The Arn",
     'ARN: "Hork-Bajir. On my doorstep. You were not made to ask questions."'),
    ("c5", None, "Gardeners",
     'ARN: "Long ago the sky burned. We made the trees to heal the air. And we made YOU to tend the trees. Gardeners. Tools. Nothing more."'),
    ("c6", None, "A tool that learned to dream",
     'DAK: "I am not a people. I am a tool that learned to dream."  ALDREA: "A tool cannot choose, Dak. You choose. That makes you a people."'),
    ("d1", "Act 4 — The Yeerks", "Bug fighters", "(silent descent through Mother Sky)"),
    ("d2", None, "Esplin 9466",
     'ESPLIN: "Scans show no weapons. No metal. No fire. Only bodies. Billions of strong, bladed bodies."'),
    ("d3", None, "The first pool", "(silent horror at the earthen pool)"),
    ("d4", None, "Jagil is... better now",
     'DAK: "Jagil. You did not eat. You do not laugh. Where does Jagil go at night?"  JAGIL (flat): "Jagil is here. Jagil is... better now."'),
    ("d5", None, "The dome burns", 'SEEROW: "Aldrea — RUN!"'),
    ("d6", None, "All of them",
     'ALDREA: "Father. Mother. Barafin. All of them. They are all of them dead."'),
    ("e1a", "Act 5 — Resistance", "A word for war (i)",
     'ALDREA: "The Yeerks take bodies, Dak. They will take every Hork-Bajir in the world unless we fight."'),
    ("e1b", None, "A word for war (ii)",
     'DAK: "Hork-Bajir do not fight. Hork-Bajir do not even have a word for war."  ALDREA: "Then we will teach them one."'),
    ("e2", None, "Borrowing", 'DAK: "What do you do?"  ALDREA: "Borrowing. Watch."'),
    ("e3", None, "The morph", "(silent — Andalite to Hork-Bajir)"),
    ("e4", None, "Blades for blades",
     'DAK: "Blades were for bark. Now blades must be for blades."'),
    ("e5", None, "Hork-Bajir blood",
     'DAK: "He was Hork-Bajir too. The Yeerk was in his head, but the blood is Hork-Bajir blood. What are we becoming?"'),
    ("e6", None, "Esplin takes interest",
     'ESPLIN: "A resistance. Led by an Andalite. Interesting. Tell the Sub-Visser I want that blue body taken alive. Someday it will be mine."'),
    ("g1", "Act 6 — Alloran", "Eight warriors",
     'ALLORAN: "Eight warriors. That is what the council sends. Eight, for a world already lost."'),
    ("g2", None, "Sentiment",
     'ALLORAN: "Your father\'s kindness armed the enemy, child. Sentiment is how wars are lost."  ALDREA: "And what do you call eight million Hork-Bajir, War-Prince? Acceptable losses?"'),
    ("g3", None, "The quantum virus",
     'ALLORAN: "If the Yeerks want Hork-Bajir bodies... we deny them the bodies."'),
    ("g4", None, "The theft", "(silent night heist)"),
    ("g5", None, "The vial falls", "(ambush — Dak wounded, the canister shatters below)"),
    ("g6", None, "Silent valleys", "(silent — the world after the virus)"),
    ("h1", "Act 7 — Nothlit", "Two hours passed long ago",
     'DAK: "Aldrea. The sun rises. Your two hours..."  ALDREA: "Passed long ago, Dak Hamee. I am Hork-Bajir now. Your people are my people. Your fight is my fight."'),
    ("h2", None, "While one is free",
     'DAK: "The Yeerks take the world. They do not take all. While one Hork-Bajir is free — Hork-Bajir are free."'),
    ("h3", None, "Esplin ascendant",
     'ESPLIN: "Sub-Visser Esplin, nine-four-double-six. Next, the Andalite home world. Next — everything."'),
    ("i1", "Act 8 — Frame close", "The tale ends",
     'JARA: "Dak and Aldrea fight long. Fight until end. Their kawatnoj — their children\'s children — still free."'),
    ("i2", None, "Toby",
     'JARA: "This is Toby. Toby Hamee. Named for you, Tobias."  TOBY: "I am a seer, like Dak. I see what others do not see. I see us free."'),
    ("i3", None, "Into the sunset", "(silent — the hawk flies; fade out)"),
]

CLIP_DIRS = ["outputs/hb1", "outputs/hb2", "outputs/hb3"]  # later dirs win


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
            rows.append(f'<h2>{html.escape(act)}</h2>')
        fname = shot if (HERE / "frames" / f"{shot}.png").exists() else shot.rstrip("ab")
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
<title>The Hork-Bajir Chronicles — storyboard</title>
<style>
 body {{ background:#111; color:#ddd; font:15px/1.5 -apple-system, sans-serif;
        max-width:1200px; margin:2em auto; padding:0 1em; }}
 h1 {{ font-weight:200; letter-spacing:.15em; }}
 h2 {{ color:#8fb; font-weight:300; border-bottom:1px solid #333; margin-top:2em; }}
 .shot {{ display:flex; gap:1em; margin:1.2em 0; background:#1a1a1a; border-radius:10px;
         padding:.8em; }}
 .media {{ display:flex; gap:.6em; }}
 .media img, .media video {{ width:380px; border-radius:6px; object-fit:cover; }}
 .missing {{ width:380px; display:flex; align-items:center; justify-content:center;
            color:#555; border:1px dashed #333; border-radius:6px; min-height:214px; }}
 .tag {{ background:#264; color:#cfc; border-radius:4px; padding:0 .5em; font-family:monospace; }}
 .meta p {{ color:#aaa; }}
</style>
<h1>THE HORK-BAJIR CHRONICLES</h1>
<p>First-pass storyboard — {len(SHOTS)} shots. Frames: Nano Banana Pro. Clips: Seedance 2.0 480p std.</p>
{"".join(rows)}'''
    (HERE / "storyboard.html").write_text(page)
    print("wrote", HERE / "storyboard.html")


if __name__ == "__main__":
    main()
