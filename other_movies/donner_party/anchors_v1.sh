#!/bin/bash
# THE CUTOFF (Donner Party) — character anchors + location plates (Nano Banana Pro).
# Characters 3:4, locations 16:9. 5 concurrent max. Snow variants ref the base anchors.
cd /Users/dawndrain/Code/videogen
A=donner_party/anchors; mkdir -p $A

STYLE="Photorealistic, shot on 35mm film, 1846 American frontier period, muted earth tones, soft natural light, plain neutral warm-gray studio background. Authentic 1840s overland emigrant clothing, no modern fabrics, no zippers. He or she is the ONLY figure in the frame. ONE single continuous photograph filling the whole frame, no borders, no collage. No text or captions."
LSTYLE="Photorealistic, shot on 35mm film, 1846 American frontier period, muted earth tones, natural light. No modern objects, no roads, no power lines. ONE single continuous photograph filling the whole frame, no borders, no collage. No text or captions."
SNOW="the same person as the reference image, after a long starving winter in the mountains: hollow cheeks, wind-burned gray skin, cracked lips, exhausted sunken eyes, frost in the hair"

img() {
  local name="$1"; shift
  local out
  if [ -f "$A/$name.png" ]; then echo "SKIP $name"; return; fi
  for attempt in 1 2; do
    out=$(./gen.py image "$@" 2>"$A/$name.err" | tail -1)
    if [ -f "$out" ]; then cp "$out" "$A/$name.png"; echo "OK $name"; return; fi
    sleep 5
  done
  echo "FAIL $name"
}

# ---- main cast, TRAIL era ----
img james_reed "Three-quarter length portrait of James Reed, a proud 45-year-old Springfield businessman of 1846: dark hair, trimmed mutton-chop whiskers, fine black frock coat, silk vest with watch chain, white cravat, wide-brimmed black hat held at his side. Dressed a class above a wagon-train emigrant. Imperious, confident, slightly haughty expression. $STYLE" --aspect_ratio 3:4 &
img margaret_reed "Three-quarter length portrait of Margaret Reed, a 32-year-old emigrant mother of 1846: brown hair center-parted under a plain slat bonnet, gray wool dress with fitted bodice, fringed woolen shawl over her shoulders. Steady, warm, tired but resolute expression. $STYLE" --aspect_ratio 3:4 &
img virginia_reed "Three-quarter length portrait of Virginia Reed, a 13-year-old emigrant girl of 1846: long brown hair in two braids, simple calico print dress, straw hat hanging on her back by its ribbon. Bright, plain, unafraid expression. She is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img patty_reed "Three-quarter length portrait of Patty Reed, a small 8-year-old emigrant girl of 1846: dark hair, white pinafore apron over a brown homespun dress, both hands cupped protectively around a tiny carved wooden doll the size of a thumb. Solemn, self-possessed little face. She is the ONLY figure in the frame. $STYLE" --aspect_ratio 3:4 &
img george_donner "Three-quarter length portrait of George Donner, a 60-year-old farmer and wagon-train captain of 1846: thick white hair, kind heavy weathered face, brown sack coat over a red flannel shirt, dark trousers with braces. Gentle, honest, grandfatherly expression. $STYLE" --aspect_ratio 3:4 &
wait

img tamsen_donner "Three-quarter length portrait of Tamsen Donner, a 44-year-old schoolteacher of 1846: small and neat, dark hair in a tight bun, small round spectacles on a ribbon around her neck, navy blue wool dress with white collar, a leather journal held in both hands. Intelligent, composed, quietly skeptical expression. $STYLE" --aspect_ratio 3:4 &
img stanton "Three-quarter length portrait of Charles Stanton, a slight gentle 35-year-old bachelor of 1846: neat brown beard, mild kind face, gray wool sack coat, brown vest, a white clay pipe held loosely in one hand. Courteous, modest, quietly brave expression. $STYLE" --aspect_ratio 3:4 &
img breen "Three-quarter length portrait of Patrick Breen, a 51-year-old Irish emigrant farmer of 1846: gaunt weathered face, gray stubble, black slouch hat, patched brown greatcoat, a small worn leather prayer book in one hand. Devout, enduring, careworn expression. $STYLE" --aspect_ratio 3:4 &
img keseberg "Three-quarter length portrait of Lewis Keseberg, a tall 32-year-old German emigrant of 1846: blond hair, handsome cold angular face with high cheekbones, dark blue coat with brass buttons, black neckerchief. Controlled, aloof, unsettlingly calm expression. $STYLE" --aspect_ratio 3:4 &
img eddy "Three-quarter length portrait of William Eddy, a lean 28-year-old frontier carriage-maker of 1846: black hair, sun-darkened sharp face, fringed buckskin jacket over a linsey homespun shirt, powder horn strap across his chest, long flintlock rifle held upright at his side. Hard, capable, watchful expression. $STYLE" --aspect_ratio 3:4 &
wait

