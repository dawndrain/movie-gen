"""The Long Game — film spec (data for tools/assemble.py).
Reproduces the v18 cut (credits ending) exactly; see storyboard_v18.html."""
from pathlib import Path

ROOT = Path(__file__).parent
OUT = "outputs/previews/preview_v18.mp4"
GRAPH = "outputs/assemble_v18_graph.txt"
SIZE = (854, 480)
FPS = 24

# (clip path, trim_start, trim_dur, mute, era_mark) — era_mark starts a music span
CUT = [
    (ROOT / "outputs/video14/t0_longgame.mp4", 0, None, False, 'omen'),
    (ROOT / "outputs/video6/a6_sign2.mp4", 0, None, False, 'silence'),
    (ROOT / "outputs/video3/a7_dibs.mp4", 0, None, False, None),
    (ROOT / "outputs/white_flash.mp4", 0, None, False, None),
    (ROOT / "outputs/video8/a_ski3.mp4", 0, None, False, None),
    (ROOT / "outputs/video9/a8_out3.mp4", 0, None, False, None),
    (ROOT / "outputs/video12/a_hard_fix.mp4", 0, None, False, None),
    (ROOT / "outputs/video11/b1_wake5.mp4", 0, None, False, 'silence'),
    (ROOT / "outputs/video2/2_2_water_carry.mp4", 0, None, False, 'bronze'),
    (ROOT / "outputs/video3/b3_goat.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/b12_cough.mp4", 0, None, False, 'silence'),
    (ROOT / "outputs/video6/b5_afterlife2.mp4", 0, None, False, None),
    (ROOT / "outputs/video12/b6_fix.mp4", 0, None, False, None),
    (ROOT / "outputs/video14/b7_name3_bronze.mp4", 0, None, False, None),
    (ROOT / "outputs/video14/b8_leave2.mp4", 0, None, False, None),
    (ROOT / "outputs/video/2_5_touched_woman.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/b10_forty.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/b12_cough.mp4", 0, None, False, None),
    (ROOT / "outputs/video10/w1d.mp4", 0, None, False, None),
    (ROOT / "outputs/video6/b13_cry2.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/b14_three_lives.mp4", 0, None, False, None),
    (ROOT / "outputs/video10/w2d.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/b15_five_lives.mp4", 0, 3.5, False, None),
    (ROOT / "outputs/video10/w3d.mp4", 0, None, False, None),
    (ROOT / "outputs/video6/b16_cure3.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/b17_rant.mp4", 0, 2.9, False, None),
    (ROOT / "outputs/video3/b17_rant.mp4", 6.95, None, False, None),
    (ROOT / "outputs/video3/b18_germs.mp4", 0, None, False, None),
    (ROOT / "outputs/video7/b19_isa.mp4", 0, None, False, None),
    (ROOT / "outputs/video5/b20_solemn2.mp4", 0, None, False, None),
    (ROOT / "outputs/video8/b21_party3.mp4", 0, None, False, None),
    (ROOT / "outputs/video7/b22_wish3.mp4", 0, None, False, None),
    (ROOT / "outputs/video5/b23_finally2.mp4", 0, None, False, 'omen_b23'),
    (ROOT / "outputs/video6/r1_sigh.mp4", 0, None, False, 'silence'),
    (ROOT / "outputs/video7/r2_aq3.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/r3_gesture_q.mp4", 0, None, False, None),
    (ROOT / "outputs/video9/r4_boil3.mp4", 0, None, False, None),
    (ROOT / "outputs/video5/r5_library2.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/r6_scroll.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/r7_bath_pitch.mp4", 0, None, False, None),
    (ROOT / "outputs/video13/r8_glass2.mp4", 0, None, False, None),
    (ROOT / "outputs/video13/r9_acid3.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/r10_page.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/r11_dictate_blood.mp4", 0, None, False, None),
    (ROOT / "outputs/video7/r12_salt4.mp4", 0, None, False, None),
    (ROOT / "outputs/video7/r13_sweet3.mp4", 0, None, False, None),
    (ROOT / "outputs/video4/n1_bridge.mp4", 0, None, False, 'ren_a'),
    (ROOT / "outputs/video4/n2_widow.mp4", 0, None, False, None),
    (ROOT / "outputs/video4/n3_card.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/e1_library2.mp4", 0, None, False, 'silence'),
    (ROOT / "outputs/video3/e2_fire.mp4", 0, 6.9, False, None),
    (ROOT / "outputs/video4/n4_fireflash.mp4", 0, None, False, None),
    (ROOT / "outputs/video3/e2_fire.mp4", 6.9, None, False, None),
    (ROOT / "outputs/video3/e3_flood.mp4", 0, None, False, None),
    (ROOT / "outputs/video4/n5_type.mp4", 0, None, False, 'ren_b'),
    (ROOT / "outputs/video3/e4_montage.mp4", 0, None, False, None),
    (ROOT / "outputs/video4/n6_boiler.mp4", 0, None, False, 'boiler'),
    (ROOT / "outputs/video4/n7_again.mp4", 0, None, False, 'silence'),
    (ROOT / "outputs/video4/n8_gauge.mp4", 0, None, False, None),
    (ROOT / "outputs/video13/n9_sixty3.mp4", 0, None, False, 'm1926'),
    (ROOT / "outputs/video5/m1_wake2.mp4", 0, None, False, None),
    (ROOT / "outputs/video5/m2_tram2.mp4", 0, None, False, None),
    (ROOT / "outputs/video12/m3_fix.mp4", 0, None, False, None),
    (ROOT / "outputs/video4/m4_teach.mp4", 0, None, False, None),
    (ROOT / "outputs/video7/m5_feet2.mp4", 0, None, False, None),
    (ROOT / "outputs/video4/m6_longtime.mp4", 0, None, False, None),
    (ROOT / "outputs/video4/m7_obit.mp4", 0, None, False, None),
    (ROOT / "outputs/video11/p1_dinner2.mp4", 0, None, False, 'warmtail'),
    (ROOT / "outputs/video14/p2_board4.mp4", 0, None, False, None),
    (ROOT / "outputs/video12/p3_fix.mp4", 0, None, False, 'machine'),
    (ROOT / "outputs/video7/p4_exit3.mp4", 0, None, False, 'silence'),
    (ROOT / "outputs/video5/q1_off2.mp4", 0, None, False, 'silence'),
    (ROOT / "outputs/video12/q2_fix.mp4", 0, None, False, None),
    (ROOT / "outputs/video16/q3_walk2.mp4", 0, None, False, None),
    (ROOT / "outputs/video6/q4_real2.mp4", 0, None, False, 'omen_q4'),
    (ROOT / "outputs/video4/q5_nested.mp4", 0, None, False, 'silence'),
    (ROOT / "outputs/video4/q6_longtime2.mp4", 0, None, False, None),
    (ROOT / "outputs/video6/q7_fail2.mp4", 0, 7.5, False, 'silence'),
    (ROOT / "outputs/credits.mp4", 0, None, False, 'silence'),
]

