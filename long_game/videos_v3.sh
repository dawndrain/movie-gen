#!/bin/bash
# v3 COMEDY CUT: arcade / bronze / roman / enlightenment-teaser. 480p std, dialogue-driven.
cd /Users/dawndrain/Code/videogen/long_game
mkdir -p outputs/video3
V=outputs/video3; F=frames; F2=frames2; A=anchors

W="Wardrobe and character lock: Cass is 17, white, lean, pale, short dark tousled hair, watchful grey eyes, wearing a plain heather-grey t-shirt, dark slim jeans, white sneakers. Deshawn is 17, Black, very tall and long-limbed, expressive mobile face, buzzed hair, wearing an iridescent blue-and-orange patterned track jacket over a black tee, black joggers, chunky white high-tops. Milo is 17, white, compact, curly brown hair, thin wire-frame glasses, wearing an olive-green hoodie and blue jeans. The arcade is spotless and gleaming, polished near-black floor with clean neon reflections, magenta and cyan light, every cabinet in perfect repair; it is never dirty or grimy."
N="Photorealistic, natural human motion and facial performance, correct anatomy and proportions. No slow motion unless stated. No text, captions or subtitles appearing anywhere. Characters keep exactly the same faces and clothes as in the reference images for the entire clip."
GESTURE="the water-greeting gesture: right hand held flat, palm down, fingers together, moving in a slow clockwise circle three times, about a hand's width above the water"

gen() {
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>"$V/$name.err" | tail -1)
  if [ -f "$out" ]; then cp "$out" "$V/$name.mp4"; echo "OK $name"; else echo "FAIL $name"; fi
}

# ============ ARCADE ============
gen a1_ddr 12 "An upbeat glossy 2020s pop track blasts from the DDR cabinet, with a female vocal hook clearly singing the words 'glitch in my heart, glitch in my heart'. Deshawn dances on the pad with lazy theatrical grace, feet landing on the arrows, loving himself. Milo films on his phone and shouts over the music: 'What are you even dancing to?' Deshawn, still dancing, not missing a beat: 'It's Glitch In My Heart. It's fleek.' Milo stares at him for a second, says flatly 'Okay. Whatever. I'm gonna go see what Cass is up to.', pockets the phone, and walks out of frame toward the back of the arcade. $W $N" --start-image $F2/1_1_arcade_wide.png --image $A/deshawn.png --image $A/milo.png &
sleep 3
gen a2_placard 8 "Cass stands alone in front of the tooth-white pod machine, hands in pockets, reading the yellow out-of-service placard taped to it, lips moving slightly as he reads. The same pop song continues from far off-screen, muffled and quieter. Slow push-in. He tilts his head at something on the placard. $W $N" --start-image $F2/f_a2_deepend_placard.png --image $A/cass_17.png &
sleep 3
gen a4_milo_arrives 8 "Cass keeps reading the placard on the white machine. Milo walks briskly into frame behind him, sees the machine, and lights up: 'Woah - they have the Deep End! What's that doing here?' Cass doesn't look up from the placard. The pop song thumps faint and distant. $W $N" --start-image $F2/f_a2_deepend_placard.png --image $A/cass_17.png --image $A/milo.png &
sleep 3
gen a5_what_it_means 10 "At the machine's small glowing screen: Cass points at the text and reads aloud, puzzled: 'It says one credit, one subjective year... what does that mean?' Milo, already running both hands over the white housing like he's frisking it for a hidden switch, answers without looking up: 'It means you can be anyone you want for a whole year. It's sick.' Deshawn leans in over their shoulders, eyes going wide. $W $N" --start-image $F2/f_a5_machine_screen.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 3
gen a6_out_of_order 12 "Cass, arms crossed: 'It says it's out of order. We can't even play it anyway.' Milo, crouched at the machine: 'Nah. That doesn't mean anything.' - and he rips the yellow tape off in one long satisfying pull, wads it, and swings open the side panel, revealing a row of chunky dials inside - 'You just need to find the control panel. With these machines you don't even need to pay.' Deshawn behind them starts bouncing on his toes. $W $N" --start-image $F2/f_a6_panel.png --image $A/milo.png --image $A/cass_17.png --image $A/deshawn.png &
sleep 3
gen a7_dibs 12 "Deshawn pushes forward: 'I want to go first.' Milo, at the open panel: 'You should be a rapper. Or a DJ.' Cass: 'You could be a basketball player. Go pro.' Deshawn, already climbing into the white reclined chair and pulling the headset down over his eyes, supremely confident: 'Nah. I want to be an alpine skier. Light me up.' $W $N" --start-image $F2/f_a6_panel.png --image $A/deshawn.png --image $A/milo.png --image $A/cass_17.png &
sleep 3

