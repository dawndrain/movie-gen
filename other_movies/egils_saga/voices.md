# EGIL — voice candidates

Two pools, per MOVIE_LESSONS:
1. **Higgsfield `text2speech_v2` presets (elevenlabs variant)** — the primary
   dialogue pipeline: deterministic forever, TTS per line → Seedance `--audio`
   refs. Audition by generating one line per preset and running `pitch.py`.
2. **ElevenLabs (Dawn's account, key at `~/.elevenlabs_key`)** — narrator
   (mixed at assembly, never sent to Seedance), dubbing via `dub_clip.py`,
   and A/B alternatives.

## Measured preset pitches (animorphs_david auditions, reusable)

| preset  | median F0 | read                        |
|---------|-----------|-----------------------------|
| Wilder  | 68 Hz     | deepest male — EGIL first choice |
| Caspian | 82 Hz     | deep male — SKALLAGRIM      |
| Mark    | 105 Hz    | male mid                    |
| Andre   | 106 Hz    | male mid (IQR wide — expressive) |
| Kevin   | 140 Hz    | high male — BARD            |
| Sienna  | 165 Hz    | lower female — THORGERD     |
| Gia     | 167 Hz    | lower female                |
| Maya    | 208 Hz    | female                      |
| Quinn   | 208 Hz    | female/child-adjacent       |
| Ava     | 229 Hz    | female                      |
| Chloe   | 262 Hz    | high female                 |
| Zoe     | 262 Hz    | high female                 |
| Leo     | 267 Hz    | child register — EGIL CHILD |
| Harper  | 286 Hz    | highest                     |

Unmeasured presets worth auditioning for this film: Roman (proven villain =
Visser Three; EIRIK), Gideon (proven warm lead; THOROLFS), Harrison,
Arthur, Alistair, Sterling, Brooks, Julian, Sloane, Elena, Vesper, Nora,
Isabella, Tasha, Mabel, Vlad, Orion, Hugo.

## Proposed cast (first choice → alternates)

| Character   | Preset (Seedance dialogue)      | ElevenLabs (narr/dub/A-B)          |
|-------------|---------------------------------|-------------------------------------|
| NARRATOR    | — (assembly-mix only)           | George → Leif (Nordic) → Viking Bjorn |
| EGIL adult  | **Wilder** → Caspian            | Kaelen, Viking Bjorn                |
| EGIL child  | **Leo** → Quinn                 | —                                   |
| EGIL old    | Wilder (aged read via punctuation) | Bill                             |
| SKALLAGRIM  | **Caspian** → Roman             | Brian (deep resonant)               |
| KVELDULF    | audition Arthur/Harrison/Mark   | Bill (wise old)                     |
| THOROLF ×2  | **Gideon** → Julian, Brooks     | Harry (fierce warrior, young)       |
| HARALD      | audition Sterling/Alistair      | Adam (dominant firm)                |
| EIRIK       | **Roman** → Andre               | Bloodgrin (in account)              |
| GUNNHILD    | audition Sloane/Elena/Vesper    | Kristen (evil queen) → Elariel X    |
| ARINBJORN   | audition Harrison/Brooks        | Daniel (steady)                     |
| ATHELSTAN   | **Alistair**                    | **Henry** (royal, in account)       |
| THORGERD    | **Sienna** → Nora, Isabella     | Lily (velvety British)              |
| BRAK        | audition Tasha/Mabel            | Matilda                             |
| BARD        | **Kevin**                       | —                                   |

Pitch-spread sanity target: adult male leads 65–110 Hz, distinct ≥10 Hz
apart; women 165–230; child Egil 250+.

## ElevenLabs IDs

### Already in the account (premades + customs)
- George (storyteller, British) — `JBFqnCBsd6RMkjVDRZzb`
- Brian (deep resonant) — `nPczCjzI2devNBz1zQrb`
- Bill (wise, old) — `pqHfZKP75CvOlQylNhV4`
- Daniel (steady broadcaster, British) — `onwK4e9ZLuTAKqWW03F9`
- Adam (dominant, firm) — `pNInz6obpgDQGcFmaJgB`
- Harry (fierce warrior, young) — `SOYHLrjzK2X1ezoPC6cr`
- Callum (husky trickster) — `N2lVS1w4EtoT3dr4eOWO` (dark-horse Egil option)
- Henry (royal, elegant, old British) — `VRAN0xryQGUWtDuwToRv` (ATHELSTAN)
- Bloodgrin (British character voice) — `KTAbPR4QFlhaTpde6md8` (berserk/EIRIK)
- BrianRaspy — `lwGnQIn0Z9pl1SoUiXZ3`
- Lily (velvety British) — `pFZP5JQG7iQjIQuC4Bku`
- Matilda — `XrExE9yKIg1WjnnlVkGX`
- Alice (clear British) — `Xb7hH8MSUJpSbSDYk0k2`

### Shared library finds (add to account before use)
- **Viking Bjorn — Epic Medieval Raider** (Swedish, gravelly deep) —
  `ljo9gAlSqKOvF6D8sOsX`
- **Leif — Warm Nordic Storyteller** (Danish/Jutlandic) — `tJDFCHyviItsYF1qqToS`
- **Kaelen — Amateur Warrior** (rugged bass-baritone) — `10NkTYmU7tSz3Kkl3Lex`
- **Kristen — Cold Evil Queen Villain** — `Qbw4VpyUrHEG7NigKzty`
- **Elariel X — Epic Queen Ethereal** (British) — `ksryVoNAGZT8GxWCTiVm`
- **Torgrim — Explosive & Furious** (roaring; berserk screams/Ljot if used) —
  `ELt1673DDdqHyrE7h2ua`
- Oyvind — Deep, Calm & Trustworthy (Oslo accent) — `nhvaqgRyAq6BmFs3WcdX`

To add a library voice (needs public_owner_id — re-query first):
```sh
curl -s -G "https://api.elevenlabs.io/v1/shared-voices" \
  --data-urlencode "search=viking" -H "xi-api-key: $(cat ~/.elevenlabs_key)"
# then:
curl -X POST "https://api.elevenlabs.io/v1/voices/add/<public_owner_id>/<voice_id>" \
  -H "xi-api-key: $(cat ~/.elevenlabs_key)" \
  -H "Content-Type: application/json" -d '{"new_name": "Viking Bjorn"}'
```

## Audition results (measured 2026-07-10, see auditions.html to listen)

50 samples generated (`auditions.py`; re-run = retry; `auditions.py html`
rebuilds the page). Key medians and casting implications:

- **Egil = Wilder (70 Hz)** confirmed — deepest of the pool.
- **Thorolf: Gideon measured 74 Hz — too close to Egil and too dark for the
  golden brother. Recommend Brooks (106 Hz) or Julian (127 Hz) instead.**
- Skallagrim = Caspian (81 Hz), 11 Hz above Egil — distinct but ear-check
  the two in dialogue together; fallback Brian (EL, 99 Hz) for dubs.
- Eirik: Roman measured 127 Hz (less deep than his Visser Three menace
  suggested); Andre 112, Bloodgrin (EL) 95 — ear decides.
- Kveldulf: Mark (113 Hz) deepest; Arthur/Harrison/Bill all ~133-137 with
  more age in the timbre.
- Gunnhild: Sloane/Vesper/ElarielQueen cluster ~162 Hz, KristenQueen 180;
  Elena came out 235 — likely too bright for a witch-queen.
- Thorgerd: Isabella 158 / Nora 160 / Sienna 167 — all distinct from
  Gunnhild if she lands ≤165; pick by ear.
- Narrator: VikingBjorn 85 (gravel), LeifNordic 111 (warm Nordic), George
  128 (classic British storyteller).
- Vlad's IQR was 61-390 — a growly character voice, unstable pitch; only
  usable for flavor lines.

## Audition procedure (before locking anything)

1. One audition line per candidate — same line for all in a role, e.g.
   Egil: "I bared blue Dragvandill, who bit not the buckler. My tooth I bade
   bite him — best of swords at need."
   Narrator: "They called him Kveldulf — the Evening-Wolf. When the sun went
   down, no man would speak with him."
2. Higgsfield presets: `hf` TTS batch → `python3 ../animorphs_david/pitch.py auditions/`
   ElevenLabs: POST /v1/text-to-speech/<id> (model `eleven_multilingual_v2`).
3. Check pitch spread, then EAR-check the shortlist — pitch stats catch
   miscasts, not character. Per MOVIE_LESSONS: don't assume the fancier tool
   wins; A/B seed_audio clones vs ElevenLabs for any dub work.
