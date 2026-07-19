#!/usr/bin/env python3
"""Build walters_deal/storyboard.html: every shot in cut order with playable clip,
dialogue, and collapsed generation prompt. Rerun after any clip change."""
import html
import re
import subprocess
from pathlib import Path

PROJ = Path(__file__).parent
V1 = PROJ / "outputs/video1"
THUMBS = PROJ / "storyboard_thumbs"
THUMBS.mkdir(exist_ok=True)

# (shot, title, dialogue)
SHOTS = [
    ("a1_rat", "Cold open — the rat", None),
    ("a2_beaming", "BEAMING", 'WALTER: "Beaming. BEAMING. It has nothing to do with beaming... It is travelling."'),
    ("a3_mob", "The lawn circus", None),
    ("a4_window", "The face at the cellar window", '(Sign: "XAVE STERN")'),
    ("a5_deal", "Deal.", 'XAVE: "I\'m here to make you a rich man." WALTER: "Me — or rather yourself?" XAVE: "Are you sure you would trust THEM more than me?" WALTER: "Deal."'),
    ("a6_lottery", "The Trekkie lottery", 'XAVE: "For ONE of you, this will be the best day ever... My number is — one!" JEREMY: "YES!"'),
    ("a7_jeremy", "First human teleport", 'WALTER: "I won\'t let you die." ... "Congratulations." (Jeremy vomits.)'),
    ("a8_mayor", "The mayor's demo", 'MAYOR: "I have to- When can we- How much do you-"'),
    ("b1_warehouse", "This is fantastic!", 'WALTER: "This is fantastic!"'),
    ("b2_stowaway", "Kristella", 'KRISTELLA: "Relax — I\'m a fan. I come in peace. ... Kristella Attenburg. Look me up in the phone book."'),
    ("b3_demo", "The dawn of a new era", 'KRISTELLA: "We are witnessing the dawn of a new era." (She turns to dust; reassembles on the big screen.)'),
    ("b4_sniper", "The sniper", None),
    ("c1_temple", "TWO YEARS LATER — the temple", 'OLD MAN: "To think that I lived long enough to experience this..."'),
    ("c2_rat2", "It hasn't decomposed", 'WALTER: "This is the first rat I ever travelled. It disappeared two years ago. ...It hasn\'t decomposed."'),
    ("c3_confess", "Neither have you", 'WALTER: "You have never travelled, have you?" XAVE: "...Neither have you." WALTER: "Maybe I\'m the devil." XAVE: "To kill a few people?" WALTER: "To kill everyone."'),
    ("c4_teens", "The booth built for one", '(The service phone rings. Her smile freezes.)'),
    ("c5_press", "Deal with the devil", 'REPORTER: "Has Walter made a deal with the devil?" KRISTELLA: "No comment."'),
    ("c6_jeremy", "Jeremy at dawn", 'JEREMY: "Is it because I was the first to travel?" WALTER: "I\'m afraid so."'),
    ("d1_epiphany", "Not enough time", 'WALTER: "Not enough time."'),
    ("d2_resurrect", "The resurrection", None),
    ("d3_lost", "Two lost years", 'JEREMY: "The last thing I remember is your basement. That was TWO YEARS ago? ...I\'m done with beaming."'),
    ("d4_isela", "Forever young", 'ISELA: "Which means... you can be forever young? ...Double that."'),
    ("e1_recluse", "FOUR YEARS LATER — the recluse", 'XAVE: "I don\'t trust an invention that scares off its own inventor. But nobody else needs to know that."'),
    ("e2_rescue", "Kristella's rescue", 'KRISTELLA: "You look like crap. Your room looks like crap."'),
    ("e3_bernand", "It's called PlayStation", 'RICK: "It\'s like saving a game on your Nintendo." BERNAND: "It\'s called PlayStation." (He is gone.)'),
    ("e4_collapse", "Kristella falls", None),
    ("e5_shutdown", "The shutdown", 'RICK: "Walter says shut it all down. ...No more blood on our hands."'),
    ("e6_bomb", "The bombing", None),
    ("f1_sorry", "Kristella. I'm sorry.", 'WALTER: "Kristella. I\'m sorry."'),
    ("f2_awake", "What time is it?", 'KRISTELLA: "What the fuck, guys. What time is it? ...And where did the coffee machine go?"'),
    ("f3_price", "The price", 'XAVE: "The save was four years old." WALTER: "Everything we were — she doesn\'t remember any of it." XAVE: "She\'s alive. You\'re welcome."'),
    ("f4_catch", "The green booth", None),
    ("f5_inside", "Back inside", 'BERNAND: "It\'s no big deal, father. ...Let\'s go back together. Back inside."'),
    ("g1_interview", "SIX YEARS LATER — the interview", 'INTERVIEWER: "They say you and Mr. Stern never use INSTANT yourselves." WALTER: "...Next question."'),
    ("g2_grave", "Graveyard number ten", 'XAVE: "And that\'s graveyard number ten."'),
    ("g3_funeral", "The INSTANT cemetery", 'WALTER: "What if I was the first to use our own INSTANT funeral service?" XAVE: "We both know that would be the first time you\'d use INSTANT... anything."'),
    ("g4_end", "Where is this all going to end?", 'WALTER: "Sometimes I stop and wonder where this is all going to end. Don\'t you ever ask yourself that question?" (Xave has no answer.)'),
]

