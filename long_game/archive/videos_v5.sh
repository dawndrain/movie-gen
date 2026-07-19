#!/bin/bash
# v5 RETAKE PASS: cold open + user notes (old 15 + new 6). 480p std. Run via pool_run.py.
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video5
V=outputs/video5; F=frames; F2=frames2; A=anchors

WARC="Wardrobe and character lock: Cass is 17, white, lean, pale, short dark tousled hair, watchful grey eyes, wearing a plain heather-grey t-shirt, dark slim jeans, white sneakers. Deshawn is 17, Black, very tall and long-limbed, expressive mobile face, buzzed hair, wearing an iridescent blue-and-orange patterned track jacket over a black tee, black joggers, chunky white high-tops. Milo is 17, white, compact, curly brown hair, thin wire-frame glasses, wearing an olive-green hoodie and blue jeans. The arcade is spotless and gleaming, polished near-black floor with clean neon reflections, magenta and cyan light, every cabinet in perfect repair; it is never dirty or grimy."
WSIXTY="Wardrobe and character lock: Cass is exactly 60 years old here, matching the reference portrait: hair steel-grey heavily streaked with the last of the dark, face lined and weathered but NOT elderly, calm grey eyes, wearing a brown tweed three-piece suit over a collarless shirt. The year is 1926: trams, filament bulbs, wireless sets."
NEG="Photorealistic, natural human motion and facial performance, correct anatomy and proportions. No slow motion unless stated. No text, captions or subtitles appearing anywhere. Characters keep exactly the same faces and clothes as in the reference images for the entire clip."
EXITSEQ="the tester's exit sequence: eyes closing in concentration, both hands raised to chest height with palms facing each other, then three slow deliberate motions - the left palm passing flat across the right, both hands rotating once around each other, then both hands closing to fists and opening again"

gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>"$V/$name.err" | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

