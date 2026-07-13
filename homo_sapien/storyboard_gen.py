#!/usr/bin/env python3
"""Build home_sapien/storyboard.html — the review page.

Cast gallery + every shot in cut order with its Nano Banana start frame, its
lyric, its timecode, and its collapsed generation prompt. The song itself is
embedded: click any shot and the track seeks to that shot's in-point, so you
can check every cut against the actual beat. Once outputs/video1/<shot>.mp4
exists, the frame is replaced by the playable clip.

Rerun after any frame/clip change.
"""
import base64
import html
import importlib.util
import subprocess
from pathlib import Path

PROJ = Path(__file__).parent
ANCHORS = PROJ / "anchors"
FRAMES = PROJ / "frames"
V1 = PROJ / "outputs/video1"
THUMBS = PROJ / "storyboard_thumbs"
AUDIO = PROJ / "audio/homo_sapien.m4a"

def _load(name):
    spec = importlib.util.spec_from_file_location(name, PROJ / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fs = _load("frames_spec")
cs = _load("clips_spec")
mi = _load("make_images")

PROMPTS = {n: p for n, _a, p, _r in fs.FRAMES}
REFS = {n: r for n, _a, _p, r in fs.FRAMES}
CLIP_PROMPT = {n: p for n, _d, p, _r in cs.CLIPS}
CLIP_DUR = {n: d for n, d, _p, _r in cs.CLIPS}
CLIP_REFS = {n: r for n, _d, _p, r in cs.CLIPS}
# anchor prompts, so the cast gallery can show how each anchor was made
ANCHOR_PROMPT = {n: p for n, _a, p, _r in (mi.ANCHORS1 + mi.ANCHORS2)}

# (shot, in_sec, out_sec, lyric_or_None, description)
SHOTS = [
    ("__act", "COLD OPEN", "0:00 – 0:17  ·  intro, no vocal", None, None),
    # One second moved from s01 to s02: s02 has to get him across the room AND land
    # the embrace, and at 6s it was arriving right on the cut. s01 loses nothing —
    # she's just dancing.
    ("s01_kitchen_dance", 0.0, 6.0, None,
     "1am. May alone, barefoot, doing a private terrible little dance while the kettle boils."),
    ("s02_two_dance", 6.0, 13.0, None,
     "Ollie shuffles in half-asleep and joins without comment. The whole film in seven seconds — "
     "and the first forehead touch."),
    ("s03_eye", 13.0, 17.5, None,
     "Push into May's eye as she laughs. The blue window in her iris breaks apart into stars."),

    ("__act", "VERSE 1", "0:17 – 1:00  ·  the cosmos and the slime", None, None),
    ("s04_bigbang", 17.5, 21.5, "First there was the big bang",
     "Two sparks — one coral, one teal — spin out of the flash already orbiting each other. "
     "The Big Bang looks like glitter in a shaft of light."),
    ("s05_binary_stars", 21.5, 25.6, "and stars began to shine",
     "A binary pair, leaning into one another. A forehead touch at cosmic scale."),
    ("s06_tidepool", 25.6, 34.9, "Then there was existence, primordial slime",
     "A tidepool the size of a soup bowl. Two glowing blobs wobble toward each other, bump, "
     "recoil, bump again. They stick."),
    ("s07_waiting", 34.9, 42.8, "How I was waiting all that time",
     "One creature alone on a rock, WAITING, with infinite deadpan patience, while a hundred "
     "million years of weather rips past behind it. The funniest shot in the video."),
    ("s08_side_by_side", 42.8, 51.5, "While we were evolving side by side",
     "Two lanes of evolution running side by side like conveyor belts, each creature glancing "
     "across to check the other one is keeping up."),
    ("s09a_fish", 51.5, 53.5, "Rock to fish…",
     "Two fish, fins touching, snouts nudged. Beat-cut."),
    ("s09b_monkeys", 53.5, 55.5, "…monkey to man",
     "Two monkeys upside-down by their tails, holding hands, foreheads bonked. Beat-cut."),
    ("s10_hominids", 55.5, 60.5, "It's why this love begun",
     "Savanna at dawn. Two hominids forehead to forehead. Third time — now the audience has "
     "learned the gesture."),

    ("__act", "CHORUS 1", "1:00 – 1:36  ·  the ancient world, cut against home", None, None),
    ("s11_flower_cave", 60.5, 64.5, "Be my Homo Sapien",
     "40,000 BCE: May offers Ollie a scrappy wildflower with total confidence. He is stunned."),
    ("s12_flower_kitchen", 64.5, 68.5, "'Cause I evolved to love you",
     "MATCH CUT — same framing, same grin, same pose: petrol-station flowers across the kitchen "
     "counter. The match is the joke and the payoff."),
    ("s13_hold_cave", 68.5, 72.5, "Let me hold you till the end",
     "The pair curled together in furs under an enormous sky of stars."),
    ("s14_hold_couch", 72.5, 77.5, "'Cause I evolved to love you",
     "MATCH CUT — the same shape on a sagging couch, TV glow instead of firelight, the same "
     "stars through the window."),
    ("s15_morph_walk", 77.5, 81.5, "We will grow and change, my friend",
     "One continuous walk, hand in hand, changing form as they go — hominid, sapien, medieval, "
     "modern. They never let go."),
    ("s16_groceries", 81.5, 85.5, "But I'll evolve to love you",
     "Ollie attempts all the groceries in one trip. May watches, delighted, and helps him not "
     "at all."),
    ("s17_diorama_dance", 85.5, 90.5, "So be my Homo Sapien",
     "The two of them doing the kitchen dance INSIDE a museum diorama, as if they wandered in "
     "and forgot to leave. First tease of the ending."),
    ("s18_tree_of_life", 90.5, 96.0, "'Cause I evolved to, I evolved to love you",
     "The tree of life drawn across the whole sky in constellation-lines — and every fork of it "
     "has two little lights on it."),

    ("__act", "INSTRUMENTAL", "1:36 – 1:43  ·  the plant", None, None),
    ("s19_handprints", 96.0, 103.8, None,
     "Two hands press into wet ochre on the cave wall and lift away. Two handprints. "
     "THE PLANT — it pays off at 3:22."),

    ("__act", "VERSE 2", "1:43 – 2:08  ·  fire and mutation", None, None),
    ("s20_clay", 103.8, 111.7, "We formed and mutated over time",
     "Two clay figures sculpting themselves into shape. One accidentally gives himself a sixth "
     "finger. He shows her. She adds one to match."),
    ("s21_fire", 111.7, 120.7, "We hunted and gathered, and played with fire",
     "He is a catastrophic hunter (a rabbit ignores him entirely); she is an excellent gatherer "
     "and extremely smug. Then the fire catches, and both their faces light up."),
    ("s22_fire_foreheads", 120.7, 128.5, "Every evolution, every step was divine",
     "Firelit forehead touch. Sparks rise off the fire and become the two stars from 0:21, "
     "still orbiting."),

    ("__act", "CHORUS 2", "2:08 – 2:44  ·  all of human history, small and domestic", None, None),
    ("s23_neolithic", 128.5, 133.5, "Be my Homo Sapien",
     "Neolithic: pushing seeds into a furrow with their thumbs, arguing cheerfully about spacing."),
    ("s24_pot", 133.5, 137.5, "'Cause I evolved to love you",
     "Two figures painted on an ancient pot turn to face each other and touch foreheads."),
    ("s25_medieval", 137.5, 141.5, "Let me hold you till the end",
     "A village festival. They dance the same terrible dance, badly, 800 years early."),
    ("s26_victorian", 141.5, 145.5, "'Cause I evolved to love you",
     "A long-exposure portrait they completely ruin by laughing."),
    ("s27_fifties_kitchen", 145.5, 150.5, "We will grow and change, my friend",
     "A 1950s kitchen — and by the end of the dolly move it has become THEIR kitchen, present "
     "day. The one real camera move in the sequence."),
    ("s28_flatpack", 150.5, 154.5, "But I'll evolve to love you",
     "Flat-pack furniture has defeated him. She sits on the one shelf he finished and pats it."),
    ("s29_proposal", 154.5, 158.5, "So be my Homo Sapien",
     "She proposes on the lino with a paperclip bent into a ring. He is crying and nodding."),
    ("s30_wedding", 158.5, 164.5, "'Cause I evolved to, I evolved to love you",
     "A tiny cheap wedding. The backlit confetti is the same drifting warm dust as the Big Bang."),

    ("__act", "BRIDGE", "2:44 – 3:08  ·  the kooky-sweet centre", None, None),
    ("s31_blush", 166.2, 170.5, "And procreate with you",
     "They look at each other across the hall. Both go pink and look away. The song says it "
     "cheerfully out loud; the video is coy for exactly one beat."),
    ("s31b_babyhand", 170.5, 175.5, "(…)",
     "SMASH CUT: a newborn's hand closing around Ollie's enormous finger. Held long enough to "
     "hurt a little."),
    ("s32_toddler_chaos", 175.5, 184.5, "Let's continue the species",
     "Total domestic chaos. The only handheld shot in the film."),
    ("s33_family_tree", 184.5, 188.5, "Expand our family tree",
     "The literal family tree: photographs hanging from the branches of a real tree, kids "
     "climbing in it."),

    ("__act", "THE MUSEUM", "3:08 – 3:34  ·  instrumental — the payoff", None, None),
    ("s34_museum_enter", 188.5, 195.0, None,
     "The family walks into an empty after-hours natural history museum. The kid runs ahead."),
    ("s35_dioramas", 195.0, 202.0, None,
     "Slow dolly past the dioramas — and every one is a pair we've already met, still doing the "
     "gesture, frozen mid-love, watching the family go by."),
    ("s36_glass_handprints", 202.0, 208.0, None,
     "The cave-painting case: THE TWO HANDPRINTS FROM 1:36. She puts her hand on the glass over "
     "one. He puts his over the other. Nobody says anything. Do not move the camera."),
    ("s37_dome_to_stars", 208.0, 214.5, None,
     "Crane up past the whale, through the dome, out into the starfield — where the two stars "
     "are still orbiting each other."),

    ("__act", "FINAL", "3:34 – 3:59", None, None),
    ("s38_old_dance", 214.5, 218.6, "So be my Homo Sapien",
     "The same kitchen, the same camera position as 0:07. Fifty years later. The same terrible "
     "dance. A grandchild watches, unimpressed."),
    ("s39_fridge_handprints", 218.6, 226.0, "'Cause I evolved to, I evolved to love you",
     "The last forehead touch. On the fridge behind them: two small handprints in poster paint."),
    ("s40_pullback", 226.0, 236.0, None,
     "The pull-back starts and never stops. One lit window in a lot of dark."),
    ("s40b_earth", 236.0, 239.0, None,
     "Earth as one warm point of light. Hold until the track fades. Cut to black on the last note."),
]


def tc(s: float) -> str:
    return f"{int(s // 60)}:{s % 60:05.2f}"


def thumb(name: str) -> str:
    """Return a data: URI for the shot's frame (or a placeholder)."""
    src = FRAMES / f"{name}.png"
    if not src.exists():
        return ""
    THUMBS.mkdir(exist_ok=True)
    dst = THUMBS / f"{name}.jpg"
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
                        "-vf", "scale=720:-1", "-q:v", "4", str(dst)], check=True)
    return "data:image/jpeg;base64," + base64.b64encode(dst.read_bytes()).decode()


