# Making movies with Higgsfield

What we've learned from making about ten films with Seedance 2.0, Nano Banana
Pro, Sonilo, and ElevenLabs. This is the playbook — deliberately the only one.
The dated per-project postmortems it was distilled from (war stories,
measurements, corrections) live in PROJECT_LOG.md; new lessons start there as
a dated entry and get promoted into a section here once they generalize.

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
first film. (Prompt-craft for designing the voices themselves is in the
Voices section below.)

With frames and voices in hand, cut an **animatic**: every start frame held for
its exact cut window, the TTS dialogue laid over the top, scratch music and
ambience underneath. It costs essentially nothing — a TTS line is ~0.3 credits
against ~24 for the clip it previews — and builds in about two minutes, which
means script, pacing, and casting problems — the things directors actually
give notes on, round after round — get fixed while every shot is still free to
change. Build it from the same shot table the assembler uses, so the animatic
and the final cut can never drift apart. Two technical notes: hold each still
from its own in-point to the *next* shot's in-point, because a concat list has
no timeline and any gap silently collapses; and if you want a Ken Burns
push-in, use the `perspective` filter rather than `zoompan` — zoompan rounds
its crop origin to whole pixels and visibly quivers at slow speeds, while
perspective takes fractional corners and moves smoothly. Getting this right
was fiddly; copy `kenburns_vf()` from `tools/templates/make_animatic.py`
instead of rederiving it. Shots that are about stillness should just be locked
off.

Only then generate **clips** with Seedance, giving each shot its start frame,
its anchors, and its voice references. Use **fast mode at 720p and below** — a
20-pair blind test settled this (Dawn picked fast in 13 of 18 decisive pairs,
including close-up faces, where the worst identity glitches were actually std
takes; the earlier "fast is unusable" verdict traced back to bad prompting,
not the mode). One roll per shot by default — per-take seed luck matters more
than mode, so re-roll individual shots that fail QC rather than paying double
up front. Std is still required for any shot with an `--audio` reference (fast+audio
jobs fail server-side with a bare "failed" status — even a single ref) and
for output above 720p. Either mode takes about three to five minutes per clip;
if clips are taking half an hour, you're not slow, you're contended — another
project is eating the workspace's eight-job cap.

Music and ambience are **assembler layers, never baked into clips**. The
assembler itself is a small Python script that builds one ffmpeg filtergraph
from a list of cuts — each entry names a clip, its trim, and optional mute and
music marks — and a full re-encode takes about ten minutes. Trims are creative
tools, not just cleanup: mid-clip splices for cutaways, tightening stilted
dialogue by cutting middle sentences, even repeating an identical two-second
beat as a running gag (repetition reads as deliberate comedy and costs
nothing). Find safe cut points with silencedetect
(`-af silencedetect=n=-32dB:d=0.35`) and cut in silences, never mid-word; bake
act transitions into the outgoing clip and hard-cut to the next act's opener.

Review happens against two artifacts: the preview mp4 and a generated
storyboard.html showing every shot in order with its playable clip, dialogue,
and prompt. Interpret the director's notes against the *clip*, not memory —
ffmpeg xstack contact sheets are the fastest way to spot-check gags and
continuity before the director sees them. The recurring note categories to
pre-empt: wardrobe anachronisms, duplicate background characters, inconsistent
voices, spontaneous camera moves, on-screen text garble, and sets that read
the wrong decade. Each note gets the cheapest fix that addresses it, and the
version number gets bumped — never overwrite a preview the director might
still be watching. On tone: comedy plays best dry (no score under jokes), and
sincerity is earned by concentrating it in one stretch of the film rather than
sprinkling it throughout.

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
narration. (Narration can still exist in the film — sparse, and mixed in at
assembly on the global timeline so lines bridge cuts — it just must never be
requested from Seedance.)

The **negative block** covers the usual suspects: photorealistic, natural
motion, no slow motion, no text or captions, characters keep exactly the
reference faces and clothes, each character appears exactly once. For dialogue
scenes, add that the location is otherwise completely empty — crowd creep is
real, extra onlookers materialize in regenerated scenes, and cleaning them out
of the start frame isn't enough; the ban has to be in the video prompt.

