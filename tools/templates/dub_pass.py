#!/usr/bin/env python3
# TEMPLATE — copied from mewtwo/dub_pass.py (batch re-voice rendered clips via demucs + ElevenLabs STS).
# Project-specific: expects that film's spec/paths. Copy into a new film
# folder and adapt; the original in mewtwo/ is the working example.
"""Re-voice every rendered dialogue clip to the locked ElevenLabs cast without
re-rendering video (lip sync survives — timing is preserved).

Per clip: demucs splits vocals/ambience -> speech segments found in the vocal
stem -> each segment converted with ElevenLabs speech-to-speech into its
speaker's target voice (speaker order known from vo_vs.LINES) -> segments laid
back at original offsets over the ambience -> remuxed onto the video.

Outputs outputs/v1_dub/<shot>.mp4. Skips existing. Clips whose segment count
doesn't match their line count are listed at the end for manual attention.
Usage: python3 dub_pass.py [shot ...]
"""
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

from vo_vs import LINES

HERE = Path(__file__).parent
SRC = HERE / "outputs/v1"
DST = HERE / "outputs/v1_dub"
DST.mkdir(parents=True, exist_ok=True)
KEY = (Path.home() / ".elevenlabs_key").read_text().strip()

# Mewtwo speaks in two registers: the suit/pod SPEAKER voice he chose himself
# (Carter, deep baritone) and his true inner/telepathic voice (Archie,
# boyish). SYNTH_LINES maps shot -> 1-based line indices that are speaker
# lines; every other mewtwo line is inner/telepathic.
SYNTH_LINES = {"b1b": {3}, "b3": {1}, "d6a": {1}, "d6b": {1}, "e1": {1}, "e7": {2},
               "f4a": {2}, "f4b": {2}, "f6a": {1}, "f6b": {1}, "f7": {2},
               "f8": {2}}
CARTER = "qNkzaJoHLLdpvgh5tISm"
ADOL = "7lrUEvfHJc6kDXxOqSEQ"   # AdolMewtwo (director's design)

CAST = {  # character -> ElevenLabs voice id (None = keep original)
    "mewtwo":   ADOL,                     # inner/telepathic default
    "sabrina":  "hpp4J3VqNfWAUOO0d1Us",   # Bella
    "giovanni": "XtNxzKiiqcVjhZYj67Lr",   # Don Giovanni
    "drlight":  "EXAVITQu4vr4xnSDxMaL",   # Sarah
    "shaw":     "N2lVS1w4EtoT3dr4eOWO",   # Callum
    "eva":      "pFZP5JQG7iQjIQuC4Bku",   # Lily
    "gyokusho": "bIHbv24MWmeRgasZH58o",   # Will
    "fuji":     "pqHfZKP75CvOlQylNhV4",   # Bill
    "sato": None, "martin": None, "collins": None,
}
SETTINGS = {"stability": 0.55, "similarity_boost": 0.8, "style": 0.2}


