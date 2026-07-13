#!/bin/bash
# Burnt Njal — shot start frames (16:9), Nano Banana Pro. Run AFTER anchors_v1.sh.
# One frame per storyboard shot. 5 concurrent max. Content-safety staging per SOURCE_NOTES.md:
# no on-frame impacts, no flames touching people, "dark-stained" not "gore".
cd /Users/dawndrain/Code/videogen
A=njals_saga/anchors; F=njals_saga/frames; mkdir -p $F

S="Photorealistic, shot on 35mm film, cinematic Viking-age Iceland c. 1000 AD, muted natural colors, overcast subarctic light. Characters keep exactly the same faces, hair and clothes as in the reference images. Viking-age wool and linen clothing, turf-and-timber halls, no modern objects, no plate armor, no horned helmets. ONE single continuous photograph filling the whole frame, no borders, no collage. No text or captions unless explicitly described."

img() {
  local name="$1"; shift
  local out
  if [ -f "$F/$name.png" ]; then echo "SKIP $name"; return; fi
  for attempt in 1 2; do
    out=$(./gen.py image "$@" --aspect_ratio 16:9 2>"$F/$name.err" | tail -1)
    if [ -f "$out" ]; then cp "$out" "$F/$name.png"; echo "OK $name"; return; fi
    sleep 5
  done
  echo "FAIL $name"
}

# ---- Prologue ----
img f_p1_thiefs_eyes "Firelit Viking-age Icelandic feast hall: a girl of eight with extraordinarily long silk-fine fair hair falling to her waist stands beside the high-seat where her father, a proud gray-bearded chieftain in feast clothes, tilts her chin up affectionately; across the fire his brother, a tall handsome grave man in his fifties in a fine dark tunic, studies the child with a deeply troubled frown. Benches of feast guests softly blurred in warm firelight behind. $S" &
img f_p2_title "Cinematic title card: aerial view over a black-sand Icelandic coast meeting green dales under heavy gray clouds, a thin white line of surf. Large elegant weathered serif letters across the sky read exactly: BURNT NJAL. Below them in smaller letters: Iceland, in the days of the Althing. $S" &

# ---- Act I: Gunnar and Hallgerda ----
img f_a1_wooing "Among turf-and-canvas booths at the great Althing assembly, bright day: the golden-haired warrior from the reference, in his finest clothes with a scarlet-trimmed cloak, stands face to face with the tall fair-haired woman from the second reference in her scarlet cloak; she looks up at him with a bold half-smile, he is mid-word, courteous and captivated. Assembly crowds behind. $S" --image $A/gunnar.png --image $A/hallgerda.png --image $A/loc_althing.png &
img f_a2_warning "Interior of a Viking-age turf hall, firelight: the beardless old chieftain from the reference sits in his carved high-seat, felt hat on his knee, speaking gravely with a raised hand; before him stands the golden-haired warrior from the second reference holding his tall halberd, jaw set in mild defiance. $S" --image $A/njal.png --image $A/gunnar.png &
img f_a3_quarrel "A feast in a Viking-age hall: at the cross-bench the tall fair-haired woman in scarlet from the reference and the iron-gray matriarch from the second reference face each other in icy confrontation over a seat, guests frozen mid-drink all down the long table; the golden-haired warrior from the third reference has risen to his feet, thunder-faced, swinging his cloak on to leave. $S" --image $A/hallgerda.png --image $A/bergthora.png --image $A/gunnar.png &
wait

