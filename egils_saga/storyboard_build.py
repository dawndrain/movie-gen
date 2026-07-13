#!/usr/bin/env python3
"""Build egils_saga/storyboard.html: every shot in cut order — start frame,
playable clip (when rendered), beat title, dialogue/narration, collapsed
generation prompt. Rerun after any change."""
import html
import importlib.util
from pathlib import Path

HERE = Path(__file__).parent

# (shot, act header or None, beat title, dialogue/action text)
SHOTS = [
    ("p1", "Prologue — The Wolf's Prophecy", "The Evening-Wolf",
     'NARR: "They called him Kveldulf — the Evening-Wolf. Each day as the sun went down he grew sullen, '
     'and no man could speak with him. It was said he was shape-strong."'),
    ("p2", None, "Kveldulf refuses the king",
     'KVELDULF: "Say this to your king: Kveldulf will sit at home. I think he has a whole load of good '
     'fortune, where our king has not a handful."'),
    ("p3", None, "Father and son",
     'THOROLF K: "I am resolved to seek the king, and become his man."  KVELDULF: "My foreboding is that '
     'we shall reap ruin from that king. Beware — keep within bounds, nor rival thy betters."'),
    ("p4", None, "The granary feast",
     'NARR: "Thorolf feasted the king with five hundred men — where the king brought three hundred. '
     'Kings do not forgive arithmetic."'),
    ("p5", None, "The slander",
     'HAREK: "He keeps a guard round him like a king. Keep Thorolf near thee, lord — that he make not '
     'himself too great for thee."'),
    ("p6", None, "The burning of Sandness",
     'THOROLF K: "Now am I but three feet short of my aim!" — he falls forward at the king\'s feet.'),
    ("p7", None, "He will be avenged who falls forward",
     'KVELDULF: "It is an old saw: he will be avenged who falls forward. But vengeance will not be mine. '
     'My sons must sail. There is new land found — westward. Iceland."'),
    ("p8", None, "The coffin overboard",
     'KVELDULF (V.O.): "Make me a coffin, and put me overboard. It will go far otherwise than I think, '
     'if I do not come to Iceland and take land there."'),
    ("p9", None, "The dead man chooses the land",
     'NARR: "The dead man chose the land. They built at Borg — and there the story truly begins."'),

    ("a1", "Act 1 — The Ugly Son", "Three years old, riding alone",
     'NARR: "Skallagrim had two sons. Thorolf, fair and beloved. And Egil: black-haired, ugly, and '
     'already too big. At three he was strong as a boy of seven — and he made verses."'),
    ("a2", None, "The first poem",
     'EGIL CHILD: "Hasting I came to the hearth-fire of Yngvar, him who on heroes bestoweth gold. '
     'Thou wilt not find a doughtier song-smith of three winters."'),
    ("a3", None, "The makings of a freebooter",
     'BERA: "You have the makings of a freebooter, my son."  EGIL CHILD: "Thus counselled my mother: for '
     'me shall they purchase a galley and good oars. So may I, high-standing, hew down many foemen."'),
    ("a4", None, "Shape-strength at sunset",
     'BRAK: "Dost thou turn thy shape-strength, Skallagrim, against thy son?"'),
    ("a5", None, "Paid in kind",
     'NARR: "That evening Egil killed the man his father loved best. They did not speak all winter. '
     'In that family, grief was paid in kind."'),

    ("b1", "Act 2 — The King's Enemy", "Bard's feast",
     'NARR: "Grown, Egil went east — and made an enemy of a queen. Gunnhild: beautiful, shrewd, and of '
     'magic cunning."'),
    ("b2", None, "The poisoned horn",
     'EGIL: "Write we runes around the horn, redden all the spell with blood. Learn that health abides '
     'in ale — holy ale that Bard hath blessed." — the horn BURSTS.'),
    ("b3", None, "Bard falls in his doorway",
     'NARR: "Bard fell dead in his own doorway. And the king\'s hunt began."'),
    ("b4", None, "The swim", "(silent — weapons bundled on his back, grey water)"),
    ("b5", None, "No odds between them",
     'GUNNHILD: "Thou lendest easy ear to talk. Egil has slain thy friends and thy steward — I reckon no '
     'odds between him and his brother."  EIRIK: "Egil shall not be long harboured in my realm."'),

    ("c1", "Act 3 — Vinheath", "The false camp",
     'NARR: "The brothers took service with Athelstan of England, against Olaf king of Scots. Athelstan '
     'bought a week with empty tents and false envoys. Then the armies met at Vinheath."'),
    ("c2", None, "This separation I shall often rue",
     'EGIL: "I will not that I and Thorolf be parted in the battle."  THOROLF S: "Brother, you will have '
     'your way — but it is the king\'s array."  EGIL: "This separation I shall often rue."'),
    ("c3", None, "The ambush from the wood", "(Thorolf falls, pierced by many spears at once)"),
    ("c4", None, "Egil turns the battle",
     'NARR: "Egil took Earl Adils\' life, and the day turned. Athelstan won England\'s greatest victory. '
     'It cost Egil his brother."'),
    ("c5", None, "Green grows on Vinheath",
     'EGIL: "Green grows on soil of Vinheath, grass o\'er my noble brother. But we our woe — a sorrow '
     'worse than death-pang — must bear."'),
    ("c6", None, "THE RING OVER THE FIRE",
     "(wordless — Athelstan hangs a gold ring on his sword-point and reaches it across the fire; Egil "
     "hooks it off point-to-point; his brows settle level; he drinks)"),

    ("d1", "Act 4 — The Curse and the Head-Ransom", "The court is broken",
     'EGIL (shouted): "Then I ban these lands! I denounce him who holds them: law-breaker, peace-breaker, '
     'and ACCURSED!"'),
    ("d2", None, "The nithing pole",
     'EGIL: "Here set I up a curse-pole, and this curse I turn on King Eirik and Queen Gunnhild — and on '
     'the land-spirits of this land: may they all wander astray, and never find their home, till they '
     'have driven King Eirik and Gunnhild from the land."'),
    ("d3", None, "Wrecked into the wolf's mouth",
     'NARR: "The curse worked. Eirik was driven from Norway — to England, where Athelstan gave him York '
     'to hold. And Gunnhild worked a spell of her own: that Egil should find no rest till she had seen '
     'him. His ship broke at Humber-mouth — in Eirik Bloodaxe\'s new kingdom."'),
    ("d4", None, "Arinbjorn's door",
     'ARINBJORN: "Egil. There is nothing for it now. You shall bring the king your head — and I will be '
     'your spokesman."'),
    ("d5", None, "Bring the king your head",
     'GUNNHILD: "Why is Egil not slain at once? Have you forgotten, king, what he has done — your '
     'friends, your kin, your own son?"  ARINBJORN: "Night-slaying is murder, king. Give him till '
     'morning. If he has spoken evil of thee, he can atone in words of praise that shall live for all time."'),
    ("d6", None, "The swallow at the window",
     "(silent — the witch-bird spoils the verse until Arinbjorn keeps watch on the roof)"),
    ("d7", None, "The Head-Ransom",
     'EGIL: "Westward I sailed the wave; within me Odin gave the sea of song I bear. My mind a galleon '
     'fraught with load of minstrel thought... Glory and fame gat Eirik\'s name."'),
    ("d8", None, "Take your head",
     'EIRIK: "The poem is well delivered. I give thee thy head this time — because thou camest freely '
     'into my power. But know this for sure: it is no reconciliation."'),

    ("e1", "Act 5 — Sonatorrek and the Silver", "The boat goes down",
     'NARR: "Egil went home to Borg, and grew old, and had sons. Bodvar was the best of them — fair, '
     'like the Thorolfs. He was seventeen when the boat went down."'),
    ("e2", None, "The kirtle splits",
     "(silent — Egil carries his son to Skallagrim's mound; his clothes split off his swollen arms)"),
    ("e3", None, "The locked bed-closet",
     'NARR: "He locked himself in his bed-closet, and would take neither food nor drink. He meant to '
     'die. Three days. Then his daughter came."'),
    ("e4", None, "The milk trick",
     'THORGERD: "Father, open the door. I will that we both travel the same road." ... EGIL: "We are '
     'deceived. This is milk." — he bites a sherd clean out of the horn.'),
    ("e5", None, "Sonatorrek begins",
     'THORGERD: "Then let us lengthen our lives, father — long enough that you make a funeral poem on '
     'Bodvar."  EGIL: "Much doth it task me my tongue to move... Me Ran, the sea-queen, roughly hath '
     'shaken: I stand of beloved ones stript and all bare."'),
    ("e6", None, "Boot for bale",
     'EGIL: "The god broke faith and friendship, false in my need — yet he gave me poesy faultless, '
     'boot for bale. And on Digra-ness Hel waits. Dauntless in bearing, her death-blow I bide."'),
    ("e7", None, "Blind by the fire",
     'EGIL: "Blind near the blaze I wander, and beg the fire-maid\'s pardon. Yet England\'s mighty '
     'monarch me whilom greatly honoured — and princes once with pleasure the poet\'s accents heard."'),
    ("e8", None, "A famous plan",
     'EGIL: "I mean to carry Athelstan\'s silver to the Hill of Laws — and sow it broadcast into the '
     'biggest crowd of the Thing. Kicks there will be, I fancy, and blows."  THORDIS: "A famous plan! '
     'It will be remembered as long as Iceland is inhabited."'),
    ("e9", None, "The silver goes into the earth",
     'NARR: "One night the silver went into the earth instead — and the two thralls with it. Blind, in '
     'his ninth decade, he killed his last two men. English pennies still wash out of the gill after '
     'thaws. The hoard has never been found."'),
    ("e10", None, "The skull that would not break",
     'NARR: "When they moved the bones, the skull would not break. Heavy and wave-marked, like a shell. '
     'It was a hard head to take, alive or dead. And so ends this story."'),
]

