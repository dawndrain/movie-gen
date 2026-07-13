# v1 morning notes for Dawn

**Watch:** `carl/outputs/animatic_v1.mp4` (10.6 min, 36 shots)
**Review:** `carl/storyboard.html` (every shot + dialogue + prompt + playable segment)
**Re-cast:** `carl/auditions.html` (2–3 candidates per character; provisional picks tagged)

## Provisional cast (all re-castable — only changed lines re-bill)

- CARL — Branok (raspy US); Gemini: "a tired person processing a horrific mistake"
- DONUT — Lily (velvety UK); Gemini: "monologue from a stage play"
- THE AI — IanAlien (modulated); Gemini: "GLaDOS mixed with a carnival barker"
- MORDECAI — Bill · ODETTE — KristenQueen · ZEV — Cooper (anxious)
- MAESTRO — DarthOxley · BRANDON — Chris · ELLE — Matilda
- AGATHA — Nana Margaret · MAGGIE — Merv · JUICER — DarthOxley · LI JUN — Kai

## Known nits (all cheap fixes; none blocked v1)

1. **Maestro's stage sign** invented its own show name ("ORC LORD'S DILEMMA")
   in the anchor and it bled into c8. Could re-text via targeted edit to
   "DEATH WATCH" if you care.
2. **c7b banner** ("LEVEL 93 DEFEATED") is partially veiled by smoke — legible
   but not crisp.
3. **a15** stages Carl's chopper escape *inside* the diner rather than through
   the doorway — reads as comedy, kept it.
4. **Mordecai's Bugaboo form** (c5) reads more "bear cub with owl eyes" than
   canonical Bugaboo — flag if it bothers you.
5. Runtime is 10.6 min vs the ~7 estimated — TTS runs long. Easy trims: AI
   announcements (a2, c1) and the Odette/Maestro scenes have the most air.

## To iterate

- Reword a line / re-cast a voice → edit `spec.py` LINES / CAST, delete the
  affected `vo/<shot>_*.mp3` (only if re-wording; re-casting needs delete too),
  then `python3 make_animatic.py all v2`.
- Fix a frame → edit its prompt in `spec.py`, delete `frames/<shot>.png`,
  `python3 make_images.py frames`, delete its `outputs/animatic_segs/NN_<shot>.mp4`,
  re-run `make_animatic.py mix v2`.
- Everything skips existing files, so re-runs only touch what you changed.

Spent ~760 credits (images 2k + 8 music cues); 1,685 remain this cycle.
All dialogue is original paraphrase — nothing quoted from the novel.
