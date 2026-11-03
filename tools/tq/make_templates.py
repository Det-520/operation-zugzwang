#!/usr/bin/env python3
"""Make the Zugzwang Tongue and Quill templates from the official Air Force ones.

Reads  tools/tq/templates/official/*.dotx  (AF E-Publishing, Nov 2020; see README.md)
Writes tools/tq/templates/zz-memo.dotx and zz-letter.dotx

The official letterhead (DEPARTMENT OF THE AIR FORCE, unit, base) becomes the
tokens {{LH1}} {{LH2}} {{LH3}}, the classification banners become {{BANNER}},
and a small line {{STAMP}} goes above the letterhead for the game's product
label (ID and rating). The DoD seal is removed: the in-game senders are
fictional states. Both templates place the banner the same way, in plain text:
on the first page, the official memo's text box 0.2 in. from the top of the
page; on later pages, centered on the line with the page number; and in the
footer. build_tq.py fills the tokens for each document.
Standard library only.
"""
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OFFICIAL = os.path.join(HERE, "templates", "official")
OUT = os.path.join(HERE, "templates")

MEMO_SRC = "Official Memorandum Template (Classification Banners)_7oct2020.dotx"
LETTER_SRC = "Personal Letter Template_10Nov2020.dotx"

STAMP_P = ('<w:p><w:pPr><w:jc w:val="right"/><w:spacing w:after="0"/></w:pPr>'
           '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:sz w:val="16"/></w:rPr>'
           '<w:t xml:space="preserve">{{STAMP}}</w:t></w:r></w:p>')
BANNER_P = ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="0"/></w:pPr>'
            '<w:r><w:t xml:space="preserve">{{BANNER}}</w:t></w:r></w:p>')
LATER_P = ('<w:p><w:pPr><w:tabs><w:tab w:val="center" w:pos="4680"/><w:tab w:val="right" w:pos="9360"/></w:tabs>'
           '<w:spacing w:after="0"/></w:pPr><w:r><w:tab/><w:t xml:space="preserve">{{BANNER}}</w:t><w:tab/></w:r>'
           '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
           '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>2</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')


def one_run(xml, old_pieces, token):
    """Replace a phrase split over runs (old_pieces, in order) with one token."""
    first, rest = old_pieces[0], old_pieces[1:]
    xml, n = re.subn(r"(<w:t(?: [^>]*)?>)%s(</w:t>)" % re.escape(first), r"\g<1>%s\g<2>" % token, xml, count=1)
    assert n == 1, (first, token)
    for piece in rest:
        xml, n = re.subn(r"<w:r(?: [^>]*)?>(?:(?!</w:r>).)*<w:t(?: [^>]*)?>%s</w:t></w:r>" % re.escape(piece), "", xml, count=1, flags=re.S)
        assert n == 1, piece
    return xml


def letterhead(xml):
    xml = re.sub(r"<w:r(?: [^>]*)?>\s*<w:drawing>.*?</w:drawing>\s*</w:r>", "", xml, flags=re.S)
    xml = one_run(xml, ["DEPARTMENT OF THE AIR FORCE"], "{{LH1}}")
    try:
        xml = one_run(xml, ["123", "rd", " Example Squadron"], "{{LH2}}")
    except AssertionError:
        xml = one_run(xml, ["123RD", " Example Squadron"], "{{LH2}}")
    xml = one_run(xml, ["Placeholder Air Force Base"], "{{LH3}}")
    xml = one_run(xml, ["[Use approved organizational letterhead]"], "")
    return xml


def set_body(xml, inner):
    return re.sub(r"(<w:(hdr|ftr) [^>]*>).*(</w:\2>)", lambda m: m.group(1) + inner + m.group(3), xml, flags=re.S)


def banner_box(xml):
    """The first-page banner: the official memo's text box, in plain text (the official one is bold)."""
    xml = xml.replace("CLASSIFICATION BANNER MARKING", "{{BANNER}}")
    return re.sub(r"<w:rPr><w:b/><w:bCs/></w:rPr>(<w:t>\{\{BANNER\}\})", r"\1", xml)


def memo_banner_run():
    """The run holding the memo's banner text box, to reuse in the letter."""
    with zipfile.ZipFile(os.path.join(OFFICIAL, MEMO_SRC)) as z:
        xml = banner_box(z.read("word/header3.xml").decode("utf-8"))
    runs = re.findall(r"<w:r(?: [^>]*)?>(?:(?!<w:r[ >]).)*?<mc:AlternateContent>.*?</mc:AlternateContent></w:r>", xml, flags=re.S)
    box = [r for r in runs if "{{BANNER}}" in r]
    assert len(box) == 1, len(box)
    return box[0]


def after_open_tag(xml, tag, insert):
    i = xml.index("<w:%s " % tag)
    j = xml.index(">", i) + 1
    return xml[:j] + insert + xml[j:]


def rebuild(src, dst, edit):
    zin = zipfile.ZipFile(os.path.join(OFFICIAL, src))
    with zipfile.ZipFile(os.path.join(OUT, dst), "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith("word/media/") and item.filename.endswith(".gif"):
                continue  # the DoD seal
            if item.filename.endswith(".rels"):
                data = re.sub(rb'<Relationship [^>]*Target="media/[^"]*\.gif"/>', b"", data)
            if item.filename == "[Content_Types].xml":
                data = data.replace(b'<Default Extension="gif" ContentType="image/gif"/>', b"")
            if item.filename.endswith(".xml") and item.filename.startswith("word/"):
                data = edit(item.filename, data.decode("utf-8")).encode("utf-8")
            zout.writestr(item, data)


def memo_edit(name, xml):
    if name == "word/header3.xml":  # first page
        xml = banner_box(letterhead(xml))
        xml = after_open_tag(xml, "hdr", STAMP_P)
    elif name == "word/header2.xml":  # later pages
        xml = set_body(xml, LATER_P)
    elif name in ("word/footer2.xml", "word/footer3.xml"):
        xml = set_body(xml, BANNER_P)
    return xml


def letter_edit(name, xml):
    if name == "word/header2.xml":  # first page
        xml = letterhead(xml)
        xml = after_open_tag(xml, "hdr", STAMP_P.replace("</w:p>", memo_banner_run() + "</w:p>"))
    elif name == "word/header1.xml":  # later pages
        xml = set_body(xml, LATER_P)
    elif re.match(r"word/footer\d\.xml", name):
        xml = set_body(xml, BANNER_P)
    return xml


if __name__ == "__main__":
    rebuild(MEMO_SRC, "zz-memo.dotx", memo_edit)
    rebuild(LETTER_SRC, "zz-letter.dotx", letter_edit)
    print("wrote", os.path.join(OUT, "zz-memo.dotx"), "and zz-letter.dotx")
