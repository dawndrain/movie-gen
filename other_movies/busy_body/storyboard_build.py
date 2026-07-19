#!/usr/bin/env python3
"""Build storyboard.html for THE BUSY BODY — every shot in order with its
start frame (or playable clip once outputs/<shot>.mp4 exists), dialogue, and
the frame's generation prompt collapsed underneath. Long Game format.

Usage: python3 storyboard_build.py [label]
Writes storyboard_<label>.html AND copies to storyboard.html.
"""
import html
import subprocess
import sys
from pathlib import Path

LABEL = sys.argv[1] if len(sys.argv) > 1 else "v1"
HERE = Path(__file__).parent
THUMBS = HERE / "storyboard_thumbs"

# frame prompts from make_images.py (single source of truth)
import importlib.util
spec = importlib.util.spec_from_file_location("mi", HERE / "make_images.py")
mi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mi)
FRAME_PROMPTS = {n: (p, r) for n, r, p in mi.F}
ANCHOR_PROMPTS = {n: (p, r) for n, a, p, r in mi.ANCHORS + mi.VARIANTS}

# (shot, frame, beat title, dialogue)  — frame may be shared across sub-shots
SHOTS = [
    ("p1", "p1", "Title",
     "(m_overture. The park, morning; an empty sedan chair waits.)"),
    ("p2", "p2", "Two loves, one mistress",
     'GEORGE: "I am in love with two women, Charles. One all wit, whose face I have '
     'never seen — and one all beauty, to whom I have never spoken." CHARLES: "Then '
     'between them, you have exactly one mistress. And my father keeps her under lock '
     'and key."'),
    ("p3", "p3", "Enter Marplot (plaster and all)",
     'CHARLES: "How came your beautiful countenance clouded in the wrong place?" '
     'MARPLOT: "I avoid fighting, purely to be serviceable to my friends."'),
    ("p4", "p4", "The letter to the husband (flashback gag)",
     'MARPLOT: "Pish, pox, that was an accident! I follow my instructions."'),
    ("p5", "p5", "Whisper whispers; Marplot combusts",
     'MARPLOT (aside): "A secret! I shall go stark mad if I am not let into this '
     'secret. I must and WILL follow him."'),
    ("p6", "p6", "The Incognito arrives",
     'MIRANDA: "Let the chair wait." PATCH: "The Spanish father has spoiled our plot — '
     'my lady shall be only Signior Babinetto\'s, he says." MIRANDA: "Let the tyrant '
     'man make what laws he will — a woman will find a way to break them."'),
    ("p7", "p7", "One hundred guineas for an hour",
     'GEORGE: "Will you take the fifty guineas?" FRANCIS: "Give me a hundred, sir, and '
     'try your fortune. He, he, he." MIRANDA (peeping, aside): "So — \'tis well it\'s '
     'no worse. I\'ll fit you both."'),
    ("p8", "p8", "Turn your back",
     'MIRANDA: "If you look upon me, I shall sink, even masked as I am. Turn your back '
     'while I confess." (He turns; she tiptoes off mid-sentence.) GEORGE: "Gone! '
     'Jilted! What woman can forgive a man that turns his back?"'),
    ("g1", "g1", "Gardee and Chargee",
     'MIRANDA: "Now methinks there\'s nobody handsomer than you — so neat, so clean, '
     'Gardee." FRANCIS: "Pretty rogue, pretty rogue! He, he, he." MIRANDA (aside, fan '
     'up): "Faugh — how he stinks of tobacco."'),
    ("g2", "g2", "Lady Wrinkle has but one eye",
     'CHARLES: "Why, she has but one eye." FRANCIS: "Then she\'ll see but half your '
     'extravagance, sir! Out of my doors, you dog!"'),
    ("g3a", "g3", "The Dumb Scene i — kissing is not in the articles",
     'FRANCIS: "Hold, hold! Kissing was not in our agreement — that\'s contrary to '
     'articles!" GEORGE: "Keep your distance, old gentleman."'),
    ("g3b", "g3", "The Dumb Scene ii — the sign language",
     'GEORGE: "A nod is yes, a shake is no. Can you prefer that old, dry, withered, '
     'sapless log of sixty-five to the vigorous, gay, sprightly love of twenty-four?" '
     '(She nods AND shakes AND sighs.) MIRANDA (aside): "How every action charms me."'),
    ("g3c", "g3", "The Dumb Scene iii — she has nicked you",
     'FRANCIS (counting guineas into her palm): "She has nicked you, Sir George! Ha, '
     'ha, ha!" GEORGE (at the door): "Marry her, old Beelzebub — and you\'ll be '
     'cuckolded. Remember that, and tremble."'),
    ("j1", "j1", "The balcony bust",
     'JEALOUS: "Why don\'t you write a bill upon your forehead, to show passengers '
     'there\'s something to be let! In, in — and lock her up till I come back from '
     '\'Change!" ISABINDA (aside): "Ay — to enjoy more freedom than he is aware of."'),
    ("j2", "j2", "Puppy-hunting",
     'JEALOUS: "Have you a letter or message for anybody in my house, sirrah?" '
     'WHISPER: "N-no, sir — I am seeking Trifle, sir — the very lap-dog my lady lost!" '
     'JEALOUS: "Let me catch you no more puppy-hunting about my doors!"'),
    ("j3", "j3", "The rope ladder",
     'CHARLES: "Fly with me now — I have raised a thousand pound." ISABINDA: "And love '
     'rarely dwells with poverty, Charles. Wait — my father cannot watch forever." '
     'PATCH (bursting in): "The master! Coming up the street!"'),
    ("j4", "j4", "Marplot bullies the wrong old man",
     'MARPLOT: "If that gentleman comes not as safe out of your house as he went in, I '
     'have half a dozen Myrmidons hard by!" JEALOUS: "Went IN? What, is he in then? '
     'Thieves! Thieves!" MARPLOT (fleeing in circles): "Murder! Murder!"'),
    ("j5", "j5", "Death from above",
     'MARPLOT: "Charles! Faith, I\'m glad to see thee safe out." CHARLES (collaring '
     'him): "It was YOU told him? Death — I could crush thee into atoms!" MARPLOT '
     '(choked): "Will you... choke me... for my KINDNESS?"'),
    ("g4", "g4", "The blunderbuss message",
     'MIRANDA: "Tell Sir George: if he dares to saunter by the garden gate on the '
     'left, about the hour of eight, he shall be saluted with a pistol or a '
     'blunderbuss." MIRANDA (aside): "I hope he understands my meaning better than to '
     'follow YOUR advice."'),
    ("t1", "t1", "The tavern decode",
     'MARPLOT (funereal): "You shall be saluted with a blunderbuss, sir. These were '
     'her very words." GEORGE (lighting up): "The garden gate — at eight — as I used '
     'to do! There must be a meaning in this! My dear Marplot, thou art my friend, my '
     'better angel!"'),
    ("j6", "j6", "The dropped letter",
     '(m_sneak. The cipher letter flutters from Patch\'s pocket.) JEALOUS (picking it '
     'up): "Humph — \'tis Hebrew, I think. This may be one of Love\'s hieroglyphics."'),
    ("j7", "j7", "The toothache charm",
     'PATCH: "My charm for the toothache! I have worn it these seven years — \'twas '
     'given me by an angel, sir, and must never be opened, on pain of dire vengeance." '
     'JEALOUS (grudging): "There, there — burn it, and I warrant you no vengeance '
     'will follow."'),
    ("j8", "j8", "The out-of-tune concert",
     'JEALOUS (banging the table): "Hey, hey! Why, you are a-top of the house, and you '
     'are down in the cellar! Play me a TUNE, or I\'ll break the spinet about your '
     'ears!" (Outside the window, Charles climbs.)'),
    ("j9", "j9", "A man in the closet",
     'JEALOUS: "Hell and Furies — a man in the closet!" PATCH: "A ghost, a ghost! This '
     'comes of opening the charm!" (Isabinda swoons flat across the closet door.)'),
    ("j10", "j10", "Personate the Spaniard",
     'CHARLES: "Here will I plant myself, and through my breast he shall make his '
     'passage." PATCH: "Softly, sir. What think you of PERSONATING this Spaniard — and '
     'marrying your mistress by her father\'s own consent? Nobody here has ever seen '
     'Don Diego." CHARLES: "My better genius!"'),
    ("g5", "g5", "The garden gate at eight",
     'SCENTWELL: "This way, sir — through many a dark passage and dirty step."'),
    ("g6", "g6", "The betrothal, interrupted",
     'MIRANDA: "My guardian has surrendered my fortune — he thinks he weds me in the '
     'morning. My emissaries are luring him to Epsom tonight." GEORGE: "Then tonight '
     'thou art mine." SCENTWELL: "Sir Francis, madam — at the door!"'),
    ("g7", "g7", "The monkey behind the chimney-board",
     'MIRANDA: "Hold, hold, dear Gardee! I have a — a — a MONKEY shut up there! '
     'Untamed! He\'ll break all my china!" MARPLOT: "A monkey! Let me but peep — oh, '
     'how I love the little miniatures of man!" FRANCIS: "Let my Chargee\'s monkey '
     'alone, or Bambo shall fly about your ears!"'),
    ("g8", "g8", "The monkey is a baronet",
     'MARPLOT (lifting the board): "Oh Lord, Oh Lord! Thieves! Thieves! Mur—" GEORGE '
     '(seizing him): "Damn ye, you unlucky dog — \'tis I!" MARPLOT (to the household, '
     'scratching his own face): "It flew over my shoulders — scratched all my face — '
     'broke yon china — and whisked out of the window!"'),
    ("g9", "g9", "Kidnapping the busybody",
     'MARPLOT: "I\'m as secret as a priest when I\'m trusted." GEORGE: "Why, \'tis '
     'with a priest our business is at present — and YOU, sir, come along with us '
     'where I can see you."'),
    ("g10", "g10", "Farewell, old Mammon — he's behind you",
     'FRANCIS: "Ah, my sweet Chargee — don\'t be frighted." MIRANDA (frozen, then '
     'sugar): "I\'m so surprised with JOY to see you, I know not what to say!" (To '
     'Scentwell, holding the necklace:) "Could you not have carried it to be MENDED, '
     'as I bid you?"'),
    ("g11", "g11", "Escorted to the wrong wedding",
     'MIRANDA: "If ever I marry, positively this is my wedding day." FRANCIS: "Adod, I '
     'am happier than the Great Mogul! The joyful bridegroom, I —" MIRANDA (aside): '
     '"— and I the happy bride."'),
    ("j11", "j11", "Don Diego arrives",
     '(m_spanish sting.) GEORGE: "Mr. Meanwell, sir, at your service — the Don speaks '
     'no English." JEALOUS (over the forged letter): "Meanwell is a very good name, '
     'and very significant! By St. Jago, my daughter weds tonight!" CHARLES (aside): '
     '"Yes, faith — if he knew all."'),
    ("j12", "j12", "Say we have brought it in commodities",
     'JEALOUS: "And the five thousand crowns, sir — paid down today?" GEORGE: "The '
     'crowns — but — but — but —" CHARLES (hissed): "Say we have brought it in '
     'COMMODITIES." GEORGE (instantly smooth): "— but of course: tobacco, sugars, '
     'spices, lemons — and so forth. My personal bond upon the rest."'),
    ("j13a", "j13", "The bride who won't look",
     'ISABINDA (kneeling, eyes shut): "Kill me, kill me instantly — \'twill be worse '
     'than death to wed him! My own hand shall cut the knot first!"'),
    ("j13b", "j13", "The whispered reveal",
     'GEORGE (low): "Suppose this Spaniard should be the very man to whom you\'d fly — '
     'those eyes that would not look on CHARLES." ISABINDA (blazing): "Where is he? '
     'Oh, let me fly into his arms!" GEORGE (through his teeth): "Take heed, madam. Be '
     'all obedience." ISABINDA (demure, to her father): "Sir... do with me what you '
     'please. I am all obedience."'),
    ("j14", "j14", "Marplot talks himself through the door",
     'MARPLOT: "Is there not a gentleman within, in a Spanish habit? ... Are you SURE '
     'he is a SPANISH gentleman? For \'tis an ENGLISH gentleman I want — though I '
     'suppose he may be DRESSED like a Spaniard." SERVANT (aside, holding the door '
     'wide): "Who knows but this may be an impostor... pray step in, sir."'),
    ("j15", "j15", "Sword at the parlor door",
     'JEALOUS: "STOP THE MARRIAGE!" GEORGE (blade out, back to the door): "Go on, Mr. '
     'Tackum! I guard this passage, old gentleman — I\'ll see \'em signed, or die '
     'for\'t!" SERVANT: "We are afraid of his SWORD, sir." MARPLOT (beaten instead): '
     '"Why — what do you beat ME for? I ha\'nt married your daughter!"'),
    ("j16", "j16", "Downright English",
     'JEALOUS: "Seize her!" CHARLES (hat off, plain English): "Rascals, retire — '
     'she\'s my WIFE. Touch her if you dare; I\'ll make dogs-meat of you." JEALOUS '
     '(staggering): "Ah! Downright ENGLISH! Oh, oh, oh!"'),
    ("j17", "j17", "The double reveal",
     'FRANCIS (trump card): "Rail on, gentlemen — this lady is my WIFE, do you see?" '
     'GEORGE: "Lawfully begotten by ME, sir." MIRANDA (handing Charles a parchment): '
     '"The writings of your uncle\'s estate, Charles — your due these three years." '
     'FRANCIS (storming out): "CONFOUND YOU ALL!"'),
    ("j18", "j18", "Forgiveness and fiddlers",
     '(m_wedding.) JEALOUS: "Seeing thou hast outwitted me — take her, and bless you '
     'both." MARPLOT: "Here\'s everybody happy, I find, but poor Pilgarlick — cuffed, '
     'kicked, and beaten in your service." GEORGE: "Thy estate is next, Marplot — '
     'I\'ll see old Gripe surrender it." MARPLOT: "THAT will make me as happy as any '
     'of you!"'),
    ("j19", "j19", "The moral (glass to camera)",
     'JEALOUS: "By my example let all parents move — and never strive to cross their '
     'children\'s love." (Freeze; m_overture reprise; black.)'),
]

