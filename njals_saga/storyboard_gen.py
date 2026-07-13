#!/usr/bin/env python3
"""Build njals_saga/storyboard.html: cast gallery + every shot in cut order with its
start frame (or playable clip once outputs/video1/<shot>.mp4 exists), dialogue, and
collapsed generation prompt. Rerun after any frame/clip change."""
import html
import re
import subprocess
from pathlib import Path

PROJ = Path(__file__).parent
ANCHORS = PROJ / "anchors"
FRAMES = PROJ / "frames"
V1 = PROJ / "outputs/video1"
THUMBS = PROJ / "storyboard_thumbs"
THUMBS.mkdir(exist_ok=True)

# (shot, target_seconds, title, dialogue)
SHOTS = [
    ("p1_thiefs_eyes", 12, "Cold open — thief's eyes",
     'HRUT: "Fair enough is this maid, and many will smart for it; but this I know not, whence thief\'s eyes have come into our race."'),
    ("p2_title", 6, "Title card", None),
    ("a1_wooing", 12, "The wooing at the Thing",
     'GUNNAR: "How wouldst thou answer were I to ask for thee?" HALLGERDA: "That can not be in thy mind." GUNNAR: "It is though."'),
    ("a2_warning", 12, "Njal takes it heavily",
     'NJAL: "From her will arise all kind of ill if she comes hither east." GUNNAR: "Never shall she spoil our friendship." NJAL: "Thou wilt have always to make atonement for her."'),
    ("a3_quarrel", 14, "The wives' feast-quarrel",
     'HALLGERDA: "Thou hast hangnails on every finger, and Njal is beardless." BERGTHORA: "But Thorwald, thy husband, was not beardless, and yet thou plottedst his death." GUNNAR: "Home I will go — never will I be egged on by thee like a fool."'),
    ("a4_purse", 12, "The travelling purse (feud montage)",
     'SKARPHEDINN (smiling): "Hallgerda does not let our house-carles die of old age."'),
    ("a5_slap", 12, "The slap",
     'GUNNAR: "Ill indeed is it if I am a partaker with thieves." HALLGERDA: "I will bear that slap in mind, and repay it if I can."'),
    ("a6_conditions", 14, "Njal's two conditions",
     'NJAL: "Never slay more than one man in the same stock, and never break the peace which good men make... else thou wilt have but a little while to live." GUNNAR: "Dost thou know what will be thine own death?" NJAL: "That which all would be the last to think."'),
    ("a7_ford", 10, "The bill sings — fight at the ford",
     'GUNNAR: "I would like to know whether I am by so much the less brisk and bold than other men, because I think more of killing men than they?"'),
    ("a8_outlawry", 8, "Outlawed",
     'GIZUR: "Gunnar shall fare abroad three winters — and if he does not fare, he may be slain."'),
    ("a9_fair_lithe", 12, "Fair is the Lithe",
     'GUNNAR: "Fair is the Lithe; so fair that it has never seemed to me so fair; the corn fields are white to harvest, and the home mead is mown; and now I will ride back home, and not fare abroad at all."'),
    ("a10_siege", 12, "The siege begins",
     'GUNNAR: "Thou hast been sorely treated, Sam, my fosterling..." THORGRIM (dying): "Find that out for yourselves; but this I am sure of — his bill is at home."'),
    ("a11_bowstring", 15, "Two locks of thy hair",
     'GUNNAR: "Give me two locks of thy hair... My life lies on it." HALLGERDA: "Then I call to thy mind that slap on the face which thou gavest me — and I care never a whit whether thou holdest out a long while or a short." GUNNAR: "Every one has something to boast of, and I will ask thee no more for this."'),
    ("a12_fall", 10, "The fall of Gunnar",
     'GIZUR: "We have now laid low to earth a mighty chief... and the fame of this defence of his shall last as long as men live in this land."'),
    ("b1_ice", 10, "The leap on the ice",
     'SKARPHEDINN: "I am tying my shoe." KARI: "This was done like a man." (He pockets Thrain\'s jaw-tooth — plant the prop.)'),
    ("b2_ring", 12, "The gold ring",
     'NJAL: "Knowest thou what brought thy father to his death?" BOY: "I know that Skarphedinn slew him; but we need not keep that in mind..." NJAL: "Better answered than asked — thou wilt live to be a good man and true."'),
    ("b3_one_law", 8, "One law for all the land",
     'THORGEIR THE LAWSPEAKER: "If there be a sundering of the laws, then there will be a sundering of the peace. This is the beginning of our laws: that all men shall be Christian here in the land."'),
    ("b4_deathbed", 10, "Valgard's poison",
     'VALGARD: "Set them by the ears by tale-bearing, so that Njal\'s sons may slay Hauskuld — and so Njal\'s sons will be slain in that quarrel."'),
    ("b5_slander", 14, "Mord's slander",
     'MORD: "They gave thee a horse... out of mockery at thee." HOSKULD: "Were it true, I would far rather suffer death at their hands than work them any harm."'),
    ("b6_cornfield", 12, "The sowing of corn",
     'SKARPHEDINN: "Don\'t try to turn on thy heel, Whiteness priest." HOSKULD: "God help me, and forgive you!"'),
    ("b7_grief", 14, "The sweetest light of my eyes",
     'NJAL: "Methinks it were better to have lost two of my sons, and that Hauskuld lived." SKARPHEDINN: "What will come after?" NJAL: "My death, and the death of my wife, and of all my sons."'),
    ("b8_cloak", 15, "The bloody cloak",
     'HILDIGUNNA: "I adjure thee, by all the might of thy Christ, and by thy manhood and bravery: take vengeance for all those wounds — or else be called every man\'s dastard." FLOSI: "Thou art the greatest hell-hag. Women\'s counsel is ever cruel."'),
    ("b9_silver", 15, "The settlement breaks",
     'FLOSI: "Thy father, the Beardless Carle? — many who look at him know not whether he is more a man than a woman." SKARPHEDINN (throwing the breeks): "Thou wilt have more need of these." FLOSI: "Go we now home — one fate shall befall us all."'),
    ("b10_oath", 8, "The oath in the Rift",
     'FLOSI: "We shall ride to Bergthorsknoll, and fall on Njal\'s sons with fire and sword, and not turn away before they are all dead."'),
    ("c1_supper", 12, "The last supper",
     'BERGTHORA: "This evening is the last that I shall set meat before my household." NJAL: "Methinks the gable wall is thrown down, and the whole board, and the meat on it, is one gore of blood."'),
    ("c2_indoors", 14, "Like a fox in his earth",
     'NJAL: "My will is that our men go indoors..." SKARPHEDINN: "I am unwilling to be stifled indoors like a fox in his earth. But I may well humour my father in this... for I am not afraid of my death." FLOSI: "Now are they all fey."'),
    ("c3_fire", 12, "Fire",
     'FLOSI: "...a deed which we shall have to answer for heavily before God, since we are Christian men. But still we must take to that counsel." SKARPHEDINN: "What, lads! Are ye lighting a fire, or are ye taking to cooking?"'),
    ("c4_refusal", 15, "I will not live in shame",
     'FLOSI: "I will offer thee, master Njal, leave to go out." NJAL: "I will not go out, for I am an old man, and little fitted to avenge my sons; but I will not live in shame." BERGTHORA: "I was given away to Njal young, and I have promised him this — that we would both share the same fate."'),
    ("c5_bed", 14, "Eager for rest",
     'THORD (the boy): "Methinks it is much better to die with thee and Njal than to live after you." NJAL: "We will go to our bed and lay us down; I have long been eager for rest."'),
    ("c6_beam", 10, "Kari's leap",
     'KARI: "This parting of ours will be in such wise that we shall never see one another more." SKARPHEDINN: "It joys me, brother-in-law, to think that if thou gettest away, thou wilt avenge me."'),
    ("c7_keepsake", 13, "A keepsake for thee",
     'GUNNAR LAMBI\'S SON: "Weepest thou now, Skarphedinn?" SKARPHEDINN: "Not so — the smoke makes one\'s eyes smart. But dost thou laugh?... Then here is a keepsake for thee." (Thrain\'s jaw-tooth.) FLOSI: "We shall have to boast of something else... there is no glory in that."'),
    ("c8_bright", 12, "The bright body",
     'ELDER: "Njal\'s body and visage seem to me so bright that I have never seen any dead man\'s body so bright as this."'),
    ("c9_vow", 8, "Kari's vow",
     'KARI: "Though all others take an atonement in their quarrels, yet will I take no atonement. My son is still unavenged — and I mean to take that on myself alone."'),
    ("d1_battle", 12, "Battle at the Althing", "(Thorhall lances the boil with Skarphedinn's spear; the law fails; the Thingfield erupts.)"),
    ("d2_peace", 10, "No price on my son",
     'HALL OF THE SIDE: "I will put no price on my son — and yet will come forward, and grant both pledges and peace to those who are my adversaries."'),
    ("d3_yule", 13, "The Yule feast",
     'GUNNAR LAMBI\'S SON: "...but the end of it was that he wept." KARI: "Many would say, Lord, that I have done this deed on your behalf." FLOSI: "Kari hath not done this without a cause; he only did what he had a right to do."'),
    ("d4_pilgrim", 8, "Rome (pilgrimage montage)", None),
    ("d5_kiss", 14, "The reconciliation",
     'FLOSI: "There are few men like Kari — and I would that my mind were shapen altogether like his."'),
    ("d6_ship", 12, "An old and death-doomed man",
     'FLOSI: "\'Tis quite good enough for an old and death-doomed man." (Of that ship no tidings were ever heard.)'),
    ("d7_endcard", 6, "End card", None),
]

