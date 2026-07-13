#!/usr/bin/env python3
"""Build animatic_v1.mp4: storyboard frames + full ElevenLabs dialogue/VO track.
Per-line mp3s cached in vo_lines/ (idempotent); per-shot segments in animatic_segs/;
final concat at donner_party/animatic_v1.mp4. Rerun after editing LINES or swapping
a frame — delete the affected vo_lines/segment files to force regeneration."""
import json
import subprocess
import urllib.request
from pathlib import Path

PROJ = Path(__file__).parent
FRAMES = PROJ / "frames"
VOL = PROJ / "vo_lines"
SEGS = PROJ / "animatic_segs"
VOL.mkdir(exist_ok=True)
SEGS.mkdir(exist_ok=True)
KEY = Path.home().joinpath(".elevenlabs_key").read_text().strip()

# primary cast picks (see casting.html)
VOICE = {
    "VIRGINIA": "cgSgspJ2msm6clMCkdW9",   # Jessica
    "VO":       "cgSgspJ2msm6clMCkdW9",   # Jessica (Virginia's letter)
    "REED":     "pNInz6obpgDQGcFmaJgB",   # Adam
    "MARGARET": "XrExE9yKIg1WjnnlVkGX",   # Matilda
    "GEORGE":   "pqHfZKP75CvOlQylNhV4",   # Bill
    "TAMSEN":   "pFZP5JQG7iQjIQuC4Bku",   # Lily
    "STANTON":  "iP95p4xoKVk53GoZ742B",   # Chris
    "BREEN":    "JBFqnCBsd6RMkjVDRZzb",   # George (storyteller)
    "KESEBERG": "N2lVS1w4EtoT3dr4eOWO",   # Callum
    "EDDY":     "nPczCjzI2devNBz1zQrb",   # Brian
    "MARY":     "EXAVITQu4vr4xnSDxMaL",   # Sarah
    "MURPHY":   "hpp4J3VqNfWAUOO0d1Us",   # Bella
    "CLYMAN":   "CwhRBWXzGAHq8TQ4Fs17",   # Roger
    "GRAVES":   "lwGnQIn0Z9pl1SoUiXZ3",   # BrianRaspy
    "SUTTER":   "MJyi2qJnZ6cONaNAgdKu",   # Kevin Elliott
    "MOTHER":   "hpp4J3VqNfWAUOO0d1Us",   # Bella (one line, c2)
    "PATTY":    "FGY2WhTYpPnrIDTdsKH5",   # Laura (closest to a child on roster)
    "GIRLS":    "FGY2WhTYpPnrIDTdsKH5",   # Laura
    "MEN":      "cjVigY5qzO86Huf0OWal",   # Eric (crowd shout)
    "RESCUER":  "cjVigY5qzO86Huf0OWal",   # Eric
    "FALLON":   "cjVigY5qzO86Huf0OWal",   # Eric
}