# --- Cold open ---
gen t0_onelife 5 "Very slow push-in on the glowing arcade machine screen displaying its amber text, exactly as in the start image, the text never changing. Dark arcade bokeh breathes around the edges, magenta and cyan neon shifting softly. A low electrical hum, the muffled thump of a distant pop song, one soft coin-clink. Subtle CRT flicker. No people." --start-image $F2/f_t0_onelife.png &
sleep 3
# --- Arcade retakes ---
gen a1_ddr2 12 "An upbeat glossy 2020s pop track blasts from the DDR cabinet, with a female vocal hook clearly singing the words 'glitch in my heart, glitch in my heart'. Deshawn dances on the pad with effortless flawless precision - hitting every arrow perfectly while barely looking, loving himself. Milo films on his phone and shouts over the music: 'What are you even dancing to?' Deshawn, still nailing every step, shrugs happily: 'No idea. It's fleek though.' Milo stares at him for a second, says flatly 'Okay. Whatever. I'm gonna go see what Cass is up to.', pockets the phone, and walks out of frame toward the back of the arcade. $WARC $NEG" --start-image $F2/1_1_arcade_wide.png --image $A/deshawn.png --image $A/milo.png &
sleep 3
gen a8_out2 12 "Deshawn reclined in the white chair, headset on: for two seconds his hands twitch and his mouth moves silently - then he tears the headset off and erupts upright, beaming, breathless, half-shouting: 'That was INCREDIBLE! I won gold at the Olympics! I had two kids - Braden and Tucker! Dude, I had the WHITEST name! You need to try this!' Cass and Milo flank the chair, Cass skeptical, Milo delighted. $WARC $NEG" --start-image $F/1_5_deshawn_chair.png --image $A/deshawn.png --image $A/cass_17.png --image $A/milo.png &
sleep 3
# --- Bronze retakes ---
gen b20_solemn2 10 "The young bearded king demonstrates the flat-palm circling gesture over the steaming pot with open sarcasm - lazy, exaggerated, one eyebrow raised, wiggling his fingers at the end, clearly mocking his own invention - and the gathered villagers mirror it back in perfect unison: slow, precise, reverent, eyes closed. He catches sight of this, stops, looks at them for a long moment, and lets out one small private sigh. Firelight. $NEG" --start-image $F/3_3_water_greeting.png --image $A/cass_28.png &
sleep 3
gen b22_wish2 10 "The young king slouches on his throne, chin on fist, feast roaring around him, and confides sideways to his attendant - a short, stout, much older man with a round face and a thick grey beard, looking nothing like the king: 'I just wish I could take a bath, you know? Go back to the arcade. See my friends again. My family.' A long pause. Quieter: '...Have some ice cream.' The old attendant nods along solemnly, comprehending absolutely nothing. $NEG" --start-image $F/3_4_bored_king.png --image $A/cass_28.png &
sleep 3
gen b23_finally2 10 "Across the crowded firelit hall the old woman lifts her head and meets the king's eye. He half-rises from his seat, hope breaking across his tired face: 'It's finally over? I'm finally through?' The old woman, her eyes clear for exactly one sentence: 'Yes, child. Your next life will begin.' His face collapses from hope into dawning horror and he croaks: 'My NEXT life?!' - and the frame washes to white. $NEG" --start-image $F/3_5_slave_nod.png --image $A/touched_woman.png &
sleep 3
# --- Roman retakes ---
gen r1_wince 8 "The man wakes on a simple Roman bed in morning light, sits up stiffly, winces hard, grabs his lower back, and takes inventory out loud through gritted teeth: 'Ow. OW. Everything hurts.' He looks down at his weathered, calloused hands, turns them over, and sighs: '...How old am I THIS time?' $NEG" --start-image $F/3_6_roman_wake.png --image $A/cass_45.png &
sleep 3
gen r5_library2 6 "The man leans on the library counter, projecting casual grandeur: 'Where is your section on the GREAT Bronze Age kings? The... legendary ones.' The ancient bald librarian, without looking up from his own scroll, wordlessly extends one arm and points to a far corner. The man follows the arm with his eyes, nods, and goes. Dust motes in the window light. $NEG" --start-image $F2/f_r4_library.png --image $A/cass_45.png &
sleep 3
gen r9_acid2 12 "The man tends the glass retort and dictates grandly, with sweeping gestures: 'Take this down, Tertius. Sulfuric acid catalyzes myriad reactions - sulfonation, esterification, the dehydration of sugars. It is also highly corrosive, and will damage your skin.' At the table, Tertius - a young man in his early twenties - writes with agonizing slowness, murmuring in a young adult male voice only what he actually writes: '...sulfuric... acid... will damage... your skin.' The man closes his eyes for one brief pained moment and keeps working. $NEG" --start-image $F/4_5_vitriol.png --image $A/cass_45.png &
sleep 3
gen r12_salt2 8 "The man packs grey salt into the snow around a bronze pot, dictating: 'Salt, added to ice, lowers its melting point.' Off-screen, Tertius - a young man in his early twenties, his voice a curious young adult male voice, definitely not a child - asks: 'What's that one?' The man turns his head and just smiles at him, slowly, saying nothing, then goes back to packing the salt. Frost blooms on the jars. $NEG" --start-image $F2/4_7_icecream_bench.png --image $A/cass_45.png &
sleep 3
# --- 1926 age fix ---
gen m1_wake2 10 "The man wakes in the narrow boarding-house bed and goes still, staring up at the steady filament bulb. No flicker. Somewhere a wireless set reads news through static; a tram sings past outside. He sits up slowly, looks at the bulb, and a grin spreads: 'Electric light.' He swings his feet down, delighted: 'Oh, we are CLOSE to home.' $WSIXTY $NEG" --start-image $F2/f_m1_wake60.png --image $A/cass_60.png &
sleep 3
gen m2_tram2 8 "Busy 1926 street, trams rattling past. The man walks along the pavement; at the tram stop the old touched woman sits muttering happily to the empty air. As he passes, she looks up mid-mutter. They exchange exactly one professional nod each, like two colleagues clocking in, nothing said. He touches his hat brim and walks on. She resumes muttering. $WSIXTY $NEG" --start-image $F2/f_m2_tram60.png --image $A/cass_60.png --image $A/touched_woman.png &
sleep 3
gen m3_twenty2 6 "The man walks the 1926 street counting on his fingers, working it out aloud to himself: 'Gate's at eighty. So... twenty years.' He stops walking. Beat. 'That's not a speedrun. That's just... a life.' A small shrug, almost a laugh: 'Huh.' He walks on lighter. $WSIXTY $NEG" --start-image $A/loc_street_1926.png --image $A/cass_60.png &
sleep 3
# --- Machine act retake ---
gen p2_board2 10 "Peter leads his uncle into the firm's workroom: the brass pod machine half-assembled, engineers at work around it. The old man stops dead at the sight of the machine. Peter steps beside it and spreads his arms proudly: 'And we're calling it... The Deep End.' A beat. The old man's face does absolutely nothing at all. Peter: 'Good, right?' The old man, perfectly flat: 'Catchy.' Wardrobe and character lock: the uncle is 70, silver-haired, weathered handsome face, brown tweed three-piece suit. Peter is mid-twenties, bright anxious face, neat side-parted sandy hair, slightly oversized grey suit. $NEG" --start-image $F/6_7_workroom.png --image $A/cass_70.png &
sleep 3
# --- Arcade-again retakes ---
gen q1_off2 10 "The arcade. Milo lifts the headset off Cass's head; the machine's screen behind flashes red warning text. Deshawn is mid-sentence, delighted, shaking Cass's shoulders: '-bro, you were in there for OVER four minutes! The thing was flashing the WHOLE time, someone went for a manager-' Cass sits in the white chair blinking at his own seventeen-year-old hands, and echoes hollowly, to nobody: '...Over four minutes.' The screen text stays exactly as in the start image. $WARC $NEG" --start-image $F/8_1_headset_off.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 3
gen q4_code1b 8 "Cass's bedroom at night, city glow through the window, one steady desk lamp. Cass sits on the edge of the bed looking at his own open hands, and asks the empty room, quietly: 'Is any of it even real?' A beat. He exhales once, and performs ${EXITSEQ} - slow, deliberate, exact. On the final motion the whole frame floods instantly to pure white. $WARC $NEG" --start-image $F/8_4_code_fails.png --image $A/cass_17.png &
sleep 3
wait
echo ALLDONE