Beyond the locks: describe behavior rather than emotion ("both are laughing",
not "cheerfully") because mood words lose to the model's default stern face;
give any directional composition an explicit axis ("oldest on the left");
say "locked-off static camera" unless you want the default drifty push-in. To
repeat a signature gesture exactly, pass a previous clip with `--video` as a
motion reference. On-screen text always comes from the frame ("the text stays
exactly as in the start image") — asking Seedance to invent legible text gets
garble. Never use a real song's lyrics — copyright aside, the model can't
render them; invent a title and hook instead. If a shot comes back off-model,
check whether that character's anchor was actually passed before blaming the
model; and don't include a character's lock text in shots they aren't in, or
the model will summon them.

## Voices, dubbing, and QC

Voice samples live in `anchors/voice/`, one per character *per register* — a
character who sounds different inside the game, or at another age, needs a
sample per context, because a reference sliced from the wrong context shifts
the whole scene's accent. Screen every sample with pitch_check.py before
trusting it; a bad reference faithfully reproduces the bad voice.

Designing voices, every adjective in the prompt is taken **literally** —
"slightly breathless" produced an airy sing-song lilt, and "teenage boy +
playful" skewed childlike. Differentiate same-demographic characters by pitch
and tempo ("light quick tenor, faster than his friends"), not by adjectives,
or they converge. Always append "clean close-mic studio recording" or previews
come back lo-fi, and audition all three previews a prompt returns, not just
the first. Age words plus pitch words can trip the safety filter (it reads as
child-voice creation); age-neutral wording ("young man with a light tenor")
passes. Write the audition line naturally — a scripted ellipsis gets heard as
the *voice* hesitating and costs a good candidate the part. Pre-screen with
pitch stats but expect surprises: fictional-age logic beats timbre logic (a
147 Hz "villain" voice won a ten-year-old character over every deep
candidate).

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
instrumental stem. Dub candidates are cheap — generate several and A/B by ear:
a seed_audio clone (~0.3 credits) plus two or three ElevenLabs takes. Don't
assume the fancier tool wins; the cheap clone has beaten ElevenLabs
head-to-head. And know what speech-to-speech preserves: the original
performance's *prosody* — ideal when the read was good but the voice was
wrong, useless when the read itself was the problem (a squeaky take stays
squeaky in a deeper voice; a scream keeps its screech — use TTS mode or
transplant a better take instead).

Whisper-transcribe every dialogue clip against the script as QC — screams and
short trailing commands are what drop most often, and they're better fixed by
overlaying the TTS line than by re-rolling the clip.

<details>
<summary>ElevenLabs &amp; voice-reference recipes</summary>

- Slice a voice reference from an approved take:
  `ffmpeg -i take.mp4 -vn -ss <start> -t <len> -c:a aac anchors/voice/name.m4a`
  — confirm only the target character speaks in the window (silencedetect),
  then pitch_check it. Seedance accepts up to 3 `--audio` refs.
- Key at `~/.elevenlabs_key` (chmod 600) or `$ELEVENLABS_API_KEY`; create keys
  at elevenlabs.io → API Keys. A paid tier is needed for voice cloning and the
  commercial license.
- List voices (premade ids included):
  `curl -s https://api.elevenlabs.io/v1/voices -H "xi-api-key: $(cat ~/.elevenlabs_key)"`
- Clone a character from an approved sample:
  `curl -X POST https://api.elevenlabs.io/v1/voices/add -H "xi-api-key: $(cat ~/.elevenlabs_key)" -F "name=..." -F "files=@sample.m4a"`
- The community library is addable by API (`GET /v1/shared-voices` search,
  then `POST /v1/voices/add/{owner}/{voice_id}`) — a far deeper casting pool
  than the ~20 premades. Note: shared voices resolve only for the account
  that added them.
- TTS: `POST /v1/text-to-speech/<voice_id>` (JSON: `text`, `model_id`
  `eleven_multilingual_v2`). STS: `/v1/speech-to-speech/<voice_id>`
  (multipart: audio file, `model_id` `eleven_multilingual_sts_v2`). PCM output
  is gated to higher tiers — take the default mp3 and convert with ffmpeg.
- Quota: `curl -s https://api.elevenlabs.io/v1/user/subscription -H "xi-api-key: $(cat ~/.elevenlabs_key)"`.
- Batch redub of a finished film: `tools/templates/dub_pass.py` (demucs
  two-stem split → silencedetect speech segments → per-segment STS into the
  cast voice → remix over the ambience stem → remux onto the untouched video).
</details>

## Music, ambience, and the mixing rule

Score scenes, not eras: short cues on specific moments, silence under comedy
dialogue, and a recurring motif at matching beats reads as intentional
scoring. Sonilo runs about 3.75 credits a minute
(`higgsfield generate create sonilo_music --prompt "..." --duration N --wait`);
always append "instrumental only, no vocals". "Background ambience music"
prompts — no drums, muffled, across-the-room — sit under scenes far better
than "a song".

Ambience is what glues cuts into scenes: one steady bed per location, living
in the assembler. Generate beds with ElevenLabs sound-generation as 22-second
loops, asking for pure texture ("steady seamless loop, no sudden events") and
naming what you *don't* want — grassland prompts default to crickets. Then EQ
them (high-pass 100 Hz, low-pass 7 kHz, which also removes ElevenLabs' baked-in
high-frequency whine), crossfade-stitch to five minutes, and normalize.

The mixing rule that prevents every "the music is overpowering" round: **set
all levels in LUFS, never in mean volume**. Spiky sounds like crickets read
quiet on an amplitude meter but loud to the ear; ebur128 hears them the way
you do. One guard on the normalizer: a bed that needs more than ~12dB of gain
to reach target isn't quiet, it's a failed generation (ElevenLabs sometimes
returns near-silence), and boosting it just amplifies the noise floor into a
mechanical drone — regenerate or drop it. A `-inf` loudness measurement is
that failure announcing itself.

The mix itself is three steps. Normalize every stem to a common -30 LUFS.
Measure the **speech anchor** — integrated LUFS of the concatenated dialogue
lines alone, never of the whole film. (Whole-film LUFS is diluted by silent
holds; that dilution actually places beds *quieter*, not louder — we once
blamed it for loud music and had the sign backwards. Speech-only measurement
buys predictability, not a level fix.) Then place music about 15dB under the
anchor and ambience about 16, expecting the mixes that sound right to run
nearer 18–22 under during dialogue.

What actually makes music drown dialogue, in order of impact: (1) **no
ducking** — the single biggest fix. A statically-placed bed at even a correct
level reads as competing the moment a line starts; sidechain-duck the whole
bed bus under the dialogue track
(`sidechaincompress=threshold=0.02:ratio=8:attack=80:release=900`), worth
~8dB during overlaps. (2) **Static offsets too hot** — hence the 18–22dB
figure above. (3) **Integrated-LUFS normalization under-reads a cue's loud
passages** — a quiet intro dilutes the average, so the normalized chorus
plays several dB hotter than nominal, usually right under a line (the same
averaging-window bug as the crickets, one level up). All of this is already
implemented: copy `speech_anchor()` and the ducked mix graph from
`tools/templates/make_animatic.py` rather than re-deriving it.

And since none of us here have ears, `listen.py` sends any audio to Gemini —
but only ever ask it to FIND FAULTS or compare A vs B, never to rate quality.
Prompted adversarially it catches whines, wrong-content beds, and "this
sounds like tinnitus" that no meter shows; asked "is this good?" it calls
everything flawless, including a voice that was literally inaudible. Even its
fault reports pattern-complete: it once found a real whine (spectrum-verified,
a +18dB narrowband spike) and then claimed the same whine in beds that
measure clean. Treat its findings as leads and confirm with an FFT/ebur128
measurement before mass-applying a fix — audibility and level questions are
measurements, not listening questions.

## Batches and money

The workspace allows eight concurrent Seedance jobs, shared across every
session and terminal (the cap is per job type; submissions past it are
rejected instantly, never created, and never billed, so retrying is always
safe). gen.py enforces the cap with a slot-file semaphore — set
`SEEDANCE_SLOTS=4` if you're also submitting outside gen.py. Nano Banana and
Sonilo aren't capped the same way (~5 concurrent images and 3 music jobs run
clean). Run batches through pool_run.py — it skips shots whose output already
exists, so re-running the same command is the retry pass, and in fast mode
it auto-upgrades any `--audio` shot to std (fast+audio jobs always fail). Name shots with
short act-prefixed slugs (`a3_reveal`, `b12_cough`) and land each pass in a
versioned `outputs/videoN/` dir so reverts stay one-line edits. Generate the
batch script from the same shot table the storyboard uses so the two can't
drift, and run `caffeinate -is` during long waits.

