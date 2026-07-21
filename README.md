# movie-gen — AI filmmaking with Higgsfield

A working pipeline for making short films (5–12 minutes, dozens of shots,
consistent characters and voices) with Seedance 2.0 (video), Nano Banana Pro
(images), Sonilo (music) — all three via Higgsfield's CLI — plus ElevenLabs
(voices), Gemini (audio/image QC), and a lot of ffmpeg. About ten films have
been made this way; the first complete one, **The Long Game** (an 11-minute
comedy, ~80 shots, ~15 iteration passes), lives in `long_game/` as the worked
example.

A taste of the output: [The Long Game's cast, voices, and start frames](https://dawndrain.github.io/movie-gen/long_game/), the [storyboard](https://dawndrain.github.io/movie-gen/long_game/storyboard.html), the [voice auditions](https://dawndrain.github.io/movie-gen/long_game/auditions.html) — and [the finished film](https://www.youtube.com/watch?v=q40M08SOhGs).
Two more finished films: [Homo Sapien](https://www.youtube.com/watch?v=QlP-dhZTQUE) (the music video) and [Walter's Deal](https://www.youtube.com/watch?v=pHtF_ApUjRo).
There's also a blog post about the whole endeavor: [Making AI Movies](https://dawndrain.notion.site/Making-AI-Movies-39cbb81dad798077b43adcd96e3ebe75).

**Start with [MOVIE_LESSONS.md](MOVIE_LESSONS.md)** — the playbook:
the pipeline, the laws (retakes regress; after two failed rewordings change
what happens; the problem dictates the fix), prompting, voices, sound, and
costs. The dated per-project postmortems behind those rules live in
[PROJECT_LOG.md](PROJECT_LOG.md).

## The pipeline in one breath

Anchors (character portraits) → start frames (one per scene, anchors as refs)
→ cast voices and TTS the script → **animatic** (the whole film as stills +
TTS, ~free — iterate here) → Seedance clips (start frame + anchors + voice
refs) → music and ambience as assembler layers → ffmpeg assembly →
storyboard.html + preview → director notes → cheapest fix per note → repeat.

## Repo map

```
gen.py            submit Seedance / Nano Banana jobs (handles the 8-job cap)
tools/
  pool_run.py     batch runner; skips finished shots, so re-run = retry
  assemble.py     spec-driven film assembler (cuts, music spans, ambience
                  beds, grades, fades) — see long_game/film_spec.py
  dub_clip.py     replace a line's audio without re-rendering
  pitch_check.py  median-F0 screen for wrong-voice takes
  listen.py       Gemini listens to audio for QC (fault-finding prompts only)
  templates/      best-of-breed per-film tools to copy into a new project:
                  animatic, auditions, ambience, images, storyboard, batch
                  emitter, frame edits, upscale, dub pass
long_game/        the worked example: story, film_spec.py, storyboard_gen,
                  archive/ of every iteration script (media is gitignored)
other_movies/     the other film projects (sagas, Donner Party, Walter's Deal,
                  the Homo Sapien music video, ...). Copyrighted source texts
                  and a few fan-IP projects are local-only via .gitignore.
veo3_compare/     the std-vs-fast blind test harness + prompts
```

## Quickstart for a new film

This repo is built to be driven by Claude Code, not by hand. Your part:

1. **Accounts.** A [Higgsfield](https://higgsfield.ai) account with credits
   (Seedance 2.0 and Nano Banana Pro run through their CLI) and an
   [ElevenLabs](https://elevenlabs.io) account for voices. Optional: a Gemini
   API key for automated audio/image QC.
2. **Run Claude Code** in the repo root. It reads the playbook
   (MOVIE_LESSONS.md) and asks what kind of movie you want to make.
3. **Answer, and stay in the director's chair.** Claude installs the tooling,
   scaffolds the project, and drives the pipeline; the only steps it hands
   back to you are the browser logins (`higgsfield auth login`) and pasting
   your API keys. From there your job is notes on the animatic and previews.

Media (clips, frames, audio, previews) is deliberately not in git — only
specs, scripts, and docs. Everything under `outputs/` is regenerable from
them, credits permitting.
