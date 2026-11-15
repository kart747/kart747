"""Neofetch-style terminal card: ASCII Kali + profile info. FREEZE=t arg renders a paused frame."""
import sys, html
freeze = float(sys.argv[2]) if len(sys.argv) > 2 else None
TW = 47
def sym(left, inner, edge_l="|", edge_r="|"):
    right = left[::-1]
    return left + edge_l + inner + edge_r + right
INNER = [
    "             /\\            ",
    "            (@@)           ",
    "  .--.       \\/       .--. ",
    " ( @@ )             ( @@ ) ",
    "  '--'       /\\       '--' ",
    "            /  \\           ",
    "    .-----------------.    ",
    "   / V V V V V V V V V \\   ",
    "   \\ ^ ^ ^ ^ ^ ^ ^ ^ ^ /   ",
]
HAIR = [",,,,", ",;;;;;", ";;;;;;;", ";;;;;;;;", ";;;;;;;;", ";;;;;;;;", ";;;;;;;;", ";;;;;;;;", ";;;;;;;;"]
rows = [".     .     .", "/ \\   / \\   / \\", ".   /   \\ /   \\ /   \\   .",
        "/ \\_/  *  V  *  V  *  \\_/ \\", "|___________________________|"]
rows += [sym(h, i) for h, i in zip(HAIR, INNER)]
rows += [
    ";;;;;;;;\\    '-----.   .-----'    /;;;;;;;;",
    ";;;;;;;;\\         |   |         /;;;;;;;;",
    ";;;;;;;;'.       |   |       .';;;;;;;;",
    ";;;;;;;;;'-.    |   |    .-';;;;;;;;;",
    ";;;;;;;;;;;'--.|   |.--';;;;;;;;;;;",
    ";;;;;;;;;;;;;\\   /;;;;;;;;;;;;;",
    ";;;;;;;;;;;;\\_/;;;;;;;;;;;;",
    "(o)" * 6 + "V" + "(o)" * 6,
]
for r in rows: assert len(r) % 2 == 1, (len(r), r)
ART = [r.center(TW).rstrip() for r in rows]
C = TW // 2
COL = {"g": "#e9b949", "h": "#6e6a86", "r": "#ff3b3b", "b": "#e8e1d6", "f": "#a9a6b8", "w": "#f4f1ea"}
def cls(r, c, ch):
    if ch == " ": return "f"
    if r <= 4: return "g"
    if ch in ",;": return "h"
    if r == len(ART) - 1: return "r" if ch == "V" else "b"
    if 5 <= r <= 7 and abs(c - C) <= 2: return "r"           # third eye
    if ch == "@": return "r"
    if r in (12, 13) and ch in "V^": return "w"              # fangs
    if r >= 14 and abs(c - C) <= 3 and ch in "|\\/_": return "r"  # tongue
    return "f"

FS, LH, CW = 14, 18, 8.43          # font size, line height, approx char width
X0, Y0 = 28, 64
INFO_X = X0 + TW * CW + 16
info = [
    [("#ff3b3b", "kart747"), ("#a9a6b8", "@"), ("#e9b949", "github")],
    [("#55526a", "-" * 22)],
    [("#ff3b3b", "name    "), ("#e8e1d6", "Karthik G K")],
    [("#ff3b3b", "role    "), ("#e8e1d6", "CS student, ML engineer")],
    [("#ff3b3b", "focus   "), ("#e8e1d6", "computer vision, deep learning")],
    [("#ff3b3b", "        "), ("#e8e1d6", "GenAI, embedded systems")],
    [("#ff3b3b", "stack   "), ("#e8e1d6", "Python, PyTorch, C++, TypeScript")],
    [("#ff3b3b", "        "), ("#e8e1d6", "Flutter, FastAPI, Docker")],
    [("#ff3b3b", "built   "), ("#e8e1d6", "AmazonML, Greenroom, mynah")],
    [("#ff3b3b", "        "), ("#e8e1d6", "autoliv-dms, TruthLens")],
    [("#ff3b3b", "status  "), ("#e8e1d6", "open to internships")],
    [],
    [("#ff3b3b", "uptime  "), ("#e8e1d6", "brute force first, then optimise")],
]
W = int(INFO_X + 42 * CW + 24)
H = Y0 + len(ART) * LH + 40
LOOP = 14.0
def a(name, delay, dur=LOOP):
    if freeze is not None:
        return f"animation:{name} {dur}s linear infinite paused;animation-delay:{delay - freeze:.2f}s"
    return f"animation:{name} {dur}s linear infinite;animation-delay:{delay:.2f}s"

o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"DejaVu Sans Mono","Liberation Mono",monospace;font-size:{FS}px;white-space:pre}}
@keyframes in{{0%{{opacity:0}}0.6%,96%{{opacity:1}}100%{{opacity:0}}}}
@keyframes glow{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
</style>
<rect width="{W}" height="{H}" rx="12" fill="#0c0b10"/>
<rect width="{W}" height="34" rx="12" fill="#17151d"/><rect y="22" width="{W}" height="12" fill="#17151d"/>
<circle cx="22" cy="17" r="6" fill="#ff5f57"/><circle cx="42" cy="17" r="6" fill="#febc2e"/><circle cx="62" cy="17" r="6" fill="#28c840"/>
<text x="{W/2}" y="22" fill="#6e6a86" text-anchor="middle" font-size="12">kart747@github: ~</text>
<text x="{X0}" y="{Y0 - 8}" fill="#e8e1d6" xml:space="preserve" style="{a('in', 0)}"><tspan fill="#ff3b3b">❯</tspan> neofetch</text>''']

for r, line in enumerate(ART):
    y = Y0 + (r + 1) * LH
    runs, cur, buf = [], None, ""
    for c, ch in enumerate(line):
        k = cls(r, c, ch)
        if k != cur and buf: runs.append((cur, buf)); buf = ""
        cur = k; buf += ch
    if buf: runs.append((cur, buf))
    spans = "".join(
        f'<tspan fill="{COL[k]}"' + (f' style="{a("glow", 0, 2.4)}"' if k == "r" else "") + f'>{html.escape(t)}</tspan>'
        for k, t in runs)
    o.append(f'<text x="{X0}" y="{y}" xml:space="preserve" style="opacity:0;{a("in", 0.8 + r * 0.09)}">{spans}</text>')

for i, row in enumerate(info):
    y = Y0 + (i + 1) * LH
    spans = "".join(f'<tspan fill="{c}">{html.escape(t)}</tspan>' for c, t in row)
    o.append(f'<text x="{INFO_X:.0f}" y="{y}" xml:space="preserve" style="opacity:0;{a("in", 3.0 + i * 0.12)}">{spans}</text>')

by = Y0 + (len(info) + 2) * LH - 12
for i, c in enumerate(["#2a2733", "#ff3b3b", "#e9b949", "#a9a6b8", "#6e6a86", "#e8e1d6", "#8b1e2d", "#f4f1ea"]):
    o.append(f'<rect x="{INFO_X + i * 26:.0f}" y="{by}" width="24" height="14" fill="{c}" style="opacity:0;{a("in", 4.8 + i * 0.05)}"/>')

py = Y0 + (len(ART) + 1) * LH + 12
o.append(f'<text x="{X0}" y="{py}" fill="#e8e1d6" xml:space="preserve" style="opacity:0;{a("in", 5.4)}"><tspan fill="#ff3b3b">❯</tspan> </text>')
o.append(f'<rect x="{X0 + 2 * CW:.0f}" y="{py - 13}" width="8" height="16" fill="#e8e1d6" style="{a("blink", 0, 1.0)}"/>')
o.append("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
