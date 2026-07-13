#!/usr/bin/env python3
"""Build the White Company animatic: storyboard frames + ElevenLabs dialogue.

Usage: python3 make_animatic.py tts     # generate vo/ line mp3s (skips existing)
       python3 make_animatic.py build   # encode segments + concat -> outputs/animatic_v1.mp4
       python3 make_animatic.py all

Chosen cast lives in CAST below (audition winners per casting.html). Library
voices are added to the account and KEPT (they are the picked cast).
"""
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from vo_casting import VOICES, api, owner_id

PROJ = Path(__file__).parent
VO = PROJ / "vo"
SEG = PROJ / "outputs" / "animatic_segs"
OUTMP4 = PROJ / "outputs" / "animatic_v1.mp4"

# speaker -> voice slug (see VOICES in vo_casting.py)
CAST = {
    "ALLEYNE": "ethan", "NIGEL": "henry", "AYLWARD": "gideon", "JOHN": "sebastian",
    "MAUDE": "mia", "LADY_MARY": "jan", "DUGUESCLIN": "dracon", "TIPHAINE": "sandy",
    "PRINCE": "cassius", "CHANDOS": "alistair", "OLIVER": "raymond", "SIMON": "sterling",
    "ABBOT": "ak", "HAWTAYNE": "john_north", "LATOUR": "blackwood", "BURLEY": "steve",
    "CALVERLEY": "adam", "STOUTLADY": "enid", "LIMNER": "steve", "CHORUS": "gideon",
}