gen a8_deshawn_out 12 "Deshawn reclined in the white chair, headset on: for two seconds his hands twitch and his mouth moves silently - then he tears the headset off and erupts upright, beaming, breathless, half-shouting: 'That was INCREDIBLE! I won gold at the Olympics! I had two kids - Braden and Tucker! You need to try this!' Cass and Milo flank the chair, Cass skeptical, Milo delighted. $W $N" --start-image $F/1_5_deshawn_chair.png --image $A/deshawn.png --image $A/cass_17.png --image $A/milo.png &
sleep 3
gen a9_your_turn 10 "Milo looks at Cass: 'Cass. You go.' Cass, eyeing the chair: 'I don't know...' Milo: 'Dude. Get in there.' A beat. Cass exhales through his nose, sits down into the white chair in one motion and pulls the headset down over his eyes. $W $N" --start-image $F2/1_6_goading.png --image $A/cass_17.png --image $A/milo.png --image $A/deshawn.png &
sleep 3
gen a10_harder 12 "Close on the open panel. Deshawn, off to the side, still glowing from his run: 'Is there anything harder? I felt like my life was so easy.' Milo grins at the panel and slowly turns a chunky dial all the way clockwise until it stops: 'Oh yeah. We can make it harder.' From the chair, muffled under the headset, Cass: 'Guys?' Milo, warmly, pressing a button: 'Have a nice life.' The machine's screen light blooms and floods the whole frame to white. $W $N" --start-image $F/1_6_toggle.png --image $A/milo.png --image $A/deshawn.png &
sleep 3

# ============ BRONZE ============
gen b1_wake_mom 10 "The boy's eye snaps open, cheek on the packed earth, breath visible. Off-screen a woman's voice, first quiet and far, then closer and louder, calling: 'Bren?... Bren!' Then, arriving, brisk and tired: 'Bren - Isa has the flux again. You need to go fetch more water. More's coming out of her than's going in, at this point.' He blinks up at the thatch, utterly lost. Cold morning, smoke, embers. $N" --start-image $F/2_1_eye_open.png --image $A/cass_17.png &
sleep 3
gen b3_goat 6 "The gaunt boy hauls on the rope with his entire body weight, leaning back almost horizontal; the goat, planted, does not move one inch and chews slowly while staring at nothing; the boy's feet slide in the mud and he nearly goes down, catching himself with a furious grunt. Wind, goat bell, squelching mud. $N" --start-image $F2/f_b3_goat.png --image $A/cass_17.png &
sleep 3
gen b4_collapse 8 "Carrying the heavy yoke through the mud, the boy slows, stops, doubles over; one clay pot slips and thuds into the mud; he says weakly, to nobody, 'Uugh... I don't feel good, mom,' and sinks to one knee, hugging his stomach. Handheld, cold wind. $N" --start-image $F2/2_2_water_carry.png --image $A/cass_17.png &
sleep 3

