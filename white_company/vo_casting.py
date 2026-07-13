#!/usr/bin/env python3
"""Generate ElevenLabs voice auditions for the White Company cast.

For each role: TTS one characteristic (verbatim-Doyle) line with each candidate
voice into vo_auditions/<role>__<slug>.mp3. Shared-library voices are added to
the account for the TTS call and deleted afterwards (slots restored); account
voices are left untouched. Skips existing mp3s, so re-running is the retry pass.
"""
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

PROJ = Path(__file__).parent
OUT = PROJ / "vo_auditions"
KEY = Path.home().joinpath(".elevenlabs_key").read_text().strip()
API = "https://api.elevenlabs.io/v1"

# (display name, voice_id, source) — source: "account" or "lib"
VOICES = {
    "ethan":      ("Ethan - Warm & Trusting",            "WoxRV1VQUDtxEHPVAZyL", "lib"),
    "cassian":    ("Cassian - British Noble",            "Veg2qijYoJAS8VPKOOmi", "lib"),
    "francis":    ("Francis - Expressive & Reflective",  "Q2AxzVplKbaj5rJp4P15", "lib"),
    "henry":      ("Henry - royal, elegant",             "VRAN0xryQGUWtDuwToRv", "account"),
    "george":     ("George - Warm Storyteller",          "JBFqnCBsd6RMkjVDRZzb", "account"),
    "nathaniel":  ("Nathaniel C - Gentle Storyteller",   "h9CKu0pq1LSjIPhJEGCv", "lib"),
    "gideon":     ("Gideon - Rugged Gravelly Northern",  "q1h5HGdnfVxp4TXTJRNN", "lib"),
    "john_north": ("John of the North - Bluff Northern", "7rQX8r6PVq3gfJ8rZzyE", "lib"),
    "dave":       ("Dave - Gritty Cheeky London",        "0m71kiyu84bdUcKDzG0L", "lib"),
    "gravel":     ("Gravel Midnight - Deep Grit",        "M5E055lOUxMi0kJpGyE9", "lib"),
    "sebastian":  ("Sebastian - Bold Baritone",          "1SaGpH4wLZDmppsPYVpx", "lib"),
    "chris_ne":   ("Chris - Northern UK (Durham)",       "AmY1pcgcEc15wyuIj50p", "lib"),
    "mia":        ("Mia - Elegant Storyteller",          "e6qsVnCuD0MWxmhZcuKz", "lib"),
    "peach":      ("Peach - Casual Friendly British",    "3cuC1hNj9E2jcHlIvndN", "lib"),
    "lily":       ("Lily - Velvety Actress",             "pFZP5JQG7iQjIQuC4Bku", "account"),
    "jan":        ("Jan - British & Well Spoken (50s)",  "s3ITUENHJxfTA8uG0Ady", "lib"),
    "enid":       ("Enid - Editorial RP",                "byQMr3answnWiGKk0ZUm", "lib"),
    "dracon":     ("Dracon - Feral & Dangerous",         "A921zklid24OpyVy1Elb", "lib"),
    "bloodgrin":  ("Bloodgrin - Deep Guttural Villain",  "KTAbPR4QFlhaTpde6md8", "account"),
    "achille":    ("Achille",                            "94VTtZwvNmsppde6nAW0", "account"),
    "sandy":      ("Sandy Soft - Velvet",                "ymZ2m14IsFBURjROEE2J", "lib"),
    "alice":      ("Alice - Clear British",              "Xb7hH8MSUJpSbSDYk0k2", "account"),
    "cassius":    ("Cassius - Velvety Commanding",       "ktrGUw7rURIQyMrQZqCu", "lib"),
    "daniel":     ("Daniel - Steady Broadcaster",        "onwK4e9ZLuTAKqWW03F9", "account"),
    "alistair":   ("Alistair - Cultured & Articulate",   "UzI1NsMEV3ni5JRkRSls", "lib"),
    "ak":         ("AK - Posh Well-Spoken Old Man",      "y0SYydk17lMbUIUvSf3N", "lib"),
    "desmond":    ("Desmond - Gravelly 75+",             "jAW0IMxOTz75sgLAYWp6", "lib"),
    "raymond":    ("Raymond Verne - Dynamic Expressive", "HWDDFlsSVOpTSkiLijPq", "lib"),
    "steve":      ("Steve Wilkes - Mellow Deep",         "jr4BEb8zU7Zqyvq3fU4R", "lib"),
    "sterling":   ("Sterling - Steady & Resonant",       "jhBzyKbsdeM6F66SZCaK", "lib"),
    "zane":       ("Zane - Sinister Narrator",           "qbkH1EDealYs8PUoNNuB", "lib"),
    "adam":       ("Adam - Steady Rich Classic",         "Gsndh0O5AnuI2Hj3YUlA", "lib"),
    "northberry": ("David Northberry - Lancashire",      "sAxd8ffzrizgUQNI8nre", "lib"),
    "dominic":    ("Dominic - Brooding & Intense",       "yhf80q1381zd2JJQ4tM7", "lib"),
    "blackwood":  ("Blackwood - Sinister Posh",          "agL69Vji082CshT65Tcy", "lib"),
}

