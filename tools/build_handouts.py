#!/usr/bin/env python3
"""Build the release PDFs in build/ from the handout markdown.

    tools/build_handouts.sh            # the usual way (sets up Python and Chromium on NixOS)
    python3 tools/build_handouts.py [--only NAME ...] [--html-only]

Needs: markdown-it-py, mdit-py-plugins, pypdf, playwright (with Chromium 131 or later,
for CSS page-margin boxes).

What it does:
- Renders each handout in RELEASES from markdown to HTML (CommonMark plus
  tables and task lists) and prints it to PDF in Chromium. The look follows the
  "Repo" theme at markdown.style (GitHub's markdown style) with one accent colour
  per audience: green public, red REDFOR, blue BLUEFOR, purple white cell.
  The running header (short name | // MARKING // | date) and the page numbers
  sit in CSS page-margin boxes, inside the page margins, so nothing is lost
  when a printer trims the edge.
- Takes the Tongue and Quill documents (commander's letters, RI-13, BI-05,
  BI-10, BI-11) from handouts/word/, built by tools/tq/build_tq.py.
  Run that first after changing one of them.
- Splices each side's intelligence products into one "Full Intel" PDF, each
  product starting on a new page.
- Copies the counters, the v10 map, and the white cell clock into place.
- Assembles the white cell's Print Packet (PACKET): everything one table
  prints to run the game, with the right number of copies, behind a cover
  sheet that lists it.

The markdown is the source. Audience lines and FORMAT NOTE blocks stay out of
the PDFs (the running header carries the audience). `render_markdown()` is
shared with tools/build_site.py.

Layout hooks in the markdown are HTML comments, so the files stay valid for
markdownlint (no inline HTML):
- `<!-- zz:NAME [NAME ...] -->` on the line before a table gives it those
  classes: `form` (labels left, room to write right; add `med` or `tall` for
  bigger boxes), `log` (rows to fill in), `track` (the track board), `markers`
  (cut-out track markers), `checkgrid` (a step-by-turn tick grid), `compact`
  (a dense reference table).
- `<!-- zz:begin cards -->` ... `<!-- zz:end -->` turns each `###` section in
  between into a cut-out card. `zz:begin slips` cuts the block into slips at
  each `---`, with a dashed cut line between them. Any other name just wraps
  the block.
- `<!-- pagebreak -->` starts a new page.
"""
import argparse
import glob
import html
import os
import re
import shutil
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
H = os.path.join(ROOT, "handouts")
FIN = os.path.join(ROOT, "build")
FONTS = os.path.join(ROOT, "tools", "fonts")

ASAP, WEEK = "Common Matrix - ASAP RELEASE", "Common Scenario - 1WK RELEASE"
RED, BLUE, WC = "REDFOR - 24H RELEASE", "BLUEFOR - 24H RELEASE", "White Cell"

MATRIX = ("Matrix Wargame", "// PUBLIC //", "October 2026")
PUBLIC = ("Operation Zugzwang", "// PUBLIC //", "12Nov2026")
RED_ONLY = ("Operation Zugzwang", "// REDFOR ONLY //", "12Nov2026")
BLUE_ONLY = ("Operation Zugzwang", "// BLUEFOR ONLY //", "12Nov2026")
WC_ONLY = ("Operation Zugzwang", "// WHITE CELL ONLY //", "12Nov2026")

# Accent and tint for each marking.
THEMES = {
    "PUBLIC": ("#1a7f37", "#dafbe1"),
    "REDFOR": ("#cf222e", "#ffebe9"),
    "BLUEFOR": ("#0969da", "#ddf4ff"),
    "WHITE CELL": ("#8250df", "#fbefff"),
}


def theme(header):
    mark = header[1] if header else "PUBLIC"
    for k, v in THEMES.items():
        if k in mark:
            return v
    return THEMES["PUBLIC"]


def intel(side):
    return sorted(glob.glob(os.path.join(H, side, "intel", f"{side[0].upper()}I-*.md")))


PACKET_NAME = "Print Packet - One Table.pdf"

