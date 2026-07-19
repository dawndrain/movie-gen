#!/usr/bin/env python3
"""Emit videos_tv1.sh for THE VARIANCE first pass (Seedance, FAST draft).
Dialogue shots use TTS --audio refs; durations auto-sized from the audio.
Run:  python3 make_videos.py
Then: python3 ../pool_run_fast.py overwhelming_beauty/videos_tv1.sh overwhelming_beauty/outputs/tv1
"""
import subprocess
from pathlib import Path

from vo_tv import LINES

HERE = Path(__file__).parent
VO = HERE / "vo"
F = "overwhelming_beauty/frames"
A = "overwhelming_beauty/anchors"

NEG = ("Photorealistic, natural human motion, no slow motion, no random camera "
       "moves, no zoom, no text or captions or subtitles. Characters keep "
       "exactly the same faces, hair and clothes as in the reference images. "
       "There is no narrator and no voiceover.")
SILENT = ("No dialogue, no speech, no narrator, no voiceover, nobody's lips "
          "move; ambient sound only.")
COLD_LOCK = ("World lock: a quiet dystopian near-future — every worker wears "
             "an identical plain slate-blue jumpsuit; muted desaturated "
             "teal-grey palette, soft overcast institutional light, clean "
             "minimal pale-concrete architecture; people move calmly, evenly, "
             "without hurry or expression.")
WARM_LOCK = ("World lock: the old quarter is warm and alive — golden light, "
             "saturated color, varied non-uniform clothing on passersby; Oren "
             "still wears his slate-blue worker jumpsuit; Dez wears a "
             "rust-orange scarf and patched olive canvas jacket.")

CHAR_NAMES = {"oren": "Oren", "petra": "Petra", "dez": "Dez"}