img f_a4_purse "Gray daylight outside a turf hall: the golden-haired warrior from the reference presses a small worn leather purse of silver into the hands of the beardless old chieftain from the second reference; both men clasp forearms, grave and friendly. Behind each of them, a woman watches coldly from an opposite doorway. $S" --image $A/gunnar.png --image $A/njal.png &
img f_a5_slap "Interior of the hall at Lithend, at table: the tall fair-haired woman from the reference has turned her face sharply aside, one hand rising toward her cheek, eyes glittering with cold fury; the golden-haired warrior from the second reference stands over the table, his hand falling back to his side, face full of shame and anger; a platter of cheese and butter on the board between them. $S" --image $A/hallgerda.png --image $A/gunnar.png &
img f_a6_conditions "The beardless old chieftain from the reference and the golden-haired warrior from the second reference walk together across a green home-meadow under a heavy sky, deep in talk; the old man holds up two fingers in counsel, the warrior listens with his halberd over his shoulder. $S" --image $A/njal.png --image $A/gunnar.png &
img f_a7_ford "At a muddy river ford between flat stones: the golden-haired warrior from the reference stands alone at bay against six mounted attackers wheeling around him, his tall halberd mid-sweep, river water spraying, gray driving sky. $S" --image $A/gunnar.png &
img f_a8_outlawry "On a rocky outcrop above the assembly crowd at the Althing, the white-bearded old chieftain from the reference proclaims judgment with one raised arm; below him among the listeners stands the beardless old chieftain from the second reference, head bowed. $S" --image $A/gizur.png --image $A/njal.png --image $A/loc_althing.png &
wait

img f_a9_fair_lithe "On a riverside track below a green hillside farm: the golden-haired warrior from the reference stands beside his halted horse, one hand on its neck, gazing back up the slope where pale ripe cornfields and a mown home-meadow shine under breaking golden light; ahead on the track his tall dark-blond bearded brother from the second reference waits on horseback, turned in the saddle. $S" --image $A/gunnar.png --image $A/kolskegg.png --image $A/loc_lithend.png &
img f_a10_siege "Night at the turf-roofed hillside farm from the reference: dozens of armed men with spears and torches crowd the sunken lane between the fences above the farmyard; at the hall gable one climber peers into a lit window-slit under the roof beams and recoils backward. $S" --image $A/loc_lithend.png &
img f_a11_bowstring "Inside a timber loft by lamplight: the golden-haired warrior from the reference kneels with his great bow, its string hanging cut and loose; he looks up at the tall fair-haired woman from the second reference, who stands gathering her waist-length hair in both hands, face cold as stone; behind her the old matriarch in the dark shawl from the third reference watches with open fury. $S" --image $A/gunnar.png --image $A/hallgerda.png --image $A/rannveig.png &
img f_a12_fall "Seen from below against a torn-open roof and gray dawn sky: the dark silhouette of a lone warrior holding a halberd at bay on the exposed roof-beams of a turf hall, ringed on all sides by the raised spears of men climbing toward him. $S" --image $A/gunnar.png &
wait

# ---- Act II: the foster-son ----
img f_b1_ice "On a frozen glacial river between white sheets of ice, brilliant winter sun: the pale sharp-faced warrior from the reference glides standing at full speed across glass-smooth dark ice, axe swung back, dark hair streaming, bearing down on a richly dressed man in a blue cloak and gilded helm who is turning too late; other armed men flounder on the frozen bank behind. $S" --image $A/skarphedinn.png &
img f_b2_ring "Firelit evening interior of a turf hall: the beardless old chieftain from the reference sits leaning toward a solemn boy of eight with fine light-brown hair, holding out a gold ring on his open palm; the boy's face is grave and gentle beyond his years. $S" --image $A/njal.png &
img f_b3_one_law "On the rocky Hill of Laws at the Althing: an old lawspeaker with a windblown gray beard rises from beneath the great cloak he has lain under, one arm flung out in proclamation, before two armed factions crowding the plain below, spears thick as reeds; shafts of pale light through cloud. $S" --image $A/loc_althing.png &
img f_b4_deathbed "A dark Viking-age hall interior lit by one guttering lamp: a gaunt dying old man props himself up on the edge of a bed-closet, gripping the sleeve of the thin fox-faced man from the reference and hissing final counsel into his ear; a small wooden cross lies snapped in two on the floor between them. $S" --image $A/mord.png &
img f_b5_slander "Interior, day: the thin fox-faced man from the reference leans close and confidential across a table toward the pale sharp-faced warrior from the second reference, one hand resting as if in friendship on the warrior's forearm; the warrior's knuckles are white around his ale-cup and his grin has gone dangerous. $S" --image $A/mord.png --image $A/skarphedinn.png &
wait

