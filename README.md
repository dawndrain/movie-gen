# movie-gen — AI filmmaking with Higgsfield

A working pipeline for making short films (5–12 minutes, dozens of shots,
consistent characters and voices) with Seedance 2.0 (video), Nano Banana Pro
(images), Sonilo (music) — all three via Higgsfield's CLI — plus ElevenLabs
(voices), Gemini (audio/image QC), and a lot of ffmpeg. About ten films have
been made this way; the first complete one, **The Long Game** (an 11-minute
comedy, ~80 shots, 18 iteration passes), lives in `long_game/` as the worked
example.

A taste of the output: [The Long Game's cast, voices, and start frames](docs/long_game/index.html) (open locally, or via Pages once public) — and [the finished film](https://www.youtube.com/watch?v=q40M08SOhGs).
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

Prerequisites: Python 3.10+, `ffmpeg`/`ffprobe` on PATH, Node 18+ for the
Higgsfield CLI (`npm i -g @higgsfield/cli` — the only path to Seedance 2.0 /
Nano Banana Pro), and `pip install numpy` (pitch_check). Optional per tool:
`edge-tts` (free draft TTS), `demucs` + Whisper (dub QC).

1. `npm i -g @higgsfield/cli`, then `higgsfield auth login` &&
   `higgsfield workspace set <id>`; put API keys at `~/.elevenlabs_key` and
   `~/.gemini_key` (`~/.fal_key` only if using fal.ai as an alternate
   Seedance provider).
2. Make a folder, write the treatment, then follow the pipeline order in
   MOVIE_LESSONS.md — anchors, frames, voices, **animatic first**.
3. Copy what you need from `tools/templates/` and adapt its spec imports.
4. Generate clips via a batch script + `python3 ../tools/pool_run.py
   videos_v1.sh outputs/video1 7`, assemble with `python3 ../tools/assemble.py
   film_spec.py`, review via the storyboard, iterate.

Media (clips, frames, audio, previews) is deliberately not in git — only
specs, scripts, and docs. Everything under `outputs/` is regenerable from
them, credits permitting.
