#!/usr/bin/env python3
"""Build donner_party/storyboard.html: every shot in cut order with its start
frame, dialogue, and collapsed generation prompt. Frames-only version (no clips
yet) — once clips exist in outputs/video1/, they replace the frame images.
Rerun after any frame/clip change."""
import html
import re
import subprocess
from pathlib import Path

PROJ = Path(__file__).parent
FRAMES = PROJ / "frames"
V1 = PROJ / "outputs/video1"
THUMBS = PROJ / "storyboard_thumbs"
THUMBS.mkdir(exist_ok=True)

# (shot, title, dur, dialogue/beat)
SHOTS = [
    ("t_title", "TITLE: THE CUTOFF", 4, None),
    ("v0_letter", "Cold open — the letter", 8,
     'VO: "My dear cousin — I take this opportunity to write to you... and to tell you what trouble is."'),
    ("t_date1", "CARD: Springfield, April 1846", 3, None),
    ("a1_departure", "The Pioneer Palace rolls out", 8,
     'VO: "Papa built mama a wagon with a stove in it. Folks called it the Pioneer Palace."'),
    ("a2_prairie", "Everything new and pleasing", 8,
     'TAMSEN: "Everything is new and pleasing. I never could have believed we could travel so far with so little difficulty." GEORGE: "Write that down twice, Mrs. Donner."'),
    ("a3_warning", "Clyman's warning", 10,
     'CLYMAN: "Take the regular wagon track and never leave it. It is barely possible to get through if you follow it — and it may be impossible if you don\'t." REED: "There is a nearer route."'),
    ("a4_vote", "Donner for captain", 8,
     'MEN: "Donner! George Donner for captain!" TAMSEN: "We are leaving a known road on the word of a man none of us has ever met."'),
    ("a5_bridger", "Hastings is gone ahead", 6,
     'REED: "He will meet us at the mountains." (Note: "Gone ahead to guide you through. Follow my trail. — L.W. Hastings")'),
    ("b1_wasatch", "Two miles a day", 10,
     'STANTON: "Two miles. We made two miles today." VO: "It took us a month to cut a road no one will ever use again."'),
    ("b2_saltdesert", "The dry drive", 10,
     'VO: "Hastings wrote it was forty miles of dry drive. It was eighty. Five days and five nights without water."'),
    ("b3_cache", "Burying the Palace", 6, "(The Reeds cache their goods; Patty hides the doll.)"),
    ("b4_snyder", "Snyder", 10,
     "(The whip catches Margaret; the men grapple hidden by the oxen; Snyder falls.) — OFF-SCREEN strike, see content-safety notes"),
    ("b5_banish", "Banished", 10,
     'GRAVES: "He hangs, or he rides out alone." REED: "I\'ll come back for you with bread in both hands. Look after your mother."'),
    ("b6_hardkoop", "Hardkoop", 6,
     'KESEBERG: "The oxen cannot pull one pound more." VO: "We were becoming people we did not know."'),
    ("b7_stanton", "Stanton comes back", 8,
     'STANTON: "Bread from Captain Sutter! And these two men — Luis and Salvador — will guide us over!"'),
    ("c1_lake", "The wall", 8, 'BREEN: "One more dry week is all we ask."'),
    ("c2_pass", "One day too late", 10,
     'STANTON: "I reached the top! We cross tonight or not at all!" MOTHER: "The children cannot go another step."'),
    ("c3_cabins", "The lake camp", 8,
     'VO: "We built three cabins by the lake... Eighty-one of us, and the snow kept coming."'),
    ("c4_alder", "Alder Creek", 6, 'TAMSEN: "It mends, girls. It mends."'),
    ("c5_breen", "Breen's diary", 6,
     'BREEN: "Snowing fast... snow higher than the shanty. No living thing without wings can get about."'),
    ("c6_hides", "We ate the roofs", 8,
     'MARGARET: "And I will pay you double, in cattle, when we reach California." VO: "We ate the roofs."'),
    ("c7_burial", "First burial", 6, "(Baylis Williams. The omen cue, first use.)"),
    ("t_forlorn", "CARD: The Forlorn Hope", 3, None),
    ("d1_snowshoes", "Oxbows and rawhide", 8,
     'GRAVES: "Fifteen of us, on these. Six days\' rations." EDDY: "It\'s not enough." GRAVES: "It\'s what there is."'),
    ("d2_depart", "Seventeen against the white", 8,
     'VO: "Fifteen grown folks and two boys went for the settlements on snowshoes."'),
    ("d3_stanton_pipe", "I am coming soon", 8,
     'MARY: "Mr. Stanton — are you coming?" STANTON: "Yes. I am coming soon." — THE scene; protect it.'),
    ("d4_death_camp", "The camp of death", 10,
     'VO: "What was done in that camp to keep breath in the living, they did not speak of after — and no one who was not there may judge them." — NOTHING shown.'),
    ("d5_warning", "Go. Now.", 8,
     'EDDY: "Foster has begun to look at you when he talks of food. Go. Now. Don\'t keep to the trail."'),
    ("d6_ridge", "Two shots", 6,
     'VO: "The two men Sutter sent to save us were repaid the way desperate men repay." — audio-only, off-screen.'),
    ("d7_ranch", "Bread", 8, 'EDDY (barely audible): "Bread."'),
    ("e1_sutter", "Reed pleads", 6,
     'SUTTER: "No animal alive can cross before March." REED: "My family is up there. I will carry the flour on my own back."'),
    ("e2_relief1", "Men from California", 8,
     'MRS. MURPHY: "Are you men from California... or do you come from heaven?" — verbatim, keep.'),
    ("e3_patty", "Do the best you can", 8,
     'PATTY: "Well, Mother — if you never see me again, do the best you can."'),
    ("e4_reunion", "PAPA!", 8,
     'VIRGINIA: "PAPA!" VO: "I have not wrote you half of the trouble we\'ve had..."'),
    ("e5_doll", "Dolly wasn't scared", 6, 'PATTY: "Dolly wasn\'t scared, Papa."'),
    ("e6_tamsen", "Remember your mother", 10,
     'TAMSEN: "Remember your mother. Say it." GIRLS: "Remember your mother." (She walks back to the tent.)'),
    ("e7_keseberg", "The last man", 8,
     'FALLON: "Where is Mrs. Donner?" KESEBERG: "I often think the Almighty singled me out — to see how much a man can bear."'),
    ("e8_paradise", "Stepped over into paradise", 8,
     'VO: "I really thought I had stepped over into paradise."'),
    ("f1_letter_end", "Never take no cutoffs", 10,
     'VIRGINIA (to camera): "We have got through with our lives. But Cousin — never take no cutoffs. And hurry along as fast as you can."'),
    ("t_end", "CARD: 48 of 87", 6, None),
]

