#!/usr/bin/env python3
"""Animatic for THE BUSY BODY: every shot's start frame held for the duration
of its ElevenLabs dialogue, cut together into animatic_<label>.mp4.

Usage: python3 make_animatic.py [label]     (default v1)
TTS lines land in vo/<shot>_<i>_<speaker>.mp3 and are skipped if present, so
edits to LINES only re-bill the changed lines. Segments rebuild every run.
"""
import json
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

LABEL = sys.argv[1] if len(sys.argv) > 1 else "v1"
HERE = Path(__file__).parent
VO = HERE / "vo"
SEG = HERE / "animatic_segs"
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()
SR = 44100
GAP, HEAD, TAIL = 0.55, 0.4, 0.8   # seconds between lines / before / after
FONT = "/System/Library/Fonts/Helvetica.ttc"

# locked cast (auditions.html 2026-07-10; Charles moved to Kevin Elliott for
# pitch separation from Sir George)
CAST = {
    "marplot":  "N2lVS1w4EtoT3dr4eOWO",   # Callum
    "george":   "JBFqnCBsd6RMkjVDRZzb",   # George
    "charles":  "MJyi2qJnZ6cONaNAgdKu",   # Kevin Elliott
    "miranda":  "pFZP5JQG7iQjIQuC4Bku",   # Lily
    "isabinda": "Xb7hH8MSUJpSbSDYk0k2",   # Alice
    "francis":  "VRAN0xryQGUWtDuwToRv",   # Henry
    "jealous":  "KTAbPR4QFlhaTpde6md8",   # Bloodgrin
    "patch":    "FGY2WhTYpPnrIDTdsKH5",   # Laura
    "whisper":  "bIHbv24MWmeRgasZH58o",   # Will
    "scentwell": "cgSgspJ2msm6clMCkdW9",  # Jessica
    "servant":  "iP95p4xoKVk53GoZ742B",   # Chris
}

