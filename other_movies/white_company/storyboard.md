# THE WHITE COMPANY — storyboard (first pass, fast mode)

Adapted from *The White Company* by Arthur Conan Doyle (1891; Project Gutenberg #903,
`white_company.txt` in this folder). England/France/Spain, 1366–67.

> Alleyne Edricson, a gentle monk-raised clerk, is turned out into the world at
> twenty and falls in with two archers — the giant renegade novice Hordle John and
> the swaggering veteran Sam Aylward — who bring him to Sir Nigel Loring: a tiny,
> bald, lisping, half-blind knight who is the deadliest and most courteous man in
> England. Nigel takes command of the White Company of archers, sails to Gascony,
> and leads them through pirates, tournaments, a peasant uprising, and a doomed
> last stand in Spain, while Alleyne wins knighthood and the hand of Nigel's
> daughter Maude. Tone: warm comic chivalry that turns genuinely tragic in Spain,
> then comes home to a happy ending.

Target: ~42 shots, ~6:30, 480p **fast** draft pass per MOVIE_LESSONS.md.
Dialogue carries everything (all quoted lines are verbatim Doyle); no narrator.
Comedy dry (Nigel's politeness, John's strength gags, Aylward's French);
sincerity concentrated in the last stand and the nunnery rescue.

## Cast (anchors, `anchors/`)

| anchor | who | look (from the text) |
|---|---|---|
| alleyne | Alleyne Edricson, 20 | thin-faced, golden-haired youth, clear pensive gray eyes, comely, girl-fair skin but firm chin; sombre brown jerkin, cloak and hose, scrip, iron-shod staff |
| alleyne_squire | Alleyne, Acts III–VI | same face; squire's dress then plain steel bassinet + mail, white surcoat with red lion |
| john | Hordle John | huge red-headed giant, freckled, neck ruddy and corded like fir bark, muscles like oak roots; homespun bursting at every seam (Act I); later archer kit: steel cap, mail, white surcoat, red lion |
| aylward | Sam Aylward, ~40 | massive chest and shoulders, hazel-nut brown shaven face, long white scar from left nostril to jaw, bright searching eyes; dinted steel cap, chain-mail brigandine, white surcoat with red lion of St. George, yellow yew war-bow over shoulder, sprig of broom in cap |
| nigel | Sir Nigel Loring, 46 | very small slight man, bald as an egg, little pointed gray-streaked beard, bulging peering near-sighted eyes, soft lisping voice; purple plum-colored cote-hardie and cap with his wife's doeskin glove pinned to it (civil); white armor, ostrich plumes, shield of five scarlet roses (war); BLACK EYE-PATCH from d1 onward |
| maude | Lady Maude Loring | tall, slight, dark; jet-black hair under a light pink coif, proud head, springy step, quick white teeth; pink-slashed gown + little brown falcon on wrist (Act I); black velvet Bruges gown with white lace (castle) |
| lady_mary | Lady Mary Loring | large square red face, fierce thick brows, taller and broader than her husband, commanding eyes; rich matronly medieval dress |
| socman | The Socman of Minstead | golden flowing beard and long yellow hair, lion-like handsome face with a mad sinister sparkle in fierce blue eyes; good Norwich-cloth tunic |
| simon | Black Simon of Norwich | gaunt, spare, long-limbed man-at-arms, fierce deep-lined face framed in steel; carries the guidon of five scarlet roses; dapple-gray charger |
| oliver | Sir Oliver Buttesthorn | wondrously fat red-faced knight, black curls; dandyish olive-green doublet picked out with pink, gold-hued pointed shoes; boar's-head arms |
| chandos | Sir John Chandos | very old, tall and straight as a lance, snow-white curling hair, ONE eye (other socket scarred shut), fierce hawk face, long thin wisp of white moustache |
| prince | Edward the Black Prince | slim dark young man, clear well-chiselled features; plain dark-blue jupon tagged with gold buckles, no crown |
| duguesclin | Bertrand du Guesclin | burly, hugely broad-shouldered; hideous face — lightest-green eyes, broken flattened nose, seamed with scars; crisp curly black hair; black jerkin trimmed with sable |
| tiphaine | Lady Tiphaine du Guesclin, ~35 | queenly; aquiline nose, dark curving brows, deep-set brilliant eyes, broad white brow; chaplet of pearls in black hair, silver gauze net over shoulders, black mantle, silver cross |
| abbot | Abbot Berghersh | thin gray ascetic face, sunken haggard cheeks, long white nervous hands; white Cistercian habit |

Location plates: Beaulieu chapter house (candle-lit, oak benches, rows of white
monks) · Pied Merlin inn common room (firelight, smoke, cauldron, low black
ceiling) · Twynham Castle (Avon bridge, torchlit gateway, great hall) · the
yellow cog at sea (purple mainsail with golden St. Christopher) · Bordeaux
abbey hall + tournament lists · Villefranche castle (moat, black keep,
firelit feast hall) · snowy Roncesvalles defile · the Spanish gorge + boulder
hill with sheer cliff behind.

## Era / wardrobe locks

- **ACT I (New Forest, autumn 1366):** Alleyne in sombre clerk's clothes with staff; John in bursting homespun; Aylward the only man in war gear. Wattle-and-daub, thatch, no plate armor on villagers, NOTHING modern.
- **ACTS II–III (Twynham + sea):** Company in snow-white surcoats with the red lion of St. George over mail; Nigel's five-scarlet-roses blazon on shield, pennon and guidon everywhere.
- **ACTS IV–VI (Gascony, France, Spain, winter):** same Company kit, weathered; Nigel wears the black eye-patch in EVERY shot from d1 until f6 (then never again); Spanish knights with the yellow-and-white lions-and-towers of Castile.
- **ACT VII (Hampshire, July):** high summer, green; Alleyne in blue Brussels doublet with a scar on brow and temple.

## Voice locks (every dialogue shot)

- ALLEYNE: gentle, earnest young British tenor, educated and courteous — never American.
- SIR NIGEL: soft, mild, LISPING older British voice, unfailingly polite — the quieter the deadlier. Catchphrase "By Saint Paul!"
- AYLWARD: hearty gravelly British soldier's voice, peppered with French tags ("ma foi", "mon gar", "camarade"). Catchphrase "By my hilt!"
- HORDLE JOHN: enormous booming bass, slow rustic West-Country drawl.
- MAUDE: quick, teasing, aristocratic young British female voice.
- DU GUESCLIN: deep bestial growl with a French accent.
- TIPHAINE: low, grave, musical French-accented female voice; trance lines distant and muffled.
- Always append: "There is no narrator and no voiceover; only characters visible on screen speak, lips moving."

### ElevenLabs voice casting (candidates — pitch-audition in one batch per MOVIE_LESSONS)

Workflow: TTS the exact lines per speaker → per-speaker mp3s as Seedance `--audio`
refs ("speak EXACTLY the dialogue in the reference audio clips, in order, in
exactly those voices"). Voices marked **[lib]** are from the shared library and
must be added to the account first (elevenlabs.io → Voice Library → add, or API);
unmarked ones are already in `/v1/voices`.

| role | 1st choice | alternates |
|---|---|---|
| Alleyne | **Ethan – Warm & Trusting** [lib] `WoxRV1VQUDtxEHPVAZyL` (young British, warm, acting background) | Cassian – British Noble [lib] `Veg2qijYoJAS8VPKOOmi`; Francis – Expressive & Reflective [lib] `Q2AxzVplKbaj5rJp4P15` |
| Sir Nigel | **Henry – royal, elegant, precise diction** `VRAN0xryQGUWtDuwToRv` (old British, gentle precision — add lisp via spelling tweaks if needed) | George – Warm Storyteller `JBFqnCBsd6RMkjVDRZzb`; Nathaniel C – gentle expressive [lib] `h9CKu0pq1LSjIPhJEGCv` |
| Aylward | **Gideon – Rugged, Gravelly & Northern** [lib] `q1h5HGdnfVxp4TXTJRNN` | John of the North – warm bluff Northern [lib] `7rQX8r6PVq3gfJ8rZzyE`; Dave – gritty cheeky London [lib] `0m71kiyu84bdUcKDzG0L` |
| Hordle John | **Gravel Midnight – deep grit character voice** [lib] `M5E055lOUxMi0kJpGyE9` | Sebastian – bold baritone [lib] `1SaGpH4wLZDmppsPYVpx`; Chris – Northern UK (Durham) [lib] `AmY1pcgcEc15wyuIj50p` |
| Maude | **Mia – Elegant Storyteller** [lib] `e6qsVnCuD0MWxmhZcuKz` (young refined British) | Peach – casual friendly British [lib] `3cuC1hNj9E2jcHlIvndN`; Lily – Velvety Actress `pFZP5JQG7iQjIQuC4Bku` |
| Lady Mary | **Jan – British & Well Spoken** [lib] `s3ITUENHJxfTA8uG0Ady` (50s, deep, character) | Enid – editorial RP [lib] `byQMr3answnWiGKk0ZUm` |
| Du Guesclin | **Dracon – Feral, Demonic & Dangerous** [lib] `A921zklid24OpyVy1Elb` (dial back with punctuation; growl is right) | Bloodgrin `KTAbPR4QFlhaTpde6md8` (already in account); Achille `94VTtZwvNmsppde6nAW0` |
| Tiphaine | **Sandy Soft – Velvet** [lib] `ymZ2m14IsFBURjROEE2J` (warm mature, refined) | Lily `pFZP5JQG7iQjIQuC4Bku`; Alice `Xb7hH8MSUJpSbSDYk0k2` |
| Black Prince | **Cassius – Velvety, Measured, Commanding** [lib] `ktrGUw7rURIQyMrQZqCu` | Daniel – Steady Broadcaster `onwK4e9ZLuTAKqWW03F9`; Sebastian [lib] `1SaGpH4wLZDmppsPYVpx` |
| Chandos | **Alistair – Cultured and Articulate** [lib] `UzI1NsMEV3ni5JRkRSls` (classic seasoned old British) | AK – posh well-spoken old man [lib] `y0SYydk17lMbUIUvSf3N`; Desmond – gravelly 75+ [lib] `jAW0IMxOTz75sgLAYWp6` |
| Sir Oliver | **Raymond Verne – dynamic, expressive** [lib] `HWDDFlsSVOpTSkiLijPq` | Desmond [lib] `jAW0IMxOTz75sgLAYWp6`; Steve Wilkes – mellow deep [lib] `jr4BEb8zU7Zqyvq3fU4R` |
| Black Simon | **Sterling – Steady and Resonant** [lib] `jhBzyKbsdeM6F66SZCaK` (deep, grounded, cinematic) | Zane – sinister narrator [lib] `qbkH1EDealYs8PUoNNuB` |
| Abbot / Johnston | **AK – posh old man** [lib] `y0SYydk17lMbUIUvSf3N` (Abbot) / David Northberry – Lancashire mill-town [lib] `sAxd8ffzrizgUQNI8nre` (Johnston) | Adam – steady rich classic narrator [lib] `Gsndh0O5AnuI2Hj3YUlA` |
| Socman | **Dominic – British, Brooding & Intense** [lib] `yhf80q1381zd2JJQ4tM7` | Blackwood – sinister posh [lib] `agL69Vji082CshT65Tcy` |

Cast pitch spread target: John lowest (~70–90 Hz), Du Guesclin/Simon ~90–110,
Aylward/Oliver ~100–120, Nigel/Chandos/Abbot ~110–140 (age raspy), Alleyne/Prince
~120–150, women distinct from each other. Verify with `pitch_check.py` on the
audition mp3s before locking.

## Shots

### Act I — The Black Sheep (Beaulieu & the New Forest, autumn 1366)
| shot | dur | beat / dialogue |
|---|---|---|
| a1_bell | 6 | Cold open. The great bell of Beaulieu Abbey tolls; white-robed monks stream in from vineyard and field. No dialogue. |
| a2_trial | 10 | Candle-lit chapter house, rows of white monks. The giant novice John grins through his charges (drained the beer, dunked Brother Ambrose in the fish-pond, carried a maiden over a stream). ABBOT: "What talk is this? Is this a tongue to be used within the walls of an old and well-famed monastery?" JOHN: "By the black rood of Waltham! if any knave among you lays a finger-end upon the edge of my gown, I will crush his skull like a filbert!" |
| a3_flight | 8 | John rips the heavy oak prie-dieu from the floor as a club; monks scatter "like poplars in a tempest"; he hurls it and sprints out the abbey gate, roaring with laughter. No dialogue. |
| a4_farewell | 8 | The gate at sunset. The thin gray Abbot blesses Alleyne (staff, scrip, parting gifts). ABBOT: "Thy father willed it: one year in the world, and then choose between cloister and mankind." ALLEYNE: "I shall come back to you, father." One long look back at the abbey in golden light. |
| a5_merlin | 10 | Night. The smoky Pied Merlin common room. The gleeman finishes a filthy verse; Alleyne stands, scandalized; the room jeers "girl-faced clerk!"; John rises beside him, slowly rolling up one sleeve. JOHN: "I shall stand by him, and he shall neither be put out on the road, nor shall his ears be offended indoors." (whisper) "Hush, lad, I count them not a fly." |
| a6_aylward | 12 | The door bursts open — Aylward, scarred and mailed, blinks in the firelight, kisses Dame Eliza, porters file in behind with plunder. AYLWARD: "By my hilt! camarades, there is no drop of French blood in my body, and I am a true English bowman, Samkin Aylward by name." Raises a cup: "To Sir Claude Latour and the White Company!" |
| a7_song | 12 | Firelit tableau: the gleeman with his gilt harp, the whole room joining the refrain, Aylward beating time with a raised finger. ALL (sung/chanted): "So we'll drink all together / To the gray goose feather / And the land where the gray goose flew!" |
| a8_wrestle | 12 | Benches pushed back. The wager: Aylward's French feather-bed against John's enlistment. John hurls Aylward across the room — then Aylward's trained shoulder-throw sends the giant flying onto the sleeping drunk limner, who wakes shrieking "'Ware the ale!" and flees. AYLWARD: "By my hilt! then, I have found a man at last!" Handshake, laughter. |
| a9_rescue | 12 | Minstead clearing, rude bridge over a brown stream. The golden-bearded Socman has seized Maude (falcon on wrist); she bites his hand; Alleyne steps between them — brothers recognize each other with hatred. ALLEYNE: "Brother or no, I swear by my hopes of salvation that I will break your arm if you do not leave hold of the maid." The Socman runs for his dogs; Alleyne and Maude flee splashing up the stream. |
| a10_bank | 10 | Mossy bank under hollies, both dripping. MAUDE: "You had him at your mercy. Why did you not kill him?" ALLEYNE: "Kill him! My brother!" MAUDE: "He would have killed you. I know him, and I read it in his eyes." Her page arrives with horses; hearing Alleyne is bound for Sir Nigel's castle she bursts out laughing and rides away, waving. |

### Act II — Twynham Castle
| shot | dur | beat / dialogue |
|---|---|---|
| b1_stone | 10 | Avon bridge, evening, dogs everywhere. Tiny Sir Nigel (purple, bald, lisping) challenges the dusty travelers to move a huge fallen coping-stone. NIGEL: "I fear that I overtask you, for it is of a grievous weight." John plucks it up one-handed and hurls it into the river. NIGEL: "Good lack!" LADY MARY: "Good lack!" |
| b2_bear | 10 | Christchurch street, dusk. A huge black bear, broken chain jangling, scatters the crowd; John scoops Lady Mary to safety; little Sir Nigel strolls alone up the middle of the road and flicks the rearing bear twice across the snout with a silk handkerchief. NIGEL (gently): "Ah, saucy! saucy." JOHN (after, awed): "I was a fool not to know that a little rooster may be the gamest." |
| b3_hall | 10 | The great hall, log fire, tapestries. Aylward delivers the sealed letter — command of the White Company. Alleyne, summoned, freezes: the lady of the castle's daughter is the girl from the forest. MAUDE (mischief): "Ma foi! and here is our wandering clerk." NIGEL: "By Saint Paul! it is a very honorable venture. Alleyne Edricson, you shall ride as my squire." |
| b4_veil | 12 | Pre-dawn. Torchlit muster in the bailey below; Maude weeping at the armory window; Alleyne's dam breaks. ALLEYNE: "You are my heart, my life, my one and only thought." MAUDE: "Win my father's love, and all may follow." She presses her GREEN VEIL into his hand and is gone. |
| b5_march | 8 | The Company marches over Christchurch bridge in snow-white surcoats with the red lion, drums and nakirs. At the forest edge Nigel binds Lady Mary's glove to his cap. NIGEL: "Your glove, my life's desire! I shall proclaim you the fairest and sweetest in Christendom, and joust with any who deny it." |

### Act III — The Yellow Cog (the Channel, winter)
| shot | dur | beat / dialogue |
|---|---|---|
| c1_sail | 8 | The canary-yellow cog under its purple mainsail with the golden St. Christopher; frosty breath, steel-blue sea. Two long black galleys knife out from behind the headland "like two fierce lean wolves." HAWTAYNE: "I like it not. And yet Goodwin Hawtayne is not the man to stand back when his fellows are for pressing forward." |
| c2_ruse | 10 | Archers lie flat behind the bulwarks feigning a helpless merchantman; drums and a hundred oars close in; then trumpets — bowmen rise as one and loose point-blank; grappling anchors bite. NIGEL: "Ma foi! but they come to our lure like chicks to the fowler. To your arms, men! Now blow out the trumpets, and may God's benison be with the honest men!" |
| c3_melee | 12 | Deck melee. John catches the pirate giant's mace-arm and bends it back with a crack; the second galley cuts its cable and drifts off WITH Sir Nigel aboard — John holds bleeding Alleyne back and narrates the far-off duel. JOHN: "My God, but it is a noble fight! ... Ah, by Our Lady, his sword is through him! Down goes the red cross, and up springs Simon with the scarlet roses!" Cheers. |

### Act IV — Bordeaux
| shot | dur | beat / dialogue |
|---|---|---|
| d1_patch | 8 | The quay at Bordeaux, forest of masts, trumpets. Sir Nigel kneels and binds a black patch over one eye. NIGEL: "I vow that I will not take this patch from my eye until I have seen something of this country of Spain." AYLWARD (aside, to Alleyne): "There will come bloodshed of that patch, or I am the more mistaken." |
| d2_chandos | 8 | Abbey hall. The snow-haired, one-eyed Chandos sweeps Nigel into an embrace. CHANDOS: "Ha, my little heart of gold! Since you have tied up one of your eyes, and I have had the mischance to lose one of mine, we have but a pair between us." |
| d3_prince | 12 | Scarlet-canopied dais; the Black Prince between two puppet kings. Nigel learns the Prince has vowed to hang the White Company's captain — his own new post — and gravely insists the vow be honored. NIGEL: "It is a very small matter that I should be hanged, but it would be a very grievous thing that you should make a vow and fail to bring it to fulfilment." PRINCE (laughing): "Peace! peace! I am very well able to look to my own vows and their performance." The court roars. |
| d4_tourney | 10 | The lists by the Garonne, a dark sea of heads. Final course: Nigel vs. the black-armored Teuton — lances shatter, Nigel's helmet flies off, his bald head shining in the sun; he trots calmly back for another helmet and wins the third course. PRINCE: "Who comes next for England, John?" CHANDOS: "Sir Nigel Loring of Hampshire, sire." |
| d5_stranger | 10 | Sunset. An unknown French knight — squat, immensely broad, vizor never opened — has felled four champions and fought Nigel to a standstill; now he refuses the Prince's wine. KNIGHT: "I will neither drink your wine nor sit at your table. I bear no love for you or for your race." He gallops off down the empty white road. PRINCE (quiet): "By St. George! he has served his master this day even as I would wish liegeman of mine to serve me." |

### Act V — France & the Jacquerie (winter)
| shot | dur | beat / dialogue |
|---|---|---|
| e1_road | 8 | Riding montage: white frozen roads, black vine-stumps, then over the marches — burned farmsteads, gray gable-ends, gaunt ragged figures watching motionless from the tree-line. Distant swine-herd horns. No dialogue. |
| e2_inn | 12 | Firelit inn. A hideous broad-shouldered Frenchman cracks nuts in his teeth, then explodes up. DU GUESCLIN: "Dogs of England, must ye be lashed hence? Tiphaine, my sword!" — he sees the five-roses shield and his scarred face splits into delight: "Mort Dieu! it is my little swordsman of Bordeaux." NIGEL: "Bertrand! Bertrand du Guesclin!" Warrior embrace. |
| e3_prophecy | 12 | Villefranche feast hall, firelight. Lady Tiphaine's cheeks blanch; her eyes fix on the wall; her voice comes low and muffled, from far away. TIPHAINE: "Danger, Bertrand — deadly, pressing danger — which creeps upon you and you know it not." DU GUESCLIN: "But is this so very close, Tiphaine?" TIPHAINE: "Here — now — close upon you!" Outside, a swine-herd horn answers from the dark woods. |
| e4_night | 8 | Alleyne's moonlit chamber window. Below, crouching figures with burdens cross the glade from wood to wood — he counts and counts. ALLEYNE: "Seventy and nine. My God! What has come upon us?" A muffled cry somewhere in the castle; his candle gutters. (Ford's murder stays OFF-SCREEN — see risk notes.) |
| e5_hall | 10 | The torch-lit hall door: Nigel and Du Guesclin, half-armored, shoulder to shoulder against the mob of Jacks. DU GUESCLIN: "France and England will fight together this night." NIGEL: "There are many ways in which a man might die, but none better than this." Arrows from the stair clear the doorway. |
| e6_keep | 8 | The dash to the keep — wrong key! John braces, tears the entire door off its hinges, and holds the stair while the others pass. Firelight, smoke, press of bodies. AYLWARD: "By my hilt! up, up, mes enfants!" |
| e7_powder | 10 | The leaning tower top ringed by fire, thousands dancing below. Alleyne spots the powder-box by the bombards. NIGEL: "Throw back the lid, John, and drop the box into the fire!" John heaves it over the parapet — a white flash, a world-filling BOOM, the tower rocks. |
| e8_song | 12 | Silence, smoke, five souls waiting to die 100 feet up. TIPHAINE: "Hush and listen! I have heard the voices of men all singing together in a strange tongue." Far off, swelling: "We'll drink all together / To the gray goose feather / And the land where the gray goose flew." AYLWARD: "By these ten finger-bones, we are saved! It is the marching song of the White Company. Hush!" Two hundred bowmen pour from the woods. |
| e9_tree | 10 | Dawn camp; Nigel on the great fallen tree ringed by upturned faces; the dapper Gascon Latour makes his silky counter-pitch of plunder and Italy. NIGEL: "I have lived in honor, and in honor I trust that I shall die." LATOUR: "I will not go to Dax." JOHN (roaring): "The proper life for a robber!" The Company thunders for Nigel; thirteen defectors slink off hissed. |

### Act VI — Spain (March 1367)
| shot | dur | beat / dialogue |
|---|---|---|
| f1_pass | 8 | The snowy defile of Roncesvalles at dawn: the Company leading an unbroken river of steel between rose-lit peaks, breath steaming like a cauldron. BLACK SIMON: "Yonder is where Roland fell." No other dialogue. |
| f2_volunteers | 10 | Vale of Pampeluna. Nigel asks who will volunteer to ride ahead into Spain; the four ranks stand stone-still; his face falls. NIGEL: "That I should live to see the day! What! not one——" ALLEYNE (whisper): "My fair lord, they have all stepped forward." Beat. OLIVER: "And I come also." NIGEL: "For honor?" OLIVER: "For pullets." |
| f3_raid | 10 | Dusk. Nigel in captured Spanish armor rides with his three into the heart of a 60,000-tent camp; Felton's diversion erupts in flame on the skyline. NIGEL: "I have come for the king; and, by Saint Paul! he must back with us or I must bide here." They burst from the royal pavilion, a limp body in Castile's surcoat over John's shoulder, and gallop through the chaos. |
| f4_mist | 10 | Cold March morning; the trapped gorge; the Company forms on the boulder hill, sheer cliff at their backs. The mist shreds away — wall-to-wall glittering Spanish host, banners, Moorish cymbals. NIGEL: "Now order the ranks, and fling wide the banners, for our souls are God's and our bodies the king's, and our swords for Saint George and for England!" |
| f5_duel | 12 | Champions' duel between the armies: lances shatter, swords whirl, the grapple to the ground — Nigel pinned, dagger-flash, the Spaniard sags. Riding back through the cheers he calmly PLUCKS THE PATCH FROM HIS EYE. NIGEL: "I think that I am now clear of my vow, for this Spanish knight was a person from whom much honor might be won." |
| f6_storm | 8 | The cavalry charge breaks under the arrow-sleet — a wall of fallen horses builds at the slope's foot. Then sling-stones hiss from the flanking cliffs; old Johnston drops mid-sentence, an arrow still in his fingers. AYLWARD (hoarse): "Johnston! ...Loose steady, mes garcons. Every shaft well sent." |
| f7_stand | 10 | The last stand on the plateau. Fat Sir Oliver grapples the giant warrior-prior and both plunge locked over the cliff; Black Simon falls ringed by his slain. BURLEY: "Might we not even now make a retreat?" NIGEL: "My soul will retreat from my body first! Here I am, and here I bide, while God gives me strength to lift a sword." The Company's triple battle-shout rolls round the crags. |
| f8_cliff | 12 | The rear cliff. The rope. Nigel kisses Alleyne on the cheek, tears in his eyes. ALLEYNE: "I pray you, my dear lord, that you will give my humble service to the Lady Maude, and say to her that I was ever her true servant and most unworthy cavalier." NIGEL: "Now may God speed ye, for ye are brave and worthy men." Alleyne swings down the rock face as stones spark around him; above, faint, three deep shouts. |
| f9_after | 12 | Calverley's riders top the ridge too late: the banner of Castile on the corpse-strewn hill. On the plateau seven bloodied bowmen — John at their center, sitting calmly ON his prisoner, the saved Company banner leaning behind him. ALLEYNE: "Tell me, John: where is my dear lord, Sir Nigel Loring?" JOHN: "He is dead, I fear. I saw them throw his body across a horse and ride away with it." SIR HUGH CALVERLEY: "Nay — the White Company is here disbanded." |

### Act VII — The Home-coming (Hampshire, July)
| shot | dur | beat / dialogue |
|---|---|---|
| g1_news | 8 | Green July lanes; Sir Alleyne (scarred, in blue) and John ride home rich. A stout lady beside her toppled gilt carriage gossips. LADY: "News hath come that not one of the Company was left alive, and so, poor lamb, she takes the veil at Romsey this very day." ALLEYNE: "Lady! Is it the Lady Maude Loring of whom you speak? — And I stand talking here! Come, John, come!" Wild gallop. |
| g2_nunnery | 12 | Romsey: flower-strewn street, incense, twenty-two white-clad singers; Maude, wreathed in white blossoms, one step from the black church arch. A dust-caked rider scatters the procession and bars the door. ALLEYNE: "Maude! The Company fell — but I live, and I am come for you." She falls sobbing into his arms; they walk away hand in hand, backs to the darkness, faces to the light. |
| g3_inn | 12 | A green-bush inn near Pitt's Deep. AYLWARD (alive! chasing two laughing serving-girls): "Ah, mes belles! I have been among the black paynim, and, by my hilt! it does me good to look at your English cheeks." Then from the upper window, a mild lisping voice: NIGEL: "Tell him that a very humble knight of England abides here, so that if he be in need of advancement, or have any small vow upon his soul, or desire to exalt his lady, I may help him to accomplish it." Alleyne's face. Triple embrace. |
| g4_end | 10 | Sunset: the four ride together toward the dark keep of Twynham, the red sun lying athwart the rippling Avon. Final tableau at the Pied Merlin, years on: Aylward the landlord at the door, John the rich franklin with his tankard, the refrain rising once more: "So we'll drink all together / To the gray goose feather / And the land where the gray goose flew." Fade out. |

## Title cards (static Nano Banana frames, cut in at assembly)
- t_title: "THE WHITE COMPANY" over the five-scarlet-roses banner against mist
- t_1366: "ENGLAND, 1366" (after a1 or over it)
- t_france: "FRANCE" (before e1)
- t_spain: "SPAIN, 1367" (before f1)
- t_home: "HAMPSHIRE, FOUR MONTHS LATER" (before g1)

## The Song of the Bow (diegetic motif)
Public-domain Doyle lyrics. Don't ask Seedance to invent the melody: TTS the
refrain as a rhythmic unison chant (one mp3, "sung roughly, like marching
soldiers") and pass it as the audio ref for a7, e8, g4; Sonilo provides the
underlying instrumental tune. The refrain is the film's musical spine —
tavern (joy), rescue (salvation), epilogue (memory).

## Music (Sonilo, later pass ok)
- Cold-open cue: sparse monastic chant/bells feel under a1–a3.
- Tavern reel (fiddle + drum, rowdy) under a6–a8.
- "Omen" stinger reused at e3 (prophecy), e4 (night), f6 (Johnston).
- March/battle cue: bold medieval drums + brass for f4–f7 (keep LOW under dialogue).
- Elegy under f9 (the disbanded Company).
- Warm homecoming cue g2–g4, resolving into the bow-song melody.
- All: "Instrumental only, no vocals." Mix 0.07–0.12 under dialogue, ~0.20 stingers.

## Prompt-risk notes (per MOVIE_LESSONS)
- **Hanging imagery is a likely nsfw trigger**: Ford's body on the rope, the hanged
  robber, Tete-noire's yard-arm corpses are all CUT or kept off-screen (e4 shows
  only Alleyne's face + the crossing figures). Don't reintroduce them in prompts.
- The Flagellants scene (self-scourging, blood) is deliberately omitted.
- **Banned word "slave"**: the epilogue backstory (galley captivity) is only
  referenced as "among the black paynim" — never describe rowing captivity in a prompt.
- Battle prompts: "arrows fly, men fall" phrasing; no gore close-ups, no blood pools.
- Maude at the nunnery: neutral wording ("young woman in white novice robes"),
  no appearance-focused adjectives (Nano Banana female-portrait trap).
- The bear: staged comedy, "the bear rears up and the small knight taps its nose
  with a silk handkerchief" — keep it storybook, not an animal attack.
- Sir Nigel's eye-patch: state "black eye-patch over LEFT eye" in every Act IV–VI
  frame/clip prompt, and "NO eye-patch" in every other act, or it will bleed.

## Budget estimate (fast pass)
42 shots ≈ 415s × 1.5 cr/s ≈ 620 cr video + ~16 anchors + ~45 frames + 5 title
cards (few cr each) + ~7 music cues ≈ 30 cr. **Total ≈ 750–800 credits** for the
full first draft. STD master of a locked ~6:30 cut later ≈ 1,250 cr.