gen b5_afterlife 8 "The mother cradles the fevered boy against her chest by the fire, smoothing his hair, rocking, and says softly and kindly: 'Hush now. Things will be better for you in the afterlife.' His eyes flutter closed. The firelight dims and the whole frame washes gently to white over the last second. $N" --start-image $F/2_3_mother.png &
sleep 3
gen b6_wake2_scream 10 "The same wake: the boy's eye snaps open on the packed earth, and far off-screen the same woman's voice is quietly calling 'Bren?...' Two seconds of stillness - then he bolts upright screaming, clawing at his temples and face with both hands, searching for a headset that is not there. His mother rushes in and grabs his shoulders: 'What's wrong, Bren?!' $N" --start-image $F/2_1_eye_open.png --image $A/cass_17.png &
sleep 3
gen b7_my_name 8 "Held by his mother, rocking slightly, the boy mutters over and over, hoarse, staring at nothing: 'My name is Cass. My name is Cass. My name is Cass.' He slowly stills. His mother strokes his hair once, and then says, gently but completely practical: '...Well. Isa has the flux. So you're going to need to go fetch more water.' $N" --start-image $F/2_3_mother.png --image $A/cass_17.png &
sleep 3
gen b8_how_do_i_leave 10 "The boy talks fast and urgently at the weathered villager, hands up: 'How do I get out of here? I was playing this game - The Deep End - at the arcade? Now how do I get out?' The villager leans slowly away from him, deeply uncomfortable, then raises one arm and points across the village: '...Go talk to her. If you're going to be acting so crazy.' $N" --start-image $F2/f_b6_villager.png --image $A/cass_17.png &
sleep 3
gen b10_forty 6 "The boy grabs the old woman's ragged sleeve, desperate: 'Forty?! I have to live to FORTY?!' But her eyes have already gone cloudy again; she beams past him and waves him off, resuming a happy muttered conversation with the empty air. He stands there with his hands still half-raised. $N" --start-image $F/2_5_touched_woman.png --image $A/touched_woman.png --image $A/cass_17.png &
sleep 3
gen b11_thud 4 "Static low shot of the empty packed-earth floor. The boy's face drops into frame from above and lands cheek-first on the earth with a heavy thud, puffing up a little dust; his eyes open slowly; one long, deeply defeated exhale. $N" --start-image $F2/f_b11_floor.png --image $A/cass_17.png &
sleep 3

gen b12_cough 6 "The boy trudges with the water yoke, coughing - hard wet racking coughs that bend him over mid-step - and keeps walking anyway, miserable, wiping his mouth with the back of his hand. Cold wind. $N" --start-image $F2/2_2_water_carry.png --image $A/cass_17.png &
sleep 3
gen b13_cry 8 "The mother cradles the fevered boy and murmurs the same soft comfort about the afterlife being kinder; this time silent tears run steadily down the boy's face while she speaks, because he knows exactly what comes next. The frame washes to white over the final second. $N" --start-image $F/2_3_mother.png --image $A/cass_17.png &
sleep 3
gen b14_three_lives 8 "The boy crouches to the muttering old woman's level, desperate, reasoning with her like tech support: 'Do I have, like, three lives or something? Die three times - and then I'm out?' She beams at him warmly and answers with cheerful complete nonsense, gesturing to the empty air beside him as if making introductions. $N" --start-image $F/2_5_touched_woman.png --image $A/touched_woman.png --image $A/cass_17.png &
sleep 3
gen b15_five_lives 8 "The boy lies cheek-down on the packed earth, eyes half-open, completely flat, and mutters to the dirt: '...Maybe five lives.' A blink. Off-screen, muffled, his mother's voice is already mid-sentence about fetching water. He closes his eyes very slowly. $N" --start-image $F/2_1_eye_open.png --image $A/cass_17.png &
sleep 3
gen b16_cure 8 "The boy sits up out of his mother's arms, suddenly composed, and says with flat determination: 'The flux, yeah? I'll get you a cure for the flux.' His mother stares at him, taken aback, and manages: '...Well. Good, then.' $N" --start-image $F/2_3_mother.png --image $A/cass_17.png &
sleep 3
gen b17_rant 10 "The boy builds the fire under the clay pot, blowing the young flame, muttering to himself with rising intensity like a man assembling a war plan: 'I need to boil water. I need a fire. I need electrolytes - sugar and salt. Honey and salt.' He stands, jaw set, firelight on his face: 'I am NOT gonna die with diarrhea coming out my ass.' $N" --start-image $F2/f_b13_fire.png --image $A/cass_17.png &
sleep 3