A client-side failure is not a job failure: `--wait` can drop while the job
finishes server-side and bills anyway, so check `higgsfield generate list
--json` before resubmitting — completed jobs download free from their
result_url. An HTTP 503 or "no response received" at submission usually means
the job was never created — check the list to be sure, then just retry. And
when a whole tail of a batch suddenly fails, check
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

Install the CLI with `npm i -g @higgsfield/cli` (Node 18+). Auth is browser
OAuth (`higgsfield auth login`) followed by `higgsfield workspace set <id>` —
without the workspace step nothing works. The npm CLI is the only path to
Seedance 2.0 and Nano Banana Pro (the REST API only has older models);
`higgsfield model list` shows everything available — TTS, 3D, upscalers,
Veo/Kling, worth re-checking for new tools — and
`higgsfield model get <job_type>` shows a job's params. **Don't buy Higgsfield
"Unlimited"** — unlimited generation only works in their web UI; CLI/API jobs
bill normal credits regardless (verified: the CLI has no unlimited flag and
web-toggle params can't be forwarded). Seedance 2.0 also exists *without*
Higgsfield: fal.ai and BytePlus ModelArk sell it by API key (~$0.30/s std) —
pricier per clip, but no OAuth, no workspace, no expiring credits.

API keys live at `~/.elevenlabs_key` and `~/.gemini_key` (plus `~/.fal_key`
if using fal.ai as an alternate Seedance provider). `gen.py` (video/image
generation) sits at the repo root; the other shared tools (pool_run,
dub_clip, pitch_check, listen) live in `tools/`, with best-of-breed per-film
tools to copy in `tools/templates/`; each film is its own subfolder. The repo
(github.com/dawndrain/movie-gen) excludes media and any project adapting a
copyrighted source — add such projects to .gitignore BEFORE committing. The
war stories and measurements behind everything above are in PROJECT_LOG.md.