ACTS = {"p": "ACT I — The Park", "g": "ACTS II–V — Gripe's house",
        "j": "ACTS II–V — Sir Jealous's house", "t": "ACT III — The Thatched House tavern"}
# order-of-appearance act headers, keyed off first occurrence
ACT_OF = {
    "p1": "ACT I — The Park (morning)",
    "g1": "ACT II — Gripe's parlor: the Dumb Scene",
    "j1": "ACT II–III — Sir Jealous's house: balcony and blunders",
    "g4": "ACT III — The coded blunderbuss",
    "j6": "ACT IV — The closet",
    "g5": "ACT IV — The chimney-board",
    "g10": "ACT V — Two weddings and a sword",
}


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def prompt_html(frame):
    if frame not in FRAME_PROMPTS:
        return ""
    prompt, refs = FRAME_PROMPTS[frame]
    ref_s = f'<div class="refs">refs: {html.escape(", ".join(refs))}</div>' if refs else ""
    return (f'<details><summary>frame prompt</summary>'
            f'<p class="prompt">{html.escape(prompt)}</p>{ref_s}</details>')


THUMBS.mkdir(exist_ok=True)
rows = []
for shot, frame, title, dialogue in SHOTS:
    if shot in ACT_OF:
        rows.append(f'<h2>{html.escape(ACT_OF[shot])}</h2>')
    clip = HERE / "outputs" / f"{shot}.mp4"
    frame_png = HERE / "frames" / f"{frame}.png"
    if clip.exists():
        thumb = THUMBS / f"{shot}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1.5", "-i", str(clip),
                        "-frames:v", "1", "-vf", "scale=480:-1", str(thumb)], check=True)
        d = dur(clip)
        media = (f'<video controls preload="none" poster="storyboard_thumbs/{shot}.jpg" '
                 f'width="480"><source src="outputs/{shot}.mp4" type="video/mp4"></video>')
        stat = f'<p class="stats">clip {d:.0f}s</p>'
    elif frame_png.exists():
        media = f'<img src="frames/{frame}.png" width="480" loading="lazy">'
        stat = '<p class="stats">start frame (clip not yet generated)</p>'
    else:
        media = '<div class="placeholder">frame rendering…</div>'
        stat = ''
    rows.append(f"""
<div class="shot">
  {media}
  <div class="meta">
    <h3>{shot} — {html.escape(title)}</h3>
    {stat}
    <p class="dlg">{html.escape(dialogue)}</p>
    {prompt_html(frame)}
  </div>
</div>""")