# (folder, file name, header, sources). A source is a markdown path, or
# ("word", name) for a PDF from handouts/word/, or ("copy", path).
# "packet" builds the Print Packet from the files above it, so it comes last.
RELEASES = [
    (ASAP, "Player Rules Handbook.pdf", MATRIX, ["common/rules-handbook.md"]),
    (ASAP, "Player Forms and Templates.pdf", MATRIX, ["common/player-forms.md"]),
    (WEEK, "Scenario Brief.pdf", PUBLIC, ["common/scenario-brief.md"]),
    (WEEK, "Scenario Schedule.pdf", PUBLIC, ["common/scenario-schedule.md"]),
    (WEEK, "Starting Conditions.pdf", PUBLIC, ["common/starting-conditions.md"]),
    (WEEK, "map-full.pdf", None, [("copy", "map/maps/strait_map_v10_full.pdf")]),
    (WEEK, "map-tiles.pdf", None, [("copy", "map/maps/strait_map_v10_tiles_letter.pdf")]),
    (RED, "REDFOR - Commander's Letter.pdf", None, [("word", "REDFOR - Commander's Letter")]),
    (RED, "REDFOR Team Packet.pdf", RED_ONLY, ["redfor/team-packet.md"]),
    (RED, "REDFOR Order of Battle.pdf", RED_ONLY, ["redfor/order-of-battle.md"]),
    (RED, "REDFOR Intel - Read Me First.pdf", RED_ONLY, ["redfor/intel/00-read-me-first.md"]),
    (RED, "REDFOR Full Intel.pdf", RED_ONLY, "intel:redfor"),
    (RED, "counters.pdf", None, [("copy", "handouts/redfor/counters.pdf")]),
    (BLUE, "BLUEFOR - Commander's Letter.pdf", None, [("word", "BLUEFOR - Commander's Letter")]),
    (BLUE, "BLUEFOR Team Packet.pdf", BLUE_ONLY, ["bluefor/team-packet.md"]),
    (BLUE, "BLUEFOR Order of Battle.pdf", BLUE_ONLY, ["bluefor/order-of-battle.md"]),
    (BLUE, "BLUEFOR Intel - Read Me First.pdf", BLUE_ONLY, ["bluefor/intel/00-read-me-first.md"]),
    (BLUE, "BLUEFOR Full Intel.pdf", BLUE_ONLY, "intel:bluefor"),
    (BLUE, "counters.pdf", None, [("copy", "handouts/bluefor/counters.pdf")]),
    (WC, "White Cell Handbook.pdf", WC_ONLY, ["whitecell/handbook.md"]),
    (WC, "White Cell Checklist.pdf", WC_ONLY, ["whitecell/checklist.md"]),
    (WC, "White Cell Intelligence and Injects.pdf", WC_ONLY, ["whitecell/intel-and-injects.md"]),
    (WC, "Master Asset List.pdf", WC_ONLY, ["whitecell/master-asset-list.md"]),
    (WC, "White Cell Forms.pdf", WC_ONLY, ["whitecell/forms.md"]),
    (WC, "counters.pdf", None, [("copy", "handouts/whitecell/counters.pdf")]),
    (WC, "whitecell-clock.html", None, [("copy", "tools/whitecell-clock.html")]),
    (WC, PACKET_NAME, WC_ONLY, "packet"),
]

# What one table prints to run the game. (label, release file, section heading
# (its start, as printed) or None for the whole file, copies, note). Copies are per table; the packet
# holds them all, in this order.
PACKET = [
    ("White Cell Checklist", (WC, "White Cell Checklist.pdf"), None, 1, "Lead adjudicator. Tick it off through the afternoon."),
    ("White Cell Forms", (WC, "White Cell Forms.pdf"), None, 1, "Score sheet, track board and markers, objective status card, both placement forms. Track board goes beside the map; the rest stays face down with the loggers."),
    ("Starting conditions: reference and cue cards", (WEEK, "Starting Conditions.pdf"), None, 1, "Cut the cue cards apart and stand them face up beside the map."),
    ("Counters, both sides", (WC, "counters.pdf"), None, 1, "Print at 100% (not \"fit to page\"), in colour, on card stock if you can. Shows hidden assets: white cell only."),
    ("Map, letter tiles", (WEEK, "map-tiles.pdf"), None, 1, "Portrait, like the rest of the packet (the map is turned on the page). Trim and tape. For one large sheet, print map-full.pdf on a plotter instead."),
    ("REDFOR: OPORD/FRAGO format", (ASAP, "Player Forms and Templates.pdf"), "1. Five-Paragraph", 1, ""),
    ("REDFOR: COA worksheets", (ASAP, "Player Forms and Templates.pdf"), "2. COA Worksheet", 7, "One per turn"),
    ("REDFOR: Cons worksheets", (ASAP, "Player Forms and Templates.pdf"), "3. Cons Worksheet", 7, "One per turn"),
    ("REDFOR: request slips (3 per page)", (ASAP, "Player Forms and Templates.pdf"), "4. Request Slips", 9, "25 slips: 4 in Phase I, 3 a turn after"),
    ("REDFOR: secret COA slips", (ASAP, "Player Forms and Templates.pdf"), "5. Secret COA Slip", 2, "One per phase"),
    ("BLUEFOR: OPORD/FRAGO format", (ASAP, "Player Forms and Templates.pdf"), "1. Five-Paragraph", 1, ""),
    ("BLUEFOR: COA worksheets", (ASAP, "Player Forms and Templates.pdf"), "2. COA Worksheet", 7, "One per turn"),
    ("BLUEFOR: Cons worksheets", (ASAP, "Player Forms and Templates.pdf"), "3. Cons Worksheet", 7, "One per turn"),
    ("BLUEFOR: request slips (3 per page)", (ASAP, "Player Forms and Templates.pdf"), "4. Request Slips", 9, "25 slips: 4 in Phase I, 3 a turn after"),
    ("BLUEFOR: secret COA slips", (ASAP, "Player Forms and Templates.pdf"), "5. Secret COA Slip", 2, "One per phase"),
    # Spares go last, for whichever side runs short. The player forms have a side box, so one stack serves both.
    ("Spare: request slips (3 per page)", (ASAP, "Player Forms and Templates.pdf"), "4. Request Slips", 3, "9 slips, either side"),
    ("Spare: COA worksheets", (ASAP, "Player Forms and Templates.pdf"), "2. COA Worksheet", 2, "Either side"),
    ("Spare: Cons worksheets", (ASAP, "Player Forms and Templates.pdf"), "3. Cons Worksheet", 2, "Either side"),
    ("Spare: secret COA slips", (ASAP, "Player Forms and Templates.pdf"), "5. Secret COA Slip", 2, "Either side"),
    ("Spare: REDFOR placement form", (WC, "White Cell Forms.pdf"), "4.1 REDFOR placement form", 1, "If the first fills up with crossings-out"),
    ("Spare: BLUEFOR placement form", (WC, "White Cell Forms.pdf"), "4.2 BLUEFOR placement form", 1, "If the first fills up with crossings-out"),
]


