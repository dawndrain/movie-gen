#!/bin/bash
# v9: tighter opening (t0 with Cass line, cut a5/a10, merged a_hard ending),
# standardized respawn picture, non-morbid b7, r4 continuity. FAST draft mode.
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video9
V=outputs/video9; F=frames; F2=frames2; A=anchors

WARC="Wardrobe and character lock: Cass is 17, white, lean, pale, short dark tousled hair, watchful grey eyes, wearing a plain heather-grey t-shirt, dark slim jeans, white sneakers. Deshawn is 17, Black, very tall and long-limbed, expressive mobile face, buzzed hair, wearing an iridescent blue-and-orange patterned track jacket over a black tee, black joggers, chunky white high-tops. Milo is 17, white, compact, curly brown hair, thin wire-frame glasses, wearing an olive-green hoodie and blue jeans. The arcade is spotless and gleaming, magenta and cyan neon. The white pod machine has NO tape and NO stickers on it - all signage was already removed."
WBRZ="Wardrobe and character lock: the boy is 17, white, lean, pale, short dark tousled hair, wearing a coarse undyed knee-length wool tunic with a rope belt - absolutely NO modern clothing. His mother is in her forties, weathered, hair bound in a cloth, wearing a rough brown wool dress and shawl. Bronze-age roundhouse: packed earth, thatch, smoke."
VBRIT="Cass speaks in the same measured, dry, understated British accent as the rest of the film - calm RP English delivery, never American, never theatrical. There is no narrator and no voiceover; only characters visible on screen speak, lips moving."
NEG="Photorealistic, natural human motion and facial performance, correct anatomy and proportions. No slow motion unless stated. No text, captions or subtitles appearing anywhere. Characters keep exactly the same faces and clothes as in the reference images for the entire clip. Each character appears exactly once - no duplicated people."

gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --duration "$dur" 2>"$V/$name.err" | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

gen t0_onelife2 6 "Very slow push-in on the glowing arcade machine screen displaying its amber text, exactly as in the start image, the text never changing. Dark arcade bokeh, magenta and cyan neon shifting softly, low electrical hum. Off-screen, close, a teenage boy's voice - American, dry, unimpressed - reads it aloud: 'The Deep End. One credit... one life.' A beat. 'Huh.' No people visible. $NEG" --start-image $F2/f_t0_onelife.png &
sleep 2
gen a6_sign3 8 "The three boys stand around the tooth-white pod machine. Cass points at the yellow tape across it: 'It says out of order.' Milo rips the tape off in one long satisfying pull, wads it, tosses it over his shoulder without looking, and says flatly: 'No it doesn't.' Cass points at a smaller red sticker: 'That one says security warning.' Milo peels that one off too and sticks it flat onto Deshawn's chest. Deshawn looks down at it, then wears it proudly. $WARC $NEG" --start-image $F2/f_a2_deepend_placard.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 2
gen a8_out3 12 "Deshawn reclined in the white chair, headset on: for two seconds his hands twitch - then he tears the headset off and erupts upright, beaming, breathless: 'That was INCREDIBLE. I won gold at the Olympics! I had a WIFE. Two kids - Braden and Tucker!' His face goes briefly, genuinely wistful: '...Man, I miss them.' Milo, checking his phone: 'You were in for ninety seconds.' Deshawn: 'It was a whole LIFE, bro. And it was SO easy.' Only one Cass and one Milo flank the chair. $WARC $NEG" --start-image $F/1_5_deshawn_chair.png --image $A/deshawn.png --image $A/cass_17.png --image $A/milo.png &
sleep 2
gen a_hard2 12 "Cass steps past Deshawn and lowers himself into the white chair like it's a throne, supremely cocky: 'Easy is boring. Put me on hard mode.' Deshawn lights up with delight: 'Ohhh - Cass wants the SMOKE!' Milo, at the machine's open side panel, turns a chunky dial all the way clockwise until it clicks. As Cass pulls the headset down over his eyes, Milo says warmly: 'Have a nice life.' Cass, eyes already covered, raises one lazy middle finger toward Milo without looking. The machine's screen light blooms and floods the whole frame to pure white. $WARC $NEG" --start-image $F2/1_6_goading.png --image $A/cass_17.png --image $A/deshawn.png --image $A/milo.png &
sleep 2
gen b7_name3 8 "The boy sits up on the packed earth floor, his mother standing over him, and mutters, hoarse, staring at nothing: 'My name is Cass. My name is Cass. My name is Cass.' A pause. His mother looks down at him and says, gently but completely practical: '...Well. Isa has the flux. So you're going to need to go fetch more water.' $WBRZ $NEG" --start-image $F2/f_w3_yoke.png --image $A/cass_17.png &
sleep 2
gen b6_scream3 10 "Static close low shot: the boy lies cheek-down on the packed earth exactly as in the start image, eyes half open, utterly still. Far off-screen a woman's voice quietly calls 'Bren?...' Two seconds of stillness - then he bolts upright screaming, clawing at his temples and face with both hands, searching for a headset that is not there. His mother rushes in and grabs his shoulders: 'What's wrong, Bren?!' $WBRZ $NEG" --start-image $F2/f_respawn.png --image $A/cass_17.png &
sleep 2
gen w1c 5 "Static close low shot: the boy lies cheek-down on the packed earth exactly as in the start image, eyes closed. His eyes snap open. Off-screen, his mother's voice, bright and businesslike: 'Bren! Water!' A beat. He says flatly, into the dirt: '...Again.' The camera never moves. $WBRZ $NEG" --start-image $F2/f_respawn.png --image $A/cass_17.png &
sleep 2
gen w2c 6 "Static close low shot: the boy lies cheek-down on the packed earth exactly as in the start image, eyes closed. His eyes snap open - and immediately squeeze shut again, and he lies perfectly rigid, playing dead. A pause. His mother's voice off-screen, closer now, deeply unimpressed: 'I can see you breathing.' His eyes stay shut. One long defeated exhale stirs the dust. The camera never moves. $WBRZ $NEG" --start-image $F2/f_respawn.png --image $A/cass_17.png &
sleep 2
gen r4_boil3 10 "Continuing directly from the start image: the man stands right beside the kneeling woman at the fountain and stays next to her the entire time, pleading, gesturing at her jar: 'You need to boil it first. You can't just do the hand thing - you need to BOIL it first.' The woman stands, hoists the jar onto her hip, gives him the long flat look you give a crazy person, says: 'Why would I boil water?' - and walks away. He stands alone by the running fountain, arms half-raised, devastated. $VBRIT $NEG" --start-image $F2/f_r4_start.png --image $A/cass_45.png &
sleep 2
wait
echo ALLDONE
