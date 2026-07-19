#!/bin/bash
# v4 COMEDY CUT back half: renaissance completion / 1926 / machine documented / arcade x2.
# 480p std, dialogue-driven, no narration. Run via pool_run.py (8-concurrent cap).
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video4
V=outputs/video4; F=frames; F2=frames2; A=anchors

WREN="Wardrobe and character lock: Cass is 55, lean, grey-streaked dark hair, trimmed grey beard, watchful grey eyes, wearing a dark ink-stained doublet under a heavy charcoal cloak. The widow is in her seventies, small, wiry, in a black widow's dress and white linen coif, bright unfocused eyes. Renaissance walled river city, tall narrow timber houses, barges, waterwheels."
WMOD="Wardrobe and character lock: Cass is 70, silver-haired, weathered handsome face, calm grey eyes, wearing a brown tweed three-piece suit over a collarless shirt. Iris is late fifties, soft round face, silver-brown hair pinned back, wool cardigan over a floral house dress. Peter is mid-twenties, bright anxious face, neat side-parted sandy hair, slightly oversized grey suit. The year is 1926: trams, filament bulbs, wireless sets."
WARC="Wardrobe and character lock: Cass is 17, white, lean, pale, short dark tousled hair, watchful grey eyes, wearing a plain heather-grey t-shirt, dark slim jeans, white sneakers. Deshawn is 17, Black, very tall and long-limbed, expressive mobile face, buzzed hair, wearing an iridescent blue-and-orange patterned track jacket over a black tee, black joggers, chunky white high-tops. Milo is 17, white, compact, curly brown hair, thin wire-frame glasses, wearing an olive-green hoodie and blue jeans. The arcade is spotless and gleaming, polished near-black floor with clean neon reflections, magenta and cyan light."
NEG="Photorealistic, natural human motion and facial performance, correct anatomy and proportions. No slow motion unless stated. No text, captions or subtitles appearing anywhere. Characters keep exactly the same faces and clothes as in the reference images for the entire clip."
EXITSEQ="the tester's exit sequence: eyes closing in concentration, both hands raised to chest height with palms facing each other, then three slow deliberate motions - the left palm passing flat across the right, both hands rotating once around each other, then both hands closing to fists and opening again"

gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>"$V/$name.err" | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