def word_name(md_path):
    """The handouts/word/ PDF that replaces this intel product, if there is one."""
    code = os.path.basename(md_path)[:5]
    hits = glob.glob(os.path.join(H, "word", code + " *.pdf"))
    return os.path.splitext(os.path.basename(hits[0]))[0] if hits else None


def expand(sources):
    if isinstance(sources, str) and sources.startswith("intel:"):
        out = []
        for md in intel(sources.split(":")[1]):
            w = word_name(md)
            out.append(("word", w) if w else os.path.relpath(md, H))
        return out
    return sources


# ---------------------------------------------------------------- markdown

FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def front_matter(text):
    m = FRONT.match(text)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    return meta, text


def clean(text, is_intel=False):
    """Drop what stays in the markdown only: audience lines and FORMAT NOTEs."""
    paras = re.split(r"(\n\s*\n)", text)
    out = []
    for p in paras:
        s = p.strip()
        if s.startswith("> **FORMAT NOTE"):
            continue
        if s.startswith("**Audience:**"):
            continue
        m = re.match(r"^\*\*(REDFOR|BLUEFOR|WHITE CELL)[^*]*\*\*\s*(\*\*Never show[^*]*\*\*\s*)?", s)
        if m:
            rest = s[m.end():].strip()
            if is_intel or not rest.startswith("*") or rest.startswith("**"):
                continue
            p = rest
        out.append(p)
    text = "".join(out)
    if is_intel:  # the rule under the audience line
        text = re.sub(r"\A(\s*# [^\n]*\n)\s*---\s*\n", r"\1", text)
    return text


def side_class(heading_html):
    """red/blue for a card or slip whose heading names a side (S-R1, R-30, REDFOR ...)."""
    t = re.sub(r"<[^>]+>", "", heading_html)
    if re.match(r"\s*(S-)?R-?\d|.*\bREDFOR\b", t):
        return " zz-red"
    if re.match(r"\s*(S-)?B-?\d|.*\bBLUEFOR\b", t):
        return " zz-blue"
    return ""


def _wrap_blocks(out):
    """<!-- zz:begin NAME --> ... <!-- zz:end --> -> <div class="zz-NAME">; cards and slips split at <h3>."""
    def block(m):
        name, inner = m.group(1), m.group(2)
        if name == "cards":
            parts = re.split(r"(?=<h3)", inner)
            inner = parts[0] + "".join('<div class="zz-card%s">%s</div>' % (side_class(p[:200]), p) for p in parts[1:])
        elif name == "slips":
            inner = "".join('<div class="zz-slip">%s</div>' % p for p in re.split(r"<hr\s*/?>", inner))
        return '<div class="zz-%s">%s</div>' % (name, inner)
    return re.sub(r"<!-- zz:begin (\w[\w-]*) -->\s*(.*?)<!-- zz:end -->", block, out, flags=re.S)


TRACK_RED, TRACK_BLUE, TRACK_AMBER = (207, 34, 46), (9, 105, 218), (212, 140, 0)


