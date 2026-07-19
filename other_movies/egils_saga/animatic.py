#!/usr/bin/env python3
"""Animatic for EGIL: start frames + full ElevenLabs voice track, no Seedance.

Usage: python3 animatic.py            # TTS all lines (skip existing) + render
       python3 animatic.py render     # re-render only (after editing timings)

Writes animatic_audio/<shot>_<i>_<speaker>.mp3, animatic_segs/<shot>.mp4,
and animatic_v1.mp4. Cheap iteration loop: edit SCRIPT, re-run.
"""
import json
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
AUD = HERE / "animatic_audio"
SEGS = HERE / "animatic_segs"
AUD.mkdir(exist_ok=True)
SEGS.mkdir(exist_ok=True)
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()

OUT = HERE / "animatic_v1.mp4"
W_, H_ = 1280, 720
FPS = 24
HEAD, GAP, TAIL = 0.8, 0.5, 1.4   # silence padding (s)

# ---- animatic voice cast (all ElevenLabs; director's first picks) ----
VOICES = {
    "narrator":   ("tJDFCHyviItsYF1qqToS", 0.55, 0.15),  # LeifNordic
    "egil":       ("ljo9gAlSqKOvF6D8sOsX", 0.45, 0.40),  # VikingBjorn
    "egil_child": ("cgSgspJ2msm6clMCkdW9", 0.45, 0.45),  # Jessica (boy read)
    "skallagrim": ("nPczCjzI2devNBz1zQrb", 0.55, 0.25),  # Brian
    "kveldulf":   ("pqHfZKP75CvOlQylNhV4", 0.55, 0.30),  # Bill
    "thorolf":    ("SOYHLrjzK2X1ezoPC6cr", 0.45, 0.45),  # Harry
    "harald":     ("pNInz6obpgDQGcFmaJgB", 0.55, 0.30),  # Adam
    "eirik":      ("KTAbPR4QFlhaTpde6md8", 0.45, 0.45),  # Bloodgrin
    "gunnhild":   ("Qbw4VpyUrHEG7NigKzty", 0.45, 0.50),  # KristenQueen
    "arinbjorn":  ("onwK4e9ZLuTAKqWW03F9", 0.55, 0.25),  # Daniel
    "thorgerd":   ("pFZP5JQG7iQjIQuC4Bku", 0.45, 0.40),  # Lily
    "thordis":    ("XrExE9yKIg1WjnnlVkGX", 0.45, 0.45),  # Matilda
    "bera":       ("EXAVITQu4vr4xnSDxMaL", 0.50, 0.35),  # Sarah
    "brak":       ("Xb7hH8MSUJpSbSDYk0k2", 0.40, 0.55),  # Alice
    "harek":      ("N2lVS1w4EtoT3dr4eOWO", 0.45, 0.50),  # Callum
}