# ============ RENAISSANCE (continues after r13 white-out) ============
gen n1_bridge 8 "Cass stands on the stone bridge at dusk taking in the walled river city: waterwheels turning, barges, chimney smoke. He looks down at his older hands, touches his grey beard, and takes stock out loud: 'Fifty years old. Ten till the gate.' A beat. He points at the city like he's giving it fair warning: 'New rule. Nobody dies this time.' $WREN $NEG" --start-image $F/5_1_city_arrival.png --image $A/cass_55.png &
sleep 3
gen n2_widow 8 "In the print-shop back yard the old widow stands talking warmly to the empty air. As Cass crosses the yard behind her with a satchel she calls out without turning her head: 'Sixty, this time, child.' Cass does not break stride: 'Sixty. Got it. Thank you.' She resumes her conversation with nobody. He exits frame. $WREN $NEG" --start-image $F2/f_n2_widow.png --image $A/cass_55.png --image $A/touched_woman.png &
sleep 3
gen n3_card 10 "Cass leans close to the apothecary's window display, reading the little printed card aloud: 'For the flux - a jug of clean water, a measure of salt, a measure of honey... old wisdom, source unknown.' A long beat. His face goes slack. Quietly, to the glass: 'Those are MY measures.' Then, breaking into a disbelieving grin, half-laughing: 'Tertius, you beautiful idiot. You actually wrote it down.' The card text stays exactly as in the start image. $WREN $NEG" --start-image $F/5_2_remedy_card.png --image $A/cass_55.png &
sleep 3
gen n4_fireflash 4 "The great ancient library burning at night: a wall of shelved scrolls fully aflame, racks collapsing in cascades of embers, a pillar of sparks rising into black sky. Roaring fire, cracking timber. No people. $NEG" --start-image $F/5_3_library_fire.png &
sleep 3
gen n5_type 8 "Cass holds a single tiny metal letter up to the candlelight between finger and thumb, over a tray of hundreds of identical letters. Off-screen a young apprentice asks: 'A thousand little letters... why?' Cass, still admiring the type: 'Because I am NEVER copying anything by hand again.' He drops it in the tray with a satisfying click. $WREN $NEG" --start-image $F/5_4_type_tray.png --image $A/cass_55.png &
sleep 3
gen n6_boiler 10 "The yard, workmen stoking the firebox of the huge riveted iron boiler. Cass presses his ear flat against the iron, listening. Off-screen apprentice, nervous: 'Master... shouldn't there be some kind of gauge?' Cass, ear on the metal, supremely confident: 'I invented this thing. I can HEAR the pressure.' A deep groan of stressed metal. Cass frowns slightly: '...That's fine.' Hard cut: the entire frame blows out to pure white with a colossal metallic boom. $WREN $NEG" --start-image $F/5_6_boiler.png --image $A/cass_55.png &
sleep 3
gen n7_again 8 "Cass stands on the same stone bridge at dusk in exactly the same spot as before, staring at the city. A very long stillness. Flat, quietly: 'The press. The type. The pamphlets. Ten years.' Beat. 'All of it. Again.' He grips the parapet, leans out over the river, and screams into the valley; startled birds scatter off the water. $WREN $NEG" --start-image $F/5_1_city_arrival.png --image $A/cass_55.png &
sleep 3
gen n8_gauge 10 "The rebuilt boiler yard: a tall vertical glass mercury gauge stands proudly mounted off the boiler, a weighted safety-valve lever on top. Cass watches the silver column from several careful paces away, arms crossed, and instructs the apprentice beside him like scripture: 'Gauge first. Valve second. THEN the fire.' The boiler sighs gently; a piston walks calmly up and down. Cass exhales through his nose: 'Okay.' No pride. Just relief. $WREN $NEG" --start-image $F2/f_n8_gauge.png --image $A/cass_55.png &
sleep 3
gen n9_sixty 6 "The busy print-shop floor, presses working, pages everywhere. Cass, older and tired, pauses mid-task; across the floor the old widow lifts her head and meets his eye and nods once. He nods back. The frame washes gently to white over the last second. $WREN $NEG" --start-image $A/loc_print_shop.png --image $A/cass_55.png --image $A/touched_woman.png &
sleep 3