# shot -> ordered (speaker, line) pairs; shots absent here are visual-only
LINES = {
    "a2_trial": [
        ("ABBOT", "What talk is this? Is this a tongue to be used within the walls of an old and well-famed monastery?"),
        ("JOHN", "By the black rood of Waltham! If any knave among you lays a finger-end upon the edge of my gown, I will crush his skull like a filbert!")],
    "a4_farewell": [
        ("ABBOT", "Thy father willed it: one year in the world, and then choose between cloister and mankind."),
        ("ALLEYNE", "I shall come back to you, father.")],
    "a5_merlin": [
        ("JOHN", "I shall stand by him, and he shall neither be put out on the road, nor shall his ears be offended indoors."),
        ("JOHN", "Hush, lad... I count them not a fly.")],
    "a6_aylward": [
        ("AYLWARD", "By my hilt! camarades, there is no drop of French blood in my body, and I am a true English bowman, Samkin Aylward by name."),
        ("AYLWARD", "To Sir Claude Latour, and the White Company!")],
    "a7_song": [
        ("CHORUS", "So we'll drink all together, to the gray goose feather! And the land where the gray goose flew!")],
    "a8_wrestle": [
        ("AYLWARD", "By my hilt! then, I have found a man at last!"),
        ("LIMNER", "'Ware the ale! Oh, holy Virgin, 'ware the ale!")],
    "a9_rescue": [
        ("ALLEYNE", "Brother or no, I swear by my hopes of salvation that I will break your arm if you do not leave hold of the maid.")],
    "a10_bank": [
        ("MAUDE", "You had him at your mercy. Why did you not kill him?"),
        ("ALLEYNE", "Kill him! My brother!"),
        ("MAUDE", "He would have killed you. I know him, and I read it in his eyes.")],
    "b1_stone": [
        ("NIGEL", "I fear that I overtask you, for it is of a grievous weight."),
        ("NIGEL", "Good lack!"),
        ("LADY_MARY", "Good lack!")],
    "b2_bear": [
        ("NIGEL", "Ah, saucy! saucy."),
        ("JOHN", "I was a fool not to know that a little rooster may be the gamest.")],
    "b3_hall": [
        ("MAUDE", "Ma foi! and here is our wandering clerk."),
        ("NIGEL", "By Saint Paul! it is a very honorable venture. Alleyne Edricson, you shall ride as my squire.")],
    "b4_veil": [
        ("ALLEYNE", "You are my heart, my life, my one and only thought."),
        ("MAUDE", "Win my father's love... and all may follow.")],
    "b5_march": [
        ("NIGEL", "Your glove, my life's desire! I shall proclaim you the fairest and sweetest in Christendom, and joust with any who deny it.")],
    "c1_sail": [
        ("HAWTAYNE", "I like it not. And yet Goodwin Hawtayne is not the man to stand back when his fellows are for pressing forward.")],
    "c2_ruse": [
        ("NIGEL", "Ma foi! but they come to our lure like chicks to the fowler. To your arms, men! Now blow out the trumpets, and may God's benison be with the honest men!")],
    "c3_melee": [
        ("JOHN", "My God, but it is a noble fight!"),
        ("JOHN", "Ah, by Our Lady! His sword is through him! Down goes the red cross, and up springs Simon with the scarlet roses!")],
    "d1_patch": [
        ("NIGEL", "I vow that I will not take this patch from my eye until I have seen something of this country of Spain."),
        ("AYLWARD", "There will come bloodshed of that patch, or I am the more mistaken.")],
    "d2_chandos": [
        ("CHANDOS", "Ha, my little heart of gold! Since you have tied up one of your eyes, and I have had the mischance to lose one of mine, we have but a pair between us.")],
    "d3_prince": [
        ("NIGEL", "It is a very small matter that I should be hanged, but it would be a very grievous thing that you should make a vow and fail to bring it to fulfilment."),
        ("PRINCE", "Peace! Peace! I am very well able to look to my own vows and their performance.")],
    "d4_tourney": [
        ("PRINCE", "Who comes next for England, John?"),
        ("CHANDOS", "Sir Nigel Loring of Hampshire, sire.")],
    "d5_stranger": [
        ("DUGUESCLIN", "I will neither drink your wine nor sit at your table. I bear no love for you, or for your race."),
        ("PRINCE", "By Saint George! He has served his master this day, even as I would wish liegeman of mine to serve me.")],
    "e2_inn": [
        ("DUGUESCLIN", "Dogs of England! Must ye be lashed hence? Tiphaine... my sword!"),
        ("DUGUESCLIN", "Mort Dieu! It is my little swordsman of Bordeaux!"),
        ("NIGEL", "Bertrand! Bertrand du Guesclin!")],
    "e3_prophecy": [
        ("TIPHAINE", "Danger, Bertrand. Deadly, pressing danger... which creeps upon you, and you know it not."),
        ("DUGUESCLIN", "But is this so very close, Tiphaine?"),
        ("TIPHAINE", "Here. Now. Close upon you!")],
    "e4_night": [
        ("ALLEYNE", "Seventy... and nine. My God! What has come upon us?")],
    "e5_hall": [
        ("DUGUESCLIN", "France and England will fight together this night."),
        ("NIGEL", "There are many ways in which a man might die, but none better than this.")],
    "e6_keep": [
        ("AYLWARD", "By my hilt! Up, up, mes enfants!")],
    "e7_powder": [
        ("NIGEL", "Throw back the lid, John, and drop the box into the fire!")],
    "e8_song": [
        ("TIPHAINE", "Hush... and listen! I have heard the voices of men, all singing together in a strange tongue."),
        ("AYLWARD", "By these ten finger-bones... we are saved! It is the marching song of the White Company. Hush!"),
        ("CHORUS", "We'll drink all together, to the gray goose feather, and the land where the gray goose flew...")],
    "e9_tree": [
        ("NIGEL", "I have lived in honor, and in honor I trust that I shall die."),
        ("LATOUR", "I will not go to Dax."),
        ("JOHN", "The proper life for a robber!")],
    "f1_pass": [
        ("SIMON", "Yonder... is where Roland fell.")],
    "f2_volunteers": [
        ("NIGEL", "That I should live to see the day! What! Not one——"),
        ("ALLEYNE", "My fair lord... they have all stepped forward."),
        ("OLIVER", "And I come also."),
        ("NIGEL", "For honor?"),
        ("OLIVER", "For pullets.")],
    "f3_raid": [
        ("NIGEL", "I have come for the king; and, by Saint Paul! he must back with us, or I must bide here.")],
    "f4_mist": [
        ("NIGEL", "Now order the ranks, and fling wide the banners! For our souls are God's, and our bodies the king's, and our swords for Saint George and for England!")],
    "f5_duel": [
        ("NIGEL", "I think that I am now clear of my vow, for this Spanish knight was a person from whom much honor might be won.")],
    "f6_storm": [
        ("AYLWARD", "Johnston!"),
        ("AYLWARD", "Loose steady, mes garcons. Every shaft well sent.")],
    "f7_stand": [
        ("BURLEY", "Might we not even now make a retreat?"),
        ("NIGEL", "My soul will retreat from my body first! Here I am, and here I bide, while God gives me strength to lift a sword.")],
    "f8_cliff": [
        ("ALLEYNE", "I pray you, my dear lord, that you will give my humble service to the Lady Maude, and say to her that I was ever her true servant, and most unworthy cavalier."),
        ("NIGEL", "Now may God speed ye... for ye are brave and worthy men.")],
    "f9_after": [
        ("ALLEYNE", "Tell me, John... where is my dear lord, Sir Nigel Loring?"),
        ("JOHN", "He is dead, I fear. I saw them throw his body across a horse, and ride away with it."),
        ("CALVERLEY", "Nay... the White Company is here disbanded.")],
    "g1_news": [
        ("STOUTLADY", "News hath come that not one of the Company was left alive; and so, poor lamb, she takes the veil at Romsey this very day."),
        ("ALLEYNE", "Lady! Is it the Lady Maude Loring of whom you speak? ...And I stand talking here! Come, John, come!")],
    "g2_nunnery": [
        ("ALLEYNE", "Maude! The Company fell — but I live... and I am come for you.")],
    "g3_inn": [
        ("AYLWARD", "Ah, mes belles! I have been among the black paynim, and, by my hilt! it does me good to look at your English cheeks."),
        ("NIGEL", "Tell him that a very humble knight of England abides here; so that if he be in need of advancement, or have any small vow upon his soul, or desire to exalt his lady, I may help him to accomplish it.")],
    "g4_end": [
        ("CHORUS", "So we'll drink all together, to the gray goose feather... and the land where the gray goose flew.")],
}

