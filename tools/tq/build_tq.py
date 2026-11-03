#!/usr/bin/env python3
"""Build the Tongue and Quill documents (.docx and .pdf) with WordCraft.

    python3 tools/tq/build_tq.py            # all six documents
    python3 tools/tq/build_tq.py RI-13      # only those whose key matches

Each document is written from its markdown in handouts/ into the Zugzwang
memo or letter template (tools/tq/templates/zz-*.dotx, made from the official
Air Force templates by make_templates.py), through the WordCraft MCP server
(`wordcraft-cli mcp`). Output goes to handouts/word/. tools/build_handouts.py
puts the PDFs into FINALIZED/.

The markdown is the source. The script reads the date, MEMORANDUM FOR, FROM,
SUBJECT, numbered paragraphs (1\\. and a.), salutation, close, signature block
(after a line of &nbsp;), and attachment from it. Letterhead lines, and dates
the markdown doesn't state, come from DOCS below and from each side's
intel/00-read-me-first.md table. Standard library only.
"""
import base64
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from wcmcp import WordCraft  # noqa: E402

OUT_DIR = os.path.join(ROOT, "handouts", "word")
TEMPLATES = os.path.join(HERE, "templates")

# key: output name; kind: memo or letter; lh: letterhead lines 1-3 (line 1 may
# come from the markdown instead); mark: the game's audience marking for the stamp.
DOCS = [
    dict(key="REDFOR - Commander's Letter", src="handouts/redfor/commanders-letter.md", kind="memo",
         lh=("COSMOPOLIS NATIONAL DEFENSE FORCES", "OFFICE OF THE CHAIRMAN OF THE JOINT STAFF", "")),
    dict(key="BLUEFOR - Commander's Letter", src="handouts/bluefor/commanders-letter.md", kind="letter",
         lh=("EXECUTIVE OFFICE OF THE PRESIDENT", "REPUBLIC OF OMAK", "OMAK CITY")),
    dict(key="RI-13 Memorandum of Conversation", src="handouts/redfor/intel/RI-13-memcon-latah.md", kind="memo",
         lh=("COSMOPOLIS MINISTRY OF DEFENSE", "OFFICE OF INTERNATIONAL SECURITY AFFAIRS", ""), mark="REDFOR ONLY"),
    dict(key="BI-05 Ministry Threat Assessment", src="handouts/bluefor/intel/BI-05-interior-threat-assessment.md", kind="memo",
         lh=("REPUBLIC OF OMAK", "MINISTRY OF THE INTERIOR", "OMAK CITY"), mark="BLUEFOR ONLY"),
    dict(key="BI-10 Letter from the Asotin Foreign Minister", src="handouts/bluefor/intel/BI-10-asotin-letter.md", kind="letter",
         lh=("ASOTIN MINISTRY OF FOREIGN AFFAIRS", "OFFICE OF THE FOREIGN MINISTER", ""), mark="BLUEFOR ONLY"),
    dict(key="BI-11 Leaked Memo", src="handouts/bluefor/intel/BI-11-leaked-ndf-memo.md", kind="memo",
         lh=("NATIONAL DEMOCRATIC FORCES", "LOGISTICS COMMAND", "FORTUNE HARBOR"), mark="BLUEFOR ONLY"),
]

DATE_RE = re.compile(r"^\d{1,2} [A-Z][a-z]+ \d{4}$")


# ---------------------------------------------------------------- markdown

def runs(md):
    """Inline markdown -> [(text, bold, italic)]."""
    md = md.replace("&nbsp;", " ")
    md = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", lambda m: "\x00%d\x00" % ord(m.group(1)), md)
    out = []
    for part in re.split(r"(\*\*.+?\*\*|\*[^*]+?\*)", md):
        if not part:
            continue
        bold, ital = part.startswith("**"), not part.startswith("**") and part.startswith("*")
        text = part[2:-2] if bold else part[1:-1] if ital else part
        text = re.sub(r"\x00(\d+)\x00", lambda m: chr(int(m.group(1))), text)
        out.append((text, bold, ital))
    return out


def plain(md):
    return "".join(t for t, _, _ in runs(md))