anchor_cells = []
for name in list(ANCHOR_PROMPTS):
    p = HERE / "anchors" / f"{name}.png"
    if p.exists():
        anchor_cells.append(f'<figure><img src="anchors/{name}.png" loading="lazy">'
                            f'<figcaption>{name}</figcaption></figure>')

page = f"""<!doctype html><meta charset="utf-8"><title>The Busy Body — storyboard</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.45 -apple-system, sans-serif;
       max-width: 1060px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight: 600; }} h2 {{ margin-top: 40px; color: #9ad; }}
.shot {{ display:flex; gap:18px; margin:18px 0; padding:14px; background:#1d1d22;
         border-radius:10px; }}
.shot img, .shot video {{ border-radius:6px; flex-shrink:0; background:#000;
                          max-height:280px; object-fit:contain; }}
.placeholder {{ width:480px; height:270px; flex-shrink:0; border-radius:6px;
                background:#111; color:#556; display:flex; align-items:center;
                justify-content:center; }}
.meta h3 {{ margin:0 0 6px; font-size:16px; }}
.stats {{ color:#889; margin:2px 0 10px; font-size:13px; }}
.dlg {{ color:#ffd479; margin:6px 0; }}
details {{ margin-top:8px; }} summary {{ color:#7a8; cursor:pointer; font-size:13px; }}
.prompt {{ color:#9a9a8a; font-size:13px; background:#17171b; padding:10px;
           border-radius:6px; margin:6px 0; }}
.refs {{ color:#667; font-size:12px; }}
.gallery {{ display:flex; flex-wrap:wrap; gap:10px; }}
.gallery figure {{ margin:0; }}
.gallery img {{ height:170px; border-radius:6px; }}
.gallery figcaption {{ color:#889; font-size:12px; text-align:center; }}
</style>
<h1>The Busy Body — storyboard ({LABEL})</h1>
<p>Susanna Centlivre, 1709. ~{len(SHOTS)} shots. Yellow = dialogue (verbatim from the
play, modernized spelling). Shots show their Nano Banana start frame until the Seedance
clip lands in outputs/&lt;shot&gt;.mp4 — re-run this script to swap clips in. Sub-shots
(g3a/b/c, j13a/b) share one start frame. Full production doc: treatment.md; voice
casting: voices.md.</p>
<details open><summary>cast &amp; location anchors ({len(anchor_cells)} rendered)</summary>
<div class="gallery">{''.join(anchor_cells)}</div></details>
{''.join(rows)}
"""
out = HERE / f"storyboard_{LABEL}.html"
out.write_text(page)
(HERE / "storyboard.html").write_text(page)
print(f"wrote {out.name} + storyboard.html ({len(SHOTS)} shots)")
