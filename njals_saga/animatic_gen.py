#!/usr/bin/env python3
"""Burnt Njal animatic: storyboard frames + ElevenLabs dialogue, no Seedance.
- TTS every line (skips existing mp3s in animatic/tts/)
- per-shot clip = frame with slow push-in + lines with natural gaps
- dialogue shot duration = lead + sum(lines+gaps) + tail (the real sizing formula)
- visual-only shots hold for their storyboard target duration
Output: animatic_v1.mp4 (854x480, 24fps). Rerun after any edit; only TTS is cached."""
import json
import os
import subprocess
import urllib.request
from pathlib import Path

PROJ = Path(__file__).parent
TTS_DIR = PROJ / "animatic" / "tts"
SHOT_DIR = PROJ / "animatic" / "shots"
for d in (TTS_DIR, SHOT_DIR):
    d.mkdir(parents=True, exist_ok=True)
KEY = (os.environ.get("ELEVENLABS_API_KEY")
       or Path(os.path.expanduser("~/.elevenlabs_key")).read_text().strip())

LEAD, GAP, TAIL = 0.6, 0.55, 0.9

VOICE = {  # character -> (voice name, voice_id) — primary picks from casting.html
    "NJAL": ("Elderon", "NwyAvGnfbFoNNEi4UuTq"),
    "GUNNAR": ("Oyvind", "nhvaqgRyAq6BmFs3WcdX"),
    "SKARPHEDINN": ("VikingBjorn", "ljo9gAlSqKOvF6D8sOsX"),
    "HALLGERDA": ("Charlotte", "rhS7yjXTU4uIlRxXhNW7"),
    "BERGTHORA": ("Alice", "Xb7hH8MSUJpSbSDYk0k2"),
    "FLOSI": ("Leif", "tJDFCHyviItsYF1qqToS"),
    "KARI": ("CJ", "9n6dGtreZHvmNb14Y1VO"),
    "HILDIGUNNA": ("Lily", "pFZP5JQG7iQjIQuC4Bku"),
    "MORD": ("Callum", "N2lVS1w4EtoT3dr4eOWO"),
    "HOSKULD": ("George", "JBFqnCBsd6RMkjVDRZzb"),
    "HRUT": ("Nils", "xVvh7KgfbHX1WS6JTNXX"),
    "NARRATOR": ("Nils", "xVvh7KgfbHX1WS6JTNXX"),
    "RANNVEIG": ("NanaMargaret", "xIzR6egd3S3LJZbVW0c1"),
    "GIZUR": ("Daniel", "onwK4e9ZLuTAKqWW03F9"),
    "GUNNAR_LAMBI": ("Harry", "SOYHLrjzK2X1ezoPC6cr"),
    "KOLSKEGG": ("Brian", "nPczCjzI2devNBz1zQrb"),
    "HAUSKULD_ELDER": ("Eric", "cjVigY5qzO86Huf0OWal"),
    "THORGRIM": ("Adam", "pNInz6obpgDQGcFmaJgB"),
    "VALGARD": ("Schmitz", "HAvvFKatz0uu0Fv55Riy"),
    "ELDER": ("Bill", "pqHfZKP75CvOlQylNhV4"),       # lawspeaker / Hall / finder — never co-occur
    "BOY": ("Jessica", "cgSgspJ2msm6clMCkdW9"),      # placeholder child voice (both boys)
    "SAILOR": ("Will", "bIHbv24MWmeRgasZH58o"),
}

