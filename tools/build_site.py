#!/usr/bin/env python3
"""Generate the white cell reference site (whitecell-site/, just-the-docs) from the markdown.

    tools/build_site.sh            # generate, then jekyll build
    tools/build_site.sh serve      # generate, then jekyll serve

Each handout becomes a page. Each intelligence product (RI-xx, BI-xx) gets its
own page under its side, and the White Cell Intelligence and Injects document
is split into one page per section. RULES.md and LLAB-SETUP.md go under
Design reference. build/ and handouts/word/ are copied into downloads/.
The markdown is rendered with the same code as the PDFs (build_handouts.py),
so the pages hold HTML and Jekyll only wraps them in the theme.
"""
import glob
import html
import os
import re
import shutil
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_handouts import (FIN, FONTS, H, PACKET_NAME, REF_PACKET_NAME, ROOT, WC, clean, front_matter,  # noqa: E402
                            packet_markdown, render_markdown)

SITE = os.path.join(ROOT, "whitecell-site")
GENERATED = ["common", "redfor", "bluefor", "whitecell", "reference", "downloads", "tools", "assets/img", "assets/fonts", "index.html"]

# Accent class for each section, matching the PDFs: green public, red REDFOR, blue BLUEFOR, purple white cell.
AUDIENCE = {"common": "zz-aud-public", "redfor": "zz-aud-red", "bluefor": "zz-aud-blue"}


def baseurl():
    m = re.search(r'^baseurl:\s*"?([^"\n]*)"?', open(os.path.join(SITE, "_config.yml")).read(), re.M)
    return (m.group(1) if m else "").rstrip("/")


BASE = ""


def url(path):
    return BASE + "/" + "/".join(urllib.parse.quote(p) for p in path.strip("/").split("/"))


