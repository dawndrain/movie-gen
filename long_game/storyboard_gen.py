#!/usr/bin/env python3
"""Build storyboard.html: every shot in cut order with playable clip, dialogue, VO.

Usage: python3 storyboard_gen.py [label]   (e.g. `python3 storyboard_gen.py v9`)
Writes storyboard_<label>.html AND copies it to storyboard.html (the latest).
Old versions stay on disk for side-by-side comparison.
"""
import sys
LABEL = sys.argv[1] if len(sys.argv) > 1 else "latest"
import html
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
THUMBS = ROOT / "storyboard_thumbs"

# import the narration lines from vo_gen
import importlib.util
spec = importlib.util.spec_from_file_location("vo_gen_data", ROOT / "vo_gen.py")


def load_vo_lines():
    src = (ROOT / "vo_gen.py").read_text()
    ns = {}
    block = src[src.index("LINES = ["): src.index("]\n", src.index("LINES = [")) + 1]
    exec(block, ns)
    return {shot: text for shot, _, text in ns["LINES"]}



VO = {}  # comedy cut: no narration — dialogue carries everything

V3 = "outputs/video3"
# (shot, clip, beat title, dialogue)
SHOTS = [
    ("t0", "outputs/video14/t0_longgame.mp4", "Cold open (music grows underneath)",
     'CASS (O.S.): "The Long Game. One credit... one life. ...Huh."'),
    ("a6", "outputs/video6/a6_sign2.mp4", "The signs mean nothing [reverted to v6 take]",
     'CASS: "It says out of order."  MILO (ripping it off): "It doesn\'t mean anything."  CASS: "That one says security warning."  (Milo sticks it on '
     'Deshawn. Deshawn wears it proudly.)'),
    ("a7", f"{V3}/a7_dibs.mp4", "Dibs",
     'DESHAWN: "I want to go first."  MILO: "You should be a rapper. Or a DJ."  '
     'CASS: "You could be a basketball player. Go pro."  DESHAWN: "Nah. I want to be an '
     'alpine skier. Light me up."  (Hard cut to white.)'),
    ("a_ski", "outputs/video8/a_ski3.mp4", "Ninety seconds later (inside the game)",
     "(The skier wins... and the helmet comes off a sandy-haired white guy. Blonde wife, two blond sons. No dialogue.)"),
    ("a8", "outputs/video9/a8_out3.mp4", "Ninety seconds later",
     'DESHAWN: "That was INCREDIBLE. I won gold! I had a WIFE. Two kids — Braden and '
     'Tucker! ...Man, I miss them."  MILO: "You were in for ninety seconds."  '
     'DESHAWN: "It was a whole LIFE, bro. And it was SO easy."'),
    ("a_hard", "outputs/video12/a_hard_fix.mp4", "Hard mode → have a nice life (dubbed 'Cass' kept)",
     'CASS: "Easy is boring. Put me on hard mode."  DESHAWN: "Ohhh — Cass wants the '
     'SMOKE!"  MILO (cranking the dial): "Have a nice life."  (Cass, eyes covered, '
     'raises one lazy middle finger. White.)'),
    ("b1", "outputs/video11/b1_wake5.mp4", "Day Zero (respawn frame, mom voice ref)",
     'MOM (O.S.): "Bren?... Bren! Isa has the flux again. You need to go fetch more '
     'water. More\'s coming out of her than\'s going in, at this point."'),
    ("b2", "outputs/video2/2_2_water_carry.mp4", "Water chore [reused]", None),
    ("b3", f"{V3}/b3_goat.mp4", "The goat is not moving", None),
    ("b5", "outputs/video6/b5_afterlife2.mp4", "First death",
     'MOM: "Hush now. Things will be better for you in the afterlife."'),
    ("b6", "outputs/video12/b6_fix.mp4", "The remembering (v6 scream transplanted)",
     'MOM: "What\'s wrong, Bren?!"'),
    ("b7", "outputs/video14/b7_name3_bronze.mp4", "My name is Cass (histogram-matched to bronze palette)",
     'CASS: "My name is Cass. My name is Cass."  MOM: "...Well. Isa has the flux. So '
     'you\'re going to need to go fetch more water."'),
    ("b8", "outputs/video14/b8_leave2.mp4", "Tech support (retake: pan follows the point to the old woman)",
     'CASS: "How do I get out of here? I was playing this game — The Long Game — at the '
     'arcade? Now how do I get out?"  VILLAGER: "...Go talk to her. If you\'re going to '
     'be acting so crazy."'),
    ("b9", "outputs/video/2_5_touched_woman.mp4", "Forty summers [reused, reverted]",
     'TOUCHED WOMAN: "Then you\'ll have to live it. All of it. Forty summers, child."'),
    ("b10", f"{V3}/b10_forty.mp4", "FORTY?! [reverted]",
     'CASS: "Forty?! I have to live to FORTY?!"'),
    ("b12", f"{V3}/b12_cough.mp4", "The cough (same cough before every death)", None),
    ("w1", "outputs/video10/w1d.mp4", "Respawn #2 ('...Again.' child voice, reverted)",
     'MOM (O.S.): "Bren! Water!"  CASS: "...Again."'),
    ("b13", "outputs/video6/b13_cry2.mp4", "This time he cries a little", None),
    ("b14", f"{V3}/b14_three_lives.mp4", "Three lives?",
     'CASS: "Do I have, like, three lives or something? Die three times — and then '
     'I\'m out?"'),
    ("w2", "outputs/video10/w2d.mp4", "Respawn #3 (playing dead, same frame)",
     'MOM (O.S.): "I can see you breathing."'),
    ("b15", f"{V3}/b15_five_lives.mp4", "Maybe five lives",
     'CASS: "...Maybe five lives."'),
    ("w3", "outputs/video10/w3d.mp4", "Respawn #4 (same frame — then the yoke drops in)",
     'MOM (O.S.): "Water."  (Yoke drops into frame. Wheeze.)'),
    ("b16", "outputs/video6/b16_cure3.mp4", "Fine. FINE. (mom standing over him)",
     'CASS: "The flux, yeah? I\'ll get you a cure for the flux."  MOM: "...Well. '
     'Good, then."'),
    ("b17", f"{V3}/b17_rant.mp4", "The war plan (middle trimmed in the cut)",
     'CASS: "I need to boil water. I need a fire. I need electrolytes — sugar and salt. '
     'Honey and salt. I am NOT gonna die with diarrhea coming out my ass."'),
    ("b18", f"{V3}/b18_germs.mp4", "Killing the germs",
     'KIDS: "What are you doing?"  CASS: "I\'m killing the germs."  KIDS: "...What?"  '
     'CASS: "There are little spirits in the water, okay? And you need to send them '
     'away. Like this."'),
    ("b19", "outputs/video7/b19_isa.mp4", "Isa is saved",
     'CASS: "Salt. Honey. Clean water — boiled first. Keep giving it, however fast it '
     'runs through her."'),
    ("b20", "outputs/video5/b20_solemn2.mp4", "The gesture graduates (he stays sarcastic)", None),
    ("b21", "outputs/video8/b21_party3.mp4", "The good years",
     'ELDER: "To Cass!"  HALL: "TO CASS!"  CASS (quietly): "Took twenty years."'),
    ("b22", "outputs/video7/b22_wish3.mp4", "The wish (locked-off camera)",
     'CASS: "I just wish I could take a bath, you know? Go back to the arcade. See my '
     'friends again. My family. ...Have some ice cream."'),
    ("b23", "outputs/video5/b23_finally2.mp4", "The gut-punch",
     'CASS: "It\'s finally over? I\'m finally through?"  TOUCHED WOMAN: "Yes, child. '
     'Your next life will begin."  CASS: "My NEXT life?!"'),
    ("r1", "outputs/video6/r1_sigh.mp4", "Roman wake (just the sigh)", None),
    ("r2", "outputs/video7/r2_aq3.mp4", "The aqueduct (another sigh, roman tunic)", None),
    ("r3", f"{V3}/r3_gesture_q.mp4", "That gesture",
     'CASS: "That gesture — why are you doing that gesture?"  WOMAN: "I\'m cleansing '
     'the water. It removes the bad spirits."  CASS: "Who TAUGHT you that?"  WOMAN: '
     '"What do you mean, who taught me? I know how to cleanse water."'),
    ("r4", "outputs/video9/r4_boil3.mp4", "You need to BOIL it (continues from r3's last frame)",
     'CASS: "You need to boil it first. You can\'t just do the hand thing — you need '
     'to BOIL it first."  WOMAN: "Why would I boil water?"'),
    ("r5", "outputs/video5/r5_library2.mp4", "The librarian points",
     'CASS: "Where is your section on the GREAT Bronze Age kings? The... legendary ones."'),
    ("r6", f"{V3}/r6_scroll.mp4", "C\'Ass",
     'SCROLL: "C\'ASS — a clever but foolish person; named for a bronze-age king who '
     'spoke often of nonsensical things no one cared to understand. Also: ASS."  '
     'CASS: "...I need to take a bath."'),
    ("r7", f"{V3}/r7_bath_pitch.mp4", "The pitch",
     'CASS: "If I\'m going to do another time jump, I need to write all of it down... '
     'And I\'ll pay you to write it all down for me."  TERTIUS: "Paid? I can write."'),
    ("r8", "outputs/video13/r8_glass2.mp4", "Better glass (he has no idea how)",
     'CASS: "First — we\'re going to need better glass."  '
     'TERTIUS: "That is the finest glass in the city."  CASS: "...How do you MAKE glass, exactly?"'),
    ("r9", "outputs/video13/r9_acid3.mp4", "Dictation, day one (reverted to v13 take)",
     'CASS: "Take this down, Tertius. Sulfuric acid. It reacts with... nearly everything. '
     'Metals. Sugar. I want to say... salts? It is also highly corrosive, and will damage your skin."'),
    ("r10", f"{V3}/r10_page.mp4", "The page (with doodles)", None),
    ("r11", f"{V3}/r11_dictate_blood.mp4", "Dictation, day two",
     'CASS: "The heart is a pump. The blood moves in a circle."  TERTIUS: "...blood... '
     'is... important."  CASS: "Close enough."'),
    ("r12", "outputs/video7/r12_salt4.mp4", "The one he keeps",
     'CASS: "Salt, added to ice, lowers its melting point."  TERTIUS: "What\'s that '
     'one?"  (Cass just smiles.)'),
    ("r13", "outputs/video7/r13_sweet3.mp4", "Pretty sweet",
     'CASS: "Things are going to be pretty sweet in the next life."'),
    ("n1", "outputs/video19/n1_bridge2.mp4", "Fifty, and a spotless record (v19 line retake)",
     'CASS: "Fifty years old. Ten till the gate. And I have not died since the '
     'BRONZE AGE. This should be easy."'),
    ("n2", "outputs/video4/n2_widow.mp4", "The widow clocks him in",
     'WIDOW: "Sixty, this time, child."  CASS: "Sixty. Got it. Thank you."'),
    ("e1", f"{V3}/e1_library2.mp4", "The librarian points, again",
     'CASS: "Where is your section on the greatest writers of antiquity?"'),
    ("e2", f"{V3}/e2_fire.mp4", "The fire",
     'CHRONICLE: "...All that survived: three cookery scrolls, one tax ledger, and '
     'several sketches by a scribe named Tertius."  CASS: "...a scribe named TERTIUS?"'),
    ("n4", "outputs/video4/n4_fireflash.mp4", "The fire itself (flash cut, spliced into e2)", None),
    ("e3", f"{V3}/e3_flood.mp4", "The vow (plays dry; music enters at n5)",
     'CASS: "Alright then. I will FLOOD the world with knowledge."'),
    ("n5", "outputs/video19/n5_type2.mp4", "The tool that makes the tool (v19 line retake)",
     'APPRENTICE: "A thousand little letters... why?"  CASS: "Because last time, '
     'everything I knew existed in ONE copy. In ONE building. Which caught ONE fire."'),
    ("e4", f"{V3}/e4_montage.mp4", "The flood", None),
    ("n6", "outputs/video4/n6_boiler.mp4", "I can HEAR the pressure",
     'APPRENTICE: "Master... shouldn\'t there be some kind of gauge?"  CASS: "I '
     'invented this thing. I can HEAR the pressure. ...That\'s fine."  (BOOM.)'),
    ("n7", "outputs/video4/n7_again.mp4", "Back at fifty",
     'CASS: "The press. The type. The pamphlets. Ten years. All of it. Again."  '
     '(Screams into the river.)'),
    ("n8", "outputs/video4/n8_gauge.mp4", "Gauge first",
     'CASS: "Gauge first. Valve second. THEN the fire. ...Okay."'),
    ("n9", "outputs/video13/n9_sixty3.mp4", "Sixty (Cass and the widow both in frame)", None),
    ("m1", "outputs/video5/m1_wake2.mp4", "1926 (he wakes at 60 now)",
     'CASS: "Electric light. Oh, we are CLOSE to home."'),
    ("m2", "outputs/video5/m2_tram2.mp4", "Colleagues", None),
    ("m3", "outputs/video12/m3_fix.mp4", "Not a speedrun (British redub)",
     'CASS: "Gate\'s at eighty. So... twenty years. That\'s not a speedrun. That\'s '
     'just... a life. Huh."'),
    ("m4", "outputs/video4/m4_teach.mp4", "The count is the boss",
     'CASS: "You don\'t argue about whose guess is prettier. You TEST it. Change one '
     'thing. Count what happens. The count is the boss — not you, not me."  BOY: "Even '
     'you, sir?"  CASS: "ESPECIALLY me."'),
    ("m5", "outputs/video7/m5_feet2.mp4", "Iris (warmer)",
     'IRIS: "Feet. Honestly. Where were you raised — a mud hut?"  CASS: "...Yes, '
     'actually."  IRIS: "Then wipe like it."'),
    ("m6", "outputs/video4/m6_longtime.mp4", "A long time (played straight)",
     'CASS: "I feel like I\'ve lived a long time."  IRIS: "Everyone our age feels '
     'that."  CASS: "No. I mean... a LONG time."  IRIS: "I know you do, love. Come '
     'to bed."'),
    ("m7", "outputs/video4/m7_obit.mp4", "Four plain lines",
     'CASS (whisper): "Beloved wife of—"'),
    ("p1", "outputs/video11/p1_dinner2.mp4", "Peter's news (warm open; the music cuts at the pitch)",
     'PETER: "It\'s a booth you SIT in, uncle — you live a whole LIFE in an hour! They '
     'haven\'t even named it yet!"  PETER: "Uncle? You alright?"  CASS: "Wonderful."'),
    ("p2", "outputs/video14/p2_board4.mp4", "The naming (one Cass only)",
     'PETER: "And we\'re calling it... The Long Game."  PETER: "Good, right?"  '
     'CASS: "Catchy."'),
    ("p3", "outputs/video12/p3_fix.mp4", "The documentation ('overrides' redubbed)",
     'CASS: "Age gates... save-point logic... exit conditions... Tester overrides. '
     'There\'s a DOOR?! There was a DOOR the WHOLE TIME?!"  PETER (O.S.): "Uncle?"  '
     'CASS: "Marvelous craftsmanship, Peter."'),
    ("p4", "outputs/video19/p4_exit4.mp4", "The staff door (v19 retake: well-kept room)",
     'CASS: "Five lifetimes. Every chore, every gate... and I am leaving through the '
     'staff door."  (He performs the sequence. White.)'),
    ("q1", "outputs/video5/q1_off2.mp4", "Over four minutes",
     'DESHAWN: "—bro, you were in there for OVER four minutes! The thing was flashing '
     'the WHOLE time, someone went for a manager—"  CASS: "...Over four minutes."'),
    ("q2", "outputs/video12/q2_fix.mp4", "I lived a long time (reverted to dubbed take)",
     'MILO: "What did you DO in there? Nobody plays maxed out!"  CASS: "I lived a '
     'long time."  (They crack up. He doesn\'t.)'),
    ("q3", "outputs/video16/q3_walk2.mp4", "Too clean, too easy (on-model retake, forward walk)",
     'DESHAWN (distant): "Bro\'s still IN there!"'),
    ("q4", "outputs/video6/q4_real2.mp4", "The code (attempt one)",
     'CASS: "Is any of it even real?"'),
    ("q5", "outputs/video4/q5_nested.mp4", "NESTED SESSION DETECTED",
     'DESHAWN: "On EASY! We put him in on EASY — and this GENIUS found the arcade '
     'INSIDE the game and got stuck a whole level DOWN!"'),
    ("q6", "outputs/video4/q6_longtime2.mp4", "Even funnier the second time",
     'MILO: "How — how was it?"  CASS: "I lived a long time."  (The arcade explodes.)'),
    ("q7", "outputs/video6/q7_fail2.mp4",
     "The code (attempts two and three) — now plays FULL: both fails + the ceiling stare", None),
    ("q7b", "outputs/video19/q7b_consider.mp4",
     "Considering attempt four (NEW in v19; chained from q7's last frame)",
     'CASS: "Maybe I\'m home. ...Maybe I\'m five levels deep."  (He raises his hands '
     'into the sequence — and holds.)'),
    ("q8", "outputs/video7/q8_come3.mp4", "The knock answers it (back in the cut in v19)",
     'DESHAWN (through door): "Yo! We\'re going out. You coming, or you gonna sit in '
     'the dark being weird about the arcade thing all night?"  CASS: "Yeah. Yeah. '
     'I\'m coming."'),
    ("q_credits", "outputs/credits.mp4",
     "Fade to black -> amber CRT credits (hum + ominous arcade cue)", None),
]

