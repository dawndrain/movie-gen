#!/bin/bash
# Walter's Deal — derived anchors (same face as walter_young, aged/altered).
cd /Users/dawndrain/Code/videogen
A=walters_deal/anchors

STYLE="Photorealistic, shot on 35mm film, late-1980s Central-European look, muted colors, soft natural light, plain neutral gray studio background. No text or captions."

img() {
  local name="$1"; shift
  local out
  for attempt in 1 2; do
    out=$(./gen.py image "$@" 2>"$A/$name.err" | tail -1)
    if [ -f "$out" ]; then cp "$out" "$A/$name.png"; echo "OK $name"; return; fi
    sleep 5
  done
  echo "FAIL $name"
}

img walter_recluse "The EXACT SAME man as in the reference image — same face, same round wire-rimmed glasses — but six years older and fallen apart: an unkempt scraggly beard, wild overgrown hair springing out of his head like a fountain, dark rings under bloodshot eyes, a stained gray cardigan over a crumpled shirt, a cigarette between his fingers. Haunted, paranoid expression. Three-quarter length portrait. $STYLE" --aspect_ratio 3:4 --image $A/walter_young.png &
img walter_older "The EXACT SAME man as in the reference image — same face, same round wire-rimmed glasses — but twelve years older and composed: clean-shaven, short hair neatly combed with graying temples, a dark tailored suit with a subtle blue tie, a few lines of wisdom around tired eyes. Quiet, melancholy, dignified. Three-quarter length portrait. $STYLE" --aspect_ratio 3:4 --image $A/walter_young.png &
wait
echo ANCHORS_DERIVED_DONE
