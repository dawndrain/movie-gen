#!/bin/bash
# Overnight video pass: Chapters I-IV at 480p std (full quality mode), storyboard frames as start-images.
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video
V=outputs/video; F=frames; A=anchors
gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>/dev/null | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

# --- Chapter I: The Arcade ---
gen 1_1_arcade_wide 10 "The tall teenager dances on the DDR pad in deliberate theatrical slow motion, missing arrows with perfect grace, laughing, while his friend films him on a phone and cheers; neon light pulses across the arcade; ambient sound of arcade machines, chiptune music, and teenage laughter" --start-image $F/1_1_arcade_wide.png --image $A/deshawn.png --image $A/milo.png &
gen 1_2_placard 5 "The boy reads the maintenance placard intently, then glances once toward his laughing friends off-screen and back to the placard; slow camera push-in; distant arcade noise, muffled laughter" --start-image $F/1_2_placard.png --image $A/cass_17.png &
gen 1_3_approach 8 "Three teenage boys walk fast toward the camera and the ominous white machine, jostling each other, shoving shoulders, pretending to be dragged toward it, grinning; camera slowly pulls back ahead of them; their footsteps and laughter against a low ominous hum that grows" --start-image $F/1_3_approach.png &
wait
gen 1_4_screen_cu 5 "Slow steady camera push-in on the glowing screen text and the yellow out-of-service tape; the screen flickers once very slightly; low electronic hum, the arcade noise fading away" --start-image $F/1_4_screen_cu.png &
gen 1_5_deshawn_chair 10 "The boy in the reclined chair twitches his hands, his mouth moves silently, then he laughs out loud at something no one can see, then tears the headset off gasping, eyes wet wide and delighted, sitting up all at once; his friends lean in; he gasps a jumble of joyful words about gold medals; arcade ambience" --start-image $F/1_5_deshawn_chair.png --image $A/deshawn.png &
gen 1_6_toggle 8 "The grinning boy with glasses flips the small toggle switch from ON to OFF with one finger, then looks up; off-screen a voice says warmly 'Have a good life'; the machine's screen floods the frame with white light growing until the whole image goes white; a rising electronic tone then silence" --start-image $F/1_6_toggle.png --image $A/milo.png &
wait

# --- Chapter II: Day Zero ---
gen 2_1_eye_open 5 "The eye snaps open, pupil contracting, the boy's breath comes fast and visible in the cold air, his cheek pressed against the packed earth, small trembling; cold wind, distant animal sounds, embers settling" --start-image $F/2_1_eye_open.png &
gen 2_2_water_carry 8 "The boy trudges through the mud carrying the heavy yoke of water pots, slipping slightly and recovering, breath visible, wind flattening the grass; handheld camera follows beside him; cold wind, creaking wood, sloshing water, morning birds" --start-image $F/2_2_water_carry.png --image $A/cass_17.png &
gen 2_3_mother 8 "The mother rocks the fevered boy slowly against her chest, one hand smoothing his hair, and quietly hums an old melody; firelight flickers over them; his breathing is shallow; the fire crackles softly under her low humming" --start-image $F/2_3_mother.png &
wait
gen 2_4_reset 8 "The boy bolts upright from the packed earth floor gasping, looks at his own hands in horror, the scene cuts hard back to him lying down and he bolts upright again in identical framing, and again, a repeating loop of the same waking, each gasp identical; disorienting match-cut rhythm; each cut punctuated by a sharp intake of breath" --start-image $F/2_1_eye_open.png --image $A/cass_17.png &
gen 2_5_touched_woman 8 "The old woman grips the boy's arm, her eyes suddenly completely clear, and speaks directly to him: 'Then you'll have to live it. All of it. Forty summers, child.' Then her eyes drift away and she resumes muttering to the empty air, releasing his arm; the boy stands stricken; cold wind" --start-image $F/2_5_touched_woman.png --image $A/touched_woman.png --image $A/cass_17.png &
wait

