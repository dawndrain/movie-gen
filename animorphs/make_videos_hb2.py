#!/usr/bin/env python3
"""Emit videos_hb2.sh: dialogue-shot retakes with TTS audio refs + acted delivery.
Clip durations auto-sized from the audio (speech + headroom, clamped 5..12s)."""
import subprocess
from pathlib import Path

from vo_hb2 import LINES

HERE = Path(__file__).parent
VO = HERE / "vo"

NEG = ("Photorealistic epic sci-fi film, natural creature motion, correct anatomy. "
       "No random camera moves. No text or captions. Only characters visible on "
       "screen speak; no narrator. Characters keep exactly the same bodies, faces, "
       "blades, fur and colors as in the reference images.")
HB = ("Species lock: Hork-Bajir are seven-foot bipedal aliens with leathery "
      "green-brown skin, a crest of bone blades raked back from the skull, curved "
      "blades on forearms, elbows and knees, a spiked tail, and a hawk-beaked "
      "gentle face.")
AND = ("Species lock: Andalites are graceful alien centaurs with blue-and-tan fur, "
       "four legs, two slender arms, stalk eyes atop the head, a scythe-blade tail "
       "and NO mouth; when an Andalite speaks, the voice is heard telepathically "
       "while the face stays completely still.")

A = "animorphs/anchors"
F = "animorphs/frames"

