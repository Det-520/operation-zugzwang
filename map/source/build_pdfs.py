import os, re, sys
from playwright.sync_api import sync_playwright

# usage: build_pdfs.py <map.svg> <out_dir> <name>   writes <name>_full.pdf and <name>_tiles_letter.pdf
SRC, D, NAME = sys.argv[1], os.path.join(os.path.abspath(sys.argv[2]), ""), sys.argv[3]
svg = open(SRC).read()
# let CSS size the root element
svg = re.sub(r'(<svg[^>]*?) width="1580" height="1140"', r'\1', svg, count=1)
SVG_W, SVG_H = 1580, 1140
ASPECT = SVG_W / SVG_H

# ---------------------------------------------------------------- full map, one page
FULL_W_IN = 21.0
FULL_H_IN = FULL_W_IN / ASPECT
full_html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: {FULL_W_IN}in {FULL_H_IN:.4f}in; margin: 0 }}
html, body {{ margin: 0; padding: 0; }}
svg {{ display: block; width: {FULL_W_IN}in; height: {FULL_H_IN:.4f}in; }}
</style></head><body>{svg}</body></html>"""

# ---------------------------------------------------------------- 2 x 2 letter tiles
# Each tile is laid out landscape, then turned onto a portrait page (top of the map
# at the left edge), so the tiles print in the same orientation as the handouts.
PW, PH = 1056.0, 816.0                       # the landscape tile, CSS px (96 dpi)
WIN_W = 1008.0                               # 10.5 in trim window per tile (0.25 in side margins)
S = WIN_W / (SVG_W / 2)                      # svg px -> css px
WIN_H = (SVG_H / 2) * S                      # about 7.10 in
X0 = (PW - WIN_W) / 2
Y0 = (PH - WIN_H) / 2

names = {(0, 0): "TILE 1  (top-left)", (0, 1): "TILE 2  (top-right)", (1, 0): "TILE 3  (bottom-left)", (1, 1): "TILE 4  (bottom-right)"}
join = {(0, 0): "joins 2 on the right, 3 below", (0, 1): "joins 1 on the left, 4 below",
        (1, 0): "joins 4 on the right, 1 above", (1, 1): "joins 3 on the left, 2 above"}

def marks():
    m = []
    L, R, T, B = X0, X0 + WIN_W, Y0, Y0 + WIN_H
    for x in (L, R):
        for y in (T, B):
            sx = -1 if x == L else 1
            sy = -1 if y == T else 1
            m.append(f'<line x1="{x + sx*3:.1f}" y1="{y:.1f}" x2="{x + sx*19:.1f}" y2="{y:.1f}"/>')
            m.append(f'<line x1="{x:.1f}" y1="{y + sy*3:.1f}" x2="{x:.1f}" y2="{y + sy*19:.1f}"/>')
    # mid-edge alignment ticks
    cx, cy = (L + R) / 2, (T + B) / 2
    for x in (cx,):
        m.append(f'<line x1="{x:.1f}" y1="{T-3:.1f}" x2="{x:.1f}" y2="{T-15:.1f}"/><line x1="{x:.1f}" y1="{B+3:.1f}" x2="{x:.1f}" y2="{B+15:.1f}"/>')
    m.append(f'<line x1="{L-3:.1f}" y1="{cy:.1f}" x2="{L-15:.1f}" y2="{cy:.1f}"/><line x1="{R+3:.1f}" y1="{cy:.1f}" x2="{R+15:.1f}" y2="{cy:.1f}"/>')
    return "".join(m)

pages = []
for (r, c), nm in names.items():
    tx, ty = -c * WIN_W, -r * WIN_H
    pages.append(f"""
<section class="page"><div class="turn">
  <div class="win"><div class="inner" style="transform: translate({tx:.2f}px,{ty:.2f}px) scale({S:.5f});">{svg}</div></div>
  <svg class="over" viewBox="0 0 {PW:.0f} {PH:.0f}" width="{PW:.0f}" height="{PH:.0f}">
    <g stroke="#000" stroke-width="0.8" fill="none">{marks()}</g>
    <g font-family="Inter, Arial, sans-serif" fill="#222" font-size="10">
      <text x="{X0:.1f}" y="{Y0 - 26:.1f}" font-weight="700" letter-spacing="1">{nm}</text>
      <text x="{X0 + 150:.1f}" y="{Y0 - 26:.1f}" fill="#555">{join[(r, c)]}</text>
      <text x="{X0:.1f}" y="{Y0 + WIN_H + 34:.1f}" fill="#555">Trim to the corner marks and butt the four tiles edge to edge. Assembled map is 21 x 15.2 in.</text>
    </g>
  </svg>
</div></section>""")

tiles_html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: 8.5in 11in; margin: 0 }}
html, body {{ margin: 0; padding: 0; }}
.page {{ position: relative; width: {PH}px; height: {PW}px; overflow: hidden; page-break-after: always; break-after: page; background: #fff; }}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
.turn {{ position: absolute; left: 0; top: 0; width: {PW}px; height: {PH}px; transform-origin: 0 0; transform: translate(0, {PW}px) rotate(-90deg); }}
.win {{ position: absolute; left: {X0:.2f}px; top: {Y0:.2f}px; width: {WIN_W}px; height: {WIN_H:.2f}px; overflow: hidden; }}
.inner {{ position: absolute; left: 0; top: 0; width: {SVG_W}px; height: {SVG_H}px; transform-origin: 0 0; }}
.inner svg {{ display: block; width: {SVG_W}px; height: {SVG_H}px; }}
.over {{ position: absolute; left: 0; top: 0; }}
</style></head><body>{''.join(pages)}</body></html>"""

open(D + "_full.html", "w").write(full_html)
open(D + "_tiles.html", "w").write(tiles_html)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
    pg = b.new_page()
    pg.goto("file://" + D + "_full.html"); pg.wait_for_timeout(800)
    pg.pdf(path=D + NAME + "_full.pdf", width=f"{FULL_W_IN}in", height=f"{FULL_H_IN:.4f}in", print_background=True,
           margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, prefer_css_page_size=True)
    pg.goto("file://" + D + "_tiles.html"); pg.wait_for_timeout(1200)
    pg.pdf(path=D + NAME + "_tiles_letter.pdf", width="8.5in", height="11in", print_background=True,
           margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, prefer_css_page_size=True)
    b.close()
for f in ("_full.html", "_tiles.html"): os.remove(D + f)
print("window", WIN_W / 96, WIN_H / 96, "in; offsets", X0 / 96, Y0 / 96)
