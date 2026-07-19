#!/bin/bash
# Burnt Njal — character anchors (3:4) + location plates (16:9), Nano Banana Pro.
# Recurring characters only; one-scene characters are described inline in frames_v1.sh.
cd /Users/dawndrain/Code/videogen
A=njals_saga/anchors; mkdir -p $A

STYLE="Photorealistic, shot on 35mm film, cinematic Viking-age Iceland period drama, muted natural colors, soft overcast light, plain neutral dark-gray studio background. Viking-age wool and linen clothing in natural plant-dye colors, no modern objects, no plate armor, no horned helmets. ONE single continuous photograph filling the whole frame, no borders, no collage. No text or captions."

img() {
  local name="$1"; shift
  local out
  if [ -f "$A/$name.png" ]; then echo "SKIP $name"; return; fi
  for attempt in 1 2; do
    out=$(./gen.py image "$@" 2>"$A/$name.err" | tail -1)
    if [ -f "$out" ]; then cp "$out" "$A/$name.png"; echo "OK $name"; return; fi
    sleep 5
  done
  echo "FAIL $name"
}

# ---- batch 1: principals ----
img njal "Three-quarter length portrait of Njal, an Icelandic chieftain and lawyer in his seventies: completely beardless smooth chin, kind sharp deeply lined face, long white hair under a black felt hat, long blue wool cape over a gray tunic, a small axe held in one hand. Wise, gentle, foreknowing expression. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img gunnar "Three-quarter length portrait of Gunnar of Lithend, a legendary Icelandic warrior-farmer in his forties: golden shoulder-length curling hair, short fair beard, bright blue eyes, ruddy cheeks, straight nose slightly upturned at the end; russet-red wool kirtle with a leather belt, holding upright a tall broad-bladed halberd spear. Noble, courteous, quietly formidable. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img hallgerda "Three-quarter length portrait of Hallgerda, a tall Icelandic noblewoman around forty: extraordinarily long fair hair falling loose past her waist, pale beautiful cold face; scarlet wool cloak trimmed with needlework over a red kirtle, silver girdle at her waist. Proud, unreadable, faintly disdainful expression. She is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img skarphedinn "Three-quarter length portrait of Skarphedinn, an Icelandic warrior in his thirties: ashen-pale sharp-featured face, prominent front teeth showing in a crooked unsettling grin, dark brown crisp curly hair brushed back behind his ears, a silken band round his brow; blue wool kirtle, gray breeks, silver belt, round wooden buckler on his arm, long-hafted bearded axe over his shoulder. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img bergthora "Three-quarter length portrait of Bergthora, an Icelandic farm matriarch in her sixties: iron-gray hair in braids pinned under a linen head-cloth, deep madder-red wool dress with an apron panel, ring of iron keys at her belt, proud weathered face, firm unyielding expression. She is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
wait

# ---- batch 2 ----
img kari "Three-quarter length portrait of Kari, a Norse-Gaelic warrior in his thirties: thick fair hair to his shoulders, handsome open weathered face, short fair beard; fine silken kirtle under a gray wool cloak, gilded helm held under one arm, a gold-inlaid spear in his hand. Calm, steady, unboastful. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img flosi "Three-quarter length portrait of Flosi, a powerful Icelandic chieftain in his fifties: tall and broad, full dark-gray beard, heavy dark fur-trimmed wool cloak with a large bronze penannular brooch, strong lined face capable of great sternness and great warmth. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img hildigunna "Three-quarter length portrait of Hildigunna, an Icelandic noblewoman around thirty: fair braided hair under an embroidered linen head-dress, fine dark-blue wool dress with a woven belt, beautiful proud face with a grim set jaw and cold steady eyes. She is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img mord "Three-quarter length portrait of Mord, an Icelandic schemer in his forties: thin fox-like face, small pale watchful eyes, thin ginger beard, dark plain but rich wool clothes with a silver ring-pin, an ingratiating half-smile that does not reach his eyes. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img hoskuld_wp "Three-quarter length portrait of Hoskuld the Whiteness Priest, an Icelandic chieftain in his early thirties: fine light-brown hair, warm open gentle handsome face, short neat beard; a SCARLET wool cloak richly embroidered at the hem worn over a cream tunic. Kind, trusting, beloved. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
wait

# ---- batch 3 ----
img gizur "Three-quarter length portrait of Gizur the White, an old Icelandic chieftain in his sixties: white hair and full white beard, noble grave bearing, fine gray-green wool cloak with a silver brooch, sword at his belt. Honorable, weary, commanding. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img rannveig "Three-quarter length portrait of Rannveig, an old Icelandic matriarch in her seventies: stern hawk-like deeply lined face, white hair under a dark shawl drawn over her head, dark wool dress. Grim, dignified, far-seeing expression. She is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img kolskegg "Three-quarter length portrait of Kolskegg, an Icelandic warrior in his late thirties: tall and strongly built, dark blond hair and full beard, plain brown wool kirtle, leather belt, sword at his hip, round shield slung on his back. Loyal, steadfast, undaunted. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img gunnar_lambi "Three-quarter length portrait of Gunnar Lambi's son, a young Icelandic fighter in his early twenties: lean cocky face with a mocking grin, sparse young beard, unruly brown hair, dark wool kirtle with a plain cloak, hand axe in his belt. Swaggering, cruel-humored. He is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
wait

# ---- batch 4: location plates ----
PSTYLE="Photorealistic, shot on 35mm film, cinematic Viking-age Iceland c. 1000 AD, muted natural colors, overcast subarctic light. No modern objects, no power lines, no roads. No text or captions."
img loc_lithend "Wide establishing shot: a Viking-age Icelandic farm on a green hillside slope - a long turf-roofed timber hall with carved gable ends, home meadow freshly mown, pale ripe cornfields below, a sunken lane between low stone-and-turf fences above the farmyard, steep green fells behind, gray sky breaking to late golden light. $PSTYLE" &
img loc_bergthorsknoll "Wide establishing shot: a Viking-age Icelandic homestead on a low grassy knoll in flat open lowland - a large turf-and-timber hall with outbuildings, a tall stack of dried vetch fodder standing just above the house, a small stream nearby, distant glacier on the horizon, brooding overcast evening light. $PSTYLE" &
img loc_althing "Wide establishing shot: the Althing assembly plain at Thingvellir, Iceland, c. 1000 AD - a great black lava rift wall, a river winding through the grassy plain, dozens of turf-and-canvas booths with small figures among them, a rocky outcrop where a crowd gathers, gray-blue subarctic light. $PSTYLE" &
img loc_swinefell "Interior establishing shot: the great hall of a wealthy Viking-age Icelandic chieftain - long central fire-pit with glowing embers, carved high-seat pillars, wall benches spread with furs, woven wall hangings, smoke drifting up to a roof louver, warm firelight against deep shadow. $PSTYLE" &
wait
echo ANCHORS_DONE
