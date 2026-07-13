#!/bin/bash
# Walter's Deal — character anchors + machine anchor (Nano Banana Pro).
# Style lock in every prompt; characters 3:4, machine/locations 16:9.
cd /Users/dawndrain/Code/videogen
A=walters_deal/anchors; mkdir -p $A

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

img walter_young "Three-quarter length portrait of Walter, an early-20s scientist: lean, pale, short slightly tousled brown hair, round wire-rimmed glasses, a white lab coat worn open over a plaid flannel shirt and blue jeans. Earnest, sleep-deprived, socially awkward expression, faint shy half-smile. $STYLE" --aspect_ratio 3:4 &
img xave "Three-quarter length portrait of Xave Stern, a salesman around 45: short neat black hair, sharp gray suit with subtle stripes, bold red tie, black leather shoes, a gold pocket watch chain at his breast pocket. Confident charming salesman grin, calculating eyes. $STYLE" --aspect_ratio 3:4 &
img kristella "Three-quarter length portrait of Kristella Attenburg, a striking woman in her mid-20s: long chestnut brown hair, elegant black pantsuit with a wide cowl-neck top, a broad silver ring on one hand. Wry amused smile, adventurous bright eyes. $STYLE" --aspect_ratio 3:4 &
img jeremy "Three-quarter length portrait of Jeremy, a short scruffy man of about 20: messy sandy hair, a retro science-fiction fan club t-shirt under an open flannel shirt, jeans. Starstruck goofy enthusiastic grin. $STYLE" --aspect_ratio 3:4 &
img rick "Three-quarter length portrait of Rick Lorand, a mechanic around 40: full brown beard, blue work overalls with suspenders over a gray pullover, a blue flat cap, strong hands with faint engine grease. Humble, warm, practical expression. $STYLE" --aspect_ratio 3:4 &
wait

img booth "Product photograph of a handmade retro teleportation machine from the late 1980s: a human-sized cylindrical glass booth with a hinged glass door, its back and base completely swallowed by a frozen black fountain of hundreds of bundled black cables that spill onto the floor, connected to a separate small wooden console with rows of chunky switches and ONE prominent round blue button. Handmade garage-inventor aesthetic, slightly crooked, no LEDs, no modern design. Dim workshop lighting. $STYLE" --aspect_ratio 16:9 &
img isela "Three-quarter length portrait of Isela Mantorry, an imperious mayoress around 55: red hair drawn back into a tight knot, elegant black ankle-length dress with a V neckline, a small sparkling jewel necklace, silver wristwatch, thick tasteful makeup, green eyes with long lashes. Shrewd, calculating, aristocratic expression. $STYLE" --aspect_ratio 3:4 &
img bernand "Three-quarter length portrait of Bernand, a 14-year-old boy: mousy brown hair, a horizontally striped t-shirt, blue jeans, white sneakers. Cocky, attention-loving grin. $STYLE" --aspect_ratio 3:4 &
wait
echo ANCHORS_BASE_DONE
