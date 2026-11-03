# Operation Zugzwang

A matrix wargame over the Strait of Great Fortune, run as a group leadership project at AFROTC LLAB 12 (12 November 2026). Designer: C/Nacanaynay. Fictional training scenario.

> **Secrecy.** This repository holds both teams' secret packets, the white cell's ground truth, and the injects. Keep it private, and don't share it with players.

## Where things are

| Path | What it is |
| --- | --- |
| `RULES.md` | How to play: turns, COAs, adjudication, requests, injects |
| `LLAB-SETUP.md` | Event logistics: schedule, rooms, groups, staffing, evaluation |
| `scenario/` | The world, each side's forces and objectives, injects, and ground truth (`scenario/README.md`) |
| `handouts/` | The documents players and the white cell get, by audience. The markdown is the source for every PDF and the site. |
| `map/` | The map generator and its zone data (`map/README.md`) |
| `tools/` | Build scripts, the counters generator, the Tongue and Quill builder, and the white cell clock |
| `whitecell-site/` | The white cell reference site's own files (Jekyll) |
| `references/` | Training objective, writing and doctrine references |
| `archive/` | The designer's original hand-made PDFs and the v9 map |

`AGENTS.md` is the full file map and the rules for editing (also read by AI agents through `CLAUDE.md`). `handouts/PDF-BUILD-NOTES.md` lists the open design decisions.

## Building

The release PDFs, the map, and the site are built from the sources and aren't in git. Files that belong to others (the reference PDFs, the Air Force Word templates, the fonts, and the site theme) aren't in git either: a script downloads them.

```bash
python3 tools/fetch_third_party.py   # once after cloning
tools/build_all.sh                   # map, counters, Tongue and Quill documents, FINALIZED/, site
npx markdownlint-cli2                # after editing markdown: keep it at 0 issues
```

| Step | Script | Output |
| --- | --- | --- |
| Map | `tools/build_map.sh` | `map/maps/`, `map/data/`, `handouts/assets/game-map.png` |
| Release PDFs | `tools/build_handouts.sh` (`--only NAME` for one) | `FINALIZED/`, by release folder |
| White cell site | `tools/build_site.sh` (`serve` to preview) | `whitecell-site/_site/` |

Needs Python 3, Chromium 131 or later, poppler-utils (`pdftotext`, `pdftoppm`), Jekyll, and `wordcraft-cli` for the Tongue and Quill documents. On NixOS the scripts pull the Python packages with `nix-shell`. Elsewhere, install `markdown-it-py`, `mdit-py-plugins`, `pypdf`, `playwright`, `numpy`, `shapely`, and `pillow`.

Air Force sites often refuse scripted downloads. When one does, `fetch_third_party.py` prints the URL: open it in a browser, save the file to the path shown, and run the script again to check it and make its text copy.
