#!/bin/bash
# v7: thud-framed respawns, white-skier reveal, British voice for adult Cass,
# dialogue for the silent stretch, softer Iris, roman clothes, static king cam,
# proper hallway door. 480p std via pool_run.py.
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video7
V=outputs/video7; F=frames; F2=frames2; A=anchors

WARC="Wardrobe and character lock: Cass is 17, white, lean, pale, short dark tousled hair, watchful grey eyes, wearing a plain heather-grey t-shirt, dark slim jeans, white sneakers. Deshawn is 17, Black, very tall and long-limbed, expressive mobile face, buzzed hair, wearing an iridescent blue-and-orange patterned track jacket over a black tee, black joggers, chunky white high-tops. Milo is 17, white, compact, curly brown hair, thin wire-frame glasses, wearing an olive-green hoodie and blue jeans."
WBRZ="Wardrobe and character lock: the boy is 17, white, lean, pale, short dark tousled hair, wearing a coarse undyed knee-length wool tunic with a rope belt - absolutely NO modern clothing. His mother is in her forties, weathered, hair bound in a cloth, wearing a rough brown wool dress and shawl. Bronze-age roundhouse village: packed earth, thatch, smoke."
VBRIT="Cass speaks in the same measured, dry, understated British accent as the rest of the film - calm RP English delivery, never American, never theatrical. There is no narrator and no voiceover; only characters visible on screen speak, lips moving."
NEG="Photorealistic, natural human motion and facial performance, correct anatomy and proportions. No slow motion unless stated. No text, captions or subtitles appearing anywhere. Characters keep exactly the same faces and clothes as in the reference images for the entire clip."
EXITSEQ="the tester's exit sequence: eyes closing in concentration, both hands raised to chest height with palms facing each other, then three slow deliberate motions - the left palm passing flat across the right, both hands rotating once around each other, then both hands closing to fists and opening again"

gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>"$V/$name.err" | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

# --- Respawns back in the thud framing (face against camera) ---
gen w1b 5 "Static low shot at ground level of the empty packed-earth floor. The boy's face drops into frame from above and lands cheek-first on the earth with a heavy THUD, his face filling the frame close to the camera, dust puffing up. His eyes open slowly. Off-screen his mother calls, bright and businesslike: 'Bren! Water!' He says flatly, into the dirt: '...Again.' $WBRZ $NEG" --start-image $F2/f_b11_floor.png --image $A/cass_17.png &
sleep 3
gen w2b 6 "Static low shot at ground level of the empty packed-earth floor. The boy's face drops into frame from above and lands cheek-first with a heavy THUD, face close to camera - and he immediately squeezes both eyes shut and lies perfectly rigid, playing dead. A pause. His mother's voice off-screen, closer now, deeply unimpressed: 'I can see you breathing.' His eyes stay shut. One long defeated exhale stirs the dust. $WBRZ $NEG" --start-image $F2/f_b11_floor.png --image $A/cass_17.png &
sleep 3

# --- The white-skier reveal ---
gen a_ski2 12 "Inside the game: an alpine ski racer in a full downhill race suit carves at ferocious speed through slalom gates, snow spraying, crowd roar building - he blasts across the finish line, skids a huge arc to a stop, pulls off his helmet revealing a lanky white man in his twenties with sandy hair, grinning ear to ear - and he is mobbed in a hug by his blonde wife and two small blond sons. Wind, carving edges, roaring crowd, laughter. No dialogue. $NEG" --start-image $F2/f_a_ski.png &
sleep 3

# --- Bronze: dialogue for the silent stretch ---
gen b19_isa 8 "By the fire the boy spoon-feeds his small feverish sister from a clay cup, steady and sure, instructing his mother without looking up: 'Salt. Honey. Clean water - boiled first. Keep giving it, however fast it runs through her.' The mother nods, wide-eyed, committing it to memory. The little girl drinks. $WBRZ $NEG" --start-image $F/3_1_salt_water.png --image $A/cass_17.png &
sleep 3
gen b21_party 8 "The firelit hall, feast roaring. A burly elder stands and bellows a toast: 'To Bren!' The entire hall roars back: 'TO BREN!' The young bearded king raises his cup with a thin smile, waits for the noise, and mutters quietly into the cup: '...Cass.' He drinks. Nobody hears him. $NEG" --start-image $F2/3_3_good_years.png --image $A/cass_28.png &
sleep 3
gen b22_wish3 10 "Locked-off static camera, no camera movement at all, no zoom, no pan: the young king slouches on his throne, chin on fist, feast roaring around him, and confides sideways to his attendant - a short, stout, much older man with a round face and a thick grey beard: 'I just wish I could take a bath, you know? Go back to the arcade. See my friends again. My family.' A long pause. Quieter: '...Have some ice cream.' The old attendant nods along solemnly, comprehending absolutely nothing. $NEG" --start-image $F/3_4_bored_king.png --image $A/cass_28.png &
sleep 3