CHAPTERS = {"t": "I — The Arcade (2044)", "a": "I — The Arcade (2044)", "b": "II — Bronze (Day Zero and the reign)", "w": "II — Bronze (Day Zero and the reign)",
            "r": "III — Roman",
            "n": "IV — Renaissance (the press, and the boiler)",
            "e": "IV — Renaissance (the press, and the boiler)",
            "m": "V — 1926 (the last era)",
            "p": "VI — The Machine Documented",
            "q": "VII — The Arcade, Again"}


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())



def load_prompts():
    """Parse gen calls from the two batch scripts: name -> (prompt, refs)."""
    import re
    prompts = {}
    for script in ("videos_ch1-4.sh", "videos_v2.sh", "videos_v3.sh", "videos_v4.sh",
                   "videos_v5.sh", "videos_v19.sh"):
        path = ROOT / script
        if not path.exists():
            path = ROOT / "archive" / script  # older batches were archived
        text = path.read_text()
        vars_ = dict(re.findall(r'^([A-Z]+)="(.*)"$', text, re.M))
        for m in re.finditer(r'^gen (\S+) (\d+) "(.*?)" (.*?)&?$', text, re.M):
            name, _, prompt, rest = m.groups()
            prompt = re.sub(r"\$\{?([A-Z]+)\}?", lambda v: vars_.get(v.group(1), ""), prompt)
            refs = [Path(r).name for r in re.findall(r"--(?:start-image|image|video) (\S+)", rest)]
            prompts[name] = (prompt.strip(), refs)
    # 3_5 was resubmitted with reworded prompt ("serving woman") after a rejection
    if "3_5_slave_nod" in prompts:
        p, r = prompts["3_5_slave_nod"]
        prompts["3_5_slave_nod"] = (p.replace("old slave woman", "old serving woman"), r)
    return prompts


