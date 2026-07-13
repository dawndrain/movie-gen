#!/usr/bin/env python3
"""Build animorphs_david/storyboard.html: every shot in cut order — frame image,
playable clip (if rendered), beat title, dialogue. Rerun after any change."""
import html
from pathlib import Path

HERE = Path(__file__).parent

# (shot, act header or None, beat title, dialogue/action)
SHOTS = [
    ("a1", "Act A — The Discovery", "The blue box", "(silent — David finds the cube at the construction site)"),
    ("a2", None, "Best offer",
     'DAVID: "Strange blue box, found at a construction site. One hundred bucks or best offer. ... Somebody out there wants you, little box. I can feel it."'),
    ("a3", None, "Title", 'TITLE CARD: "ANIMORPHS — THE DAVID TRILOGY"'),
    ("a4a", None, "Marco finds the listing",
     'MARCO: "Jake. Tell me that is not what I think it is."  JAKE: "The morphing cube. Elfangor\'s cube."'),
    ("a4b", None, "The race begins",
     'MARCO: "It\'s on a public auction site, Jake. If we found it, the Yeerks found it an hour ago."  JAKE: "Then we go tonight."'),
    ("a5", None, "The raid", "(silent — Yeerk forces hit David's house; his parents are taken)"),
    ("v1", None, "Visser Three",
     'VISSER THREE: "A human child found the Escafil device... and offered it for sale. On their internet. Find the boy. Bring me the box. And bring me the boy."'),
    ("a6", None, "Nowhere to go",
     'DAVID: "Those things at my house. They took my mom and dad. Tell me what is happening."  JAKE: "They\'re called Yeerks. They take people. You can\'t go home, David. Not ever again."'),
    ("a7", None, "The seventh",
     'JAKE: "Put your hand on it. You\'ll be one of us. The seventh."  MARCO (low): "For the record? Bad idea."'),
    ("a8", None, "First morph", "(silent — David becomes a golden eagle; first flight)"),
    ("b1", "Act B — The Threat", "Hello, king",
     'DAVID: "Hawks. Wolves. Kid stuff. This is more like it. Hello, king."'),
    ("b2a", None, "The rules",
     'JAKE: "World leaders downstairs, Yeerks in the walls. We watch. We report. We do not engage. Nothing happens unless I say it happens."'),
    ("b2b", None, "Nobody is the boss of me",
     'DAVID: "You know your problem, Jake? You think you\'re the boss of me. Nobody is the boss of me."'),
    ("b3", None, "The mission burns", "(silent — a lion breaks cover in the summit hotel)"),
    ("b4a", None, "The accusation",
     'MARCO: "He broke cover. He blew the mission. He almost got us killed. Twice."'),
    ("b4b", None, "Because of you people",
     'DAVID: "You get to go home after. To your dad. To your bed. I sleep in a barn. I lost everything. Because of you people."'),
    ("b5", None, "The eagle stoops", "(silent — the attack on Tobias's meadow; drifting feathers)"),
    ("b6", None, "Feathers",
     'RACHEL: "He killed him, Jake. He killed Tobias. Don\'t tell me you weren\'t thinking it too."  JAKE: "He wants us hunting him angry. We end this my way."'),
    ("b7a", None, "Tiger and lion",
     'DAVID: "The famous Jake. Came alone. You should have let me sell the box."  JAKE: "It ends tonight, David."'),
    ("b7b", None, "The fight", "(silent — tiger vs lion through the house frames)"),
    ("b7c", None, "Rachel's warning",
     'DAVID: "Say it. Say I win."  RACHEL: "Touch him again, and there is no morph on Earth that will save you."'),
    ("c1a", "Act C — The Solution", "No good options",
     'JAKE: "We can\'t kill him. We can\'t watch our backs forever. And we can\'t hand him to the Yeerks."'),
    ("c1b", None, "The third way",
     'CASSIE: "Then we don\'t do any of those. There is a third way. You\'re all going to hate it. Especially me."'),
    ("c2a", None, "Tobias lives",
     'TOBIAS: "Before anyone cries at my funeral — the eagle got a wild hawk. Not me. I\'ve been shadowing David for two days. I know where he sleeps."'),
    ("c2b", None, "Don't you ever",
     'RACHEL: "You\'re alive. Don\'t you EVER do that to me again."'),
    ("c3", None, "The plan", "(silent — the map, the cove, the X)"),
    ("c4a", None, "The staged meeting (i)",
     'JAKE (too loud, for the rat under the floor): "Tomorrow. Dawn. We move the cube to the sea cave at Widows Point. Rachel carries it. Alone."'),
    ("c4b", None, "The staged meeting (ii)",
     'MARCO: "Alone? With the one thing the Yeerks want more than air?"  JAKE: "Alone. After tomorrow, no one will ever find it again."'),
    ("c5", None, "Hook, line, sinker",
     'TOBIAS: "He was here. He heard every word. Hook, line... sinker."  JAKE: "Then tomorrow, we do the worst good thing we\'ve ever done."'),
    ("c6", None, "The bait",
     'RACHEL: "It\'s just me, David! Just me, and the box! I know you\'re watching! Come and take it!"'),
    ("c7", None, "The trap springs",
     'JAKE: "Six against one, David. It\'s over."  DAVID: "The meeting. The box. All of it... a play. For me."'),
    ("c8", None, "Catch the rat", 'DAVID: "Catch the rat." (morphs rat, darts into the crevice)'),
    ("c9a", None, "The wait",
     'AX: "One hour and fifty-nine minutes. ... Two hours, Prince Jake. It is done."'),
    ("c9b", None, "The sentence",
     'AX: "He will never morph again. He will never be anything again... except what he is."'),
    ("c9c", None, "Demorph, everyone", 'JAKE: "Demorph, everyone. It\'s over."'),
    ("c10", None, "The island",
     'DAVID: "You can\'t leave me here. Rachel! RACHEL! Come back! KILL ME!"  RACHEL: "I\'m sorry, David. It\'s done."'),
    ("c12", None, "The order",
     'CASSIE: "We did the only thing we could do."  RACHEL: "Then why does it feel like this?"  JAKE: "Nobody ever mentions David again. That\'s an order."'),
    ("c13", None, "Fade out", "(silent — the rock, the rat, the grey ocean)"),
]

