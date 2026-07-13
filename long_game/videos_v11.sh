#!/bin/bash
# v11: voice-referenced retakes (Seedance --audio), b1/b6 on the standard respawn
# frame, warm p1 dinner opening for the music drop-out. STD.
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video11
V=outputs/video11; F=frames; F2=frames2; A=anchors

WBRZ="Wardrobe and character lock: the boy is 17, white, lean, pale, short dark tousled hair, wearing a coarse undyed wool tunic - absolutely NO modern clothing. His mother is in her forties, weathered, hair bound in a cloth, rough brown wool dress and shawl. Bronze-age roundhouse: packed earth, thatch, smoke."
WMOD="Wardrobe and character lock: Cass is 70, silver-haired, weathered handsome face, brown tweed three-piece suit. Peter is mid-twenties, bright anxious face, neat side-parted sandy hair, slightly oversized grey suit. 1926 boarding-house dining room, warm electric light."
NEG="Photorealistic, natural human motion and facial performance, correct anatomy and proportions. No slow motion unless stated. No text, captions or subtitles appearing anywhere. Characters keep exactly the same faces and clothes as in the reference images for the entire clip. Each character appears exactly once. Voices match the provided audio reference."

gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>"$V/$name.err" | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

gen t0_onelife4 6 "Very slow push-in on the glowing arcade machine screen displaying its amber text, exactly as in the start image, the text never changing. Dark arcade bokeh, magenta and cyan neon shifting softly, low electrical hum. Off-screen, close, a 17-year-old boy - his voice exactly matching the audio reference - reads it aloud, dry and unimpressed: 'The Deep End. One credit... one life.' A beat. 'Huh.' No people visible. $NEG" --start-image $F2/f_t0_onelife.png --audio $A/voice/cass_teen.m4a &
sleep 3
gen b1_wake5 10 "Static low close shot, camera never moves for the first three seconds: the boy lies cheek-down on the packed earth exactly as in the start image, eyes closed. His eyes snap open. Then the camera cuts to a wider shot of the roundhouse as his mother's voice - matching the audio reference - approaches, calling: 'Bren?... Bren!' Then, arriving, brisk and tired: 'Bren - Isa has the flux again. You need to go fetch more water. More's coming out of her than's going in, at this point.' He blinks up at the thatch, utterly lost. $WBRZ $NEG" --start-image $F/2_1_eye_open.png --image $A/cass_17.png --audio $A/voice/mom_bronze.m4a &
sleep 3
gen b6_scream4 10 "Static low close shot: the boy lies cheek-down on the packed earth exactly as in the start image, eyes closed. Far off-screen his mother's voice - matching the audio reference - quietly calls 'Bren?...' His eyes snap open. Two seconds of frozen stillness as memory floods in - then he bolts upright screaming, clawing at his temples and face with both hands, searching for a headset that is not there. His mother rushes in and grabs his shoulders: 'What's wrong, Bren?!' $WBRZ $NEG" --start-image $F/2_1_eye_open.png --image $A/cass_17.png --audio $A/voice/mom_bronze.m4a &
sleep 3
gen p1_dinner2 12 "The boarding-house dining table, Sunday roast, warm and convivial: for the first three seconds just family dinner sounds - cutlery, a chuckle, Peter passing the gravy boat. Then Peter, his voice matching the audio reference, lights up: 'Uncle - you won't BELIEVE what the firm's building. A booth you SIT in - you live a whole LIFE in an hour! They haven't even named it yet!' Cass sets his own fork down very, very carefully, squares it with his plate, and keeps his face perfectly still. Peter: 'Uncle? You alright?' Cass, evenly: 'Wonderful.' $WMOD $NEG" --start-image $F2/f_p1_dinner.png --image $A/cass_70.png --audio $A/voice/peter.m4a &
sleep 3
wait
echo ALLDONE
