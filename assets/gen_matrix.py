#!/usr/bin/env python3
"""Deterministic generator for an original Matrix-rain banner SVG (Tokyonight palette)."""
import random

W, H = 1200, 220
TITLE_H = 30
TOP = TITLE_H + 8          # content top
BOT = H - 8               # content bottom
LINE = 20                 # vertical glyph spacing
PERIOD = 11               # glyphs per period (PERIOD*LINE ~= one screen)
TRAVEL = PERIOD * LINE    # 220 -> seamless loop distance
COL_W = 26                # horizontal spacing between columns
FONT = 16

GLYPHS = list("0123456789ABCDEF<>/\\|=+*$#%01")
# matrix-ish palette, weighted toward green/cyan
COLORS = ["#9ece6a", "#9ece6a", "#7dcfff", "#7dcfff", "#7aa2f7", "#bb9af7"]
HEAD = "#c0caf5"          # bright leading glyph

rnd = random.Random(1337)  # fixed seed -> reproducible

def esc(c):
    return {"<": "&lt;", ">": "&gt;", "&": "&amp;"}.get(c, c)

out = []
out.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="\'Courier New\', Courier, monospace" font-size="{FONT}" font-weight="bold">'
)
out.append('<defs>')
out.append('<linearGradient id="medge" x1="0" y1="0" x2="1" y2="0">'
           '<stop offset="0" stop-color="#f7768e"/><stop offset="0.5" stop-color="#7aa2f7"/>'
           '<stop offset="1" stop-color="#bb9af7"/></linearGradient>')
out.append('<clipPath id="mclip"><rect x="6" y="' + str(TITLE_H) +
           f'" width="{W-12}" height="{H-TITLE_H-6}" rx="8"/></clipPath>')
out.append('</defs>')

# frame + title bar
out.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12" fill="#1a1b26" '
           'stroke="url(#medge)" stroke-width="2"/>')
out.append(f'<path d="M2 14a12 12 0 0 1 12-12h{W-28}a12 12 0 0 1 12 12v{TITLE_H-14}H2z" fill="#16161e"/>')
out.append('<circle cx="28" cy="16" r="6" fill="#f7768e"/>')
out.append('<circle cx="48" cy="16" r="6" fill="#e0af68"/>')
out.append('<circle cx="68" cy="16" r="6" fill="#9ece6a"/>')
out.append(f'<text x="{W//2}" y="21" text-anchor="middle" font-size="13" font-weight="normal" '
           'fill="#565f89">// incoming_data.stream — decrypting</text>')

# rain columns
out.append(f'<g clip-path="url(#mclip)">')
n_cols = (W - 24) // COL_W
for ci in range(n_cols):
    x = 18 + ci * COL_W + rnd.randint(-2, 2)
    base = rnd.choice(COLORS)
    dur = round(rnd.uniform(4.5, 11.0), 1)
    phase = round(rnd.uniform(0, dur), 2)          # negative begin -> desync
    # one period of glyphs with an opacity ramp (head brightest at the bottom)
    seq = [rnd.choice(GLYPHS) for _ in range(PERIOD)]
    # build a strip = 2 IDENTICAL periods so the translate loop is seamless
    y0 = TOP - TRAVEL
    out.append(f'<text x="{x}" y="{y0}" fill="{base}">')
    for rep in range(2):
        for i, g in enumerate(seq):
            # head = last glyph of each period (leads downward)
            t = i / (PERIOD - 1)
            op = round(0.10 + 0.90 * t, 2)
            dy = LINE if (rep or i) else 0
            if i == PERIOD - 1:
                out.append(f'<tspan x="{x}" dy="{dy}" fill="{HEAD}" '
                           f'fill-opacity="1">{esc(g)}</tspan>')
            else:
                out.append(f'<tspan x="{x}" dy="{dy}" fill-opacity="{op}">{esc(g)}</tspan>')
    out.append(
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 0;0 {TRAVEL}" dur="{dur}s" begin="-{phase}s" '
        f'calcMode="linear" repeatCount="indefinite"/>'
    )
    out.append('</text>')
out.append('</g>')
out.append('</svg>')

svg = "\n".join(out)
with open("assets/matrix.svg", "w") as f:
    f.write(svg + "\n")
print(f"wrote assets/matrix.svg  ({n_cols} columns, {len(svg)} bytes)")