gen b18_germs 12 "The pot boils. The two small children, heads tilted: 'What are you doing?' The boy, stirring: 'I'm killing the germs.' The children, in flat unison: '...What?' The boy stops, exhales, and goes big, exasperated, hamming it: 'There are little spirits in the water, okay? And you need to send them away. Like this.' He performs an exaggerated slow flat-palm circle over the steaming pot, three times, maintaining eye contact with the children. The little girl copies the circle, tiny and deadly serious. $N" --start-image $F2/f_b14_kids.png --image $A/cass_17.png &
sleep 3
gen b20_solemn 10 "The young bearded king demonstrates the flat-palm circling gesture over the steaming pot fast and perfunctory, like a man who has done it ten thousand times, already half-turning away - and the gathered villagers mirror it back in perfect unison: slow, precise, reverent, eyes closed. He catches sight of this, stops, looks at them for a moment, and lets out one small private sigh. Firelight. $N" --start-image $F/3_3_water_greeting.png --image $A/cass_28.png &
sleep 3
gen b22_wish 10 "The young king slouches on his throne, chin on fist, feast roaring around him, and confides sideways to a dutiful attendant: 'I just wish I could take a bath, you know? Go back to the arcade. See my friends again. My family.' A long pause. Quieter: '...Have some ice cream.' The attendant nods along solemnly, comprehending absolutely nothing. $N" --start-image $F/3_4_bored_king.png --image $A/cass_28.png &
sleep 3
gen b23_finally 10 "Across the crowded firelit hall the old woman lifts her head and meets the king's eye. He half-rises from his seat, hope breaking across his tired face: 'It's finally over? I'm finally through?' The old woman, her eyes clear for exactly one sentence: 'Yes, child. Your next life will begin.' His face collapses from hope into dawning horror, and the frame washes to white. $N" --start-image $F/3_5_slave_nod.png --image $A/touched_woman.png &
sleep 3

# ============ ROMAN ============
gen r3_gesture_q 12 "The kneeling woman at the marble fountain performs ${GESTURE} over the mouth of her clay jar, exactly the same slow ceremonial movement as in the reference video. The man interrupts, urgent, stepping close: 'That gesture - why are you doing that gesture?' The woman, not looking up: 'I'm cleansing the water. It removes the bad spirits.' The man: 'Who TAUGHT you that?' The woman, annoyed now: 'What do you mean, who taught me? I know how to cleanse water.' She turns back to her jar. $N" --start-image $F/4_2_fountain_gesture.png --image $A/cass_45.png --video outputs/video/3_3_water_greeting.mp4 &
sleep 3
gen r4_boil_it 10 "The man pleads with the woman at the fountain, gesturing at her jar: 'You need to boil it first. You can't just do the hand thing - you need to BOIL it first.' The woman stands, hoists the jar onto her hip, gives him the long flat look you give a crazy person, says: 'Why would I boil water?' - and walks away. He stands alone by the running fountain, arms half-raised, devastated. $N" --start-image $F/4_2_fountain_gesture.png --image $A/cass_45.png &
sleep 3
gen r5_library 6 "The man leans on the library counter: 'Where is your section on Bronze Age kings?' The ancient bald librarian, without looking up from his own scroll, wordlessly extends one arm and points to a far corner. The man follows the arm with his eyes, nods, and goes. Dust motes in the window light. $N" --start-image $F2/f_r4_library.png --image $A/cass_45.png &
sleep 3
gen r6_scroll 10 "Slow pan over the man's shoulder across the scroll's dark lettering as he reads. A long beat as the words land. His free hand rises slowly into frame and covers his entire face in a complete, unhurried facepalm. Muffled through his fingers: '...I need to take a bath.' A bird chirps outside. The scroll text stays exactly as in the start image, unchanged." --start-image $F2/f_r5_scroll.png --image $A/cass_45.png &
sleep 3
gen r7_bath_pitch 12 "In the steaming bath, the man gestures grandly with a wet hand: 'If I'm going to do another time jump, I need to write all of it down. Then the technology will be waiting for me when I wake up in the future.' The young man beside him nods along absentmindedly, eyes wandering, clearly not listening. The man adds: 'And I'll pay you to write it all down for me.' The young man's head snaps around instantly: 'Paid? I can write.' $N" --start-image $F2/f_r6_bath2.png --image $A/cass_45.png &
sleep 3

