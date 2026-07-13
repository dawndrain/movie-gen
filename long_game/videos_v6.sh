#!/bin/bash
# v6 DIRECTOR'S PASS: arcade restructure (arrogant Cass), funnier respawns, bronze
# wardrobe sweep, roman sighs, voice locks, 2044 bedroom. 480p std, via pool_run.py.
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video6
V=outputs/video6; F=frames; F2=frames2; A=anchors

WARC="Wardrobe and character lock: Cass is 17, white, lean, pale, short dark tousled hair, watchful grey eyes, wearing a plain heather-grey t-shirt, dark slim jeans, white sneakers. Deshawn is 17, Black, very tall and long-limbed, expressive mobile face, buzzed hair, wearing an iridescent blue-and-orange patterned track jacket over a black tee, black joggers, chunky white high-tops. Milo is 17, white, compact, curly brown hair, thin wire-frame glasses, wearing an olive-green hoodie and blue jeans. The arcade is spotless and gleaming, polished near-black floor with clean neon reflections, magenta and cyan light, every cabinet in perfect repair; it is never dirty or grimy."
WBRZ="Wardrobe and character lock: the boy is 17, white, lean, pale, short dark tousled hair, wearing a coarse undyed knee-length wool tunic with a rope belt and simple leather shoes - absolutely NO modern clothing. His mother is in her forties, weathered, hair bound in a cloth, wearing a rough brown wool dress and shawl. Bronze-age roundhouse village: packed earth floors, thatch, smoke, mud."
VLOCK="Cass speaks in a relaxed, dry, modern American accent - a casual male voice, never British, never formal or theatrical. There is no narrator and no voiceover; only characters visible on screen speak."
NEG="Photorealistic, natural human motion and facial performance, correct anatomy and proportions. No slow motion unless stated. No text, captions or subtitles appearing anywhere. Characters keep exactly the same faces and clothes as in the reference images for the entire clip."
EXITSEQ="the tester's exit sequence: eyes closing in concentration, both hands raised to chest height with palms facing each other, then three slow deliberate motions - the left palm passing flat across the right, both hands rotating once around each other, then both hands closing to fists and opening again"

gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>"$V/$name.err" | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

# ============ ARCADE RESTRUCTURE ============
gen a6_sign2 8 "The three boys stand around the tooth-white pod machine. Cass points at the yellow tape across it: 'It says out of order.' Milo rips the tape off in one long satisfying pull, wads it, and tosses it over his shoulder without looking: 'It doesn't mean anything.' Cass points at a smaller red sticker: 'That one says security warning.' Milo peels that one off too and sticks it flat onto Deshawn's chest. Deshawn looks down at it, then wears it proudly. $VLOCK $WARC $NEG" --start-image $F2/f_a2_deepend_placard.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 3
gen a_ski 12 "Inside the game: a tall Black alpine ski racer in a full downhill race suit carves at ferocious speed through slalom gates, snow spraying, edges biting, crowd roar building - he blasts across the finish line, skids a huge arc to a stop, pulls off his helmet grinning, and is mobbed in a hug by his wife and two small sons. Wind, carving edges, roaring crowd, laughter. No dialogue. $NEG" --start-image $F2/f_a_ski.png --image $A/deshawn.png &
sleep 3
gen a_hard 8 "Deshawn, freshly out of the chair and still glowing: 'Honestly? It was kind of easy.' Cass steps past him and lowers himself into the white chair like it's a throne, pulls the headset down, and says with complete cockiness: 'Easy is boring. Put me on hard mode.' Deshawn's face lights up with delight: 'Ohhh - Cass wants the SMOKE!' $VLOCK $WARC $NEG" --start-image $F2/1_6_goading.png --image $A/cass_17.png --image $A/deshawn.png --image $A/milo.png &
sleep 3
gen a10_v3 12 "Close on the open side panel of the white machine: MILO's hand turns the chunky dial all the way clockwise until it clicks at the stop, then keeps his hand there, savoring it. Deshawn leans in over his shoulder, grinning. From the chair, muffled under the headset, Cass, slightly less confident: 'Wait - what does max even do?' Milo presses the button and says warmly: 'Have a nice life.' The machine's screen light blooms and floods the whole frame to white. $VLOCK $WARC $NEG" --start-image $F/1_6_toggle.png --image $A/milo.png --image $A/deshawn.png &
sleep 3