# ============ 1926 ============
gen m1_wake 10 "The old man wakes in the narrow boarding-house bed and goes still, staring up at the steady filament bulb. No flicker. Somewhere a wireless set reads news through static; a tram sings past outside. He sits up slowly, looks at the bulb, and a grin spreads: 'Electric light.' He swings his feet down, delighted: 'Oh, we are CLOSE to home.' $WMOD $NEG" --start-image $F/6_1_wake_1926.png --image $A/cass_70.png &
sleep 3
gen m2_tram 8 "Busy 1926 street, trams rattling past. Cass walks along the pavement; at the tram stop the old touched woman sits muttering happily to the empty air. As he passes, she looks up mid-mutter. They exchange exactly one professional nod each, like two colleagues clocking in, nothing said. He touches his hat brim and walks on. She resumes muttering. $WMOD $NEG" --start-image $F/6_2_tram_stop.png --image $A/cass_70.png --image $A/touched_woman.png &
sleep 3
gen m3_twenty 6 "Cass walks the 1926 street counting on his fingers, working it out aloud to himself: 'Gate's at eighty. So... twenty years.' He stops walking. Beat. 'That's not a speedrun. That's just... a life.' A small shrug, almost a laugh: 'Huh.' He walks on lighter. $WMOD $NEG" --start-image $A/loc_street_1926.png --image $A/cass_70.png &
sleep 3
gen m4_teach 10 "Sunlit schoolroom. Cass at the blackboard, teaching with easy pleasure: 'You don't argue about whose guess is prettier. You TEST it. Change one thing. Count what happens. The count is the boss - not you, not me. The count.' A small boy raises his hand: 'Even you, sir?' Cass, with feeling, from somewhere deep: 'ESPECIALLY me.' $WMOD $NEG" --start-image $F/6_3_teaching.png --image $A/cass_70.png &
sleep 3
gen m5_feet 10 "The boarding-house hallway. Iris stands by the door and points one finger straight down at the doormat without a word: 'Feet.' Cass obediently wipes his shoes. Iris, arms crossed: 'Honestly. Where were you raised - a mud hut?' Cass, still wiping, perfectly matter-of-fact: '...Yes, actually.' Iris, not missing a beat, already walking away: 'Then wipe like it.' A tiny smile cracks his face. $WMOD $NEG" --start-image $F/6_4_iris_doormat.png --image $A/cass_70.png --image $A/iris.png &
sleep 3
gen m6_longtime 12 "Night, the warm lamplit bedroom, the old couple side by side in bed. Cass, quietly, to the ceiling: 'I feel like I've lived a long time.' Iris, not looking up from folding back the quilt: 'Everyone our age feels that.' Cass turns his head to her: 'No. I mean... a LONG time.' A pause. Iris looks at him in the electric light, not distant at all, and says gently: 'I know you do, love. Come to bed.' She pats his hand once. He watches her, and lets it be enough. $WMOD $NEG" --start-image $F/6_5_bed_scene.png --image $A/cass_70.png --image $A/iris.png &
sleep 3
gen m7_obit 10 "The hushed library reading room. Cass, older now and alone, turns the huge pages of a bound newspaper volume, stops, and goes very still. He reads in a whisper: 'Beloved wife of...' and doesn't finish. He lays his hand flat over the four printed lines and leaves it there. The room ticks. Dust in the lamplight. Played completely straight. $WMOD $NEG" --start-image $F/6_6_obituary.png --image $A/cass_70.png &
sleep 3

# ============ THE MACHINE DOCUMENTED ============
gen p1_dinner 10 "The boarding-house dining table, Sunday roast. Peter, talking with his fork, glowing: 'It's a booth you SIT in, uncle - you live a whole LIFE in an hour! The papers are going to lose their minds. They haven't even named it yet!' Cass sets his own fork down very, very carefully, squares it with his plate, and keeps his face perfectly still. Peter: 'Uncle? You alright?' Cass, evenly: 'Wonderful.' $WMOD $NEG" --start-image $F2/f_p1_dinner.png --image $A/cass_70.png &
sleep 3
gen p2_board 10 "The firm's workroom: the brass pod machine half-assembled, engineers at work, the chalkboard of crossed-out names. A young engineer calls across the room: 'What about - The Deep End?' The room laughs and applauds; someone raps the board approvingly. Cass stands beside Peter staring at the chalkboard, his face doing absolutely nothing at all. Peter, proud: 'Good, right?' Cass, flat: 'Catchy.' $WMOD $NEG" --start-image $F/6_7_workroom.png --image $A/cass_70.png &
sleep 3
gen p3_manual 12 "Under the green banker's lamp Cass speed-reads the thick service manual, flipping pages, murmuring faster and faster: 'Age gates... save-point logic... exit conditions...' He turns one more page and freezes solid. Whispers: 'Tester overrides.' His eyes race down the page. He grips the book with both hands and whisper-screams at it: 'There's a DOOR?! There was a DOOR the WHOLE TIME?!' Off-screen Peter calls: 'Uncle?' Cass, instantly composed, turning a page smoothly: 'Marvelous craftsmanship, Peter.' $WMOD $NEG" --start-image $F/7_1_manual.png --image $A/cass_70.png &
sleep 3
gen p4_exit80 12 "Morning light in the boarding-house room. Cass, eighty now, stands at the window; outside, the old touched woman passes and nods to him through the glass. He nods back. He steps to the middle of the room, straightens his jacket, and announces to nobody: 'Five lifetimes. Every chore, every gate...' a small smile, '...and I am leaving through the staff door.' He performs ${EXITSEQ}, precise and unhurried - and on the final motion the room floods to pure white. $WMOD $NEG" --start-image $F/7_2_exit_80.png --image $A/cass_70.png &
sleep 3

