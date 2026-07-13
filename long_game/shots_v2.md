# The Long Game — Shots v2 (Chapters I–IV)

## How to read this document

Each shot entry has a status and up to two blocks:

- **KEEP v1 clip** — no generation. The existing video in `outputs/video/` is used
  unchanged (its original prompt is in `videos_ch1-4.sh`). Only narration is added.
- **RETAKE** / **NEW** — a video gets generated; the full Seedance prompt is included
  under **Prompt:**.
- **VO:** — the voiceover narration line for that shot. This is NOT a prompt and is
  never sent to Seedance; it's recorded/generated separately and mixed over the clip in
  post. It describes what the narrator says while the shot plays, not what's on screen.

So the film = (kept v1 clips + new/retaken clips) with the VO track laid over the top.

The v1 diagnosis, in order of importance:

1. **No voice.** The story's prose IS the film. v2 is narration-driven: every shot gets a
   VO line (adapted nearly verbatim from the story) laid over it in post, plus in-clip
   dialogue wherever the story has it (Seedance lip-syncs quoted lines). Narration is
   generated/recorded separately and mixed with ffmpeg — costs no credits and can be
   iterated freely.
2. **Disjointedness.** Missing connective beats are added as new shots: the remembering,
   the happy-king stretch, the ice-cream experiment that sets up the bath, the touched
   woman planted in the background before her scene. Setups now precede payoffs.
3. **Minimalist prompts.** Every video prompt is now a full director's treatment:
   wardrobe, performance beats in order, camera, lighting, audio, and explicit
   "do nots". The model improvises whatever you don't specify — so specify everything.

## Continuity bible (paste-into-every-prompt blocks)

**THE GESTURE (identical wording everywhere it appears):**
> the water-greeting gesture: right hand held flat, palm down, fingers together, moving
> in a slow clockwise circle three times, about a hand's width above the water

**Arcade wardrobe locks (every 2044 shot):**
> Cass: 17, white, lean, pale, short dark tousled hair, watchful grey eyes, plain
> heather-grey t-shirt, dark slim jeans, white sneakers.
> Deshawn: 17, Black, very tall and long-limbed, expressive face, buzzed hair,
> iridescent blue-and-orange patterned track jacket over black tee, black joggers,
> chunky white high-tops.
> Milo: 17, white, compact, curly brown hair, thin wire-frame glasses, olive-green
> hoodie, blue jeans.
> The arcade: spotless and gleaming, polished near-black floor with clean neon
> reflections, magenta and cyan light, cabinets in perfect repair. It is never dirty,
> dusty, or grimy.

**Global negative block (every shot):**
> Photorealistic, natural human motion and facial performance, correct anatomy and
> proportions. No slow motion unless stated. No text, captions, subtitles, dates, or
> logos anywhere in frame. Characters keep exactly the same faces and clothes as in the
> reference images for the entire clip.

## Narration voice