def anchor_thumb(name: str) -> str:
    src = ANCHORS / f"{name}.png"
    if not src.exists():
        return ""
    THUMBS.mkdir(exist_ok=True)
    dst = THUMBS / f"a_{name}.jpg"
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
                        "-vf", "scale=420:-1", "-q:v", "4", str(dst)], check=True)
    return "data:image/jpeg;base64," + base64.b64encode(dst.read_bytes()).decode()


CAST = [
    ("may", "May", "coral"),
    ("ollie", "Ollie", "teal"),
    ("may_sapien", "May · 40,000 BCE", "coral"),
    ("ollie_sapien", "Ollie · 40,000 BCE", "teal"),
    ("may_old", "May · 75", "coral"),
    ("ollie_old", "Ollie · 77", "teal"),
    ("kid", "The kid", ""),
    ("pair_fish", "The fish", ""),
    ("pair_monkeys", "The monkeys", ""),
    ("pair_hominids", "The hominids", ""),
]
PLATES = [
    ("loc_kitchen", "The kitchen"),
    ("loc_cave", "The cave"),
    ("loc_museum", "The museum"),
    ("loc_savanna", "The savanna"),
]


def main():
    audio_uri = ("data:audio/mp4;base64," +
                 base64.b64encode(AUDIO.read_bytes()).decode()) if AUDIO.exists() else ""

    def anchor_card(n, t, c="", wide=False):
        p = html.escape(ANCHOR_PROMPT.get(n, ""))
        return (f'<figure class="card{" wide" if wide else ""}">'
                f'<img src="{anchor_thumb(n)}" alt="{html.escape(t)}">'
                f'<figcaption><span class="dot {c}"></span>{html.escape(t)}</figcaption>'
                f'<details class="p frame"><summary><b>anchor prompt</b></summary>'
                f'<pre>{p}</pre></details></figure>')

    cast_html = "".join(anchor_card(n, t, c) for n, t, c in CAST if anchor_thumb(n))
    plates_html = "".join(anchor_card(n, t, wide=True) for n, t in PLATES if anchor_thumb(n))

    rows = []
    n = 0
    for entry in SHOTS:
        if entry[0] == "__act":
            _, title, sub, _, _ = entry
            rows.append(
                f'<h2 class="act"><span>{html.escape(title)}</span>'
                f'<small>{html.escape(sub)}</small></h2>')
            continue
        name, tin, tout, lyric, desc = entry
        n += 1
        clip = V1 / f"{name}.mp4"
        if clip.exists():
            # muted: Seedance's own audio is discarded in the real cut. Playing a
            # clip drives the master track from this shot's in-point instead, so
            # what you hear over the picture is exactly what the film will play.
            media = (f'<video class="clip" controls muted playsinline preload="none" '
                     f'data-t="{tin}" poster="{thumb(name)}">'
                     f'<source src="outputs/video1/{name}.mp4" type="video/mp4"></video>')
        else:
            t = thumb(name)
            media = (f'<img class="frame" src="{t}" alt="{name}">' if t else
                     '<div class="pending">frame pending…</div>')
        lyr = (f'<p class="lyric">{html.escape(lyric)}</p>' if lyric else
               '<p class="lyric instr">[instrumental]</p>')
        def reflist(rs):
            return ("".join(f'<span class="ref">{html.escape(r)}</span>' for r in rs)
                    if rs else '<span class="ref none">no refs</span>')

        fprompt = html.escape(PROMPTS.get(name, ""))
        vprompt = html.escape(CLIP_PROMPT.get(name, "— not written —"))
        gdur = CLIP_DUR.get(name)
        rows.append(f"""
<section class="shot" id="{name}">
  <div class="media">{media}</div>
  <div class="meta">
    <div class="head">
      <span class="num">{n:02d}</span>
      <button class="tcbtn" data-t="{tin}">{tc(tin)}</button>
      <span class="dur">cut {tout - tin:.1f}s</span>
      <code class="slug">{name}</code>
    </div>
    {lyr}
    <p class="desc">{html.escape(desc)}</p>
    <details class="p frame">
      <summary><b>frame prompt</b> — Nano Banana Pro
        <span class="tag">{"".join("")}{len(REFS.get(name, []))} refs</span></summary>
      <div class="refs">{reflist(REFS.get(name, []))}</div>
      <pre>{fprompt}</pre>
    </details>
    <details class="p clip">
      <summary><b>clip prompt</b> — Seedance 2.0
        <span class="tag">gen {gdur}s · 480p std</span></summary>
      <div class="refs"><span class="ref start">--start-image frames/{name}.png</span>
        {reflist(CLIP_REFS.get(name, []))}</div>
      <pre>{vprompt}</pre>
    </details>
  </div>
</section>""")

    doc = f"""<!doctype html>
<meta charset="utf-8">
<title>Homo Sapien — storyboard</title>
<style>
  :root {{ --coral:#e8734a; --teal:#3f8f9d; --bg:#14110f; --card:#1e1a17;
           --ink:#f0e7dd; --dim:#a1928a; --line:#332c27; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,sans-serif; }}
  .wrap {{ max-width:1180px; margin:0 auto; padding:0 24px 120px; }}
  header {{ padding:64px 0 28px; border-bottom:1px solid var(--line); }}
  h1 {{ font-size:44px; margin:0 0 6px; letter-spacing:-.02em; }}
  h1 em {{ font-style:normal; color:var(--coral); }}
  .sub {{ color:var(--dim); margin:0; }}
  .concept {{ margin:26px 0 0; padding:20px 22px; background:var(--card);
    border-left:3px solid var(--coral); border-radius:6px; max-width:760px; }}
  .concept b {{ color:var(--coral); }}
  .motifs {{ display:flex; gap:14px; flex-wrap:wrap; margin:18px 0 0; padding:0; list-style:none; }}
  .motifs li {{ background:var(--card); border:1px solid var(--line); border-radius:20px;
    padding:6px 14px; font-size:13px; color:var(--dim); }}
  .motifs b {{ color:var(--ink); font-weight:600; }}
  h2.act {{ display:flex; align-items:baseline; gap:14px; margin:64px 0 22px;
    padding-bottom:10px; border-bottom:1px solid var(--line);
    font-size:13px; letter-spacing:.16em; text-transform:uppercase; color:var(--coral); }}
  h2.act small {{ letter-spacing:0; text-transform:none; color:var(--dim); font-size:13px; }}
  h3 {{ font-size:13px; letter-spacing:.16em; text-transform:uppercase; color:var(--dim);
    margin:40px 0 16px; }}
  .gallery {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:14px; }}
  .gallery.plates {{ grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); }}
  .card {{ margin:0; background:var(--card); border-radius:8px; overflow:hidden;
    border:1px solid var(--line); }}
  .card img {{ width:100%; display:block; aspect-ratio:3/4; object-fit:cover; }}
  .card.wide img {{ aspect-ratio:16/9; }}
  figcaption {{ padding:9px 11px; font-size:13px; color:var(--dim);
    display:flex; align-items:center; gap:7px; }}
  .dot {{ width:8px; height:8px; border-radius:50%; display:inline-block; }}
  .dot.coral {{ background:var(--coral); }} .dot.teal {{ background:var(--teal); }}
  .shot {{ display:grid; grid-template-columns:minmax(0,1.35fr) minmax(0,1fr); gap:26px;
    padding:22px 0; border-bottom:1px solid var(--line); scroll-margin-top:96px; }}
  .shot.playing {{ background:linear-gradient(90deg,rgba(232,115,74,.10),transparent 60%); }}
  .media img.frame, .media video {{ width:100%; border-radius:8px; display:block;
    background:#000; aspect-ratio:16/9; object-fit:cover; }}
  .pending {{ aspect-ratio:16/9; display:grid; place-items:center; border-radius:8px;
    background:var(--card); border:1px dashed var(--line); color:var(--dim); font-size:13px; }}
  .head {{ display:flex; align-items:center; gap:10px; margin-bottom:10px; }}
  .num {{ font:600 12px/1 ui-monospace,monospace; color:var(--bg); background:var(--dim);
    padding:5px 6px; border-radius:4px; }}
  .tcbtn {{ font:600 13px/1 ui-monospace,monospace; color:var(--coral); background:transparent;
    border:1px solid var(--line); border-radius:4px; padding:5px 8px; cursor:pointer; }}
  .tcbtn:hover {{ background:var(--coral); color:var(--bg); border-color:var(--coral); }}
  .dur {{ font:12px/1 ui-monospace,monospace; color:var(--dim); }}
  .slug {{ font:12px/1 ui-monospace,monospace; color:var(--dim); margin-left:auto; }}
  .lyric {{ margin:0 0 8px; font-size:19px; font-weight:600; letter-spacing:-.01em; }}
  .lyric.instr {{ font-weight:400; font-size:15px; color:var(--dim); font-style:italic; }}
  .desc {{ margin:0 0 12px; color:var(--dim); font-size:14.5px; }}
  .refs {{ display:flex; gap:6px; flex-wrap:wrap; margin-bottom:10px; }}
  .ref {{ font:11px/1 ui-monospace,monospace; color:var(--teal); border:1px solid var(--line);
    background:var(--card); border-radius:4px; padding:5px 7px; }}
  .ref.none {{ color:var(--line); }}
  details.p {{ margin-top:7px; border:1px solid var(--line); border-radius:6px;
    background:var(--card); overflow:hidden; }}
  details.p summary {{ cursor:pointer; padding:8px 11px; font-size:12.5px; color:var(--dim);
    display:flex; align-items:center; gap:8px; list-style:none; }}
  details.p summary::-webkit-details-marker {{ display:none; }}
  details.p summary::before {{ content:"▸"; font-size:10px; color:var(--dim); }}
  details.p[open] summary::before {{ content:"▾"; }}
  details.p.frame summary b {{ color:var(--coral); font-weight:600; }}
  details.p.clip summary b {{ color:var(--teal); font-weight:600; }}
  details.p summary .tag {{ margin-left:auto; font:11px/1 ui-monospace,monospace;
    color:var(--dim); border:1px solid var(--line); border-radius:4px; padding:4px 6px; }}
  details.p .refs {{ padding:0 11px 2px; }}
  details.p pre {{ white-space:pre-wrap; padding:2px 12px 12px; font-size:12px;
    color:var(--ink); opacity:.75; margin:0; line-height:1.5; }}
  .card details.p {{ border:0; border-top:1px solid var(--line); border-radius:0; }}
  .card details.p pre {{ font-size:11px; max-height:220px; overflow:auto; }}
  .ref.start {{ color:var(--coral); }}
  .expand {{ margin-left:auto; font:12px/1 inherit; color:var(--dim); background:transparent;
    border:1px solid var(--line); border-radius:5px; padding:8px 11px; cursor:pointer; }}
  .expand:hover {{ color:var(--ink); border-color:var(--dim); }}
  .player {{ position:sticky; top:0; z-index:10; background:rgba(20,17,15,.94);
    backdrop-filter:blur(10px); border-bottom:1px solid var(--line); padding:11px 0; }}
  .player .inner {{ max-width:1180px; margin:0 auto; padding:0 24px;
    display:flex; align-items:center; gap:14px; }}
  .player audio {{ flex:1; height:34px; }}
  .player .hint {{ font-size:12.5px; color:var(--dim); }}
  @media (max-width:820px) {{ .shot {{ grid-template-columns:1fr; }} }}
</style>

<div class="player"><div class="inner">
  <audio id="song" controls src="{audio_uri}"></audio>
  <span class="hint">click a timecode to jump the song · play a clip and the song
    plays over it from that shot's in-point</span>
  <button class="expand" id="expandall">expand all prompts</button>
</div></div>

<div class="wrap">
<header>
  <h1>Be my <em>Homo Sapien</em></h1>
  <p class="sub">Lenka — <i>Attune</i> (2017) · 3:59 · music video storyboard ·
     {sum(1 for e in SHOTS if e[0] != "__act")} shots · all frames Nano Banana Pro</p>
  <div class="concept">
    <p style="margin:0"><b>The Same Two.</b> Every stage of the universe is <i>them</i>. Two sparks
    off the Big Bang, two stars in a binary, two blobs in a tidepool the size of a soup bowl, two
    fish, two monkeys, two hominids, and two people doing a terrible dance in a kitchen at 1am —
    the same pair of souls, reincarnating up the tree of life, always finding each other, always a
    little bit useless at it, always in love. Sincere about the love, silly about the evolution:
    the cosmic scale is the joke, the couple is the point.</p>
    <ul class="motifs">
      <li><b>The forehead touch</b> — every incarnation does it</li>
      <li><b>Coral + teal</b> — how you know which two are them</li>
      <li><b>Two handprints</b> — ochre at 1:36, museum glass at 3:22, poster paint at 3:38</li>
    </ul>
  </div>
</header>

<h3>Cast</h3>
<div class="gallery">{cast_html}</div>
<h3>Plates</h3>
<div class="gallery plates">{plates_html}</div>

{"".join(rows)}
</div>

<script>
  const song = document.getElementById('song');
  document.querySelectorAll('.tcbtn').forEach(b => b.onclick = () => {{
    song.currentTime = parseFloat(b.dataset.t); song.play();
  }});
  // highlight the shot the song is currently inside
  const marks = [...document.querySelectorAll('.shot')].map(s => ({{
    el: s, t: parseFloat(s.querySelector('.tcbtn').dataset.t)
  }}));
  song.addEventListener('timeupdate', () => {{
    let cur = null;
    for (const m of marks) if (song.currentTime >= m.t) cur = m;
    marks.forEach(m => m.el.classList.toggle('playing', m === cur));
  }});
  // Playing a clip plays THE SONG over it, from that shot's in-point — the clip's
  // own Seedance audio is muted and never used in the cut. Only one at a time.
  const clips = document.querySelectorAll('video.clip');
  clips.forEach(v => {{
    v.addEventListener('play', () => {{
      clips.forEach(o => {{ if (o !== v) o.pause(); }});
      song.currentTime = parseFloat(v.dataset.t) + v.currentTime;
      song.play();
    }});
    v.addEventListener('seeked', () => {{
      if (!v.paused) song.currentTime = parseFloat(v.dataset.t) + v.currentTime;
    }});
    v.addEventListener('pause', () => song.pause());
    v.addEventListener('ended', () => song.pause());
  }});
  const btn = document.getElementById('expandall');
  btn.onclick = () => {{
    const ds = document.querySelectorAll('details.p');
    const open = ![...ds].every(d => d.open);
    ds.forEach(d => d.open = open);
    btn.textContent = open ? 'collapse all prompts' : 'expand all prompts';
  }};
</script>
"""
    out = PROJ / "storyboard.html"
    out.write_text(doc)
    print(out)


if __name__ == "__main__":
    main()
