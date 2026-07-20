# The Long Game

An ~11-minute AI-generated comedy — the first complete film made with this
pipeline, and the repo's worked example. A teenager gets cocky at a mysterious
arcade machine ("THE LONG GAME — one credit, one life"), picks maximum
difficulty, and has to live an entire life — bronze age to 1926 — to get back
to the exit. It took about 15 iteration passes over about a week — the film
was broadly in shape by v12, the YouTube upload is roughly v15, and the
archive holds 18 rounds counting the experiments past the uploaded cut.

**Watch it:** https://www.youtube.com/watch?v=q40M08SOhGs

**Browse it:** [cast & voices](../docs/long_game/index.html) ·
[full storyboard with per-shot audio](../docs/long_game/storyboard.html) ·
[voice auditions](../docs/long_game/auditions.html)

## What's here

- `the_long_game.md` — Dawn's original short story
- `film_spec.py` — the entire final cut as data: 79 cuts, 9 music spans,
  ambience beds, grades, fades. `python3 ../tools/assemble.py film_spec.py`
  rebuilds the film from the (gitignored) clips.
- `storyboard_gen.py` — generates the per-shot review page used every round
- `vo_gen.py` — TTS/voice utilities from the voice-consistency wars
- `archive/` — all 18 rounds of iterative assemblers, batch scripts, and
  storyboards, plus the production TODO log. The full history, kept honest.

Caveat for imitators: this film predates two big workflow upgrades — animatic-
first production and prompted ElevenLabs voice design (it was cast from catalog
voices and take-cloning instead). See MOVIE_LESSONS.md for the current
pipeline; the auditions page linked above retrofits the modern casting format
onto this cast as a demonstration.
