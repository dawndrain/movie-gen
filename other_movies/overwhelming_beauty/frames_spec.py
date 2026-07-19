"""Scene start-frame prompts for THE VARIANCE. Loaded by make_images.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from make_images import COLD, WARM, OREN, PETRA, DEZ

MATCH = ("Characters exactly match the reference images in face, hair, build "
         "and clothing.")

# (name, aspect, prompt, [anchor refs])
FRAMES = [
    # ---- Act 1: specification ----
    ("t1", "16:9",
     "Dawn. A long covered commuter path beneath an arched transparent "
     "weather-shield: a dense silent stream of workers in identical slate-blue "
     "jumpsuits walks away from camera toward a distant fabrication complex, "
     "evenly spaced, nobody talking. Deep blue morning sky visible through the "
     f"shield glass. Locked-off symmetrical wide shot. {MATCH} {COLD}",
     ["oren", "loc_path"]),
    ("t2", "16:9",
     f"On the covered commuter path at dawn, {OREN} has stopped dead in the "
     f"middle of the walkway and stands looking straight up at the sky through "
     f"the transparent shield, face slack with something new, while the stream "
     f"of identical workers parts and flows around him like water around a "
     f"piling, none of them glancing at him. {MATCH} {COLD}",
     ["oren", "loc_path"]),
    ("t3", "16:9",
     "Looking straight up from below through the transparent arched "
     "weather-shield: the sky — deep, living, enormous blue with slow towering "
     "clouds catching first light, the shield's thin ribs framing it. The sky "
     "is the most alive thing in the film. Almost abstract. No people. "
     f"{COLD}", ["loc_path"]),
    ("t4", "16:9",
     "Movie title card: over an empty frame of flat pale grey — the exact "
     "texture of an overcast institutional sky seen through frosted glass — "
     "small precise pale-blue sans-serif letters in the exact center read "
     "exactly: \"THE VARIANCE\". The title text must be spelled exactly as "
     "given, in clean thin type, nothing else in frame. No other text. "
     f"{COLD}", []),
    ("t5", "16:9",
     f"Interior, vast fabrication hall: hundreds of identical white "
     f"workstations in perfect receding rows, a uniformed worker seated "
     f"motionless at each; in the middle distance {OREN} sits at his station "
     f"among them, one of many, facing his pale screen. High frosted "
     f"skylights, even shadowless light. Locked-off wide. {MATCH} {COLD}",
     ["oren", "loc_fab"]),

    # ---- Act 2: the drawer ----
    ("t6", "16:9",
     f"Institutional cafeteria: long pale tables of uniformed workers eating "
     f"quietly and identically. In the foreground {OREN} has half-turned on "
     f"his bench, chopsticks forgotten, looking across the hall toward a "
     f"table where a young woman is caught mid-laugh, head back — the only "
     f"motion in the room. {MATCH} {COLD}", ["oren", "loc_cafeteria"]),
    ("t7", "16:9",
     f"Late afternoon in the fabrication hall: low sun slips under the "
     f"skylight louvres and the rows of pale screens catch it, turning "
     f"briefly molten gold — a wash of warm light across the grey hall. "
     f"{OREN} sits at his station, face lit gold, watching the light instead "
     f"of the data. {MATCH} {COLD}", ["oren", "loc_fab"]),
    ("t8", "16:9",
     f"Close shot: {OREN} at his workstation, his right hand pressed flat "
     f"against the cool white surface beside the input panel; he is looking "
     f"down at his own hand — the lines in it, the warmth of it — as if it "
     f"belonged to someone else. Screen glow on his face. {MATCH} {COLD}",
     ["oren", "loc_fab"]),
    ("t9", "16:9",
     f"A bare concrete wall where years of moisture have left a tall rust-grey "
     f"stain uncannily shaped like a human figure mid-stride, running. {OREN} "
     f"stands before it at a respectful distance, hands at his sides, studying "
     f"it the way one studies a painting in a gallery. {MATCH} {COLD}",
     ["oren", "loc_courtyard"]),
    ("t10", "16:9",
     f"The small concrete courtyard behind a dormitory block: {OREN} crouches "
     f"at the center where a single dead woody plant stem pushes up through "
     f"cracked pavement, waist-high, dead but structural, like a monument. One "
     f"of his fingers touches it lightly. The weathered bench behind him. "
     f"{MATCH} {COLD}", ["oren", "loc_courtyard"]),
    ("t11", "16:9",
     f"A minimal pale office: {PETRA} sits behind a white desk, composed, "
     f"hands folded, regarding {OREN} who sits opposite her in his slate-blue "
     f"jumpsuit, upright, polite, but his eyes slightly elsewhere. Frosted "
     f"glass wall behind her. Two-shot in profile, symmetrical. {MATCH} "
     f"{COLD}", ["petra", "oren"]),

    # ---- Act 3: eleven days ----
    ("t12", "16:9",
     f"The forgotten archive room: {OREN} stands in a shaft of dusty light "
     f"between steel shelves of old paper books, one book open in his hands, "
     f"lips just parted as he reads aloud to himself in a whisper; other "
     f"opened books lie around him. The dust glitters. First hint of warmth "
     f"in the grade. {MATCH} {COLD}", ["oren", "loc_archive"]),
    ("t13", "16:9",
     f"Morning: {OREN} walks OUT through the wide gates of the fabrication "
     f"complex, against the dense inbound stream of identical workers, the "
     f"only figure moving toward camera into open unshielded golden light, "
     f"his face lifting into it. Handheld energy. {MATCH} {WARM}",
     ["oren", "loc_path"]),
    ("t14", "16:9",
     f"A small plaza where districts meet, morning light: {OREN} stands "
     f"mid-story, both hands raised sketching the shape of the sky, and "
     f"{DEZ} laughs at him — delighted, head tilted — reaching out to take "
     f"his hand. Around them, varied non-uniformed people pass. {MATCH} "
     f"{WARM}", ["oren", "dez", "loc_oldquarter"]),
    ("t15", "16:9",
     f"The old quarter at dusk: narrow crooked brick streets under strings of "
     f"warm hanging lights, laundry lines, doorways spilling amber light and "
     f"faint music. {OREN} and {DEZ} walk side by side through it, his head "
     f"turning everywhere at once, her watching him discover it. {MATCH} "
     f"{WARM}", ["oren", "dez", "loc_oldquarter"]),
    ("t16", "16:9",
     f"A flat rooftop at dusk, the old quarter glowing warm below and the "
     f"pale ordered district grey in the far distance: {OREN} sits on the "
     f"parapet edge beside {DEZ}, mid-sentence, gesturing at the horizon, "
     f"eyes shining too bright; she watches him with a slight worried "
     f"tenderness. {MATCH} {WARM}", ["oren", "dez", "loc_oldquarter"]),
    ("t17", "16:9",
     f"Deep night on the same rooftop: {OREN} alone, standing, wide awake, "
     f"eyes open too wide, faint tremor in his hands, the city lights "
     f"smearing into streaks around him — beautiful and far too much. His "
     f"breath is visible. {MATCH} {WARM}", ["oren", "loc_oldquarter"]),

    # ---- Act 4: variance collapse ----
    ("t18", "16:9",
     f"Grey harsh dawn in the concrete courtyard: {OREN} sits on the "
     f"weathered bench where he slept, jumpsuit rumpled, hunched forward, "
     f"hands visibly shaking, squinting against ordinary daylight as if it "
     f"burned. The dead stem in the pavement before him. Overexposed, "
     f"aching light. {MATCH} {COLD}", ["oren", "loc_courtyard"]),
    ("t19", "16:9",
     f"The courtyard, grey dawn: {PETRA} stands a few steps from the bench "
     f"looking down at {OREN} — hunched, trembling, wild-eyed — and her "
     f"composed face is failing for the first time: she is afraid, not of "
     f"him, for him. {MATCH} {COLD}", ["petra", "oren", "loc_courtyard"]),
    ("t20", "16:9",
     f"The courtyard bench: {PETRA} now sits beside {OREN}, careful not to "
     f"touch him. He is crying — the first tears of his life, his face "
     f"bewildered by them. She looks straight ahead at the dead stem in the "
     f"pavement. Quiet two-shot, locked off. {MATCH} {COLD}",
     ["petra", "oren", "loc_courtyard"]),
    ("t21", "16:9",
     f"The recalibration suite, white and soft and shadowless: {OREN} lies "
     f"back calmly on the reclined padded chair, eyes open at the ceiling, "
     f"while the smooth white instrument halo lowers toward his head; a "
     f"technician in pale clothing stands at a console, gentle, unhurried. "
     f"No restraints. Nobody is cruel. {MATCH} {COLD}",
     ["oren", "loc_recal"]),

    # ---- Act 5: baseline ----
    ("t22", "16:9",
     f"Dawn on the covered commuter path — the exact composition of the "
     f"opening shot: the silent stream of slate-blue workers walking away "
     f"from camera, and {OREN} among them now, in step, on time, eyes level, "
     f"not looking up. The blue sky above the shield, ignored. Locked-off "
     f"symmetrical wide. {MATCH} {COLD}", ["oren", "loc_path"]),
    ("t23", "16:9",
     f"The fabrication hall: {OREN} seated at his workstation among the "
     f"hundreds, posture correct, face placid, the pale screen reflecting in "
     f"his calm eyes. Everything at baseline. {MATCH} {COLD}",
     ["oren", "loc_fab"]),
    ("t24", "16:9",
     f"Final close shot: {OREN}'s right hand pressed flat against the cool "
     f"white surface of his workstation, fingers spread; above it his placid "
     f"face looking down at the hand — at the lines in it, the warmth of it "
     f"— with no expression he has a word for. Screen glow, silence. {MATCH} "
     f"{COLD}", ["oren", "loc_fab"]),
]