# shot -> ordered dialogue; [] = silent hold
LINES = {
    "p1": [],
    "p2": [("george", "I am in love with two women, Charles. One all wit, whose face I have never seen — and one all beauty, to whom I have never spoken."),
           ("charles", "Then between them, you have exactly one mistress. And my father keeps her under lock and key.")],
    "p3": [("charles", "Marplot! How came your beautiful countenance clouded in the wrong place?"),
           ("marplot", "I avoid fighting, purely to be serviceable to my friends.")],
    "p4": [("marplot", "Pish, pox, that was an accident! I follow my instructions.")],
    "p5": [("marplot", "A secret! I shall go stark mad if I am not let into this secret. I must — and WILL — follow him.")],
    "p6": [("miranda", "Let the chair wait."),
           ("patch", "The Spanish father has spoiled our plot, madam — my lady shall be only Signior Babinetto's, he says."),
           ("miranda", "Let the tyrant man make what laws he will — a woman will find a way to break them.")],
    "p7": [("george", "Will you take the fifty guineas?"),
           ("francis", "Give me a hundred, sir, and try your fortune. He, he, he."),
           ("miranda", "So — 'tis well it's no worse. I'll fit you both.")],
    "p8": [("miranda", "If you look upon me, I shall sink, even masked as I am. Turn your back while I confess."),
           ("george", "Gone! Jilted! What woman can forgive a man that turns his back?")],
    "g1": [("miranda", "Now methinks there's nobody handsomer than you — so neat, so clean, Gardee."),
           ("francis", "Pretty rogue, pretty rogue! He, he, he."),
           ("miranda", "Faugh — how he stinks of tobacco.")],
    "g2": [("charles", "Sir — some means to support me —"),
           ("francis", "Marry Lady Wrinkle! Forty thousand pound!"),
           ("charles", "Why, she has but one eye."),
           ("francis", "Then she'll see but half your extravagance, sir! Out of my doors, you dog!")],
    "g3a": [("francis", "Hold, hold! Kissing was not in our agreement — that's contrary to articles!"),
            ("george", "Keep your distance, old gentleman.")],
    "g3b": [("george", "A nod is yes, a shake is no. Can you prefer that old, dry, withered, sapless log of sixty-five... to the vigorous, gay, sprightly love of twenty-four?"),
            ("miranda", "How every action charms me.")],
    "g3c": [("francis", "She has nicked you, Sir George! Ha, ha, ha!"),
            ("george", "Marry her, old Beelzebub — and you'll be cuckolded. Remember that... and tremble.")],
    "j1": [("jealous", "Why don't you write a bill upon your forehead, to show passengers there's something to be let! In, in — and lock her up till I come back from Change!"),
           ("isabinda", "Ay — to enjoy more freedom than he is aware of.")],
    "j2": [("jealous", "Have you a letter or message for anybody in my house, sirrah?"),
           ("whisper", "N-no, sir — I am seeking Trifle, sir — the very lap-dog my lady lost!"),
           ("jealous", "Let me catch you no more puppy-hunting about my doors!")],
    "j3": [("charles", "Fly with me now — I have raised a thousand pound."),
           ("isabinda", "And love rarely dwells with poverty, Charles. Wait — my father cannot watch forever."),
           ("patch", "The master! Coming up the street!")],
    "j4": [("marplot", "If that gentleman comes not as safe out of your house as he went in, I have half a dozen Myrmidons hard by!"),
           ("jealous", "Went IN? What — is he in then? Thieves! Thieves!"),
           ("marplot", "Murder! Murder! I was never in your house, sir!")],
    "j5": [("marplot", "Charles! Faith, I'm glad to see thee safe out."),
           ("charles", "It was YOU told him? Death — I could crush thee into atoms!"),
           ("marplot", "Will you... choke me... for my KINDNESS?")],
    "g4": [("miranda", "Tell Sir George: if he dares to saunter by the garden gate on the left, about the hour of eight, he shall be saluted with a pistol or a blunderbuss."),
           ("miranda", "I hope he understands my meaning better than to follow YOUR advice.")],
    "t1": [("marplot", "You shall be saluted... with a blunderbuss, sir. These were her very words."),
           ("george", "The garden gate — at eight — as I used to do! There must be a meaning in this! My dear Marplot, thou art my friend, my better angel!")],
    "j6": [("jealous", "Humph — 'tis Hebrew, I think. This may be one of Love's hieroglyphics.")],
    "j7": [("patch", "My charm for the toothache! I have worn it these seven years — 'twas given me by an angel, sir, and must never be opened, on pain of dire vengeance."),
           ("jealous", "There, there — burn it, and I warrant you no vengeance will follow.")],
    "j8": [("jealous", "Hey, hey! Why, you are a-top of the house, and you are down in the cellar! Play me a TUNE — or I'll break the spinet about your ears!")],
    "j9": [("jealous", "Hell and Furies — a man in the closet!"),
           ("patch", "A ghost, a ghost! Oh, this comes of opening the charm!")],
    "j10": [("charles", "Here will I plant myself, and through my breast he shall make his passage."),
            ("patch", "Softly, sir. What think you of PERSONATING this Spaniard — and marrying your mistress by her father's own consent? Nobody here has ever seen Don Diego."),
            ("charles", "My better genius! Thou hast revived my drooping soul.")],
    "g5": [("scentwell", "This way, sir — through many a dark passage and dirty step.")],
    "g6": [("miranda", "My guardian has surrendered my fortune — he thinks he weds me in the morning. My emissaries are luring him to Epsom tonight."),
           ("george", "Then tonight thou art mine."),
           ("scentwell", "Sir Francis, madam — and Master Marplot — at the door!")],
    "g7": [("miranda", "Hold, hold, dear Gardee! I have a — a — a MONKEY shut up there! Untamed! He'll break all my china!"),
           ("marplot", "A monkey! Let me but peep — I can tame a monkey as well as the best of them — oh, how I love the little miniatures of man!"),
           ("francis", "Let my Chargee's monkey alone, or Bambo shall fly about your ears!")],
    "g8": [("marplot", "Oh Lord, Oh Lord! Thieves! Thieves! Mur—"),
           ("george", "Damn ye, you unlucky dog — 'tis I!"),
           ("marplot", "It flew over my shoulders — scratched all my face — broke yon china — and whisked out of the window!")],
    "g9": [("marplot", "I'm as secret as a priest when I'm trusted."),
           ("george", "Why, 'tis with a priest our business is at present — and YOU, sir, come along with us, where I can see you.")],
    "g10": [("francis", "Ah, my sweet Chargee — don't be frighted."),
            ("miranda", "I'm so surprised with JOY to see you, I know not what to say! ... Could you not have carried it to be MENDED, as I bid you?")],
    "g11": [("miranda", "If ever I marry, positively this is my wedding day."),
            ("francis", "Adod, I am happier than the Great Mogul! The joyful bridegroom, I —"),
            ("miranda", "— and I the happy bride.")],
    "j11": [("george", "Mr. Meanwell, sir, at your service — the Don speaks no English."),
            ("jealous", "Meanwell is a very good name, and very significant! By St. Jago, my daughter weds tonight!"),
            ("charles", "Yes, faith — if he knew all.")],
    "j12": [("jealous", "And the five thousand crowns, sir — paid down today?"),
            ("george", "The crowns — but — but — but —"),
            ("charles", "Say we have brought it in COMMODITIES."),
            ("george", "— but of course! Tobacco, sugars, spices, lemons — and so forth. My personal bond upon the rest.")],
    "j13a": [("isabinda", "Kill me, kill me instantly — 'twill be worse than death to wed him! My own hand shall cut the knot first!")],
    "j13b": [("george", "Suppose this Spaniard... should be the very man to whom you'd fly — those eyes that would not look on CHARLES."),
             ("isabinda", "Where is he? Oh, let me fly into his arms!"),
             ("george", "Take heed, madam — you don't betray yourself. Be all obedience."),
             ("isabinda", "Sir... do with me what you please. I am all obedience.")],
    "j14": [("marplot", "Is there not a gentleman within, in a Spanish habit? ... Are you SURE he is a SPANISH gentleman? For 'tis an ENGLISH gentleman I want — though I suppose he may be DRESSED like a Spaniard."),
            ("servant", "Who knows but this may be an impostor... pray step in, sir.")],
    "j15": [("jealous", "STOP THE MARRIAGE!"),
            ("george", "Go on, Mr. Tackum! I guard this passage, old gentleman — I'll see 'em signed, or die for't!"),
            ("servant", "We are afraid of his SWORD, sir — take that from him, and we'll knock him down presently."),
            ("marplot", "Why — what do you beat ME for? I ha'nt married your daughter!")],
    "j16": [("jealous", "Seize her!"),
            ("charles", "Rascals, retire — she's my WIFE. Touch her if you dare; I'll make dogs-meat of you."),
            ("jealous", "Ah! Downright ENGLISH! Oh, oh, oh!")],
    "j17": [("francis", "Rail on, gentlemen — this lady is my WIFE, do you see?"),
            ("george", "Lawfully begotten by ME, sir."),
            ("miranda", "The writings of your uncle's estate, Charles — your due these three years."),
            ("francis", "CONFOUND YOU ALL!")],
    "j18": [("jealous", "Seeing thou hast outwitted me — take her, and bless you both."),
            ("marplot", "Here's everybody happy, I find, but poor Pilgarlick — cuffed, kicked, and beaten in your service."),
            ("george", "Thy estate is next, Marplot — I'll see old Gripe surrender it."),
            ("marplot", "THAT will make me as happy as any of you!")],
    "j19": [("jealous", "By my example let all parents move — and never strive to cross their children's love.")],
}
ORDER = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8",
         "g1", "g2", "g3a", "g3b", "g3c", "j1", "j2",
         "j3", "j4", "j5", "g4", "t1",
         "j6", "j7", "j8", "j9", "j10", "g5", "g6", "g7", "g8", "g9",
         "g10", "g11", "j11", "j12", "j13a", "j13b", "j14", "j15", "j16",
         "j17", "j18", "j19"]