img mary_graves "Three-quarter length portrait of Mary Graves, a tall 19-year-old emigrant of 1846: dark hair loosely pinned, dark eyes, wine-red wool dress, gray blanket-shawl around her shoulders. Steady, clear-eyed, serious expression. $STYLE" --aspect_ratio 3:4 &
img luis_salvador "Three-quarter length portrait of TWO young Miwok men of 1846, vaqueros employed at Sutter's Fort in California, standing side by side: both with dark hair to the shoulders, one in a red-and-gray striped wool serape over a white work shirt, the other in a plain brown wool poncho over a faded blue work shirt, both in dark trousers. Calm, competent, dignified expressions. They are the ONLY two figures in the frame. $STYLE" --aspect_ratio 3:4 &
img clyman "Three-quarter length portrait of James Clyman, a leathery 54-year-old mountain man and trapper of 1846: long gray-streaked hair, deep sun-creased face, fringed and stained buckskin jacket, fur cap held in one hand. Grave, warning, seen-everything expression. $STYLE" --aspect_ratio 3:4 &
img snyder "Three-quarter length portrait of John Snyder, a burly 25-year-old ox-team driver of 1846: sandy hair, red face, rolled shirtsleeves over thick forearms, canvas trousers with braces, a coiled bullwhip in one fist. Hot-tempered, glowering expression. $STYLE" --aspect_ratio 3:4 &
img graves_sr "Three-quarter length portrait of Franklin Graves, a rawboned 57-year-old Vermont farmer of 1846: gray hair, long plain face, heavy homespun coat, thick knitted mittens tucked in his belt, large practical hands. Practical, dour, dependable expression. $STYLE" --aspect_ratio 3:4 &
wait

img murphy_woman "Three-quarter length portrait of Levinah Murphy, a 36-year-old widowed emigrant mother at the end of a starving mountain winter in 1847: thin hollow-cheeked wind-burned face, exhausted sunken eyes, gray-brown hair escaping a ragged knitted shawl worn over her head, layered ragged wool dress and quilt wrapped around her shoulders. Dazed, half-believing expression. $STYLE" --aspect_ratio 3:4 &
img prairie_train "A mile-long wagon train of white-topped covered wagons drawn by teams of oxen, winding through green spring prairie grass under a huge sky, families walking beside the wheels, loose cattle herded behind, 1846. Wide landscape. $LSTYLE" &
img salt_desert "A blinding white salt flat stretching to the horizon under a merciless sky, heat shimmer, distant island mountains floating in mirage, scattered abandoned covered wagons and ox bones far apart on the crust, 1846. Wide desolate landscape. $LSTYLE" &
img wasatch "A steep boulder-choked canyon in the Wasatch mountains dense with aspen and cottonwood tangles, a rough hacked path of fresh-cut stumps winding up it, covered wagons stalled nose to tail among the rocks, 1846. $LSTYLE" &
img truckee_lake "A dark cold alpine lake beneath a sheer granite mountain wall, the notch of a high pass above, storm clouds pouring over the crest like smoke, pines black along the shore, first snow dusting the ground, late October 1846. Wide brooding landscape. $LSTYLE" &
wait