CHAPTERS = {"a": "I — The Deal", "b": "II — The Demonstration",
            "c": "III — The Cracks (two years later)", "d": "IV — The Time Machine",
            "e": "V — The Fall (four years later)", "f": "VI — Resurrections",
            "g": "VII — The Cemetery (six years later)"}


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def load_prompts():
    text = (PROJ / "videos_v1.sh").read_text()
    vars_ = dict(re.findall(r'^([A-Z0-9]+)="(.*)"$', text, re.M))
    prompts = {}
    for m in re.finditer(r'^gen (\S+) (\d+) "(.*?)" (.*?)&?$', text, re.M | re.S):
        name, _, prompt, rest = m.groups()
        prompt = re.sub(r"\$\{?([A-Z0-9]+)\}?", lambda v: vars_.get(v.group(1), ""), prompt)
        refs = [Path(r).name for r in re.findall(r"--(?:start-image|image) (\S+)", rest)]
        prompts[name] = (prompt.strip(), refs)
    return prompts


PROMPTS = load_prompts()

rows, chapter_seen = [], set()
for shot, title, dialogue in SHOTS:
    ch = shot[0]
    if CHAPTERS[ch] not in chapter_seen:
        chapter_seen.add(CHAPTERS[ch])
        rows.append(f'<h2>{html.escape(CHAPTERS[ch])}</h2>')
    clip = V1 / f"{shot}.mp4"
    prompt_html = ""
    if shot in PROMPTS:
        p, refs = PROMPTS[shot]
        ref_s = f'<div class="refs">refs: {html.escape(", ".join(refs))}</div>' if refs else ""
        prompt_html = (f'<details><summary>generation prompt</summary>'
                       f'<p class="prompt">{html.escape(p)}</p>{ref_s}</details>')
    if not clip.exists():
        rows.append(f'<div class="shot"><div class="meta"><h3>{shot} — '
                    f'{html.escape(title)} <span class="tag visual">missing</span></h3>'
                    f'{f"<p class=dlg>{html.escape(dialogue)}</p>" if dialogue else ""}'
                    f'{prompt_html}</div></div>')
        continue
    thumb = THUMBS / f"{shot}.jpg"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1.5", "-i", str(clip),
                    "-frames:v", "1", "-vf", "scale=480:-1", str(thumb)], check=True)
    d = dur(clip)
    carried = "dialogue" if dialogue else "visual only"
    rows.append(f"""
<div class="shot">
  <video controls preload="none" poster="storyboard_thumbs/{shot}.jpg" width="480">
    <source src="outputs/video1/{shot}.mp4" type="video/mp4"></video>
  <div class="meta">
    <h3>{shot} — {html.escape(title)}
        <span class="tag {carried.split()[0]}">{carried}</span></h3>
    <p class="stats">clip {d:.0f}s</p>
    {f'<p class="dlg">{html.escape(dialogue)}</p>' if dialogue else ''}
    {prompt_html}
  </div>
</div>""")

page = f"""<!doctype html><meta charset="utf-8"><title>Walter's Deal — storyboard v1</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.45 -apple-system, sans-serif;
       max-width: 1060px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight: 600; }} h2 {{ margin-top: 40px; color: #9ad; }}
.shot {{ display:flex; gap:18px; margin:18px 0; padding:14px; background:#1d1d22;
         border-radius:10px; }}
video {{ border-radius:6px; flex-shrink:0; background:#000; }}
.meta h3 {{ margin:0 0 6px; font-size:16px; }}
.stats {{ color:#889; margin:2px 0 10px; font-size:13px; }}
.dlg {{ color:#ffd479; margin:6px 0; }}
.tag {{ font-size:11px; padding:2px 8px; border-radius:10px; vertical-align:middle;
        margin-left:8px; font-style:normal; }}
.tag.dialogue {{ background:#3a5f3a; }} .tag.visual {{ background:#3a4a5f; }}
details {{ margin-top:8px; }} summary {{ color:#7a8; cursor:pointer; font-size:13px; }}
.prompt {{ color:#9a9a8a; font-size:13px; background:#17171b; padding:10px;
           border-radius:6px; margin:6px 0; }}
.refs {{ color:#667; font-size:12px; }}
</style>
<h1>WALTER'S DEAL — first-pass storyboard (fast mode)</h1>
<p>Adapted from the novel by Philipp Lehner. {len(SHOTS)} shots, 480p fast draft.
Click any frame to play. Yellow = dialogue in the clip. Full prompts collapsed
under each shot.</p>
{''.join(rows)}
"""
(PROJ / "storyboard.html").write_text(page)
print(f"wrote walters_deal/storyboard.html ({len(SHOTS)} shots)")
