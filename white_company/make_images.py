#!/usr/bin/env python3
"""Generate White Company anchors, shot frames and title cards via Nano Banana.

Usage: python3 make_images.py anchors|frames|cards|all
Skips images that already exist, so re-running is the retry pass.
Nano Banana is not subject to the seedance slot cap; 5 workers is safe.
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROJ = Path(__file__).parent
GEN = PROJ.parent / "gen.py"
ANCHORS_DIR = PROJ / "anchors"
FRAMES_DIR = PROJ / "frames"
CARDS_DIR = PROJ / "cards"

STYLE = ("Photorealistic cinematic film still from a live-action 1360s medieval "
         "historical epic, natural light, ONE single continuous photograph filling "
         "the whole frame, no borders, no collage, no text, no captions, no "
         "watermark. Strictly 14th-century period accurate: no modern clothing, "
         "objects, or buildings.")

PORTRAIT = ("Full-length character portrait for a film, standing head to toe "
            "against a plain neutral warm-gray studio backdrop, even soft light. ")

W = {  # wardrobe/appearance locks, reused verbatim in anchor + frame prompts
    "alleyne": "Alleyne: a slim 20-year-old man with golden shoulder-length hair, clear gray eyes and a gentle boyish face with a firm chin, wearing a sombre dark-brown medieval clerk's jerkin, cloak and hose, a leather scrip on a strap and an iron-shod wooden staff",
    "alleyne_squire": "Alleyne the squire: the same slim golden-haired gray-eyed young man, now in chain mail with a snow-white surcoat bearing a red upright lion, an open-faced steel bassinet under his arm",
    "john": "Hordle John: an enormous red-headed giant of a man, nearly seven feet tall, freckled face, neck ruddy and corded, in coarse ill-fitting homespun tunic and hose bursting at every seam",
    "john_archer": "Hordle John the archer: the same enormous red-headed giant, now in a steel cap, chain mail and a snow-white surcoat with a red upright lion, a huge yellow yew longbow in one hand",
    "aylward": "Sam Aylward: a burly, massively broad-chested English archer of forty, shaven weather-beaten face as brown as a hazelnut with a long white scar from the left nostril to the jaw, wearing a dinted steel cap with a sprig of yellow broom, a chain-mail brigandine, a white surcoat with a red upright lion, a straight sword at his belt and a long yellow yew war-bow over his shoulder",
    "nigel": "Sir Nigel Loring: a very small, slight, middle-aged knight, completely bald with a little pointed gray-streaked beard and mild bulging near-sighted eyes, wearing a plum-purple velvet cote-hardie and a velvet cap with a lady's small white doeskin glove pinned to its front and a curling ostrich feather",
    "nigel_war": "Sir Nigel Loring in war harness: the same very small, slight, bald middle-aged knight with pointed gray beard and mild bulging eyes, in gleaming white plate armor with white ostrich plumes on his bassinet, his shield blazoned with five scarlet roses on a silver-white field",
    "maude": "Lady Maude: a tall, slender young woman with jet-black hair gathered under a light pink coif, dark eyes, a proud poised bearing, wearing a fitted medieval gown of faded rose slashed with pink, a small brown falcon perched on her red-gloved wrist",
    "maude_castle": "Lady Maude in a long sweeping medieval gown of black Bruges velvet with delicate white lace at the neck and wrists, her jet-black hair loose",
    "lady_mary": "Lady Mary Loring: a tall, broad, commanding older lady with a large square ruddy face and fierce thick brows, in a rich dark medieval gown and white wimple",
    "socman": "the Socman of Minstead: a powerfully built Saxon man with long flowing golden hair and a great yellow beard, a handsome lion-like face with fierce wild blue eyes, in a russet Norwich-cloth tunic",
    "simon": "Black Simon: a gaunt, spare, long-limbed man-at-arms with a fierce deep-lined face framed in a steel mail coif, carrying a lance with a small square guidon of five scarlet roses on white",
    "oliver": "Sir Oliver Buttesthorn: a hugely fat, red-faced middle-aged knight with black curls, in a dandyish olive-green medieval doublet picked out with pink, gold-hued pointed shoes",
    "chandos": "Sir John Chandos: a very old but ramrod-straight tall knight with snow-white curling hair to his shoulders, a fierce hawk-like clean-shaven face with a long thin wisp of white moustache, one bright eye and the other closed by an old scar, in an elegant dark surcoat over mail",
    "prince": "Edward the Black Prince: a slim dark-haired young man with clear, well-chiselled noble features, in a plain dark-blue jupon tagged with gold buckles and pendants, no crown",
    "duguesclin": "Bertrand du Guesclin: a hugely broad-shouldered, burly French knight with crisp curly black hair and a memorably ugly face - pale green eyes, a flattened broken nose, skin seamed with old scars - wearing a black jerkin trimmed with sable fur and a black velvet cap with a curling white feather",
    "tiphaine": "Lady Tiphaine: a stately, grave woman of thirty-five with an aquiline nose, dark curving brows, deep-set brilliant eyes and a broad white brow, a chaplet of pearls in her black hair, a silver gauze net flowing over her shoulders, swathed in a black mantle with a small silver cross",
    "abbot": "the Abbot: a thin, ascetic old monk with a gray thought-worn face, sunken haggard cheeks and long white nervous hands, in a white Cistercian habit",
}

ANCHORS = [
    # (name, prompt, refs, aspect)
    ("alleyne", PORTRAIT + W["alleyne"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("john", PORTRAIT + W["john"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("aylward", PORTRAIT + W["aylward"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("nigel", PORTRAIT + W["nigel"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("maude", PORTRAIT + W["maude"] + ". She is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("lady_mary", PORTRAIT + W["lady_mary"] + ". She is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("socman", PORTRAIT + W["socman"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("simon", PORTRAIT + W["simon"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("oliver", PORTRAIT + W["oliver"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("chandos", PORTRAIT + W["chandos"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("prince", PORTRAIT + W["prince"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("duguesclin", PORTRAIT + W["duguesclin"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("tiphaine", PORTRAIT + W["tiphaine"] + ". She is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    ("abbot", PORTRAIT + W["abbot"] + ". He is the ONLY figure in the frame. " + STYLE, [], "3:4"),
    # era variants, generated from the base anchor as reference
    ("alleyne_squire", PORTRAIT + "The same young man as the reference image, exactly the same face and golden hair. " + W["alleyne_squire"] + ". He is the ONLY figure in the frame. " + STYLE, ["alleyne"], "3:4"),
    ("john_archer", PORTRAIT + "The same giant man as the reference image, exactly the same face and red hair. " + W["john_archer"] + ". He is the ONLY figure in the frame. " + STYLE, ["john"], "3:4"),
    ("nigel_war", PORTRAIT + "The same small knight as the reference image, exactly the same bald head, pointed gray beard and face. " + W["nigel_war"] + ". No eye-patch. He is the ONLY figure in the frame. " + STYLE, ["nigel"], "3:4"),
    ("maude_castle", PORTRAIT + "The same young woman as the reference image, exactly the same face and jet-black hair. " + W["maude_castle"] + ". She is the ONLY figure in the frame. " + STYLE, ["maude"], "3:4"),
    # location plates
    ("loc_merlin", "Interior location plate, no people: the common room of a 14th-century English wayside inn at night. Low smoke-blackened ceiling and beams, a huge open fire with a bubbling cauldron, benches and trestle tables sunk in a clay floor, resinous torches, painted wooden heraldic shields over the fireplace, red firelight and black shadow. " + STYLE, [], "16:9"),
    ("loc_twynham", "Exterior location plate, no people: a small 14th-century English castle at dusk - black gateway with two torches casting a red glare, drawbridge over a river, grass-grown bailey, a gaunt square windowless stone keep on a mound, banners with five scarlet roses on white. " + STYLE, [], "16:9"),
    ("loc_cog", "Location plate, no people: a high-ended, deep-waisted 14th-century merchant cog painted canary yellow on a steel-blue winter sea, one broad purple mainsail painted with a large golden image of a bearded robed giant wading through water carrying a small child on his shoulder (Saint Christopher), wooden fore and stern castles, frosty bright light. " + STYLE, [], "16:9"),
    ("loc_villefranche", "Exterior location plate, no people: a grim French castle by moonlight - broad moat, high turreted outer wall, one great black square keep towering above, two torches burning at the gate, dark woods and a silver moonlit glade beyond. " + STYLE, [], "16:9"),
    ("loc_gorge", "Location plate, no people: a wild Spanish mountain gorge on a cold March morning, rolling mist tearing apart, brown crags walling in a wedge-shaped valley, one small boulder-strewn hill with a flat top and a sheer cliff at its back, a pink snow-capped peak high above the vapor. " + STYLE, [], "16:9"),
]

F = W  # shorthand

FRAMES = [
    # (shot, prompt, anchor refs)
    ("a1_bell", "Wide establishing shot: a great 14th-century Cistercian abbey in the green English New Forest at golden morning light, a bell swinging in the tower, lines of white-robed monks streaming in from vineyards and fields. " + STYLE, ["abbot"]),
    ("a2_trial", "A broad candle-lit monastery chapter house with rows of white-robed monks on long oak benches. Center: " + F["john"] + ", standing at a carved oak prayer-desk, grinning defiantly. Facing him on a raised chair, " + F["abbot"] + ", one long hand raised in stern accusation. " + STYLE, ["john", "abbot"]),
    ("a3_flight", "The gate of a medieval abbey: " + F["john"] + ", sprinting out through the arch roaring with laughter, carrying a heavy carved oak prayer-desk overhead like a club, white-robed monks scattering behind him like poplars in a tempest. " + STYLE, ["john", "abbot"]),
    ("a4_farewell", "Sunset at the abbey gate. " + F["abbot"] + ", laying a blessing hand on the bowed golden head of " + F["alleyne"] + ", who holds his staff and scrip. Long mellow evening light on the cloister arches behind. " + STYLE, ["abbot", "alleyne"]),
    ("a5_merlin", "The smoky firelit common room of the inn from the reference image, crowded with rough medieval travellers jeering. " + F["alleyne"] + " stands flushed and defiant; beside him " + F["john"] + " rises from a bench, slowly rolling up one sleeve over an arm like a leg of mutton. " + STYLE, ["alleyne", "john", "loc_merlin"]),
    ("a6_aylward", "The inn door burst open on a cold night: EXACTLY the same archer as in the first reference image - the same weather-beaten hazelnut-brown face with the long white scar from left nostril to jaw, the same plain dinted steel cap with a sprig of yellow broom (no crest, no plume), chain-mail brigandine, white surcoat with a red upright lion, yellow yew bow over his shoulder - stands blinking in the red firelight with a raised leather cup, laughing heartily; behind him porters carry in bundles of plunder; a buxom landlady laughs with her hands on her hips. Same inn as the second reference image. " + STYLE, ["aylward", "loc_merlin"]),
    ("a7_song", "Firelit tableau in the inn from the reference image: a fat red-faced minstrel plays a gilt harp; the whole rough room sings together, cups raised; " + F["aylward"] + " beats time with one raised finger; " + F["john"] + " sprawls huge by the fire; " + F["alleyne"] + " watches wide-eyed. Red light and black shadow. " + STYLE, ["aylward", "john", "alleyne", "loc_merlin"]),
    ("a8_wrestle", "Wrestling match in the inn, benches pushed back, crowd ringing the walls: " + F["john"] + ", stripped to the waist, mid-throw hurling " + F["aylward"] + " clean through the air across the firelit room. Motion, flying tankards, delighted faces. " + STYLE, ["john", "aylward", "loc_merlin"]),
    ("a9_rescue", "A green forest clearing with a brown stream and a rude plank bridge. " + F["socman"] + " grips the wrist of " + F["maude"] + ", her falcon flapping wildly; on the bridge " + F["alleyne"] + " steps forward with his iron-shod staff raised, face pale and resolute. Autumn sunlight. " + STYLE, ["socman", "maude", "alleyne"]),
    ("a10_bank", "A mossy bank under holly bushes by a forest stream, dappled autumn light. " + F["maude"] + " and " + F["alleyne"] + " sit talking, both dripping wet, her falcon preening on her wrist; she is half-laughing, he is grave. " + STYLE, ["maude", "alleyne"]),
    ("b1_stone", "An old stone bridge over a glassy river at evening, dozens of hounds milling about. " + F["john"] + " holds an enormous coping-stone overhead one-handed, about to hurl it in the river; " + F["nigel"] + " and " + F["lady_mary"] + " watch open-mouthed; " + F["aylward"] + " grins. Castle of the reference image in the background. " + STYLE, ["john", "nigel", "lady_mary", "aylward", "loc_twynham"]),
    ("b2_bear", "A narrow medieval town street at dusk, townsfolk fleeing into doorways. A huge black bear with a broken jangling chain rears up on its hind legs in the middle of the road; facing it stands EXACTLY the man from the reference image - a short, slight, normally-proportioned adult knight, bald with a small pointed gray beard, in his plum-purple velvet cote-hardie and feathered cap - calmly reaching up to flick a white silk handkerchief across the bear's snout like a man shooing a fly, completely unafraid. " + STYLE, ["nigel"]),
    ("b3_hall", "A castle great hall at night: log fire, bracket-lamps, tapestries. " + F["nigel"] + " holds an unrolled letter with two red seals; " + F["aylward"] + " stands at attention; " + F["maude_castle"] + " laughs behind a carved screen; " + F["alleyne"] + " stares at her thunderstruck. " + STYLE, ["nigel", "aylward", "maude_castle", "alleyne", "loc_twynham"]),
    ("b4_veil", "A dim stone armory window before dawn. " + F["maude_castle"] + " presses a folded green gauze veil into the hands of " + F["alleyne_squire"] + "; their faces close, torch-lit ranks of archers and horsemen mustered in the bailey far below through the window. " + STYLE, ["maude_castle", "alleyne_squire"]),
    ("b5_march", "A company of a hundred English archers in snow-white surcoats with red upright lions marches over a stone bridge behind drums, a great banner of five scarlet roses flying. At the front rides " + F["nigel"] + ", binding a small white glove to his velvet cap; " + F["lady_mary"] + " rides at his side; " + F["simon"] + " carries the guidon. Cold bright morning. " + STYLE, ["nigel", "lady_mary", "simon", "loc_twynham"]),
    ("c1_sail", "The yellow cog of the reference image ploughing a steel-blue winter sea, breath of frost in the air; behind it two long, black, low galleys knife through the water in pursuit, double oar-banks flashing, one sail badged with a dark head, the other with a red cross. " + STYLE, ["loc_cog"]),
    ("c2_ruse", "The deck of the yellow cog: a line of English archers in white surcoats springs up from behind the bulwarks loosing arrows point-blank at a black galley grinding alongside, grappling anchors biting; " + F["nigel_war"] + " points forward with his sword; trumpets blare. " + STYLE, ["nigel_war", "aylward", "john_archer", "loc_cog"]),
    ("c3_melee", "Savage melee on a ship's deck: " + F["john_archer"] + " has caught the mace-arm of a gigantic pirate in black plate armor and bends it backward, the pirate buckling; around them archers and boarders struggle; a second galley drifts away in the background. " + STYLE, ["john_archer", "loc_cog"]),
    ("d1_patch", "A busy medieval quay, forest of masts and gray crescent city behind. " + F["nigel_war"] + " kneels solemnly on the stones, binding a BLACK EYE-PATCH over his left eye; " + F["alleyne_squire"] + " and " + F["aylward"] + " stand over him, Aylward wry, Alleyne grave. " + STYLE, ["nigel_war", "alleyne_squire", "aylward"]),
    ("d2_chandos", "A great abbey hall with a blazing fireplace: " + F["chandos"] + ", sweeps up " + F["nigel_war"] + " (wearing a black eye-patch over his left eye) in a laughing embrace, one very tall and one very small, both one-eyed. Courtiers smile around them. " + STYLE, ["chandos", "nigel_war"]),
    ("d3_prince", "A dais under a broad scarlet velvet canopy spangled with silver fleurs-de-lis; two crowned kings on high blue-silk thrones behind, and BEFORE them on a plain stool " + F["prince"] + ", laughing heartily; " + F["nigel_war"] + " (black eye-patch, helmet under arm) stands before him earnest and puzzled; the court roars. " + STYLE, ["prince", "nigel_war"]),
    ("d4_tourney", "Tournament lists by a river, a dark sea of heads, banners and pavilions: two knights collide at full tilt, lances shattering into splinters; the smaller knight's helmet flies off revealing a shining bald head with a black eye-patch - " + F["nigel_war"] + " riding on unmoved. " + STYLE, ["nigel_war"]),
    ("d5_stranger", "Red sunset over tournament lists. A squat, immensely broad knight in a plain white surcoat with a plain black shield, vizor closed, sits like a statue of steel on his horse, refusing a golden goblet offered by a page; " + F["prince"] + " watches him gravely from the stand. " + STYLE, ["prince"]),
    ("e1_road", "Winter in ravaged France: four riders pass a burned farmstead - black roof-beams, gray gable-ends, broken fences under a leaden sky; at the distant tree-line a handful of gaunt ragged figures stand motionless, watching. Riders: " + F["nigel_war"] + " (black eye-patch), " + F["alleyne_squire"] + ", " + F["aylward"] + ", " + F["john_archer"] + ". " + STYLE, ["nigel_war", "alleyne_squire", "aylward", "john_archer"]),
    ("e2_inn", "A firelit French inn room: " + F["duguesclin"] + " explodes up from his chair, scattering a dish of walnuts, hand thrown out for a sword - but his scarred face is breaking into an enormous delighted grin; opposite him " + F["nigel"] + " (black eye-patch) bows with perfect mildness; " + F["tiphaine"] + " watches serene by the fire. " + STYLE, ["duguesclin", "nigel", "tiphaine"]),
    ("e3_prophecy", "A castle feast hall by candlelight, table laden, hooded hawks on perches. " + F["tiphaine"] + " stands rigid, cheeks blanched lily-white, eyes fixed on the tapestried wall, one hand half-raised; " + F["duguesclin"] + " and " + F["nigel"] + " (black eye-patch) watch frozen; shadows lean long. " + STYLE, ["tiphaine", "duguesclin", "nigel"]),
    ("e4_night", "Night. " + F["alleyne_squire"] + " at a moonlit stone casement, face drained with horror, counting; far below, across a silver moonlit glade between two black woods, a long file of crouching men with burdens creeps toward the castle. " + STYLE, ["alleyne_squire", "loc_villefranche"]),
    ("e5_hall", "A torchlit castle hall doorway: " + F["nigel_war"] + " (black eye-patch) and " + F["duguesclin"] + ", both half-armored, stand shoulder to shoulder with swords up, holding the door against a press of wild ragged men with scythes and clubs; arrows flash past from a stair behind them. " + STYLE, ["nigel_war", "duguesclin"]),
    ("e6_keep", "A narrow stone stair by torchlight: " + F["john_archer"] + " holds an entire massive iron-studded oak door, torn off its hinges, overhead like a shield, roaring, while defenders slip past behind him up the winding steps. " + STYLE, ["john_archer"]),
    ("e7_powder", "The flat top of a black stone keep at night, ringed far below by a sea of fire and thousands of upturned faces. " + F["john_archer"] + " heaves a heavy wooden powder-box over the parapet; beside him " + F["nigel_war"] + " (black eye-patch) watches calmly; the first white flash blooms below. " + STYLE, ["john_archer", "nigel_war", "loc_villefranche"]),
    ("e8_song", "Smoky dawn on the scorched keep top: five exhausted survivors lean on the parapet - " + F["tiphaine"] + " with one hand raised, listening; " + F["nigel_war"] + " (black eye-patch), " + F["duguesclin"] + ", " + F["aylward"] + " and " + F["john_archer"] + " turning toward the sound; far below, ranks of archers in snow-white surcoats pour singing from the woods. " + STYLE, ["tiphaine", "nigel_war", "duguesclin", "aylward", "john_archer"]),
    ("e9_tree", "A forest camp at dawn, wood-smoke drifting: " + F["nigel_war"] + " (black eye-patch) stands high on a great fallen tree-trunk, arms out, ringed by hundreds of upturned faces of archers in white surcoats; " + F["aylward"] + " punches the air; a dapper Gascon knight in rich clothes scowls at the edge with a knot of sulking men. " + STYLE, ["nigel_war", "aylward", "john_archer"]),
    ("f1_pass", "Dawn in a snowy mountain defile: an unbroken river of steel - thousands of armored men, horses and banners - winds between towering cliffs, knee-deep in snow, breath steaming like a cauldron; rose-pink light on the peaks. " + STYLE, ["simon"]),
    ("f2_volunteers", "A hillside camp: four long ranks of archers in white surcoats stand utterly still, every face fixed forward. In front, " + F["nigel_war"] + " (black eye-patch) stands crestfallen, and " + F["alleyne_squire"] + " leans in to whisper in his ear, suppressing a smile. " + STYLE, ["nigel_war", "alleyne_squire"]),
    ("f3_raid", "Dusk in a vast enemy camp, thousands of tents, distant flames on the skyline: four riders gallop hard down a tent-street - " + F["nigel_war"] + " in captured black Spanish armor with a black eye-patch, and " + F["john_archer"] + " with a limp man in a yellow-and-white royal surcoat slung over his shoulder; Spanish soldiers scatter. " + STYLE, ["nigel_war", "john_archer"]),
    ("f4_mist", "The boulder hill of the reference image: three hundred English archers and men-at-arms formed in a tight harrow on the summit under the banner of five scarlet roses, utterly still; the morning mist tears away to reveal, filling the whole valley below, a glittering many-colored host of thousands - lances, plumes, banners. " + F["nigel_war"] + " (black eye-patch) sits his horse at the front. " + STYLE, ["nigel_war", "aylward", "loc_gorge"]),
    ("f5_duel", "Between two watching armies, shattered lances on the trampled ground: " + F["nigel_war"] + " rides back toward the English hill, helmet off, bald head high - and plucks the black patch from his eye with a small satisfied smile. Behind him a fallen Spanish champion's riderless horse. " + STYLE, ["nigel_war"]),
    ("f6_storm", "The hillside: a wave of Spanish knights breaks against a storm of arrows, horses rearing and falling in a tangle at the slope's foot; on the crest the archers loose in perfect rhythm, arms all drawn back together; " + F["aylward"] + " at the line's end, face grim. " + STYLE, ["aylward", "john_archer", "loc_gorge"]),
    ("f7_stand", "The plateau's cliff edge in battle-haze: " + F["oliver"] + " locked chest-to-chest with a gigantic warrior-monk in a brown habit over mail, both toppling together over the brink; behind them " + F["nigel_war"] + " (NO eye-patch now) fights on, sword high amid the press. " + STYLE, ["oliver", "nigel_war", "loc_gorge"]),
    ("f8_cliff", "A sheer hundred-foot rock face: " + F["alleyne_squire"] + " swings on a rope halfway down the cliff, feet braced on the stone, jaw set, stones sparking off the rock around him; far below a single horse waits in the ravine. " + STYLE, ["alleyne_squire", "loc_gorge"]),
    ("f9_after", "The gray silent hilltop at evening, battle over, broken weapons and still figures half-hidden by mist; on the highest rock sits " + F["john_archer"] + ", bloodied and calm, one hand steadying a tattered banner of five scarlet roses, six weary bowmen around him; English riders crest the ridge, too late. " + STYLE, ["john_archer", "loc_gorge"]),
    ("g1_news", "A green Hampshire lane in high July, hedgerows and sheep: a gilt carriage tilted over a broken wheel, a stout over-dressed elderly lady gesturing; " + F["alleyne"] + " - now with a thin scar on brow and temple, in a fine blue doublet - wheels his horse round mid-gallop, face electrified; " + F["john"] + " in fine clothes behind him. " + STYLE, ["alleyne", "john"]),
    ("g2_nunnery", "A flower-strewn street before an old gray nunnery church, a procession of twenty white-clad singing girls scattered in surprise: a dust-caked young man has flung himself on foot before the black church arch (no horse anywhere in the frame) -" + F["alleyne"] + " with open arms, and the young woman from the second reference image (same face, same jet-black hair) dressed in plain WHITE novice robes with a wreath of white blossoms in her hair - NOT a pink gown, no falcon - falls sobbing against his chest. Sunlight behind them, darkness in the arch. " + STYLE, ["alleyne", "maude"]),
    ("g3_inn", "A summer inn with a great green bush hung on a pole: " + F["aylward"] + ", laughing with a serving-girl on each arm - and above, leaning from an upper window, " + F["nigel"] + " (no eye-patch) calls mildly down; in the lane " + F["alleyne"] + " stares up, stunned with joy. " + STYLE, ["aylward", "nigel", "alleyne"]),
    ("g4_end", "Gloaming: four riders cross a meadow toward the dark keep of the castle from the reference image, the red sun lying athwart the rippling river; long shadows, banners furled, home. " + STYLE, ["loc_twynham"]),
]

CARDS = [
    ("t_title", 'A film title card: the exact words "THE WHITE COMPANY" in large elegant off-white medieval serif capitals, centered over a dark misty background with a hanging red war-banner bearing five scarlet roses on a silver-white field. No other text.'),
    ("t_1366", 'A film title card: the exact words "ENGLAND, 1366" in small elegant off-white serif capitals, centered on a near-black background with the faintest mist. No other text.'),
    ("t_france", 'A film title card: the exact word "FRANCE" in small elegant off-white serif capitals, centered on a near-black background with the faintest mist. No other text.'),
    ("t_spain", 'A film title card: the exact words "SPAIN, 1367" in small elegant off-white serif capitals, centered on a near-black background with the faintest mist. No other text.'),
    ("t_home", 'A film title card: the exact words "HAMPSHIRE, FOUR MONTHS LATER" in small elegant off-white serif capitals, centered on a near-black background with the faintest mist. No other text.'),
]


def gen_image(dest: Path, prompt: str, refs: list[Path], aspect: str) -> str:
    if dest.exists():
        return f"skip {dest.name}"
    cmd = [sys.executable, str(GEN), "image", prompt, "--aspect_ratio", aspect]
    for r in refs:
        if not r.exists():
            return f"FAIL {dest.name}: missing ref {r}"
        cmd += ["--image", str(r)]
    for attempt in (1, 2):
        res = subprocess.run(cmd, capture_output=True, text=True)
        out = res.stdout.strip().splitlines()
        if res.returncode == 0 and out:
            src = Path(out[-1])
            if src.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(src.read_bytes())
                return f"ok   {dest.name}"
        err = (res.stdout + res.stderr).strip()[-200:]
    return f"FAIL {dest.name}: {err}"


def run_batch(jobs):
    with ThreadPoolExecutor(max_workers=5) as ex:
        for msg in ex.map(lambda j: gen_image(*j), jobs):
            print(msg, flush=True)


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    if phase in ("anchors", "all"):
        # base anchors first (variants reference them)
        base = [(ANCHORS_DIR / f"{n}.png", p, [ANCHORS_DIR / f"{r}.png" for r in refs], a)
                for n, p, refs, a in ANCHORS if not refs]
        variants = [(ANCHORS_DIR / f"{n}.png", p, [ANCHORS_DIR / f"{r}.png" for r in refs], a)
                    for n, p, refs, a in ANCHORS if refs]
        print(f"== anchors: {len(base)} base"); run_batch(base)
        print(f"== anchors: {len(variants)} variants"); run_batch(variants)
    if phase in ("frames", "all"):
        jobs = [(FRAMES_DIR / f"{n}.png", p, [ANCHORS_DIR / f"{r}.png" for r in refs], "16:9")
                for n, p, refs in FRAMES]
        print(f"== frames: {len(jobs)}"); run_batch(jobs)
    if phase in ("cards", "all"):
        jobs = [(CARDS_DIR / f"{n}.png", p, [], "16:9") for n, p in CARDS]
        print(f"== cards: {len(jobs)}"); run_batch(jobs)


if __name__ == "__main__":
    main()
