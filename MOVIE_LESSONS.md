# Making movies with Higgsfield

What we've learned from making about ten films with Seedance 2.0, Nano Banana
Pro, Sonilo, and ElevenLabs. This is the readable version; the complete archive
— per-project war stories, API recipes, every detail — lives in
MOVIE_LESSONS_FULL.md. New project addenda go in the full doc, and anything
that turns out to generalize gets promoted to a line or two here.

## How a film gets made

Work in this order, and don't skip ahead to video.

Start with **anchors**: one Nano Banana portrait per recurring character, one
per age or era if they change, plus plates for the main locations. Characters
who appear in a single scene don't need anchors — just describe them in their
one frame. Then build **start frames**, one per scene, passing the anchors as
image references. The start frame matters more than the prompt: wardrobe, set
dressing, and any on-screen text mostly come from it, so problems in the frame
become problems in every clip shot from it.

**Cast the voices before you shoot anything.** Generate custom voices by
*prompting* ElevenLabs (voice design) rather than browsing its catalog — the
stock and searchable voices skew podcaster-generic, and the characterful ones
veer cartoonish (one candidate was inexplicably a pirate). Describe the voice
you want for each character, audition the results on an HTML page that shows
the character's face next to the audio players, and let the director pick; one
"base" read per candidate is enough — calm/drama delivery variants never
changed a casting decision. Then TTS the entire script. Retrofitting voices
with dubs after the clips existed was the single biggest time sink of the
first film.

With frames and voices in hand, cut an **animatic**: every start frame held for
its exact cut window, the TTS dialogue laid over the top, scratch music and
ambience underneath. It costs essentially nothing and builds in about two
minutes, which means script, pacing, and casting problems — the things
directors actually give notes on, round after round — get fixed while every
shot is still free to change. Two technical notes: hold each still from its own
in-point to the *next* shot's in-point, because a concat list has no timeline
and any gap silently collapses; and if you want a Ken Burns push-in, use the
`perspective` filter rather than `zoompan` — zoompan rounds its crop origin to
whole pixels and visibly quivers at slow speeds, while perspective takes
fractional corners and moves smoothly. Getting this right was fiddly; copy
`kenburns_vf()` from `tools/templates/make_animatic.py` instead of rederiving
it. Shots that are about stillness should just be locked off.

Only then generate **clips** with Seedance, giving each shot its start frame,
its anchors, and its voice references. Use **fast mode at 720p and below** — a
20-pair blind test settled this (Dawn picked fast in 13 of 18 decisive pairs,
including close-up faces, where the worst identity glitches were actually std
takes; the earlier "fast is unusable" verdict traced back to bad prompting,
not the mode). One roll per shot by default — per-take seed luck matters more
than mode, so re-roll individual shots that fail QC rather than paying double
up front. Std is still required for shots with multiple `--audio` references and
for output above 720p. Either mode takes about three to five minutes per clip;
if clips are taking half an hour, you're not slow, you're contended — another
project is eating the workspace's eight-job cap.

Music and ambience are **assembler layers, never baked into clips**. The
assembler itself is a small Python script that builds one ffmpeg filtergraph
from a list of cuts — each entry names a clip, its trim, and optional mute and
music marks — and a full re-encode takes about ten minutes. Review happens
against two artifacts: the preview mp4 and a generated storyboard.html showing
every shot in order with its playable clip, dialogue, and prompt. The director
leaves per-shot notes, each note gets the cheapest fix that addresses it, and
the version number gets bumped — never overwrite a preview the director might
still be watching.

## The laws

**Retakes regress randomly.** A retake reliably fixes the flaw you noted and
then breaks something you didn't — a voice, a face, the camera, extras
wandering in. If a take is 95% there, dub it, trim it, or live with it; a
slightly awkward dub of a good take usually beats a native retake. Keep every
old take on disk in versioned output folders, so any revert is a one-line edit.

**After two failed rewordings, change what happens.** Persistent failures —
content flags, stagings the model can't hold — are almost never fixed by a
third phrasing. Restage the event, or move it off-screen.

Every fix has a price — an assembler trim is free, a dub is a third of a
credit, a regenerated frame a few credits, a retake 24–36 — but they aren't
interchangeable: the problem dictates the fix. The discipline is just to check,
before reaching for a retake, whether the note is really a trim, dub, or mix
problem in disguise, and never to promise yourself "just one more retake
round".

