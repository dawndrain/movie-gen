# THE VAULTED SKY — retake plan (post credit-reset)

Director's notes 2026-07-10 + accumulated known issues. All renders 480p std.
Current balance ~190 cr; full plan below ≈ 900–1000 cr.

## 1. Phantom / off-model Mewtwos (director note #1)
Cause: creature-lock text in prompts without a Mewtwo image ref (fixed in
make_videos_vs.py — NO_CREATURE set) + off-model hallucinations.
- a1 — fake baby Mewtwo in the abstract womb shot → retake, no creature
- a3 — emaciated alien cat in Eva's room → retake, no creature
- d4 — phantom Mewtwo among the scientists → retake, no creature
- f1 — pale tailed figure in quake room → retake, no creature
- title — cartoon Mewtwo in ocean + garbled text ("THE VAU TED SKY") → retake
- c1 — creature in drained pod reads xenomorph-ish → retake with mewtwo ref

## 2. Static clips (director note #2 — "a lot of nothing moving")
Measured by mean luma frame-diff; worst rendered offenders:
g7a (0.09), e4 (0.10), a2 (0.12), g6 (0.15), b3 (0.16), d2 (0.17),
d6a (0.18), c6 (0.22), e8 (0.22), a3 (0.26).
Fix in retake prompts: inject micro-motion — fluid convection + rising
bubbles in the pod, drifting dust, monitor flicker, visible breathing, tail
sway, rain streaks, and ALLOW a slow camera drift (drop "locked-off" for
these). Interim free fix: trim the static clips shorter in assembly.

## 3. Goofy fight (director note #3)
- g1 (the snatch) — blue rope-tail, donkey-kick pose, toy-dog weavile.
  Retake with rebuilt frame (already in frames2) + tightened action prompt.
  e6/e7 hold up on contact-sheet review.

## 4. Voices (director note #4)
- 35 lip-free clips adopted ElevenLabs dubs (Damien Mewtwo throughout).
- 12 on-camera-mouth clips kept original audio — dubbing fails on visible
  lips (Long Game rule). Re-render with cast ElevenLabs voice refs as
  --audio: b3, c3, d2, d3, d4, d5, d6a, e2, f2, f3, f6a, f8.
- Scientists (d1, sato/martin) stay on Higgsfield presets — director likes.
- Mewtwo voice: Damien provisional; round-3 adolescent/androgynous
  candidates on auditions.html (Merv, Cooper, Jocelyn, Archie, August,
  IanAlien, Jarvis, Adina). Possible split-register idea: robotic Jarvis for
  the SUIT-SPEAKER voice only (canon: Mewtwo picked his synthetic voice),
  organic androgynous voice for telepathy/inner.

## 5. Still-frame placeholders (never rendered)
a4, a6, a7, b1, d6b, f4a, f4b, g7b, h3, h5 — frames2 versions ready and
filter-safe; render with ElevenLabs --audio refs (new voices, natively
lip-synced where applicable).

## 6. Sabrina wardrobe
sabrina = alt_canon look now (white top / crimson wrap-skirt / red gloves);
teen anchor rebuilt to match. gym4_coat is the alt for Gym-Leader-era scenes
if the director wants era differentiation. All Sabrina-featuring retakes use
the new anchors; remaining old-tunic clips (c3, c4, c5, e1, e2, e5a/b, e6)
re-render only if wardrobe consistency is wanted film-wide (~8 shots).

## 7. Animatic round-2 notes (2026-07-11, all applied to animatic; carry into renders)
- a4: added "Four. ...Yes. Four." — the 2+2 mantra now visibly lands (canon ch28).
- a5: Fuji scene dramatized — he murmurs the lonely line aloud first; the
  projection answers. New fuji cast: Bill (animatic), recast properly later.
- b1b NEW SHOT: the voice-choosing scene (speaker install; first Carter words
  "This one. ...This one is mine.") — sets up the two-voice split on screen.
- e3: footprint deception now narrated (inner line); gag reads.
- f1: frame regenerated — Groudon properly described on the TV (was an
  Attack-on-Titan-looking humanoid; never describe a monster as "titan"
  without its species checklist).
- f5: frame regenerated with MODERN staff wardrobe ("mansion/estate" wording
  had dressed the crowd Victorian).
- h2: frame regenerated with the podback-recipe creature visible (was a
  generic merman-back).
- g7/g7b: split into two clear frames — empty hollow suit alone (g7a) /
  extreme CU violet eyes in the dark (g7b); kills the "second shadow
  mewtwo" confusion. g6's wrong-reflection is INTENTIONAL (Victory).
- h3: emotive re-read (low-stability take, Gemini-audited 9/10 "voice
  genuinely breaks"). listen.py QC loop works — use for every key read.
- All vo_el lines loudnormed to -16 LUFS (Giovanni was reading quiet).
- Giovanni Voice Design candidates on auditions.html (DsgnDon p1-3,
  DsgnVelvetBoss p1-3) — pick pending.

## Order of operations
1. Director locks Mewtwo voice (+ optional suit-voice split).
2. Regenerate ALL dialogue lines as ElevenLabs TTS (vo_el/) with natural
   phrasing; these become --audio refs for every re-render AND the dub
   source for any remaining lip-free swaps.
3. One pool_run batch: sections 1+2+3+5 + the 12 lip-sync shots (+ optional
   Sabrina wardrobe pass).
4. Whisper QC + motion audit + contact sheets.
5. Re-dub pass for anything still off; assemble preview_v3.
6. Remaining credits → 720p master of the locked cut.