CLIP_DIRS = ["outputs/v1", "outputs/v2", "outputs/v3"]  # later dirs win


def load_frame_prompts():
    spec = importlib.util.spec_from_file_location("frames_spec", HERE / "frames_spec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {n: (p, refs) for n, _a, p, refs in mod.FRAMES}


def clip_for(shot: str):
    best = None
    for d in CLIP_DIRS:
        p = HERE / d / f"{shot}.mp4"
        if p.exists():
            best = p
    return best


def main():
    prompts = load_frame_prompts()
    rows = []
    for shot, act, title, dialog in SHOTS:
        if act:
            rows.append(f'<h2>{html.escape(act)}</h2>')
        frame = HERE / "frames" / f"{shot}.png"
        img = (f'<a href="frames/{shot}.png"><img src="frames/{shot}.png" loading="lazy"></a>'
               if frame.exists() else '<div class="missing">frame pending</div>')
        clip = clip_for(shot)
        vid = (f'<video src="{clip.relative_to(HERE)}" controls preload="none"></video>'
               if clip else '<div class="missing">clip pending</div>')
        prompt, refs = prompts.get(shot, ("", []))
        det = (f'<details><summary>frame prompt · refs: {", ".join(refs) or "none"}</summary>'
               f'<p class="prompt">{html.escape(prompt)}</p></details>') if prompt else ''
        rows.append(f'''
<div class="shot" id="{shot}">
  <div class="media">{img}{vid}</div>
  <div class="meta">
    <span class="tag">{shot}</span> <b>{html.escape(title)}</b>
    <p>{dialog}</p>
    {det}
  </div>
</div>''')

    anchors = sorted((HERE / "anchors").glob("*.png")) if (HERE / "anchors").exists() else []
    anchor_html = "".join(
        f'<figure><a href="anchors/{a.name}"><img src="anchors/{a.name}" loading="lazy"></a>'
        f'<figcaption>{a.stem}</figcaption></figure>' for a in anchors)

    page = f'''<!doctype html><meta charset="utf-8">
<title>EGIL — storyboard</title>
<style>
 body {{ background:#101014; color:#ddd; font:15px/1.5 -apple-system, sans-serif;
        max-width:1200px; margin:2em auto; padding:0 1em; }}
 h1 {{ font-weight:200; letter-spacing:.18em; }}
 h2 {{ color:#c9a86a; font-weight:300; border-bottom:1px solid #333; margin-top:2em; }}
 .shot {{ display:flex; gap:1em; margin:1.2em 0; background:#191920; border-radius:10px;
         padding:.8em; }}
 .media {{ display:flex; gap:.6em; flex-shrink:0; }}
 .media img, .media video {{ width:380px; border-radius:6px; object-fit:cover; }}
 .missing {{ width:380px; display:flex; align-items:center; justify-content:center;
            color:#555; border:1px dashed #333; border-radius:6px; min-height:214px; }}
 .tag {{ background:#4a3a1a; color:#f0d9a8; border-radius:4px; padding:0 .5em;
        font-family:monospace; }}
 .meta p {{ color:#bbb; }}
 details {{ color:#777; font-size:13px; }} .prompt {{ color:#888; }}
 .anchors {{ display:flex; flex-wrap:wrap; gap:.8em; }}
 .anchors figure {{ margin:0; text-align:center; }}
 .anchors img {{ height:200px; border-radius:6px; }}
 .anchors figcaption {{ color:#888; font-family:monospace; font-size:12px; }}
</style>
<h1>EGIL</h1>
<p>A film of Egil's Saga — first-pass storyboard, {len(SHOTS)} shots.
Frames: Nano Banana Pro 2k. Clips: Seedance 2.0 (pending).
Treatment: <a href="storyboard.md" style="color:#c9a86a">storyboard.md</a> ·
Voices: <a href="voices.md" style="color:#c9a86a">voices.md</a> ·
Auditions: <a href="auditions.html" style="color:#c9a86a">auditions.html</a></p>
{'<h2>Animatic</h2><video src="animatic_v1.mp4" controls style="width:100%;max-width:1000px;border-radius:10px"></video>' if (HERE / "animatic_v1.mp4").exists() else ''}
{"".join(rows)}
<h2>Anchors ({len(anchors)})</h2>
<div class="anchors">{anchor_html}</div>
'''
    (HERE / "storyboard.html").write_text(page)
    print("wrote", HERE / "storyboard.html", f"({len(SHOTS)} shots, {len(anchors)} anchors)")


if __name__ == "__main__":
    main()
