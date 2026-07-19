# THE BUSY BODY — voice casting (ElevenLabs, Dawn's account)

Full raw list in `elevenlabs_voices.json` (fetched 2026-07-10, 31 voices).
Pipeline: TTS each line → per-speaker mp3 → Seedance `--audio` ref (clones the
voice). Audition the whole cast in ONE batch and pitch-check (pitch_check.py /
animorphs pitch.py) before committing — spread median F0 so all ten speakers
read distinct (David-trilogy spread was 82–208 Hz for 8 speakers).

British premades are scarce (4 male + 2 female usable), so they go to the
biggest parts; American-accent picks carry an accent note — the Seedance
voice-lock line ("speaks in a period English accent") plus the cloned timbre
usually lands it, but audition first.

## Primary casting

| Character | Voice | voice_id | Why |
|---|---|---|---|
| **Marplot** (comic lead) | Callum — Husky Trickster | `N2lVS1w4EtoT3dr4eOWO` | Literally tagged "trickster", characters/animation use-case; eager, husky, breathless energy. American — needs the accent lock. |
| **Sir George Airy** (gallant, 24) | George — Warm, Captivating Storyteller | `JBFqnCBsd6RMkjVDRZzb` | British, warm, confident; the name is a bonus omen. |
| **Charles** (earnest, 21, plays Don Diego) | Daniel — Steady Broadcaster | `onwK4e9ZLuTAKqWW03F9` | British, steady, earnest; reads younger with faster pacing. Also carries the Spanish-accented "Don Diego" lines (write them phonetically). |
| **Miranda** (witty heroine) | Lily — Velvety Actress | `pFZP5JQG7iQjIQuC4Bku` | British, confident, velvety — built for the asides and the con. |
| **Isabinda** (imprisoned heroine) | Alice — Clear, Engaging | `Xb7hH8MSUJpSbSDYk0k2` | British, clear; contrasts cleanly with Lily. |
| **Sir Francis Gripe** (miser, 65) | Henry — royal, elegant, precise diction | `VRAN0xryQGUWtDuwToRv` | Old + British + formal; add the wheezy "he, he, he" in the TTS text. |
| **Sir Jealous Traffick** (blustering father) | Bloodgrin | `KTAbPR4QFlhaTpde6md8` | Intense middle-aged British character voice — the bellowing "by St. Jago!" tyrant. |
| **Patch** (scheming maid) | Laura — Enthusiast, Quirky Attitude | `FGY2WhTYpPnrIDTdsKH5` | Sassy, quick — the improviser. American; accent lock needed. |
| **Whisper** (footman) | Will — Relaxed Optimist | `bIHbv24MWmeRgasZH58o` | Light, unassuming; he whispers anyway — accent barely surfaces. |
| **Scentwell** (maid, small part) | Jessica — Playful, Bright, Warm | `cgSgspJ2msm6clMCkdW9` | Bright contrast to Laura's Patch. |

## Alternates / swaps to audition alongside

- **Marplot alt**: Chris (`iP95p4xoKVk53GoZ742B`, charming down-to-earth) if
  Callum reads too gravelly; or Liam (`TX3LPaxmHKxFdv7VOQHJ`) for a younger,
  yappier Marplot.
- **Sir Francis alt**: Bill (`pqHfZKP75CvOlQylNhV4`, old, crisp — American) if
  Henry is too grand and not creaky enough. Henry is `generated`-category —
  verify he TTSes consistently before locking.
- **Sir Jealous alt**: Kevin Elliott (`MJyi2qJnZ6cONaNAgdKu`, professional
  British) played angry — if Bloodgrin is too monster-movie.
- **Charles alt**: Kevin Elliott, or Callum if Marplot moves to Chris.
- **Patch alt**: Matilda (`XrExE9yKIg1WjnnlVkGX`, upbeat).
- **Miranda/Isabinda swap** is the fallback if Lily and Alice sit too close in
  pitch — check F0 separation first.
- **Sarah** (`EXAVITQu4vr4xnSDxMaL`) held in reserve for either heroine.
- Existing clone "Cass (Long Game clone)" (`ioiKECc02TnNzxlXEDw8`) is free
  continuity if you want a cameo voice, but casting her as a principal makes
  cross-film characters collide.

## Higgsfield presets (plan B / mix-in)

`hf voices list` shows 42 text2speech_v2 elevenlabs-variant presets (Tallulah,
Roman, Sterling, Alistair, Gideon, Imogen, Vesper, ...). These are what the
animorphs films cast from and are deterministic forever. If any ElevenLabs
premade disappoints, pitch-audition presets — Alistair/Gideon/Arthur sound
promising on name alone for the two old men, Imogen/Vesper for the heroines.
(Starter-tier ElevenLabs quota is finite; ~38 shots of dialogue fits
comfortably, but presets are quota-free.)

## Audition results (2026-07-10 — see auditions.html, median F0 per take)

- whisper/Will 96 · francis/Henry 114 · marplot/Callum 122 · george/George 144 ·
  charles/Daniel 149 · jealous/Bloodgrin 160 · scentwell/Jessica 185 ·
  miranda/Lily 195 · patch/Laura 219 · isabinda/Alice 240
- **Collision: George (144 Hz) vs Charles-as-Daniel (149 Hz)** — 5 Hz apart and
  they share half their scenes. Recommended fix: cast Charles = Kevin Elliott
  (88 Hz, British) — max separation, and his Don Diego lines gain gravitas.
  Runner-up: keep Daniel and simply listen whether timbre separates them.
- Miranda/Lily (195) vs Scentwell/Jessica (185) are close but share almost no
  dialogue; acceptable.
- Everything else is well spread (88–240 Hz across ten speakers if Kevin
  Elliott takes Charles).

## Audition batch (run before generating any clips)

One line each, in character, through the primary + alternate voices:

- Marplot: "I'm as secret as a priest when I'm trusted — oh, how I love the little miniatures of man!"
- George: "The garden gate — at eight! There must be a meaning in this."
- Charles: "Rascals, retire — she's my wife; I'll make dogs-meat of you."
- Miranda: "Now methinks there's nobody handsomer than you — so neat, so clean. Faugh, how he stinks of tobacco!"
- Isabinda: "Where is he? Oh, let me fly into his arms!"
- Sir Francis: "She has nicked you, Sir George! He, he, he. Out of my doors, you dog!"
- Sir Jealous: "By St. Jago — hell and furies, a man in the closet!"
- Patch: "It is a charm for the toothache — 'twas given me by an angel!"
- Whisper: "Trifle, sir — the very lap-dog my lady lost!"
- Scentwell: "This way, sir — through many a dark passage and dirty step."

TTS call:
```
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/<voice_id>" \
  -H "xi-api-key: $(cat ~/.elevenlabs_key)" -H "Content-Type: application/json" \
  -d '{"text": "<line>", "model_id": "eleven_multilingual_v2"}' \
  -o auditions/<char>_<voice>.mp3
```
Then median-F0 the batch and check the spread before locking the cast.