Third-person, close, dry, warm — the story's own sentences trimmed for the ear. One
consistent older male voice, unhurried. (Options: Dawn records it, or ElevenLabs/other
TTS; either way it's a post step, zero generation credits, endlessly revisable.)

---

## Chapter I — The Arcade (rebuild, 8 shots, ~70s)

### 1.1 — WIDE: the retro floor (10s)
**VO:** "The retro floor was where you went to be seen not caring. Deshawn was up on the
DDR pad doing a song from before any of them were born, losing on purpose, and making
losing look like the coolest thing a body could do."
**Prompt:** Wide shot inside a spotless futuristic retro arcade at night, magenta and
cyan neon, a huge neon sign reading RETRO on the back wall. [ARCADE WARDROBE LOCKS.]
Deshawn stands on a proper DDR arcade machine — a dance cabinet with a large screen
showing scrolling arrows, metal safety bar behind him, the pad physically part of the
cabinet — dancing at one-third speed with deliberate theatrical grace: a lazy spin, an
exaggerated slow lunge onto one arrow panel, arms flowing, head tipped back laughing,
fully human weight and balance in every step. Milo stands just off the pad filming him
on a phone, grinning, shifting to keep him in frame. In the far background, two aisles
away, Cass stands alone reading a small placard on a machine, not watching. Camera: slow
lateral dolly right, eye level. Audio: pumping chiptune dance track from the DDR
cabinet, arcade ambience, Milo laughing; Deshawn calls out happily "Bro reads the safety
warnings on the skee-ball!" [GLOBAL NEGATIVE BLOCK.]
**Refs:** start frame (retake: DDR pad must be attached to its cabinet), deshawn, milo.

### 1.2 — MED: the placard (8s)
**VO:** "Cass — seventeen, and carrying it like a sentence he'd been handed — was
reading the maintenance placard on a machine two aisles over. The way you read a thing
when you want an excuse to be standing somewhere."
**Prompt:** Medium shot. [WARDROBE LOCKS.] Cass stands very still in the neon-lit aisle
reading a small yellow maintenance placard taped to a machine, eyes moving down the
text, face quiet and intent. At the 4-second mark Milo leans into frame over his
shoulder from behind, pushes his glasses up, reads the placard, and his face lights up
with delighted mischief; he says, announcing it like a ring announcer: "The Deep End.
They put the Deep End back." Cass doesn't look at him. Camera: slow push-in from
three-quarter angle. Audio: muffled arcade noise, the DDR track distant, Milo's line
clear and close. [GLOBAL NEGATIVE BLOCK.]

### 1.3 — TRACKING: the approach (8s)
**VO:** "There is a specific fear a broken ride produces — not fear of the ride, which
is rated and survivable, but fear of the broken. And the three of them walked toward it
the way boys walk toward exactly this fear."
**Prompt:** Camera pulls back smoothly ahead of the three boys as they walk fast down
the arcade aisle toward the lens, normal speed, jostling — Deshawn shoves Cass's
shoulder, Cass shoves back without smiling, Milo skips a step to keep up, all three
grinning except Cass who is half-grinning despite himself. The spotless arcade glows
around them. Dialogue as they walk — Cass, flat: "It's off. It says it's off." Deshawn,
delighted: "It says *temporarily*." Audio: their footsteps and voices close, arcade
noise receding, a low ominous electronic hum slowly rising underneath. [WARDROBE LOCKS.
GLOBAL NEGATIVE BLOCK.]

### 1.4 — CU: the rules (6s)
**VO:** "Full-immersion life simulator. One credit — one subjective year. You will not
remember the outside while inside. You will remember everything when you leave."
**Prompt:** Slow steady push-in on the tooth-white machine's small screen glowing
green-on-black, the yellow OUT OF SERVICE tape across the credit slot below it. The
screen text stays perfectly legible and unchanged. At the last second the screen
flickers once, slightly. Audio: the arcade fades to near silence; one low electronic
hum; a single soft click. [GLOBAL NEGATIVE BLOCK — except the existing screen text and
tape, which must remain exactly as in the start image.]

### 1.5 — MED: Deshawn's five years (12s)
**VO:** "Deshawn's five years took about ninety seconds on the outside."
**Prompt:** [WARDROBE LOCKS.] Deshawn reclined in the tooth-white chair, headset over
his eyes. Performance in strict order: seconds 0–3, his hands twitch minutely on the
armrests and his mouth moves silently; seconds 3–5, he laughs out loud once at something
no one else can see; seconds 5–8, he tears the headset off, gulping air, eyes wet and
wide and delighted, sitting up all at once with fully natural motion; seconds 8–12, he
grabs Cass's forearm and babbles, breathless and joyful: "Sochi. Two golds. There was a
woman — there was a whole —" looking at his own hands like they belong to a stranger.
Cass and Milo lean in on either side of the chair, Milo filming, Cass wary. Camera:
locked medium shot, slight slow push. Audio: chair servos, his gasp, the dialogue clear.
[GLOBAL NEGATIVE BLOCK.]

### 1.6 — MED: the goading (8s)
**VO:** "Here is the thing they got right about Cass: he could be goaded. Because
underneath the placard-reading there was a boy who wanted, badly, to find out what was
down there — and who needed his friends to hand him the permission he wouldn't give
himself."
**Prompt:** [WARDROBE LOCKS.] Deshawn, still glowing from his run, points both index
fingers at Cass: "Cass has to." Milo, deadpan, arms crossed: "He has to." Beat. Cass
looks at the chair, looks at them, and sits down into it in one decisive motion, pulling
the headset down over his eyes, saying as he does: "Harder than his. I'm not doing
biathlon." Milo, already turning to the panel, grinning: "Way harder." Camera: medium
two-shot rotating slowly to follow Cass into the chair. Audio: dialogue close and
natural, arcade ambience low, the hum underneath. [GLOBAL NEGATIVE BLOCK.]

### 1.7 — CU: the toggle (8s)
**VO:** "Milo set the difficulty not one notch above Deshawn's, but as high as the
uncapped machine would go. And then — grinning, because he was seventeen, because it
would be so funny —"
**Prompt:** Extreme close-up on the open maintenance panel: Milo's finger slides a small
metal toggle labeled by position only (no readable text) from up to down with a hard
click; camera tilts up to Milo's face lit green by the panel, grinning the specific grin
of a boy doing something hilarious and terrible; off-screen Deshawn says, warm and
cheerful: "Have a good life." Then the machine's screen light blooms and floods the
whole frame to pure white over the final 2 seconds. Audio: the click; the line; a rising
clean electronic tone that cuts to silence at the white. [WARDROBE LOCKS. GLOBAL
NEGATIVE BLOCK.]

---

## Chapter II — Day Zero (keep 5, add 1, retouch prompts)

### 2.1 — CU: eye open (5s) — KEEP v1 clip
**VO:** "He was cold, and the cold was wrong. That was the first thing, before he had a
self to notice it with."

### 2.2 — MONTAGE: eleven days (8s) — RETAKE, plant the woman
**VO:** "The sim did what it was built to do. It seated a life. He was a boy of the
village, and he had always been a boy of the village. He lived eleven days like that."
**Prompt:** …as v1 (yoke, mud, wind, handheld) but add: in the background at the edge of
the village, unremarked, an old weathered woman in rags sits by a doorway talking softly
to the empty air; no one looks at her, Cass trudges past without a glance. [Refs: cass_17,
touched_woman. GLOBAL NEGATIVE BLOCK.]

### 2.3 — MED: first death (8s) — KEEP v1 clip
**VO:** "On the eleventh day he drank from the near stream, which was clean, which
everyone knew was clean. And the gripe took him — the thirst no water answered — and he
died on the packed earth that had been the first cold thing he ever felt."

### 2.4 — NEW — THE REMEMBERING (12s)
**VO:** "And woke up. On the packed earth. Day Zero. With — this time — all of it.
Remembering isn't like being told. It's the arcade slamming home into a body eleven days
from dying of something a spoon of salt could have fixed."
**Prompt:** Dark hut interior, dawn. Cass (17, gaunt, dirty) lies on packed earth
exactly as in the waking shot; his eye snaps open; two seconds of stillness — then his
whole body convulses upright in one terrified motion and he claws at his own face and
temples with both hands, searching for a headset that is not there, fingers dragging
down his cheeks, hyperventilating; he screams, raw, voice breaking: "Milo! Turn it off!
Turn it OFF! I want OUT!" — and his village mother rushes in from the doorway, drops to
her knees, and wraps him against her chest exactly the way a mother holds a fevered
child, one hand smoothing his hair, and he fights her for one second and then collapses
into her, sobbing, fists in her dress. Camera: handheld, close, urgent. Audio: his
ragged breathing and scream, her murmured soothing in a strange language, wind under the
door. [Refs: cass_17. GLOBAL NEGATIVE BLOCK.]

### 2.5 — the reset loop (8s) — KEEP v1 clip
**VO:** "If dying reset the day, maybe dying was the exit. It wasn't despair. It was
debugging. There was no counter. There was no 'lives remaining.' There was only Day
Zero, patient as a wall."

### 2.6 — the touched woman (8s) — KEEP v1 clip (it's one of the best)
**VO (before her line):** "There was a woman at the edge of the village whom everyone
called touched, who talked to the air. And on maybe his fortieth Day Zero, Cass went to
her and said the true thing."
**VO (after):** "And she went back to talking to the air, and never said a true thing
again. Forty summers. That was the gate. The only way out of the game was to play it."

---

## Chapter III — Bronze (keep 5, add 1, retake 1)

### 3.1 — salt water (8s) — RETAKE with dialogue tying it to the cure
**VO:** "He knew the whole shape of the tech tree — knew that a spoon of salt and a
pinch of sweetness in clean water would hold a dying child in the world long enough to
recover."
**Prompt:** …as v1, plus: as he spoons the water he murmurs, half to the mother, half to
himself: "Salt. Honey. Clean water. Keep giving it — however fast it runs through her."
The mother watches his mouth like the words are a spell. [GLOBAL NEGATIVE BLOCK.]

### 3.2 — bronze pour → rise (8s) — KEEP v1 clip
**VO:** "That was the drug, and he'd found it in his first dose: the world listens to
me. He gave them the tin ratio. A deeper plow. And Cass — nineteen, then twenty-two,
then twenty-five, rising on a column of grain and clean water and listened-to words —
became, without ever quite deciding to, a king."

### 3.3 — NEW — THE GOOD YEARS (12s)
**VO:** "It is a very good feeling to be a bronze-age king when you have a
twenty-first-century head and you think the whole thing is a ride you're about to step
off. He spent like a man who knew the money was fake."
**Prompt:** Firelit great hall, feast in full roar. Cass (late 20s, bearded, bronze
circlet, half-cloak thrown back, wine cup in hand) is LAUGHING — genuinely, head back,
delighted. Performance beats: he slaps a chieftain's shoulder mid-joke; he leans over a
game board of holes and pebbles and makes a move that makes three warriors groan and
shove each other; his young queen, a potter's daughter with clever hands, says something
in his ear and he laughs again, harder, wiping an eye; he tosses a drumstick to a dog.
Everything about him is loose, golden, wildly alive — a man having the time of several
lives. Camera: slow float through the feast toward him, warm firelight. Audio: drums and
pipes, roaring laughter, pebbles clacking, his big open laugh above it. [Refs: cass_28.
GLOBAL NEGATIVE BLOCK.]

### 3.4 — water greeting (10s) — KEEP v1 clip; gesture defined
**VO:** "They heard a boy raving about invisible demons — so he stopped telling the
truth and started telling a story: the water spirits are offended by water that has not
been greeted. He did it to trick them. A shortcut past an argument he was tired of
having. He had no idea he'd just done the single most durable thing of his entire reign."
(Any retake of this shot must use THE GESTURE block verbatim.)

### 3.5 — bored king (8s) — KEEP v1 clip
**VO:** "He grew tired of it the way Deshawn had gotten bored of his gold medals. Been
there. Ruled that. The throne a chore by thirty-five, and a cage by the last of it."

### 3.6 — the nod (6s) — KEEP v1 (retaken) clip
**VO:** "He reached forty — the door, the gate he'd structured an entire life around
walking toward. And the touched woman, a slave in this life too, she was in every life,
caught his eye and nodded, once. And Cass braced for the chair, for Deshawn's hands, for
the bright clean arcade evening —"

### 3.7 — roman wake (8s) — KEEP v1 clip
**VO:** "— and came back on a raised bed, under a latticed window, with a fountain
running somewhere below. Not the arcade. Not 2044. Not the chair. *Go on,* she had said.
Not *go home.* He'd misread the one instruction the machine had ever given him plainly —
and he'd built a whole life on the misreading."

---

## Chapter IV — Roman (keep 6, add 1, retake 1)

### 4.1 — aqueduct (8s) — KEEP v1 clip
**VO:** "A thousand years. He did the arithmetic and had to sit down. Every era fed the
next: the world he woke into was built on the foundations of the one he'd left — and he
had poured the minimum, and now he had to live on top of the minimum."

### 4.2 — fountain gesture (10s) — RETAKE with THE GESTURE verbatim
**VO:** "He knew the gesture. He'd *invented* the gesture. Worn down by a thousand
years, carried on the backs of grandmothers. She didn't even boil the water anymore; the
meaning had rubbed off and only the gesture was left. It saved no one now. And it was
his — the last living trace of an entire lifetime."
**Prompt:** …as v1, but the woman performs [THE GESTURE block verbatim] over the jar,
and pass the Bronze clip as a motion reference: `--video outputs/video/3_3_water_greeting.mp4`.

### 4.3 — the obituary scroll (6s) — KEEP v1 clip
**VO:** "He read his own obituary in a stranger's parlor: a clever-fool king who raised
the dead with clean water and went to the gods in a single night. Four lines. One of
them an insult. He laughed — because the alternative was the other thing."

### 4.4 — workshop (8s) — KEEP v1 clip
**VO:** "This time he did not become a king. He became a workshop owner — useful enough
to be wealthy, boring enough to live. He built water first, because water is free power.
Then he geared the wheel to bellows, and the bellows to a furnace — and heat is the gate
all of chemistry waits behind."

### 4.5 — vitriol (8s) — KEEP v1 clip
**VO:** "He made acid — the first strong acid in the world made on purpose by a man who
knew what it was for. He offered it free to a city, and got exactly one taker in ten
years: a grave young apothecary who liked that it cleaned wounds. But the apothecary
wrote things down. Cass called it the consolation prize. He was wrong about that in
exactly the way he'd been wrong before — and he wouldn't find out for three hundred years."

### 4.6 — Faustus (10s) — KEEP v1 clip
**VO:** "You cannot study a person that closely without coming to love them. Faustus
confided one night about a dead son, grieving it fresh and particular and years old at
once — and Cass understood in his chest what he'd been trying to prove with his head:
they were all as real as grief gets. He never again treated a real thing as a variable."

### 4.7 — NEW — THE ICE CREAM EXPERIMENT (10s)
**VO:** "He wanted, on a killing-hot afternoon, something cold and sweet. He knew the
one counter­intuitive thing the age did not: salt on ice makes it *colder*. Nobody in the
world knew that but him — and even he knew it as a fact without a number. So he got the
number the way he got everything now."
**Prompt:** Roman workshop bench in hard afternoon light. A row of six clay jars, each
packed with snow, a bronze scoop of grey salt beside them. Cass (mid-40s, sweating,
sleeves rolled) works the row with total focus: pours a measured scoop of salt into a
jar, stirs, nests a thimble-sized cup of cream into the slush, moves to the next jar
with more salt; frost blooms visibly on the outside of the middle jars; he lifts one
thimble, tips it — still liquid, he scowls — lifts the next, turns it upside down and
the cream holds solid, and his face breaks into slow astonished triumph; he laughs once,
alone, the laugh of a man who has just beaten the universe at cards, and reaches for a
larger bronze pot of cream. Camera: start close on the frosting jar, pull to a medium as
he works. Audio: scrape of the scoop, crunch of salted snow, cicadas outside, his
single delighted laugh. [Refs: cass_45. GLOBAL NEGATIVE BLOCK.]

### 4.8 — the bath (10s) — KEEP v1 clip
**VO:** "He ate the first bowl in the bath. The fire outside and the frost in the bowl —
and Cass, who had been a king, and a boy dead of dirty water, and a man who'd
back-chained from a bath all the way to despair, sat in the hot and ate the cold and
thought, with his whole chest: *I have made it.* And the only thing wrong with the
moment was that the person he wanted to hand the second bowl to was a glassblower named
Faustus — and wanting to share it was the first crack in the wall between Cass and the
idea that the people in here were real."

---

## What this costs

| Work | Shots | Seconds | Credits (480p std, 3/s) |
|---|---|---|---|
| Chapter I rebuild | 8 | 68 | ~204 |
| Ch II: new remembering + 2.2 retake | 2 | 20 | ~60 |
| Ch III: good-years + 3.1 retake | 2 | 20 | ~60 |
| Ch IV: ice-cream + 4.2 retake | 2 | 20 | ~60 |
| New start frames (nano banana) | ~8 | — | ~8 |
| **Total v2 patch** | | | **~390** |

Everything else from v1 is kept. Current balance: **35.25** — the patch needs a credit
top-up (or the monthly refresh) before it can run.

## On total runtime

Ch I–IV v2 lands at ~4.5 min of picture; with Chapters V–VIII done the same way the film
is ~9–10 min. The story reads in 20–30 min, so a faithful-feeling adaptation probably
wants **15–20 min** (~2.5–3 min per era — roughly double the current shot counts, plus
15s clips instead of 8s where scenes breathe). At 480p std that's very roughly
2,700–3,600 credits for a full-length draft. The narration script is the thing to lock
first — it dictates pacing, and it's free.

## Post pipeline (free)

1. Lock narration text (this file) → generate/record VO.
2. Cut clips to the VO with ffmpeg, trimming clip heads/tails to breathe.
3. Duck clip audio under narration; keep dialogue clips at full level.
4. White-out transitions between eras (2-frame white holds already baked into several clips).