gen r8_glass 6 "The man holds a cloudy lumpy glass vessel up to the furnace light between two fingers, deeply unimpressed: 'First - we're going to need better glass. This is cloudy garbage.' Off-screen, the young scribe, wounded: 'That's the finest glass in the city.' The man, still examining it: 'I know.' $N" --start-image $F/4_4_workshop.png --image $A/cass_45.png &
sleep 3
gen r9_dictate_acid 12 "The man tends the glass retort and dictates grandly, with sweeping gestures: 'Sulfuric acid catalyzes myriad reactions - sulfonation, esterification, the dehydration of sugars. It is also highly corrosive, and will damage your skin.' At the table, the overwhelmed young scribe writes with agonizing slowness, murmuring only what he actually writes: '...sulfuric... acid... will damage... your skin.' The man closes his eyes for one brief pained moment and keeps working. $N" --start-image $F/4_5_vitriol.png --image $A/cass_45.png &
sleep 3
gen r10_page 4 "Slow push-in on the papyrus workbook page and its ink doodles by lamplight; the lamp flame breathes; the scratch of a pen somewhere off-screen; embers settling. The page text and doodles stay exactly as in the start image." --start-image $F2/f_r8_page.png &
sleep 3
gen r11_dictate_blood 8 "The man taps his own chest as he dictates: 'The heart is a pump. The blood moves in a circle - round, and round, and round.' The young scribe writes carefully and murmurs as he writes: '...blood... is... important.' A beat. The man, flatly: 'Close enough.' $N" --start-image $F/4_5_vitriol.png --image $A/cass_45.png &
sleep 3
gen r12_salt_ice 8 "The man packs grey salt into the snow around a bronze pot, dictating: 'Salt, added to ice, lowers its melting point.' The young scribe, off-screen, curious: 'What's that one?' The man turns his head and just smiles at him, slowly, saying nothing, then goes back to packing the salt. Frost blooms on the jars. $N" --start-image $F2/4_7_icecream_bench.png --image $A/cass_45.png &
sleep 3
gen r13_sweet 8 "Feet up in the scroll-stuffed study, the man takes a slow spoonful from the little bronze bowl, closes his eyes to savor it, gazes around at the hundreds of scrolls filling every shelf, and says to the empty room, richly satisfied: 'Things are going to be pretty sweet in the next life.' He clinks the spoon back into the bowl. The frame washes to white at the very end. $N" --start-image $F2/f_r11_study.png --image $A/cass_45.png &
sleep 3

# ============ ENLIGHTENMENT TEASER ============
gen e1_library2 8 "The distinguished grey-haired man strides to the heavy oak counter of the candlelit Renaissance library, brisk and confident: 'Where is your section on the greatest writers of antiquity?' The ancient spectacled librarian, without looking up, wordlessly extends one arm and points into the stacks. The man nods once, satisfied, and strides off. $N" --start-image $F2/f_e1_library.png --image $A/cass_55.png &
sleep 3
gen e2_fire 10 "Slow pan across the printed chronicle page as the grey-haired man reads. A beat. He reads the last line aloud in rising disbelief: '...several sketches... by a scribe named TERTIUS?' His hand comes up into frame and he facepalms, slowly and completely, fingers dragging down his face. Candlelight. The page text stays exactly as in the start image." --start-image $F2/f_e2_parchment.png --image $A/cass_55.png &
sleep 3
gen e3_flood 6 "The grey-haired man slams a heavy tray of metal type down onto the press table with a crash, looks around the print shop with wild determined eyes, and declares to the whole room: 'Alright then. I will FLOOD the world with knowledge.' Startled apprentices look up. $N" --start-image $A/loc_print_shop.png --image $A/cass_55.png &
sleep 3
gen e4_montage 8 "A bustling early-modern market street awash in printed pamphlets: sellers hawking broadsheets, hands passing pages along, pamphlets pinned up on posts flapping in the wind, and in the foreground a fishmonger wraps a fish in a printed page, pauses, and starts reading the wrapping instead. Lively period street noise. $N" --start-image $F/5_5_pamphlet_market.png &
sleep 3
wait
echo ALLDONE