# ============ THE ARCADE, AGAIN ============
gen q1_off 10 "The arcade. Milo lifts the headset off Cass's head; the machine's screen behind flashes red warning text. Deshawn is mid-sentence, delighted, shaking Cass's shoulders: '-forever, bro! Four minutes on the clock and the thing was flashing the WHOLE time, someone went for a manager-' Cass sits in the white chair blinking at his own seventeen-year-old hands, touching his smooth face like it belongs to someone else, saying nothing. The screen text stays exactly as in the start image. $WARC $NEG" --start-image $F/8_1_headset_off.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 3
gen q2_longtime 8 "Milo leans in over the chair, grinning: 'What did you DO in there? Nobody plays maxed out!' Cass looks up from his hands, and says, quiet and completely level: 'I lived a long time.' A beat - then Deshawn and Milo crack up, howling, thumping his back, while Cass does not laugh at all. $WARC $NEG" --start-image $F/8_1_headset_off.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 3
gen q3_walk 6 "Night. Clean bright suburban street under humming smart streetlights. Deshawn and Milo goof ahead, re-enacting a ski crouch, laughing. Cass trails behind, hands in pockets, and slows, looking around at the street - too clean, too easy - like a man reading a room. Distant, Deshawn: 'Bro's still IN there!' $WARC $NEG" --start-image $F/8_2_night_walk.png --image $A/cass_17.png &
sleep 3
gen q4_code1 8 "Cass's bedroom at night, city glow through the window, one steady desk lamp. Cass sits on the edge of the bed, exhales once, and performs ${EXITSEQ} - slow, deliberate, exact. On the final motion the whole frame floods instantly to pure white. $WARC $NEG" --start-image $F/8_4_code_fails.png --image $A/cass_17.png &
sleep 3
gen q5_nested 10 "The arcade - the same arcade - but a different crowd, everyone howling with laughter around the white chair. On the machine's big screen: the warning text exactly as in the start image. Deshawn, arms wide, telling the whole room: 'On EASY! We put him in on EASY - and this GENIUS found the arcade INSIDE the game and got stuck a whole level DOWN!' Milo is laughing so hard he slides down the side of a cabinet to the floor. Cass sits in the chair, freshly unplugged, staring at nothing. $WARC $NEG" --start-image $F/8_3_nested.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 3
gen q6_longtime2 8 "Milo, on the arcade floor, wheezing, tears in his eyes, manages: 'How - how was it?' Cass, dazed, utterly sincere: 'I lived a long time.' The entire arcade EXPLODES - it is somehow even funnier the second time. Deshawn has to hold onto a cabinet. Cass just sits there, deadpan, waiting for it to pass. $WARC $NEG" --start-image $F/8_3_nested.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 3
gen q7_code2 12 "Cass's bedroom at night, the same steady lamp. Cass stands and performs ${EXITSEQ}, precise. Nothing happens. The lamp stays steady. The room stays the room. He does it again - slower, perfect, every motion exact. Nothing. He looks down at his own two open hands for a long moment. Then he sits back down on the bed, lies back, and stares at the ceiling. Quiet. $WARC $NEG" --start-image $F/8_4_code_fails.png --image $A/cass_17.png &
sleep 3
gen q8_door 10 "Dark bedroom. A knock, and Deshawn's voice through the door, ordinary and immortal: 'Yo! We're going out. You coming, or you gonna sit in the dark being weird about the arcade thing all night?' Cass, sitting in the dark, looks at his open hand one last time - then closes it, and a small real smile arrives. 'Yeah.' He stands, grabbing his jacket. 'Yeah. I'm coming.' He opens the door into warm hallway light. $WARC $NEG" --start-image $F/8_5_door.png --image $A/cass_17.png --image $A/deshawn.png &
sleep 3
wait
echo ALLDONE
