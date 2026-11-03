"""Make printable, cut-out counters from scenario/data/assets.csv.

Usage: python3 tools/make_counters.py [--size INCHES] [--copies N]

Writes three US Letter PDFs, one per audience folder, so each team only gets
its own counters:
  handouts/redfor/counters.pdf     REDFOR counters
  handouts/bluefor/counters.pdf    BLUEFOR counters
  handouts/whitecell/counters.pdf  all counters, on one page at the default size

Each counter is a small square: ID and owner in a colored band, a short asset
name, then service and availability (HOME, RFF, HIDDEN) along the bottom.
Counters share cut lines, so a paper cutter can take a whole row at once.
No third-party packages are needed; the PDF is written directly.
"""

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "scenario" / "data" / "assets.csv"
OUTPUTS = {
    ROOT / "handouts" / "redfor" / "counters.pdf": ("REDFOR",),
    ROOT / "handouts" / "bluefor" / "counters.pdf": ("BLUEFOR",),
    ROOT / "handouts" / "whitecell" / "counters.pdf": ("REDFOR", "BLUEFOR"),
}
AUDIENCE = {
    ("REDFOR",): "REDFOR + white cell only",
    ("BLUEFOR",): "BLUEFOR + white cell only",
    ("REDFOR", "BLUEFOR"): "White cell only",
}

PAGE_W, PAGE_H = 612, 792  # US Letter, points
MARGIN = 36
HEADER = 30

# Band color and light fill, as RGB 0-1.
COLORS = {
    "REDFOR": ((0.70, 0.11, 0.11), (1.00, 0.92, 0.92)),
    "BLUEFOR": ((0.10, 0.25, 0.60), (0.91, 0.94, 1.00)),
}

# Helvetica and Helvetica-Bold advance widths (1/1000 em), ASCII 32-126.
_HELV = [
    278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278,
    556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556,
    1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556,
    333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
    556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584,
]
_HELV_B = [
    278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278,
    556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611,
    975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778,
    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556,
    333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611,
    611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584,
]
FONTS = {"F1": _HELV, "F2": _HELV_B}  # F1 regular, F2 bold


def text_width(text, font, size):
    widths = FONTS[font]
    return sum(widths[ord(c) - 32] if 32 <= ord(c) <= 126 else 556 for c in text) * size / 1000


def short_name(asset):
    """Drop parentheticals and extra spaces: 'F-22A Raptor squadron (~12)' -> 'F-22A Raptor squadron'."""
    return re.sub(r"\s+", " ", re.sub(r"\([^)]*\)", "", asset)).strip()


