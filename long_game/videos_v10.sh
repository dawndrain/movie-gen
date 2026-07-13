#!/bin/bash
# v10: STD ONLY (fast retired). t0 voice fix, static a6, respawns all opening on
# b15's exact start frame (frames/2_1_eye_open.png).
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video10
V=outputs/video10; F=frames; F2=frames2; A=anchors

WARC="Wardrobe and character lock: Cass is 17, white, lean, pale, short dark tousled hair, watchful grey eyes, wearing a plain heather-grey t-shirt, dark slim jeans, white sneakers. Milo is 17, white, compact, curly brown hair, thin wire-frame glasses, wearing an olive-green hoodie and blue jeans. Deshawn is 17, Black, very tall and long-limbed, buzzed hair, iridescent blue-and-orange track jacket, black joggers, chunky white high-tops. The arcade is spotless and gleaming, magenta and cyan neon."
WBRZ="Wardrobe and character lock: the boy is 17, white, lean, pale, short dark tousled hair, wearing a coarse undyed wool tunic - absolutely NO modern clothing. Bronze-age roundhouse: packed earth, thatch, smoke."
NEG="Photorealistic, natural human motion and facial performance, correct anatomy and proportions. No slow motion unless stated. No text, captions or subtitles appearing anywhere. Characters keep exactly the same faces and clothes as in the reference images for the entire clip. Each character appears exactly once."

gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>"$V/$name.err" | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

gen t0_onelife3 6 "Very slow push-in on the glowing arcade machine screen displaying its amber text, exactly as in the start image, the text never changing. Dark arcade bokeh, magenta and cyan neon shifting softly, low electrical hum. Off-screen, close, a 17-year-old male voice - a teenage boy, low, dry, unimpressed, definitely NOT a young child - reads it aloud: 'The Deep End. One credit... one life.' A beat. 'Huh.' No people visible. $NEG" --start-image $F2/f_t0_onelife.png &
sleep 3
gen a6_sign4 8 "Locked-off static camera, no camera movement at all, no push-in, no pan: the three boys stand around the tooth-white pod machine. Cass points at the yellow tape across it: 'It says out of order.' Milo rips the tape off in one long satisfying pull, wads it, tosses it over his shoulder without looking, and says flatly: 'No it doesn't.' Cass points at a smaller red sticker: 'That one says security warning.' Milo peels that one off too and sticks it flat onto Deshawn's chest. Deshawn looks down at it, then wears it proudly. $WARC $NEG" --start-image $F2/f_a2_deepend_placard.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 3
gen w1d 5 "Static low close shot, camera never moves: the boy lies cheek-down on the packed earth exactly as in the start image, eyes closed. His eyes snap open. Off-screen his mother calls, bright and businesslike: 'Bren! Water!' A beat. He says flatly, into the dirt: '...Again.' $WBRZ $NEG" --start-image $F/2_1_eye_open.png --image $A/cass_17.png &
sleep 3
gen w2d 6 "Static low close shot, camera never moves: the boy lies cheek-down on the packed earth exactly as in the start image, eyes closed. His eyes snap open - then immediately squeeze shut again, and he lies perfectly rigid, playing dead. A pause. His mother's voice off-screen, closer, deeply unimpressed: 'I can see you breathing.' His eyes stay shut. One long defeated exhale stirs the dust. $WBRZ $NEG" --start-image $F/2_1_eye_open.png --image $A/cass_17.png &
sleep 3
gen w3d 6 "Static low close shot, camera never moves: the boy lies cheek-down on the packed earth exactly as in the start image, eyes closed. His eyes snap open - a shadow falls across his face - and a heavy wooden water yoke drops into frame across him with a hard thud. He wheezes. His mother's voice, off-screen, flat: 'Water.' Footsteps walk away. $WBRZ $NEG" --start-image $F/2_1_eye_open.png --image $A/cass_17.png &
sleep 3
wait
echo ALLDONE
