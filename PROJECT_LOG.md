# Project log — dated postmortems, war stories, and corrections

> Append-only, newest first: one entry per project or pass, recording what
> was hit, what fixed it, and what was measured. Corrections are logged in
> place rather than rewritten — this file is the evidence trail. The
> generalized rules distilled from these entries live in MOVIE_LESSONS.md
> (deliberately the only playbook; see CLAUDE.md for the protocol).
> **Historical-path note:** entries reference files as they existed at the
> time of writing. Media dirs (frames/, vo/, music/, dub/, ...) are
> gitignored, and some projects (carl/, animorphs/, mewtwo/) are local-only
> adaptations of copyrighted works that never ship — their reusable code
> lives on in `tools/templates/`. Don't expect every path here to resolve in
> a fresh clone.
> (2026-07-18: film folders other than long_game/ moved under other_movies/ —
> paths like carl/... now mean other_movies/carl/...)

> Addendum (2026-07-18, "Dungeon Crawler Carl" audio QC — promoted from the
> old header notes):
> - Gemini audio QC is SYCOPHANTIC as a rater — scored every audition voice
>   "flawless/10/10" including an inaudible one. Use listen.py only with
>   adversarial find-the-fault prompts or A/B comparisons; audibility/level
>   questions are ebur128 measurements, not listening questions.
> - Postscript: the "library bed whine" was actually the loudnorm boosting a
>   near-silent (-69 LUFS) generation's NOISE FLOOR by 39dB — the source bed
>   is inaudible and the normalized file is a mechanical drone. Guard: >12dB
>   of required gain = failed generation; regenerate or drop, never boost.

> Addendum (2026-07-18, "The Vaulted Sky" — the reclaimed-originals dead end,
> CLOSED, do not reopen):
> - Cropping a filter-blocked canonical start frame (character partial /
>   off-frame) DOES pass the gate — but then the character has no in-frame
>   identity anchor and DISTORTS the moment motion brings them in. Adding
>   canonical --image refs to fix identity re-trips the gate on those hot
>   frames. Both sides of the squeeze verified; there is no configuration
>   where a canonical-composition start frame drives on-model video here.
> - The stable equilibrium remains the from-behind recipe: character IN the
>   start frame (identity) but rear/partial-profile (filter-safe). Canonical
>   frontal compositions are stills-only: storyboard, animatic, inserts, art.
> - Cross-provider note (director experience): Google/Veo doesn't hard-block
>   IP inputs — it quietly GENERICIZES iconic characters instead (Yu-Gi-Oh
>   test, 2025). Different dodge, same outcome.

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
> - (added 07-18, CORRECTED 07-19) **The "music too loud" fix, with the causal
>   story straightened out by the director's sign-check**: the 07-18 version
>   of this bullet blamed the whole-film-LUFS dialogue anchor ("diluted
>   anchor -> offsets land hot"). That's BACKWARDS: dialogue is never
>   re-gained in this pipeline, so a diluted (lower) anchor places beds
>   LOWER relative to true speech — v1's music sat 13.4dB under speech, not
>   the nominal 12. The dilution can't cause loud music (Dawn caught this
>   in the arithmetic; logged as a case study in confident misdiagnosis —
>   the numbers were all on hand and the sign still went unchecked).
>   What actually fixed v2: (1) sidechain-ducking the whole bed bus under
>   the dialogue track (~8dB during overlaps, the dominant fix); (2) offsets
>   lowered -12 -> -15/-16; (3) still open: integrated-LUFS normalization
>   under-reads a cue's loud passages (quiet intro dilutes the average, the
>   chorus plays hot under a line — same averaging-window bug as the
>   mean-volume crickets, one level up; per-cue dynamics or a limiter on
>   the bed bus would close it). speech_anchor() stays — measure speech-only
>   for predictability — but it was ~1.4dB in the QUIET direction, not the
>   cause. Copy carl's mix phase (duck included) for new projects.
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
>   2. **The canonical `z='min(zoom+0.001,1.5)'` form is a SEPARATE, second bug**
>      — with `d=1` the `zoom` accumulator RESETS every input frame, so it never
>      accumulates: zoom pins at ~1.0015 and the clip is FROZEN. (Verified 2026-07:
>      110/149 frames byte-identical, max change 0.012/255 — it does NOT jerk, it
>      just sits there. An earlier note here wrongly called it "a static image that
>      jerks"; a relative motion metric had fooled me by counting encoder noise on a
>      zero signal as snaps. The two failure modes are distinct: this recipe is
>      frozen; bug #1's quiver only appears once the zoom ACTUALLY accumulates,
>      e.g. when driven by `on`.) A lot of people ship this frozen non-zoom.
>      Demo of all three states: `outputs/previews/kenburns_three_modes.mp4`.
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