img cabin_interior "The dim interior of a cramped 1846 log cabin buried in snow: low ceiling, ox-hide stretched overhead as a roof, a small fire in a stone hearth, a single grease-lamp on a rough plank table, quilts and sleeping children bundled along the walls, firelight the only light. $LSTYLE" &
img alder_tent "A makeshift winter shelter at Alder Creek 1846: a canvas tent reinforced with brush and pine boughs, buried to the ridgepole in deep snow, a smoke hole, a trampled snow path leading down into its dark entrance, gray falling snow, bare aspens. $LSTYLE" &
img summit_snow "A white ocean of snowdrifts high in the Sierra Nevada, snow ten feet deep, only the tops of pines showing as short dark brushes above the surface, wind-smoked crest of the pass above, iron-gray sky, 1846. Wide hostile landscape. $LSTYLE" &
img johnsons_ranch "A green foothill valley in California in January: wet emerald grass, oak trees, a low adobe ranch house with smoke from the chimney, wildflowers beginning, soft rain-washed light, 1847. $LSTYLE" &
img napa_porch "The porch of a modest California ranch house in May 1847: whitewashed posts, a small wooden table and chair set out on the boards, oak trees and green hills beyond, warm late-afternoon light, a jar of wildflowers on the table. $LSTYLE" &
wait
echo BASE_DONE

# ---- SNOW variants (ref the base anchors) ----
img margaret_snow "Three-quarter length portrait of $SNOW, wrapped in a heavy patched quilt over the same gray wool dress, the same slat bonnet now ragged. Steady and unbroken despite everything. $STYLE" --image $A/margaret_reed.png --aspect_ratio 3:4 &
img virginia_snow "Three-quarter length portrait of the same 13-year-old girl as the reference image, after a hard hungry mountain winter: thinner, tired, wind-burned cheeks, chapped lips, the same brown braids now frayed, wrapped in a heavy woolen blanket over the same calico dress. Worn but bright-eyed and unafraid. $STYLE" --image $A/virginia_reed.png --aspect_ratio 3:4 &
img tamsen_snow "Three-quarter length portrait of $SNOW, the same tight bun and spectacles on a ribbon, wrapped in a dark shawl and blanket over the same navy dress. Composed, resolute, already decided. $STYLE" --image $A/tamsen_donner.png --aspect_ratio 3:4 &
img breen_snow "Three-quarter length portrait of $SNOW, the same black slouch hat and patched greatcoat now frost-rimmed, the prayer book clutched against his chest. Enduring, prayerful. $STYLE" --image $A/breen.png --aspect_ratio 3:4 &
img keseberg_snow "Three-quarter length portrait of $SNOW, the same blond hair now long and matted, beard grown in, wrapped in a dark buffalo-hide robe over the same blue coat with brass buttons. Eerily calm, unreadable. $STYLE" --image $A/keseberg.png --aspect_ratio 3:4 &
wait

img eddy_snow "Three-quarter length portrait of $SNOW, the same buckskin jacket scoured pale by wind, a wool blanket tied around his shoulders with cord, snow-blind squint, frost in his black hair. Grim, unstoppable. $STYLE" --image $A/eddy.png --aspect_ratio 3:4 &
img mary_snow "Three-quarter length portrait of $SNOW, the same wine-red dress faded and ragged at the hem, gray blanket-shawl pulled over her head, improvised rawhide snowshoe held in one hand. Clear-eyed and steadier than the men. $STYLE" --image $A/mary_graves.png --aspect_ratio 3:4 &
img stanton_snow "Three-quarter length portrait of $SNOW, the same gray sack coat frost-rimmed, eyes weak and unfocused from snow-blindness, the same white clay pipe held calmly in one hand. Gentle, serene, at peace. $STYLE" --image $A/stanton.png --aspect_ratio 3:4 &
img george_snow "Three-quarter length portrait of the same 60-year-old man as the reference image, after a long winter dying in a mountain tent: hollow-cheeked, gray-skinned, white hair long and unkempt, lying propped against rolled quilts, his right hand and forearm wrapped in stained linen bandages, blankets to his chest. Weak but calm, eyes still kind. $STYLE" --image $A/george_donner.png --aspect_ratio 3:4 &
wait
echo ANCHORS_DONE