# ============ BRONZE: wardrobe sweep + funnier respawns ============
gen b1_wake3 10 "The boy's eye snaps open, cheek on the packed earth, breath visible. Off-screen a woman's voice, first quiet and far, then closer and louder, calling: 'Bren?... Bren!' Then, arriving, brisk and tired: 'Bren - Isa has the flux again. You need to go fetch more water. More's coming out of her than's going in, at this point.' He blinks up at the thatch, utterly lost. Cold morning, smoke, embers. $WBRZ $NEG" --start-image $F2/f_bronze_wake.png --image $A/cass_17.png &
sleep 3
gen b5_afterlife2 8 "The mother cradles the fevered boy against her chest by the fire, smoothing his hair, rocking, and says softly and kindly: 'Hush now. Things will be better for you in the afterlife.' His eyes flutter closed. The firelight dims and the whole frame washes gently to white over the last second. $WBRZ $NEG" --start-image $F2/f_bronze_mother.png --image $A/cass_17.png &
sleep 3
gen b6_scream2 10 "The same wake: the boy's eye snaps open on the packed earth, and far off-screen the same woman's voice is quietly calling 'Bren?...' Two seconds of stillness - then he bolts upright screaming, clawing at his temples and face with both hands, searching for a headset that is not there. His mother rushes in and grabs his shoulders: 'What's wrong, Bren?!' $WBRZ $NEG" --start-image $F2/f_bronze_wake.png --image $A/cass_17.png &
sleep 3
gen b7_name2 8 "Held by his mother by the fire, rocking slightly, the boy mutters over and over, hoarse, staring at nothing: 'My name is Cass. My name is Cass. My name is Cass.' He slowly stills. His mother strokes his hair once, and then says, gently but completely practical: '...Well. Isa has the flux. So you're going to need to go fetch more water.' $VLOCK $WBRZ $NEG" --start-image $F2/f_bronze_mother.png --image $A/cass_17.png &
sleep 3
gen b13_cry2 8 "The mother cradles the fevered boy by the fire and murmurs the same soft comfort about the afterlife being kinder; this time silent tears run steadily down the boy's face while she speaks, because he knows exactly what comes next. The frame washes to white over the final second. $WBRZ $NEG" --start-image $F2/f_bronze_mother.png --image $A/cass_17.png &
sleep 3
gen w1_again 5 "The boy's eye snaps open, cheek on the packed earth. Off-screen, his mother's voice, bright and businesslike: 'Bren! Water!' A beat. He stares at nothing and says flatly, into the dirt: '...Again.' $VLOCK $WBRZ $NEG" --start-image $F2/f_bronze_wake.png --image $A/cass_17.png &
sleep 3
gen w2_dead 6 "The boy's eye snaps open on the packed earth - and he immediately squeezes both eyes shut again and lies perfectly rigid, playing dead. A pause. His mother's voice, off-screen, closer, deeply unimpressed: 'I can see you breathing.' His eyes stay shut. One long defeated exhale through his nose. $WBRZ $NEG" --start-image $F2/f_bronze_wake.png --image $A/cass_17.png &
sleep 3
gen w3_yoke 6 "The boy wakes on his back on the packed earth to find his mother already standing directly over him, holding the heavy wooden water yoke with its two clay pots. She drops it flat across his chest: 'Water.' He wheezes. She walks off without another word. $WBRZ $NEG" --start-image $F2/f_w3_yoke.png --image $A/cass_17.png &
sleep 3
gen b16_cure3 8 "The boy sits up off the packed earth floor, his mother still standing over him, and says with sudden flat determination, looking up at her: 'The flux, yeah? I'll get you a cure for the flux.' His mother stares down at him, taken aback, and manages: '...Well. Good, then.' $VLOCK $WBRZ $NEG" --start-image $F2/f_w3_yoke.png --image $A/cass_17.png &
sleep 3