# --- Roman: clothes + British voice ---
gen r2_aq3 8 "The man - wearing a simple knee-length Roman tunic and a worn woollen cloak, leather sandals, absolutely no modern clothing - stands in the Roman street staring up at the great aqueduct crossing the sky, people and carts passing around him. He takes it in for a long moment, lets out a long, deep, defeated sigh, drops his gaze, and walks on. No dialogue. Street ambience. $NEG" --start-image $F/4_1_aqueduct.png --image $A/cass_45.png &
sleep 3
gen r12_salt4 8 "The man packs grey salt into the snow around a bronze pot, dictating: 'Salt, added to ice, lowers its melting point.' Off-screen, Tertius - a young man in his early twenties with a curious young adult male voice - asks: 'What's that one?' The man turns his head and just smiles at him, slowly, saying nothing, then goes back to packing the salt. Frost blooms on the jars. $VBRIT $NEG" --start-image $F2/4_7_icecream_bench.png --image $A/cass_45.png &
sleep 3
gen r13_sweet3 8 "Feet up in the scroll-stuffed study, the man holds a small bronze bowl clearly half-full of pale soft ice cream. He lifts a visibly heaped spoonful, eats it with real relish, closes his eyes to savor it, gazes around at the hundreds of scrolls filling every shelf, and says to the empty room, richly satisfied: 'Things are going to be pretty sweet in the next life.' He clinks the spoon back into the bowl. The frame washes to white at the very end. $VBRIT $NEG" --start-image $F2/f_r11_study.png --image $A/cass_45.png &
sleep 3

# --- 1926: softer Iris ---
gen m5_feet2 10 "The boarding-house hallway. Iris stands by the door and points one finger down at the doormat, mock-stern but with warmth in her eyes: 'Feet.' Cass obediently wipes his shoes. Iris, teasing: 'Honestly. Where were you raised - a mud hut?' Cass, still wiping, perfectly matter-of-fact: '...Yes, actually.' Iris laughs despite herself - a real, warm laugh - and walks off: 'Then wipe like it.' Cass smiles after her. Wardrobe: Cass is 70, silver-haired, brown tweed three-piece suit. Iris is late fifties, soft round face, silver-brown hair pinned back, wool cardigan over a floral house dress. $NEG" --start-image $F/6_4_iris_doormat.png --image $A/cass_70.png --image $A/iris.png &
sleep 3

# --- Exit: British, absolutely no narration ---
gen p4_exit3 12 "Morning light in the boarding-house room. Cass, eighty now, stands at the window; outside, the old touched woman passes and nods to him through the glass. He nods back. He steps to the middle of the room, straightens his jacket, and says out loud to the empty room - his own lips clearly moving, in the same measured dry British accent as the rest of the film, aged: 'Five lifetimes. Every chore, every gate...' a small smile, '...and I am leaving through the staff door.' He performs ${EXITSEQ}, precise and unhurried - and on the final motion the room floods to pure white. There is absolutely no narrator, no voiceover, no off-screen voice; the only voice heard is the old man speaking on camera. $NEG" --start-image $F/7_2_exit_80.png --image $A/cass_70.png &
sleep 3

# --- Ending: the door opens to a normal hallway ---
gen q8_come3 10 "The dark sleek 2044 bedroom, city glow through the window. A knock, and Deshawn's voice through the door, ordinary and immortal: 'Yo! We're going out. You coming, or you gonna sit in the dark being weird about the arcade thing all night?' Cass, sitting on the bed in the dark, looks at his open hand one last time - then closes it, and a small real smile arrives. 'Yeah.' He stands, grabbing his jacket, and opens the door into an ordinary warm apartment hallway - soft hallway light, Deshawn leaning against the corridor wall opposite. It is a normal home corridor, absolutely NOT an arcade. 'Yeah. I'm coming.' $WARC $NEG" --start-image $F2/f_q_room2044.png --image $A/cass_17.png --image $A/deshawn.png &
sleep 3
wait
echo ALLDONE