# ---- script: (shot, [(speaker, line), ...], min_dur_for_silent) ----
SCRIPT = [
    ("title", [], 4.0),
    ("p1", [("narrator",
             "They called him Kveldulf — the Evening-Wolf. Each day as the "
             "sun went down he grew sullen, and no man could speak with him. "
             "It was said... he was shape-strong.")], 0),
    ("p2", [("kveldulf",
             "Say this to your king: Kveldulf will sit at home. I think he "
             "has a whole load of good fortune... where our king has not a "
             "handful.")], 0),
    ("p3", [("thorolf", "I am resolved to seek the king, and become his man."),
            ("kveldulf",
             "My foreboding is that we shall reap ruin from that king. "
             "Beware — keep within bounds, nor rival thy betters.")], 0),
    ("p4", [("narrator",
             "Thorolf feasted the king with five hundred men — where the "
             "king brought three hundred. Kings do not forgive "
             "arithmetic.")], 0),
    ("p5", [("harek",
             "He keeps a guard round him like a king. Keep Thorolf near "
             "thee, lord — that he make not himself too great for "
             "thee.")], 0),
    ("p6", [("thorolf", "Now am I but three feet short of my aim!")], 0),
    ("p7", [("kveldulf",
             "It is an old saw: he will be avenged who falls forward. But "
             "vengeance will not be mine. My sons must sail. There is new "
             "land found — westward. ... Iceland.")], 0),
    ("p8", [("kveldulf",
             "Make me a coffin, and put me overboard. It will go far "
             "otherwise than I think... if I do not come to Iceland, and "
             "take land there.")], 0),
    ("p9", [("narrator",
             "The dead man chose the land. They built at Borg — and there "
             "the story truly begins.")], 0),
    ("a1", [("narrator",
             "Skallagrim had two sons. Thorolf, fair and beloved. And Egil: "
             "black-haired, ugly, and already too big. At three he was "
             "strong as a boy of seven — and he made verses.")], 0),
    ("a2", [("egil_child",
             "Hasting I came to the hearth-fire of Yngvar, him who on "
             "heroes bestoweth gold. Thou wilt not find a doughtier "
             "song-smith... of three winters!")], 0),
    ("a3", [("bera", "You have the makings of a freebooter, my son."),
            ("egil_child",
             "Thus counselled my mother: for me shall they purchase a "
             "galley and good oars. So may I, high-standing, hew down many "
             "foemen.")], 0),
    ("a4", [("brak",
             "Dost thou turn thy shape-strength, Skallagrim — against thy "
             "son?")], 0),
    ("a5", [("narrator",
             "That evening, Egil killed the man his father loved best. They "
             "did not speak all winter. In that family, grief was paid in "
             "kind.")], 0),
    ("b1", [("narrator",
             "Grown, Egil went east — and made an enemy of a queen. "
             "Gunnhild: beautiful, shrewd, and of magic cunning.")], 0),
    ("b2", [("egil",
             "Write we runes around the horn, redden all the spell with "
             "blood. Learn that health abides in ale — holy ale... that "
             "Bard hath blessed.")], 0),
    ("b3", [("narrator",
             "Bard fell dead in his own doorway. And the king's hunt "
             "began.")], 0),
    ("b4", [], 5.0),
    ("b5", [("gunnhild",
             "Thou lendest easy ear to talk. Egil has slain thy friends and "
             "thy steward — I reckon no odds between him and his brother."),
            ("eirik",
             "Egil shall not be long harboured in my realm.")], 0),
    ("c1", [("narrator",
             "The brothers took service with Athelstan of England, against "
             "Olaf king of Scots. Athelstan bought a week with empty tents "
             "and false envoys. Then the armies met, at Vinheath.")], 0),
    ("c2", [("egil", "I will not that I and Thorolf be parted in the battle."),
            ("thorolf",
             "Brother, you will have your way — but it is the king's array."),
            ("egil", "This separation... I shall often rue.")], 0),
    ("c3", [], 5.0),
    ("c4", [("narrator",
             "Egil took Earl Adils' life, and the day turned. Athelstan won "
             "England's greatest victory. It cost Egil his brother.")], 0),
    ("c5", [("egil",
             "Green grows on soil of Vinheath, grass o'er my noble brother. "
             "But we our woe — a sorrow worse than death-pang — must "
             "bear.")], 0),
    ("c6", [], 11.0),
    ("d1", [("egil",
             "Then I ban these lands! I denounce him who holds them: "
             "law-breaker, peace-breaker... and accursed!")], 0),
    ("d2", [("egil",
             "Here set I up a curse-pole, and this curse I turn on King "
             "Eirik and Queen Gunnhild — and on the land-spirits of this "
             "land: may they all wander astray, and never find their home, "
             "till they have driven King Eirik and Gunnhild from the "
             "land.")], 0),
    ("d3", [("narrator",
             "The curse worked. Eirik was driven from Norway — to England, "
             "where Athelstan gave him York to hold. And Gunnhild worked a "
             "spell of her own: that Egil should find no rest till she had "
             "seen him. His ship broke at Humber-mouth — in Eirik "
             "Bloodaxe's new kingdom.")], 0),
    ("d4", [("arinbjorn",
             "Egil. There is nothing for it now. You shall bring the king "
             "your head — and I will be your spokesman.")], 0),
    ("d5", [("gunnhild",
             "Why is Egil not slain at once? Have you forgotten, king, what "
             "he has done — your friends, your kin... your own son?"),
            ("arinbjorn",
             "Night-slaying is murder, king. Give him till morning. If he "
             "has spoken evil of thee, he can atone — in words of praise "
             "that shall live for all time.")], 0),
    ("d6", [], 6.0),
    ("d7", [("egil",
             "Westward I sailed the wave; within me Odin gave the sea of "
             "song I bear. My mind a galleon, fraught with load of minstrel "
             "thought. ... Glory and fame... gat Eirik's name.")], 0),
    ("d8", [("eirik",
             "The poem is well delivered. I give thee now thy head — this "
             "time — because thou camest freely into my power. But know "
             "this for sure: it is no reconciliation."),
            ("narrator",
             "So Egil bought his head with a poem. The Head-Ransom, men "
             "call it, to this day.")], 0),
    ("e1", [("narrator",
             "Egil went home to Borg, and grew old, and had sons. Bodvar "
             "was the best of them — fair, like the Thorolfs. He was "
             "seventeen when the boat went down.")], 0),
    ("e2", [], 8.0),
    ("e3", [("narrator",
             "He locked himself in his bed-closet, and would take neither "
             "food nor drink. He meant to die. Three days. Then his "
             "daughter came.")], 0),
    ("e4", [("thorgerd",
             "Father, open the door. I will that we both travel the same "
             "road."),
            ("egil", "We are deceived. ... This is milk.")], 0),
    ("e5", [("thorgerd",
             "Then let us lengthen our lives, father — long enough that you "
             "make a funeral poem, on Bodvar."),
            ("egil",
             "Much doth it task me... my tongue to move. ... Me Ran, the "
             "sea-queen, roughly hath shaken: I stand of beloved ones... "
             "stript, and all bare.")], 0),
    ("e6", [("egil",
             "The god broke faith and friendship, false in my need — yet he "
             "gave me poesy faultless... boot for bale. And on Digra-ness, "
             "Hel waits. Dauntless in bearing... her death-blow I bide."),
            ("narrator",
             "The Sonatorrek — the Loss of Sons. The poem brought him back. "
             "Odin took his sons, and paid him in verse.")], 0),
    ("e7", [("egil",
             "Blind near the blaze I wander, and beg the fire-maid's "
             "pardon. Yet England's mighty monarch... me whilom greatly "
             "honoured — and princes once with pleasure the poet's accents "
             "heard.")], 0),
    ("e8", [("egil",
             "I mean to carry Athelstan's silver to the Hill of Laws — and "
             "sow it broadcast into the biggest crowd of the Thing. Kicks "
             "there will be, I fancy, and blows. Nay — it may end in a "
             "general fight of all the assembled Thing."),
            ("thordis",
             "A famous plan! It will be remembered as long as Iceland is "
             "inhabited.")], 0),
    ("e9", [("narrator",
             "One night the silver went into the earth instead — and the "
             "two thralls with it. Blind, in his ninth decade, he killed "
             "his last two men. English pennies still wash out of the gill "
             "after thaws. The hoard has never been found.")], 0),
    ("e10", [("narrator",
              "When they moved the bones, the skull would not break. Heavy, "
              "and wave-marked, like a shell. It was a hard head to take... "
              "alive or dead. And so ends this story.")], 0),
]


