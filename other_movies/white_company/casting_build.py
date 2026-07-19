#!/usr/bin/env python3
"""Build white_company/casting.html: every role with its anchor portrait and
playable ElevenLabs voice auditions (name, id, source, measured pitch).
Rerun after adding/retaking auditions."""
import html
import re
import subprocess
from pathlib import Path

from vo_casting import ROLES, VOICES

PROJ = Path(__file__).parent
VO = PROJ / "vo_auditions"
PITCH = PROJ.parent / "pitch_check.py"

ROLE_INFO = {  # role -> (display name, anchor image, one-line brief)
    "alleyne":    ("Alleyne Edricson", "anchors/alleyne.png", "The hero. Gentle, earnest young British tenor — courteous, monk-bred, steel underneath."),
    "nigel":      ("Sir Nigel Loring", "anchors/nigel.png", "Soft, mild, LISPING older voice, unfailingly polite — the quieter the deadlier. 'By Saint Paul!'"),
    "aylward":    ("Sam Aylward", "anchors/aylward.png", "Hearty gravelly soldier, French tags sprinkled through. 'By my hilt!'"),
    "john":       ("Hordle John", "anchors/john.png", "Enormous booming bass, slow rustic West-Country drawl, deadpan."),
    "maude":      ("Lady Maude Loring", "anchors/maude.png", "Quick, teasing, aristocratic young female voice; mercurial."),
    "lady_mary":  ("Lady Mary Loring", "anchors/lady_mary.png", "Commanding older female voice; rules the castle; fondly scolding."),
    "duguesclin": ("Bertrand du Guesclin", "anchors/duguesclin.png", "Deep bestial growl, French accent, flips from menace to warmth."),
    "tiphaine":   ("Lady Tiphaine", "anchors/tiphaine.png", "Low, grave, musical French-accented voice; trance lines distant and muffled."),
    "prince":     ("The Black Prince", "anchors/prince.png", "Commanding refined young voice, regal but hot-tempered. 'By my soul!'"),
    "chandos":    ("Sir John Chandos", "anchors/chandos.png", "Very old, wise, wry, warm; the legend of the army."),
    "oliver":     ("Sir Oliver Buttesthorn", "anchors/oliver.png", "Blustery fat knight, food-obsessed, quick to rage and to laugh."),
    "simon":      ("Black Simon", "anchors/simon.png", "Grim flat veteran voice; vengeance, not gold."),
    "abbot":      ("Abbot Berghersh", "anchors/abbot.png", "Thin ascetic authority; thunders when roused."),
    "johnston":   ("Johnston (old master-bowman)", None, "Grizzled Lancashire veteran; modest, dry, dies at the last stand."),
    "socman":     ("The Socman of Minstead", "anchors/socman.png", "Alleyne's villain brother: stormy, sneering Saxon menace."),
}


def pitch(mp3: Path) -> str:
    out = subprocess.run(["python3", str(PITCH), str(mp3)],
                         capture_output=True, text=True).stdout
    m = re.search(r"median f0 = (\d+) Hz", out)
    return f"{m.group(1)} Hz" if m else "?"


sections = []
for role, (line, cands) in ROLES.items():
    name, img, brief = ROLE_INFO[role]
    img_html = (f'<a href="{img}" target="_blank"><img src="{img}" loading="lazy"></a>'
                if img and (PROJ / img).exists() else '<div class="noimg">no anchor</div>')
    cand_rows = []
    for i, slug in enumerate(cands):
        vname, vid, src = VOICES[slug]
        mp3 = VO / f"{role}__{slug}.mp3"
        if not mp3.exists():
            cand_rows.append(f'<div class="cand missing">{html.escape(vname)} — audition missing</div>')
            continue
        tag = '<span class="rec">1st choice</span>' if i == 0 else ""
        srcnote = "in account" if src == "account" else "library (re-add to use)"
        cand_rows.append(f"""
    <div class="cand">
      <div class="candhead"><b>{html.escape(vname)}</b> {tag}
        <span class="vid">{vid} · {srcnote} · {pitch(mp3)}</span></div>
      <audio controls preload="none" src="vo_auditions/{mp3.name}"></audio>
    </div>""")
    sections.append(f"""
<div class="role" id="{role}">
  {img_html}
  <div class="meta">
    <h2>{html.escape(name)}</h2>
    <p class="brief">{html.escape(brief)}</p>
    <p class="line">Audition line: “{html.escape(line)}”</p>
    {''.join(cand_rows)}
  </div>
</div>""")

page = f"""<!doctype html><meta charset="utf-8"><title>The White Company — voice casting</title>
<style>
body {{ background:#141417; color:#e8e8ea; font: 15px/1.5 -apple-system, sans-serif;
       max-width: 1000px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-weight: 600; }}
.role {{ display:flex; gap:20px; margin:22px 0; padding:16px; background:#1d1d22;
         border-radius:10px; }}
.role img {{ width:180px; border-radius:8px; flex-shrink:0; align-self:flex-start; }}
.noimg {{ width:180px; height:240px; flex-shrink:0; display:flex; align-items:center;
          justify-content:center; color:#556; border:1px dashed #334; border-radius:8px; }}
.meta {{ flex:1; }} .meta h2 {{ margin:0 0 4px; font-size:19px; color:#d99; }}
.brief {{ color:#aab; margin:2px 0 6px; }}
.line {{ color:#ffd479; font-size:13px; margin:4px 0 12px; }}
.cand {{ margin:10px 0; padding:10px 12px; background:#17171b; border-radius:8px; }}
.cand.missing {{ color:#a66; }}
.candhead {{ margin-bottom:6px; }}
.vid {{ color:#778; font-size:12px; margin-left:8px; }}
.rec {{ background:#3a5f3a; font-size:11px; padding:2px 8px; border-radius:10px;
        margin-left:6px; vertical-align:middle; }}
audio {{ width:100%; max-width:520px; height:34px; }}
p.note {{ color:#99a; }}
</style>
<h1>THE WHITE COMPANY — voice casting</h1>
<p class="note">Each role: anchor portrait + ElevenLabs candidates reading a verbatim-Doyle
audition line (eleven_multilingual_v2). Pitch is median f0 measured by pitch_check.py —
note that heavy rasp reads artificially high. Library voices were deleted after the
audition TTS; re-add by voice id when cast. Pipeline: TTS the shot lines with the chosen
voice → per-speaker mp3s as Seedance <code>--audio</code> refs.</p>
{''.join(sections)}
"""
(PROJ / "casting.html").write_text(page)
print(f"wrote casting.html ({len(ROLES)} roles, "
      f"{sum(len(c) for _, c in ROLES.values())} auditions)")
