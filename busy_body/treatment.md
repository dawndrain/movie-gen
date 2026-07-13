# THE BUSY BODY — film treatment & storyboard (first pass)

Adapted from Susanna Centlivre's *The Busie Body* (1709) — full text in
`busie_body_source.txt` (Project Gutenberg #16740). A Queen Anne London farce:
two pairs of lovers outwit two tyrannical old guardians, while their
well-meaning friend Marplot — the original busybody — wrecks every scheme he
touches. No narrator; dialogue only (house rule). Dialogue below is verbatim
from the play with modernized spelling, lightly trimmed for lip-sync length.

Target: ~38 shots × 8–12s ≈ 6–7 min. Draft in 480p fast, master in std.
Nano Banana anchors/frames, TTS voice locks per MOVIE_LESSONS.md.

## The two plots (keep them legible)

- **Plot A**: MIRANDA (heiress, £30,000) is ward to SIR FRANCIS GRIPE (65,
  miser), who means to marry her himself. She fake-dotes on him ("Gardee"/
  "Chargee") to recover her fortune, while falling for SIR GEORGE AIRY (24,
  rich gallant) — whom she teases masked in the Park as his mystery
  "Incognito". She cons Sir Francis into signing away her estate and escorting
  her to her own wedding with George.
- **Plot B**: ISABINDA is locked up Spanish-style by her father SIR JEALOUS
  TRAFFICK (merchant, Spain-obsessed), promised to a never-seen Spaniard, Don
  Diego Babinetto. Her lover CHARLES (Sir Francis's disinherited son)
  impersonates the Spaniard — coached by the maid PATCH — and marries her with
  her father's own blessing.
- **The chaos agent**: MARPLOT, ward of Sir Francis, compulsively nosy,
  cowardly, loyal, catastrophic. Every act he ruins something: tips off Sir
  Jealous, exposes the chimney-board, nearly stops the wedding. Beaten in
  every act; forgiven in the last.

## Cast (anchors — one Nano Banana portrait each, full wardrobe lock)

- **marplot** — Marplot, mid-20s, round eager puppyish face, wide curious eyes,
  a black sticking-plaster across the bridge of his nose (broken in a gambling
  brawl — keep the plaster ALL film, it's his badge), brown bob-wig slightly
  askew, mustard-yellow coat a bit too flashy and a bit too worn, long
  waistcoat, breeches, scuffed shoes, small sword he never draws. Always
  breathless, always leaning in to listen.
- **george** — Sir George Airy, 24, tall, handsome, confident half-smile,
  immaculate full-bottomed dark periwig, sky-blue embroidered justacorps coat
  with silver lace, lace cravat, dress sword, tricorne. In Act V doubles as
  "MR. MEANWELL": sober plain dark-brown merchant's suit, simple tie-wig, no
  lace (generate a second anchor for the disguise).
- **charles** — Charles Gripe, 21, lean, dark-eyed, earnest and a little
  desperate, plain grey gentleman's coat (good cut, worn cuffs — he's broke),
  dark short periwig, riding boots. In Act V doubles as "DON DIEGO": theatrical
  black Spanish habit from the playhouse — short cloak, golilla collar,
  broad-brimmed Spanish hat with a red plume, slashed sleeves (second anchor).
- **miranda** — Miranda, 18, sharp amused eyes, dark hair dressed high, elegant
  rose-and-cream silk mantua gown, stays, pearl earrings, folding fan, diamond
  necklace (plot prop). Park disguise variant: loose hooded morning gown and a
  black vizard mask (second anchor: masked, hooded).
- **isabinda** — Isabinda, 19, gentle oval face, dark ringlets, modest
  dove-grey indoor gown with a hint of Spanish severity (high neck, mantilla-
  style lace shawl her father insists on). Melancholy but quick.
- **francis** — Sir Francis Gripe, 65, gaunt, stooped, sly toothy grin,
  old-fashioned long grey wig a generation stale, rusty-black coat with worn
  rich trim, cane ("Bambo"), pocket watch on a chain, purse of guineas at his
  belt. Giggles "he, he, he" when money or Miranda is near.
- **jealous** — Sir Jealous Traffick, late 50s, florid, barrel-chested,
  bristling brows, prosperous merchant's dark coat with Spanish touches —
  severe black, Toledo-style sword on the wall at home, cane in the street.
  Swears "by St. Jago!" Explodes, then melts.
- **patch** — Patch, 30s, Isabinda's maid, knowing face, crisp cap and apron
  over a practical brown gown, letters tucked in her bosom, tie-on pocket at
  her hip (the dropped-letter gag lives in it).
- **whisper** — Whisper, 20s, Charles's footman in plain livery, hunched
  conspiratorial posture, hand permanently cupped beside his mouth.
- **scentwell** — Scentwell, 20s, Miranda's maid, bright-faced, neat cap and
  apron over a striped gown.

She is the ONLY figure in the frame (add to every solo portrait prompt).

## Locations (plates)

- **loc_park** — St James's Park, 1709, early morning: gravel walk, avenue of
  limes, distant deer, a sedan chair with two chairmen. (Acts I bookend.)
- **loc_gripe_parlor** — Sir Francis's parlor: dark old oak panelling, worn
  rich furnishings, strong-box, ledger desk, cane by the chair. Miserly rich.
- **loc_miranda_room** — Miranda's chamber in Gripe's house: lighter panelling,
  dressing table with jewel casket, mantel crowded with blue-and-white china,
  and a FIREPLACE sealed by a painted CHIMNEY-BOARD big enough to hide a man.
- **loc_garden_gate** — Gripe's walled garden at dusk: brick wall, ivy, a
  wooden gate standing ajar into the park, lantern light.
- **loc_jealous_street** — street before Sir Jealous's townhouse: Georgian
  brick facade, stout front door, practical BALCONY and casement window above.
- **loc_isabinda_room** — Isabinda's chamber: closet door center-stage, small
  spinet, supper table, casement window (rope-ladder access), Spanish lattice
  vibes on the windows.
- **loc_jealous_hall** — Sir Jealous's receiving hall: merchant prosperity,
  Spanish touches (dark portraits, Toledo sword), adjoining PARLOR door — the
  climax's battleground.
- **loc_tavern** — the Thatched House tavern, private room: candles, wine
  bumpers, wooden table.

## Voice locks

Cast per-character ElevenLabs voices (Dawn's account list + ids in
`voices.md` / `elevenlabs_voices.json`). Pipeline per MOVIE_LESSONS.md: TTS
every line → per-speaker mp3s as Seedance `--audio` refs + "speak EXACTLY the
dialogue in the reference audio clips, in order, in exactly those voices."
Pitch-audition the whole cast in one batch (pitch_check.py) before committing;
spread F0 so all ten speakers stay distinct. FAST mode: one concatenated mp3
per shot (0.7s gaps), "the first line is spoken by X, the second by Y."

Every dialogue shot gets: "All characters speak in period English accents,
consistent across the whole film. There is no narrator and no voiceover; only
characters visible on screen speak, lips moving."

## Music (Sonilo, sparse — silence under comedy dialogue)

- **m_overture** — sprightly baroque harpsichord-and-strings minuet, comic and
  bustling (title + park open, reprise under the dance/finale). Instrumental only.
- **m_sneak** — pizzicato tiptoe cue for hidings/chases (chimney-board, closet).
- **m_spanish** — solo Spanish guitar sting for Don Diego's entrance.
- **m_wedding** — country-dance jig with fiddles for the finale. Instrumental only.
- The out-of-tune spinet/singing in j8 is DIEGETIC — generate it in-shot, not Sonilo.

## Production cautions (from MOVIE_LESSONS.md, applied to this script)

- The lecherous-guardian gags (Sir Francis "muzzle and tuzzle", grabbing at
  Miranda) are nsfw-filter bait: stage as hand-kissing, arm-patting, capering
  at a distance; keep all wording neutral ("takes her hand, beams at her").
  If two rewordings fail, change what happens on screen.
- Miranda's Park "dishabille" = fully-dressed hooded morning gown + mask.
- The caning/beating gags: keep cartoonish ("swats at him with his cane as
  Marplot scrambles away"), no impacts on faces.
- On-screen text (title card, the cipher letter, the forged Spanish letter):
  render in Nano Banana frames, never ask Seedance for legible text.
- Marplot's nose-plaster and self-inflicted "monkey scratches" are continuity
  props — put them in the anchor/frames, scan contact sheets for them.

---

## Shot list

Prefix = location/act: p Park, g Gripe house, t tavern, j Jealous house.
(v = start frame needed; most shots also take character anchors as `--image` refs.)

### ACT I — The Park (morning)

- **p1** — TITLE. loc_park plate, morning light; an empty sedan chair waits.
  Nano Banana text card: "THE BUSY BODY — a comedy of 1709". m_overture under.
- **p2** — George & Charles strolling. GEORGE: "I am in love with two women,
  Charles. One all wit, whose face I have never seen — and one all beauty, to
  whom I have never spoken." CHARLES: "Then between them, you have exactly one
  mistress. And my father keeps her under lock and key."
- **p3** — Marplot bounds up, black plaster across his nose, fawning. CHARLES:
  "How came your beautiful countenance clouded in the wrong place?" MARPLOT:
  "I avoid fighting, purely to be serviceable to my friends."
- **p4** — FLASHBACK GAG (silent, m_sneak): a merchant's doorstep — Marplot
  solemnly hands the love letter to the HUSBAND and presents the horses to the
  WIFE. Snap back: MARPLOT: "Pish, pox, that was an accident! I follow my
  instructions."
- **p5** — Whisper sidles up, hand cupped, murmurs in Charles's ear; Charles
  strides off. MARPLOT (aside, watching): "A secret! I shall go stark mad if I
  am not let into this secret. I must and WILL follow him."
- **p6** — Sedan chair sets down; a masked lady in a hooded gown steps out,
  meets Patch. MIRANDA: "Let the chair wait." PATCH: "The Spanish father has
  spoiled our plot — but my lady shall be only Signior Babinetto's, he says."
  MIRANDA: "Let the tyrant man make what laws he will — a woman will find a
  way to break them."
- **p7** — THE BARGAIN. Sir Francis and Sir George haggle by a tree; Miranda
  and Patch peep from behind shrubbery. George pours out a chinking purse.
  GEORGE: "Will you take the fifty guineas?" FRANCIS: "Give me a hundred, sir,
  and try your fortune. He, he, he." MIRANDA (whispered aside): "So — 'tis
  well it's no worse. I'll fit you both."
- **p8** — TURN-YOUR-BACK. George corners the masked Miranda, seizes her hand.
  MIRANDA: "If you look upon me, I shall sink, even masked as I am. Turn your
  back while I confess." He turns, rapt — she tiptoes away mid-sentence. He
  spins to empty gravel. GEORGE: "Gone! Jilted! What woman can forgive a man
  that turns his back?"

### ACT II — Gripe's house / Jealous's house

- **g1** — Miranda coos over Sir Francis in the parlor. MIRANDA: "Now methinks
  there's nobody handsomer than you — so neat, so clean, Gardee." FRANCIS:
  "Pretty rogue, pretty rogue! He, he, he." MIRANDA (aside, fan up): "Faugh —
  how he stinks of tobacco."
- **g2** — Charles begs; the cane rises. CHARLES: "Sir, some means to support
  me —" FRANCIS: "Marry Lady Wrinkle, forty thousand pound!" CHARLES: "Why,
  she has but one eye." FRANCIS: "Then she'll see but half your extravagance,
  sir! Out of my doors, you dog!"
- **g3a** — THE DUMB SCENE i. Four o'clock; Sir Francis at the back with his
  pocket watch; George bows and kisses Miranda's hand — she stands stone-
  silent. FRANCIS: "Hold, hold! Kissing was not in our agreement — that's
  contrary to articles!" GEORGE: "Keep your distance, old gentleman."
- **g3b** — THE DUMB SCENE ii. George invents sign language, cross-examining
  her. GEORGE: "A nod is yes, a shake is no. Can you prefer that old, dry,
  withered, sapless log of sixty-five to the vigorous, gay, sprightly love of
  twenty-four?" — she nods AND shakes AND sighs; he clutches his wig. MIRANDA
  (whispered aside): "How every action charms me."
- **g3c** — THE DUMB SCENE iii. The watch snaps shut; Sir Francis counts
  guineas into Miranda's palm. FRANCIS: "She has nicked you, Sir George! Ha,
  ha, ha!" GEORGE (exiting, at the door): "Marry her, old Beelzebub — and
  you'll be cuckolded. Remember that, and tremble."
- **j1** — BALCONY BUST. Isabinda takes air on the balcony; Sir Jealous rages
  below. JEALOUS: "Why don't you write a bill upon your forehead, to show
  passengers there's something to be let! In, in — and lock her up till I come
  back from 'Change!" ISABINDA (aside, retreating): "Ay — to enjoy more
  freedom than he is aware of."
- **j2** — Whisper caught lurking at the door. JEALOUS: "Have you a letter or
  message for anybody in my house, sirrah?" WHISPER: "N-no, sir — I am seeking
  Trifle, sir — the very lap-dog my lady lost!" JEALOUS: "Let me catch you no
  more puppy-hunting about my doors! O my conscience, this is some he-bawd."

### ACT III — Lovers, blunders, the coded threat

- **j3** — Isabinda's chamber; Charles in through the casement, rope ladder
  behind him; they clasp hands. CHARLES: "Fly with me now — I have raised a
  thousand pound." ISABINDA: "And love rarely dwells with poverty, Charles.
  Wait — my father cannot watch forever." PATCH (bursting in): "The master!
  Coming up the street!"
- **j4** — STREET CANING. Marplot swaggers up to Sir Jealous at his own door.
  MARPLOT: "If that gentleman comes not as safe out of your house as he went
  in, I have half a dozen Myrmidons hard by!" JEALOUS: "Went IN? What, is he
  in then? Thieves! Thieves!" — cane swats, Marplot scrambling in circles:
  "Murder! Murder! I was never in your house, sir!"
- **j5** — Charles drops from the balcony ONTO Marplot; both sprawl. MARPLOT:
  "Charles! Faith, I'm glad to see thee safe out." CHARLES (collaring him):
  "It was YOU told him? Death — I could crush thee into atoms!" MARPLOT
  (choked): "Will you... choke me... for my KINDNESS?"
- **g4** — THE BLUNDERBUSS MESSAGE. Parlor; Miranda's hand clapped in Sir
  Francis's; Marplot glowering. MIRANDA: "Tell Sir George: if he dares to
  saunter by the garden gate on the left, about the hour of eight, he shall be
  saluted with a pistol or a blunderbuss." FRANCIS: "He, he, he." MIRANDA
  (aside): "I hope he understands my meaning better than to follow YOUR advice."
- **t1** — THE TAVERN DECODE. Wine; Marplot delivers it funereally. MARPLOT:
  "You shall be saluted with a blunderbuss, sir. These were her very words."
  GEORGE (lighting up, rising): "The garden gate — at eight — as I used to do!
  There must be a meaning in this! My dear Marplot, thou art my friend, my
  better angel!" — embraces him; Marplot toasts, utterly baffled.

### ACT IV — The closet and the chimney-board

- **j6** — THE DROPPED LETTER (m_sneak). Doorstep: Patch pockets Charles's
  ciphered letter — it flutters out of the tie-on pocket behind her. Sir
  Jealous picks it up, turns it every way. JEALOUS: "Humph — 'tis Hebrew, I
  think. This may be one of Love's hieroglyphics."
- **j7** — THE TOOTHACHE CHARM. Chamber; he brandishes the paper; Patch
  snatches it to her bosom. PATCH: "My charm for the toothache! I have worn it
  these seven years — 'twas given me by an angel, sir, and must never be
  opened, on pain of dire vengeance." JEALOUS (grudging): "There, there — burn
  it, and I warrant you no vengeance will follow."
- **j8** — THE OUT-OF-TUNE CONCERT. Supper laid in Isabinda's chamber; he
  eats; Isabinda mangles the spinet, Patch croaks a song, both watching the
  closet door; outside the window, Charles climbs the rope ladder. JEALOUS
  (banging the table): "Hey, hey! Why, you are a-top of the house, and you are
  down in the cellar! Play me a TUNE, or I'll break the spinet about your ears!"
- **j9** — MAN IN THE CLOSET. The closet door swings open — Charles mid-love-
  poem — freezes at Papa mid-mouthful — slams back in. Both women SHRIEK.
  JEALOUS: "Hell and Furies — a man in the closet!" PATCH: "A ghost, a ghost!
  This comes of opening the charm!" — Isabinda swoons flat across the closet
  door. (Inside: sash up, bird flown.)
- **j10** — STREET, NIGHT. Patch, evicted with no bundle, stops Charles's
  drawn sword. CHARLES: "Here will I plant myself, and through my breast he
  shall make his passage." PATCH: "Softly, sir. What think you of PERSONATING
  this Spaniard — and marrying your mistress by her father's own consent?
  Nobody here has ever seen Don Diego." CHARLES: "My better genius! Thou hast
  revived my drooping soul."
- **g5** — GARDEN GATE, EIGHT O'CLOCK (near-silent, m_sneak). George steels
  himself at the open gate — no blunderbuss — Scentwell takes his hand.
  SCENTWELL: "This way, sir — through many a dark passage and dirty step."
- **g6** — Miranda's chamber; brisk betrothal. MIRANDA: "My guardian has
  surrendered my fortune — he thinks he weds me in the morning. My emissaries
  are luring him to Epsom tonight." GEORGE: "Then tonight thou art mine."
  SCENTWELL (rushing in): "Sir Francis, madam — and Master Marplot — at the
  door!" — George crams behind the CHIMNEY-BOARD.
- **g7** — THE ORANGE PEEL / THE MONKEY. Sir Francis ambles toward the
  fireplace, peeling an orange, peel in hand for tossing behind the board.
  MIRANDA: "Hold, hold, dear Gardee! I have a — a — a MONKEY shut up there!
  Untamed! He'll break all my china!" MARPLOT: "A monkey! Let me but peep — I
  can tame a monkey as well as the best of them — oh, how I love the little
  miniatures of man!" FRANCIS (cane up): "Let my Chargee's monkey alone, or
  Bambo shall fly about your ears!"
- **g8** — MARPLOT FINDS THE MONKEY. Alone, he doubles back and lifts the
  board. MARPLOT: "Oh Lord, Oh Lord! Thieves! Thieves! Mur—" GEORGE (seizing
  him): "Damn ye, you unlucky dog — 'tis I!" Marplot, covering, sweeps the
  china off the mantel — CRASH — and performs for the returning household:
  MARPLOT (scratching his own face): "It flew over my shoulders — scratched
  all my face — broke yon china — and whisked out of the window!"
- **g9** — KIDNAPPING THE BUSYBODY. Sir Francis gone to Epsom; George emerges;
  Patch arrives with a summons from Charles. MARPLOT: "I'm as secret as a
  priest when I'm trusted." GEORGE: "Why, 'tis with a priest our business is
  at present — and YOU, sir, come along with us where I can see you." — grabs
  the squirming Marplot by the collar and marches him out.

### ACT V — Two weddings and a sword

- **g10** — "FAREWELL, OLD MAMMON." Morning; jewels being packed; Miranda
  gloats at the door — Sir Francis is already standing BEHIND her. FRANCIS:
  "Ah, my sweet Chargee — don't be frighted." MIRANDA (frozen, then sugar):
  "I'm so surprised with JOY to see you, I know not what to say!" (Scentwell
  breezes in dangling the diamond necklace; Miranda, smooth: "Could you not
  have carried it to be MENDED, as I bid you?")
- **g11** — ESCORTED TO THE WRONG WEDDING. MIRANDA: "If ever I marry,
  positively this is my wedding day." FRANCIS (levitating): "Adod, I am
  happier than the Great Mogul! The joyful bridegroom, I —" MIRANDA (taking
  his arm, aside to camera): "— and I the happy bride." Exit arm in arm.
- **j11** — DON DIEGO ARRIVES (m_spanish sting). Jealous's hall: Charles in
  full Spanish habit sweeps a deep bow, rolling Spanish; George at his side in
  sober merchant brown. GEORGE: "Mr. Meanwell, sir, at your service — the Don
  speaks no English." JEALOUS (delighted, over the forged letter): "Meanwell
  is a very good name, and very significant! By St. Jago, my daughter weds
  tonight!" CHARLES (aside): "Yes, faith — if he knew all."
- **j12** — COMMODITIES PANIC. JEALOUS: "And the five thousand crowns, sir —
  paid down today?" GEORGE: "The crowns — but — but — but —" CHARLES (behind
  his Spanish hat, hissed): "Say we have brought it in COMMODITIES." GEORGE
  (instantly smooth): "— but of course: tobacco, sugars, spices, lemons — and
  so forth. My personal bond upon the rest."
- **j13a** — THE BRIDE WHO WON'T LOOK. Isabinda dragged in, kneels, eyes shut.
  ISABINDA: "Kill me, kill me instantly — 'twill be worse than death to wed
  him! My own hand shall cut the knot first!" (Charles, two feet away,
  vibrating; JEALOUS wavering between rage and tears.)
- **j13b** — THE WHISPERED REVEAL. George kneels beside her as peacemaker,
  low: "Suppose this Spaniard should be the very man to whom you'd fly — those
  eyes that would not look on CHARLES." ISABINDA (blazing up): "Where is he?
  Oh, let me fly into his arms!" GEORGE (through his teeth, smiling at Papa):
  "Take heed, madam — you don't betray yourself. Be all obedience." ISABINDA
  (instant demure curtsy, to her father): "Sir... do with me what you please.
  I am all obedience."
- **j14** — MARPLOT TALKS HIMSELF THROUGH THE DOOR. Street, dusk; Whisper
  lurking at the corner. MARPLOT (to the servant): "Is there not a gentleman
  within, in a Spanish habit? ... Are you SURE he is a SPANISH gentleman? For
  'tis an ENGLISH gentleman I want — though I suppose he may be DRESSED like a
  Spaniard." SERVANT (aside, sweetly holding the door wide): "Who knows but
  this may be an impostor... pray step in, sir."
- **j15** — SWORD AT THE PARLOR DOOR. JEALOUS: "STOP THE MARRIAGE!" — George
  explodes into the hall, blade out, back to the parlor door. GEORGE: "Go on,
  Mr. Tackum! I guard this passage, old gentleman — I'll see 'em signed, or
  die for't!" Servants shuffle forward and stop: SERVANT: "We are afraid of
  his SWORD, sir — take that from him and we'll knock him down presently."
  Sir Jealous, boiling over, thrashes MARPLOT instead. MARPLOT: "Why — what do
  you beat ME for? I ha'nt married your daughter!"
- **j16** — DOWNRIGHT ENGLISH. The parlor doors open on the newlyweds.
  JEALOUS: "Seize her!" CHARLES (Spanish hat off, plain English, arm round his
  bride): "Rascals, retire — she's my WIFE. Touch her if you dare; I'll make
  dogs-meat of you." JEALOUS (staggering): "Ah! Downright ENGLISH! Oh, oh, oh!"
- **j17** — THE DOUBLE REVEAL. Sir Francis marches in beaming with Miranda on
  his arm — into the riot. FRANCIS (trump card): "Rail on, gentlemen — this
  lady is my WIFE, do you see?" GEORGE (stepping beside her): "Lawfully
  begotten by ME, sir." Miranda hands Charles a parchment: MIRANDA: "The
  writings of your uncle's estate, Charles — your due these three years."
  FRANCIS (volcanic, storming out): "CONFOUND YOU ALL!"
- **j18** — FORGIVENESS + DANCE (m_wedding, fiddlers crowding in). JEALOUS
  (hand out to Charles): "Seeing thou hast outwitted me — take her, and bless
  you both." MARPLOT (mournful, rubbing his bruises): "Here's everybody happy,
  I find, but poor Pilgarlick — cuffed, kicked, and beaten in your service."
  GEORGE (clapping his shoulder): "Thy estate is next, Marplot — I'll see old
  Gripe surrender it." MARPLOT: "THAT will make me as happy as any of you!"
  The country-dance begins.
- **j19** — BUTTON. Sir Jealous, glass raised, straight to camera as the dance
  whirls behind: JEALOUS: "By my example let all parents move — and never
  strive to cross their children's love." (Freeze; m_overture reprise; cut to
  black.)

## Assembly notes

- Estimated first pass: 10 char anchors + 4 disguise/variant anchors + 8
  location plates + ~40 frames + ~38 clips (480p fast) + 4 music cues
  ≈ 800–900 credits, in line with Walter's Deal / The Variance.
- Dialogue-heavy shots (g3b, j13b, j15, j17) — measure TTS first, split at
  write-time if sum(audio)+2.5+0.8/speaker > 15s (auto-size rule).
- Running gag to exploit in the edit: Marplot's beating pratfall can be
  trimmed and reprised as a motif (repetition is comedy).
- Asides to camera (Miranda, Marplot) are the play's engine — frame them as
  quick push-in singles; the "aside" text goes in quotes like normal dialogue
  with "she turns her head to the camera and says, low:".
