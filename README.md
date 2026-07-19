# videogen — AI filmmaking with Higgsfield

A working pipeline for making short films (5–12 minutes, dozens of shots,
consistent characters and voices) with Seedance 2.0, Nano Banana Pro, Sonilo,
ElevenLabs, and a lot of ffmpeg. About ten films have been made this way; the
first complete one, **The Long Game** (an 11-minute comedy, ~80 shots, 18
iteration passes), lives in `long_game/` as the worked example.

A taste of the output: [The Long Game's cast, voices, and start frames](docs/long_game/index.html) (open locally, or via Pages once public) — and [the finished film](https://www.youtube.com/watch?v=q40M08SOhGs).

**Start with [MOVIE_LESSONS.md](MOVIE_LESSONS.md)** — the distilled playbook:
the pipeline, the laws (retakes regress; after two failed rewordings change
what happens; targeted edits beat re-rolls), prompting, voices, sound, and
costs. The unabridged version with per-project war stories is
[MOVIE_LESSONS_FULL.md](MOVIE_LESSONS_FULL.md).

## The pipeline in one breath

Anchors (character portraits) → start frames (one per scene, anchors as refs)
→ cast voices and TTS the script → **animatic** (the whole film as stills +
TTS, ~free — iterate here) → Seedance clips (start frame + anchors + voice
refs) → music and ambience as assembler layers → ffmpeg assembly →
storyboard.html + preview → director notes → cheapest fix per note → repeat.

## Repo map

```
gen.py            submit Seedance / Nano Banana jobs (handles the 8-job cap)
pool_run.py       batch runner; skips finished shots, so re-run = retry
dub_clip.py       replace a line's audio without re-rendering
pitch_check.py    median-F0 screen for wrong-voice takes
listen.py         Gemini listens to audio and gives QC verdicts
tools/
  assemble.py     spec-driven film assembler (cuts, music spans, ambience
                  beds, grades, fades) — see long_game/film_spec.py
  templates/      best-of-breed per-film tools to copy into a new project:
                  animatic, auditions, ambience, images, storyboard, batch
                  emitter, targeted frame edits, upscale, dub pass
long_game/        the worked example: story, film_spec.py, storyboard_gen,
                  archive/ of every iteration script (media is gitignored)
other_movies/     the other film projects (sagas, Donner Party, Walter's Deal,
                  the Homo Sapien music video, ...). Copyrighted source texts
                  and a few fan-IP projects are local-only via .gitignore.
veo3_compare/     the std-vs-fast blind test harness + prompts
```

## Quickstart for a new film

1. `higgsfield auth login` && `higgsfield workspace set <id>`; put API keys at
   `~/.elevenlabs_key`, `~/.gemini_key`.
2. Make a folder, write the treatment, then follow the pipeline order in
   MOVIE_LESSONS.md — anchors, frames, voices, **animatic first**.
3. Copy what you need from `tools/templates/` and adapt its spec imports.
4. Generate clips via a batch script + `python3 ../pool_run.py videos_v1.sh
   outputs/video1 7`, assemble with `python3 ../tools/assemble.py
   film_spec.py`, review via the storyboard, iterate.

Media (clips, frames, audio, previews) is deliberately not in git — only
specs, scripts, and docs. Everything under `outputs/` is regenerable from
them, credits permitting.