# shot -> list of (SPEAKER, line). Empty list = visual-only (holds target duration).
SCRIPT = {
    "p1_thiefs_eyes": [
        ("HAUSKULD_ELDER", "Come hither to me, daughter. What dost thou think of this maiden — is she not fair?"),
        ("HRUT", "Fair enough is this maid, and many will smart for it; but this I know not, whence thief's eyes have come into our race."),
    ],
    "p2_title": [],
    "a1_wooing": [
        ("GUNNAR", "How wouldst thou answer, were I to ask for thee?"),
        ("HALLGERDA", "That can not be in thy mind."),
        ("GUNNAR", "It is though."),
    ],
    "a2_warning": [
        ("NJAL", "From her will arise all kind of ill, if she comes hither east."),
        ("GUNNAR", "Never shall she spoil our friendship."),
        ("NJAL", "Ah — but yet that may come very near. Thou wilt have always to make atonement for her."),
    ],
    "a3_quarrel": [
        ("HALLGERDA", "There's not much to choose between you two. Thou hast hangnails on every finger, and Njal is beardless."),
        ("BERGTHORA", "But Thorwald, thy husband, was not beardless — and yet thou plottedst his death."),
        ("HALLGERDA", "It stands me in little stead to have the bravest man in Iceland, if thou dost not avenge this, Gunnar!"),
        ("GUNNAR", "Home I will go. Never will I be egged on by thee like a fool."),
    ],
    "a4_purse": [
        ("SKARPHEDINN", "Hallgerda does not let our house-carles die of old age."),
        ("NJAL", "More men now become man-slayers than I weened."),
    ],
    "a5_slap": [
        ("GUNNAR", "Ill indeed is it, if I am a partaker with thieves."),
        ("HALLGERDA", "I will bear that slap in mind — and repay it, if I can."),
    ],
    "a6_conditions": [
        ("NJAL", "Never slay more than one man in the same stock; and never break the peace which good men make between thee and others. Else thou wilt have but a little while to live — but otherwise, thou wilt come to be an old man."),
        ("GUNNAR", "Dost thou know what will be thine own death?"),
        ("NJAL", "I know it."),
        ("GUNNAR", "What?"),
        ("NJAL", "That which all would be the last to think."),
    ],
    "a7_ford": [
        ("GUNNAR", "I would like to know whether I am by so much the less brisk and bold than other men — because I think more of killing men than they?"),
    ],
    "a8_outlawry": [
        ("GIZUR", "Gunnar shall fare abroad, and be away three winters. But if he does not fare, then he may be slain by those who have blood to avenge."),
    ],
    "a9_fair_lithe": [
        ("GUNNAR", "Fair is the Lithe; so fair that it has never seemed to me so fair. The corn fields are white to harvest, and the home mead is mown. And now I will ride back home, and not fare abroad at all."),
        ("KOLSKEGG", "Tell my kinsmen and my mother, that I never mean to see Iceland again. For I shall soon learn that thou art dead, brother."),
    ],
    "a10_siege": [
        ("GUNNAR", "Thou hast been sorely treated, Sam, my fosterling. And this warning is so meant, that our two deaths will not be far apart."),
        ("GIZUR", "Well — is Gunnar at home?"),
        ("THORGRIM", "Find that out for yourselves. But this I am sure of: his bill is at home."),
    ],
    "a11_bowstring": [
        ("GUNNAR", "Give me two locks of thy hair; and ye two, my mother and thou, twist them together into a bowstring for me."),
        ("HALLGERDA", "Does aught lie on it?"),
        ("GUNNAR", "My life lies on it. For they will never come to close quarters with me, if I can keep them off with my bow."),
        ("HALLGERDA", "Then I call to thy mind that slap on the face which thou gavest me. And I care never a whit whether thou holdest out a long while, or a short."),
        ("GUNNAR", "Every one has something to boast of; and I will ask thee no more for this."),
        ("RANNVEIG", "Thou behavest ill — and this shame shall long be had in mind."),
    ],
    "a12_fall": [
        ("GIZUR", "We have now laid low to earth a mighty chief, and hard work has it been. And the fame of this defence of his shall last, as long as men live in this land."),
    ],
    "b1_ice": [
        ("SKARPHEDINN", "I am tying my shoe."),
        ("KARI", "This was done like a man."),
    ],
    "b2_ring": [
        ("NJAL", "Knowest thou what brought thy father to his death?"),
        ("BOY", "I know that Skarphedinn slew him. But we need not keep that in mind, when an atonement has been made for it, and a full price paid."),
        ("NJAL", "Better answered than asked. Thou wilt live to be a good man and true."),
    ],
    "b3_one_law": [
        ("ELDER", "If there be a sundering of the laws, then there will be a sundering of the peace. This is the beginning of our laws: that all men shall be Christian here in the land."),
    ],
    "b4_deathbed": [
        ("VALGARD", "Set them by the ears by tale-bearing, so that Njal's sons may slay Hauskuld. There are many who will have the blood-feud after him — and so Njal's sons will be slain in that quarrel."),
    ],
    "b5_slander": [
        ("MORD", "They gave thee a horse which they called a dark horse; and that they did out of mockery at thee. They mean to fall upon you."),
        ("HOSKULD", "Thou canst never say so much ill of Njal's sons, as to make me believe it. And were it true — I would far rather suffer death at their hands, than work them any harm."),
    ],
    "b6_cornfield": [
        ("SKARPHEDINN", "Don't try to turn on thy heel, Whiteness priest."),
        ("HOSKULD", "God help me — and forgive you!"),
    ],
    "b7_grief": [
        ("NJAL", "Methinks it were better to have lost two of my sons, and that Hauskuld lived. The sweetest light of my eyes is quenched."),
        ("SKARPHEDINN", "What will come after?"),
        ("NJAL", "My death. And the death of my wife, and of all my sons."),
        ("KARI", "What dost thou foretell for me?"),
        ("NJAL", "They will have hard work to go against thy good fortune. For thou wilt be more than a match for all of them."),
    ],
    "b8_cloak": [
        ("HILDIGUNNA", "This cloak, Flosi, thou gavest to Hauskuld — and now I will give it back to thee. He was slain in it. I call God and all good men to witness, that I adjure thee, by all the might of thy Christ, and by thy manhood and bravery: take vengeance for all those wounds which he had on his dead body — or else be called every man's dastard."),
        ("FLOSI", "Thou art the greatest hell-hag. Women's counsel is ever cruel."),
    ],
    "b9_silver": [
        ("FLOSI", "Who may have given this? Thy father, the Beardless Carle? For many who look at him know not whether he is more a man than a woman."),
        ("SKARPHEDINN", "He has had sons by his wife; and few of our kinsfolk lie unavenged by our house. Take these — thou wilt have more need of them."),
        ("FLOSI", "Go we now home. One fate shall befall us all."),
    ],
    "b10_oath": [
        ("FLOSI", "We shall ride to Bergthorsknoll with all our band, and fall on Njal's sons with fire and sword — and not turn away before they are all dead. Ye shall hide this plan, for our lives lie on it."),
    ],
    "c1_supper": [
        ("BERGTHORA", "Now shall ye choose your meat to-night, each what he likes best. For this evening is the last that I shall set meat before my household."),
        ("NJAL", "Methinks I see all round the room. The gable wall is thrown down — and the whole board, and the meat on it, is one gore of blood."),
    ],
    "c2_indoors": [
        ("NJAL", "My will is that our men go indoors. They had hard work to master Gunnar of Lithend, and he was alone."),
        ("SKARPHEDINN", "These men will fall on us with fire. I am unwilling to be stifled indoors, like a fox in his earth. But I may well humour my father in this, by being burnt indoors along with him — for I am not afraid of my death."),
        ("FLOSI", "Now are they all fey, since they have gone indoors."),
    ],
    "c3_fire": [
        ("FLOSI", "Now there are but two choices, and neither of them good. One is to turn away — and that is our death. The other, to set fire, and burn them inside; and that is a deed which we shall have to answer for heavily before God, since we are Christian men ourselves. But still, we must take to that counsel."),
        ("SKARPHEDINN", "What, lads! Are ye lighting a fire — or are ye taking to cooking?"),
    ],
    "c4_refusal": [
        ("FLOSI", "I will offer thee, master Njal, leave to go out. It is unworthy that thou shouldst burn indoors."),
        ("NJAL", "I will not go out. For I am an old man, and little fitted to avenge my sons — but I will not live in shame."),
        ("BERGTHORA", "I was given away to Njal young; and I have promised him this, that we would both share the same fate."),
    ],
    "c5_bed": [
        ("BOY", "Thou hast promised me this, grandmother — that we should never part, so long as I wished to be with thee. And methinks it is much better to die with thee and Njal, than to live after you."),
        ("NJAL", "We will go to our bed, and lay us down. I have long been eager for rest."),
    ],
    "c6_beam": [
        ("KARI", "This parting of ours will be in such wise, that we shall never see one another more."),
        ("SKARPHEDINN", "It joys me, brother-in-law, to think that if thou gettest away — thou wilt avenge me."),
    ],
    "c7_keepsake": [
        ("GUNNAR_LAMBI", "Weepest thou now, Skarphedinn?"),
        ("SKARPHEDINN", "Not so. But true it is, the smoke makes one's eyes smart. But is it as it seems to me — dost thou laugh?"),
        ("GUNNAR_LAMBI", "So it is surely. And I have never laughed, since thou slewest Thrain on Markfleet."),
        ("SKARPHEDINN", "Then here is a keepsake for thee."),
        ("FLOSI", "We shall have to boast of something else, than that Njal has been burnt in his house. For there is no glory in that."),
    ],
    "c8_bright": [
        ("ELDER", "Njal's body and visage seem to me so bright — I have never seen any dead man's body so bright as this."),
    ],
    "c9_vow": [
        ("KARI", "Though all others take an atonement in their quarrels, yet will I take no atonement. My son is still unavenged — and I mean to take that on myself alone."),
    ],
    "d1_battle": [],
    "d2_peace": [
        ("ELDER", "I will put no price on my son. And yet will I come forward, and grant both pledges and peace to those who are my adversaries."),
    ],
    "d3_yule": [
        ("GUNNAR_LAMBI", "Well at first, for a long time. But still, the end of it was — that he wept."),
        ("KARI", "Many would say, Lord, that I have done this deed on your behalf — to avenge your henchman."),
        ("FLOSI", "Kari hath not done this without a cause. He is in no atonement with us; and he only did what he had a right to do."),
    ],
    "d4_pilgrim": [],
    "d5_kiss": [
        ("FLOSI", "There are few men like Kari. And I would that my mind were shapen altogether like his."),
    ],
    "d6_ship": [
        ("SAILOR", "That ship is not seaworthy."),
        ("FLOSI", "'Tis quite good enough, for an old and death-doomed man."),
    ],
    "d7_endcard": [
        ("NARRATOR", "And of that ship, no tidings were ever heard. And here we end the story of Burnt Njal."),
    ],
}

