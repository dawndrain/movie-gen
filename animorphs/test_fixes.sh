#!/bin/bash
# Experiment: voice/pronunciation lock via TTS audio refs, torso lock, acted delivery.
# Run from repo root: bash animorphs/test_fixes.sh
set -e
cd "$(dirname "$0")/.."
mkdir -p animorphs/outputs/hbtest animorphs/vo

tts() { # name voice_id text
  local out="animorphs/vo/$1.mp3"
  [ -f "$out" ] && { echo "skip tts $1"; return; }
  local url
  url=$(higgsfield generate create text2speech_v2 --prompt "$3" \
        --variant elevenlabs --voice_id "$2" --voice_type preset --wait 2>&1 \
        | grep -oE 'https://[^ ]+\.(mp3|m4a|wav)[^ ]*' | tail -1)
  [ -n "$url" ] && curl -s -o "$out" "$url" && echo "tts $1 ok" || echo "tts $1 FAIL"
}

# Dak = Gideon, Aldrea = Imogen (placeholders — audition and swap freely)
tts dak_h1 "1ad38ba4-9cc4-4f2f-9fde-b0fefdf67ae5" \
  "Aldrea. The sun rises. Your two hours..."
tts aldrea_h1 "3811e986-0891-47cf-a1f5-78a1d62a547a" \
  "Passed long ago, Dak Hamee. I am Hork-Bayjeer now. Your people are my people. Your fight is my fight."

NEG="Photorealistic epic sci-fi film, natural creature motion, correct anatomy. No random camera moves. No text or captions. Only characters visible on screen speak. Characters keep exactly the same bodies, faces, blades and colors as in the reference images."
HB="Species lock: Hork-Bajir are seven-foot bipedal aliens with leathery green-brown skin, a crest of bone blades raked back from the skull, curved blades on forearms, elbows and knees, a spiked tail, and a hawk-beaked gentle face."

gen() { # name dur ... (passthrough)
  local name="$1" dur="$2"; shift 2
  local out
  out=$(./gen.py video "$@" --resolution 480p --std --duration "$dur" 2>"animorphs/outputs/hbtest/$name.err" | tail -1)
  [ -f "$out" ] && cp "$out" "animorphs/outputs/hbtest/$name.mp4" && echo "OK $name" || echo "FAIL $name"
}

gen h1_tts 12 "Sunrise between them. The wounded male Hork-Bajir speaks first, then the blue-sheened female answers. They speak EXACTLY the dialogue heard in the reference audio clips, lip-syncing to them precisely: the male speaks the first audio clip (male voice), the female answers with the second audio clip (female voice). Their voices are exactly the voices in the reference audio. He dreads the answer; she is calm, resolved, gentle. Their foreheads touch at the end, blades carefully apart. ${HB} ${NEG}" \
  --start-image animorphs/frames/h1.png --image animorphs/anchors/dak.png --image animorphs/anchors/aldrea_hb.png \
  --audio animorphs/vo/dak_h1.mp3 --audio animorphs/vo/aldrea_h1.mp3 &

gen a3_torso 6 "The young Andalite female gallops at full stride along the grassy ridge above the colossal-tree valley, golden light. CRITICAL anatomy lock, never violated: she is a centaur with SIX limbs — four deer legs on the ground AND an upright humanoid torso with two slender arms and a head rising vertically from the shoulders of the four-legged body. The upright torso, arms and head stay clearly visible above the galloping legs in every single frame; she is never a simple four-legged deer. Her long tail with its scythe blade streams behind. Medium-close side tracking shot keeping her whole body large in frame. Hooves drumming, wind. No dialogue. ${NEG}" \
  --start-image animorphs/frames/a3.png --image animorphs/anchors/aldrea.png &

gen e1_acted 12 "Storm-grey morning argument, performed with raw naturalistic emotion, not recited. The young female Andalite leans toward the Hork-Bajir, her telepathic voice urgent and pleading, cracking with grief for her dead family: 'The Yeerks take bodies, Dak. They will take every Hork-Bajir in the world unless we fight.' A long pause. Dak turns half away, gripping the bark so hard it splinters; he answers slowly, torn, almost a whisper, shame and fear in his voice: 'Hork-Bajir do not fight. Hork-Bajir do not even have a word... for war.' Aldrea steps closer; a beat of silence; then quiet, hard, resolute: 'Then we will teach them one.' Voice lock: Aldrea's telepathic voice is a clear young formal female voice heard while her mouthless face stays still; Dak speaks aloud, deep, warm, gravelly. ${HB} ${NEG}" \
  --start-image animorphs/frames/e1.png --image animorphs/anchors/dak.png --image animorphs/anchors/aldrea.png &

wait
echo TESTS_DONE