def tts(dest: Path, speaker: str, text: str) -> str:
    if dest.exists():
        return f"skip {dest.name}"
    vid, stability, style = VOICES[speaker]
    body = json.dumps({
        "text": text, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": stability, "similarity_boost": 0.75,
                           "style": style, "use_speaker_boost": True},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}",
        data=body, method="POST",
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    err = "?"
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                dest.write_bytes(r.read())
            return f"OK   {dest.name}"
        except Exception as e:  # noqa: BLE001
            err = str(e)
    return f"FAIL {dest.name}: {err[:120]}"


def dur_of(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def line_files(shot: str, lines) -> list[Path]:
    return [AUD / f"{shot}_{i}_{spk}.mp3" for i, (spk, _t) in enumerate(lines)]


def render_segment(shot: str, lines, min_dur: float) -> Path:
    frame = HERE / "frames" / f"{shot}.png"
    seg = SEGS / f"{shot}.mp4"
    vf = (f"scale={W_}:{H_}:force_original_aspect_ratio=increase,"
          f"crop={W_}:{H_},setsar=1,fps={FPS}")
    files = line_files(shot, lines)
    if lines:
        durs = [dur_of(f) for f in files]
        total = HEAD + sum(durs) + GAP * (len(durs) - 1) + TAIL
        total = max(total, min_dur, 4.0)
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", f"{total:.2f}",
               "-i", str(frame)]
        for f in files:
            cmd += ["-i", str(f)]
        fc = []
        chain = []
        fc.append(f"aevalsrc=0:d={HEAD}:s=44100[g0]")
        chain.append("[g0]")
        for i in range(len(files)):
            fc.append(f"[{i+1}:a]aresample=44100,aformat=channel_layouts=mono[a{i}]")
            chain.append(f"[a{i}]")
            if i < len(files) - 1:
                fc.append(f"aevalsrc=0:d={GAP}:s=44100[g{i+1}]")
                chain.append(f"[g{i+1}]")
        fc.append("".join(chain) + f"concat=n={len(chain)}:v=0:a=1,"
                  f"apad,atrim=0:{total:.2f}[aout]")
        cmd += ["-filter_complex", ";".join(fc), "-map", "0:v",
                "-map", "[aout]", "-vf", vf]
    else:
        total = max(min_dur, 4.0)
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", f"{total:.2f}",
               "-i", str(frame), "-f", "lavfi", "-t", f"{total:.2f}",
               "-i", "anullsrc=r=44100:cl=mono",
               "-map", "0:v", "-map", "1:a", "-vf", vf]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            "-ar", "44100", str(seg)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"segment {shot} failed:\n{r.stderr[-800:]}")
    print(f"seg {shot:6s} {total:5.1f}s", flush=True)
    return seg


def main():
    render_only = len(sys.argv) > 1 and sys.argv[1] == "render"
    if not render_only:
        jobs = [(AUD / f"{shot}_{i}_{spk}.mp3", spk, text)
                for shot, lines, _md in SCRIPT
                for i, (spk, text) in enumerate(lines)]
        with ThreadPoolExecutor(max_workers=4) as pool:
            for res in pool.map(lambda j: tts(*j), jobs):
                print(res, flush=True)
        missing = [j[0].name for j in jobs if not j[0].exists()]
        if missing:
            sys.exit(f"missing audio, aborting render: {missing}")

    segs = [render_segment(shot, lines, md) for shot, lines, md in SCRIPT]
    lst = SEGS / "concat.txt"
    lst.write_text("".join(f"file '{s.resolve()}'\n" for s in segs))
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat",
                        "-safe", "0", "-i", str(lst), "-c", "copy", str(OUT)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"concat failed:\n{r.stderr[-800:]}")
    print("wrote", OUT, f"({dur_of(OUT):.0f}s)")


if __name__ == "__main__":
    main()