# role -> (audition line, [candidate slugs, first = current recommendation])
ROLES = {
    "alleyne": (
        "Brother or no, I swear by my hopes of salvation that I will break your arm "
        "if you do not leave hold of the maid. ... You are my heart, my life, my one "
        "and only thought.",
        ["ethan", "cassian", "francis"]),
    "nigel": (
        "By Saint Paul! It is a very small matter that I should be hanged... but it "
        "would be a very grievous thing that you should make a vow and fail to bring "
        "it to fulfilment. I think that I am now clear of my vow, for this Spanish "
        "knight was a person from whom much honor might be won.",
        ["henry", "george", "nathaniel"]),
    "aylward": (
        "By my hilt! camarades, there is no drop of French blood in my body, and I am "
        "a true English bowman, Samkin Aylward by name. To Sir Claude Latour and the "
        "White Company!",
        ["gideon", "john_north", "dave"]),
    "john": (
        "By the black rood of Waltham! If any knave among you lays a finger-end upon "
        "the edge of my gown, I will crush his skull like a filbert! ... Hush, lad, I "
        "count them not a fly.",
        ["gravel", "sebastian", "chris_ne"]),
    "maude": (
        "You had him at your mercy. Why did you not kill him? He would have killed "
        "you. I know him, and I read it in his eyes. ... Win my father's love, and "
        "all may follow.",
        ["mia", "peach", "lily"]),
    "lady_mary": (
        "Good lack! Ma foi, my fair lord, you will be the death of me yet. See that "
        "your linens are dry, and your wine well watered.",
        ["jan", "enid"]),
    "duguesclin": (
        "Dogs of England, must ye be lashed hence? Tiphaine, my sword! ... Mort Dieu! "
        "It is my little swordsman of Bordeaux! France and England will fight "
        "together this night.",
        ["dracon", "bloodgrin", "achille"]),
    "tiphaine": (
        "Danger, Bertrand. Deadly, pressing danger, which creeps upon you and you "
        "know it not. Here... now... close upon you!",
        ["sandy", "lily", "alice"]),
    "prince": (
        "Peace! Peace! I am very well able to look to my own vows and their "
        "performance. By my soul! He has served his master this day even as I would "
        "wish liegeman of mine to serve me.",
        ["cassius", "daniel", "sebastian"]),
    "chandos": (
        "Ha, my little heart of gold! Since you have tied up one of your eyes, and I "
        "have had the mischance to lose one of mine, we have but a pair between us.",
        ["alistair", "ak", "desmond"]),
    "oliver": (
        "For pullets! By the apple of Eve! I was prodding for my food into a "
        "camp-kettle when they were howling for their pap.",
        ["raymond", "desmond", "steve"]),
    "simon": (
        "Yonder is where Roland fell. It is not the Frenchman's gold, but the "
        "Frenchman's blood that I would have.",
        ["sterling", "zane"]),
    "abbot": (
        "What talk is this? Is this a tongue to be used within the walls of an old "
        "and well-famed monastery?",
        ["ak", "adam"]),
    "johnston": (
        "My day is past... a broken bowman. The eye to the string, the string to the "
        "shaft, and the shaft to the mark.",
        ["northberry", "gideon"]),
    "socman": (
        "Must pay Saxon toll on Saxon land, my proud Maude, for all your airs and "
        "graces. Doff to me, young cub of Beaulieu.",
        ["dominic", "blackwood"]),
}


def api(path, method="GET", data=None, raw=False):
    req = urllib.request.Request(API + path, method=method,
                                 headers={"xi-api-key": KEY})
    if data is not None:
        req.data = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as r:
        body = r.read()
    return body if raw else (json.loads(body) if body else {})


def owner_id(name, voice_id):
    """Find a shared-library voice's public_owner_id by searching its name."""
    q = urllib.parse.quote(name.split(" - ")[0].strip())
    d = api(f"/shared-voices?page_size=100&search={q}")
    for v in d.get("voices", []):
        if v["voice_id"] == voice_id:
            return v["public_owner_id"]
    raise LookupError(f"{name} ({voice_id}) not found in shared library")


def main():
    OUT.mkdir(exist_ok=True)
    mine = {v["voice_id"] for v in api("/voices")["voices"]}
    added = []
    used = {s for _, (_, cands) in ROLES.items() for s in cands}
    try:
        for slug in sorted(used):
            name, vid, src = VOICES[slug]
            jobs = [(role, line) for role, (line, cands) in ROLES.items()
                    if slug in cands
                    and not (OUT / f"{role}__{slug}.mp3").exists()]
            if not jobs:
                print(f"skip {slug} (all mp3s exist)")
                continue
            if vid not in mine:
                if src == "account":
                    print(f"WARN {slug}: expected in account but missing; adding from lib")
                oid = owner_id(name, vid)
                api(f"/voices/add/{oid}/{vid}", "POST", {"new_name": f"audition_{slug}"})
                mine.add(vid)
                added.append(vid)
                print(f"added {slug} from library")
            for role, line in jobs:
                dest = OUT / f"{role}__{slug}.mp3"
                body = api(f"/text-to-speech/{vid}", "POST",
                           {"text": line, "model_id": "eleven_multilingual_v2"},
                           raw=True)
                dest.write_bytes(body)
                print(f"ok   {dest.name} ({len(body)//1024} KB)")
                time.sleep(0.5)
    finally:
        for vid in added:
            try:
                api(f"/voices/{vid}", "DELETE")
            except Exception as e:
                print(f"WARN could not delete {vid}: {e}")
        if added:
            print(f"cleaned up {len(added)} library voices (slots restored)")


if __name__ == "__main__":
    main()
