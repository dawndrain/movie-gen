#!/bin/bash
# v8 quick pass: hidden-skier reveal, close-up Day Zero wake, touched-woman wardrobe
# + rambling, To Cass toast.
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video8
V=outputs/video8; F=frames; F2=frames2; A=anchors

WBRZ="Wardrobe and character lock: the boy is 17, white, lean, pale, short dark tousled hair, wearing a coarse undyed knee-length wool tunic with a rope belt - absolutely NO modern clothing. Bronze-age roundhouse village: packed earth, thatch, smoke, mud."
NEG="Photorealistic, natural human motion and facial performance, correct anatomy and proportions. No slow motion unless stated. No text, captions or subtitles appearing anywhere. Characters keep exactly the same faces and clothes as in the reference images for the entire clip."

gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>"$V/$name.err" | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

gen a_ski3 12 "Inside the game: an alpine ski racer in a full-face helmet with the mirrored visor completely down - no part of his face visible for the entire run - carves at ferocious speed through slalom gates, snow spraying, crowd roar building. He blasts across the finish line, skids a huge arc to a stop, and only then pulls the helmet off, revealing a lanky white man in his twenties with sandy hair, grinning ear to ear - and he is mobbed in a hug by his blonde wife and two small blond sons. Wind, carving edges, roaring crowd. No dialogue. $NEG" --start-image $F2/f_a_ski_visor.png &
sleep 3
gen b1_wake4 10 "Extreme close low shot at ground level: the boy's face fills the frame, cheek pressed to the packed earth, breath visible - his eye snaps open. Two seconds of stillness. Then the camera cuts to a wider shot of the roundhouse interior as a woman's voice approaches from off-screen, calling: 'Bren?... Bren!' Then, arriving, brisk and tired: 'Bren - Isa has the flux again. You need to go fetch more water. More's coming out of her than's going in, at this point.' He blinks up at the thatch, utterly lost. $WBRZ $NEG" --start-image $F2/f_b11_floor.png --image $A/cass_17.png &
sleep 3
gen b9_summers 10 "The boy stands before the wild-haired old woman on her log. She is mid-conversation with the empty air, rambling happily: '...and the third river is made of sky, he says, HE says, but the geese never agreed to any of it...' - then her eyes suddenly clear, she looks straight at the boy, and says with total lucidity: 'Then you'll have to live it. All of it. Forty summers, child.' - and instantly her eyes drift away and she resumes rambling to the air: '...which is why the geese...' $WBRZ $NEG" --start-image $F2/f_touched_bronze.png --image $A/cass_17.png --image $A/touched_woman.png &
sleep 3
gen b10_forty2 8 "The boy grabs the old woman's ragged sleeve, desperate: 'Forty?! I have to live to FORTY?!' But her eyes have already gone cloudy again; she beams straight past him and carries on her happy muttered conversation with the empty air, gesturing to nobody. He stands there with his hands still half-raised. $WBRZ $NEG" --start-image $F2/f_touched_bronze.png --image $A/cass_17.png --image $A/touched_woman.png &
sleep 3
gen b21_party3 8 "The firelit hall, feast roaring. A burly elder stands and bellows a toast: 'To Cass!' The entire hall roars back: 'TO CASS!' The young bearded king raises his cup, allows himself one small satisfied smile, and says quietly, mostly to himself: 'Took twenty years.' He drinks. $NEG" --start-image $F2/3_3_good_years.png --image $A/cass_28.png &
sleep 3
wait
echo ALLDONE