# cut order: (name, kind, fallback duration for visual-only shots)
ORDER = [
    ("t_title", "card", 3.5), ("t_1366", "card", 2.5),
    ("a1_bell", "frame", 6), ("a2_trial", "frame", 0), ("a3_flight", "frame", 6),
    ("a4_farewell", "frame", 0), ("a5_merlin", "frame", 0), ("a6_aylward", "frame", 0),
    ("a7_song", "frame", 0), ("a8_wrestle", "frame", 0), ("a9_rescue", "frame", 0),
    ("a10_bank", "frame", 0),
    ("b1_stone", "frame", 0), ("b2_bear", "frame", 0), ("b3_hall", "frame", 0),
    ("b4_veil", "frame", 0), ("b5_march", "frame", 0),
    ("c1_sail", "frame", 0), ("c2_ruse", "frame", 0), ("c3_melee", "frame", 0),
    ("d1_patch", "frame", 0), ("d2_chandos", "frame", 0), ("d3_prince", "frame", 0),
    ("d4_tourney", "frame", 0), ("d5_stranger", "frame", 0),
    ("t_france", "card", 2.5),
    ("e1_road", "frame", 7), ("e2_inn", "frame", 0), ("e3_prophecy", "frame", 0),
    ("e4_night", "frame", 0), ("e5_hall", "frame", 0), ("e6_keep", "frame", 0),
    ("e7_powder", "frame", 0), ("e8_song", "frame", 0), ("e9_tree", "frame", 0),
    ("t_spain", "card", 2.5),
    ("f1_pass", "frame", 0), ("f2_volunteers", "frame", 0), ("f3_raid", "frame", 0),
    ("f4_mist", "frame", 0), ("f5_duel", "frame", 0), ("f6_storm", "frame", 0),
    ("f7_stand", "frame", 0), ("f8_cliff", "frame", 0), ("f9_after", "frame", 0),
    ("t_home", "card", 2.5),
    ("g1_news", "frame", 0), ("g2_nunnery", "frame", 0), ("g3_inn", "frame", 0),
    ("g4_end", "frame", 0),
]