img f_b6_cornfield "A small cornfield beside a low turf fence at dawn, the sun just risen, dew on the grass: the fair young chieftain from the reference in his scarlet embroidered cloak walks sowing seed-corn broadcast from a basket at his hip, serene and unaware; behind the fence at his back several dark figures are rising with weapons, their faces unseen. $S" --image $A/hoskuld_wp.png &
img f_b7_grief "Interior turf hall: the beardless old chieftain from the reference sits stricken in his high-seat, tears bright on his lined face; before him stand the pale sharp-faced warrior from the second reference and the fair-haired warrior from the third reference, sober and utterly still. $S" --image $A/njal.png --image $A/skarphedinn.png --image $A/kari.png &
img f_b8_cloak "In a chieftain's firelit hall: the proud noblewoman from the reference hurls a stiff dark-stained man's cloak so it lands over the shoulders of the seated gray-bearded chieftain from the second reference, dry dark flakes scattering in the firelight; his face is caught between dead pale and furious red, half risen from the bench. $S" --image $A/hildigunna.png --image $A/flosi.png --image $A/loc_swinefell.png &
img f_b9_silver "At the Court of Laws on the assembly plain: a great heap of silver coin and arm-rings piled on a spread cloak, a fine silken scarf laid on top; the gray-bearded chieftain from the reference holds the scarf aloft with a scornful laugh; across the pile the pale sharp-faced warrior from the second reference hurls a pair of dark-blue breeches at his chest; ranked chieftains recoil on either side. $S" --image $A/flosi.png --image $A/skarphedinn.png --image $A/loc_althing.png &
img f_b10_oath "Dusk inside a great black lava rift: a hundred armed men stand in a ring, clasping hands one over another in a stack of fists at the center; the gray-bearded chieftain from the reference speaks the oath over the joined hands, torches guttering against the rock walls. $S" --image $A/flosi.png &
wait

# ---- Act III: the Burning ----
img f_c1_supper "Evening meal in the turf hall: the iron-gray matriarch from the reference stands at the head of the long table setting down a wooden dish, mid-word; around the table her household has gone still, spoons halted; beside her the beardless old chieftain from the second reference stares past the fire with wide unseeing eyes, at something no one else can see. $S" --image $A/bergthora.png --image $A/njal.png &
img f_c2_indoors "Night in the farmyard of the lowland homestead from the reference: torches of many armed men approaching across the dark meadow; before the hall door the beardless old chieftain from the second reference stands calm with one arm raised, ushering his armed sons inside; the pale sharp-faced warrior from the third reference pauses last in the doorway, looking back at the torches with a grim smile. $S" --image $A/loc_bergthorsknoll.png --image $A/njal.png --image $A/skarphedinn.png &
img f_c3_fire "Night: attackers heap burning bundles of dried vetch against the timber gable of the turf hall, flames climbing the loft, sparks streaming into the black sky; in the foreground the gray-bearded chieftain from the reference stands lit orange by the blaze, his face a grim mask of resolve. $S" --image $A/flosi.png --image $A/loc_bergthorsknoll.png &
img f_c4_refusal "At the hall door with fire-glow behind them: the beardless old chieftain from the reference and the iron-gray matriarch from the second reference stand together in the doorway facing out toward ranked spears in the dark, their hands clasped; past them women and children file out to safety between the spear-lines. $S" --image $A/njal.png --image $A/bergthora.png &
img f_c5_bed "Interior with smoke gathering high under the roof beams: an old beardless chieftain and his iron-gray wife from the references lie down together on a broad bed with a small boy nestled between them, all three calm with eyes closed as if for sleep; a servant draws a dark ox-hide over the three of them. Soft, still, solemn; no flames near them. $S" --image $A/njal.png --image $A/bergthora.png &
wait

