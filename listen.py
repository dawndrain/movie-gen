#!/usr/bin/env python3
"""Ask Gemini to LISTEN to an audio/video file and answer questions about it.

The ears of the pipeline: Claude can't hear, Gemini can. Use for QC-ing
ambience beds, music cues, dubs, and final mixes before a human ever listens.

Usage:
  python3 listen.py <file.(mp3|m4a|wav|mp4)> "question about the audio"
  python3 listen.py mix.mp4 --start 310 --dur 15 "is the ambience audible under the dialogue?"

Key: ~/.gemini_key or $GEMINI_API_KEY. Video inputs have audio extracted first
(Gemini gets audio only — cheaper and it's the point). Inline upload, so keep
excerpts under ~15 min of mp3.
"""
import argparse, base64, json, os, subprocess, sys, tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("file")
ap.add_argument("prompt")
ap.add_argument("--start", type=float, default=None)
ap.add_argument("--dur", type=float, default=None)
ap.add_argument("--model", default="gemini-3-flash-preview")
a = ap.parse_args()

key = os.environ.get("GEMINI_API_KEY") or (Path.home() / ".gemini_key").read_text().strip()

src = Path(a.file)
tmp = None
if src.suffix.lower() != ".mp3" or a.start is not None or a.dur is not None:
    tmp = Path(tempfile.mkstemp(suffix=".mp3")[1])
    cmd = ["ffmpeg", "-v", "error"]
    if a.start is not None:
        cmd += ["-ss", str(a.start)]
    if a.dur is not None:
        cmd += ["-t", str(a.dur)]
    cmd += ["-i", str(src), "-vn", "-ac", "1", "-b:a", "64k", "-y", str(tmp)]
    subprocess.run(cmd, check=True)
    src = tmp

data = base64.b64encode(src.read_bytes()).decode()
if tmp:
    tmp.unlink()

body = {"contents": [{"parts": [
    {"inline_data": {"mime_type": "audio/mp3", "data": data}},
    {"text": a.prompt},
]}]}

for model in (a.model, "gemini-2.5-flash"):
    r = subprocess.run(
        ["curl", "-sf", "-X", "POST",
         f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
         "-H", "Content-Type: application/json", "-d", "@-"],
        input=json.dumps(body), capture_output=True, text=True)
    if r.returncode == 0:
        try:
            print(json.loads(r.stdout)["candidates"][0]["content"]["parts"][0]["text"])
            sys.exit(0)
        except (KeyError, IndexError, json.JSONDecodeError):
            print(f"[{model}] unexpected response: {r.stdout[:300]}", file=sys.stderr)
    else:
        print(f"[{model}] request failed, trying fallback...", file=sys.stderr)
sys.exit("all models failed")
