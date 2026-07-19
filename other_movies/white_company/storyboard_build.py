#!/usr/bin/env python3
"""Build white_company/storyboard.html: illustrated storyboard — every shot in cut
order with its Nano Banana frame, dialogue, and collapsed generation prompt.
Rerun after regenerating any image (and later, swap frames for clips)."""
import html
from pathlib import Path

from make_images import ANCHORS, FRAMES

PROJ = Path(__file__).parent

# (shot, duration, title, dialogue) — mirrors storyboard.md
SHOTS = [
    ("t_title", 0, "Title", None),
    ("t_1366", 0, "England, 1366", None),
    ("a1_bell", 6, "Cold open — the bell of Beaulieu", None),
    ("a2_trial", 10, "The trial of brother John", 'ABBOT: "What talk is this? Is this a tongue to be used within the walls of an old and well-famed monastery?" JOHN: "By the black rood of Waltham! if any knave among you lays a finger-end upon the edge of my gown, I will crush his skull like a filbert!"'),
    ("a3_flight", 8, "The black sheep comes forth", None),
    ("a4_farewell", 8, "Alleyne comes out into the world", 'ABBOT: "Thy father willed it: one year in the world, and then choose between cloister and mankind." ALLEYNE: "I shall come back to you, father."'),
    ("a5_merlin", 10, "The Pied Merlin", 'JOHN: "I shall stand by him, and he shall neither be put out on the road, nor shall his ears be offended indoors. ...Hush, lad, I count them not a fly."'),
    ("a6_aylward", 12, "Enter Samkin Aylward", 'AYLWARD: "By my hilt! camarades... I am a true English bowman, Samkin Aylward by name. To Sir Claude Latour and the White Company!"'),
    ("a7_song", 12, "The Song of the Bow", 'ALL (sung): "So we\'ll drink all together / To the gray goose feather / And the land where the gray goose flew!"'),
    ("a8_wrestle", 12, "The feather-bed wager", 'AYLWARD: "By my hilt! then, I have found a man at last!" (The limner wakes: "\'Ware the ale!")'),
    ("a9_rescue", 12, "Brother against brother", 'ALLEYNE: "Brother or no, I swear by my hopes of salvation that I will break your arm if you do not leave hold of the maid."'),
    ("a10_bank", 10, "The maid of the forest", 'MAUDE: "You had him at your mercy. Why did you not kill him?" ALLEYNE: "Kill him! My brother!" MAUDE: "He would have killed you. I know him, and I read it in his eyes."'),
    ("b1_stone", 10, "The stone test", 'NIGEL: "I fear that I overtask you, for it is of a grievous weight." — "Good lack!" — "Good lack!"'),
    ("b2_bear", 10, "The bear and the handkerchief", 'NIGEL: "Ah, saucy! saucy." JOHN (after): "I was a fool not to know that a little rooster may be the gamest."'),
    ("b3_hall", 10, "The letter — and the laugh", 'MAUDE: "Ma foi! and here is our wandering clerk." NIGEL: "By Saint Paul! it is a very honorable venture. Alleyne Edricson, you shall ride as my squire."'),
    ("b4_veil", 12, "The green veil", 'ALLEYNE: "You are my heart, my life, my one and only thought." MAUDE: "Win my father\'s love, and all may follow."'),
    ("b5_march", 8, "The Company marches", 'NIGEL: "Your glove, my life\'s desire! I shall proclaim you the fairest and sweetest in Christendom, and joust with any who deny it."'),
    ("c1_sail", 8, "Two lean wolves", 'HAWTAYNE: "I like it not. And yet Goodwin Hawtayne is not the man to stand back when his fellows are for pressing forward."'),
    ("c2_ruse", 10, "The trap springs", 'NIGEL: "Ma foi! but they come to our lure like chicks to the fowler. To your arms, men! Now blow out the trumpets, and may God\'s benison be with the honest men!"'),
    ("c3_melee", 12, "John's play-by-play", 'JOHN: "My God, but it is a noble fight! ...Ah, by Our Lady, his sword is through him! Down goes the red cross, and up springs Simon with the scarlet roses!"'),
    ("d1_patch", 8, "The eye-patch vow", 'NIGEL: "I vow that I will not take this patch from my eye until I have seen something of this country of Spain." AYLWARD: "There will come bloodshed of that patch, or I am the more mistaken."'),
    ("d2_chandos", 8, "A pair between us", 'CHANDOS: "Ha, my little heart of gold! Since you have tied up one of your eyes, and I have had the mischance to lose one of mine, we have but a pair between us."'),
    ("d3_prince", 12, "Hang me, my liege", 'NIGEL: "It is a very small matter that I should be hanged, but it would be a very grievous thing that you should make a vow and fail to bring it to fulfilment." PRINCE: "Peace! peace! I am very well able to look to my own vows and their performance."'),
    ("d4_tourney", 10, "The bald head shining", 'PRINCE: "Who comes next for England, John?" CHANDOS: "Sir Nigel Loring of Hampshire, sire."'),
    ("d5_stranger", 10, "The champion from the East", 'KNIGHT: "I will neither drink your wine nor sit at your table. I bear no love for you or for your race." PRINCE: "By St. George! he has served his master this day even as I would wish liegeman of mine to serve me."'),
    ("t_france", 0, "France", None),
    ("e1_road", 8, "The ravaged land", None),
    ("e2_inn", 12, "Du Guesclin", 'DU GUESCLIN: "Dogs of England, must ye be lashed hence? Tiphaine, my sword! ...Mort Dieu! it is my little swordsman of Bordeaux." NIGEL: "Bertrand! Bertrand du Guesclin!"'),
    ("e3_prophecy", 12, "The blessed hour of sight", 'TIPHAINE: "Danger, Bertrand — deadly, pressing danger — which creeps upon you and you know it not." DU GUESCLIN: "But is this so very close, Tiphaine?" TIPHAINE: "Here — now — close upon you!"'),
    ("e4_night", 8, "Seventy and nine", 'ALLEYNE: "Seventy and nine. My God! What has come upon us?"'),
    ("e5_hall", 10, "France and England together", 'DU GUESCLIN: "France and England will fight together this night." NIGEL: "There are many ways in which a man might die, but none better than this."'),
    ("e6_keep", 8, "The door off its hinges", 'AYLWARD: "By my hilt! up, up, mes enfants!"'),
    ("e7_powder", 10, "The powder-box", 'NIGEL: "Throw back the lid, John, and drop the box into the fire!"'),
    ("e8_song", 12, "The song in the dark", 'TIPHAINE: "Hush and listen! I have heard the voices of men all singing together in a strange tongue." AYLWARD: "By these ten finger-bones, we are saved! It is the marching song of the White Company. Hush!"'),
    ("e9_tree", 10, "Counsel round the fallen tree", 'NIGEL: "I have lived in honor, and in honor I trust that I shall die." LATOUR: "I will not go to Dax." JOHN: "The proper life for a robber!"'),
    ("t_spain", 0, "Spain, 1367", None),
    ("f1_pass", 8, "Roncesvalles", 'BLACK SIMON: "Yonder is where Roland fell."'),
    ("f2_volunteers", 10, "They have all stepped forward", 'NIGEL: "That I should live to see the day! What! not one——" ALLEYNE: "My fair lord, they have all stepped forward." OLIVER: "For pullets."'),
    ("f3_raid", 10, "I have come for the king", 'NIGEL: "I have come for the king; and, by Saint Paul! he must back with us or I must bide here."'),
    ("f4_mist", 10, "The mist parts — 370 against 6,000", 'NIGEL: "Now order the ranks, and fling wide the banners, for our souls are God\'s and our bodies the king\'s, and our swords for Saint George and for England!"'),
    ("f5_duel", 12, "The patch comes off", 'NIGEL: "I think that I am now clear of my vow, for this Spanish knight was a person from whom much honor might be won."'),
    ("f6_storm", 8, "The arrow-storm", 'AYLWARD: "Johnston! ...Loose steady, mes garcons. Every shaft well sent."'),
    ("f7_stand", 10, "The last stand", 'BURLEY: "Might we not even now make a retreat?" NIGEL: "My soul will retreat from my body first! Here I am, and here I bide, while God gives me strength to lift a sword."'),
    ("f8_cliff", 12, "The rope", 'ALLEYNE: "I pray you, my dear lord, that you will give my humble service to the Lady Maude, and say to her that I was ever her true servant and most unworthy cavalier." NIGEL: "Now may God speed ye, for ye are brave and worthy men."'),
    ("f9_after", 12, "The White Company is here disbanded", 'ALLEYNE: "Tell me, John: where is my dear lord, Sir Nigel Loring?" JOHN: "He is dead, I fear. I saw them throw his body across a horse and ride away with it." CALVERLEY: "Nay — the White Company is here disbanded."'),
    ("t_home", 0, "Hampshire, four months later", None),
    ("g1_news", 8, "News on the road", 'LADY: "News hath come that not one of the Company was left alive, and so, poor lamb, she takes the veil at Romsey this very day." ALLEYNE: "Lady! Is it the Lady Maude Loring of whom you speak? — And I stand talking here! Come, John, come!"'),
    ("g2_nunnery", 12, "The church door", 'ALLEYNE: "Maude! The Company fell — but I live, and I am come for you."'),
    ("g3_inn", 12, "The inn resurrection", 'AYLWARD: "Ah, mes belles! ...by my hilt! it does me good to look at your English cheeks." NIGEL (from the window): "...a very humble knight of England abides here, so that if he be in need of advancement, or have any small vow upon his soul, or desire to exalt his lady, I may help him to accomplish it."'),
    ("g4_end", 10, "Home-coming", 'ALL (sung, reprise): "So we\'ll drink all together / To the gray goose feather / And the land where the gray goose flew."'),
]

