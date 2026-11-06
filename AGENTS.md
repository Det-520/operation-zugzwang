# Operation Zugzwang — Guide for AI Agents (and Humans Editing the Docs)

This repository holds the design for **Operation Zugzwang**, a matrix wargame run as a group leadership project at AFROTC LLAB 12 (12 Nov 2026). **Owner and designer: C/Nacanaynay.** Read this file before you change anything. `README.md` covers setup and building.

## File map

| Path | What it is | Notes |
| --- | --- | --- |
| `RULES.md` | Game mechanics: turns, COAs, adjudication, requests, injects | Single source of truth for *how* to play |
| `LLAB-SETUP.md` | Event logistics: schedule, rooms, groups, flight commanders, POC staffing, evaluation, risks | Not game rules |
| `scenario/README.md` | Scenario index, packet assembly, scenario open decisions | Start here for scenario work |
| `scenario/00-overview.md` | Public world: background, map, actors, tracks, starting conditions, timing, ROE | Goes to **both** teams |
| `scenario/redfor-packet.md` | REDFOR forces, intel estimate, objectives | **REDFOR + white cell only** |
| `scenario/bluefor-packet.md` | BLUEFOR forces, Asotin support, intel estimate, objectives | **BLUEFOR + white cell only** |
| `scenario/whitecell-injects.md` | Kickoff inject, inject pool, Tekoa actor notes | **White cell only** |
| `scenario/whitecell-ground-truth.md` | Truth behind each side's intel, scoring notes | **White cell only** |
| `scenario/data/assets.csv` | One row per asset, mirrored from the packets. `parts` (blank = 1) prints that many lettered counters (B-07a, b, c) for an asset spread over several zones, with part zones listed in `zone` as `Z8;Z10` and an optional singular `part_asset` name for each part. RFF rows give the arrival zone. | Run `python3 tools/check_assets.py` after edits, then `python3 tools/make_counters.py` to regenerate the printable counters (`handouts/{redfor,bluefor,whitecell}/counters.pdf`) |
| `tools/whitecell-clock.html` | The timer, dice, and track program the lead adjudicator runs, covering the whole run of show on one screen (`LLAB-SETUP.md` §3; `RULES.md` §2.2, §4; App. C; `scenario/00-overview.md` §5.1) | One self-contained file that works offline. Open it in a browser. It holds durations only, with no clock times, so it can run at any start time. If the block order or durations, turn timings, result bands, the estimative-vote table, or the tracks change, update its `BLOCKS`, `turnSteps`, `BANDS`, `VOTES`, and `TRACKS` definitions. |
| `handouts/<group>/*.md` | The documents players and the white cell use, in four audience folders: `common/` (rules handbook, scenario brief, scenario schedule, starting conditions, player forms), `redfor/` and `bluefor/` (commander's letter, team packet, order of battle, and an `intel/` folder with one file per intelligence product plus `00-read-me-first.md`), `whitecell/` (handbook, checklist, intelligence and injects, master asset list, forms) | Mostly derived from the design docs, so update them when those change. The intelligence products (RI-xx, BI-xx) and their key exist only here. The folder sets the audience, and the same secrecy rules apply as in `scenario/`. The markdown is the source for the PDFs and the site (see the build rows below). Audience lines and `FORMAT NOTE` blocks stay in the markdown only. A `FORMAT NOTE` names the Tongue and Quill format a document uses. `common/starting-conditions.md` repeats Scenario Brief §6 as a reference page and cue cards, so change both together. The white cell's Print Packet cover has no markdown file: `packet_markdown()` in `tools/build_handouts.py` writes it. |
| `build/` | The release files (not in git), in release folders: `Common Matrix - ASAP RELEASE`, `Common Scenario - 1WK RELEASE`, `REDFOR - 24H RELEASE`, `BLUEFOR - 24H RELEASE`, `White Cell` | **Generated.** Don't edit the PDFs: change the markdown and run `tools/build_handouts.sh` (or `tools/build_all.sh` for everything). `tools/build_handouts.py` `RELEASES` lists which markdown makes which file. `handouts/PDF-BUILD-NOTES.md` records the open decisions about the build. |
| `tools/build_handouts.sh` | Builds everything in `build/`: it checks `assets.csv` and makes the counters, then the Tongue and Quill documents, then each handout (markdown → HTML → PDF in Chromium), the Full Intel files, copies of the counters, map, and clock, and last the white cell's `Print Packet - One Table.pdf` (`PACKET` in `tools/build_handouts.py` sets what goes in it and how many copies) and `Print Packet - One Table, Reference Forms.pdf` (one copy of each player form per side, no spares) | NixOS: the script pulls Python packages with `nix-shell`. Elsewhere it needs `markdown-it-py`, `mdit-py-plugins`, `pypdf`, and `playwright` with Chromium 131 or later. `--only NAME` builds part of it, and `SKIP_TQ=1` uses the committed `handouts/word/` files instead of running WordCraft. The look is the "Repo" theme from markdown.style (GitHub's markdown style) with one accent per audience; the header and page numbers sit inside the page margins. Layout hooks are HTML comments in the markdown (`<!-- zz:form -->` before a table, `<!-- zz:begin cards -->` … `<!-- zz:end -->`, `<!-- pagebreak -->`); the module docstring lists them. JetBrains Mono goes in `tools/fonts/` (OFL; fetched). |
| `tools/tq/` | The Tongue and Quill documents (both commander's letters, RI-13, BI-05, BI-10, BI-11), built with WordCraft through its MCP server: `build_tq.py` (reads the markdown, writes `handouts/word/*.docx` and `.pdf`), `wcmcp.py` (MCP client), `make_templates.py` and `templates/` (`official/` holds the AF templates, which are fetched; `zz-*.dotx` are the game versions, in git) | Letterheads not named in the markdown are set in `build_tq.py` `DOCS`. A new Tongue and Quill document needs an entry there. Needs `wordcraft-cli` on the PATH. |
| `handouts/word/` | Generated Word and PDF versions of the Tongue and Quill documents, kept in git because CI can't run WordCraft | Don't edit them. Change the markdown, run `python3 tools/tq/build_tq.py`, and commit the results. |
| `whitecell-site/` | The white cell reference site (Jekyll, just-the-docs v0.12.0; the theme is fetched, not in git): every handout, one page per intelligence product, the Intelligence and Injects document split by section, `RULES.md`, `LLAB-SETUP.md`, and downloads | **White cell only.** Run `tools/build_site.sh` (or `tools/build_site.sh serve`) after `tools/build_handouts.sh`. The pages are generated by `tools/build_site.py`; see `whitecell-site/README.md` for which files are hand-written. Don't publish it where players can reach it. |
| `map/` | The game map (v10) and the Python that generates it: `maps/strait_map_v10_full.pdf` (one page) and `maps/strait_map_v10_tiles_letter.pdf` (letter tiles), built into `maps/` (not in git), with zone data in `data/` | Edit `map/source/make_map.py`, then run `tools/build_map.sh`. It rebuilds `maps/`, `data/`, and `handouts/assets/game-map.png`, the image `handouts/common/scenario-brief.md` embeds. The output is identical on every run. If a distance changes, update `scenario/00-overview.md` §3.3. `tools/build_handouts.sh` copies the v10 PDFs into `build/Common Scenario - 1WK RELEASE/` as `map-full.pdf` and `map-tiles.pdf`. |
| `.markdownlint-cli2.jsonc` | markdownlint settings: every rule on except line length (MD013), since the files keep one paragraph per line | Run `npx markdownlint-cli2` after editing any markdown, and keep it at 0 issues. Don't use inline HTML (MD033): use the `zz:` comment hooks instead. |
| `references/` | `training-objective.txt` (LLAB training objective 1.3 and its performance measures), `tongue-and-quill-summary.md`, and the third-party references: AFH 33-337 *The Tongue and Quill*, Tom Mouat's *Practical Advice on Matrix Games* v15 (the method), and `doctrine/` (AFDP and JP PDFs), each with a `text/` copy for grep | Read-only. The PDFs and text copies are not in git: `python3 tools/fetch_third_party.py` downloads them. The summary says which format and style each handout uses. Indexed in `references/README.md` and `references/doctrine/README.md`. |
| `tools/fetch_third_party.py` | Downloads everything that belongs to others: the reference PDFs (and makes their text copies), the AF Word templates, the Inter and JetBrains Mono fonts, and the site theme | Run once after cloning. Each file is checked against a SHA-256. Air Force sites often refuse scripted downloads; the script then prints the URL to open in a browser. |
| `.github/workflows/pages.yml` | GitHub Action: on every push to `main`, runs `SKIP_TQ=1 tools/build_all.sh` and publishes `whitecell-site/_site/` to GitHub Pages (`https://j-nac.github.io/operation-zugzwang/`; `baseurl` in `whitecell-site/_config.yml` must match) | The Pages site is public, and this site shows both sides' secrets. |
| `tools/build_all.sh` | Builds everything in order: the map (if missing, or with `--map`), then `tools/build_handouts.sh`, then `tools/build_site.sh` | Fetch the third-party files first. |

## Status tags

| Tag | Meaning | What you may do |
| --- | --- | --- |
| **[CANON]** | Decided by the designer | Don't change it without the designer's explicit approval |
| **[PROPOSED]** | Drafted to fill a gap | Refine it. Say what you changed and why. |
| **[OPEN]** | Awaiting the designer's decision | Present options with a recommendation. Don't decide silently. |

Open decisions are listed in `RULES.md` §11 and `scenario/README.md`.

## Rules for editing

1. **Keep the separation.** Mechanics go in `RULES.md`, event logistics in `LLAB-SETUP.md`, and world facts in `scenario/`. Reference other files by path and section rather than restating them.
2. **Secrecy is enforced by files.** Each file has an audience line at the top. Never put hidden assets, secret objectives, injects, or ground truth into `00-overview.md`, and never put one side's secrets into the other side's packet. Watch for indirect leaks too: a public file must not describe a capability that only the hidden asset list reveals.
3. **IDs are stable.** Assets (R-xx, B-xx), zones (Zxx), starting conditions (S-Rx, S-Bx), objectives (R1–R3, B1–B3), injects (I-xx), intelligence products (RI-xx, BI-xx), and open items (Ox, Sx) are referenced across files and on the White Cell Forms. Add new items with new IDs. Don't renumber.
4. **Forces have two homes.** When you change a force table in a packet, update `scenario/data/assets.csv` and run `python3 tools/check_assets.py`.
5. **Keep it simple.** The designer consistently chooses simplicity: no turn-order switching, no event cards, no recalculation of late objections. A turn is 15 minutes, and the white cell has 2 minutes to resolve both COAs. Any proposed rule should state its time cost.
6. **All assets are real U.S. systems** (CANON), with an Air Force emphasis. Use unclassified, approximate capabilities. Every asset needs a stated limitation the other side can use as a Con. Tag REDFOR Air Force assets with their AFDP 3-0 core function.
7. **Write in-world documents the way the real thing reads.** Follow `references/tongue-and-quill-summary.md`: plain language, BLUF, active voice, understated tone. Official correspondence uses the Tongue and Quill memorandum or letter format; intelligence products use the intelligence conventions in its §6. Write the words only, and add a `FORMAT NOTE` for layout the designer will do by hand.
8. **Ground doctrine claims** in `references/doctrine/` by citing the file and section. Note that `references/doctrine/JP_3-0_Joint_Operations_2017_SUPERSEDED.pdf` is the 2017 edition; the 2022 edition is CAC-only.

## CANON scenario facts (quick reference)

- **Cosmopolis** = REDFOR (CNDF). It claims to be democratic, with an apolitical military. It is very large, rich, populous, and advanced, ~8,000 mi NE of the conflict. It hosts the exiled Sapphire president. Its objectives are aggressive.
- **Omak** = BLUEFOR. Its parts are the NDF (apolitical), the Sapphire Party (ousted, allied with Cosmopolis through trade deals and a defense treaty), the Indigo Party, and the PFA (Indigo's armed wing). An election controversy over revealed Cosmopolis backing led to an uprising, and the NDF let the PFA seize power. Its objectives are defensive.
- **Strait of Great Fortune:** Omak on the south shore, Tekoa on the north. Tekoa is neutral, sparse, mountainous, weak, and decentralized, with pirates, gangs, and tribes.
- **Latah** (west of Tekoa) and **Camas** (an island east of Tekoa) side with Cosmopolis.
- **Asotin** is ~1,200 mi W of Omak, comparable to Cosmopolis, a peer adversary of Cosmopolis, and it **backs the PFA**.
- **Balance:** REDFOR has more assets. BLUEFOR has home-ground, population, and Asotin advantages.
- Each side has 3 secret objectives.

## Useful ideation tasks

- Stress-test balance by playing out likely COA sequences for both sides.
- Draft each side's intel report in that actor's own voice (Mouat: one page, short and interesting).
- Design printable counters from `scenario/data/assets.csv`, plus the tracks in `scenario/00-overview.md` §5.
- Propose extra injects in the I-xx format.
- Write a "Turn Zero" practice example for homework.

## Balance heuristics

- Each side should have at least 3 strong non-kinetic COA options.
- BLUEFOR's advantages should make a REDFOR win *costly*, not impossible.
- No single COA should be able to settle an objective.