SILENT_HOLD = 4.0


def frame_for(shot: str) -> Path:
    p = HERE / "frames" / f"{shot}.png"
    return p if p.exists() else HERE / "frames" / f"{shot[:-1]}.png"


def tts(shot: str, i: int, speaker: str, text: str) -> str:
    out = VO / f"{shot}_{i}_{speaker}.mp3"
    if out.exists():
        return f"skip {out.name}"
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{CAST[speaker]}",
        data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2"}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    for attempt in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out.write_bytes(r.read())
            return f"OK   {out.name}"
        except Exception as e:
            err = str(e)
    return f"FAIL {out.name}: {err}"


def decode(mp3: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp3), "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def build_segment(shot: str) -> tuple[Path, float]:
    lines = LINES[shot]
    if lines:
        gap = np.zeros(int(GAP * SR), dtype=np.float32)
        parts = [np.zeros(int(HEAD * SR), dtype=np.float32)]
        for i, (speaker, _) in enumerate(lines):
            parts.append(decode(VO / f"{shot}_{i}_{speaker}.mp3"))
            parts.append(gap if i < len(lines) - 1 else
                         np.zeros(int(TAIL * SR), dtype=np.float32))
        audio = np.concatenate(parts)
        dur = len(audio) / SR
    else:
        dur = SILENT_HOLD
        audio = np.zeros(int(dur * SR), dtype=np.float32)
    wav = SEG / f"{shot}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR),
                    "-ac", "1", "-i", "-", str(wav)],
                   input=audio.tobytes(), check=True)
    mp4 = SEG / f"{shot}.mp4"
    vf = "scale=854:480,setsar=1,fps=24"
    if Path(FONT).exists():
        vf += (f",drawtext=fontfile={FONT}:text='{shot}':x=10:y=10:fontsize=16:"
               f"fontcolor=white@0.55:box=1:boxcolor=black@0.3:boxborderw=4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1",
                    "-i", str(frame_for(shot)), "-i", str(wav),
                    "-t", f"{dur:.3f}", "-vf", vf,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", str(mp4)], check=True)
    return mp4, dur


def main():
    VO.mkdir(exist_ok=True)
    SEG.mkdir(exist_ok=True)
    jobs = [(s, i, sp, tx) for s in ORDER for i, (sp, tx) in enumerate(LINES[s])]
    print(f"{len(jobs)} lines, {sum(len(t) for *_ , t in jobs)} chars")
    with ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(lambda j: tts(*j), jobs):
            print(r, flush=True)

    total = 0.0
    concat = []
    for shot in ORDER:
        mp4, dur = build_segment(shot)
        total += dur
        concat.append(f"file '{mp4.name}'")
        print(f"seg {shot}: {dur:.1f}s", flush=True)
    (SEG / "concat.txt").write_text("\n".join(concat) + "\n")
    out = HERE / f"animatic_{LABEL}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(SEG / "concat.txt"), "-c", "copy", str(out)],
                   check=True)
    print(f"wrote {out.name} — {total/60:.1f} min, {len(ORDER)} shots")


if __name__ == "__main__":
    main()