ACTS = {
    "a": "Act I — The Black Sheep (New Forest, autumn 1366)",
    "b": "Act II — Twynham Castle",
    "c": "Act III — The Yellow Cog",
    "d": "Act IV — Bordeaux",
    "e": "Act V — France & the Jacquerie",
    "f": "Act VI — Spain (March 1367)",
    "g": "Act VII — The Home-coming (Hampshire, July)",
}

FRAME_PROMPTS = {name: (prompt, refs) for name, prompt, refs in FRAMES}


def img_cell(rel, cls="frame"):
    return (f'<a href="{rel}" target="_blank"><img class="{cls}" src="{rel}" '
            f'loading="lazy"></a>')


rows, act_seen = [], set()
total = 0
for shot, dur, title, dialogue in SHOTS:
    if shot.startswith("t_"):
        rel = f"cards/{shot}.png"
        exists = (PROJ / rel).exists()
        rows.append(f'<div class="card">{img_cell(rel, "cardimg") if exists else ""}'
                    f'<p class="cardtitle">{html.escape(title)}'
                    f'{"" if exists else " <span class=tag>missing</span>"}</p></div>')
        continue
    ch = shot[0]
    if ch not in act_seen:
        act_seen.add(ch)
        rows.append(f"<h2>{html.escape(ACTS[ch])}</h2>")
    total += dur
    rel = f"frames/{shot}.png"
    exists = (PROJ / rel).exists()
    prompt_html = ""
    if shot in FRAME_PROMPTS:
        p, refs = FRAME_PROMPTS[shot]
        ref_s = (f'<div class="refs">anchor refs: {html.escape(", ".join(refs))}</div>'
                 if refs else "")
        prompt_html = (f"<details><summary>frame prompt</summary>"
                       f'<p class="prompt">{html.escape(p)}</p>{ref_s}</details>')
    carried = "dialogue" if dialogue else "visual"
    rows.append(f"""
<div class="shot">
  {img_cell(rel) if exists else '<div class="frame missing">frame pending</div>'}
  <div class="meta">
    <h3>{shot} — {html.escape(title)} <span class="tag {carried}">{carried}</span></h3>
    <p class="stats">planned {dur}s</p>
    {f'<p class="dlg">{html.escape(dialogue)}</p>' if dialogue else ''}
    {prompt_html}
  </div>
</div>""")