def image_url(path):
    """Copy an image the markdown uses into assets/img/ and return its site URL."""
    os.makedirs(os.path.join(SITE, "assets", "img"), exist_ok=True)
    shutil.copyfile(path, os.path.join(SITE, "assets", "img", os.path.basename(path)))
    return url("assets/img/" + os.path.basename(path))


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_page(rel, title, body, nav_order=None, parent=None, grand_parent=None, has_children=False, extra=""):
    lines = ["---", "title: " + yaml_str(title), "render_with_liquid: false"]
    if nav_order is not None:
        lines.append(f"nav_order: {nav_order}")
    if parent:
        lines.append("parent: " + yaml_str(parent))
    if grand_parent:
        lines.append("grand_parent: " + yaml_str(grand_parent))
    if has_children:
        lines.append("has_children: true")
    lines += ["permalink: /" + rel.rstrip("/") + "/", "---", ""]
    path = os.path.join(SITE, rel.rstrip("/") + ".html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    aud = AUDIENCE.get(rel.split("/")[0], "zz-aud-wc")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + extra + '<div class="zz-page %s">\n' % aud + body + "\n</div>\n")


def downloads_note(files):
    """A line of download links for a page: [(label, path under downloads/)]."""
    links = " · ".join('<a href="%s">%s</a>' % (url("downloads/" + p), html.escape(label)) for label, p in files)
    return '<p class="zz-downloads"><span>Download</span> %s</p>\n' % links


def head_html(meta, fallback=""):
    """The front matter's title (and subtitle) as the page heading. "Operation Zugzwang — X" puts the first part above."""
    title = meta.get("title", fallback)
    kicker, _, main = title.partition(" — ")
    if not main:
        kicker, main = "", title
    head = '<p class="zz-kicker">%s</p>\n' % html.escape(kicker) if kicker else ""
    head += "<h1>%s</h1>\n" % html.escape(main)
    if meta.get("subtitle"):
        head += '<p class="zz-doc-subtitle">%s</p>\n' % html.escape(meta["subtitle"])
    return head


def md_page(src, rel, title=None, dl=(), text=None, **nav):
    """One handout -> one page. Returns the page title."""
    path = os.path.join(ROOT, src)
    meta, text = front_matter(text if text is not None else open(path, encoding="utf-8").read())
    is_product = bool(re.match(r"^[RB]I-\d\d", os.path.basename(path)))
    text = clean(text, is_intel=is_product)
    body = render_markdown(text, os.path.dirname(path), image_url=image_url)
    head = head_html(meta) if meta.get("title") else ""
    title = title or meta.get("short") or meta.get("title") or plain_h1(text) or os.path.basename(src)
    write_page(rel, title, head + (downloads_note(dl) if dl else "") + body, **nav)
    return title


def plain_h1(text):
    m = re.search(r"^#{1,2} (.+)$", text, re.M)
    return re.sub(r"[*_`]", "", m.group(1)).strip() if m else None


def split_sections(src, rel, parent_title, nav_order, dl=()):
    """A long document -> a parent page (front matter and intro) plus one child page per ## section."""
    path = os.path.join(ROOT, src)
    meta, text = front_matter(open(path, encoding="utf-8").read())
    text = clean(text)
    parts = re.split(r"^(?=## )", text, flags=re.M)
    intro, sections = parts[0], parts[1:]
    head = head_html(meta, parent_title)
    toc = "<ol>%s</ol>" % "".join("<li>%s</li>" % html.escape(re.sub(r"^\d+\.\s*", "", plain_h1(s))) for s in sections)
    body = render_markdown(intro, os.path.dirname(path), image_url=image_url)
    write_page(rel, parent_title, head + (downloads_note(dl) if dl else "") + body + "<p>Sections (in the menu):</p>" + toc,
               nav_order=nav_order, parent="White Cell", has_children=True)
    for i, s in enumerate(sections, 1):
        title = re.sub(r"^\d+\.\s*", "", plain_h1(s))
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        s = re.sub(r"^#(#+ )", r"\1", s, flags=re.M)
        write_page(f"{rel}/{slug}", title, render_markdown(s, os.path.dirname(path), image_url=image_url),
                   nav_order=i, parent=parent_title, grand_parent="White Cell")


def intel_pages(side, label):
    top = f"{label} Intelligence"
    md_page(f"handouts/{side}/intel/00-read-me-first.md", f"{side}/intel", title=top, nav_order=4, parent=label, has_children=True,
            dl=[(f"{label} Full Intel (PDF)", f"{label} - 24H RELEASE/{label} Full Intel.pdf")])
    for i, md in enumerate(sorted(glob.glob(os.path.join(H, side, "intel", f"{side[0].upper()}I-*.md"))), 1):
        code = os.path.basename(md)[:5]
        word = glob.glob(os.path.join(H, "word", code + " *.docx"))
        dl = []
        if word:
            name = os.path.splitext(os.path.basename(word[0]))[0]
            dl = [("formatted PDF", f"word/{name}.pdf"), ("Word", f"word/{name}.docx")]
        md_page(os.path.relpath(md, ROOT), f"{side}/intel/{code.lower()}", nav_order=i, parent=top, grand_parent=label, dl=dl)


def copy_downloads():
    dst = os.path.join(SITE, "downloads")
    shutil.copytree(FIN, dst)
    shutil.copytree(os.path.join(H, "word"), os.path.join(dst, "word"))
    os.makedirs(os.path.join(SITE, "tools"), exist_ok=True)
    shutil.copyfile(os.path.join(ROOT, "tools", "whitecell-clock.html"), os.path.join(SITE, "tools", "whitecell-clock.html"))
    shutil.copytree(FONTS, os.path.join(SITE, "assets", "fonts"))
    rows = []
    for folder in sorted(os.listdir(dst)):
        if not os.path.isdir(os.path.join(dst, folder)):
            continue
        for f in sorted(os.listdir(os.path.join(dst, folder))):
            rows.append("<tr><td>%s</td><td><a href=\"%s\">%s</a></td></tr>" % (html.escape(folder), url(f"downloads/{folder}/{f}"), html.escape(f)))
    body = ("<h1>Downloads</h1>\n<p>The release files exactly as they go to each audience. Each release folder goes only to "
            "the audience its name gives. <code>word</code> holds the Tongue and Quill documents as Word files, for editing.</p>\n"
            "<table><thead><tr><th>Release</th><th>File</th></tr></thead><tbody>%s</tbody></table>" % "".join(rows))
    write_page("downloads", "Downloads", body, nav_order=7)


INDEX = """---
title: "Home"
nav_order: 1
render_with_liquid: false
permalink: /
---

<div class="zz-page zz-aud-wc">
<p class="zz-kicker">Operation Zugzwang</p>
<h1>White Cell</h1>
<p class="zz-doc-subtitle">AFROTC LLAB 12 · 12 November 2026 · <strong>WHITE CELL ONLY</strong></p>
<p>Every document in the game, for the lead adjudicators and loggers. This site shows <strong>both sides' secrets</strong>: hidden assets, secret objectives, intelligence ground truth, and injects. Keep it off the screens the players can see.</p>
<h2>During the game</h2>
<ul>
<li><a href="{clock}" target="_blank">Timer and dice program</a> (opens in a new tab; works offline once loaded)</li>
<li><a href="{checklist}">White Cell Checklist</a>: everything to do, in order, from a week out to cleanup</li>
<li><a href="{handbook}">White Cell Handbook</a>: running a turn, adjudication, scoring</li>
<li><a href="{injects}">Injects</a> and the <a href="{key}">intelligence product key</a></li>
<li><a href="{assets}">Master Asset List</a> and <a href="{forms}">White Cell Forms</a> (placement forms, trackers)</li>
<li><a href="{starting}">Starting conditions</a> and the <a href="{map}">game map (PDF)</a></li>
</ul>
<h2>Before the game</h2>
<ul>
<li><a href="{packet}">Print Packet</a>: everything one table prints, in one PDF</li>
<li><a href="{downloads}">Downloads</a>: every release folder as it goes to each audience</li>
</ul>
<h2>What's here</h2>
<table><thead><tr><th>Section</th><th>Contents</th><th>Players see it?</th></tr></thead><tbody>
<tr><td>White Cell</td><td>Handbook, Checklist, Intelligence and Injects (one page per section), Master Asset List, Forms, Print Packet</td><td>No</td></tr>
<tr><td>Common</td><td>Rules Handbook, Scenario Brief, Scenario Schedule, Starting Conditions, Player Forms</td><td>Both teams</td></tr>
<tr><td>REDFOR</td><td>Commander's letter, Team Packet, Order of Battle, and each intelligence product (RI-01 to RI-15) on its own page</td><td>REDFOR only</td></tr>
<tr><td>BLUEFOR</td><td>Commander's letter, Team Packet, Order of Battle, and each intelligence product (BI-01 to BI-15) on its own page</td><td>BLUEFOR only</td></tr>
<tr><td>Design reference</td><td>The full rules (<code>RULES.md</code>) and event setup (<code>LLAB-SETUP.md</code>)</td><td>No</td></tr>
<tr><td>Downloads</td><td>The release PDFs, counters, map, and the Tongue and Quill documents as Word files</td><td>By release folder</td></tr>
</tbody></table>
<p>Search with the box at the top (Ctrl+K). Generated from the project markdown by <code>tools/build_site.sh</code>.</p>
</div>
"""


def main():
    global BASE
    BASE = baseurl()
    for g in GENERATED:
        p = os.path.join(SITE, g)
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.exists(p):
            os.remove(p)

    # Section parents
    write_page("whitecell", "White Cell", "<h1>White Cell</h1><p>The white cell's own documents.</p>", nav_order=2, has_children=True)
    write_page("common", "Common", "<h1>Common</h1><p>Released to both teams.</p>", nav_order=3, has_children=True)
    write_page("redfor", "REDFOR", "<h1>REDFOR</h1><p>Released to REDFOR only, 24 hours before the LLAB.</p>", nav_order=4, has_children=True)
    write_page("bluefor", "BLUEFOR", "<h1>BLUEFOR</h1><p>Released to BLUEFOR only, 24 hours before the LLAB.</p>", nav_order=5, has_children=True)
    write_page("reference", "Design reference", "<h1>Design reference</h1><p>The designer's working documents. They carry [CANON], [PROPOSED], and [OPEN] tags.</p>", nav_order=6, has_children=True)

    md_page("handouts/whitecell/handbook.md", "whitecell/handbook", nav_order=1, parent="White Cell",
            dl=[("PDF", "White Cell/White Cell Handbook.pdf")])
    md_page("handouts/whitecell/checklist.md", "whitecell/checklist", nav_order=2, parent="White Cell",
            dl=[("PDF", "White Cell/White Cell Checklist.pdf")])
    split_sections("handouts/whitecell/intel-and-injects.md", "whitecell/intel-and-injects", "Intelligence and Injects", 3,
                   dl=[("PDF", "White Cell/White Cell Intelligence and Injects.pdf")])
    md_page("handouts/whitecell/master-asset-list.md", "whitecell/master-asset-list", nav_order=4, parent="White Cell",
            dl=[("PDF", "White Cell/Master Asset List.pdf"), ("counters", "White Cell/counters.pdf")])
    md_page("handouts/whitecell/forms.md", "whitecell/forms", nav_order=5, parent="White Cell",
            dl=[("PDF", "White Cell/White Cell Forms.pdf")])
    md_page("handouts/whitecell/print-packet.md", "whitecell/print-packet", nav_order=6, parent="White Cell",
            text=packet_markdown(), dl=[("PDF, one table", f"{WC}/{PACKET_NAME}"),
                                         ("PDF, reference forms only", f"{WC}/{REF_PACKET_NAME}")])

    md_page("handouts/common/rules-handbook.md", "common/rules-handbook", nav_order=1, parent="Common",
            dl=[("PDF", "Common Matrix - ASAP RELEASE/Player Rules Handbook.pdf")])
    md_page("handouts/common/scenario-brief.md", "common/scenario-brief", nav_order=2, parent="Common",
            dl=[("PDF", "Common Scenario - 1WK RELEASE/Scenario Brief.pdf"), ("map", "Common Scenario - 1WK RELEASE/map-full.pdf"),
                ("map tiles", "Common Scenario - 1WK RELEASE/map-tiles.pdf")])
    md_page("handouts/common/scenario-schedule.md", "common/scenario-schedule", nav_order=3, parent="Common",
            dl=[("PDF", "Common Scenario - 1WK RELEASE/Scenario Schedule.pdf")])
    md_page("handouts/common/starting-conditions.md", "common/starting-conditions", nav_order=4, parent="Common",
            dl=[("PDF", "Common Scenario - 1WK RELEASE/Starting Conditions.pdf")])
    md_page("handouts/common/player-forms.md", "common/player-forms", nav_order=5, parent="Common",
            dl=[("PDF", "Common Matrix - ASAP RELEASE/Player Forms and Templates.pdf")])

    for side, label in (("redfor", "REDFOR"), ("bluefor", "BLUEFOR")):
        rel = f"{label} - 24H RELEASE"
        md_page(f"handouts/{side}/commanders-letter.md", f"{side}/commanders-letter", title="Commander's Letter", nav_order=1, parent=label,
                dl=[("formatted PDF", f"{rel}/{label} - Commander's Letter.pdf"), ("Word", f"word/{label} - Commander's Letter.docx")])
        md_page(f"handouts/{side}/team-packet.md", f"{side}/team-packet", title="Team Packet", nav_order=2, parent=label,
                dl=[("PDF", f"{rel}/{label} Team Packet.pdf")])
        md_page(f"handouts/{side}/order-of-battle.md", f"{side}/order-of-battle", title="Order of Battle", nav_order=3, parent=label,
                dl=[("PDF", f"{rel}/{label} Order of Battle.pdf"), ("counters", f"{rel}/counters.pdf")])
        intel_pages(side, label)

    md_page("RULES.md", "reference/rules", title="Full rules (RULES.md)", nav_order=1, parent="Design reference")
    md_page("LLAB-SETUP.md", "reference/llab-setup", title="Event setup (LLAB-SETUP.md)", nav_order=2, parent="Design reference")

    copy_downloads()
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX.format(clock=url("tools/whitecell-clock.html"), handbook=url("whitecell/handbook/"),
                             checklist=url("whitecell/checklist/"), packet=url("whitecell/print-packet/"),
                             starting=url("common/starting-conditions/"), downloads=url("downloads/"),
                             injects=url("whitecell/intel-and-injects/injects/"),
                             key=url("whitecell/intel-and-injects/intelligence-product-key/"),
                             assets=url("whitecell/master-asset-list/"), forms=url("whitecell/forms/"),
                             map=url("downloads/Common Scenario - 1WK RELEASE/map-full.pdf")))
    print("generated", os.path.relpath(SITE, ROOT))


if __name__ == "__main__":
    main()