PROMPTS = load_prompts()

W_BLOCK = "Wardrobe and character lock:"
N_BLOCK = "Photorealistic, natural human motion"


def prompt_html(clip):
    key = Path(clip).stem
    if key not in PROMPTS:
        return ""
    prompt, refs = PROMPTS[key]
    # collapse the repeated boilerplate blocks into chips
    import re as _re
    i = prompt.find(W_BLOCK)
    if i > -1:
        j = prompt.find(N_BLOCK)
        prompt = prompt[:i].rstrip() + " [wardrobe lock] " + (prompt[j:] if j > -1 else "")
    i = prompt.find(N_BLOCK)
    if i > -1:
        prompt = prompt[:i].rstrip() + " [global negative block]"
    ref_s = f'<div class="refs">refs: {html.escape(", ".join(refs))}</div>' if refs else ""
    return (f'<details><summary>generation prompt</summary>'
            f'<p class="prompt">{html.escape(prompt)}</p>{ref_s}</details>')

THUMBS.mkdir(exist_ok=True)
rows, chapter_seen = [], set()
for shot, clip, title, dialogue in SHOTS:
    ch = shot[0]
    if CHAPTERS[ch] not in chapter_seen:
        chapter_seen.add(CHAPTERS[ch])
        rows.append(f'<h2>{html.escape(CHAPTERS[ch])}</h2>')
    if not (ROOT / clip).exists():
        rows.append(f'<div class="shot"><div class="meta"><h3>{shot.replace("_", ".")} — '
                    f'{html.escape(title)} <span class="tag visual">rendering…</span></h3>'
                    f'{f"<p class=dlg>{html.escape(dialogue)}</p>" if dialogue else ""}'
                    f'{prompt_html(clip)}</div></div>')
        continue
    thumb = THUMBS / f"{shot}.jpg"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1.5", "-i", str(ROOT / clip),
                    "-frames:v", "1", "-vf", "scale=480:-1", str(thumb)], check=True)
    vo = VO.get(shot)
    d = dur(ROOT / clip)
    vo_d = dur(ROOT / f"vo/{shot}.mp3") if vo else 0
    if dialogue and vo:
        carried = "dialogue + VO"
    elif dialogue:
        carried = "dialogue"
    elif vo:
        carried = "VO only"
    else:
        carried = "visual only"
    over = f' &nbsp;<span class="warn">VO overruns clip by {vo_d - d:.0f}s</span>' if vo_d > d + 1 else ""
    rows.append(f"""
<div class="shot">
  <video controls preload="none" poster="storyboard_thumbs/{shot}.jpg" width="480">
    <source src="{clip}" type="video/mp4"></video>
  <div class="meta">
    <h3>{shot.replace('_', '.')} — {html.escape(title)}
        <span class="tag {carried.split()[0].replace('+','')}">{carried}</span></h3>
    <p class="stats">clip {d:.0f}s{f' · VO {vo_d:.0f}s' if vo else ''}{over}</p>
    {f'<p class="dlg">{html.escape(dialogue)}</p>' if dialogue else ''}
    {f'<p class="vo"><b>NARRATOR:</b> {html.escape(vo)}</p>' if vo else ''}
    {prompt_html(clip)}
  </div>
</div>""")