CLIP_DIRS = ["outputs/dv1", "outputs/dv2", "outputs/dv3"]  # later dirs win

FRAME_ALIAS = {  # split shots share the parent's frame
    "a4a": "a4", "a4b": "a4", "b2a": "b2", "b2b": "b2", "b4a": "b4",
    "b4b": "b4", "c1a": "c1", "c1b": "c1", "c2a": "c2", "c2b": "c2",
    "c4a": "c4", "c4b": "c4", "c9a": "c9", "c9b": "c9", "c9c": "c9",
}


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
        fname = FRAME_ALIAS.get(shot, shot)
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
<title>The David Trilogy — storyboard</title>
<style>
 body {{ background:#111; color:#ddd; font:15px/1.5 -apple-system, sans-serif;
        max-width:1200px; margin:2em auto; padding:0 1em; }}
 h1 {{ font-weight:200; letter-spacing:.15em; }}
 h2 {{ color:#8ab; font-weight:300; border-bottom:1px solid #333; margin-top:2em; }}
 .shot {{ display:flex; gap:1em; margin:1.2em 0; background:#1a1a1a; border-radius:10px;
         padding:.8em; }}
 .media {{ display:flex; gap:.6em; }}
 .media img, .media video {{ width:380px; border-radius:6px; object-fit:cover; }}
 .missing {{ width:380px; display:flex; align-items:center; justify-content:center;
            color:#555; border:1px dashed #333; border-radius:6px; min-height:214px; }}
 .tag {{ background:#246; color:#cdf; border-radius:4px; padding:0 .5em; font-family:monospace; }}
 .meta p {{ color:#aaa; }}
</style>
<h1>ANIMORPHS: THE DAVID TRILOGY</h1>
<p>First-pass storyboard — {len(SHOTS)} shots. Frames: Nano Banana Pro. Clips: Seedance 2.0 480p std.</p>
{"".join(rows)}'''
    (HERE / "storyboard.html").write_text(page)
    print("wrote", HERE / "storyboard.html")


if __name__ == "__main__":
    main()
