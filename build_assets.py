#!/usr/bin/env python3
"""Builds README.md + assets/*.svg (dark and light) that mirror the HTML profile.
Run from this folder:  python3 build_assets.py
"""
import os, textwrap
from html import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
os.makedirs(A, exist_ok=True)
FONT = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

T = {
    "dark": dict(bg="#0c0f15", bg2="#121824", surface="#141a24", line="#222b3a", ink="#e8eef7", muted="#8a97aa",
                 blue="#6fa8e8", blue2="#a9d1ff", on="#07121f",
                 h=["#1a212d", "#2b4468", "#4a76ad", "#6fa3dd", "#aad2ff"],
                 pa="#4a76ad", pb="#2b4468", pt="#ffffff", ps="#dbe9fb", pm="#c3d9f5", ptag="#0c0f15", ptagc="#a9d1ff"),
    "light": dict(bg="#f4f7fb", bg2="#e6eefa", surface="#ffffff", line="#d6e0ee", ink="#0e1a2b", muted="#566a85",
                  blue="#2f6fbd", blue2="#1d4f90", on="#ffffff",
                  h=["#e3e9f2", "#bcd3f1", "#86b0e6", "#4f8bd6", "#1f5fb4"],
                  pa="#86b0e6", pb="#bcd3f1", pt="#07121f", ps="#17335a", pm="#17335a", ptag="#ffffff", ptagc="#1d4f90"),
}