# cut order + visual-only hold durations (from storyboard targets)
ORDER = ["p1_thiefs_eyes", "p2_title", "a1_wooing", "a2_warning", "a3_quarrel", "a4_purse",
         "a5_slap", "a6_conditions", "a7_ford", "a8_outlawry", "a9_fair_lithe", "a10_siege",
         "a11_bowstring", "a12_fall", "b1_ice", "b2_ring", "b3_one_law", "b4_deathbed",
         "b5_slander", "b6_cornfield", "b7_grief", "b8_cloak", "b9_silver", "b10_oath",
         "c1_supper", "c2_indoors", "c3_fire", "c4_refusal", "c5_bed", "c6_beam",
         "c7_keepsake", "c8_bright", "c9_vow", "d1_battle", "d2_peace", "d3_yule",
         "d4_pilgrim", "d5_kiss", "d6_ship", "d7_endcard"]
HOLD = {"p2_title": 5, "d1_battle": 7, "d4_pilgrim": 6}   # visual-only shots


def sh(*cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def tts(voice_id, text, dest):
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2"}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    dest.write_bytes(urllib.request.urlopen(req).read())


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


# ---- 1. TTS all lines (cached) + convert to uniform wav ----
for shot, lines in SCRIPT.items():
    for i, (speaker, text) in enumerate(lines):
        mp3 = TTS_DIR / f"{shot}_{i:02d}_{speaker}.mp3"
        wav = mp3.with_suffix(".wav")
        if not mp3.exists():
            print(f"TTS {mp3.name}")
            tts(VOICE[speaker][1], text, mp3)
        if not wav.exists():
            sh("ffmpeg", "-y", "-v", "error", "-i", str(mp3),
               "-ar", "44100", "-ac", "2", str(wav))

# silence pieces
for name, secs in (("lead", LEAD), ("gap", GAP), ("tail", TAIL)):
    w = TTS_DIR / f"_sil_{name}.wav"
    if not w.exists():
        sh("ffmpeg", "-y", "-v", "error", "-f", "lavfi",
           "-i", f"anullsrc=r=44100:cl=stereo:d={secs}", str(w))

# ---- 2. per-shot audio + clip ----
clips = []
total = 0.0
for shot in ORDER:
    lines = SCRIPT[shot]
    frame = PROJ / "frames" / f"f_{shot}.png"
    clip = SHOT_DIR / f"{shot}.mp4"
    if lines:
        lst = TTS_DIR / f"_{shot}.txt"
        parts = [f"file '_sil_lead.wav'"]
        for i, (speaker, _) in enumerate(lines):
            parts.append(f"file '{shot}_{i:02d}_{speaker}.wav'")
            parts.append(f"file '_sil_gap.wav'")
        parts[-1] = f"file '_sil_tail.wav'"
        lst.write_text("\n".join(parts) + "\n")
        aud = TTS_DIR / f"_{shot}_mix.wav"
        sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
           "-i", str(lst), "-c", "copy", str(aud))
        d = dur(aud)
        audio_in = ["-i", str(aud)]
    else:
        d = HOLD.get(shot, 6)
        audio_in = ["-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={d}"]
    # static hold — ffmpeg zoompan "Ken Burns" pushes quiver at slow zoom rates
    # (integer-pixel crop rounding); see MOVIE_LESSONS.md
    still = "scale=854:480,setsar=1,fps=24,format=yuv420p"
    sh("ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(frame), *audio_in,
       "-filter_complex", f"[0:v]{still}[v]", "-map", "[v]", "-map", "1:a",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
       "-c:a", "aac", "-b:a", "128k", "-t", f"{d:.3f}", str(clip))
    clips.append(clip)
    total += d
    print(f"{shot}: {d:.1f}s")

# ---- 3. concat ----
lst = SHOT_DIR / "_concat.txt"
lst.write_text("\n".join(f"file '{c.name}'" for c in clips) + "\n")
sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
   "-c", "copy", str(PROJ / "animatic_v1.mp4"))
print(f"\nwrote animatic_v1.mp4 — {len(clips)} shots, {total/60:.1f} min")
