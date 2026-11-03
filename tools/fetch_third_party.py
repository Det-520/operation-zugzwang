#!/usr/bin/env python3
"""Download the third-party files the project uses but doesn't keep in git.

    python3 tools/fetch_third_party.py           # fetch whatever is missing
    python3 tools/fetch_third_party.py --force   # fetch everything again
    python3 tools/fetch_third_party.py --check   # only report what is missing or different

These files belong to others, so .gitignore keeps them out of the repo:

- references/: Mouat's Practical Advice on Matrix Games, AFH 33-337 The Tongue
  and Quill, and the doctrine PDFs in references/doctrine/. Each PDF also gets a
  plain-text copy in text/ (pdftotext -layout, from poppler-utils) for searching.
- tools/tq/templates/official/: the Air Force Tongue and Quill Word templates,
  which tools/tq/make_templates.py turns into the game's zz-*.dotx.
- Fonts: Inter (map/fonts/) and JetBrains Mono (tools/fonts/), SIL OFL.
- whitecell-site/: the just-the-docs v0.12.0 theme and the jekyll-include-cache
  plugin (MIT). The site's own files (_config.yml, *_custom.html, _sass/custom/,
  _sass/color_schemes/zugzwang.scss) are in git and are never overwritten.

Every file is checked against the SHA-256 of the copy the project was built with.
A different hash is a warning, not an error: the publisher may have issued a new
edition. Air Force and DoD sites often refuse scripted downloads. When one does,
the script prints the URL: open it in a browser and save the file to the path shown.
Standard library only.
"""
import argparse
import hashlib
import io
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.path.join(ROOT, "whitecell-site")
DOC = "references/doctrine/"
AF_DOC = "https://www.doctrine.af.mil/Portals/61/documents/"
TQ_TPL = "https://www.e-publishing.af.mil/Portals/1/Documents/The%20Tongue%20and%20Quill%20Doc/"

# (path, url, sha256). PDFs under references/ also get a text copy.
FILES = [
    ("references/PracticalAdviceOnMatrixGames.pdf", "http://www.mapsymbs.com/PracticalAdviceOnMatrixGames.pdf",
     "15106207bd58458fa6c15bafa6316b3eaafd2b3f6c2ee20058f15bf6e351f098"),
    ("references/AFH_33-337_Tongue_and_Quill.pdf", "https://static.e-publishing.af.mil/production/1/saf_cio_a6/publication/afh33-337/afh33-337.pdf",
     "65887fe7085227b34ed538624cbf122204609dae9fe9c98560cb2a83e7fe3e1c"),
    (DOC + "AFDP_1-1_Mission_Command_2023-08-14.pdf", AF_DOC + "AFDP_1-1/AFDP%201-1%20Mission%20Command.pdf",
     "5d18560e15144474e4fe5c516a976c00c71dc62840476d8b33f2d57a9d6c38f6"),
    (DOC + "AFDP_1-1_Placemat.pdf", AF_DOC + "AFDP_1-1/AFDP1-1Placemat.pdf",
     "2eee606eb032d5293a2bd978ca700e5eef78d05e4b0eef36e906344a20b0dc71"),
    (DOC + "AFDP_3-0_One_Pager.pdf", AF_DOC + "3.0%20One%20Pager%20Final.pdf",
     "7fc0f8678177f6e67603b2e75eaefdb1baa1003219880e00488a287451706b1a"),
    (DOC + "AFDP_3-0_Operations_2025-01-22.pdf", AF_DOC + "AFDP_3-0/AFDP%203-0%20Operations.pdf",
     "8ce76e1ba7e655ea05e9bf6ee3b731ab6c41c5ea8c3b6cb004b68b74fb7fd19a"),
    (DOC + "AFDP_3-0_Summary_of_Changes.pdf", AF_DOC + "AFDP_3-0/AFDP%203-0%20Summary%20of%20Changes.pdf",
     "2703d02f635355eee64b84f066ab5cc6b785eb72c0a5e2cf0e41d404e02c271f"),
    (DOC + "AFDP_3-99_DAF_Role_in_JADO_2021-11-19.pdf",
     "https://media.defense.gov/2022/Jan/19/2002924106/-1/-1/0/SDP%203-99,%20THE%20DAF%20ROLE%20IN%20JOINT%20ALL-DOMAIN%20OPERATIONS.PDF",
     "e7e1f6a945db7d2b1cf06b947c1159a6abcf3d5ba6a80df392e26da64865011a"),
    (DOC + "AFDP_5-0_One_Pager.pdf", AF_DOC + "5.0%20One%20Pager%20Final.pdf",
     "dd0c7fb402286accbe4a53a523c442ebdadbeae8cc62f870cb0f52661baee870"),
    (DOC + "AFDP_5-0_Planning.pdf", AF_DOC + "AFDP_5-0/AFDP%205-0%20Planning.pdf",
     "7d00ed67f3fdf374163fe3f7e9c5981956be77684ce60575c5279e652625e3f9"),
    (DOC + "JP_3-0_Joint_Operations_2017_SUPERSEDED.pdf", "https://irp.fas.org/doddir/dod/jp3_0.pdf",
     "c54cf86518caa0d43f6cbeabea255b8cb800a6d204a93268a9c8078bd54120a1"),
    (DOC + "JP_5-0_Joint_Planning_2020-12-01.pdf",
     "https://www.safety.marines.mil/Portals/92/Ground%20Safety%20for%20Marines%20(GSM)/References%20Tab/JP%205-0%20Joint%20Planning%20PDF.pdf",
     "6a32504b5875a4c7217da44c0f13ecaa918d61f5be6ac12b9bc4345db355dbd1"),
    ("tools/tq/templates/official/Official Memorandum Template (Classification Banners)_7oct2020.dotx",
     TQ_TPL + "Official%20Memorandum%20Template%20(Classification%20Banners)_7oct2020.dotx",
     "d5176d5615642fe5b02b9a06373c4d22cb6701159cf10c601335f02afd0081da"),
    ("tools/tq/templates/official/Personal Letter Template_10Nov2020.dotx",
     TQ_TPL + "Personal%20Letter%20Template_10Nov2020.dotx",
     "6369a4534089bd44797ab5d66922cfb5f1cb9278d34077d73c4c8f93ac8364de"),
]

