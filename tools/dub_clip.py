#!/usr/bin/env python3
"""Redub a clip's dialogue without re-rendering the video.

Pipeline: demucs splits dialogue from ambience/SFX -> new voice audio is produced
-> mixed over the original ambience at the original timing -> remuxed onto the
untouched video track.

Backends:
  seed (default)  higgsfield seed_audio TTS, voice-cloned from a local sample
                  (~0.3 credits/line). Needs the line text.
  elevenlabs      ElevenLabs. Two modes:
                  * speech-to-speech (default, NO text needed): converts the clip's
                    own vocal performance to the target voice — original timing and
                    emphasis preserved, best lip sync.
                  * TTS (pass text): regenerate the line from scratch.
                  Key: $ELEVENLABS_API_KEY or ~/.elevenlabs_key.
                  Voice: --voice-id <elevenlabs voice id> (see `/v1/voices`).

Usage:
  python3 dub_clip.py clip.mp4 voice_sample.m4a "line text" [start] [-o out.mp4]
  python3 dub_clip.py clip.mp4 --backend elevenlabs --voice-id <id> [-o out.mp4]
  python3 dub_clip.py clip.mp4 --backend elevenlabs --voice-id <id> "line text"
"""
import argparse, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).parent

ap = argparse.ArgumentParser()
ap.add_argument("clip")
ap.add_argument("voice", nargs="?", default=None,
                help="local voice sample (seed backend)")
ap.add_argument("text", nargs="?", default=None)
ap.add_argument("start", nargs="?", type=float, default=None,
                help="seconds where the line begins (default: auto from vocal stem)")
ap.add_argument("--backend", choices=["seed", "elevenlabs"], default="seed")
ap.add_argument("--voice-id", default=None, help="ElevenLabs voice id")
ap.add_argument("-o", "--out", default=None)
a = ap.parse_args()
if a.backend == "elevenlabs" and a.text is None and a.voice:
    a.text, a.voice = a.voice, None   # positional shift: elevenlabs takes no local sample
def eleven_key():
    import os
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k:
        f = Path.home() / ".elevenlabs_key"
        if f.exists():
            k = f.read_text().strip()
    if not k:
        sys.exit("no ElevenLabs key: set ELEVENLABS_API_KEY or write ~/.elevenlabs_key")
    return k
clip = Path(a.clip)
out = Path(a.out) if a.out else clip.with_name(clip.stem + "_dubbed.mp4")

tmp = Path(tempfile.mkdtemp(prefix="dub_"))
src_wav = tmp / "src.wav"
subprocess.run(["ffmpeg", "-v", "error", "-i", str(clip), "-vn", "-ac", "2",
                "-ar", "44100", str(src_wav), "-y"], check=True)
subprocess.run([sys.executable, "-m", "demucs", "--two-stems=vocals",
                "-o", str(tmp / "stems"), str(src_wav)],
               check=True, capture_output=True)
stems = tmp / "stems/htdemucs/src"

start = a.start
if start is None:
    det = subprocess.run(["ffmpeg", "-i", str(stems / "vocals.wav"), "-af",
                          "silencedetect=n=-30dB:d=0.3", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    for line in det.splitlines():
        if "silence_end" in line:
            start = float(line.split("silence_end:")[1].split("|")[0])
            break
    start = start or 0.3
print(f"line starts at {start:.2f}s")

line_wav = tmp / "line.wav"
if a.backend == "elevenlabs":
    if not a.voice_id:
        sys.exit("--voice-id required for elevenlabs backend")
    key = eleven_key()
    if a.text:  # TTS mode
        r = subprocess.run(["curl", "-sf", "-X", "POST",
            f"https://api.elevenlabs.io/v1/text-to-speech/{a.voice_id}",
            "-H", f"xi-api-key: {key}", "-H", "Content-Type: application/json",
            "-d", __import__("json").dumps({"text": a.text, "model_id": "eleven_multilingual_v2"}),
            "-o", str(tmp / "line.mp3")], capture_output=True)
        if r.returncode:
            sys.exit(f"elevenlabs tts failed: {r.stderr.decode()[:300]}")
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(tmp / "line.mp3"),
                        "-ar", "44100", "-ac", "1", str(line_wav), "-y"], check=True)
    else:       # speech-to-speech: convert the clip's own vocal stem
        r = subprocess.run(["curl", "-sf", "-X", "POST",
            f"https://api.elevenlabs.io/v1/speech-to-speech/{a.voice_id}",
            "-H", f"xi-api-key: {key}",
            "-F", f"audio=@{stems / 'vocals.wav'}",
            "-F", "model_id=eleven_multilingual_sts_v2",
            "-o", str(tmp / "line.mp3")], capture_output=True)
        if r.returncode:
            sys.exit(f"elevenlabs sts failed: {r.stderr.decode()[:300]}")
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(tmp / "line.mp3"),
                        "-ar", "44100", "-ac", "1", str(line_wav), "-y"], check=True)
        start = 0.0  # converted stem keeps original timeline; overlay from t=0
else:
    if not (a.voice and a.text):
        sys.exit("seed backend needs: clip voice_sample \"line text\"")
    r = subprocess.run(["higgsfield", "generate", "create", "seed_audio",
                        "--prompt", a.text, "--audio", a.voice,
                        "--format", "wav", "--wait"], capture_output=True, text=True)
    url = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    if not url.startswith("http"):
        sys.exit(f"seed_audio failed: {r.stdout} {r.stderr}")
    subprocess.run(["curl", "-sf", "-o", str(line_wav), url], check=True)

ms = int(start * 1000)
subprocess.run(["ffmpeg", "-v", "error", "-i", str(clip), "-i", str(stems / "no_vocals.wav"),
                "-i", str(line_wav), "-filter_complex",
                f"[2:a]adelay={ms}|{ms}[line];"
                f"[1:a][line]amix=inputs=2:normalize=0:duration=first[am]",
                "-map", "0:v", "-map", "[am]", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", str(out), "-y"], check=True)
print(f"wrote {out}")