def read_dates():
    """Product dates from the Read Me First tables: {'RI-13': 'D−5', ...}."""
    dates = {}
    for f in glob.glob(os.path.join(ROOT, "handouts", "*", "intel", "00-read-me-first.md")):
        for line in open(f, encoding="utf-8"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and re.match(r"^[RB]I-\d\d$", cells[0]):
                dates[cells[0]] = cells[-1]
    return dates


def parse(path):
    text = open(os.path.join(ROOT, path), encoding="utf-8").read()
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    doc = dict(blocks=[], banner="", lh1="", date="", stamp_bits=[], title="")
    after_spacer = False
    for para in re.split(r"\n\s*\n", text.strip()):
        p = para.strip()
        lines = [ln.rstrip("\\").strip() for ln in p.split("\n")]
        first = lines[0]
        if first.startswith("# "):
            doc["title"] = plain(first[2:])
        elif re.match(r"^\*\*(REDFOR|BLUEFOR|WHITE CELL)[^*]*\*\*", first) or first.startswith(">") or p == "---":
            continue
        elif first.startswith("**Rating:**"):
            bits = [plain(b).strip() for b in p.split("·") if not b.strip().startswith("**Date:**")]
            doc["stamp_bits"] += bits
            m = re.search(r"\*\*Date:\*\*\s*([^·]+)", p)
            if m:
                doc["date"] = plain(m.group(1)).strip()
        elif re.match(r"^// .* //$", p):
            doc["banner"] = doc["banner"] or p
        elif first.startswith("*") and not first.startswith("**") and not doc["blocks"]:
            doc["stamp_bits"].append(plain(p))  # a caption that sits outside the document
        elif DATE_RE.match(p):
            doc["date"] = p
        elif p.isupper() and not doc["blocks"] and not p.startswith("MEMORANDUM"):
            doc["lh1"] = p
        elif p == "&nbsp;":
            after_spacer = True
            continue
        elif first.startswith("MEMORANDUM FOR "):
            doc["blocks"].append(("memofor", first[len("MEMORANDUM FOR "):]))
        elif first.startswith("FROM: "):
            doc["blocks"].append(("from", first[len("FROM: "):]))
        elif first.startswith("SUBJECT: "):
            doc["blocks"].append(("subject", first[len("SUBJECT: "):]))
        elif re.match(r"^\d+\\\. ", first):
            doc["blocks"].append(("num0", re.sub(r"^\d+\\\. ", "", p)))
        elif re.match(r"^[a-z]\. ", first):
            doc["blocks"].append(("num1", p[3:]))
        elif first.startswith("Attachment"):
            doc["blocks"].append(("attach", lines))
        elif first.startswith("1st Ind"):
            doc["blocks"].append(("ind", first))
        elif first.startswith("Dear "):
            doc["blocks"].append(("salute", first))
        elif p == "Sincerely":
            doc["blocks"].append(("close", p))
        elif after_spacer:
            doc["blocks"].append(("sig", lines))
        elif not any(k == "salute" for k, _ in doc["blocks"]) and all(len(ln) < 60 for ln in lines) and "letter" in path:
            doc["blocks"].append(("address", lines))
        else:
            doc["blocks"].append(("para", p))
        after_spacer = False
    return doc


# ---------------------------------------------------------------- templates

def instantiate(kind, tokens, dst):
    """Copy zz-<kind>.dotx to dst as a .docx with the {{TOKENS}} filled in."""
    with zipfile.ZipFile(os.path.join(TEMPLATES, f"zz-{kind}.dotx")) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.replace(b"wordprocessingml.template.main+xml", b"wordprocessingml.document.main+xml")
            if re.match(r"word/(header|footer)\d+\.xml$", item.filename):
                s = data.decode("utf-8")
                for k, v in tokens.items():
                    v = v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    s = s.replace("{{%s}}" % k, v)
                data = s.encode("utf-8")
            zout.writestr(item, data)


def serif_fonts():
    """Liberation Serif stands in for Times New Roman in the PDF (same metrics)."""
    try:
        out = subprocess.run(["fc-list", ":family=Liberation Serif", "file"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        return []
    return sorted({ln.split(":")[0].strip() for ln in out.splitlines() if ln.strip()})


# ---------------------------------------------------------------- writing

class Writer:
    def __init__(self, wc, kind):
        self.wc, self.kind, self.first = wc, kind, True
        self.sig_left = 324  # 4.5 inches from the left edge of the text

    def para(self, style="Normal", text="", num=None, align="left", before=None, after=None):
        wc = self.wc
        if not self.first:
            wc.run("text.newParagraph")
        self.first = False
        wc.batch([("para.reset", {}), ("para.style", {"style": style})])
        props = {"align": align}
        if before is not None or after is not None:
            wc.run("para.spacing", **{k: v for k, v in (("before", before), ("after", after)) if v is not None})
        if num is not None:
            props["numbering"] = num
        wc.run("para.set", props=props)
        if num is None and self.kind == "memo":
            wc.run("para.numbering", off=True)  # a new paragraph inherits the list from the one before
        if style == "SignatureBlock":
            wc.run("para.indents", left=self.sig_left, firstLine=0)
        for t, bold, ital in (runs(text) if isinstance(text, str) else text):
            if bold:
                wc.run("format.bold")
            if ital:
                wc.run("format.italic")
            wc.call("type_text", text=t)
            if bold:
                wc.run("format.bold")
            if ital:
                wc.run("format.italic")


LINE = 13.8  # one blank line of 12-point Times New Roman

# Times-Roman advance widths (AFM, per 1000 em), for fitting signature blocks.
_TIMES = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [722, 667, 667, 722, 611, 556, 722, 722, 333, 389, 722, 611, 889,
                                                  722, 722, 556, 722, 667, 556, 611, 722, 722, 944, 722, 722, 611]))
_TIMES.update(zip("abcdefghijklmnopqrstuvwxyz", [444, 500, 444, 500, 444, 333, 500, 500, 278, 278, 500, 278, 778,
                                                  500, 500, 500, 500, 333, 389, 278, 500, 500, 722, 500, 500, 444]))
_TIMES.update({" ": 250, ",": 250, ".": 250, "'": 333, "(": 333, ")": 333, "-": 333, "§": 500})


def sig_left(lines):
    """T&Q: the block starts 4.5 in. from the left edge, or further left so the longest line fits."""
    widest = max(sum(_TIMES.get(c, 500) for c in plain(ln)) * 12 / 1000 for ln in lines)
    return max(0, min(324, 468 - widest - 2))


def write_memo(w, doc, list_num):
    blocks, i = doc["blocks"], 0
    w.para("Normal", doc["date"], align="right")
    in_ind = False
    while i < len(blocks):
        kind, val = blocks[i]
        if kind == "memofor":
            w.para("MEMOFOR", [("MEMORANDUM FOR  ", False, False)] + runs(val), before=0 if in_ind else LINE)
        elif kind == "from":
            w.para("FROM", [("FROM:  ", False, False)] + runs(val), before=LINE)
        elif kind == "subject":
            w.para("SUBJECT", [("SUBJECT:  ", False, False)] + runs(val), before=LINE, after=LINE)
        elif kind == "num0":
            w.para("Body", val, num={"level": 0, "num": list_num})
        elif kind == "num1":
            w.para("Body", val, num={"level": 1, "num": list_num})
        elif kind == "para":
            w.para("Body", val, num={"level": 0, "num": 0}, before=LINE if in_ind else None)
        elif kind == "sig":
            w.sig_left = sig_left(val)
            for j, line in enumerate(val):
                w.para("SignatureBlock", line, before=4 * LINE if j == 0 else 0)
        elif kind == "attach":
            for j, line in enumerate(val):
                w.para("Normal", line, before=2 * LINE if j == 0 else 0)
        elif kind == "ind":
            in_ind = True
            w.para("Normal", val, before=3 * LINE, after=LINE)
        i += 1


def write_letter(w, doc):
    w.para("Normal", doc["date"], align="right")
    for kind, val in doc["blocks"]:
        if kind == "address":
            for j, line in enumerate(val):
                w.para("Normal", line, before=2 * LINE if j == 0 else 0)
        elif kind == "salute":
            w.para("Normal", val, before=LINE, after=LINE)
        elif kind == "para":
            w.para("BodyParagraph", val, after=LINE)
        elif kind == "close":
            sig = next((v for k, v in doc["blocks"] if k == "sig"), [val])
            w.sig_left = sig_left(sig)
            w.para("SignatureBlock", val)
        elif kind == "sig":
            w.sig_left = sig_left(val)
            for j, line in enumerate(val):
                w.para("SignatureBlock", line, before=4 * LINE if j == 0 else 0)
        elif kind == "attach":
            for j, line in enumerate(val):
                w.para("Normal", line, before=2 * LINE if j == 0 else 0)


def build(wc, spec, dates, work):
    doc = parse(spec["src"])
    code = re.match(r"^([RB]I-\d\d)", spec["key"])
    if code and not doc["date"]:
        doc["date"] = dates.get(code.group(1), "")
    lh = list(spec["lh"])
    if doc["lh1"]:
        lh[0] = doc["lh1"]
    stamp = ""
    if spec.get("mark"):
        stamp = " · ".join(["OPERATION ZUGZWANG", spec["mark"], doc["title"]] + doc["stamp_bits"])
    src = os.path.join(work, "in.docx")
    instantiate(spec["kind"], dict(LH1=lh[0], LH2=lh[1], LH3=lh[2], BANNER=doc["banner"], STAMP=stamp), src)
    wc.call("open_document", path=src)
    if not getattr(wc, "fonts_added", False):
        for f in serif_fonts():
            with open(f, "rb") as fh:
                wc.run("font.add", data=base64.b64encode(fh.read()).decode(), name=os.path.basename(f))
        wc.fonts_added = True
    wc.batch([("select.all", {}), ("text.delete", {})])
    w = Writer(wc, spec["kind"])
    if spec["kind"] == "memo":
        wc.batch([("para.reset", {}), ("para.style", {"style": "Body"})])
        wc.call("type_text", text="x")
        list_num = int(re.search(r'"num":\s*(\d+)', wc.run("list.get")).group(1))
        wc.batch([("select.all", {}), ("text.delete", {})])
        w.first = True
        write_memo(w, doc, list_num)
    else:
        write_letter(w, doc)
    base = os.path.join(OUT_DIR, spec["key"])
    wc.call("save_document", path=base + ".docx")
    wc.call("save_document", path=base + ".pdf")
    print("wrote", os.path.relpath(base, ROOT) + ".docx and .pdf")


def main(argv):
    os.makedirs(OUT_DIR, exist_ok=True)
    picks = [d for d in DOCS if not argv or any(a.lower() in d["key"].lower() for a in argv)]
    dates = read_dates()
    work = tempfile.mkdtemp(prefix="zz-tq-")
    try:
        with WordCraft(read_root=work, write_root=os.path.realpath(OUT_DIR)) as wc:
            for spec in picks:
                build(wc, spec, dates, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main(sys.argv[1:])