def svg(w, h, body, defs="", style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{FONT}" role="img"><defs>{defs}</defs><style>{style}</style>{body}</svg>')

def save(name, mode, content):
    with open(os.path.join(A, f"{name}-{mode}.svg"), "w", encoding="utf-8") as f:
        f.write(content)

def txt(x, y, s, size=16, fill="#fff", weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'

GH = "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"

# ---------- header ----------
BIOS = ["Medical electronics & embedded instrumentation.", "Biomedical signal processing.",
        "Vascular health research.", "Engineering technology for better healthcare."]

def header(t):
    defs = (f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg2"]}"/><stop offset="1" stop-color="{t["bg"]}"/></linearGradient>')
    style = ".b{opacity:0;animation:cyc 12s infinite}.b0{opacity:1}@keyframes cyc{0%{opacity:0}4%{opacity:1}22%{opacity:1}26%{opacity:0}100%{opacity:0}}"
    b = f'<rect x="1" y="1" width="958" height="298" rx="24" fill="url(#g)" stroke="{t["line"]}" stroke-width="2"/>'
    b += txt(72, 130, "Nadiya Azka", 60, t["ink"], 600, extra='letter-spacing="-2"')
    b += (f'<text x="72" y="172" font-size="18" font-weight="500" fill="{t["ink"]}">@Azka79'
          f'<tspan fill="{t["muted"]}">   •   </tspan>LinkedIn<tspan fill="{t["muted"]}">   •   </tspan>Surabaya, ID</text>')
    b += txt(72, 210, "M.Eng. Student at ITS.", 19, t["ink"], 600)
    for i, s in enumerate(BIOS):
        b += txt(72, 238, s, 19, t["muted"], 400, extra=f'class="b{" b0" if i == 0 else ""}" style="animation-delay:{i*3}s"')
    b += txt(900, 190, "GPA 3.75", 18, t["muted"], 500, "end") + txt(900, 218, "5+ Years in ITS", 18, t["muted"], 500, "end")
    return svg(960, 300, b, defs, style)

# ---------- journey heatmap (dates from the CV) ----------
MN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ITEMS = [
    ("B.Eng. Biomedical Engineering, ITS", (2021, 8), (2025, 8)),
    ("Student Research Assistant, ITS", (2023, 9), (2025, 7)),
    ("Coordinator, Biomedical Signal Processing Lab", (2024, 9), (2025, 7)),
    ("M.Eng. Electrical & Electronics Engineering, ITS", (2026, 2), (2026, 11)),
    ("Graduate Research Assistant, ITS", (2026, 3), (2026, 11)),
    ("Practicum Assistant, ITS", (2024, 3), (2024, 7)),
    ("Quality Control Intern, PT TESENA INOVINDO", (2024, 1), (2024, 2)),
    ("Technical Training Assistant, TNI AU", (2023, 11), (2023, 11)),
]
idx = lambda y, m: y * 12 + m - 1
START, END = idx(2021, 8), idx(2026, 11)

def journey(t):
    left, cw, ch, gap, top = 68, 66.8, 36, 6, 92
    style = ".c{animation:in .5s ease backwards}@keyframes in{from{opacity:0}}"
    b = ""
    active = 0
    cells = ""
    n = 0
    for r, y in enumerate(range(2021, 2027)):
        cells += txt(24, top + r * (ch + gap) + ch / 2 + 5, str(y), 13, t["muted"])
        for m in range(1, 13):
            i = idx(y, m)
            x = left + (m - 1) * (cw + gap)
            yy = top + r * (ch + gap)
            on = [it for it in ITEMS if idx(*it[1]) <= i <= idx(*it[2])]
            if i < START or i > END:
                cells += f'<rect class="c" opacity=".35" x="{x:.1f}" y="{yy}" width="{cw}" height="{ch}" rx="6" fill="{t["h"][0]}" style="animation-delay:{n*10}ms"/>'
            else:
                if on:
                    active += 1
                lvl = min(len(on), 4)
                st = f' stroke="{t["ink"]}" stroke-width="2"' if i == END else ""
                cells += f'<rect class="c" x="{x:.1f}" y="{yy}" width="{cw}" height="{ch}" rx="6" fill="{t["h"][lvl]}"{st} style="animation-delay:{n*10}ms"/>'
            n += 1
    b += txt(24, 34, "Academic & Professional Journey", 17, t["ink"], 600) + txt(360, 34, f"{active} active months", 15, t["muted"], 500)
    b += txt(936, 34, "Each square is one month, 2021 to now. Brighter means more running at once.", 14, t["blue2"], 500, "end")
    for m in range(12):
        b += txt(left + m * (cw + gap) + cw / 2, 80, MN[m], 13, t["muted"], 400, "middle")
    b += cells
    H = top + 6 * (ch + gap) + 40
    ly = H - 22
    b += txt(780, ly + 12, "Fewer", 13, t["muted"], 400, "end")
    for k in range(5):
        b += f'<rect x="{790+k*20}" y="{ly}" width="14" height="14" rx="4" fill="{t["h"][k]}"/>'
    b += txt(896, ly + 12, "More", 13, t["muted"], 400, "start")
    return svg(960, H, b, "", style), active

# ---------- section headings ----------
def heading(t, title, sub=None):
    h = 78 if sub else 48
    b = txt(0, 36, title, 34, t["ink"], 600, extra='letter-spacing="-0.5"')
    if sub:
        b += txt(0, 66, sub, 16, t["muted"])
    return svg(960, h, b)

# ---------- facts ----------
FACTS = [("Now", "M.Eng. Electrical & Electronics Engineering, ITS (Feb 2026–present)"),
         ("Research", "Graduate Research Assistant, vascular health and instrumentation"),
         ("Before", "B.Eng. Biomedical Engineering, ITS (2021–2025)")]

def facts(t):
    w, g = 310, 15
    b = ""
    for i, (lab, s) in enumerate(FACTS):
        x = i * (w + g)
        b += f'<rect x="{x+1}" y="1" width="{w-2}" height="118" rx="14" fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="2"/>'
        b += txt(x + 18, 32, lab, 13, t["blue"], 500)
        for k, ln in enumerate(textwrap.wrap(s, 36)):
            b += txt(x + 18, 58 + k * 22, ln, 15, t["ink"])
    return svg(960, 120, b)

# ---------- publication ----------
TITLE = ["Heartbeat Signal Imputation in Doppler Radar Using", "Bidirectional Long Short-Term Memory for Random", "Body Movement Mitigation"]

def publication(t):
    defs = f'<linearGradient id="p" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["pa"]}"/><stop offset=".7" stop-color="{t["pb"]}"/></linearGradient>'
    b = f'<rect x="1" y="1" width="958" height="338" rx="22" fill="url(#p)" stroke="{t["pa"]}" stroke-width="2"/>'
    b += f'<rect x="36" y="32" width="250" height="32" rx="16" fill="{t["ptag"]}"/>' + txt(161, 54, "Publication · IEEE Access, 2026", 14, t["ptagc"], 600, "middle")
    for i, ln in enumerate(TITLE):
        b += txt(36, 120 + i * 40, ln, 31, t["pt"], 600, extra='letter-spacing="-0.6"')
    b += txt(36, 262 - 12, "Azka, N., et al.", 17, t["ps"], 500)
    for x, lab, val in [(36, "Journal", "IEEE Access"), (270, "Volume", "14"), (400, "Year", "2026"), (540, "DOI", "10.1109/ACCESS.2026.3738353")]:
        b += txt(x, 282, lab, 13, t["pm"]) + txt(x, 308, val, 18, t["pt"], 600)
    return svg(960, 340, b, defs)

def award(t):
    defs = f'<linearGradient id="p" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["pa"]}"/><stop offset=".7" stop-color="{t["pb"]}"/></linearGradient>'
    b = f'<rect x="1" y="1" width="958" height="338" rx="22" fill="url(#p)" stroke="{t["pa"]}" stroke-width="2"/>'
    b += f'<rect x="36" y="32" width="250" height="32" rx="16" fill="{t["ptag"]}"/>' + txt(161, 54, "Award · GEMASTIK XVII 2024", 14, t["ptagc"], 600, "middle")
    b += txt(36, 150, "Gold Medalist", 44, t["pt"], 600, extra='letter-spacing="-1"')
    b += txt(36, 200, "Division 7: ICT Scientific Paper", 24, t["ps"], 500)
    for x, lab, val in [(36, "Competition", "GEMASTIK XVII"), (330, "Division", "7"), (430, "Year", "2024"), (560, "Award", "Gold Medalist")]:
        b += txt(x, 282, lab, 13, t["pm"]) + txt(x, 308, val, 18, t["pt"], 600)
    return svg(960, 340, b, defs)

# ---------- skills ----------
SK = {"Software": ["Python", "C++", "MATLAB", "Git & GitHub", "VS Code", "Blender", "OpenCV", "LabVIEW"],
      "Hardware": ["STM32", "ESP32", "Atmel", "Raspberry Pi", "Analog circuit design", "PCB prototyping", "KiCad (advanced)", "Proteus"],
      "Standards": ["ISO 14971 risk management", "ISO 13485 quality management", "IEC 60601 electrical safety"],
      "Practice": ["Signal acquisition", "Troubleshooting", "Preventive maintenance", "Calibration", "Electrical safety testing"]}

def skills(t):
    b, y = "", 0
    for grp, lst in SK.items():
        b += txt(2, y + 18, grp, 14, t["blue"], 600)
        y += 30
        x = 0
        for s in lst:
            w = len(s) * 8 + 30
            if x + w > 960:
                x, y = 0, y + 46
            b += f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="36" rx="10" fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="2"/>'
            b += txt(x + w / 2, y + 24, s, 15, t["ink"], 400, "middle")
            x += w + 8
        y += 62
    return svg(960, y, b)

# ---------- learning / awards ----------
CERTS = ["ISO 14971 Medical Device Development & Risk Management", "Advanced PCB Design with KiCad 9",
         "Diploma in Python Programming", "Health and Technology Research Ethics", "3D Design with Blender"]
AW = [("Gold Medalist, GEMASTIK XVII 2024", "Division 7: ICT Scientific Paper."),
      ("Angka Nitisastro Top Tier Scholar, 2026", "Recognized for academic and research potential.")]

def learning(t):
    b = ""
    for i, (a, d) in enumerate(AW):
        x = i * 477
        b += f'<rect x="{x+1}" y="1" width="461" height="104" rx="14" fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="2"/>'
        b += txt(x + 22, 44, a, 19, t["ink"], 600) + txt(x + 22, 76, d, 15, t["muted"])
    b += txt(0, 156, "Learning and certifications", 21, t["ink"], 600)
    for i, c in enumerate(CERTS):
        y = 176 + i * 44
        b += f'<rect x="2" y="{y+14}" width="10" height="10" rx="3" fill="{t["h"][3]}"/>' + txt(26, y + 25, c, 16, t["ink"])
        b += f'<line x1="0" y1="{y+40}" x2="960" y2="{y+40}" stroke="{t["line"]}" stroke-width="1.5"/>'
    return svg(960, 176 + 5 * 44 + 4, b)

# ---------- buttons, footer ----------
def chip(t, s):
    w = int(len(s) * 8.4 + 34)
    return svg(w, 38, f'<rect x="1" y="1" width="{w-2}" height="36" rx="10" fill="{t["blue"]}"/>' + txt(w / 2, 24, s, 15, t["on"], 600, "middle"))

def button(t, s, primary):
    w = int(len(s) * 8.8 + 48)
    if primary:
        b = f'<rect width="{w}" height="44" rx="11" fill="{t["blue"]}"/>' + txt(w / 2, 28, s, 15, t["on"], 600, "middle")
    else:
        b = f'<rect x="1" y="1" width="{w-2}" height="42" rx="10" fill="none" stroke="{t["line"]}" stroke-width="2"/>' + txt(w / 2, 28, s, 15, t["ink"], 600, "middle")
    return svg(w, 44, b)

def gh_button(t):
    label = "GitHub · Azka79"
    w = int(len(label) * 8.6 + 78)
    b = f'<rect x="1" y="1" width="{w-2}" height="42" rx="10" fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="2"/>'
    b += f'<g transform="translate(20,11) scale(2)" fill="{t["ink"]}"><path d="{GH}"/></g>'
    b += txt(56, 27, label, 15, t["ink"], 600)
    return svg(w, 44, b)

def wide_button(t, s):
    b = f'<rect x="1" y="1" width="958" height="42" rx="11" fill="{t["blue"]}"/>' + txt(480, 28, s, 15, t["on"], 600, "middle")
    return svg(960, 44, b)

def footer(t):
    b = f'<line x1="0" y1="2" x2="960" y2="2" stroke="{t["line"]}" stroke-width="2"/>'
    b += txt(480, 76, "Let’s build better healthcare technology", 30, t["ink"], 600, "middle", 'letter-spacing="-0.5"')
    b += txt(480, 112, "Open to research collaboration and biomedical R&D conversations.", 17, t["muted"], 400, "middle")
    return svg(960, 130, b)

for m, t in T.items():
    save("header", m, header(t))
    save("h-highlights", m, heading(t, "Highlights", "Publication and awards."))
    save("h-about", m, heading(t, "About"))
    save("h-skills", m, heading(t, "Technical skills", "Grouped by area."))
    save("h-contributions", m, heading(t, "GitHub Contributions", "Live activity: commits, pull requests, issues and reviews."))
    save("facts", m, facts(t))
    save("publication", m, publication(t))
    save("award", m, award(t))
    save("skills", m, skills(t))
    save("footer", m, footer(t))
    save("btn-doi", m, wide_button(t, "Open paper (DOI)"))
    save("btn-linkedin", m, button(t, "Message on LinkedIn", True))
    save("btn-github", m, button(t, "View GitHub", False))

def pic(name, alt, w="100%"):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">'
            f'<img alt="{esc(alt)}" src="assets/{name}-dark.svg"' + (f' width="{w}"' if w else '') + '></picture>')

README = f"""<!--
  Nadiya Azka profile README.
  Mirrors the HTML profile. GitHub cannot run CSS/JS, so visuals are themed SVGs in /assets
  (dark + light via <picture>) and interaction uses native <details>.
  Edit build_assets.py, then run: python3 build_assets.py
-->

<div align="center">
{pic("header", "Nadiya Azka. M.Eng. Student at ITS: medical electronics, embedded instrumentation, biomedical signal processing, vascular health research.")}
</div>

<br>

<div align="center">
{pic("h-contributions", "GitHub Contributions")}
<a href="https://github.com/Azka79">{pic("contributions", "Live GitHub contribution graph for Azka79 over the past year: commits, pull requests, issues and reviews, rendered in the profile blue palette with dark and light variants.")}</a>
</div>

<br>

<div align="center">
{pic("h-highlights", "Highlights")}
{pic("publication", "Publication in IEEE Access, 2026: Heartbeat Signal Imputation in Doppler Radar Using Bidirectional Long Short-Term Memory for Random Body Movement Mitigation. Azka, N., et al. Volume 14. DOI 10.1109/ACCESS.2026.3738353")}
<br>
<a href="https://doi.org/10.1109/ACCESS.2026.3738353">{pic("btn-doi", "Open paper (DOI)", "100%")}</a>
{pic("award", "Award: Gold Medalist, GEMASTIK XVII 2024, Division 7 ICT Scientific Paper.")}
</div>

<br>

<div align="center">
{pic("h-about", "About")}
</div>

I'm an Electrical Engineering master's student at Institut Teknologi Sepuluh Nopember (ITS), specializing in Medical Electronics and Embedded Instrumentation, with a bachelor's in Biomedical Engineering from ITS.

I like the whole engineering loop: designing circuits, prototyping hardware, acquiring physiological signals, processing them, then testing and validating the result.

Interested in biomedical R&D, medical electronics, research collaboration and healthcare technology.

<div align="center">
{pic("facts", "Now: M.Eng. at ITS. Research: Graduate Research Assistant. Before: B.Eng. Biomedical Engineering, ITS.")}
</div>

<br>

<div align="center">
{pic("h-skills", "Technical skills")}
{pic("skills", "Skills. Software: Python, C++, MATLAB, Git and GitHub, VS Code, Blender, OpenCV, LabVIEW. Hardware: STM32, ESP32, Atmel, Raspberry Pi, analog circuit design, PCB prototyping, KiCad, Proteus. Standards: ISO 14971, ISO 13485, IEC 60601. Practice: signal acquisition, troubleshooting, preventive maintenance, calibration, electrical safety testing.")}
</div>

<br>

<div align="center">
{pic("footer", "Let's build better healthcare technology. Open to research collaboration and biomedical R&D conversations.")}
<a href="https://linkedin.com/in/nadiyaazkaa">{pic("btn-linkedin", "Message on LinkedIn", "")}</a>
&nbsp;
<a href="https://github.com/Azka79">{pic("btn-github", "View GitHub", "")}</a>
</div>
"""

with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as f:
    f.write(README)
print("ok")
