# The Long Game — resume notes (updated 2026-07-10)

PUBLISHED: https://www.youtube.com/watch?v=q40M08SOhGs (upload master:
outputs/previews/youtube_v18_1080p.mp4). Dawn's earlier veo3 compilation:
https://www.youtube.com/watch?v=dbwaUy7mXAA

Current best cut: outputs/previews/preview_v17.mp4 · storyboard_v17.html
Dawn: "diminishing returns land" — treat v17 as near-locked.

## Done in v17 (2026-07-10)
- REVERTED a_hard cutaway + q2 native retake back to the dubbed takes (retakes
  came back with English accents despite --audio refs, Deshawn continuity bad).
  "Slightly awkward dubs" > retake regressions — Dawn's explicit call.
- KEPT q3_walk2 ("bro's still IN there" line is really good; Milo has a buzz cut
  and the physics is a bit weird, but net improvement).
- Lessons from this whole arc written to MOVIE_LESSONS.md addendum (accent drift,
  crowd creep, missing anchors, Hald LUT recipe, same-scene continuity playbook).
CREDITS ENDING IS NOW THE ENDING (Dawn: "definitely the better one"). Door
version retired at preview_v15.mp4; assemble_v16.py is the single assembler.

## Done in v16 (2026-07-10)
- a_smoke_stand2: Deshawn STANDING for the smoke line (was seated in v15 insert).
  Start frame frames2/f_deshawn_standing.png (nano-banana'd from a7_dibs frame).
  First retake re-added background kids -> "arcade is otherwise EMPTY" lock fixed it.
- q2_longtime3: native "I lived a long time", single shoulder clap, just the three
  friends (first retake grew a crowd — same empty-arcade lock needed).
- q3_walk2: Deshawn/Milo on-model (anchors were missing from the original gen),
  Cass walks forward now.
- q7→credits transition softened: video fade 0.8s + audio fade 0.6s (AFADE dict).

## Done in v15 (2026-07-10)
- t0 approved by Dawn; ending "really cool".
- r9 reverted to r9_acid3 per Dawn ("maybe the old one is actually better").
  acid4 (murmur echo) and acid5 (doodle insert) both still in outputs/video14/.
- b7 color finally right: histogram-matched to pooled b6/b1 bronze frames via a
  Hald CLUT (75% match / 25% identity blend), baked into
  video14/b7_name3_bronze.mp4 — no per-frame flicker, GRADE dict no longer used
  for it. Recipe: pool ref+src frame pixels -> per-channel CDF match -> apply LUT
  to haldclutsrc=8 identity PNG -> ffmpeg haldclut, -c:a copy.
- a_hard smoke-line dub replaced by a NATIVE CUTAWAY: 5s insert of Deshawn
  ("Ohhh - Cass wants the SMOKE!" + cackle, video14/a_smoke_insert.mp4, deshawn
  voice ref) spliced as three CUT entries: a_hard[0:2.70] + insert[0:3.95] +
  a_hard[5.60:]. No lip-sync problem because the lips are new.
Alt ending (Dawn leaning this way): preview_v14_alt_ending.mp4 — q7 plays dry,
dips to black, then outputs/credits.mp4: amber CRT cards (THE LONG GAME / ONE
CREDIT. ONE LIFE. / blinking INSERT COIN TO CONTINUE) over the cold-open hum +
music/mus_credits.m4a (ominous minor-key arcade chiptune, sonilo).
(historical cuts: storyboard_cut_v3..v10.html, storyboard_v9..v13.html)

## Done in v14 (2026-07-10) — second notes batch
- b8 retaken (dub was bad): "The Long Game" spoken natively, pan follows the
  villager's point and lands on the old woman outside her hut. (video14/b8_leave2)
- p2_board4: only ONE silver-haired man in the room; board stays "THE LONG GAME".
- r9_acid5: doodle-page insert (spiral, fish, stick figure, half-written misspelled
  "Sulfric") while Cass dictates — kills the Tertius lip-flap too. r9_acid4 (murmur
  attempt, has a "your skin" echo) also on disk if wanted.
- t0: approved "...Huh." tail spliced back from dub/t0_line.wav (the cut-off one
  is video13/t0_longgame). New file video14/t0_longgame.mp4.
- b7 grade retuned to the cold-blue early-bronze palette
  (eq=saturation=0.45,colorbalance=bs=0.12:bm=0.08:bh=0.06).
- m1 blanket phase-through: parked per Dawn's "eh".

## Done in v13 (2026-07-10) — Dawn's notes batch
- w1 "...Again." reverted to the child-voice take (video10/w1d).
- e3 "The vow" now plays dry; ren_b music enters at n5 (after "I will FLOOD...").
- n9_sixty3 retake: Cass visibly at the press in frame with the widow. (std)
- b7 "My name is Cass" graded grayer (GRADE dict in assembler: saturation 0.35).
- r9_acid3 retake: high-schooler chemistry ("It reacts with... nearly everything.
  Metals. Sugar. I want to say... salts?"). Tertius murmur gag not in this take.
- r8_glass2 retake: he can't improve glass ("...How do you MAKE glass, exactly?").
- "The Deep End" → "The Long Game" everywhere: t0 full-line seed_audio redub
  (video13/t0_longgame), b8 phrase splice (video13/b8_longgame, atempo 1.16),
  p2_board3 retake with regenerated chalkboard frame (frames2/f_p2_longgame.png).
- Watch-out: p2_board3 wide shot (~3s) has a background engineer who reads slightly
  Cass-like for a beat; recovers into a clean two-shot. Revert path: video5/p2_board2.

## Done in v18 (2026-07-11) — AMBIENCE PASS
- 8 beds via ElevenLabs /v1/sound-generation (22s each, ~3.4k EL credits),
  stitched to 300s seamless loops (acrossfade 1.5s) in ambience/*_loop.m4a.
- AMBIENCE list in assemble_v18.py: (start_stem, end_stem, bed, gain) — spans
  resolved from clip offsets at build time, beds faded 1.5s in/out, mixed with
  the music into the same amix.
- KEY GOTCHA (two rounds): (1) mean_volume is a BAD loudness proxy — spiky beds
  (crickets) read quiet on mean but loud to the ear. (2) ElevenLabs beds span
  -26 to -69 LUFS natively. THE FIX = LUFS workflow: two-pass loudnorm every
  bed to a common -30 LUFS (ambience/amb_*_n.m4a), measure the film's dialogue
  anchor with ebur128 (-22.4 LUFS), then volumes are plain dB offsets:
  featured beds -6dB (~-36 LUFS in-mix), background -10dB, library -14dB.
  Content notes: "electrical hum" reads as tinnitus (say "wash of distant game
  melodies, NO steady tone"); grassland prompts default to crickets (say "NO
  insects, NO crickets"). Loop repeat period = 20.5s — fine for steady
  textures, audible for distinctive events.
- ambience_sampler.mp4 = labeled 8s excerpts of every bed span for quick ear QC.
- GEMINI IS THE EARS NOW: ../listen.py (key ~/.gemini_key, gemini-3-flash-preview,
  audio inline) auditions any bed/mix. It caught: 15kHz whine baked into ALL
  ElevenLabs beds (fixed by lowpass 7k), tinnitus-arcade, furnace-basement baths,
  4 failed roman-street candidates (span dropped — native audio carries it),
  library bed that was literally nothing but artifacts (dropped). Workflow:
  generate bed -> listen.py verdict -> only PASS beds enter the mix -> final
  in-mix sampler audition. Final v18 config: arcade/baths -12dB, bronze (ends
  pre-party)/workshop/ren_city/1926 -16dB, all -30 LUFS normalized + EQ'd.
  Gemini verdict on the final mix: READY TO SHIP.
- Beds are textures only (hum/water/wind/murmur, "no sudden events" in the
  prompt) so they never fight Seedance's sparse native ambience; skipped
  boiler-yard, machine act, ski run where native SFX/music already carry it.
- storyboard_v18.html has an "Ambience beds" section with players per bed.
- Upload file: outputs/previews/youtube_v18_1080p.mp4.
- FOR NEXT FILM: scratch beds + scratch music at the ANIMATIC stage; ambience
  lives in the assembler as a layer, never baked into clips.

## Open items
- Endings: Dawn says alt "has more potential" — v14_alt is the reworked version
  (dry q7 → dip to black → CRT credits). Door version kept current in v14 too.
- Credits sequence is v1: cue choice, card timing, blink rate all tweakable free
  (outputs/credits_graph.txt + assemble). More cue candidates cheap via sonilo.
- q5_nested: crowd pointing/laughing reads unrealistic (KEEP Milo rolling on the
  floor — that part works); subtler crowd reaction. Retake, ~30cr.
- q8 end frame: Milo(?) looks off-model — clarify which figure Dawn means (the door
  person should be Deshawn).
- std-vs-fast head-to-head: credits topped up (3,278). Day-one pairs exist locally
  in outputs/video_720fast/ vs outputs/video/. Build side-by-side comparison, then
  resolve the conflicting fast/std guidance in MOVIE_LESSONS.md. (CLI `generate
  list` caps at 100, no pagination; do NOT read ~/.config/higgsfield/credentials.)
- a_hard_lipsync.mp4 (LatentSync demo) exists but NOT in the cut — Dawn lukewarm.
- Music: Dawn still unsure overall. Current design: sparse scene-matched cues, gags
  dry, warm 1926 cue cuts out at Peter's pitch. Untried: one recurring 4-5 note
  motif arranged per era (lyre → harpsichord → piano → synth).
- 720p std master render of the locked cut: ~2,000 credits.
- Credits expire at end of cycle — spend leftovers deliberately.

## Lessons this round (also in MOVIE_LESSONS.md)
- If a take is 95% there, DON'T retake it for a dialogue tweak — dub the line
  (0.3 cr) or live with it. Retakes regress randomly; several had to be reverted.
- Voice consistency: pass anchors/voice/*.m4a via --audio on every dialogue shot;
  verify new samples with pitch_check.py BEFORE using.
- Segment-surgery dubbing (Whisper word timestamps → replace exact phrase over
  no_vocals stem, atempo to fit the hole, volume-match) works well — see dub/v14/.
- For mid-sentence name swaps, TTS the WHOLE sentence for context, then crop just
  the phrase — natural prosody, no robotic isolated words.
- Renaming a prop: regenerate the frame with Nano Banana ("same scene, heading now
  reads exactly '...'"), then retake from that start frame with "the chalkboard
  exactly as in the start image, its writing unchanged the entire clip".
- fal.ai / BytePlus have Seedance 2.0 without Higgsfield (API key, no expiring
  credits, ~$0.30/s std — pricier per clip but no subscription games).