def sts(seg_wav: Path, voice_id: str, out_mp3: Path) -> None:
    import mimetypes, uuid
    boundary = uuid.uuid4().hex
    data = seg_wav.read_bytes()
    body = b""
    def field(name, value):
        return (f"--{boundary}\r\nContent-Disposition: form-data; "
                f'name="{name}"\r\n\r\n{value}\r\n').encode()
    body += field("model_id", "eleven_multilingual_sts_v2")
    body += field("voice_settings", json.dumps(SETTINGS))
    body += (f"--{boundary}\r\nContent-Disposition: form-data; "
             f'name="audio"; filename="seg.wav"\r\n'
             f"Content-Type: audio/wav\r\n\r\n").encode() + data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/speech-to-speech/{voice_id}",
        data=body, method="POST",
        headers={"xi-api-key": KEY,
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        out_mp3.write_bytes(r.read())


def speech_segments(vocal_wav: Path, total: float) -> list:
    """[(start, end)] of speech in the vocal stem via silencedetect inversion."""
    det = subprocess.run(
        ["ffmpeg", "-i", str(vocal_wav), "-af",
         "silencedetect=n=-32dB:d=0.45", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", det)]
    ends = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", det)]
    # build speech spans between silences
    spans, cur = [], 0.0
    for s, e in zip(starts, ends + [None]):
        if s - cur > 0.25:
            spans.append((cur, s))
        cur = e if e is not None else total
    if total - cur > 0.25:
        spans.append((cur, total))
    # merge spans separated by tiny gaps
    merged = []
    for s, e in spans:
        if merged and s - merged[-1][1] < 0.35:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return [(max(0, s - 0.12), min(total, e + 0.12)) for s, e in merged]


def dur_of(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)


def dub(shot: str) -> str:
    src, dst = SRC / f"{shot}.mp4", DST / f"{shot}.mp4"
    if dst.exists():
        return f"skip {shot}"
    chars = [c for c, _ in LINES[shot]]
    voices = [CAST.get(c) for c in chars]
    for i, c in enumerate(chars):
        if c == "mewtwo" and (i + 1) in SYNTH_LINES.get(shot, set()):
            voices[i] = CARTER
    if all(v is None for v in voices):
        subprocess.run(["cp", str(src), str(dst)])
        return f"keep {shot} (no recast speakers)"

    tmp = Path(tempfile.mkdtemp(prefix=f"dub_{shot}_"))
    wav = tmp / "src.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vn",
                    "-ac", "2", "-ar", "44100", str(wav)], check=True)
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems=vocals",
                    "-o", str(tmp / "st"), str(wav)],
                   check=True, capture_output=True)
    stems = tmp / "st/htdemucs/src"
    total = dur_of(wav)
    segs = speech_segments(stems / "vocals.wav", total)

    # a pause inside a line can split it into two segments: greedily merge the
    # closest-gap neighbours until the count matches the script's line count
    while len(segs) > len(chars):
        gaps = [(segs[i + 1][0] - segs[i][1], i) for i in range(len(segs) - 1)]
        _, i = min(gaps)
        segs[i] = (segs[i][0], segs[i + 1][1])
        del segs[i + 1]
    if len(segs) != len(chars):
        # tolerate the very common one-speaker case by converting the whole stem
        if len(set(v for v in voices if v)) == 1 and all(v for v in voices):
            segs = [(0.0, total)]
            voices = [voices[0]]
            chars = [chars[0]]
        else:
            return f"MISMATCH {shot}: {len(segs)} segments vs {len(chars)} lines"

    parts = []
    for i, ((s, e), v) in enumerate(zip(segs, voices)):
        seg = tmp / f"seg{i}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i",
                        str(stems / "vocals.wav"), "-ss", f"{s:.3f}", "-to",
                        f"{e:.3f}", str(seg)], check=True)
        if v is None:
            parts.append((s, seg))       # keep original performance
            continue
        conv = tmp / f"seg{i}_conv.mp3"
        sts(seg, v, conv)
        parts.append((s, conv))

    # mix: ambience + each converted segment at its offset
    inputs = ["-i", str(stems / "no_vocals.wav")]
    fc, labels = [], []
    for j, (s, p) in enumerate(parts):
        inputs += ["-i", str(p)]
        fc.append(f"[{j+1}:a]aresample=44100,"
                  f"adelay={int(s*1000)}|{int(s*1000)},apad,"
                  f"atrim=duration={total:.3f}[v{j}]")
        labels.append(f"[v{j}]")
    fc.append(f"[0:a]apad,atrim=duration={total:.3f}[amb]")
    fc.append("[amb]" + "".join(labels)
              + f"amix=inputs={len(labels)+1}:normalize=0:duration=first[out]")
    mixed = tmp / "mixed.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs +
                   ["-filter_complex", ";".join(fc), "-map", "[out]",
                    str(mixed)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-i",
                    str(mixed), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", str(dst)], check=True)
    return f"OK   {shot} ({len(parts)} segs)"


if __name__ == "__main__":
    shots = sys.argv[1:] or sorted(
        s for s in LINES if (SRC / f"{s}.mp4").exists())
    issues = []
    for s in shots:
        try:
            r = dub(s)
        except Exception as e:  # noqa: BLE001
            r = f"FAIL {s}: {str(e)[:140]}"
        print(r, flush=True)
        if r.startswith(("MISMATCH", "FAIL")):
            issues.append(r)
    print(f"\n{len(issues)} issues")
    for i in issues:
        print(" ", i)