page = f"""<!doctype html><meta charset="utf-8"><title>The Long Game — storyboard</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.45 -apple-system, sans-serif;
       max-width: 1060px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight: 600; }} h2 {{ margin-top: 40px; color: #9ad; }}
.shot {{ display:flex; gap:18px; margin:18px 0; padding:14px; background:#1d1d22;
         border-radius:10px; }}
video {{ border-radius:6px; flex-shrink:0; background:#000; }}
.meta h3 {{ margin:0 0 6px; font-size:16px; }}
.stats {{ color:#889; margin:2px 0 10px; font-size:13px; }}
.warn {{ color:#e6a23c; }}
.dlg {{ color:#ffd479; margin:6px 0; }}
.vo {{ color:#aab4c8; font-style:italic; margin:6px 0; }}
.tag {{ font-size:11px; padding:2px 8px; border-radius:10px; vertical-align:middle;
        margin-left:8px; font-style:normal; }}
.tag.dialogue {{ background:#3a5f3a; }} .tag.VO {{ background:#5f3a3a; }}
.tag.visual {{ background:#3a4a5f; }}
details {{ margin-top:8px; }}
.score {{ background:#1d1d22; padding:12px; border-radius:10px; margin:14px 0; }}
.cue {{ margin:10px 0; color:#cfd3da; font-size:14px; }}
.cue audio {{ width: 420px; height: 30px; margin-top:4px; }} summary {{ color:#7a8; cursor:pointer; font-size:13px; }}
.prompt {{ color:#9a9a8a; font-size:13px; background:#17171b; padding:10px;
           border-radius:6px; margin:6px 0; }}
.refs {{ color:#667; font-size:12px; }}
</style>
<h1>The Long Game — COMEDY CUT storyboard ({LABEL}) — v19 ending: attempts fail in full, he weighs one more, the knock answers it, credits</h1>
<details class="score"><summary>The score — click to listen to each cue</summary>
<div class="cue"><b>omen</b> (cold open, crescendo · the "next life" gut-punch · before the first code attempt)<br><audio controls preload="none" src="music/mus_omen.m4a"></audio></div>
<div class="cue"><b>arcade ambience</b> (under the arcade scenes, very low)<br><audio controls preload="none" src="music/mus_arcade2.m4a"></audio></div>
<div class="cue"><b>bronze folk</b> (chores montage only)<br><audio controls preload="none" src="music/mus_bronze.m4a"></audio></div>
<div class="cue"><b>renaissance harpsichord</b> (arrival · the flood montage)<br><audio controls preload="none" src="music/mus_ren.m4a"></audio></div>
<div class="cue"><b>boiler brass</b> (the boiler only)<br><audio controls preload="none" src="music/mus_boiler.m4a"></audio></div>
<div class="cue"><b>1926 piano/strings</b> (widow's nod through all of 1926)<br><audio controls preload="none" src="music/mus_1926.m4a"></audio></div>
<div class="cue"><b>machine clockwork</b> (the Peter act)<br><audio controls preload="none" src="music/mus_machine.m4a"></audio></div>
<div class="cue"><b>end reprise</b> (failed code + the door)<br><audio controls preload="none" src="music/mus_end.m4a"></audio></div>
</details>
<details class="score"><summary>Ambience beds (new in v18) — steady scene textures, mixed at 0.035–0.055 under everything</summary>
<div class="cue"><b>arcade room tone</b> (a6→ski · post-ski→bronze · the return, q1→q3) — hum, idle cabinet bleeps<br><audio controls preload="none" src="ambience/amb_arcade_loop.m4a"></audio></div>
<div class="cue"><b>bronze village</b> (the whole bronze act) — wind, distant goats, fire crackle<br><audio controls preload="none" src="ambience/amb_bronze_loop.m4a"></audio></div>
<div class="cue"><b>roman street</b> (r1→library) — crowd murmur, fountain, footsteps<br><audio controls preload="none" src="ambience/amb_roman_city_loop.m4a"></audio></div>
<div class="cue"><b>stone library</b> (library scenes) — cavernous quiet, parchment<br><audio controls preload="none" src="ambience/amb_library_loop.m4a"></audio></div>
<div class="cue"><b>the baths</b> (bath pitch) — lapping water, echoing drips (loudest bed, 0.055)<br><audio controls preload="none" src="ambience/amb_baths_loop.m4a"></audio></div>
<div class="cue"><b>workshop</b> (glass → dictation) — furnace, steam hiss, bubbling retorts (0.055)<br><audio controls preload="none" src="ambience/amb_workshop_loop.m4a"></audio></div>
<div class="cue"><b>renaissance river town</b> (bridge → library) — river, waterwheel, gulls<br><audio controls preload="none" src="ambience/amb_ren_city_loop.m4a"></audio></div>
<div class="cue"><b>1926 town</b> (wake → the dinner) — distant motorcar, tram bell, street murmur<br><audio controls preload="none" src="ambience/amb_1926_loop.m4a"></audio></div>
<p class="stats">Mix levels in the film are 0.07–0.20 of these — everything not listed plays with no score.</p>
</details>
<p>Click any frame to play the clip. Yellow = the dialogue in the clip. No narration in
this cut — dialogue carries everything. [reused] = a clip kept from the earlier serious
draft. The b6 wake repeats as the respawn beat in the assembled cut; the n4 fire flash
is spliced into the middle of e2. Each shot's generation prompt is collapsed underneath
([wardrobe lock] / [global negative block] stand in for repeated boilerplate; full text
in videos_v3.sh / videos_v4.sh).</p>
{''.join(rows)}
"""
out = ROOT / f"storyboard_{LABEL}.html"
out.write_text(page)
(ROOT / "storyboard.html").write_text(page)
print(f"wrote {out.name} + storyboard.html ({len(SHOTS)} shots)")