CHAPTERS = [
    ("t_title", "Cold open (May 1847)"),
    ("t_date1", "I — The Shortcut (spring–summer 1846)"),
    ("b1_wasatch", "II — The Desert (Sep–Oct)"),
    ("c1_lake", "III — The Mountain Closes (Nov–Dec)"),
    ("t_forlorn", "IV — The Forlorn Hope (Dec 16 – Jan 17)"),
    ("e1_sutter", "V — Relief (Feb–Apr 1847)"),
    ("f1_letter_end", "Epilogue"),
]
CH_AT = dict(CHAPTERS)


def load_prompts():
    """Parse img lines from anchors_v1.sh + frames_v1.sh (frame name -> prompt, refs)."""
    prompts = {}
    for sh in ["frames_v1.sh", "anchors_v1.sh"]:
        text = (PROJ / sh).read_text()
        vars_ = dict(re.findall(r'^([A-Z_]+)="(.*)"$', text, re.M))
        for m in re.finditer(r'^img (\S+) "(.*?)"((?: --\S+ \S+)*) *&?$', text, re.M | re.S):
            name, prompt, rest = m.groups()
            prompt = re.sub(r"\$\{?([A-Z_]+)\}?", lambda v: vars_.get(v.group(1), ""), prompt)
            refs = [Path(r).name for r in re.findall(r"--image (\S+)", rest)]
            prompts[name] = (prompt.strip(), refs)
    return prompts


PROMPTS = load_prompts()


def dur_of(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


rows, total = [], 0
for shot, title, dur, dialogue in SHOTS:
    if shot in CH_AT:
        rows.append(f"<h2>{html.escape(CH_AT[shot])}</h2>")
    total += dur
    fname = shot if shot.startswith("t_") else f"f_{shot}"
    # frame names in frames_v1.sh use a few short aliases
    alias = {"f_a5_bridger": "f_a5_bridger", "f_d3_stanton_pipe": "f_d3_stanton",
             "f_b7_stanton": "f_b7_stanton", "f_c5_breen": "f_c5_breen"}
    fname = alias.get(fname, fname)
    frame = FRAMES / f"{fname}.png"
    clip = V1 / f"{shot}.mp4"

    prompt_html = ""
    if fname in PROMPTS:
        p, refs = PROMPTS[fname]
        ref_s = f'<div class="refs">refs: {html.escape(", ".join(refs))}</div>' if refs else ""
        prompt_html = (f'<details><summary>frame prompt</summary>'
                       f'<p class="prompt">{html.escape(p)}</p>{ref_s}</details>')

    if clip.exists():
        thumb = THUMBS / f"{shot}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1.0", "-i", str(clip),
                        "-frames:v", "1", "-vf", "scale=480:-1", str(thumb)], check=True)
        media = (f'<video controls preload="none" poster="storyboard_thumbs/{shot}.jpg" '
                 f'width="480"><source src="outputs/video1/{shot}.mp4" type="video/mp4"></video>')
        stats = f"clip {dur_of(clip):.0f}s (planned {dur}s)"
    elif frame.exists():
        media = f'<img src="frames/{fname}.png" width="480" loading="lazy">'
        stats = f"start frame — planned {dur}s"
    else:
        media = '<div class="missing">frame not yet generated</div>'
        stats = f"planned {dur}s"

    carried = "dialogue" if dialogue else "visual only"
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

page = f"""<!doctype html><meta charset="utf-8"><title>The Cutoff — storyboard v1</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.45 -apple-system, sans-serif;
       max-width: 1060px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight: 600; }} h2 {{ margin-top: 40px; color: #9ad; }}
.shot {{ display:flex; gap:18px; margin:18px 0; padding:14px; background:#1d1d22;
         border-radius:10px; }}
img, video {{ border-radius:6px; flex-shrink:0; background:#000; align-self:flex-start; }}
.missing {{ width:480px; height:270px; flex-shrink:0; border-radius:6px; background:#26262c;
            color:#667; display:flex; align-items:center; justify-content:center;
            font-size:13px; }}
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
<h1>THE CUTOFF — Donner Party storyboard (first pass)</h1>
<p>{len(SHOTS)} shots incl. title cards, ~{total}s ({total/60:.1f} min) planned.
Historical drama, 1846–47, framed by Virginia Reed's real 1847 letter.
Yellow = dialogue/VO in the shot. Frame prompts collapsed under each shot.
Once clips exist in outputs/video1/ they replace the frames here.</p>
{''.join(rows)}
"""
(PROJ / "storyboard.html").write_text(page)
print(f"wrote donner_party/storyboard.html ({len(SHOTS)} shots, ~{total}s)")