def _tint(rgb, k):
    """rgb mixed with white: k=0 is white, k=1 is the full colour."""
    return "#%02x%02x%02x" % tuple(round(255 + (c - 255) * k) for c in rgb)


def track_colours(out):
    """Colour the track board's cells: deeper blue favours Omak, deeper red favours Cosmopolis.
    Opinion runs blue to red through white; Will is a red ramp, Stability a blue one;
    Strait Traffic goes amber as it closes."""
    def cell(label, value):
        v = value.replace("−", "-").strip(" •")
        if "Opinion" in label and re.fullmatch(r"[+-]?\d", v):
            n = int(v)
            return (TRACK_BLUE if n < 0 else TRACK_RED), abs(n) / 3 * 0.85
        if "Will" in label and v.isdigit():
            return TRACK_RED, int(v) / 5 * 0.6
        if "Stability" in label and v.isdigit():
            return TRACK_BLUE, int(v) / 5 * 0.6
        if "Strait" in label and v in ("Restricted", "Closed"):
            return TRACK_AMBER, 0.25 if v == "Restricted" else 0.5
        return None

    def row(m):
        tds = re.findall(r"<td>(.*?)</td>", m.group(0), re.S)
        if not tds:
            return m.group(0)
        label = re.sub(r"<[^>]+>", "", tds[0])
        cells = ["<td>%s</td>" % tds[0]]
        for t in tds[1:]:
            c = cell(label, re.sub(r"<[^>]+>", "", t))
            if c:
                rgb, k = c
                fg = "#fff" if k > 0.55 else "#1f2328"
                cells.append('<td style="background:%s;color:%s">%s</td>' % (_tint(rgb, k), fg, t))
            else:
                cells.append("<td>%s</td>" % t)
        return "<tr>%s</tr>" % "".join(cells)

    def table(m):
        return re.sub(r"<tr>.*?</tr>", row, m.group(0), flags=re.S)
    return re.sub(r'<table class="[^"]*zz-track[^"]*">.*?</table>', table, out, flags=re.S)


def render_markdown(text, base_dir, image_url=None):
    """Markdown (as the handouts use it) -> HTML."""
    from markdown_it import MarkdownIt
    from mdit_py_plugins.tasklists import tasklists_plugin

    text = re.sub(r"\)\{width=[^}]*\}", ")", text)
    text = text.replace("<!-- pagebreak -->", '<div class="pagebreak"></div>')
    md = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table").enable("strikethrough")
    md.use(tasklists_plugin)
    out = md.render(text)

    # table classes from <!-- zz:a b --> on the line before
    out = re.sub(r"<!-- zz:((?!begin|end)[\w -]+?) -->\s*<table>",
                 lambda m: '<table class="%s">' % " ".join("zz-" + c for c in m.group(1).split()), out)
    out = _wrap_blocks(out)
    out = track_colours(out)
    # a header row with no text (key-value tables in the intel products) is dropped
    out = re.sub(r"<table( class=\"[^\"]*\")?>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)+</tr>\s*</thead>",
                 lambda m: '<table class="zz-kv%s">' % (" " + m.group(1)[8:-1] if m.group(1) else ""), out)
    # a header cell followed by empty ones spans them (form titles)
    def span(m):
        n = 1 + len(re.findall(r"<th[^>]*>\s*</th>", m.group(2)))
        return '<th colspan="%d"%s</th></tr>' % (n, m.group(1)) if n > 1 else m.group(0)
    out = re.sub(r"<th(?: [^>]*)?(>(?:(?!</th>).)*\S(?:(?!</th>).)*)</th>((?:\s*<th[^>]*>\s*</th>)+)\s*</tr>", span, out)
    # an all-capitals heading is an issuing office's masthead (intel products), not a headline
    out = re.sub(r"<h2>([^<a-z]+)</h2>", r'<h2 class="zz-masthead">\1</h2>', out)
    # ☐ prints as a drawn box, the same size everywhere; a box and its label don't split
    out = re.sub(r"☐ ?([^☐<|/]*?[^☐<|/\s])(?=\s*(?:☐|/|<|$))",
                 lambda m: '<span class="zz-opt"><span class="zz-box" aria-hidden="true">☐</span>%s</span>' % m.group(1)
                 if len(m.group(1)) <= 14 else m.group(0), out)
    out = out.replace("☐", '<span class="zz-box" aria-hidden="true">☐</span>')
    out = re.sub(r"<td>((?:\s*<span class=\"zz-opt\">(?:(?!</span></span>).)*</span></span>)+\s*)</td>",
                 r'<td class="zz-opts">\1</td>', out)

    def img(m):
        src = m.group(1)
        if re.match(r"^[a-z]+:", src):
            return m.group(0)
        path = os.path.normpath(os.path.join(base_dir, src))
        return 'src="%s"' % (image_url(path) if image_url else "file://" + path)
    return re.sub(r'src="([^"]+)"', img, out)


