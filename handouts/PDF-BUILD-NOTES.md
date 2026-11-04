# PDF Build Notes and Open Decisions

**Audience:** designer and white cell only. Mentions hidden assets and white-cell material.

## 1. How the PDFs are made now

Since 3 Nov 2026 the files in `build/` are **built from the handout markdown**, so the markdown and the PDFs no longer drift apart. The earlier list of differences between them is closed: every fix in it is in the rebuilt PDFs. The designer's hand-made Word PDFs are in git history (commit `f7c9263`, `archive/FINALIZED-2026-11-03/`).

| Step | Command | Output |
| --- | --- | --- |
| Third-party files, once after cloning (references, AF templates, fonts, site theme) | `python3 tools/fetch_third_party.py` | see `.gitignore` |
| Map | `tools/build_map.sh` | `map/maps/`, `map/data/`, `handouts/assets/game-map.png` |
| Counters | `python3 tools/make_counters.py` | `handouts/*/counters.pdf` |
| Tongue and Quill documents (both commander's letters, RI-13, BI-05, BI-10, BI-11) | `python3 tools/tq/build_tq.py` | `handouts/word/*.docx` and `.pdf` |
| Everything in `build/` (runs the counters and Tongue and Quill steps first) | `tools/build_handouts.sh` | `build/**` |
| White cell site | `tools/build_site.sh` (or `tools/build_site.sh serve`) | `whitecell-site/_site/` |
| All of the above, in order (the map only if it's missing, or with `--map`) | `tools/build_all.sh` | all of the above |

The outputs aren't in git. Rebuild them after cloning.

**Don't edit the PDFs by hand.** A hand edit is lost on the next build. Change the markdown and rebuild. If a PDF ever has to be finished by hand (for example, in Word), record here what was changed, so the next build doesn't silently undo it.

### 1.1 What changed from the hand-made PDFs

- **Ordinary handouts** were first built in the designer's Word layout (Calibri, blue headings). Since the restyle (§1.2) they use the markdown.style "Repo" look instead.
- **Tongue and Quill documents** are built in WordCraft through its MCP server (`wordcraft-cli mcp`), from the official AF E-Publishing templates (Official Memorandum with Classification Banners, and Personal Letter, Nov 2020). `tools/tq/templates/official/` has the originals, and `tools/tq/make_templates.py` makes the game versions: fictional letterhead and banners, with the DoD seal removed. The Word files in `handouts/word/` use Times New Roman and Copperplate Gothic. In the PDFs, Liberation Serif (same metrics) stands in for Times New Roman, and a sans-serif font stands in for Copperplate Gothic, because neither is installed. Open the `.docx` in Word and re-export it if you want the exact fonts.
- **Letterheads** the markdown didn't name are now set in `tools/tq/build_tq.py` (`DOCS`): CNDF Office of the Chairman of the Joint Staff; Omak Executive Office of the President; Cosmopolis Ministry of Defense, Office of International Security Affairs (RI-13); Omak Ministry of the Interior (BI-05); Asotin Ministry of Foreign Affairs (BI-10); NDF Logistics Command, Fortune Harbor (BI-11).
- **Intel memo dates** come from each side's Read Me First table (RI-13 D−5, BI-05 D−3, BI-10 D−10, BI-11 D−6). Each product's rating and caption print in a small line above the letterhead, outside the memo, as its FORMAT NOTE asks.
- **BI-10** gained a receiver's address ("The President of the Republic of Omak, Omak City"), which the personal-letter format requires.
- **Full Intel** files still combine each side's products, one product per page. On the white cell site each product has its own page.
- **Audience lines and FORMAT NOTEs** stay in the markdown only, as before. The running header (or, on Tongue and Quill documents, the banner and the product line) carries the audience.
- **White Cell Forms §4:** the placement forms' state boxes are now "☐ R ☐ D ☐ X" with a legend, so the "Now in" column has room to write.

### 1.2 Restyle and new documents (3 Nov 2026)

- **Look:** the "Repo" theme from markdown.style (GitHub's markdown style): Noto Sans (the system font stack on the build machine), JetBrains Mono for code and cables, rules under the top two heading levels, zebra-striped tables. Each audience has one accent colour, used for the marking in the header, the title rule, table headers, and forms: green public, red REDFOR, blue BLUEFOR, purple white cell. The white cell site uses the same palette.
- **Margins:** pages have 0.75 in side margins, 0.9 in top, 0.8 in bottom. The running header (short name · `// MARKING //` · date) and the footer (document name · "Page X of Y") are CSS page-margin boxes, at least 0.45 in from the paper edge, so a printer that can't print to the edge loses nothing. Print at 100%.
- **Forms** are real forms now: a tinted label column, room to write, and drawn check boxes. Layout hooks are HTML comments in the markdown (`<!-- zz:form -->` and others, listed in `tools/build_handouts.py`), so the markdown passes markdownlint.
- **Player Forms:** request slips are 3 to a page with dashed cut lines, and the printing note asks for 9 pages a team (25 slips: 4 in Phase I and 3 a turn for 7 turns; the old note said "about 8"). The COA worksheet's "Planned COA?" line moved up beside Turn / Team, and the Cons worksheet gained a "Their COA" line. The OPORD template's content is unchanged (3.4 is still open).
- **White Cell Forms:** the score sheet gained the group, the lead adjudicator, the flight commanders, A/P/N boxes, and an end-state box for the debrief. The "Open Status Trackers" are now the **track board**, with cells big enough for a marker and cut-out track markers. Each placement form fits on one page.
- **New: Starting Conditions** (`handouts/common/starting-conditions.md`, in the 1-week release): Scenario Brief §6 as a one-page reference, then the nine cue cards, three to a page, coloured by side, with a "Removed on turn" line.
- **New: White Cell Checklist** (`handouts/whitecell/checklist.md`, White Cell folder): from a week out to cleanup, with a step-by-turn tick grid for Turns 1–7. It includes the "agree auto-success rules across all four tables" item from §4 below.
- **New: Print Packet** (`White Cell/Print Packet - One Table.pdf`): everything one table prints, in order and with the right number of copies, behind a cover sheet that lists it. Print one per table. `PACKET` in `tools/build_handouts.py` sets the contents.
- **Markdown headings:** documents with a front-matter title now use `##` for their numbered sections (markdownlint MD025), and bold lines used as headings are headings. Section numbers and cross-references are unchanged.

### 1.3 Printing changes (3 Nov 2026, later)

- **Map tiles are portrait.** `map/source/build_pdfs.py` now turns each landscape tile onto a portrait letter page (the top of the map at the page's left edge), so the whole Print Packet prints in one orientation. Same trim marks. The tiles are now a 3 x 3 grid (9 pages, 31.5 x 22.7 in assembled), and `map-full.pdf` is drawn at the same scale.
- **Less ink on paperwork.** Forms, worksheets, slips, logs, and table headers have no filled bars, tinted label columns, zebra stripes, or shaded blocks. A form's title is dark text between an accent rule and a dark rule. Quotes and cables keep their outline only. Colour stays on the game pieces: counters, map, cue cards, track board, and track markers.
- **Track board in colour.** `track_colours()` in `tools/build_handouts.py` shades the cells: International Opinion runs from blue (−3, pro-Omak) through white to red (+3, pro-Cosmopolis); Domestic Will is a red ramp and Regime Stability a blue one (deeper = better for that side); Strait Traffic turns amber as it closes. Opinion uses the same blue and red as `tools/whitecell-clock.html`. A • marks each trigger value, with a one-paragraph key under the board.
- **Reference Forms packet.** `White Cell/Print Packet - One Table, Reference Forms.pdf` is the same packet with one copy of each player form and slip per side and no spares. `packet_items()` in `tools/build_handouts.py` derives it from `PACKET`.
- **Spares in the Print Packet.** After both teams' forms come spares for either side: 3 pages of request slips (9 slips), 2 COA worksheets, 2 Cons worksheets, 2 secret COA slips, and one more placement form for each side. The cover lists them under "Spares, at the back".
- **Commander's letter banners.** Both letters now place the `// … SECRET //` banner the same way, in plain (not bold) text: 0.2 in. from the top of the first page (the official memo's text box), on later pages on the line with the page number, and in the footer. `tools/tq/make_templates.py` sets this for the memo and letter templates, so RI-13, BI-05, BI-10, and BI-11 match too.
- **White cell site.** Task-list check boxes hang in the left indent, so wrapped lines line up with the text (the PDFs do the same), and the site has no favicon.
- **Phase III name.** The handouts and the clock now use RULES.md §2.1's "Phase III – Planning and FRAGO" (the handbook, checklist, and schedule had said "Handover and FRAGO").

## 2. Decisions still open

These weren't changed, because each one either touches CANON or has more than one reasonable fix. A recommendation follows each. (Numbering kept from the earlier changelog. 3.1 map scale, 3.2 GRAYFOR, 3.3 forms, and 3.5 FRAGO are resolved.)

### 3.4 The OPORD template no longer has a place for planned COAs

The Player Forms §1 is now the bare five-paragraph outline. The Scenario Schedule §1.3 says to use that template for the Phase I brief, and the planned COAs (worth +1 each) are the most important part of it. **Recommendation:** add "d. Planned COAs (Turns 1–3; FRAGO: up to 2 for Phase IV)" under 3. EXECUTION.

### 3.6 Dates in the commander's letters

Both letters are dated **12 November 2026**, the real LLAB date. Every intelligence product uses relative dates (D−8, D−3), and the letters' FORMAT NOTEs say the in-game date is D−4. **Recommendation:** either date the letters "D−4", or accept the real date and note that 12 November is D−3 in the game.

### 3.7 Inject I-12 is now set in Phase III

The finalized injects table puts I-12 (mediation offer) in Phase III. Injects are "at most one per turn" and Phase III has no turns. A mediation offer during the Phase III handover could work well, because the new flight commander can fold it into the FRAGO. If that's the intent, say so in I-12's note ("read at the start of Phase III"). `scenario/whitecell-injects.md` was updated to Phase III to match.

### 3.8 Intelligence products: classification lines are now uneven

Most products lost their in-world classification line (RI-01, 03, 04, 11, 12; BI-01 to 04, 15). Four kept one: RI-08 and RI-10 ("COSMOPOLIS SECRET …"), RI-13 ("// COSMOPOLIS SECRET //"), and BI-05 ("// OMAK SECRET //"). It reads as accidental. **Recommendation:** keep them on all official products or on none.

### 3.9 Redaction gaps in the ASAP Rules Handbook

The redacted example still shows "PAT-1" (example resolution and §2.2), "NDF", and "Strait Traffic" once each, while redacting the same terms elsewhere. All of them are public in the Scenario Brief a week later, so nothing secret leaks. It only looks uneven.

### 3.10 Balance: REDFOR's R3 can fail before Turn 1

Opinion starts at −1, which already meets B-42's condition (Opinion ≤ −1). If BLUEFOR files B-42 as a Phase I RFF, the "volunteer" PAC-3 crews arrive on Turn 4 and R3 ("Cut Asotin out!") becomes Not achieved unless REDFOR first raises Opinion to 0. That gives REDFOR only three turns. The White Cell Handbook §7 warns about this but leaves it to judgment. **Recommendation:** set B-42's condition to Opinion ≤ −2, **or** REDFOR has struck an Asotin shipment.

### 3.11 The bypass routes weaken the Strait

The v10 map shows a southern bypass around Omak of about +650 mi (+45%), about 2 days at 15 kt. If the white cell reads that literally, closing the Strait costs shipping 2 days, which is mild next to the −1 Domestic Will every turn the Strait stays Closed. **Recommendation:** keep the penalty and give the white cell one line to say if asked: the bypass runs through open ocean along Omak's south coast, inside the reach of Omak's aircraft and Asotin's navy, so insurers and shipowners treat it as no safer than the Strait.

## 4. Smaller notes

- The finalized White Cell Handbook dropped the "run-through" and "agree auto-success rules across all four tables" prep items. Comparable tables across the four groups matter for the evaluation in `LLAB-SETUP.md`. Consider restoring the second one.
