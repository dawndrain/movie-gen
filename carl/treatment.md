# DUNGEON CRAWLER CARL — Book One animatic

Condensed original adaptation of Matt Dinniman's *Dungeon Crawler Carl* (book 1,
Floors 1–2). All dialogue is original paraphrase written for this animatic —
none of it is quoted from the novel (short famous catchphrases excepted).
Fan project for Dawn.

## Shape

35 segments, ~6–7 minutes. Three movements:

- **A (Floor 1):** the Collapse → tutorial → Donut's ascension → the Hoarder →
  the goblin war and its cost (War Criminal is the tonal thesis: the UI stays
  chipper while Carl breaks).
- **B (Meadow Lark / floor 1 end):** found family → the Juicer → the Speedbump
  vs. the Ball of Swine → Odette.
- **C (Floor 2):** timer slashed → Jug O'Boom → Krakaren (Donut drags Carl from
  the fire — emotional core, locked-off shot) → Yolanda's death → the Bomb
  Chicken chase (spectacle climax) → spiting Maestro → Mongo → the stairs down.

## Tone rules (from the research brief)

- Comedy and horror in the SAME beat, not alternating. Candy-colored game UI
  (gold achievement banners, blue holo text) superimposed on grim spaces.
- The AI is the laugh track from hell; Carl's deadpan is the stabilizer;
  Donut's oblivious diva glamour is the engine.
- Play scenes absurd at full commitment, then hold one beat too long on the
  cost (a14 workshop, c6 Yolanda — both locked off, scored with the same
  tragedy motif so it reads as intentional).

## Continuity locks

- Donut has NO crown before a8 (donut_plain anchor), crown from a8 on.
- Carl: pink Crocs a1–a3 only; barefoot from a4 forever. Cloak+trollskin shirt
  from a7; war gauntlet from b4 (looted at b3); glittery feet from c2.
- Mordecai is a rat-man on Floor 1 (a6), a Bugaboo on Floor 2 (c5).
- Agatha stands in an unnatural dark patch in b2 (cameras refuse her).
- The AI has no body — voice only, never a character in frame.

## Everything else

Single source of truth is `spec.py` (anchors, frames, dialogue, cut order,
music/ambience marks, cast). `make_images.py`, `make_auditions.py`,
`make_animatic.py`, `storyboard_build.py` all import it, so the storyboard and
the cut can't drift.