# Archives: (url, sha256, [(member, path)]). A member ending in "/" is a folder.
INTER = "map/fonts/"
JBM = "tools/fonts/"
ARCHIVES = [
    ("https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip",
     "9883fdd4a49d4fb66bd8177ba6625ef9a64aa45899767dde3d36aa425756b11e",
     [("extras/otf/Inter-%s.otf" % w, INTER + "Inter-%s.otf" % w)
      for w in ("Regular", "Italic", "SemiBold", "SemiBoldItalic", "Bold", "BoldItalic")]
     + [("LICENSE.txt", INTER + "LICENSE.txt")]),
    ("https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip",
     "6f6376c6ed2960ea8a963cd7387ec9d76e3f629125bc33d1fdcd7eb7012f7bbf",
     [("fonts/ttf/JetBrainsMono-%s.ttf" % w, JBM + "JetBrainsMono-%s.ttf" % w) for w in ("Regular", "Italic", "Bold")]
     + [("OFL.txt", JBM + "OFL.txt")]),
    ("https://github.com/just-the-docs/just-the-docs/archive/refs/tags/v0.12.0.tar.gz",
     "4373960109aa03099789c09c8011fba4d104cf965325c7581cd13b6a4af1ce3a",
     [("just-the-docs-0.12.0/%s/" % d, "whitecell-site/%s/" % d) for d in ("_layouts", "_includes", "_sass", "assets")]
     + [("just-the-docs-0.12.0/LICENSE.txt", "whitecell-site/THEME-LICENSE.txt")]),
    ("https://github.com/benbalter/jekyll-include-cache/archive/refs/tags/v0.3.1.tar.gz",
     "034a10e7a10107e94192a924e4279d881b1e12b5c7a7268cc8f156bbc91c05b3",
     [("jekyll-include-cache-0.3.1/lib/", "whitecell-site/_plugins/"),
      ("jekyll-include-cache-0.3.1/LICENSE.md", "whitecell-site/_plugins/jekyll-include-cache-LICENSE.txt")]),
]

# The site's own files, which sit among the theme's: never overwritten.
SITE_OWN = {"whitecell-site/_includes/head_custom.html", "whitecell-site/_includes/header_custom.html",
            "whitecell-site/_sass/custom/custom.scss", "whitecell-site/_sass/custom/setup.scss"}