# --- Chapter III: Bronze ---
gen 3_1_salt_water 8 "The teenage boy carefully spoons water into the sick child's mouth; the child swallows weakly, then again more strongly; the mother presses her hands to her mouth; villagers murmur at the doorway; the fire crackles; a soft murmur of awe passes through the onlookers" --start-image $F/3_1_salt_water.png --image $A/cass_17.png &
gen 3_2_bronze_pour 8 "Molten bronze pours in a bright ribbon from the crucible into the stone mold, sparks bursting upward, the young man directing with a raised hand, smiths straining, orange light dancing on every face; roar of the fire, hiss of the pour, awed silence of the watchers" --start-image $F/3_2_bronze_pour.png --image $A/cass_28.png &
gen 3_3_water_greeting 10 "The bearded young man slowly circles his flat hand over the steaming pot of water, speaking low ceremonial words, and the villagers around the fire watch and then mirror the gesture with their own hands, one small child copying it seriously; firelight flickers; the water bubbles softly under his quiet chant" --start-image $F/3_3_water_greeting.png --image $A/cass_28.png &
wait
gen 3_4_bored_king 8 "The young king slouches on his throne, chin on fist, eyes drifting over the feast without landing on anything; a musician plays, chieftains laugh and toast him, a server refills his cup; he exhales slowly through his nose; drums and pipes and hall noise around his silence" --start-image $F/3_4_bored_king.png &
gen 3_5_slave_nod 6 "Across the crowded firelit hall, the old slave woman lifts her head, meets the king's eye, and nods once, slowly; the king holds her gaze and nods back; around them the feast blurs and its noise falls away to almost nothing; then she is muttering to the air again and the noise returns" --start-image $F/3_5_slave_nod.png --image $A/touched_woman.png &
gen 3_6_roman_wake 8 "The man lies utterly still on the raised bed, only his eyes moving, taking in the latticed window and the strange ceiling; morning light shifts slowly across him; his hand slowly closes on the linen sheet; a fountain runs somewhere below, birdsong, his own breathing" --start-image $F/3_6_roman_wake.png --image $A/cass_45.png &
wait

# --- Chapter IV: Roman ---
gen 4_1_aqueduct 8 "Extreme wide shot, the camera rises slowly and steadily upward, the tiny figure of the man standing motionless on the road beneath the immense striding aqueduct, heat shimmer over the valley; wind, distant water in the channel, cicadas" --start-image $F/4_1_aqueduct.png &
gen 4_2_fountain_gesture 10 "The kneeling woman makes her small slow circling gesture over the water, murmurs to it, then dips her jar and fills it; behind her the walking man stops dead mid-stride, staring at her hand, and does not move again for the rest of the shot; the street sounds fall away until only the fountain remains" --start-image $F/4_2_fountain_gesture.png --image $A/cass_45.png &
gen 4_3_legend_scroll 6 "The man reads the scroll by the window; a short laugh escapes him, and then his face falls apart a little around the laugh, and he lowers the scroll and looks out the window; the parlor is quiet, a bird outside, the scroll paper crackling" --start-image $F/4_3_legend_scroll.png --image $A/cass_45.png &
wait
gen 4_4_workshop 8 "The furnace roars white-orange as the waterwheel-driven bellows breathe in slow rhythm; the man turns a crucible in the heat with long tongs, his face lit and streaming sweat, utterly focused; the bellows wheeze, the fire howls, the waterwheel creaks steadily outside" --start-image $F/4_4_workshop.png --image $A/cass_45.png &
gen 4_5_vitriol 8 "The heavy oily liquid drips slowly from the glass beak into the flask, one drop, another; white vapor curls; the man adjusts the retort minutely; the young apothecary dips his pen and writes carefully in his book; embers settle, the pen scratches, a drop lands" --start-image $F/4_5_vitriol.png &
gen 4_6_faustus 10 "The bearded glassblower speaks quietly by lamplight, wine in hand, grief moving through his face, telling his old sorrow; the other man listens without moving, his whole body still with attention; the lamp flame breathes; low murmured voice, the workshop settling around them at night" --start-image $F/4_6_faustus.png --image $A/faustus.png --image $A/cass_45.png &
wait
gen 4_7_bath_icecream 10 "Steam drifts through the shaft of light; the man lifts the small bronze spoon to his mouth and eats, and his eyes close in absolute transcendent happiness; he exhales a long breath that is almost a laugh, then goes still, savoring; water lapping gently, steam hissing faintly, distant echo of the baths" --start-image $F/4_7_bath_icecream.png --image $A/cass_45.png &
wait
echo ALLDONE