# shot -> (duration or None for auto, staging prompt, [anchor refs], lock)
SHOTS = {
    "t1": (8, "Locked-off static camera. The dense stream of workers walks "
              "steadily away from camera down the covered path, perfectly "
              "even pace, nobody speaking, footsteps soft and synchronized. "
              "Dawn light through the shield slowly strengthens.",
           ["oren"], COLD_LOCK),
    "t2": (8, "Locked-off static camera. Oren stands motionless in the middle "
              "of the walkway staring straight up through the transparent "
              "shield, lips slightly parted; the stream of identical workers "
              "parts and flows around him like water around a piling, not one "
              "of them glancing at him; one worker's shoulder brushes his and "
              "Oren does not move.", ["oren"], COLD_LOCK),
    "t3": (6, "Locked-off static camera pointing straight up: the enormous "
              "living blue sky through the arched weather-shield, towering "
              "clouds drifting very slowly, morning light swelling almost "
              "imperceptibly. The shield ribs stay perfectly still. Wind, "
              "faint and far away.", [], COLD_LOCK),
    "t4": (5, "Locked-off static camera. The title text stays EXACTLY as in "
              "the start image, perfectly legible and unchanged. The only "
              "motion: condensation on the frosted glass drifts almost "
              "imperceptibly and the light brightens very slightly. Nothing "
              "else happens.", [], COLD_LOCK),
    "t5": (8, "Locked-off static wide. Hundreds of seated workers work their "
              "input panels in near-unison, small identical hand movements; "
              "Oren works among them, indistinguishable; the hall hums "
              "faintly. Nothing else moves.", ["oren"], COLD_LOCK),
    "t6": (7, "Locked-off static camera. The cafeteria murmurs with quiet "
              "identical eating. Somewhere across the hall a young woman "
              "laughs once — bright, unguarded, ringing — and Oren half-turns "
              "on his bench toward the sound, food forgotten, and keeps "
              "looking. Nobody else reacts at all. No words are spoken; the "
              "only human sound is that one laugh.", ["oren"], COLD_LOCK),
    "t7": (7, "Locked-off static camera. Low golden sunlight slides across "
              "the rows of pale screens, turning them briefly molten gold; "
              "Oren's face lifts into the warm light; then the UV filters "
              "adjust and the gold drains smoothly away back to grey, and his "
              "face falls slightly.", ["oren"], COLD_LOCK),
    "t8": (7, "Locked-off static close shot. Oren slowly presses his right "
              "hand flat against the cool white surface of the workstation "
              "and studies it — turning his attention across the lines of it "
              "— as if the hand belonged to someone else. He barely breathes. "
              "The screen glow flickers softly on his face.",
           ["oren"], COLD_LOCK),
    "t9": (7, "Locked-off static camera. Oren stands very still before the "
              "tall moisture stain shaped like a running figure, studying it "
              "the way one studies a painting in a gallery; after a long "
              "moment his head tilts a few degrees. Distant wind.",
           ["oren"], COLD_LOCK),
    "t10": (7, "Locked-off static camera. Oren crouches at the dead woody "
               "stem pushing through the cracked pavement and touches it "
               "lightly with one finger, tracing it upward, careful, as if "
               "it might wake. Quiet courtyard ambience.",
            ["oren"], COLD_LOCK),
    "t11a": (None, "Static two-shot in the pale office. Petra, behind the "
                   "desk, asks her questions kindly and precisely, hands "
                   "folded, while Oren sits opposite, upright and polite, "
                   "his eyes slightly elsewhere. Only Petra speaks.",
             ["petra", "oren"], COLD_LOCK),
    "t11b": (None, "Static two-shot in the pale office. Oren starts to "
                   "answer, stops mid-sentence — there is no next word — his "
                   "eyes drop, and after a long beat he finishes flatly. "
                   "Petra watches him a moment too long. Only Oren speaks, "
                   "and he speaks the COMPLETE exact words of the reference "
                   "audio, clearly and word for word — 'I'll re-baseline' "
                   "must be audible exactly as recorded — nothing added, "
                   "nothing changed.", ["petra", "oren"], COLD_LOCK),
    "t12": (None, "Static camera in the dusty archive light. Oren reads "
                  "aloud from the old book in a hushed whisper, tracing the "
                  "line with one finger; as he finishes, his whole body "
                  "responds like a struck bell — a small shiver, his breath "
                  "catching, his eyes lifting off the page into the middle "
                  "distance.", ["oren"], COLD_LOCK),
    "t13": (7, "Gentle handheld camera. Oren walks toward camera OUT through "
               "the complex gates against the dense inbound stream of "
               "identical workers, the only figure moving this way, his pace "
               "quickening, his face lifting into open golden morning light; "
               "the crowd flows past him indifferent.", ["oren"], WARM_LOCK),
    "t14": (None, "Gentle handheld camera, warm morning plaza. Oren stands "
                  "mid-story, both hands raised sketching the shape of the "
                  "sky, earnest and lit up; Dez laughs at him — delighted, "
                  "not unkind — speaks, and on her last words takes his hand "
                  "and pulls him out of frame; he stumbles after her, "
                  "half-laughing for the first time in his life.",
            ["oren", "dez"], WARM_LOCK),
    "t15": (8, "Gentle handheld camera drifting behind them. Oren and Dez "
               "walk side by side through the narrow warm streets under "
               "strings of hanging lights; his head turns everywhere at once "
               "— the lights, the laundry lines, the doorways — while she "
               "watches him discover it; faint unfamiliar street music "
               "drifts from an unseen doorway. No one speaks.",
            ["oren", "dez"], WARM_LOCK),
    "t16a": (None, "Static two-shot on the rooftop parapet at dusk, the warm "
                   "city below. Oren speaks fast and shining-eyed, gesturing "
                   "at the horizon; Dez watches him, smiling, starting to be "
                   "a little worried. Oren speaks the words of the reference "
                   "audio exactly ONCE and then the shot holds; no phrase is "
                   "ever repeated, no other words are spoken, Dez stays "
                   "silent.", ["oren", "dez"], WARM_LOCK),
    "t16b": (None, "Static two-shot on the rooftop parapet at dusk. Oren "
                   "finishes his thought quieter, almost pleading; Dez holds "
                   "his gaze and answers softly, and the smile she gives him "
                   "doesn't quite hold.", ["oren", "dez"], WARM_LOCK),
    "t17": (7, "Slow drifting handheld. Deep night on the rooftop: Oren "
               "alone, standing, wide awake, eyes open too wide, a faint "
               "tremor starting in his hands; the city lights seem to smear "
               "and swim around him, beautiful and far too much; his visible "
               "breath quickens.", ["oren"], WARM_LOCK),
    "t18": (8, "Locked-off static camera, harsh grey dawn. Oren wakes on the "
               "courtyard bench, jumpsuit rumpled, and sits hunched forward; "
               "his hands are visibly shaking and he squints against "
               "ordinary daylight as if it burned; his breathing is fast and "
               "shallow; the dead stem stands before him.", ["oren"], COLD_LOCK),
    "t19": (None, "Static camera, grey dawn courtyard. Oren, hunched and "
                  "trembling on the bench, speaks too fast, the words "
                  "spilling and cracking; Petra stands a few steps away, "
                  "her composed face failing — afraid, not of him, for him. "
                  "She answers with two quiet words, then slowly sits down "
                  "on the bench beside him, careful not to touch him.",
            ["petra", "oren"], COLD_LOCK),
    "t20a": (None, "Locked-off static frontal two-shot on the bench, the dead "
                   "stem between them. Oren is crying — the first tears of "
                   "his life, his face bewildered by them — and speaks "
                   "slowly, wrung out, looking at nothing. Petra sits beside "
                   "him looking straight ahead. Only Oren speaks.",
             ["petra", "oren"], COLD_LOCK),
    "t20b": (10, "Locked-off static frontal two-shot on the bench, the dead "
                 "stem between them. Petra, looking straight ahead, answers "
                 "with one quiet word. Then Oren asks his question — and she "
                 "does not answer. She keeps looking at the dead stem. The "
                 "rest of the shot is complete silence and stillness; nobody "
                 "moves, nobody speaks again.",
             ["petra", "oren"], COLD_LOCK),
    "t21": (8, "Locked-off static camera, white shadowless recalibration "
               "suite. Oren lies back calmly on the reclined chair, eyes on "
               "the ceiling; the smooth white instrument halo lowers slowly "
               "and silently toward his head; a technician makes one gentle "
               "unhurried adjustment at the console; as the halo settles, "
               "Oren's eyes close, peaceful. Nobody is cruel. Soft machine "
               "hum.", ["oren"], COLD_LOCK),
    "t22": (8, "Locked-off static camera — the exact composition of the "
               "opening shot. The stream of workers walks steadily away down "
               "the covered path at dawn, Oren among them now, in step, on "
               "time, eyes level; he passes the spot where he once stopped, "
               "and does not look up. The blue sky above the shield goes "
               "unregarded.", ["oren"], COLD_LOCK),
    "t23": (7, "Locked-off static camera. Oren works at his station among "
               "the hundreds, posture correct, face placid, hands moving in "
               "the same small unison as everyone else's; the pale screen "
               "light reflects in his calm eyes.", ["oren"], COLD_LOCK),
    "t24": (10, "Locked-off static close shot, long and quiet. Oren's right "
                "hand rests flat against the cool white surface; slowly his "
                "gaze comes down to it and stays there — the lines in it, "
                "the warmth of it — his placid face almost, almost changing; "
                "at the very end his fingers curl slightly against the "
                "surface. Hold. Silence except the hall's hum.",
            ["oren"], COLD_LOCK),
}