## Writing clip prompts

A good clip prompt is the action in ordered beats, dialogue written verbatim in
quotes, and three lock blocks that ride along on every prompt in the scene:

The **wardrobe lock** describes everyone in the shot head to toe, plus the set,
restated word for word in every prompt of the scene — not just the first. Keep
a face-only variant too, because a lock ending in "wearing an orange cardigan"
quietly wins the argument against "in a wedding dress" later in the sentence.

The **voice lock** pins accent and delivery in words ("measured, dry British —
never American, never theatrical") on top of the `--audio` reference, and
always includes "there is no narrator and no voiceover; only characters visible
on screen speak, lips moving" — otherwise clips occasionally grow spontaneous
narration.

The **negative block** covers the usual suspects: photorealistic, natural
motion, no slow motion, no text or captions, characters keep exactly the
reference faces and clothes, each character appears exactly once. For dialogue
scenes, add that the location is otherwise completely empty — crowd creep is
real, extra onlookers materialize in regenerated scenes, and cleaning them out
of the start frame isn't enough; the ban has to be in the video prompt.

Beyond the locks: describe behavior rather than emotion ("both are laughing",
not "cheerfully") because mood words lose to the model's default stern face;
give any directional composition an explicit axis ("oldest on the left");
say "locked-off static camera" unless you want the default drifty push-in.
On-screen text always comes from the frame ("the text stays exactly as in the
start image") — asking Seedance to invent legible text gets garble. If a shot
comes back off-model, check whether that character's anchor was actually passed
before blaming the model; and don't include a character's lock text in shots
they aren't in, or the model will summon them.

## Voices, dubbing, and QC

Voice samples live in `anchors/voice/`, one per character *per register* — a
character who sounds different inside the game, or at another age, needs a
sample per context, because a reference sliced from the wrong context shifts
the whole scene's accent. Screen every sample with pitch_check.py before
trusting it; a bad reference faithfully reproduces the bad voice.

Know that one `--audio` reference gets applied to every speaker in the shot —
Seedance doesn't map voices to characters. For multi-speaker shots, either
concatenate the TTS lines into one mp3 and say "the first line is spoken by X,
the second by Y", or go reference-less and fix voices in the dub pass.

Dubbing itself only works when the lips aren't visible: off-screen lines,
telepathy, recordings, mouthless creatures. Even speech-to-speech conversion
that preserves timing exactly still reads as off-sync on a visible mouth, so
on-camera dialogue has to be re-rendered with the right voice reference
instead. For surgical fixes there's a reliable recipe: TTS the whole sentence
(for natural prosody), crop out just the phrase you need using Whisper word
timestamps, tempo-fit and volume-match it, and lay it over the demucs
instrumental stem. Whisper-transcribe every dialogue clip against the script
as QC — screams and short trailing commands are what drop most often, and
they're better fixed by overlaying the TTS line than by re-rolling the clip.

## Music, ambience, and the mixing rule

Score scenes, not eras: short cues on specific moments, silence under comedy
dialogue, and a recurring motif at matching beats reads as intentional
scoring. Sonilo runs about 3.75 credits a minute; always append "instrumental
only, no vocals".

Ambience is what glues cuts into scenes: one steady bed per location, living
in the assembler. Generate beds with ElevenLabs sound-generation as 22-second
loops, asking for pure texture ("steady seamless loop, no sudden events") and
naming what you *don't* want — grassland prompts default to crickets. Then EQ
them (high-pass 100 Hz, low-pass 7 kHz, which also removes ElevenLabs' baked-in
high-frequency whine), crossfade-stitch to five minutes, and normalize.

The mixing rule that prevents every "the music is overpowering" round: set all
levels in LUFS, never in mean volume — spiky sounds like crickets read quiet on
an amplitude meter but loud to the ear. Normalize every stem to a common
-30 LUFS, measure the film's dialogue loudness once with ebur128, and then
every bed and cue is a simple dB offset below that anchor (ambience sits 12–16
dB under). And since none of us here have ears, `listen.py` sends any audio to
Gemini — but only ever ask it to FIND FAULTS or compare A vs B, never to rate
quality. Prompted adversarially it catches whines, wrong-content beds, and
"this sounds like tinnitus" that no meter shows; asked "is this good?" it
calls everything flawless, including a voice that was literally inaudible.
And even its fault reports pattern-complete: it found one real whine (spectrum-
verified, +18 dB narrowband spike) then claimed the same whine in beds that
measure clean. Treat its findings as leads — confirm with an FFT/ebur128
measurement before mass-applying a fix. Audibility and level questions are
measurements, not listening questions.

## Batches and money

The workspace allows eight concurrent Seedance jobs, shared across every
session and terminal; gen.py enforces this with a slot-file semaphore (set
`SEEDANCE_SLOTS=4` if you're also submitting outside gen.py). Nano Banana and
Sonilo aren't capped the same way. Run batches through pool_run.py — it skips
shots whose output already exists, so re-running the same command is the retry
pass. Generate the batch script from the same shot table the storyboard uses
so the two can't drift, and run `caffeinate -is` during long waits.

A client-side failure is not a job failure: `--wait` can drop while the job
finishes server-side and bills anyway, so check `higgsfield generate list
--json` before resubmitting — completed jobs download free from their
result_url. And when a whole tail of a batch suddenly fails, check
`higgsfield account status` before debugging anything; it's usually just
credits running out mid-batch.

Money, roughly: an 8-second clip is about 12 credits in fast, 24 in std; a
complete 11-minute film is around 2,000 credits of video; a 15-shot retake
round is about 400; frames and music are noise by comparison. Subscription
credits expire at the end of each cycle, so spend leftovers deliberately.
Clips cap at 15 seconds — size dialogue shots from their TTS audio (total
audio + 2.5s + 0.8s per speaker) and split any shot or line that exceeds the
cap before generating.

**`generate cost` is UNRELIABLE — always confirm with `account status` before
and after ONE real job.** It quoted 0.1 credits for `bytedance_video_upscale`;
the true price was ~37 cr/clip (~5 cr/s — *more* than generating the clip). Ten
clips silently burned 374 credits before the discrepancy showed up in the
balance. For any unfamiliar job type, run one, diff the balance, then decide.

**Don't AI-upscale for a "1080p" upload — it's the wrong tool twice over.** (a)
It's expensive (see above). (b) It can't fix anything: a glitchy patch of a face
just comes back bigger, and using it on only some shots reads as inconsistent
sharpness. What you actually want is the **resolution trick**: YouTube picks its
bitrate ladder from the UPLOAD RESOLUTION, not the real detail. Encode the
finished film at **1440p or higher** (`scale=...:flags=lanczos` + a light
`unsharp`, from the native 480p clips) and YouTube serves it with VP9/AV1 at a
far higher bitrate than a true-480p upload gets on the stingy H.264 ladder — so
the SAME source looks cleaner. Free, uniform, no per-clip jobs. Make the master
FILE itself high-bitrate (CRF ~16 + fat maxrate) or YT sees low-bitrate 1440p and
throttles anyway. Held stills sourced from 2k PNGs are natively sharp at 1440p.

## Content filters

An occasional false-positive nsfw flag is normal: reword once or twice, and if
it persists, change the staging — the filter reads prose, and it has objected
to confinement-before-a-crowd staging and to intimacy adjectives applied to
literal planets. Some words ("slave") reject instantly. Flags can also come
from the input image rather than the prompt: front-facing famous IP characters
in a start frame fail instantly, bare-skinned figures from behind read as
nudity, and a byte-identical file re-uploaded across many failed submissions
starts getting auto-rejected (re-encode it to change the hash). Anchor
references and the output video itself are not checked.

## Setup

Auth is browser OAuth (`higgsfield auth login`) followed by
`higgsfield workspace set <id>` — without the workspace step nothing works.
The npm CLI is the only path to Seedance 2.0 and Nano Banana Pro. API keys
live at `~/.elevenlabs_key`, `~/.gemini_key`, and `~/.fal_key`. Shared tools
sit at the repo root (gen.py, pool_run.py, dub_clip.py, pitch_check.py,
listen.py); each film is its own subfolder, and `long_game/` is the template
worth copying. The repo (github.com/dawndrain/movie-gen, private) excludes
media and any project adapting a copyrighted source — add such projects to
.gitignore BEFORE committing. Everything else is in MOVIE_LESSONS_FULL.md.