MUS_DIR = "music"
MUSIC = {
    "omen": {"file": "mus_omen.m4a", "vol": 0.4, "fade_in": "span"},
    "arcade": {"file": "mus_arcade2.m4a", "vol": 0.08},
    "bronze": {"file": "mus_bronze.m4a", "vol": 0.09},
    "omen_b23": {"file": "mus_omen.m4a", "vol": 0.16},
    "ren_a": {"file": "mus_ren.m4a", "vol": 0.07},
    "ren_b": {"file": "mus_ren.m4a", "vol": 0.12},
    "boiler": {"file": "mus_boiler.m4a", "vol": 0.2},
    "m1926": {"file": "mus_1926.m4a", "vol": 0.06, "fade_out": 0.25},
    "machine": {"file": "mus_machine.m4a", "vol": 0.09},
    "omen_q4": {"file": "mus_omen.m4a", "vol": 0.14},
    "end": {"file": "mus_end.m4a", "vol": 0.1},
}
SPAN_MERGES = [("warmtail", "m1926", 3.0)]  # warm 1926 cue runs 3s into the dinner, then cuts hard

AMB_DIR = "ambience"
# (start_stem, end_stem, bed, dB offset) — beds normalized to -30 LUFS; anchor -22.4 LUFS
AMBIENCE = [
    ("a6_sign2", "a_ski3", "amb_arcade_n.m4a", "-12dB"),
    ("a8_out3", "b1_wake5", "amb_arcade_n.m4a", "-12dB"),
    ("b1_wake5", "b21_party3", "amb_bronze_n.m4a", "-16dB"),
    ("r7_bath_pitch", "r8_glass2", "amb_baths_n.m4a", "-12dB"),
    ("r8_glass2", "n1_bridge", "amb_workshop_n.m4a", "-16dB"),
    ("n1_bridge", "e1_library2", "amb_ren_city_n.m4a", "-16dB"),
    ("m1_wake2", "p1_dinner2", "amb_1926_n.m4a", "-16dB"),
    ("q1_off2", "q3_walk2", "amb_arcade_n.m4a", "-12dB"),
]

GRADE = {'q7_fail2': 'fade=t=out:st=6.7:d=0.8,'}
AFADE = {'q7_fail2': (6.9, 0.6)}
FREEZE = {}