AGENT = "operation-zugzwang/fetch_third_party.py (+https://github.com/j-nac/operation-zugzwang)"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


# What each kind of file starts with: a page from a bot check is not the file.
MAGIC = {".pdf": b"%PDF", ".dotx": b"PK", ".zip": b"PK", ".gz": b"\x1f\x8b"}


def download(url, kind):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    if not data.startswith(MAGIC[kind]):
        raise ValueError("the server sent something other than the file (%d bytes, HTTP %d)" % (len(data), r.status))
    return data


def write(rel, data):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def text_copy(rel):
    """references/x/Name.pdf -> references/x/text/Name.txt"""
    pdf = os.path.join(ROOT, rel)
    txt = os.path.join(os.path.dirname(pdf), "text", os.path.splitext(os.path.basename(pdf))[0] + ".txt")
    if os.path.exists(txt) and os.path.getmtime(txt) >= os.path.getmtime(pdf):
        return True
    if not shutil.which("pdftotext"):
        print("  no pdftotext (poppler-utils): skipped the text copy of", rel)
        return False
    os.makedirs(os.path.dirname(txt), exist_ok=True)
    if subprocess.run(["pdftotext", "-q", "-layout", pdf, txt]).returncode:
        print("  pdftotext failed: no text copy of", rel)
        return False
    print("  text copy", os.path.relpath(txt, ROOT))
    return True


def fetch_files(force, check):
    failed = []
    for rel, url, want in FILES:
        path = os.path.join(ROOT, rel)
        have = os.path.exists(path)
        if have and not force:
            if check and sha256(open(path, "rb").read()) != want:
                print("differs  ", rel)
        elif check:
            print("missing  ", rel)
        else:
            try:
                data = download(url, os.path.splitext(rel)[1].lower())
            except Exception as e:  # noqa: BLE001 - report and carry on
                print("FAILED   %s (%s)\n  download it in a browser: %s" % (rel, e, url))
                failed.append(rel)
                continue
            write(rel, data)
            print("fetched  ", rel, "" if sha256(data) == want else "(WARNING: not the copy the project was built with)")
        if rel.startswith("references/") and rel.endswith(".pdf") and os.path.exists(path) and not check:
            text_copy(rel)
    return failed


def members(arc, url):
    """{name: bytes} for every file in a zip or tar.gz."""
    if url.endswith(".zip"):
        z = zipfile.ZipFile(io.BytesIO(arc))
        return {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
    t = tarfile.open(fileobj=io.BytesIO(arc), mode="r:gz")
    return {m.name: t.extractfile(m).read() for m in t.getmembers() if m.isfile()}


def fetch_archives(force, check):
    failed = []
    for url, want, picks in ARCHIVES:
        dests = [p for _, p in picks]
        missing = [p for p in dests if not os.path.exists(os.path.join(ROOT, p))]
        if not missing and not force:
            continue
        if check:
            for p in missing:
                print("missing  ", p)
            continue
        try:
            arc = download(url, os.path.splitext(url)[1])
        except Exception as e:  # noqa: BLE001
            print("FAILED   %s (%s)" % (url, e))
            failed.append(url)
            continue
        if sha256(arc) != want:
            print("  WARNING: %s is not the copy the project was built with" % url)
        files = members(arc, url)
        n = 0
        for member, dest in picks:
            todo = [(member, dest)] if not member.endswith("/") else \
                [(m, dest + m[len(member):]) for m in files if m.startswith(member)]
            for m, d in todo:
                if d in SITE_OWN and os.path.exists(os.path.join(ROOT, d)):
                    continue
                write(d, files[m])
                n += 1
        print("fetched  ", url.rsplit("/", 1)[-1], "->", ", ".join(sorted({os.path.dirname(d.rstrip("/")) or d for d in dests})), "(%d files)" % n)
    return failed


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--force", action="store_true", help="fetch everything again")
    ap.add_argument("--check", action="store_true", help="only report what is missing or different")
    a = ap.parse_args()
    failed = fetch_files(a.force, a.check) + fetch_archives(a.force, a.check)
    if failed:
        print("\n%d download(s) failed. Save each one by hand to the path shown, then run this again for the text copies." % len(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