def wrap(text, font, size, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if text_width(trial, font, size) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit_name(text, width, height):
    """Largest font size (and its lines) that fits the name area."""
    size = 7.0
    while size > 3.5:
        lines = wrap(text, "F1", size, width)
        if len(lines) * size * 1.12 <= height and all(text_width(l, "F1", size) <= width for l in lines):
            return size, lines
        size -= 0.25
    return size, wrap(text, "F1", size, width)


def esc(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class Page:
    def __init__(self):
        self.ops = []

    def rect(self, x, y, w, h, fill=None, stroke=None, line=0.4):
        if fill:
            self.ops.append("%.3f %.3f %.3f rg" % fill)
        if stroke:
            self.ops.append("%.3f %.3f %.3f RG %.2f w" % (*stroke, line))
        op = "B" if fill and stroke else "f" if fill else "S"
        self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re {op}")

    def text(self, x, y, s, font="F1", size=6, color=(0, 0, 0), align="left"):
        if align == "center":
            x -= text_width(s, font, size) / 2
        elif align == "right":
            x -= text_width(s, font, size)
        self.ops.append("%.3f %.3f %.3f rg" % color)
        self.ops.append(f"BT /{font} {size:.2f} Tf {x:.2f} {y:.2f} Td ({esc(s)}) Tj ET")

    def stream(self):
        return "\n".join(self.ops).encode("latin-1")


def draw_counter(page, x, y, s, row):
    band, fill = COLORS[row["side"]]
    pad = s * 0.06
    band_h = s * 0.24
    foot = s * 0.14

    page.rect(x, y, s, s, fill=fill)
    page.rect(x, y + s - band_h, s, band_h, fill=band)

    id_size = band_h * 0.62
    base = y + s - band_h + (band_h - id_size * 0.72) / 2
    page.text(x + pad, base, row["id"], "F2", id_size, (1, 1, 1))
    owner = row["owner"]
    owner_size = min(band_h * 0.42, (s * 0.42) / max(text_width(owner, "F2", 1), 1))
    page.text(x + s - pad, base, owner, "F2", owner_size, (1, 1, 1), "right")

    area_w = s - 2 * pad
    area_h = s - band_h - foot - 2 * pad
    size, lines = fit_name(short_name(row["asset"]), area_w, area_h)
    block = len(lines) * size * 1.12
    top = y + foot + pad + (area_h + block) / 2
    for i, line in enumerate(lines):
        page.text(x + s / 2, top - (i + 0.85) * size * 1.12, line, "F1", size, align="center")

    foot_size = foot * 0.62
    fy = y + pad * 0.7
    service = row["service"].replace(" (US-type)", "").replace("-type", "")
    page.text(x + pad, fy, service, "F1", foot_size, (0.25, 0.25, 0.25))
    tags = []
    if row["availability"] == "home":
        tags.append("HOME")
    elif row["availability"] == "rff":
        tags.append("RFF")
    if row["visibility"] == "hidden":
        tags.append("HIDDEN")
    if tags:
        page.text(x + s - pad, fy, " ".join(tags), "F2", foot_size, band, "right")


def layout(rows, s, title, audience):
    cols = int((PAGE_W - 2 * MARGIN) // s)
    per_page = cols * int((PAGE_H - 2 * MARGIN - HEADER) // s)
    pages = []
    for start in range(0, len(rows), per_page):
        chunk = rows[start:start + per_page]
        page = Page()
        page.text(MARGIN, PAGE_H - MARGIN - 10, title, "F2", 11)
        page.text(PAGE_W - MARGIN, PAGE_H - MARGIN - 10, audience, "F2", 9, (0.6, 0, 0), "right")
        page.text(MARGIN, PAGE_H - MARGIN - 22,
                  "Cut along the gray lines. HOME = starts at home base; RFF = request for forces; "
                  "HIDDEN = keep off the board until revealed.", "F1", 7, (0.3, 0.3, 0.3))
        top = PAGE_H - MARGIN - HEADER
        x0 = (PAGE_W - cols * s) / 2
        for i, row in enumerate(chunk):
            r, c = divmod(i, cols)
            if row:
                draw_counter(page, x0 + c * s, top - (r + 1) * s, s, row)
        # Cut lines drawn last so they sit on top of the fills.
        for i, row in enumerate(chunk):
            r, c = divmod(i, cols)
            if row:
                page.rect(x0 + c * s, top - (r + 1) * s, s, s, stroke=(0.55, 0.55, 0.55), line=0.5)
        pages.append(page)
    return pages


def write_pdf(path, pages):
    objs = [None, None, None, None]  # catalog, pages, font F1, font F2
    objs[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objs[2] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    objs[3] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
    kids = []
    for page in pages:
        data = page.stream()
        objs.append(b"<< /Length %d >>\nstream\n" % len(data) + data + b"\nendstream")
        content = len(objs)
        objs.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] "
            b"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents %d 0 R >>"
            % (PAGE_W, PAGE_H, content)
        )
        kids.append(len(objs))
    objs[1] = b"<< /Type /Pages /Kids [%s] /Count %d >>" % (
        " ".join(f"{k} 0 R" for k in kids).encode(), len(kids))

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for n, obj in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % n + obj + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(out))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--size", type=float, default=0.75, help="counter edge in inches (default 0.75)")
    parser.add_argument("--copies", type=int, default=1, help="copies of each counter (default 1)")
    args = parser.parse_args()

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    s = args.size * 72
    cols = int((PAGE_W - 2 * MARGIN) // s)
    for path, sides in OUTPUTS.items():
        sheet = []
        for side in sides:
            # Blank cells finish the row, so each side starts on a fresh row.
            sheet += [None] * (-len(sheet) % cols)
            sheet += [r for r in rows if r["side"] == side for _ in range(args.copies)]
        label = sides[0] if len(sides) == 1 else "all"
        pages = layout(sheet, s, f"Operation Zugzwang - {label} counters", AUDIENCE[sides])
        write_pdf(path, pages)
        print(f"{path.relative_to(ROOT)}: {len(pages)} page(s)")


if __name__ == "__main__":
    main()