CHAPTERS = {"p": "Prologue — The Prophecy", "a": "Act I — Gunnar and Hallgerda",
            "b": "Act II — The Foster-Son", "c": "Act III — The Burning",
            "d": "Epilogue — Vengeance and Peace"}

# (anchor, character, elevenlabs voice)
CAST = [
    ("njal", "NJAL — beardless lawyer-prophet", "Elderon (NwyAvGnfbFoNNEi4UuTq)"),
    ("bergthora", "BERGTHORA — his wife", "Alice (Xb7hH8MSUJpSbSDYk0k2)"),
    ("gunnar", "GUNNAR of Lithend", "Oyvind (nhvaqgRyAq6BmFs3WcdX)"),
    ("hallgerda", "HALLGERDA Long-hair", "Charlotte (rhS7yjXTU4uIlRxXhNW7)"),
    ("skarphedinn", "SKARPHEDINN — the grin", "Viking Bjorn (ljo9gAlSqKOvF6D8sOsX)"),
    ("kari", "KARI — the survivor", "CJ (9n6dGtreZHvmNb14Y1VO)"),
    ("flosi", "FLOSI — the burner", "Leif (tJDFCHyviItsYF1qqToS)"),
    ("hildigunna", "HILDIGUNNA — the whetter", "Lily (pFZP5JQG7iQjIQuC4Bku)"),
    ("mord", "MORD — the Iago", "Callum (N2lVS1w4EtoT3dr4eOWO)"),
    ("hoskuld_wp", "HOSKULD — the foster-son", "George (JBFqnCBsd6RMkjVDRZzb)"),
    ("gizur", "GIZUR the White", "Daniel (onwK4e9ZLuTAKqWW03F9)"),
    ("rannveig", "RANNVEIG — Gunnar's mother", "Nana Margaret (xIzR6egd3S3LJZbVW0c1)"),
    ("kolskegg", "KOLSKEGG — the brother", "Brian (nPczCjzI2devNBz1zQrb)"),
    ("gunnar_lambi", "GUNNAR LAMBI'S SON", "Harry (SOYHLrjzK2X1ezoPC6cr)"),
    ("loc_lithend", "Lithend (plate)", None),
    ("loc_bergthorsknoll", "Bergthorsknoll (plate)", None),
    ("loc_althing", "The Althing (plate)", None),
    ("loc_swinefell", "Swinefell hall (plate)", None),
]


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def load_prompts():
    """Parse img calls out of frames_v1.sh: name, prompt (with $S expanded), refs."""
    text = (PROJ / "frames_v1.sh").read_text()
    vars_ = dict(re.findall(r'^([A-Z][A-Z0-9]*)="(.*)"$', text, re.M))
    prompts = {}
    for m in re.finditer(r'^img (\S+) "(.*?)" ?(.*?)&?$', text, re.M | re.S):
        name, prompt, rest = m.groups()
        prompt = re.sub(r"\$\{?([A-Z][A-Z0-9]*)\}?", lambda v: vars_.get(v.group(1), ""), prompt)
        refs = [Path(r).name for r in re.findall(r"--image (\S+)", rest)]
        prompts[name] = (prompt.strip(), refs)
    return prompts