# shot -> (base staging/acting prompt, [anchor refs], andalite_present)
SHOTS = {
    "f2": ("The red-tailed hawk perches still on a low branch, firelight flickering. The old scarred Hork-Bajir on the log leans toward it and tells the story slowly, warmly, like a grandfather beginning a bedtime tale, one clawed hand rising on the last words.", ["jara", "tobias"], False),
    "a2": ("Inside the dome at dusk. The young Andalite paces angrily behind her father, tail lashing on her bitter words; the old Andalite keeps gazing out at the valley and answers slowly, heavy with old shame, his stalk eyes drooping.", ["seerow", "aldrea"], True),
    "b2": ("Close on the young Hork-Bajir drawing careful circles in bark-dust. The stockier bark-brown one peers over his shoulder, genuinely puzzled. Dak looks up through the canopy with quiet wonder as he answers, eyes shining. Both characters speak the COMPLETE exact sentences of the reference audio, word for word, nothing shortened.", ["dak", "jagil"], False),
    "b3": ("The ancient grey Hork-Bajir elder raises both bladed arms over the kneeling young seer and pronounces the words with slow ceremonial weight; the watching circle is silent. The elder speaks ONLY the exact English words of the reference audio, clearly and completely — no alien language, no chanting, no added words.", ["dak"], False),
    "b4": ("First meeting, wary and slow: the young Hork-Bajir freezes mid-step and speaks haltingly, half afraid. The Andalite holds very still, tail blade lowered, and answers gently, carefully, like calming a wild animal.", ["dak", "aldrea"], True),
    "b5": ("Night. A blue holographic star map spins between them, painting their faces with light. Her telepathic voice is soft, patient, a teacher sharing a secret. Dak reaches one careful claw toward a projected world and breathes his answer, hushed, hungry with longing.", ["dak", "aldrea"], True),
    "b6": ("Comedy beat: the Andalite leaps between branches and lands badly, all four legs splayed, dignity gone. The young Hork-Bajir throws his head back and roars the line through helpless honking laughter, pointing at her; her stalk eyes glare with wounded dignity.", ["dak", "aldrea"], True),
    "c1": ("They climb down a root the size of a cathedral wall into blue bioluminescent darkness. Her telepathic voice echoes hushed and tense, half excitement, half fear, slowing on the final words.", ["dak", "aldrea"], True),
    "c3": ("The two tiny silhouettes stand on the ledge as the hidden amber city glows below. Dak whispers the line in pure awe, barely audible, each word separated by wonder.", ["dak", "aldrea"], False),
    "c4": ("The small iridescent Arn stalks toward the intruders, crest flaring crimson, one thin arm pointing in outrage; it spits the words with reedy aristocratic contempt, biting off each sentence.", ["arn", "dak", "aldrea"], False),
    "c5": ("The Arn sweeps a thin arm along the wall of turquoise gene-tanks with embryonic shapes floating inside, declaiming with pitiless pride, savoring the cruelty of the final three words while the young Hork-Bajir stares frozen at his own reflection in the glass.", ["arn", "dak"], False),
    "c6": ("Quiet devastation in blue fungal light. Dak sits slumped, staring at his open claws, and speaks his line hollowed-out and slow, a man whose world has ended. Aldrea lays her hand on his shoulder; her answer is fierce and gentle, tightening on the word choose.", ["dak", "aldrea"], True),
    "d2": ("The harnessed Hork-Bajir-Controller studies the rotating tactical hologram and speaks softly, coldly, savoring each item of the list, ending with relish on the final word. Orange light plays over his cruel eyes.", ["esplin"], False),
    "d4": ("Dusk. Dak searches his friend's face, worried, his questions gentle and mounting with fear. The stocky one stands too still and answers flat and dead, a pause before the word better, eyes empty. Dak's head draws back in dread.", ["dak", "jagil"], False),
    "d5": ("Night attack: crimson beams rake the burning dome. The old Andalite wheels toward his daughter, main eyes wide with terror, and his telepathic voice cracks like thunder on the single desperate command as she gallops from the blast light.", ["seerow", "aldrea"], True),
    "d6": ("Grey dawn. The young Andalite walks slowly through the smoking skeleton of the dome, ash drifting like snow. Her telepathic voice is numb and flat, each name a small collapse, barely finishing the last sentence.", ["aldrea"], True),
    "e1": ("Storm-grey morning argument, raw and naturalistic. She leans in urgent and pleading, voice cracking with grief. A long pause. Dak turns half away, gripping the bark until it splinters, and answers slowly, torn, almost a whisper. She steps closer; a beat of silence; her last line lands quiet, hard, final.", ["dak", "aldrea"], True),
    "e2": ("Strange quiet moment: she presses her hand flat on his chest; his eyes drift calm and trance-like as a faint shimmer passes between them. His question is dreamy, far away. Her answer is a soft murmur with the ghost of a smile.", ["dak", "aldrea"], True),
    "e4": ("Training in beginning rain: Dak demonstrates a slow blade-block stance before a ragged line of free Hork-Bajir who copy him clumsily; he calls out the line steady and grave, then holds the stance in silence. He speaks ONLY the words of the reference audio and nothing more.", ["dak", "aldrea_hb"], False),
    "e5": ("After the ambush, rain: Dak stands over the fallen harnessed enemy, blades lowered, chest heaving, and speaks with grief, almost to himself, breaking on the final question. The free Hork-Bajir behind him look away. No gore.", ["dak"], False),
    "e6": ("The Controller commander turns slowly from the battle-report hologram, head tilting with predatory delight, and purrs the lines cold and silky, ending almost tenderly on the last three words as he gazes at the viewport.", ["esplin"], False),
    "g1": ("Dawn on the scorched ridge before eight ivory fighters: the scarred war-prince surveys the smoke rising from the valley and states the lines flat and contemptuous, a soldier reporting a death sentence; his tail blade flicks once.", ["alloran"], True),
    "g2": ("Face-off in the dome wreckage, circling slowly, tails half-raised. His voice is clipped, icy, final. Hers blazes back, shaking with fury on the number, contempt sharpening the final two words. Neither face moves.", ["alloran", "aldrea"], True),
    "g3": ("Close-up: the war-prince's hand raises the crystalline vial, sickly blue-white light swirling inside, reflected in his cold eyes. His telepathic voice is quiet, measured, and utterly final, a long pause at the ellipsis.", ["alloran"], True),
    "g5": ("Ambush chaos at night: crimson beams streak the dark, bark exploding; Dak is thrown backward clutching his side; the glowing vial spins from his claw into the abyss and bursts into blue-white mist far below. Her single telepathic scream — the exact cry heard in the reference audio — rings out LOUD and clear above the explosion noise, raw terror, unmistakable.", ["dak", "aldrea"], True),
    "h1": ("Sunrise between them. Dak, wounded side bound with bark, speaks first, dreading the answer, trailing away. She steps closer, calm and sure, and answers with quiet unshakable love, now speaking aloud through a Hork-Bajir mouth. Their foreheads touch at the end, blades carefully apart.", ["dak", "aldrea_hb"], False),
    "h2": ("The highest thin branches above the clouds, dawn: the ragged band shelters in the woven hide. Dak stands watch at the edge and speaks quietly, steady as stone, a vow rising with strength on the final sentence. Wind and creaking branches under it.", ["dak", "aldrea_hb"], False),
    "h3": ("Alone at the tall viewport, the conquered green world turning below, the Controller commander speaks to no one, cold and silky, savoring his own name, a slow breath before the final word, ambition burning quietly.", ["esplin"], False),
    "i1": ("Dusk on Earth, embers rising. The old scarred Hork-Bajir spreads both bladed arms wide and finishes the tale, warm and proud and sad at once, slowing with reverence on the alien word. The hawk shifts its wings.", ["jara", "tobias"], False),
    "i2": ("The slender adolescent female Hork-Bajir steps into the firelight. The old one introduces her with quiet pride. She looks directly at the hawk and speaks clearly, young and bright with gravel underneath, utterly certain of the final three words.", ["toby", "jara", "tobias"], False),
}