anchor_cells = "".join(
    f'<figure><a href="anchors/{n}.png" target="_blank">'
    f'<img src="anchors/{n}.png" loading="lazy"></a>'
    f"<figcaption>{n}</figcaption></figure>"
    for n, _, _, _ in ANCHORS if (PROJ / f"anchors/{n}.png").exists())

page = f"""<!doctype html><meta charset="utf-8"><title>The White Company — storyboard</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.45 -apple-system, sans-serif;
       max-width: 1100px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight: 600; }} h2 {{ margin-top: 44px; color: #d99; }}
.shot {{ display:flex; gap:18px; margin:18px 0; padding:14px; background:#1d1d22;
         border-radius:10px; }}
.frame {{ width:480px; border-radius:6px; flex-shrink:0; background:#000; display:block; }}
.frame.missing {{ height:270px; display:flex; align-items:center; justify-content:center;
                  color:#556; border:1px dashed #334; }}
.shot a {{ flex-shrink:0; }}
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
.card {{ margin:26px 0; text-align:center; }}
.cardimg {{ max-width:640px; width:100%; border-radius:6px; }}
.cardtitle {{ color:#99a; font-size:13px; margin:6px 0; }}
.anchors {{ display:flex; flex-wrap:wrap; gap:12px; }}
.anchors figure {{ margin:0; width:130px; }}
.anchors img {{ width:130px; border-radius:6px; display:block; }}
.anchors figcaption {{ color:#889; font-size:12px; text-align:center; margin-top:3px; }}
</style>
<h1>THE WHITE COMPANY — illustrated storyboard (frame pass)</h1>
<p>Adapted from Arthur Conan Doyle (1891). {sum(1 for s,_,_,_ in SHOTS if not s.startswith('t_'))} shots,
planned ~{total // 60}:{total % 60:02d}. All frames are Nano Banana stills generated from the
character anchors below; they will become Seedance start frames in the clip pass.
Yellow = dialogue carried by the shot (verbatim Doyle). Click any image for full size.</p>
<h2>Cast &amp; location anchors</h2>
<div class="anchors">{anchor_cells}</div>
{''.join(rows)}
"""
(PROJ / "storyboard.html").write_text(page)
print(f"wrote storyboard.html ({sum(1 for s, *_ in SHOTS if not s.startswith('t_'))} shots, "
      f"~{total}s planned)")