PROMPTS = load_prompts()

cast_cells = []
for anchor, label, voice in CAST:
    png = ANCHORS / f"{anchor}.png"
    imgtag = (f'<a href="anchors/{anchor}.png"><img src="anchors/{anchor}.png"></a>'
              if png.exists() else '<div class="missing">missing</div>')
    voice_s = f'<div class="voice">{html.escape(voice)}</div>' if voice else ""
    cast_cells.append(f'<div class="castcard">{imgtag}'
                      f'<div class="castname">{html.escape(label)}</div>{voice_s}</div>')

rows, chapter_seen = [], set()
n_frames = 0
for shot, target, title, dialogue in SHOTS:
    ch = shot[0]
    if CHAPTERS[ch] not in chapter_seen:
        chapter_seen.add(CHAPTERS[ch])
        rows.append(f'<h2>{html.escape(CHAPTERS[ch])}</h2>')
    prompt_html = ""
    key = f"f_{shot}"
    if key in PROMPTS:
        p, refs = PROMPTS[key]
        ref_s = f'<div class="refs">refs: {html.escape(", ".join(refs))}</div>' if refs else ""
        prompt_html = (f'<details><summary>generation prompt</summary>'
                       f'<p class="prompt">{html.escape(p)}</p>{ref_s}</details>')
    carried = "dialogue" if dialogue else "visual only"
    clip = V1 / f"{shot}.mp4"
    frame = FRAMES / f"{key}.png"
    if clip.exists():
        thumb = THUMBS / f"{shot}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1.5", "-i", str(clip),
                        "-frames:v", "1", "-vf", "scale=480:-1", str(thumb)], check=True)
        media = (f'<video controls preload="none" poster="storyboard_thumbs/{shot}.jpg" '
                 f'width="480"><source src="outputs/video1/{shot}.mp4" type="video/mp4"></video>')
        stats = f"clip {dur(clip):.0f}s (target {target}s)"
    elif frame.exists():
        media = f'<a href="frames/{key}.png"><img class="frame" src="frames/{key}.png" width="480"></a>'
        stats = f"start frame — target {target}s"
        n_frames += 1
    else:
        media = '<div class="missing frame480">frame missing</div>'
        stats = f"target {target}s"
    rows.append(f"""
<div class="shot">
  {media}
  <div class="meta">
    <h3>{shot} — {html.escape(title)}
        <span class="tag {carried.split()[0]}">{carried}</span></h3>
    <p class="stats">{stats}</p>
    {f'<p class="dlg">{html.escape(dialogue)}</p>' if dialogue else ''}
    {prompt_html}
  </div>
</div>""")