# ---------------------------------------------------------------- style

FONT_FACES = "".join(
    '@font-face { font-family: "JetBrains Mono"; src: url("file://%s/JetBrainsMono-%s.ttf"); font-weight: %s; font-style: %s; }\n'
    % (FONTS, f, w, s) for f, w, s in (("Regular", 400, "normal"), ("Bold", 700, "normal"), ("Italic", 400, "italic")))

# The Repo theme (markdown.style), set for paper: system sans, JetBrains Mono for
# code, rules under the top two heading levels, zebra-striped tables.
CSS = """
:root {
  --fg: #1f2328; --muted: #59636e; --line: #d1d9e0; --soft: #f6f8fa; --link: #0969da;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "DejaVu Sans Mono", "Liberation Mono", monospace;
}
html { font-family: var(--sans); font-size: 10pt; color: var(--fg); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; line-height: 1.45; }
a { color: var(--link); text-decoration: none; }
h1, h2, h3, h4, h5, h6 { font-weight: 600; line-height: 1.25; margin: 1.3em 0 0.5em; break-after: avoid; color: var(--fg); }
h1 { font-size: 18pt; padding-bottom: 0.25em; border-bottom: 1px solid var(--line); }
h2 { font-size: 14pt; padding-bottom: 0.25em; border-bottom: 1px solid var(--line); }
h3 { font-size: 11.5pt; }
h4 { font-size: 10pt; }
h5, h6 { font-size: 9.5pt; color: var(--muted); }
h2 + *, h3 + *, h4 + * { break-before: avoid; }
p { margin: 0 0 0.65em; orphans: 3; widows: 3; }
strong { font-weight: 600; }
ul, ol { margin: 0 0 0.65em; padding-left: 1.7em; } li { margin: 0.2em 0; } li > p { margin: 0.2em 0; }
blockquote { margin: 0.4em 0 0.8em; padding: 0.15em 0.9em; color: var(--muted); border-left: 0.25em solid var(--accent); }
blockquote p { margin: 0.35em 0; } blockquote strong { color: var(--fg); }
code { font-family: var(--mono); font-size: 0.86em; background: var(--soft); padding: 0.1em 0.3em; border-radius: 4px; }
pre { font-family: var(--mono); font-size: 8.5pt; line-height: 1.45; white-space: pre-wrap;
      border: 1px solid var(--line); border-radius: 6px; padding: 9pt 11pt; break-inside: avoid; }
pre code { background: none; padding: 0; font-size: inherit; }
hr { border: 0; height: 0.25em; background: var(--line); margin: 1.2em 0; }
img { max-width: 100%; }

table { border-collapse: collapse; width: 100%; margin: 0.4em 0 1em; font-size: 9pt; line-height: 1.35; break-inside: auto; }
tr { break-inside: avoid; }
th, td { border: 1px solid var(--line); padding: 4pt 6pt; vertical-align: top; text-align: left; }
thead th { font-weight: 600; border-bottom: 1.5pt solid var(--accent); }
td:empty { height: 1.3em; }

/* the title block made from the front matter */
.doc-head { margin: 0 0 1.4em; padding: 0 0 0.8em; border-bottom: 2pt solid var(--accent); }
.doc-kicker { font-size: 8.5pt; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); margin: 0 0 0.3em; }
.doc-head h1 { font-size: 24pt; border: 0; padding: 0; margin: 0 0 0.2em; }
.doc-subtitle { color: var(--muted); font-size: 11pt; margin: 0; }

/* intelligence products */
.product > h1:first-child { margin-top: 0; border-bottom: 2pt solid var(--accent); }
h2.zz-masthead { font-size: 10pt; letter-spacing: 0.06em; color: var(--muted); border: 0; padding: 0; margin: 1em 0 0.5em; }

/* checkboxes */
.zz-box { display: inline-block; width: 0.8em; height: 0.8em; border: 1.1pt solid var(--fg); border-radius: 2px;
          color: transparent; overflow: hidden; line-height: 0.8em; vertical-align: -0.08em; margin: 0 0.3em 0 0.35em; }
.zz-box:first-child { margin-left: 0; }
ul.contains-task-list { list-style: none; padding-left: 1.4em; }
.task-list-item-checkbox { appearance: none; -webkit-appearance: none; width: 0.85em; height: 0.85em; border: 1.1pt solid var(--accent);
          border-radius: 2px; margin: 0 0.55em 0 -1.4em; vertical-align: -0.1em; }

/* forms: label column on the left, room to write on the right */
table.zz-form { font-size: 10pt; }
table.zz-form thead th { color: var(--fg); border-top: 2pt solid var(--accent); border-bottom: 1.5pt solid var(--fg); font-size: 11pt; letter-spacing: 0.04em; }
table.zz-form td:first-child { width: 31%; font-weight: 600; }
table.zz-form td { height: 0.42in; vertical-align: middle; box-sizing: border-box; }
table.zz-form.zz-tall td { height: 0.9in; vertical-align: top; }
table.zz-form.zz-med td { height: 0.6in; vertical-align: top; }
table.zz-form.zz-tall td:first-child, table.zz-form.zz-med td:first-child { vertical-align: top; }
.zz-opt { white-space: nowrap; margin-right: 0.35em; }
td.zz-opts { white-space: nowrap; width: 1%; }
table.zz-log td:empty, table.zz-log td { height: 0.3in; padding-top: 1pt; padding-bottom: 1pt; vertical-align: middle; box-sizing: border-box; }
table.zz-kv td:first-child { width: 28%; font-weight: 600; }

/* the track board: cells big enough for a marker, coloured by track_colours() */
table.zz-track { font-size: 11pt; table-layout: fixed; }
table.zz-track td { height: 0.5in; box-sizing: border-box; text-align: center; vertical-align: middle; font-weight: 600; font-size: 10pt; padding: 2pt; }
table.zz-track td:first-child, table.zz-track th:first-child { text-align: left; width: 27%; font-size: 9.5pt; }
table.zz-track td:empty { border: 0; }
table.zz-markers { width: auto; margin: 0.3em 0 1em; }
table.zz-markers td { width: 0.95in; height: 0.62in; text-align: center; vertical-align: middle; font-weight: 700; font-size: 9pt;
                      border: 1px dashed var(--muted); background: var(--tint) !important; color: var(--accent); }
table.zz-checkgrid { font-size: 8.5pt; }
table.zz-checkgrid th:nth-child(n+3), table.zz-checkgrid td:nth-child(n+3) { text-align: center; width: 5.2%; padding: 3pt 2pt; }
table.zz-checkgrid td { height: 0.27in; vertical-align: middle; }
table.zz-checkgrid td:first-child { width: 10%; white-space: nowrap; color: var(--muted); font-family: var(--mono); font-size: 7.5pt; }

/* cut-out cards and slips */
.zz-card { border: 1.2pt dashed var(--muted); border-radius: 6px; padding: 0.16in 0.22in; height: 2.88in; box-sizing: border-box;
           margin: 0 0 0.14in; break-inside: avoid; overflow: hidden; position: relative; font-size: 12.5pt; line-height: 1.4; }
.zz-card h3 { margin: -0.16in -0.22in 0.12in; padding: 0.1in 0.22in; font-size: 15pt; color: #fff; background: var(--card); border-radius: 5px 5px 0 0; }
.zz-card p { margin: 0 0 0.45em; }
.zz-card { --card: var(--accent); }
.zz-card.zz-red { --card: #cf222e; } .zz-card.zz-blue { --card: #0969da; }
.zz-slip { border-bottom: 1.2pt dashed var(--muted); padding: 0 0 0.12in; margin: 0 0 0.16in; break-inside: avoid; }
.zz-slip:last-child { border-bottom: 0; }
table.zz-compact { font-size: 8pt; table-layout: fixed; line-height: 1.3; }
table.zz-compact td { padding: 3pt 5pt; }
table.zz-compact th:first-child { width: 6%; } table.zz-compact th:nth-child(2) { width: 16%; }
table.zz-compact th:nth-child(3) { width: 50%; }
.zz-slip table.zz-form td { height: 0.36in; }
.zz-slip table { margin-bottom: 0; }

.pagebreak { break-after: page; height: 0; }
.product { break-before: page; } .product:first-child { break-before: auto; }
"""