# ============ ROMAN: sighs + geometry + voice ============
gen r1_sigh 6 "The man wakes on a simple Roman bed in morning light, sits up stiffly, rubs his face with both hands, looks slowly around the unfamiliar Roman room, and lets out one enormous, world-weary sigh. No dialogue at all. Distant street sounds. $NEG" --start-image $F/3_6_roman_wake.png --image $A/cass_45.png &
sleep 3
gen r2_aq2 8 "The man stands in the Roman street staring up at the great aqueduct crossing the sky, people and carts passing around him. He takes it in for a long moment - then lets out a long, deep, defeated sigh, drops his gaze, and walks on. No dialogue. Street ambience, gulls, cart wheels. $NEG" --start-image $F/4_1_aqueduct.png --image $A/cass_45.png &
sleep 3
gen r4_boil2 10 "The man stands directly beside the kneeling woman at the fountain, one step away, and stays right next to her the entire time, pleading and gesturing at her jar: 'You need to boil it first. You can't just do the hand thing - you need to BOIL it first.' The woman stands, hoists the jar onto her hip, gives him the long flat look you give a crazy person from arm's length away, says: 'Why would I boil water?' - and walks away. He stands alone by the running fountain, arms half-raised, devastated. $VLOCK $NEG" --start-image $F/4_2_fountain_gesture.png --image $A/cass_45.png &
sleep 3
gen r12_salt3 8 "The man packs grey salt into the snow around a bronze pot, dictating: 'Salt, added to ice, lowers its melting point.' Off-screen, Tertius - a young man in his early twenties with a curious young adult male voice - asks: 'What's that one?' The man turns his head and just smiles at him, slowly, saying nothing, then goes back to packing the salt. Frost blooms on the jars. $VLOCK $NEG" --start-image $F2/4_7_icecream_bench.png --image $A/cass_45.png &
sleep 3

# ============ P4: no narrator ============
gen p4_exit2 12 "Morning light in the boarding-house room. Cass, eighty now, stands at the window; outside, the old touched woman passes and nods to him through the glass. He nods back. He steps to the middle of the room, straightens his jacket, and says out loud to the empty room, in a dry aged American voice: 'Five lifetimes. Every chore, every gate...' a small smile, '...and I am leaving through the staff door.' He performs ${EXITSEQ}, precise and unhurried - and on the final motion the room floods to pure white. There is no narrator and no voiceover; only the old man on screen speaks, with his own lips moving. $NEG" --start-image $F/7_2_exit_80.png --image $A/cass_70.png &
sleep 3

# ============ 2044 BEDROOM (set fix) ============
gen q4_real2 8 "A sleek minimal 2044 bedroom at night: floor-to-ceiling window, soft city light towers beyond, one thin warm light-strip, a low platform bed. Cass sits on the edge of the bed looking at his own open hands, and asks the empty room, quietly: 'Is any of it even real?' A beat. He exhales once, and performs ${EXITSEQ} - slow, deliberate, exact. On the final motion the whole frame floods instantly to pure white. $VLOCK $WARC $NEG" --start-image $F2/f_q_room2044.png --image $A/cass_17.png &
sleep 3
gen q7_fail2 12 "The same sleek minimal 2044 bedroom at night, the light-strip steady. Cass stands and performs ${EXITSEQ}, precise. Nothing happens. The room stays the room. He does it again - slower, perfect, every motion exact. Nothing. He looks down at his own two open hands for a long moment. Then he sits back down on the low bed, lies back, and stares at the ceiling. Quiet. $WARC $NEG" --start-image $F2/f_q_room2044.png --image $A/cass_17.png &
sleep 3
gen q8_come2 10 "The dark sleek 2044 bedroom, city glow through the window. A knock, and Deshawn's voice through the door, ordinary and immortal: 'Yo! We're going out. You coming, or you gonna sit in the dark being weird about the arcade thing all night?' Cass, sitting on the bed in the dark, looks at his open hand one last time - then closes it, and a small real smile arrives. 'Yeah.' He stands, grabbing his jacket. 'Yeah. I'm coming.' He opens the door into warm hallway light. $VLOCK $WARC $NEG" --start-image $F2/f_q_room2044.png --image $A/cass_17.png --image $A/deshawn.png &
sleep 3
wait
echo ALLDONE
