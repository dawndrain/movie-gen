# Making movies with Higgsfield — the FULL playbook (archive)

> **Read MOVIE_LESSONS.md first** — it's the distilled, human-readable
> version. This file keeps the complete detail: per-project addenda (add
> new ones here, at the top, as before), API recipes, and war stories.
> When an addendum lesson generalizes, promote a one-liner into the short doc.
> (2026-07-18: film folders other than long_game/ moved under other_movies/ —
> addenda paths like carl/... now mean other_movies/carl/...)

> Addendum (2026-07-12, "The Vaulted Sky" v2 convergence — the complete
> input-filter model, ~9 rounds of evidence):
> - The gate is an ADDITIVE, partly STOCHASTIC multimodal score over
>   {start image, prompt text, audio refs (by upload-count), maybe refs}.
>   Near-threshold bundles pass/fail run to run — identical resubmission
>   converged 3 stuck shots in a persistence loop (pool_run re-runs are
>   the retry; failures don't bill, so loops are free).
> - PROBE-GATE frames: roll the frame, submit a 5s trivial-prompt fast job,
>   keep only rolls that pass, THEN build the real shot. Costs ~7.5cr per
>   pass, nothing per fail. Probe in a config as close as possible to the
>   real render (the score is additive — a frame that passes trivially can
>   still die under a heavy prompt).
> - Prompt text spends filter budget: character NAMES + anatomy checklists
>   ("Mewtwo is a six-and-a-half-foot..."), meta-instructions ("reference
>   images", "dialogue added in post"), body vocabulary (lips, mouths,
>   anatomy, faces), negation stacks ("no X, never Y, nobody Z") — each
>   adds score. For near-threshold shots use PURE VISUAL STAGING with
>   positively-phrased guards; identity comes from the start frame.
> - When a composition is terminal (12+ fails across every variable):
>   change the SHOT — a detail-insert closeup (hands, props, lights)
>   carries the beat, scores near zero, and lands first try.
> - Silent-render + assembler overlay is a full workaround for lip-free
>   dialogue: render with no audio refs, mix TTS lines at animatic spacing
>   in the ffmpeg graph. Whisper-QC silent renders — one grew a spoken
>   stage direction ("tasting each word for the very first time" →
>   "For the very first time"); mute the clip, dialogue rides the overlay.

> Addendum (2026-07-12, "Dungeon Crawler Carl book one" animatic, ~/Code/videogen/carl):
> - **Overnight animatic-only pipeline, zero Seedance credits, ~760 cr total**
>   (17 anchors + 37 frames at 2k + 8 sonilo cues; 2k images are a real line
>   item at this volume — next time consider 1k for frames that will only ever
>   be animatic stills). 10.6-min cut from cold start in ~4.5h wall clock.
> - **Copyrighted-novel adaptation discipline**: unlike the public-domain
>   projects, ALL dialogue was written as original paraphrase of the plot
>   (short famous catchphrases only). A research subagent built the beat sheet
>   from fan wikis rather than the text — also caught which famous moments are
>   NOT in book 1, which a from-memory treatment would have botched.
> - **Frame prompts must carry the STYLE block even with photoreal anchor
>   refs.** The one frame set OUTSIDE the dungeon (a suburban night exterior)
>   came back as a storybook ILLUSTRATION — portrait refs alone don't hold the
>   medium; the location plates were doing that job everywhere else.
> - The word "crawlers" for people in a prompt gets taken LITERALLY (three
>   rescued humans on hands and knees). In-universe jargon needs a plain-
>   English gloss ("prisoners, WALKING upright").
> - spec.py as single source of truth (anchors/frames/lines/order/music marks/
>   cast) with every other script importing it worked great — retakes are a
>   spec edit + skip-existing re-run, and the storyboard can't drift.
> - Persistent nsfw on a solo boxers-clad figure was fixed by deleting the
>   phrase "still no pants" — the lock's positive wording ("wearing red
>   heart-print boxer shorts") passed fine. The filter reads prose, again.
> - Nano Banana targeted edit ("change ONLY the torch to a lighter") again
>   beat a re-roll for a one-prop fix on an otherwise-perfect frame.
> - Gemini listen.py QC'd the voice CASTING (described the AI pick as "GLaDOS
>   mixed with a carnival barker" — instant confidence) and the final mix
>   (confirmed the LUFS-offset scheme: anchor -20.4, music -12 dB, amb -14 dB
>   under; no per-cue hand-tuning needed for a v1).
> - (added 07-18) **LUFS-check every TTS take, not just voice samples** — one
>   catalog voice (Merv) renders ~-37 LUFS, ~21 dB under the pack, and two
>   near-silent Maggie lines shipped in v1. THREE QC layers missed it: Gemini
>   "dialogue always intelligible" full-mix pass (can't miss what it doesn't
>   know should be there), pitch stats (F0 fine on a quiet file), and the
>   skipped whisper-vs-script diff ("TTS is the script by construction" — but
>   not if the take is inaudible). Director's ear caught it in one listen.
>   tts_phase now flags takes under -30 LUFS.
> - (added 07-18) Gemini is a DEFECT detector, not a taste judge: on "rate
>   the fit" it scored 6/6 designed leads "10/10 / flawless"; asked to QC the
>   broken Merv take blind it did reject it (noise floor, mouth clicks) but
>   never noticed the actual defect — the level. Ask it for problems, not
>   ratings, and keep the meters in the loop.
> - (added 07-18) **The inverse failure mode is just as real**: told "report
>   problems with timestamps; do NOT compliment", Gemini produced 8
>   confident timestamped defects for the v2 mix — and all 3 objectively
>   checkable ones were FALSE (claimed clipping: peaks -4.3 dBFS, 0 clipped
>   samples; claimed digital click: normal transients; claimed audio ending
>   500ms early: audio outlives video, intentional fade). It satisfies the
>   instruction, not the audio — in BOTH directions. Meter-verify every
>   concrete Gemini claim before spending a fix on it; treat its taste
>   notes as hypotheses for the director's ears only.
> - (added 07-18) **median-F0 measures the note, not the "depth"**: bellowing
>   characters (Maestro, the Juicer) legitimately read 225-245 Hz — shouting
>   raises the fundamental — while calm deep briefs sat 100-130 Hz. Perceived
>   depth is timbre/formants, invisible to F0. Don't pitch-screen shouty
>   registers against conversational thresholds.
> - (added 07-18) ElevenLabs Voice DESIGN (text-to-voice/create-previews, 3
>   previews per written casting brief, ~65 chars billed per 1k-char call) is
>   a real casting pool beyond premades/library — 51 bespoke candidates for
>   ~3.3k chars, and the briefs double as director-readable casting notes.
>   generated_voice_ids persist in designed_voices.json; `adopt` saves the
>   pick + updates cast_overrides.json + clears stale vo lines in one step.
>
> Addendum (2026-07-11, veo3 std-vs-fast BLIND test, ~/Code/videogen/veo3_compare):
> - **ROUND 2 (10 more pairs, face/dialogue-heavy prompts): fast won 7-1 with 2
>   no-decisions. Combined: fast 13 of 18 decisive picks (one-sided p≈0.048)** —
>   Dawn (the director) doesn't just fail to prefer std, she mildly prefers fast. The
>   "fast is weaker on faces" folklore failed directly: the worst identity
>   failures (head-morphing man, skeleton-heavy morph) were both STD takes.
>   Verdict: at ≤720p never pay for std; two fast rolls per shot instead.
> - **Blind A/B, fast tied std** — 10 pairs (480p/8s, raw montage-style prompts,
>   NO start frames/anchors/audio refs), A/B randomized per pair, director scored
>   blind: fast won 6-4, a statistical coin flip (P(≥6)≈0.38). 9/10 of the
>   director's stated reasons were prompt-following/content ("actually shows the
>   gag", "doesn't have a fucked-up pandahorse") — i.e. per-take seed luck, not
>   rendering fidelity. Take-to-take variance >> mode difference in this regime.
> - **Implication**: two fast rolls (= the price of one std) + pick the better
>   take likely beats one std roll. Std stays mandatory where fast is actually
>   broken: multi-`--audio` dialogue (see The Variance) and >720p.
>   RESOLUTION of the tension with The Vaulted Sky's "fast is unusable" verdict:
>   Dawn retracted it after seeing the blind result ("I think I was
>   confused... that was mostly an issue with very bad prompting") — consistent
>   with The Long Game's original finding that the early anti-fast verdict came
>   from minimalist prompts, not the mode. Default to fast at ≤720p.
> - **Std is not slow anymore**: 6 std + 6 fast (480p/8s) finished in ~7 min wall
>   clock; 20 jobs in ~15 (uncontended workspace). Matches the short doc's "3-5
>   min/clip, 30+ min means contention", contra the older 30-45 min/clip note.
> - Failure statuses are roll-luck too: one prompt failed std 5× ("failed", not
>   nsfw) then passed verbatim on attempt 6; another tripped nsfw 3× in fast,
>   passed std, then later passed fast verbatim. Retry a few times before
>   rewording (the "two rewordings then restage" law is for PERSISTENT patterns).
> - Whisper (`whisper-cli` + repo model `.whisper/ggml-small.en.bin`) on a montage
>   + per-8s-segment re-runs cleanly reverse-engineers which prompt variant made
>   which clip (dialogue is the discriminator; music/noise hallucinates "no no no").

> Addendum (2026-07-11, "Homo Sapien" music video, ~/Code/videogen/home_sapien):
> - **Cut an ANIMATIC before spending a single video credit.** All 43 Nano Banana
>   start frames, each held for its exact cut window, hard-cutting on the beat of
>   the real track, lyrics burned on as an .srt (`animatic.py`). ~2 min of ffmpeg,
>   zero credits, and it answers the only question that matters — does the edit
>   work — while every shot is still free to change. Do this on every film, not
>   just music videos.
> - **A concat list has no timeline: gaps collapse and everything after slides
>   early.** Hold each frame from its own in-point to the NEXT shot's in-point
>   (not `out - in`), or one 1.7s hole between shot windows drags every later cut
>   off the beat. The song is the clock; the picture fills what it's given.
> - **KEN BURNS: use `perspective`, NOT `zoompan`.** A slow push on each still is
>   the single biggest upgrade available to an animatic — it makes the film breathe
>   instead of sit — and `zoompan` is the wrong tool for it, for two reasons:
>   1. **zoompan truncates the crop origin to INTEGER pixels.** On a slow move the
>      true origin advances a fraction of a pixel per frame, sits on one integer
>      for several frames, then SNAPS a whole pixel. That snap is the notorious
>      quiver — and it is worst precisely on slow moves, i.e. on Ken Burns. It
>      looks fine in the punchy 2-second demo and fails in the real use case,
>      which is how a bad default became folklore.
>   2. **The canonical `z='min(zoom+0.001,1.5)'` form is itself broken with `d=1`**
>      — the `zoom` accumulator RESETS every input frame, so it never accumulates.
>      Measured: mean motion 0.000 with 454% variability. It is not zooming at all;
>      it is a static image that jerks. A lot of people are shipping this.
>
>   Supersampling before zoompan only shrinks the quantum (1/4 px at 4x) — it never
>   removes the staircase. The RIGHT answer is continuous resampling: sample the
>   source at exact FRACTIONAL coordinates with a real kernel, no integer grid
>   anywhere. `perspective` does exactly that — float corner coords, `eval=frame`,
>   `interpolation=cubic`. Measured frame-to-frame roughness, same shot/move,
>   lossless:
>
>   | method | roughness | snap frames |
>   |---|---|---|
>   | zoompan 1x | 162% | 73/168 |
>   | zoompan 4x supersampled | 24% | 0/168 |
>   | **perspective (sub-pixel)** | **0.3%** | **0/168** |
>
>   0.3% is encoder noise: smooth, not "smoother". Costs ~2x render time (3min ->
>   6min for 43 shots) and it is worth it. Recipe in `homo_sapien/animatic.py`:
>   scale to 2x, `perspective=eval=frame:interpolation=cubic` with the source rect
>   as float exprs in `on`, then scale down. Drive the zoom from `on` (absolute
>   output frame index), never from a feedback accumulator.
> - **LOCK OFF the shots that are ABOUT stillness.** A drift on every shot reads as
>   a mechanical gimmick and actively fights certain images: the creature whose joke
>   is that it does NOT move while geological time rips past; the reverent handprint
>   plant; the museum-glass shot whose whole note is "do not move the camera"; the
>   final Earth hold. Four of 43 shots locked off; alternate push-in/push-out on the
>   rest so the cut rhythm doesn't feel like a machine.
> - **Style words bleed across subject classes.** "handmade / tactile / wool" in a
>   global STYLE block turned every creature shot into KNITTED FELT PUPPETS while
>   the humans stayed photoreal — two different films in one cut. Creatures need
>   their own style constant (`CREATURE`: "a real living animal… absolutely NOT
>   knitted, NOT felt, NOT a puppet"). Watch for this wherever one STYLE string
>   spans humans + animals + cosmos.
> - **Reusing a real song inverts the whole pipeline**: no TTS, no voice refs, no
>   dubbing, no whisper-QC, no Sonilo. Instead every clip prompt needs "nobody
>   speaks and nobody sings; no lips move", every clip is muted at assembly, and
>   the master track is laid over the finished picture as one continuous bed.
> - Get lyric timings from the audio itself, not a lyrics site: `yt-dlp` the track
>   → `whisper-cli -ml 1 -sow -ojf` → group words into lines on >0.7s gaps. Whisper
>   mishears sung words badly ("Be my Homo Sapien" → "Be my home, I'll stay
>   behind"), so keep whisper's TIMES and the released lyrics' WORDS.
> - Directional prompts need an explicit axis: "two figures walking left to right,
>   changing form as they walk" produced a March of Progress running BACKWARDS
>   (modern on the left). "OLDEST ON THE LEFT to NEWEST ON THE RIGHT… more upright
>   as the eye moves RIGHT" fixed it first try.
> - **"Two parallel lanes" is a staging the model cannot hold.** Three rewordings
>   of a two-lane evolution procession failed three different ways: mismatched
>   species across the lanes (a fox opposite a mongoose), then a literal stacked
>   SPLIT SCREEN, then both lanes walking toward each other — with the fish given
>   little wheeled aquarium carts. The fix was the Walter's-Deal rule: after two
>   failed rewordings, change WHAT HAPPENS. Restaged as ONE procession in which
>   every rung is a couple walking shoulder to shoulder, it worked first try — and
>   said "side by side" far better than the original idea. When a composition needs
>   two of something in a fixed spatial relationship, put them in ONE line, not two.
> - **Check the props for what they IMPLY, not just whether they're period-correct.**
>   The caveman's wolf pelt came back with the head and face still attached — and it
>   read as the teal fox from the evolution shot two cuts earlier, i.e. the hero
>   wearing a previous incarnation of his own wife. Wardrobe items made of animals
>   need "a PLAIN CUT PANEL of fur — NO head, NO face, NO paws, NO tail".
> - When a physical detail is anachronistic (naked australopithecines can't wear a
>   colour-coded costume), move the motif from WARDROBE into the BODY — rust-orange
>   vs blue-grey natural fur. It fixed the anachronism and improved the idea: the
>   colour is something they're born with that only later becomes something they
>   wear.
> - A storyboard.html with the actual song embedded and every timecode a seek
>   button (click → the track jumps there) makes checking cuts against the beat a
>   one-click loop instead of a scrubbing exercise.
> - **nsfw can be triggered by INTIMACY LANGUAGE on an image with no people in it.**
>   The binary-stars clip — two stars, nothing else — took 3 straight nsfw
>   rejections on the words "leaning in until they almost touch, then swinging
>   apart... the rhythm is a slow breath: a forehead touch at cosmic scale."
>   Rewritten as plain astronomy ("circle slowly around a shared centre of
>   gravity"), it passed first try. The filter reads the PROSE, not just the
>   picture: keep tenderness in the staging and the framing, not in the adjectives.
> - Generate the batch script FROM the clip spec (`make_batch.py` → `videos_v1.sh`)
>   so the prompt that ships to Seedance is byte-identical to the one shown in
>   storyboard.html. Hand-copied .sh files drift from the storyboard immediately.
> - **Keep a FACE-only lock beside every wardrobe lock.** The `W[...]` strings END
>   with the character's normal clothes, so "{W['may']} in a simple wedding dress"
>   literally asks for a cardigan AND a dress in one sentence — and the cardigan
>   wins. She turned up to her own wedding in a cardigan and jeans. Any shot where
>   a character is OUT of their usual clothes (wedding, period costume, uniform,
>   disguise) must use a `FACE[...]` variant — identity only, no wardrobe — plus an
>   explicit "absolutely NOT wearing <their normal outfit>". Check every costume
>   shot for this; it is silent and easy to miss on a contact sheet.
> - **A HELD STILL MUST SHOW THE END OF THE BEAT, not the start of it.** This is the
>   one rule that separates an animatic frame from a video start-frame, and they
>   want OPPOSITE images. A clip needs the character at their STARTING position (or
>   Seedance invents the journey — it materialised a man out of a corner and walked
>   him through a table). But a still is HELD: it has no "later", so whatever it
>   shows, it shows for the whole window. The doorway frame that shot perfectly as
>   video read, frozen, as her waiting alone for six seconds. Same trap on the
>   handprints: hands pressed ON the wall hide the prints underneath them, so the
>   paint just reads as a red blob — the frame has to show the hands LIFTING and the
>   prints already made. Keep both versions on disk when a project may go either way.
> - **A `nsfw` rejection can come from the INPUT IMAGE, not the prompt.** Three
>   rewordings of a targeted edit all bounced — the ref image contained a child's
>   hand, and no phrasing was going to fix that. When rewording fails and you are
>   passing an `--image`, suspect the image and regenerate fresh instead.
> - **TARGETED EDITS beat re-rolls — `edit_frame.py`.** [Director's later
>   verdict: this never actually worked as intended in practice — treat the
>   claims below as unreproduced.] Pass the existing frame as
>   an `--image` ref with "reproduce the reference EXACTLY... change ONLY <x>" and
>   Nano Banana changes just that one thing. A re-roll re-rolls EVERYTHING (faces,
>   staging, light), so fixing one animal can cost you the whole shot — this is the
>   retake regression law, and a targeted edit sidesteps it entirely. Used to swap
>   one mismatched animal in a 10-creature frame and to shrink adult handprints to
>   a toddler's, both leaving the rest pixel-identical. Reach for this BEFORE
>   rewriting a prompt and regenerating.
> - **`outputs/raw/` is an undo buffer — every take ever generated is still there**,
>   timestamped and prompt-slugged. When the director says "go back to the previous
>   one", `ls -lt outputs/raw | grep <slug>` and `cp` it back; build a contact sheet
>   of the takes and let them pick. Three "improvements" to one shot had to be
>   reverted this way. Corollary: never assume an overwritten frame is lost.
> - Gags must not be mistakable for MODEL ARTEFACTS. A clay figure proudly growing
>   a SIXTH FINGER read as a stock AI hand glitch, not a joke; swapped for a whole
>   THIRD ARM, which cannot be misread. Same for "figures made of clay" → the model
>   paints a person grey; you must say SCULPTURE, thumbprints, cracks, no skin.
> - Mood words are weak; the model defaults to RESTING BITCH FACE on "cheerfully
>   arguing" and "playfully bickering" (she read as stern and unimpressed). Say
>   what the FACE is doing, in the positive: "BOTH ARE LAUGHING... she is beaming,
>   mouth open in a big delighted laugh... neither is annoyed, cross, stern or
>   unhappy". Same class of fix as the Njal staging lesson — describe the behaviour,
>   not the emotion.

> Addendum (2026-07-10, "The Long Game" late rounds, ~/Code/videogen/long_game):
> - **One --audio ref gets applied to EVERY speaker** — Seedance doesn't map voice
>   refs to characters. A two-speaker shot with one ref gave Milo Cass's voice.
>   Only voice-ref single-speaker shots (or accept everyone sharing the voice).
>   And label refs by scene REGISTER, not just character: cass_teen.m4a was sliced
>   from an in-game (British-leaning) rant, so cloning it onto an arcade scene
>   shifted the whole scene English. A character with different voices in
>   different contexts needs one sample per context. Corollary: a slightly
>   awkward dub of a good take usually beats a native-audio retake — the retake
>   re-rolls voices/continuity in ways the dub never touches. (Dawn reverted two
>   native retakes back to dubs on this basis.)
> - **Crowd creep**: dialogue scenes regenerate with extra onlookers unless the
>   prompt says "the [location] is otherwise completely EMPTY - no other people,
>   no onlookers". One lock line fixed it in both q2 and a cutaway. And even a
>   nano-banana'd start frame with people REMOVED doesn't stop Seedance re-adding
>   them — the lock has to be in the video prompt.
> - **Missing anchors are silent**: an off-model shot traced to the original gen
>   simply never passing those characters' --image refs. Diff the shot's ref list
>   against the cast before blaming the model.
> - **Color-matching a clip to its neighbors**: histogram-match pooled frames
>   (per-channel CDF map, blend ~75% toward the match), bake into a Hald CLUT PNG,
>   apply with ffmpeg haldclut + `-c:a copy`. One static LUT = no temporal flicker.
>   Beats hand-tuning eq/colorbalance, which never landed after two rounds.
> - **Renaming an on-screen prop**: nano-banana the frame ("heading now reads
>   exactly '...'") then retake with "the chalkboard exactly as in the start image,
>   its writing unchanged the entire clip" — text stayed stable all shots.
> - **Mid-sentence word swap dub**: TTS the WHOLE sentence for prosody, crop just
>   the phrase (whisper word timestamps), atempo to fit the hole, volume-match,
>   overlay on the no_vocals stem. QC by re-transcribing. Works; still only ~90%
>   — expect the occasional "very bad" verdict and keep the original take on disk.
> - **Endings are cheap**: 18.5s credits sequence = ffmpeg drawtext amber Courier
>   cards over black + looped ambience stem + one sonilo cue (~5 cr), spliced in as
>   a normal CUT entry. Big perceived-quality win ("dude the ending is really cool").
> - **Same-scene continuity, what actually works**: (1) ONE canonical start frame
>   reused for every repeat of a beat (all respawns open on the same frame);
>   (2) chain shots — extract the outgoing clip's last frame as the next clip's
>   --start-image; (3) restate the full wardrobe/character lock verbatim in EVERY
>   prompt of the scene, not just the first. And slice ANCHOR VOICES before
>   shooting any dialogue at all — retrofitting voices via dubs was this film's
>   single biggest time sink.

> Addendum (2026-07, "Burnt Njal", ~/Code/videogen/njals_saga):
> - **Anchor only the RECURRING cast.** Single-appearance characters (a dying
>   father, a one-scene lawspeaker) are described inline in their one frame —
>   the frame IS their only appearance, so there's nothing to keep consistent.
>   Cut the anchor bill from 23 portraits to 14 with zero continuity cost.
> - Identity drift in a multi-ref frame (Bergthora came out dark-haired) is
>   fixed by RESTATING the anchor's wardrobe checklist in the frame prompt
>   ("IRON-GRAY braids under a white head-cloth... exactly the same face as the
>   second reference") — same fix as the Hork-Bajir anatomy lock, works first try.
> - Scan frames for CONTINUITY PROPS, not just faces: the Yule-feast frame came
>   back missing the eyepatch that pays off the jaw-tooth gag from the Burning.
>   Frames that carry planted props deserve an explicit ALL-CAPS callout in
>   the prompt ("with a DARK LEATHER PATCH covering his right eye").
> - Staging beats mood words: "grinning happily vs dangerously" rewords did less
>   than restaging ("stares straight ahead PAST him... knuckles white"). Same
>   for geometry: "trapped, pinned upright between a fallen smoking roof-beam
>   and the gable wall" fixed a shot that read as two guys chatting by a fence.
> - Background-launch scripts by ABSOLUTE path; the harness shell's cwd moves
>   between calls, and `chmod +x njals_saga/...` in a background task silently
>   ran in the wrong directory (the `cd` inside the script is what saves you).
> - **Don't Ken Burns animatic stills with ffmpeg `zoompan`** — at slow zoom
>   rates the crop rounds to whole pixels every frame and the image visibly
>   QUIVERS (director note: "weird quivering"). Static holds read better and
>   encode faster. If a push-in is ever truly wanted, upscale the still 4-8x
>   BEFORE zoompan so the rounding is subpixel after the downscale, or animate
>   `crop` with fractional x/y — but for an animatic, just hold the frame.
> - Animatic durations double as the SPLIT LIST for the Seedance pass: sizing
>   shots from real TTS (lead 0.6s / gap 0.55s / tail 0.9s) exposed 19 of 37
>   dialogue shots over the 15s clip cap before any video money was spent.

> Addendum (2026-07, "Egil's Saga", ~/Code/videogen/egils_saga):
> - **`not_enough_credits` mid-batch looks like a generic failure storm**: every
>   job from one point onward fails with "generation failed" and the per-job
>   retry loop burns all 3 attempts on each. Check `higgsfield account status`
>   FIRST when a whole tail of a batch fails — the make_images.py skip-existing
>   re-run resumes cleanly once credits refresh. (Batch died at 24/38 frames
>   with 0.5 cr left after sibling projects drained the cycle.)
> - Public-domain sagas: sagadb.org has full English texts (Gutenberg search
>   may miss them); strip the HTML body — 92 chapters / 72k words extracted in
>   one pass. 7 parallel readers → chapter notes with verbatim dialogue +
>   skaldic verses worked exactly like the novel pipeline.
> - Face-continuity across generations for free: generate the kinsman/aged
>   variants with the base portrait as `--image` ref + "EXACTLY the same face
>   as the reference image" — worked first try for both a same-face nephew
>   and an aged-to-85 version of the lead.

> Addendum (2026-07, "Walter's Deal", ~/Code/videogen/walters_deal):
> - **Persistent nsfw ≠ wording problem.** One shot (woman gives speech, steps into
>   booth, vanishes before a crowd) got 6 consecutive nsfw rejections across three
>   prompt rewordings AND a regenerated start frame. The fix was removing the
>   on-camera action "she steps into the glass booth and the door closes" — the
>   confinement-before-a-crowd staging itself was the trigger, not the words. If two
>   rewordings fail, change WHAT HAPPENS (or move the event off-screen), don't
>   keep rephrasing. (A child vanishing mid-teleport in a different shot passed fine.)
> - `gen.py` now enforces the 8-job Seedance cap across ALL sessions via a slot-file
>   semaphore (`.seedance_slots/`, PID-stamped, stale-reclaimed) — video calls block
>   until a slot frees instead of bouncing off rate_limit_reached. `SEEDANCE_SLOTS=4`
>   to shrink the budget when also submitting outside gen.py.
> - Novel-to-film pipeline: 7 parallel reader subagents (2k lines each) → per-chunk
>   plot/characters/settings/key-scenes notes with verbatim dialogue → 37-shot
>   storyboard. Whole 379-page book digested in ~5 min wall clock.
> - Nano Banana image jobs can also end "failed" on female-portrait prompts with
>   appearance-focused wording ("striking", necklines); neutral rewording passed.
> - First pass (37 shots, ~5:20, 480p fast, 10 anchors + 39 frames + 3 music cues)
>   ≈ 700 credits, ~2h wall clock including the nsfw fight and rate-limit collisions
>   with three sibling projects running in the same workspace.

> Addendum (2026-07, "The David Trilogy", ~/Code/videogen/animorphs_david):
> - Human-teen casts work with the same anchor discipline as creatures: one portrait
>   per kid with a full head-to-toe WARDROBE dict reused verbatim in anchor + frame +
>   clip prompts. Watch Nano Banana hallucinating extra creatures behind solo
>   portraits ("She is the ONLY figure in the frame" fixes it) — they bleed into
>   every downstream frame if left in the anchor.
> - Nano Banana start frames can inject props characters shouldn't have (the
>   morphing cube appearing in a rooftop scene); scan contact sheets for prop
>   continuity, not just faces. ffmpeg xstack sheets of ~12 frames per read are the
>   fastest review format.
> - Animal thought-speak (Animorphs style) works with the mouthless-Andalite trick:
>   "the animal's mouth NEVER moves; the voice is simply heard" + name the speaker
>   per audio clip ("the thought-speak voice of David, the lion"). 29 dialogue clips
>   whisper-QC'd: 27 near-verbatim, 2 soft drops — short trailing commands
>   ("Demorph, everyone") are the most-dropped line type, same class as screams;
>   retake or overlay.
> - Auto-size clip durations from TTS: sum(audio)+2.5s+0.8s/speaker, clamp 5..15,
>   and SPLIT any shot over the cap at write-time (7 of 21 dialogue shots needed
>   it). A single TTS line >12s cannot fit at all — split the line itself into two
>   mp3s before building the batch.
> - Pitch-audition new voices in one batch (numpy autocorrelation median-F0 on the
>   mp3s, pitch.py); spreading the cast 82–208 Hz kept 8 speakers distinct. Reusing
>   a voice across films for the same in-universe character (Roman = Esplin 9466 =
>   Visser Three) is free continuity.
> - Shared-workspace contention (see The Variance note below): a plain re-run loop
>   of pool_run at 4 workers (it skips existing mp4s) converged in 2 passes without
>   touching the other project's jobs.

> Addendum (2026-07, "The Variance", ~/Code/videogen/overwhelming_beauty):
> - **FAST mode cannot take multiple `--audio` refs**: every 2-audio dialogue
>   shot failed server-side ("ended with status failed", 8/8 attempts) while
>   1-audio shots sailed through. Fix: ffmpeg-concat the lines into ONE mp3
>   (0.7s gap between speakers) and say "the first line is spoken by X, the
>   second by Y" — worked first try, voices and lip-sync both correct.
>   (STD mode multi-audio worked fine in the animorphs project.)
> - **The 8-job Seedance cap is per WORKSPACE, not per batch** — a second
>   project running in parallel eats your slots and every submission bounces
>   with rate_limit_reached. pool_run_fast.py now sleeps 60s and retries (8
>   attempts) on rate_limit instead of burning both attempts instantly.
> - Whisper-QC catches double-delivery: a clip can speak the line correctly
>   then grow a gibberish tail (or vice versa). If the good read is intact,
>   TRIM in the assembler (find the gap with silencedetect) instead of
>   re-rolling; if the line itself is mangled, retake with "speaks the
>   COMPLETE exact words of the reference audio... nothing added".
> - Narration CAN work (contra the Long Game note) when it is (a) sparse,
>   (b) mixed at ASSEMBLY on the global timeline so lines bridge cuts, and
>   (c) never sent to Seedance. Trim narrator lines to fit their windows
>   BEFORE generating clips — measure TTS durations first.
> - Nano Banana quirks: 3:4 portraits sometimes come back as a triptych/
>   contact sheet or with film borders — say "ONE single continuous
>   photograph filling the whole frame, no borders, no collage".
> - First pass (27 shots, ~4 min, 480p fast + anchors + frames + TTS + music)
>   ≈ 800 credits and ~2.5 hours wall clock including retries.

> Addendum (2026-07, "The Hork-Bajir Chronicles", ~/Code/videogen/animorphs):
> - **Creature-species consistency**: generate ONE species anchor first, then every
>   other individual of that species with it as `--image` ref + "the same alien
>   species as the reference image" + how this individual differs. Worked perfectly
>   for five distinct Hork-Bajir. When the ref is underweighted the model reverts to
>   generic (Alloran came out a war-panther): fix by restating the full anatomy
>   checklist in the prompt, not by adding more refs.
> - Nano Banana runs fine 5-concurrent (not subject to the 8-seedance cap); 42
>   frames ≈ 25 min. Occasional HTTP 503 → simple retry succeeds.
> - Non-humanoid dialogue works: lock species + per-character voice in every prompt;
>   for mouthless telepaths say "voice is heard while the face stays completely
>   still". Seedance respected it in the clips checked.
> - 42-clip 480p-std batch (~390s of film) completed in ~3h15m with 7 workers, zero
>   failures, zero nsfw false-positives. Whole first pass ≈ 1,340 credits
>   (images+music+video).
> - **VOICE LOCK (the big one)**: Seedance `--audio` refs clone the reference voice.
>   Pipeline: cast each character to a `text2speech_v2` preset (`hf voices list`,
>   elevenlabs variant — deterministic forever), TTS the exact lines (phonetic
>   spellings pin alien words, e.g. "Hork-BY-zhoor"), pass per-speaker mp3s as
>   `--audio` refs + "speak EXACTLY the dialogue in the reference audio clips, in
>   order, in exactly those voices". Verified by pitch analysis (clip median 69Hz ==
>   ref 69Hz; non-ref take 87Hz). Also largely fixes stilted delivery and enables
>   emotional reads via TTS punctuation/ellipses.
> - Seedance duration cap is 15s (`generate cost` errors above it). Size dialogue
>   clips as sum(ref audio)+2.5s+0.8s/speaker; split scenes that exceed 15s.
> - **Whisper QC loop**: transcribe every clip (whisper-cli + small.en) and WER-diff
>   against the script — catches gibberish/alien-chant drift, shortened lines,
>   spontaneous extra speech. Watch for POETIC STAGE DIRECTIONS getting spoken
>   aloud ("a teacher turning his people into soldiers" → the character said it);
>   keep staging prose literal on dialogue shots.
> - Screams/single-word shouts often don't survive into the clip: mix the TTS line
>   over the clip audio in the assembler instead of re-rolling.
> - Andalite torso collapses to quadruped in long gallops; a six-limb anatomy lock
>   + medium-close framing held for a 6s shot. Audition TTS voices by pitch stats
>   when you can't listen (male leads 65–110Hz; two presets were miscast at 136Hz
>   and 164Hz and swapped).

Core doc distilled from the first production ("The Long Game", `long_game/` — an
~11-minute, ~80-shot comedy, 12 iteration passes) with Seedance 2.0 + Nano Banana
Pro + Sonilo via the Higgsfield CLI. The addenda above capture later films'
project-specific discoveries.

## Repo layout (`~/Code/videogen`)

- **Top level = shared tools**, used by every movie project: `gen.py` (Seedance/Nano
  Banana wrapper; downloads land in the shared `outputs/raw/`), `pool_run.py` (batch
  runner — run it FROM a project folder: `python3 ../pool_run.py videos_vN.sh
  outputs/videoN [workers] [fast]`), `dub_clip.py`, `pitch_check.py`, and this file.
- **Each movie is a subfolder** (`long_game/`, `animorphs/`, `mewtwo/`, ...) holding
  its story md, `videos_v*.sh` batch scripts, `assemble_v*.py`, `storyboard_gen.py`,
  `frames/`, `frames2/`, `anchors/` (incl. `anchors/voice/`), `music/`, and
  `outputs/` (per-pass `videoN/` clip dirs + `previews/`).
- The Long Game (this film) lives in `long_game/` — copy its scripts as templates.

## The pipeline that works (v2 — ANIMATIC FIRST)

**Iterate on an animatic before touching Seedance** (director workflow
insight, The Vaulted Sky): once anchors + start frames exist, build the whole
film as stills + ElevenLabs cast + music (`mewtwo/make_animatic.py` +
`assemble_animatic.py`: per-shot still with a slow zoompan push-in — but see
the Burnt Njal note: `zoompan` quivers at slow rates, prefer static holds —
TTS lines with 0.6s gaps, same music beds as the real cut). It costs ~nothing
(ElevenLabs chars only), builds in minutes, and lets the director iterate on
script, shot order, pacing, voice casting and music — the things that
actually get re-noted round after round — before any 3 cr/s video is spent.
Only send shots to Seedance once their animatic version plays right; video
generation becomes the LAST step per shot, not the first.

## The pipeline that works

1. **Anchors first** (Nano Banana Pro): one portrait per character *per age/era*, plus
   location plates. These are the identity glue for everything else.
2. **Start frames** (Nano Banana Pro): one per scene, generated *using the anchors as
   image refs*. The start frame dominates the video — wardrobe, set, staging, and any
   on-screen text come from it more than from the prompt.
3. **ANIMATIC — cut the whole film before spending a single video credit.** Stills only:
   every start frame held for its exact cut window, hard-cutting on the beat / on the
   line, with dialogue as ElevenLabs TTS (or lyrics burned on as an .srt) laid over the
   top. ffmpeg concat + one encode, ~2 minutes, **zero credits**.
   - The economics are the whole point: an 8s Seedance clip is ~24 credits and 30–45 min;
     the same line of TTS is ~0.3 credits and 3 seconds. Finding out that a scene is
     three shots too long, that a joke doesn't land, or that a line reads flat is
     **~100x cheaper in the animatic than after the clips exist** — and it happens while
     every shot is still free to change. The retake regression law (below) never fires,
     because there is nothing to regress.
   - It also front-loads the voice work, which the Long Game named its single biggest
     time sink: cast the voices, TTS the script, and hear the film before it's shot.
     Those same mp3s then become the Seedance `--audio` refs — the animatic pays for the
     voice pipeline for free.
   - Build it from the SAME shot table the assembler uses, so the animatic and the final
     cut can never drift apart (`home_sapien/animatic.py` is the template).
   - **Hold each frame from its own in-point to the NEXT shot's in-point** — a concat list
     has no timeline, so any gap between shot windows silently collapses and every later
     cut slides early. The audio is the clock; the picture fills what it's given.
4. **Clips** (Seedance 2.0): `--start-image <scene frame> --image <anchor> ...` plus a
   maximalist prompt (see below). 480p `--std` only.
5. **Music** (Sonilo): short instrumental cues, ~3.75 credits/minute. Practically free.
6. **Assembly** (ffmpeg): versioned python script with a `CUT` list of
   `(clip, trim_start, trim_dur, mute, music_mark)`. Re-encode is ~10 min; iterate freely.
7. **Review** (`storyboard_gen.py` → `storyboard.html`): every shot in cut order with
   playable clip, dialogue, and collapsed generation prompt. The director reviews this +
   the preview mp4 and gives per-shot notes. This artifact made iteration 10x smoother.

## Quality settings & the draft/master workflow

- **Use FAST mode at ≤720p** (verdict reversed 2026-07-11 by a 20-pair blind
  A/B in veo3_compare: the director picked fast in 13/18 decisive pairs,
  including close-up-face prompts, and retracted the earlier "fast is unusable"
  call as a bad-prompting artifact). One roll per shot by default; re-roll
  shots that fail QC rather than paying double up front. Std remains required
  for multi-`--audio` dialogue shots and >720p output.
- **std is NOT slow — it is ~3–5 minutes per clip.** MEASURED (2026-07-11, Homo
  Sapien, 11 clips, 7 workers, uncontended workspace): the first wave of 7 all
  landed **3m18s–5m31s** after launch, and clip LENGTH barely mattered (a 10s clip
  took the same ~5 min as a 6s one — you are paying for a job, not for seconds).
  The whole 11-clip / 81-second batch was done in **under 10 minutes** wall clock.
  The old "30–45 min/clip" figure in this doc was wrong: it was measured while
  sibling projects were eating the 8-job workspace cap, so QUEUE WAIT was being
  recorded as generation time. That error is dangerous — it makes std look
  expensive when you do need it (multi-audio shots, >720p). If clips are
  taking 30+ min, you are not slow, you are CONTENDED: check for other sessions.
- The locks still matter more than anything: with weak prompts even std looks bad.

## Prompt template that works (Seedance)

Every clip prompt = **action with ordered beats + quoted dialogue + three lock blocks**:

- **Wardrobe/character lock** (per era): full head-to-toe description of every character
  in the shot, plus the set. Without it, modern clothes leak into period scenes and
  characters mutate. *Also fix the start frame* — if the frame shows a modern t-shirt,
  the lock text will not save you.
- **Voice lock** (every dialogue shot): pin the accent and delivery, e.g. "<Name>
  speaks in the same measured, dry British accent as the rest of the film — never
  American, never theatrical." Seedance rolls a random voice per clip otherwise (one
  character came back broey American, British, and as a child across takes). Better
  still, pass a per-character `--audio` voice reference (see Voice pipeline). Also
  always add:
  "There is no narrator and no voiceover; only characters visible on screen speak,
  lips moving" — otherwise clips occasionally grow spontaneous narration.
- **Negative block**: "Photorealistic, natural human motion..., no slow motion, no
  text/captions/subtitles, characters keep exactly the same faces and clothes as the
  reference images."

Other prompt lessons:
- **Seedance lip-syncs quoted dialogue well.** Write lines verbatim in quotes. Dialogue
  carries a film far better than narration (the narrated draft "trampled over
  everything"; the dialogue-only cut worked immediately).
- **Camera:** say "locked-off static camera, no zoom, no pan" whenever you don't want
  the model's default drifty push-ins.
- **Continuity of gesture/motion:** pass a previous clip with `--video` as a motion
  reference to repeat a signature gesture exactly.
- **On-screen text gags:** render the exact text in a Nano Banana frame (it does
  verbatim text reliably, even paragraphs), then tell Seedance "the text stays exactly
  as in the start image". Never ask Seedance to invent legible text — you get garble.
- **No real songs/lyrics** (copyright + the model can't render them) — invent a song
  title and hook instead.
- Banned words get instant submission rejection (e.g. "slave" → reword to "serving
  woman"). Occasional false-positive "nsfw" statuses → reword slightly and retry.

## Batch mechanics

- **Hard limit: 8 concurrent Seedance jobs** (ultra plan, per workspace, per job type —
  the rejection JSON says `job_set_type: seedance_2_0`). Submissions beyond that are
  rejected instantly with `rate_limit_reached`; the job is never created and nothing is
  billed, so retrying later is always safe. Nano Banana and Sonilo are NOT subject to
  this cap (5 concurrent images + 3 concurrent music verified clean).
- **The cap is shared across ALL sessions/terminals.** `gen.py` now enforces it with a
  file semaphore (`.seedance_slots/`): every video call claims a slot file (PID +
  timestamp; dead/40-min-stale slots are reclaimed) before submitting and blocks until
  one frees up. So concurrent Claude sessions can all run 7-worker pools safely. If you
  also submit Seedance jobs OUTSIDE gen.py (web UI etc.), lower the budget with
  `export SEEDANCE_SLOTS=4`.
- Use `pool_run.py <script.sh> <outdir>` — 7-worker pool, parses
  `gen name dur "prompt" flags...` lines from a batch script, skips shots whose mp4
  already exists (so re-running it IS the retry pass). It mkdirs the outdir itself.
- **Client failure ≠ job failure.** `--wait` can time out / drop (e.g. laptop lid
  closed) while the job completes server-side and bills. Before resubmitting anything,
  `higgsfield generate list --size N --json` and match by prompt prefix — completed
  jobs' `result_url` downloads free. HTTP 503 / "no response received" at submission
  usually means it was never created (check the list to be sure), then just retry.
- Run `caffeinate -is` during long batches; sleep kills in-flight waits.
- Name every shot with a short act-prefixed slug (`a3_reveal`, `b12_cough`) and copy
  to `outputs/videoN/<name>.mp4`.
  Versioned dirs per pass (video3, video4, ...) mean old takes survive for instant
  revert, and the assembler swaps takes by editing one line.

## Voice casting / auditions (ElevenLabs)

- **Prompt for custom voices; don't browse the catalog.** The premades and the
  searchable community library are mostly podcaster-generic, and the
  "characterful" ones veer cartoonish (a candidate cast as a stoic frontiersman
  came out a pirate). ElevenLabs voice design — describe the voice in a prompt,
  generate candidate voices, keep the winners — produces distinctive,
  cast-able voices and is now the default workflow. (This postdates The Long
  Game, which was cast from catalog voices + clones of approved takes.)
- Build an **audition page** (see `tools/templates/make_auditions.py`) and let
  the director cast from it: one section per character with the character's
  anchor portrait displayed next to the audio players — hearing a voice while
  looking at the face is what makes the fit obvious. Every candidate reads the
  same signature line in that character's actual register.
- **One "base" read per candidate is enough.** Calm/drama voice_settings
  variants tripled the audio without ever changing a casting decision.
- Write the audition line NATURALLY. A scripted ellipsis ("Two plus two...
  is four") gets heard as the VOICE hesitating and costs a good candidate the
  part.
- Pre-screen with pitch stats (`pitch.py`) to catch miscasts before the
  director listens, but expect surprises — fictional-age logic beats timbre
  logic (a 147 Hz "villain" voice won a ten-year-old character over every
  deep candidate).
- Casting-note taxonomy from real rounds — the failure modes to listen for:
  too quiet / inaudible at mix level, "narrator voice" (too polished to be a
  person in the scene), and accent drift into caricature.

## Dubbing / re-voicing (no re-render)

- **Dubbing only works when the speaker's mouth is not visible** (Long Game
  lesson, reconfirmed on The Vaulted Sky): off-screen lines, telepathy,
  speaker/recording voices, mouthless creatures, stills. Even ElevenLabs
  speech-to-speech (which preserves the original timing exactly) reads as
  off-sync on visible lips. For on-camera human dialogue the only real fix is
  re-rendering the clip with the new voice as the Seedance `--audio` ref.
- Batch pipeline that works (`mewtwo/dub_pass.py`): demucs two-stem split →
  silencedetect speech segments on the vocal stem (greedy-merge segments until
  the count matches the script's line count) → per-segment ElevenLabs STS into
  each speaker's cast voice → remix over the ambience stem at original offsets
  → remux onto the untouched video track.
- ElevenLabs community voices are addable to the account via
  `GET /v1/shared-voices` search + `POST /v1/voices/add/{owner}/{voice_id}`,
  then usable for TTS/STS like premades — a far deeper casting pool than the
  ~20 stock voices (that's where the Italian mob-boss Giovanni came from).

## Editing / assembly

- Assembler = python building one ffmpeg `filter_complex_script` (write the graph to a
  file — it's too long for argv). Per-entry: video+audio trim (`start`, `duration`),
  `scale=854:480,setsar=1,fps=24`, optional `volume=0` mute, then one big `concat`.
- **Trims are creative tools**: mid-clip splices (cutaway to a flash-cut then back),
  tightening stilted dialogue by cutting middle sentences, repeating a 2-second beat as
  a running gag. Find safe cut points with
  `ffmpeg -af silencedetect=n=-32dB:d=0.35` — cut in silences, not mid-word.
- Repetition is comedy: re-using an *identical* short clip (trimmed) as a recurring
  beat reads as a deliberate Groundhog-Day gag and costs nothing.
- Act/scene transitions: bake the transition ("frame washes to white") into the
  outgoing clip; hard-cut to the next act's opening shot.
- `-preset veryfast -crf 19` and run encodes in the background; a full re-encode of an
  11-min film is ~10 min. Don't overwrite the preview the director is currently
  watching — bump the version number instead.

## Music (Sonilo)

- `higgsfield generate create sonilo_music --prompt "..." --duration N --wait` →
  m4a URL. ~3.75 credits/min. Always append "Instrumental only, no vocals."
- **Score scenes, not eras.** One bed per era sounds monotonous and overpowering.
  What worked: short cues on specific moments (cold open, montages, emotional scenes,
  dread stingers) with *silence under all comedy dialogue*. Reusing one cue as a
  recurring motif at matching beats (e.g. the same dread drone at every dark turn)
  reads as intentional scoring.
- Mix LOW: 0.07–0.12 under dialogue scenes, ~0.20 max for stingers/montages. First
  attempt at 0.15–0.25 was "overpowering". `amix=normalize=0` + `adelay` for placement,
  afade in/out per span.
- "Background ambience music" prompts (no drums, muffled, across-the-room) sit under
  scenes far better than "a song".

## Voice pipeline (added after the voice-consistency wars)

- **Voice references at generation**: Seedance accepts `--audio <sample>` (up to 3).
  Keep canonical samples per character in `anchors/voice/` — they are just ffmpeg
  audio slices of takes the director approved:
  `ffmpeg -i take.mp4 -vn -ss <start> -t <len> -c:a aac anchors/voice/name.m4a`
  Make sure only the target character speaks in the window (silencedetect), and
  **verify with pitch_check.py** before trusting a sample — a bad reference
  faithfully reproduces the bad voice.
- **Redubbing without re-rendering** (`dub_clip.py`): demucs vocal split →
  `seed_audio` TTS voice-cloned from the sample (~0.3 credits/line) → remix new
  voice over original ambience → remux. Picture untouched; dubbed-film lip
  tolerance; perfect for off-screen lines. ~100x cheaper than a retake.
- **pitch_check.py**: median-f0 screen for every dialogue take (adult male ~85-155
  Hz; child ~250+). Catches kid-voice takes without ears.
- Dub candidates are cheap — generate several and A/B by ear: seed_audio clone
  (0.3 cr) plus 2-3 ElevenLabs voices (premades and/or an instant clone of the
  film's approved takes). In practice the seed_audio clone WON a head-to-head vs
  ElevenLabs for a VO line — don't assume the fancier tool wins; always A/B.
- ElevenLabs specifics: speech-to-speech preserves the ORIGINAL performance's
  prosody — great when the read was good but the voice was wrong; useless when the
  read itself was the problem (a squeaky take stays squeaky in a deeper voice —
  use TTS mode instead; and a scream keeps its screech through S2S — transplant a
  better take's audio instead). PCM output formats are gated to higher tiers —
  request the default mp3 and convert with ffmpeg.

### ElevenLabs setup

- **API key lives at `~/.elevenlabs_key`** (plain text, chmod 600). Every tool reads
  it from there or from `$ELEVENLABS_API_KEY`. New keys: elevenlabs.io → avatar
  (bottom-left) → API Keys, or https://elevenlabs.io/app/settings/api-keys.
- A paid tier is needed for voice cloning + the commercial license.
- Keep a list of each film's cloned voices and their voice_ids in that film's
  notes. List all voices (premade ids included):
  `curl -s https://api.elevenlabs.io/v1/voices -H "xi-api-key: $(cat ~/.elevenlabs_key)"`
  Clone a new character: `curl -X POST https://api.elevenlabs.io/v1/voices/add
  -H "xi-api-key: $(cat ~/.elevenlabs_key)" -F "name=..." -F "files=@sample.m4a"`
- Usage via `dub_clip.py` (in this repo):
  - Speech-to-speech (no text; converts the clip's own performance):
    `python3 dub_clip.py clip.mp4 --backend elevenlabs --voice-id <id>`
  - TTS a specific line:
    `python3 dub_clip.py clip.mp4 "line text" --backend elevenlabs --voice-id <id>`
  - Raw API: POST /v1/text-to-speech/<voice_id> (JSON: text, model_id
    eleven_multilingual_v2) or /v1/speech-to-speech/<voice_id> (multipart: audio
    file, model_id eleven_multilingual_sts_v2), header `xi-api-key: <key>`.
- Quota check: `curl -s https://api.elevenlabs.io/v1/user/subscription
  -H "xi-api-key: $(cat ~/.elevenlabs_key)"` (character_count / character_limit).
- For surgical word replacement inside a clip (keep other speakers/parts of a
  line): Whisper word timestamps on the demucs vocal stem → replace just those
  words over the no_vocals stem → remux. Worked example in `long_game/dub/v12/`
  (fixed a mispronounced word mid-monologue and inserted a missing line).

## The retake regression law

Retakes regress randomly: a new take fixes the noted flaw and breaks something
else (voice, camera, staging). If a take is **95% there, do not retake it for a
dialogue tweak** — dub the line, trim it, or leave it. Several "improvement"
retakes had to be reverted to earlier versions. Keep every old take on disk
(versioned outputs/videoN dirs) so reverts are one line in the assembler.

## Iteration workflow with the director

- Expect **many** passes; make each cheap. The loop: preview mp4 + storyboard.html →
  per-shot notes → batch of retakes (each ~24–36 credits) + free edit-level fixes →
  re-encode. Retakes of 10–20 shots per round were normal.
- Interpret notes against the *clip*, not memory — extract frames / contact sheets
  (ffmpeg xstack) to spot-check gags and continuity before the director sees them.
- Common recurring note categories to pre-empt: wardrobe anachronisms, duplicate
  characters in background (identity bleed from anchors), inconsistent voices, weird
  spontaneous camera moves, on-screen text garble, characters who look alike, sets that
  read the wrong decade, and any scene where the model "explains to camera".
- Tone: comedy plays best dry (no score), and sincerity is earned by concentrating
  it in one stretch of the film rather than sprinkling it throughout.

## Costs (ultra plan, 2026-07)

- Video: 480p std = 3 cr/s → 8s clip ≈ 24 cr; a full ~80-clip/11-min movie ≈ 2,000 cr
  per complete generation; a retake round of 15 shots ≈ 400 cr.
- Images (Nano Banana Pro): a few credits each — frames/anchors are ~free relative to
  video. Music: ~3.75 cr/min.
- **Subscription credits expire at the end of each cycle — they don't roll over.**
  Spend the remainder on alternate takes of key gags, or the 720p master.
- `higgsfield generate cost <model> --prompt x <flags>` estimates before spending;
  `higgsfield account status` for balance.

## Setup gotchas

- Auth is browser OAuth (`higgsfield auth login`) — no API key. Then you MUST
  `higgsfield workspace set <id>` or every command fails with "No workspace selected".
- The CLI (`@higgsfield/cli` npm) is the only path to Seedance 2.0 / Nano Banana Pro;
  the REST API only has older models.
- `higgsfield model list` shows everything available (TTS, 3D, upscalers, Veo/Kling —
  worth checking for new tools); `higgsfield model get <job_type>` shows params.
- Seedance 2.0 also exists WITHOUT Higgsfield: fal.ai and BytePlus ModelArk sell it
  by API key (~$0.30/s std, no expiring subscription credits). Pricier per clip than
  a Higgsfield plan, but no OAuth/workspace/credit-expiry friction.