# Page frame. The header and footer sit in the margin boxes, inside the page margins.
PAGE = """
@page {
  size: Letter; margin: 0.9in 0.75in 0.8in 0.75in;
  @top-left { content: "%(left)s"; font: 8pt var(--sans); color: #59636e; vertical-align: bottom; padding-bottom: 0.14in; border-bottom: 0.75pt solid #d1d9e0; }
  @top-center { content: "%(mid)s"; font: 700 8pt var(--sans); letter-spacing: 0.06em; color: %(accent)s; vertical-align: bottom; padding-bottom: 0.14in; border-bottom: 0.75pt solid #d1d9e0; }
  @top-right { content: "%(right)s"; font: 8pt var(--sans); color: #59636e; vertical-align: bottom; padding-bottom: 0.14in; border-bottom: 0.75pt solid #d1d9e0; }
  @bottom-left { content: "%(title)s"; font: 7.5pt var(--sans); color: #59636e; vertical-align: top; padding-top: 0.14in; }
  @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 7.5pt var(--sans); color: #59636e; vertical-align: top; padding-top: 0.14in; }
}
:root { --accent: %(accent)s; --tint: %(tint)s; }
"""


def css_str(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def title_block(meta):
    """The front matter's title and subtitle as a title block. "Operation Zugzwang — X" puts the first part above."""
    title = meta.get("title", "")
    kicker, _, main = title.partition(" — ")
    if not main:
        kicker, main = "", title
    sub = '<p class="doc-subtitle">%s</p>' % html.escape(meta["subtitle"]) if meta.get("subtitle") else ""
    kick = '<p class="doc-kicker">%s</p>' % html.escape(kicker) if kicker else ""
    return '<header class="doc-head">%s<h1>%s</h1>%s</header>' % (kick, html.escape(main), sub)


def page_html(md_paths, header=WC_ONLY, doc_title=""):
    """One HTML document for one or more markdown files (several = intel products)."""
    bodies = []
    many = any(re.match(r"^[RB]I-\d\d", os.path.basename(p)) for p in md_paths)
    for rel in md_paths:
        path = rel if os.path.isabs(rel) else os.path.join(H, rel)
        meta, text = front_matter(open(path, encoding="utf-8").read())
        is_product = bool(re.match(r"^[RB]I-\d\d", os.path.basename(path)))
        text = clean(text, is_intel=is_product)
        body = render_markdown(text, os.path.dirname(path))
        if meta.get("title"):
            body = title_block(meta) + body
            doc_title = doc_title or meta.get("short", "")
        bodies.append('<section class="product">%s</section>' % body if many else body)
    accent, tint = theme(header)
    left, mid, right = header or ("", "", "")
    page = PAGE % dict(left=css_str(left), mid=css_str(mid), right=css_str(right), title=css_str(doc_title),
                       accent=accent, tint=tint)
    return ('<!doctype html><html><head><meta charset="utf-8"><style>%s%s%s</style></head><body>%s</body></html>'
            % (FONT_FACES, CSS, page, "".join(bodies)))


# ---------------------------------------------------------------- PDF

def print_pdf(browser, page_doc, out_path):
    src = out_path[:-4] + ".html"  # a file:// page may load file:// images and fonts; set_content may not
    with open(src, "w", encoding="utf-8") as f:
        f.write(page_doc)
    page = browser.new_page()
    page.goto("file://" + src, wait_until="load")
    page.evaluate("document.fonts.ready")
    page.pdf(path=out_path, print_background=True, prefer_css_page_size=True, display_header_footer=False)
    page.close()


def write_pdf(pdfs_or_pages, name, dst):
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for item in pdfs_or_pages:
        if isinstance(item, str):
            w.append(item)
        else:  # (path, [page indexes])
            r = PdfReader(item[0])
            for i in item[1]:
                w.add_page(r.pages[i])
    w.add_metadata({"/Title": os.path.splitext(name)[0], "/Author": "C/Nacanaynay", "/Creator": "tools/build_handouts.py"})
    with open(dst, "wb") as f:
        w.write(f)


def build_one(browser, folder, name, header, sources, work):
    dst = os.path.join(FIN, folder, name)
    if sources == "packet":
        return build_packet(browser, header, dst, work)
    sources = expand(sources)
    if len(sources) == 1 and isinstance(sources[0], tuple) and sources[0][0] == "copy":
        shutil.copyfile(os.path.join(ROOT, sources[0][1]), dst)
        return dst
    # group consecutive markdown files so each run prints as one PDF
    parts, run = [], []
    for s in sources:
        if isinstance(s, tuple):
            if run:
                parts.append(("md", run))
                run = []
            parts.append(s)
        else:
            run.append(s)
    if run:
        parts.append(("md", run))
    short = os.path.splitext(name)[0]
    pdfs = []
    for i, (kind, val) in enumerate(parts):
        if kind == "md":
            p = os.path.join(work, f"{len(os.listdir(work))}-{i}.pdf")
            print_pdf(browser, page_html(val, header, short), p)
            pdfs.append(p)
        elif kind == "word":
            p = os.path.join(H, "word", val + ".pdf")
            if not os.path.exists(p):
                sys.exit(f"missing {os.path.relpath(p, ROOT)}: run tools/tq/build_tq.py first")
            pdfs.append(p)
    write_pdf(pdfs, name, dst)
    return dst


# ---------------------------------------------------------------- print packet

def section_pages(pdf, heading):
    """Page indexes of the section that starts with the heading `heading`, up to where the next one starts."""
    from pypdf import PdfReader
    pages = PdfReader(pdf).pages
    others = {h for _l, f, h, _c, _n in PACKET if h and os.path.join(FIN, *f) == pdf}
    starts = {}
    for i, pg in enumerate(pages):
        text = pg.extract_text() or ""
        for h in others:
            if re.search(r"^\s*" + re.escape(h), text, re.M):
                starts.setdefault(h, i)
    if heading not in starts:
        sys.exit(f"{os.path.relpath(pdf, ROOT)}: no section {heading!r}")
    later = sorted(v for v in starts.values() if v > starts[heading])
    return list(range(starts[heading], later[0] if later else len(pages)))


def packet_rows():
    """[(label, file, pages per copy, copies, note)] with the page counts read from the built PDFs."""
    from pypdf import PdfReader
    rows = []
    for label, (folder, fname), heading, copies, note in PACKET:
        pdf = os.path.join(FIN, folder, fname)
        if not os.path.exists(pdf):
            sys.exit(f"missing {os.path.relpath(pdf, ROOT)}: build it before the print packet")
        pages = section_pages(pdf, heading) if heading else list(range(len(PdfReader(pdf).pages)))
        rows.append((label, pdf, pages, copies, note))
    return rows


def packet_markdown(rows=None):
    """The cover sheet, as markdown. Also used for the site page (rows=None reads the counts without page numbers)."""
    lines = [
        "---",
        'title: "Operation Zugzwang — Print Packet"',
        'subtitle: "Everything one table prints to run the game · print one packet per table (4 tables)"',
        'short: "Print Packet"',
        "---",
        "",
        "**WHITE CELL ONLY.** This packet holds **both** sides' hidden counters and the white cell forms. "
        "Print it, split it into the stacks below, and keep it away from the players until each piece is handed out.",
        "",
        "## Contents (one table)",
        "",
        "| Printed | Item | Copies | Pages | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    total = 0
    spares = False
    for i, (label, _pdf, pages, copies, note) in enumerate(rows or [(r[0], None, [], r[3], r[4]) for r in PACKET]):
        n = len(pages) * copies
        total += n
        if label.startswith("Spare: ") and not spares:
            spares = True
            lines.append("| | **Spares, at the back.** Keep them with the white cell and hand them out as needed. | | | |")
        label = label.removeprefix("Spare: ")
        lines.append("| ☐ | %s | %d | %s | %s |" % (label, copies, n or "", note))
    lines += [
        "",
        f"Packet total: **{total} pages** after this cover, in the order listed." if rows else "",
        "",
        "## Printing",
        "",
        "- Print **single-sided at 100% scale** (\"actual size\", not \"fit to page\"). Every page keeps its content inside a 0.75 in margin.",
        "- **Colour** for the game pieces: the counters, map tiles, cue cards, track board, and track markers use colour for sides. "
        "Everything else (the forms, worksheets, and slips) is black and white, so print it in greyscale to save ink.",
        "- **Card stock** for the counters and cue cards, if you have it.",
        "- Cut the counters along the grey lines, and the cue cards and request slips along the dashed lines.",
        "",
        "## Also needed at each table",
        "",
        "- [ ] The lead adjudicator's laptop with the timer and dice program (`whitecell-clock.html`), shown where both teams can see it",
        "- [ ] An envelope for the hidden counters",
        "- [ ] Coins or tokens for the four track markers, if you don't cut out the printed ones",
        "- [ ] Pens for each team and each logger",
        "",
    ]
    return "\n".join(lines)


def build_packet(browser, header, dst, work):
    rows = packet_rows()
    cover_md = os.path.join(work, "print-packet.md")
    with open(cover_md, "w", encoding="utf-8") as f:
        f.write(packet_markdown(rows))
    cover = os.path.join(work, "packet-cover.pdf")
    print_pdf(browser, page_html([cover_md], header, "Print Packet"), cover)
    items = [cover]
    for _label, pdf, pages, copies, _note in rows:
        items += [(pdf, pages)] * copies
    write_pdf(items, os.path.basename(dst), dst)
    return dst


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", default=[], help="build only files whose name contains one of these")
    ap.add_argument("--html-only", action="store_true", help="write the HTML to a temp folder instead of printing")
    a = ap.parse_args()
    picks = [r for r in RELEASES if not a.only or any(o.lower() in r[1].lower() for o in a.only)]
    work = tempfile.mkdtemp(prefix="zz-pdf-")
    if a.html_only:
        for folder, name, header, sources in picks:
            if sources == "packet":
                continue
            md = [s for s in expand(sources) if isinstance(s, str)]
            if md:
                p = os.path.join(work, name.replace(".pdf", ".html"))
                open(p, "w", encoding="utf-8").write(page_html(md, header, os.path.splitext(name)[0]))
                print(p)
        return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        for folder, name, header, sources in picks:
            os.makedirs(os.path.join(FIN, folder), exist_ok=True)
            dst = build_one(browser, folder, name, header, sources, work)
            print("wrote", os.path.relpath(dst, ROOT))
        browser.close()
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