LEAD, GAP, TAIL = 0.6, 0.45, 0.8


def dur_of(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def tts_phase():
    VO.mkdir(exist_ok=True)
    mine = {v["voice_id"] for v in api("/voices")["voices"]}
    for shot, lines in LINES.items():
        for i, (spk, text) in enumerate(lines):
            dest = VO / f"{shot}_{i}_{spk.lower()}.mp3"
            if dest.exists():
                continue
            name, vid, src = VOICES[CAST[spk]]
            if vid not in mine:
                oid = owner_id(name, vid)
                api(f"/voices/add/{oid}/{vid}", "POST",
                    {"new_name": f"wc_{CAST[spk]}"})
                mine.add(vid)
                print(f"added {CAST[spk]} to account (kept - chosen cast)")
            body = api(f"/text-to-speech/{vid}", "POST",
                       {"text": text, "model_id": "eleven_multilingual_v2"}, raw=True)
            dest.write_bytes(body)
            print(f"ok   {dest.name} ({len(body)//1024} KB)")
            time.sleep(0.4)


def build_phase():
    SEG.mkdir(parents=True, exist_ok=True)
    seg_files = []
    for idx, (name, kind, fallback) in enumerate(ORDER):
        img = PROJ / ("cards" if kind == "card" else "frames") / f"{name}.png"
        seg = SEG / f"{idx:02d}_{name}.mp4"
        seg_files.append(seg)
        if seg.exists():
            continue
        lines = LINES.get(name, [])
        mp3s = [VO / f"{name}_{i}_{spk.lower()}.mp3" for i, (spk, _) in enumerate(lines)]
        durs = [dur_of(m) for m in mp3s]
        total = (LEAD + sum(durs) + GAP * max(0, len(durs) - 1) + TAIL) if durs \
            else fallback
        total = max(total, 2.0)
        n = int(round(total * 24))
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(img)]
        for m in mp3s:
            cmd += ["-i", str(m)]
        # gentle push-in on frames, static cards
        if kind == "card":
            vf = (f"[0]scale=1280:720:force_original_aspect_ratio=decrease,"
                  f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,"
                  f"loop=loop={n}:size=1:start=0,fps=24,format=yuv420p[v]")
        else:
            vf = (f"[0]scale=2560:1440:force_original_aspect_ratio=increase,"
                  f"crop=2560:1440,zoompan=z='1+0.08*on/{n}':d={n}:"
                  f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=24,"
                  f"format=yuv420p[v]")
        af = f"aevalsrc=0|0:s=48000:d={LEAD}[l];"
        parts = "[l]"
        for i in range(len(mp3s)):
            af += f"[{i + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo[a{i}];"
            parts += f"[a{i}]"
            if i < len(mp3s) - 1:
                af += f"aevalsrc=0|0:s=48000:d={GAP}[g{i}];"
                parts += f"[g{i}]"
        af += f"aevalsrc=0|0:s=48000:d={TAIL}[t];"
        parts += "[t]"
        af += f"{parts}concat=n={len(mp3s) * 2 + 1 if mp3s else 2}:v=0:a=1[a]"
        if not mp3s:
            af = f"aevalsrc=0|0:s=48000:d={total}[a]"
        cmd += ["-filter_complex", vf + ";" + af, "-map", "[v]", "-map", "[a]",
                "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "19", "-c:a", "aac", "-ar", "48000",
                str(seg)]
        subprocess.run(cmd, check=True)
        print(f"seg  {seg.name} ({total:.1f}s)")
    listing = SEG / "concat.txt"
    listing.write_text("".join(f"file '{s.resolve()}'\n" for s in seg_files))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-c", "copy", str(OUTMP4)], check=True)
    print(f"wrote {OUTMP4} ({dur_of(OUTMP4):.0f}s)")


if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    if phase in ("tts", "all"):
        tts_phase()
    if phase in ("build", "all"):
        build_phase()