def adur(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


lines_out = [
    "#!/bin/bash",
    "# hb2 retake round: dialogue shots with TTS audio refs (auto-generated by make_videos_hb2.py)",
    "# Run: python3 pool_run.py animorphs/videos_hb2.sh animorphs/outputs/hb2",
]

# e1 is too long for one clip: split across two takes of the same setup.
SPLITS = {
    "e1": [
        ("e1a", ["e1_1_aldrea"],
         "Storm-grey morning, raw and naturalistic. The young Andalite leans urgently "
         "toward the Hork-Bajir, tail blade quivering, her telepathic voice pleading "
         "and cracking with grief while he listens frozen, gripping the bark. She "
         "speaks the reference audio exactly ONCE and then the shot holds in tense "
         "silence; no phrase is ever repeated."),
        ("e1b", ["e1_2_dak", "e1_3_aldrea"],
         "Storm-grey morning, raw and naturalistic. The Hork-Bajir turns half away, "
         "gripping the bark until it splinters, and answers slowly, torn, almost a "
         "whisper. The Andalite steps closer; a beat of silence; her final line lands "
         "quiet, hard, resolute, her main eyes locked on his."),
    ],
}

render_jobs = []
for shot, (staging, anchors, andalite) in SHOTS.items():
    if shot in SPLITS:
        for sub, files, sub_staging in SPLITS[shot]:
            render_jobs.append((sub, shot, sub_staging, anchors, andalite,
                                [VO / f"{f}.mp3" for f in files],
                                [f.split("_", 2)[2] if f.split("_")[1].isdigit() else f
                                 for f in files]))
        continue
    entries = LINES[shot]
    afiles = [VO / f"{shot}_{n}_{char}.mp3" for n, (char, _) in enumerate(entries, 1)]
    chars = [char for char, _ in entries]
    render_jobs.append((shot, shot, staging, anchors, andalite, afiles, chars))

for shot, frame, staging, anchors, andalite, afiles, chars in render_jobs:
    speech = sum(adur(p) for p in afiles)
    dur = min(15, max(5, int(speech + 2.5 + len(afiles) * 0.8)))
    order = "; ".join(
        f"audio clip {n} is spoken by {'the ' + c if c in ('elder', 'arn') else c.replace('_', ' ').title()}"
        for n, c in enumerate(chars, 1))
    audio_lock = (f"The characters speak EXACTLY the dialogue heard in the reference "
                  f"audio clips, in order, lip-syncing to them precisely, in exactly "
                  f"those voices — never any other voice: {order}. No dialogue beyond "
                  f"the reference audio.")
    species = HB + (" " + AND if andalite else "")
    prompt = f"{staging} {audio_lock} {species} {NEG}"
    refs = " ".join(f"--image {A}/{a}.png" for a in anchors)
    auds = " ".join(f"--audio animorphs/vo/{p.name}" for p in afiles)
    lines_out.append(
        f'gen {shot} {dur} "{prompt}" --start-image {F}/{frame}.png {refs} {auds}')

# torso-locked gallop retake (silent)
lines_out.append(
    'gen a3 6 "The young Andalite female gallops at full stride along the grassy '
    'ridge above the colossal-tree valley, golden light. CRITICAL anatomy lock, '
    'never violated: she is a centaur with SIX limbs - four deer legs on the ground '
    'AND an upright humanoid torso with two slender arms and a head rising '
    'vertically from the shoulders of the four-legged body; the upright torso, arms '
    'and head stay clearly visible above the galloping legs in every single frame; '
    'she is never a simple four-legged deer. Her long tail with its scythe blade '
    'streams behind. Medium-close side tracking shot keeping her whole body large '
    f'in frame. Hooves drumming, wind. No dialogue. {NEG}" '
    f'--start-image {F}/a3.png --image {A}/aldrea.png')

out = HERE / "videos_hb2.sh"
out.write_text("\n".join(lines_out) + "\n")
print(f"wrote {out} ({len(SHOTS) + 1} shots)")
for shot, (_, _, _) in SHOTS.items():
    entries = LINES[shot]
    speech = sum(adur(VO / f"{shot}_{n}_{c}.mp3") for n, (c, _) in enumerate(entries, 1))
    print(f"  {shot}: speech {speech:.1f}s")