# (shot, frame, planned_dur, [(speaker, line), ...])
SHOTS = [
    ("t_title", "t_title", 4, []),
    ("v0_letter", "f_v0_letter", 8, [
        ("VO", "My dear cousin. I take this opportunity to write to you, to let you know that we are all well at present... and to tell you what trouble is.")]),
    ("t_date1", "t_date1", 3, []),
    ("a1_departure", "f_a1_departure", 8, [
        ("VO", "We set out in April, as fine an outfit as ever crossed the plains. Papa built mama a wagon with a stove in it. Folks called it the Pioneer Palace.")]),
    ("a2_prairie", "f_a2_prairie", 8, [
        ("TAMSEN", "Everything is new and pleasing. I never could have believed we could travel so far with so little difficulty."),
        ("GEORGE", "Write that down twice, Mrs. Donner.")]),
    ("a3_warning", "f_a3_warning", 10, [
        ("CLYMAN", "Take the regular wagon track, and never leave it. It is barely possible to get through if you follow it... and it may be impossible if you don't."),
        ("REED", "There is a nearer route. It is of no use to take so roundabout a course.")]),
    ("a4_vote", "f_a4_vote", 8, [
        ("MEN", "Donner! George Donner for captain!"),
        ("TAMSEN", "We are leaving a known road... on the word of a man none of us has ever met.")]),
    ("a5_bridger", "f_a5_bridger", 6, [
        ("REED", "He will meet us at the mountains.")]),
    ("b1_wasatch", "f_b1_wasatch", 10, [
        ("STANTON", "Two miles. We made two miles today."),
        ("VO", "It took us a month to cut a road no one will ever use again.")]),
    ("b2_saltdesert", "f_b2_saltdesert", 10, [
        ("VO", "Hastings wrote it was forty miles of dry drive. It was eighty. Five days and five nights without water.")]),
    ("b3_cache", "f_b3_cache", 5, []),
    ("b4_snyder", "f_b4_snyder", 8, []),
    ("b5_banish", "f_b5_banish", 10, [
        ("GRAVES", "He hangs... or he rides out alone."),
        ("KESEBERG", "Hang him."),
        ("VIRGINIA", "Papa..."),
        ("REED", "I'll come back for you, Virginia. With bread in both hands. Look after your mother.")]),
    ("b6_hardkoop", "f_b6_hardkoop", 6, [
        ("KESEBERG", "The oxen cannot pull one pound more."),
        ("VO", "We were becoming people we did not know.")]),
    ("b7_stanton", "f_b7_stanton", 8, [
        ("STANTON", "Bread from Captain Sutter! And these two men, Luis and Salvador, will guide us over!")]),
    ("c1_lake", "f_c1_lake", 8, [
        ("BREEN", "One more dry week is all we ask.")]),
    ("c2_pass", "f_c2_pass", 10, [
        ("STANTON", "I reached the top! We cross tonight or not at all!"),
        ("MOTHER", "The children cannot go another step.")]),
    ("c3_cabins", "f_c3_cabins", 8, [
        ("VO", "We built three cabins by the lake. The Donners, caught behind, had only tents of brush at Alder Creek. Eighty-one of us... and the snow kept coming.")]),
    ("c4_alder", "f_c4_alder", 6, [
        ("TAMSEN", "It mends, girls. It mends.")]),
    ("c5_breen", "f_c5_breen", 6, [
        ("BREEN", "Snowing fast. Snow higher than the shanty. No living thing without wings can get about.")]),
    ("c6_hides", "f_c6_hides", 8, [
        ("MARGARET", "And I will pay you double, in cattle, when we reach California."),
        ("VO", "We ate the roofs.")]),
    ("c7_burial", "f_c7_burial", 6, []),
    ("t_forlorn", "t_forlorn", 3, []),
    ("d1_snowshoes", "f_d1_snowshoes", 8, [
        ("GRAVES", "Fifteen of us, on these. Six days' rations."),
        ("EDDY", "It's not enough."),
        ("GRAVES", "It's what there is. Every mouth that walks out is a mouth that stops eating here.")]),
    ("d2_depart", "f_d2_depart", 8, [
        ("VO", "Fifteen grown folks and two boys went for the settlements on snowshoes. Mama wanted to go... she had us instead.")]),
    ("d3_stanton", "f_d3_stanton", 8, [
        ("MARY", "Mr. Stanton... are you coming?"),
        ("STANTON", "Yes. I am coming soon.")]),
    ("d4_death_camp", "f_d4_death_camp", 10, [
        ("VO", "What was done in that camp to keep breath in the living, they did not speak of after. And no one who was not there may judge them.")]),
    ("d5_warning", "f_d5_warning", 8, [
        ("EDDY", "Foster has begun to look at you when he talks of food. Go. Now. Don't keep to the trail.")]),
    ("d6_ridge", "f_d6_ridge", 6, [
        ("VO", "The two men Sutter sent to save us... were repaid the way desperate men repay.")]),
    ("d7_ranch", "f_d7_ranch", 8, [
        ("EDDY", "Bread.")]),
    ("e1_sutter", "f_e1_sutter", 6, [
        ("SUTTER", "No animal alive can cross before March."),
        ("REED", "My family is up there. I will carry the flour on my own back.")]),
    ("e2_relief1", "f_e2_relief1", 8, [
        ("MURPHY", "Are you men from California... or do you come from heaven?")]),
    ("e3_patty", "f_e3_patty", 8, [
        ("PATTY", "Well, Mother. If you never see me again... do the best you can.")]),
    ("e4_reunion", "f_e4_reunion", 8, [
        ("VIRGINIA", "PAPA!"),
        ("VO", "I have not wrote you half of the trouble we've had. But I have wrote you enough to know what trouble is.")]),
    ("e5_doll", "f_e5_doll", 6, [
        ("PATTY", "Dolly wasn't scared, Papa.")]),
    ("e6_tamsen", "f_e6_tamsen", 10, [
        ("RESCUER", "Ma'am. The storm won't wait."),
        ("TAMSEN", "Take my daughters. ... Remember your mother. Say it."),
        ("GIRLS", "Remember your mother.")]),
    ("e7_keseberg", "f_e7_keseberg", 8, [
        ("FALLON", "Where is Mrs. Donner?"),
        ("KESEBERG", "I often think the Almighty has singled me out... to see how much a man can bear.")]),
    ("e8_paradise", "f_e8_paradise", 8, [
        ("VO", "It was long ago that we crossed. And when I came down into that valley... I really thought I had stepped over into paradise.")]),
    ("f1_letter_end", "f_f1_letter_end", 10, [
        ("VIRGINIA", "We have left everything. But I don't care for that. We have got through with our lives. But Cousin... never take no cutoffs. And hurry along as fast as you can.")]),
    ("t_end", "t_end", 8, []),
]