img f_c6_beam "Inside the smoke-filled roof-space of a burning hall: the fair-haired warrior from the reference runs along a high cross-beam through dense gray smoke and drifting embers, a wet cloak wrapped over his head and shoulders, sparks streaming past him, a gap of cold night sky ahead where the roof has fallen in. $S" --image $A/kari.png &
img f_c7_keepsake "Against a firelit gable wall: the pale sharp-faced warrior from the reference stands wedged upright between a fallen roof-beam and the wall, lit by orange fire-glow, grinning his crooked grin up at the cocky young man from the second reference, who leans over the wall-top laughing down at him; smoke coils between them. $S" --image $A/skarphedinn.png --image $A/gunnar_lambi.png &
img f_c8_bright "Gray dawn over the smoking ruin of a turf hall, a silent crowd of neighbors standing in drifting ash: men lift away a scorched ox-hide, and beneath it an old beardless chieftain, his wife and a small boy lie unburnt and peaceful as if asleep, the old man's face strangely luminous, as if lit from within. Ash drifting like snow. $S" --image $A/njal.png --image $A/bergthora.png &
img f_c9_vow "A soot-blackened fair-haired man, the warrior from the reference with his hair singed and cloak burnt ragged, stands on a hillside at dawn looking down at a thread of smoke rising from a ruined farm far out on the plain; the wind stirs his ruined cloak; his face is quiet and terrible. $S" --image $A/kari.png --image $A/loc_bergthorsknoll.png &
wait

# ---- Epilogue ----
img f_d1_battle "Battle erupting across the Althing assembly plain between the turf booths: two shield-walls colliding, spears in flight, men grappling; in the foreground the fair-haired warrior from the reference catches a flying spear clean out of the air, mid-stride. Gray sky, churned grass. $S" --image $A/kari.png --image $A/loc_althing.png &
img f_d2_peace "On the Hill of Laws the morning after battle: an old gentle-faced chieftain in a blue cape, a little silver-studded axe in his belt, stands over a bier where a young man lies covered to the chin by a cloak, and addresses the hushed assembly with open empty hands. $S" --image $A/loc_althing.png &
img f_d3_yule "A Norse earl's Yule feast in a long timber hall, boards laden, firelight: the cocky young man from the reference, now wearing a dark leather patch over one eye, stands performing a story before the high-seat where a king and an earl sit with raised cups; far behind him at the door, the fair-haired warrior from the second reference steps out of shadow with drawn sword held low, snow blowing in around him. $S" --image $A/gunnar_lambi.png --image $A/kari.png &
img f_d4_pilgrim "A lone figure in a rough pilgrim's cloak with staff in hand walks a mountain road south, tiny against vast snow-streaked peaks and a pale sky. $S" &
img f_d5_kiss "Winter night in the chieftain's firelit hall from the reference: the gray-bearded chieftain from the second reference has sprung from his high-seat to embrace and kiss the brow of a storm-battered, hollow-eyed fair-haired traveler from the third reference, snow still on the traveler's shoulders; by the hearth beyond, the proud noblewoman from the fourth reference watches with one hand at her throat. $S" --image $A/loc_swinefell.png --image $A/flosi.png --image $A/kari.png --image $A/hildigunna.png &
wait

img f_d6_ship "A gray harbor under an iron sky: an old weathered Viking longship with a patched sail stands out to sea, small and alone on a vast dark swell; on the stony shore, wooden mooring stakes and a few silent watchers wrapped in cloaks. $S" &
img f_d7_endcard "Cinematic end card: dark iron-gray sea and sky, a tiny pale sail on the far horizon. Elegant pale weathered serif letters across the middle of the frame read exactly: AND HERE WE END THE STORY OF BURNT NJAL. $S" &
wait
echo FRAMES_DONE
