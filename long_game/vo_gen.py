#!/usr/bin/env python3
"""Generate the narration VO track, one mp3 per shot, via edge-tts.

Usage: .venv-tts/bin/python vo_gen.py
Prints each line's audio duration next to its clip budget so overlong lines are obvious.
"""
import asyncio
import subprocess
from pathlib import Path

import edge_tts

VOICE = "en-US-AndrewNeural"
RATE = "-8%"
OUT = Path(__file__).parent / "vo"

# (shot, clip_seconds, text) — clip_seconds is the picture budget; VO may spill ~2s into
# the next shot. None = no narration over that shot (dialogue carries it).
LINES = [
    ("1_1", 10, "The retro floor was where you went to be seen not caring. Deshawn was up on the DDR pad, losing on purpose — and making losing look like the coolest thing a body could do."),
    ("1_2", 8, "Cass — seventeen, and carrying it like a sentence he'd been handed — was reading the maintenance placard on a machine two aisles over."),
    ("1_3", 8, "There is a specific fear a broken ride produces — not fear of the ride. Fear of the broken. They walked toward it the way boys walk toward exactly this fear."),
    ("1_4", 6, "One credit — one subjective year. You will not remember the outside while inside. You will remember everything when you leave."),
    ("1_5", 12, "Deshawn's five years took about ninety seconds on the outside."),
    ("1_6", 8, "Here is the thing they got right about Cass: he could be goaded. Because underneath the placard-reading was a boy who wanted, badly, to find out what was down there."),
    ("1_7", 8, "Milo set the difficulty as high as the uncapped machine would go. And then — because he was seventeen, because it would be so funny —"),
    ("2_1", 5, "He was cold. And the cold was wrong. That was the first thing, before he had a self to notice it with."),
    ("2_2", 8, "The sim did what it was built to do. It seated a life. He was a boy of the village, and he had always been a boy of the village. He lived eleven days like that."),
    ("2_3", 8, "On the eleventh day he drank from the near stream — which was clean, which everyone knew was clean. And he died on the packed earth that had been the first cold thing he ever felt."),
    ("2_4", 12, "And woke up. On the packed earth. Day Zero. With — this time — all of it."),
    ("2_5", 8, "If dying reset the day, maybe dying was the exit. It wasn't despair — it was debugging. But there was no counter. There was only Day Zero, patient as a wall. So he went to the woman at the edge of the village — the one everyone called touched, who talked to the air — and said the true thing."),
    ("2_6", 8, None),
    ("3_1", 8, "Forty summers. That was the gate. And he knew the whole shape of the tech tree — knew that salt and sweetness in clean water would hold a dying child in the world."),
    ("3_2", 8, "That was the drug, and he'd found it in his first dose: the world listens to me. And Cass — nineteen, then twenty-two, then twenty-five — became, without ever quite deciding to, a king."),
    ("3_3", 12, "It is a very good feeling to be a bronze-age king with a twenty-first-century head, when you think the whole thing is a ride you're about to step off. He spent like a man who knew the money was fake."),
    ("3_4", 10, "The truth had sounded like a boy raving about demons in the water. So he told a story instead: the water spirits are offended by water that has not been greeted. He had no idea it was the single most durable thing he would ever do."),
    ("3_5", 8, "He grew tired of it the way Deshawn had grown bored of his gold medals. Been there. Ruled that. The throne a chore by thirty-five, and a cage by the last of it."),
    ("3_6", 6, "He reached forty — the door he'd built an entire life around walking toward. And he braced for the chair, for the bright clean arcade evening —"),
    ("3_7", 8, "— and came back a thousand years further on. Go on, she had said. Not go home. He'd misread the one instruction the machine had ever given him plainly — and built a whole life on the misreading."),
    ("4_1", 8, "Every era fed the next. The world he woke into was built on the foundations of the one he'd left — and he had poured the minimum. And now he had to live on top of the minimum."),
    ("4_2", 10, "He knew the gesture. He'd invented the gesture — worn down by a thousand years, carried on the backs of grandmothers. Only the gesture was left. It saved no one now. And it was his — the last living trace of an entire lifetime."),
    ("4_3", 6, "A book of old legends held a clever-fool king who raised the dead with clean water. His own obituary, read centuries late. Four lines — one of them an insult."),
    ("4_4", 8, "This time, no crown. A workshop — wealthy enough to build, boring enough to live. He geared a waterwheel to bellows, and the bellows to a furnace — because heat is the gate all of chemistry waits behind."),
    ("4_5", 8, "He made the first strong acid in the world made on purpose. He offered it free to a city — and got exactly one taker: a grave young apothecary who liked that it cleaned wounds. But the apothecary wrote things down."),
    ("4_6", 10, "You cannot study a person that closely without coming to love them. Faustus confided, one night, about a dead son — and Cass understood in his chest what he'd been trying to prove with his head: they were all as real as grief gets."),
    ("4_7", 10, "He wanted, on a killing-hot afternoon, something cold and sweet. And he knew the one thing the age did not: salt on ice makes it colder. Nobody in the world knew that but him. So he got the number the way he got everything now."),
    ("4_8", 10, "He ate the first bowl in the bath. The fire outside — and the frost in the bowl. And Cass, who had been a king, and a boy dead of dirty water, sat in the hot, and ate the cold, and thought, with his whole chest: I have made it."),
]


async def main() -> None:
    OUT.mkdir(exist_ok=True)
    for shot, budget, text in LINES:
        if text is None:
            continue
        dest = OUT / f"{shot}.mp3"
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(dest))
        dur = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(dest)],
            capture_output=True, text=True).stdout.strip())
        flag = "  <-- LONG" if dur > budget + 2.5 else ""
        print(f"{shot}: vo {dur:5.1f}s / clip {budget}s{flag}")


asyncio.run(main())
