"""Canonical style + wardrobe/appearance locks for HOME SAPIEN.

Imported by make_images.py (anchors) and frames_spec.py (start frames) so the
two can never drift. Reuse these strings VERBATIM in Seedance clip prompts too
— restating the full lock in every prompt is what keeps identity stable.
"""

STYLE = (
    "Photorealistic cinematic film still from a warm, handmade, slightly "
    "whimsical indie feature — 35mm, shallow depth of field, soft golden "
    "practical light, gentle film grain, tactile textures of wool, wood, "
    "paper and skin. Storybook warmth, never clinical, never chrome, never "
    "sci-fi blue. Sincere and a little funny. No text, no watermark, no "
    "captions, no subtitles. ONE single continuous photograph filling the "
    "whole frame, no borders, no collage, no split screen."
)

# Cosmic/creature shots share a painterly, hand-mixed look so they sit in the
# same world as the kitchen — no Hubble photorealism.
COSMIC = (
    "Painterly, hand-mixed, tactile cosmos — like ink and glitter suspended "
    "in water, warm amber and deep teal, not a photographic telescope image. "
    "Intimate rather than epic. No text, no watermark, no captions. ONE "
    "single continuous image filling the whole frame, no borders, no collage, "
    "no split screen."
)

# Creatures MUST be photoreal living animals. The words "handmade / tactile /
# wool" in STYLE bled into the first fish + monkey anchors and produced KNITTED
# FELT PUPPETS — charming, but a completely different film from the photoreal
# humans. Creature-only frames use this instead of STYLE.
CREATURE = (
    "Photorealistic wildlife cinematography — a real living animal, real wet "
    "skin, real fur, real eyes, natural history documentary realism, shot on "
    "35mm with a long lens, warm golden natural light, shallow depth of "
    "field, gentle film grain. Absolutely NOT knitted, NOT felt, NOT wool, "
    "NOT a puppet, NOT a plush toy, NOT clay, NOT a cartoon, NOT an "
    "illustration — a real photographed animal. No text, no watermark. ONE "
    "single continuous photograph filling the whole frame, no borders, no "
    "collage."
)

# FACE-ONLY locks — identity WITHOUT wardrobe.
#
# Use these (never W[...]) whenever the character is out of their normal clothes:
# the wedding, the period shots, any costume. The W[...] strings END with the
# wardrobe ("wearing a soft coral-orange knitted cardigan... faded jeans"), so
# "{W['may']} in a wedding dress" literally asks for a cardigan AND a dress in
# one sentence — and the cardigan wins. She turned up to her own wedding in a
# cardigan and jeans because of exactly this.
FACE = {
    "may":
        "a warm, funny woman of about thirty-two with EXACTLY the same face as "
        "the reference image — the same dark curly shoulder-length hair, the "
        "same freckles, the same laugh lines and the same enormous "
        "uncontrollable grin",
    "ollie":
        "a tall soft-featured gentle man of about thirty-four with EXACTLY the "
        "same face as the reference image — the same messy light-brown hair, "
        "the same round wire glasses, the same slightly startled kind face and "
        "stubble",
}

# The film's two rules, restated in the prompts that need them:
PAIR = (
    "The pair are always colour-coded: one of them is warm coral-orange, the "
    "other is cool teal-blue. They are the ONLY two in the frame."
)

W = {
    "may":
        "a warm, funny woman of about thirty-two with dark curly shoulder-"
        "length hair, freckles, laugh lines and an enormous uncontrollable "
        "grin, wearing a soft coral-orange knitted cardigan over a cream "
        "t-shirt, faded jeans, and bare feet",
    "ollie":
        "a tall soft-featured gentle man of about thirty-four with messy "
        "light-brown hair, round wire glasses, a slightly startled kind face "
        "and stubble, wearing a rumpled teal-blue button-down shirt with the "
        "sleeves rolled up and grey jeans",
    "may_old":
        "the same woman aged to about seventy-five — the same freckles, the "
        "same laugh lines now deep, the same enormous grin, her curly hair "
        "now silver-white and short, wearing the same soft coral-orange "
        "knitted cardigan, now visibly worn and mended, over a cream blouse, "
        "and bare feet",
    "ollie_old":
        "the same man aged to about seventy-seven — the same round wire "
        "glasses, the same kind startled face, now thin white hair and a "
        "lined face, slightly stooped, wearing the same teal-blue button-"
        "down shirt, now faded and soft with age",
    "may_sapien":
        "a woman with EXACTLY the same face as the reference — the same "
        "freckles, the same enormous grin, the same dark curly hair, now "
        "matted and tied back with sinew — living forty thousand years ago: "
        "warm red-ochre paint in stripes across her cheekbones, wearing "
        "soft hide and fur clothing with a rust-orange ochre-dyed hide wrap "
        "across one shoulder, bone beads at her throat",
    "ollie_sapien":
        "a man with EXACTLY the same face as the reference — the same soft "
        "startled kind features, the same stubble, the same messy light-"
        "brown hair, now long and tangled (no glasses) — living forty "
        "thousand years ago: blue-grey clay markings on his forehead, "
        "wearing rough hide clothing with a plain teal-grey fur cloak over "
        "his shoulders. The cloak is a PLAIN CUT PANEL OF FUR ONLY — it has "
        "NO animal head, NO animal face, NO eyes, NO ears, NO snout, NO paws "
        "and NO tail attached to it anywhere; it must never look like a whole "
        "dead animal draped over him, only like a piece of worked hide",
    "kid":
        "a small round-faced four-year-old girl with wild dark curly hair "
        "exactly like her mother's, wearing a mustard-yellow t-shirt and "
        "spotty leggings, permanently mid-sprint",
    "kitchen":
        "a small shabby beloved kitchen at one in the morning — worn yellow "
        "lino floor, mismatched wooden chairs, a kettle on the hob, one warm "
        "tungsten pendant lamp, crowded shelves, a fridge covered in "
        "postcards and magnets, and one window of deep blue night",
}