total = sum(t for _, t, _, _ in SHOTS)
page = f"""<!doctype html><meta charset="utf-8"><title>Burnt Njal — storyboard v1</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.45 -apple-system, sans-serif;
       max-width: 1060px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight: 600; }} h2 {{ margin-top: 40px; color: #9ad; }}
.shot {{ display:flex; gap:18px; margin:18px 0; padding:14px; background:#1d1d22;
         border-radius:10px; }}
video, img.frame {{ border-radius:6px; flex-shrink:0; background:#000; display:block; }}
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
.castgrid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
             gap:12px; margin:16px 0 8px; }}
.castcard img {{ width:100%; border-radius:6px; display:block; }}
.castname {{ font-size:12px; margin-top:4px; color:#ccd; }}
.voice {{ font-size:11px; color:#7a8; }}
.missing {{ color:#a66; background:#221a1a; border-radius:6px; padding:20px;
            text-align:center; font-size:13px; }}
.frame480 {{ width:480px; flex-shrink:0; align-self:stretch; display:flex;
             align-items:center; justify-content:center; }}
</style>
<h1>BURNT NJAL — storyboard v1 (frames)</h1>
<p><a href="casting.html" style="color:#9ad">voice casting auditions &rarr;</a> &nbsp;|&nbsp;
<a href="animatic_v1.mp4" style="color:#9ad">animatic v1 (frames + dialogue) &rarr;</a></p>
<p>From Njal's Saga, Dasent translation — all quoted dialogue verbatim. {len(SHOTS)} shots,
target ≈ {total // 60}:{total % 60:02d}. Frames are Nano Banana start frames; clips will
replace them as outputs/video1/&lt;shot&gt;.mp4 land. Yellow = lip-synced dialogue.
Full generation prompts collapsed under each shot. See STORYBOARD.md for the shot-by-shot
staging and SOURCE_NOTES.md for the dialogue bank.</p>
<h2>Cast &amp; plates</h2>
<div class="castgrid">{''.join(cast_cells)}</div>
{''.join(rows)}
"""
(PROJ / "storyboard.html").write_text(page)
print(f"wrote njals_saga/storyboard.html ({len(SHOTS)} shots, {n_frames} frames present)")
