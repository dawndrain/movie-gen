#!/usr/bin/env python3
"""Full-film ANIMATIC: locked ElevenLabs cast + still frames + gentle push-in.

The cheap iteration layer — script, voices, pacing and music are all
reviewable here before spending any Seedance credits.

1. TTS every dialogue line in the locked cast -> vo_el/<shot>_<n>_<char>.mp3
2. Build one still+audio clip per shot -> outputs/animatic_clips/<shot>.mp4
   (frame = frames2/ replacement when one exists, else frames/; slow Ken
   Burns push-in so nothing is a dead freeze)
Then run assemble_animatic.py for the scored cut.
Skips existing files; re-run = retry. `--force-vo shot ...` re-TTSes shots.
"""
import json
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from vo_vs import LINES

HERE = Path(__file__).parent
VOEL = HERE / "vo_el"
CLIPS = HERE / "outputs/animatic_clips"
VOEL.mkdir(exist_ok=True)
CLIPS.mkdir(parents=True, exist_ok=True)
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()

# locked cast (casting.md). Mewtwo: Archie = inner/telepathic true voice,
# Carter = the deep suit-speaker voice he chose himself.
SYNTH_LINES = {"b1b": {3}, "b3": {1}, "d6a": {1}, "d6b": {1}, "e1": {1}, "e7": {2},
               "f4a": {2}, "f4b": {2}, "f6a": {1}, "f6b": {1}, "f7": {2},
               "f8": {2}}
CAST = {
    "mewtwo":   "7lrUEvfHJc6kDXxOqSEQ",   # AdolMewtwo (inner default)
    "sabrina":  "hpp4J3VqNfWAUOO0d1Us",   # Bella
    "giovanni": "XtNxzKiiqcVjhZYj67Lr",   # Don Giovanni (Voice Design)
    "drlight":  "EXAVITQu4vr4xnSDxMaL",   # Sarah
    "shaw":     "N2lVS1w4EtoT3dr4eOWO",   # Callum
    "eva":      "pFZP5JQG7iQjIQuC4Bku",   # Lily
    "gyokusho": "bIHbv24MWmeRgasZH58o",   # Will
    "fuji":     "pqHfZKP75CvOlQylNhV4",   # Bill — old, kind, worn
    "sato":     "iP95p4xoKVk53GoZ742B",   # Chris (animatic stand-in)
    "martin":   "cjVigY5qzO86Huf0OWal",   # Eric (animatic stand-in)
    "collins":  "IKne3meq5aSn9XLyUdCD",   # Charlie (animatic stand-in)
}
CARTER = "qNkzaJoHLLdpvgh5tISm"
CALM = {"stability": 0.6, "similarity_boost": 0.8, "style": 0.15,
        "use_speaker_boost": True}

# line-text overrides for the animatic (natural phrasing where the scripted
# ellipsis reads as voice hesitancy)
TEXT_FIX = {("a4", 3): "Calm. Two plus two is four."}
# per-line voice_settings overrides (emotional reads)
SETTINGS_FIX = {("h3", 1): {"stability": 0.28, "similarity_boost": 0.75,
                            "style": 0.65, "use_speaker_boost": True}}

SILENT_DUR = {"a2": 6, "f1": 7, "f5": 8, "g1": 6, "g4": 8, "title": 5}


def voice_for(shot: str, n: int, char: str) -> str:
    if char == "mewtwo" and n in SYNTH_LINES.get(shot, set()):
        return CARTER
    return CAST[char]


def tts(dest: Path, voice_id: str, text: str, settings=None) -> str:
    if dest.exists():
        return f"skip {dest.name}"
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
                       "voice_settings": settings or CALM}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=body, method="POST",
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                dest.write_bytes(r.read())
            return f"OK   {dest.name}"
        except Exception as e:  # noqa: BLE001
            err = str(e)
    return f"FAIL {dest.name}: {err[:100]}"


def adur(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)


def frame_for(shot: str) -> Path:
    if (Path("frames2") / f"{shot}.png").exists():
        return Path("frames2") / f"{shot}.png"
    base = (shot[:-1] if shot and shot[-1] in "ab"
            and shot not in SILENT_DUR else shot)
    for d in ("frames2", "frames"):
        p = HERE / d / f"{base}.png"
        if p.exists():
            return p
    raise SystemExit(f"no frame for {shot}")


def build_clip(shot: str) -> str:
    dest = CLIPS / f"{shot}.mp4"
    if dest.exists():
        return f"skip clip {shot}"
    frame = frame_for(shot)
    auds = []
    if shot in LINES:
        auds = [VOEL / f"{shot}_{n}_{c}.mp3"
                for n, (c, _) in enumerate(LINES[shot], 1)]
    dur = SILENT_DUR.get(shot) or round(
        sum(adur(a) for a in auds) + 1.6 + 0.6 * len(auds), 2)
    # plain stills — zoompan jitters (integer-pixel rounding each frame)
    vf = "scale=854:480:force_original_aspect_ratio=decrease," \
         "pad=854:480:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24"
    inputs = ["-loop", "1", "-t", str(dur), "-i", str(frame)]
    for a in auds:
        inputs += ["-i", str(a)]
    if auds:
        gaps = "".join(
            f"anullsrc=r=48000:cl=stereo,atrim=duration=0.6[g{i}];"
            for i in range(len(auds)))
        conv = "".join(f"[{i+1}:a]aresample=48000[a{i}];"
                       for i in range(len(auds)))
        chain = "[sil]" + "".join(f"[a{i}][g{i}]" for i in range(len(auds)))
        fc = (f"anullsrc=r=48000:cl=stereo,atrim=duration=1.0[sil];{gaps}{conv}"
              f"{chain}concat=n={2*len(auds)+1}:v=0:a=1,apad,"
              f"atrim=duration={dur}[aout]")
    else:
        fc = (f"anullsrc=r=48000:cl=stereo,atrim=duration={dur}[aout]")
    r = subprocess.run(
        ["ffmpeg", "-y", "-v", "error"] + inputs +
        ["-filter_complex", fc, "-map", "0:v", "-map", "[aout]", "-vf", vf,
         "-t", str(dur), "-c:v", "libx264", "-preset", "veryfast", "-crf",
         "19", "-pix_fmt", "yuv420p", "-c:a", "aac", str(dest)],
        capture_output=True, text=True)
    return f"OK   clip {shot} ({dur}s)" if r.returncode == 0 else \
        f"FAIL clip {shot}: {r.stderr[-120:]}"


if __name__ == "__main__":
    jobs = []
    for shot, lines in LINES.items():
        for n, (char, text) in enumerate(lines, 1):
            text = TEXT_FIX.get((shot, n), text)
            jobs.append((VOEL / f"{shot}_{n}_{char}.mp3",
                         voice_for(shot, n, char), text,
                         SETTINGS_FIX.get((shot, n))))
    with ThreadPoolExecutor(max_workers=4) as pool:
        for res in pool.map(lambda j: tts(*j), jobs):
            if not res.startswith("skip"):
                print(res, flush=True)
    all_shots = set(LINES) | set(SILENT_DUR)
    for shot in sorted(all_shots):
        res = build_clip(shot)
        if not res.startswith("skip"):
            print(res, flush=True)