def adur(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True
    ).stdout.strip())


out = ["#!/bin/bash",
       "# THE VARIANCE first pass (auto-generated by make_videos.py)",
       "# Run: python3 pool_run_fast.py overwhelming_beauty/videos_tv1.sh "
       "overwhelming_beauty/outputs/tv1"]

for shot, (dur, staging, anchors, lock) in SHOTS.items():
    refs = " ".join(f"--image {A}/{a}.png" for a in anchors)
    frame = shot[:-1] if shot[-1] in "ab" else shot
    if shot in LINES:
        entries = LINES[shot]
        afiles = [VO / f"{shot}_{n}_{c}.mp3" for n, (c, _) in enumerate(entries, 1)]
        speech = sum(adur(p) for p in afiles)
        auto = min(15, max(5, int(speech + 2.5 + len(afiles) * 0.8)))
        dur = dur if dur else auto  # fixed dur wins (e.g. held silence)
        order = "; ".join(f"audio clip {n} is spoken by {CHAR_NAMES[c]}"
                          for n, (c, _) in enumerate(entries, 1))
        audio_lock = (f"The characters speak EXACTLY the dialogue heard in the "
                      f"reference audio clips, in order, lip-syncing to them "
                      f"precisely, in exactly those voices — never any other "
                      f"voice: {order}. No dialogue beyond the reference "
                      f"audio.")
        auds = " ".join(f"--audio overwhelming_beauty/vo/{p.name}" for p in afiles)
        prompt = f"{staging} {audio_lock} {lock} {NEG}"
        out.append(f'gen {shot} {dur} "{prompt}" '
                   f'--start-image {F}/{frame}.png {refs} {auds}')
    else:
        prompt = f"{staging} {SILENT} {lock} {NEG}"
        out.append(f'gen {shot} {dur} "{prompt}" '
                   f'--start-image {F}/{frame}.png {refs}'.rstrip())

sh = HERE / "videos_tv1.sh"
sh.write_text("\n".join(out) + "\n")
total = 0
for shot, (dur, _, _, _) in SHOTS.items():
    pass
print(f"wrote {sh} ({len(SHOTS)} shots)")
for shot in LINES:
    entries = LINES[shot]
    speech = sum(adur(VO / f"{shot}_{n}_{c}.mp3")
                 for n, (c, _) in enumerate(entries, 1))
    print(f"  {shot}: speech {speech:.1f}s")