LEAD, GAP, TAIL = 0.6, 0.6, 1.0


def tts(speaker, text, dest):
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE[speaker]}",
        data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2"}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        dest.write_bytes(r.read())


def adur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


concat_list = []
total = 0.0
for shot, frame, planned, lines in SHOTS:
    # 1) per-line mp3s
    mp3s = []
    for i, (spk, text) in enumerate(lines):
        mp3 = VOL / f"{shot}_{i}_{spk.lower()}.mp3"
        if not mp3.exists():
            print(f"tts {shot}/{i} {spk}")
            tts(spk, text, mp3)
        mp3s.append(mp3)

    # 2) shot duration from audio
    durs = [adur(m) for m in mp3s]
    audio_len = LEAD + sum(durs) + GAP * max(0, len(durs) - 1) + TAIL if durs else 0
    dur = round(max(planned, audio_len), 2)
    total += dur

    seg = SEGS / f"{shot}.mp4"
    concat_list.append(seg)
    if seg.exists():
        continue

    # 3) build segment: still frame + offset-mixed lines
    cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", str(dur),
           "-i", str(FRAMES / f"{frame}.png")]
    for m in mp3s:
        cmd += ["-i", str(m)]
    fparts = ["[0:v]scale=854:480,setsar=1,fps=24,format=yuv420p[vout]"]
    if mp3s:
        off = LEAD
        amix_in = ""
        for i, d in enumerate(durs):
            ms = int(off * 1000)
            fparts.append(f"[{i+1}:a]aresample=44100,aformat=channel_layouts=stereo,"
                          f"adelay={ms}|{ms}[a{i}]")
            amix_in += f"[a{i}]"
            off += d + GAP
        fparts.append(f"{amix_in}amix=inputs={len(mp3s)}:normalize=0,apad[aout]")
    else:
        cmd += ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=44100:cl=stereo"]
        fparts.append(f"[{len(mp3s)+1}:a]anull[aout]")
    cmd += ["-filter_complex", ";".join(fparts), "-map", "[vout]", "-map", "[aout]",
            "-t", str(dur), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
            "-c:a", "aac", "-b:a", "160k", str(seg)]
    subprocess.run(cmd, check=True)
    print(f"seg {shot} {dur:.1f}s")

# 4) concat
lst = SEGS / "list.txt"
lst.write_text("".join(f"file '{p.resolve()}'\n" for p in concat_list))
out = PROJ / "animatic_v1.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                "-i", str(lst), "-c", "copy", str(out)], check=True)
print(f"wrote {out} — {len(SHOTS)} shots, {total:.0f}s ({total/60:.1f} min)")
