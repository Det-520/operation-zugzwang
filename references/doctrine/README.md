# Doctrine Library — Operation Zugzwang

These are the doctrine references named in the LLAB 1.3 Training Objective (`../training-objective.txt`), downloaded 19 Oct 2026. They aren't in git: `python3 tools/fetch_third_party.py` downloads them from the URLs listed in that script and checks each one against the copy downloaded on that date. Every PDF has a plain-text copy in `text/` made with `pdftotext -layout`. Use the text copies for searching and for AI agents, and the PDFs for printing and figures.

| File | Publication | Edition | Source | Status / notes |
| --- | --- | --- | --- | --- |
| `AFDP_3-0_Operations_2025-01-22.pdf` | AFDP 3-0, *Operations* | 22 Jan 2025 | doctrine.af.mil | Current. Covers tenets of airpower, principles of joint ops, the 5 USAF core functions, the competition continuum, and ACE (App. C). Took over the JADO content from AFDP 3-99. |
| `AFDP_3-0_Summary_of_Changes.pdf` | AFDP 3-0 summary of key changes | 2025 | doctrine.af.mil | Says the JADO material was added "to eventually rescind AFDP 3-99." |
| `AFDP_3-0_One_Pager.pdf` | AFDP 3-0 one-pager | 2025 | doctrine.af.mil | Good handout for cadets. |
| `AFDP_5-0_Planning.pdf` | AFDP 5-0, *Planning* | Jan 2025 (PDF created 22 Jan 2025) | doctrine.af.mil | Current. Covers the Air Force Planning Process (AFPP): COA development (Ch 5), **COA analysis & wargaming (Ch 6)**, modified five-paragraph order (App. E), and the AFPP kneeboard (App. F). |
| `AFDP_5-0_One_Pager.pdf` | AFDP 5-0 one-pager | 2025 | doctrine.af.mil | Good handout for cadets. |
| `AFDP_1-1_Mission_Command_2023-08-14.pdf` | AFDP 1-1, *Mission Command* | 14 Aug 2023 | doctrine.af.mil | Current. Covers mission command principles, the "Five Cs", and CC-DC-DE. |
| `AFDP_1-1_Placemat.pdf` | AFDP 1-1 placemat | 2023 | doctrine.af.mil | One-page summary graphic. |
| `AFDP_3-99_DAF_Role_in_JADO_2021-11-19.pdf` | AFDP 3-99 / SDP 3-99, *DAF Role in Joint All-Domain Operations* | 19 Nov 2021 | media.defense.gov (official DoD mirror) | **Being phased out.** The doctrine.af.mil link now returns 404, and AFDP 3-0 (2025) absorbed its content. Kept here because the training objective lists it. |
| `JP_5-0_Joint_Planning_2020-12-01.pdf` | JP 5-0, *Joint Planning* | 1 Dec 2020 | safety.marines.mil (official .mil host) | Latest edition with a public copy. jcs.mil now serves joint pubs only through JEL+ (CAC required), so check JEL+ for a newer edition. |
| `JP_3-0_Joint_Operations_2017_SUPERSEDED.pdf` | JP 3-0, *Joint Operations* | 17 Jan 2017, Change 1 (22 Oct 2018) | irp.fas.org mirror | **Superseded.** The current edition is JP 3-0, *Joint Campaigns and Operations* (18 Jun 2022), which is CAC-only on JEL+ (<https://jdeis.js.mil>). A cadre member with a CAC should download it and replace this file. The 2017 edition is still useful for principles of joint operations and joint functions. |

## Most useful sections for this wargame

| Topic | Where | Used in game for |
| --- | --- | --- |
| Tenets of airpower and principles of joint operations | AFDP 3-0, Ch 1 (p. 1–2) | Raw material for Pros and Cons. Players cite them as reasons. |
| Five USAF core functions | AFDP 3-0 ("USAF Functions and Capabilities") | REDFOR Air Force assets are tagged with their core function. |
| Agile Combat Employment (ACE) | AFDP 3-0, App. C | Dispersal and basing COAs (Camas/Latah). |
| Competition continuum | AFDP 3-0 Ch 1; AFDP 3-99 | Phase I (pre-war competition) → Phase II/III (armed conflict). |
| COA validity: Feasible, Acceptable, Suitable, Distinguishable, Complete | AFDP 5-0, Ch 5 (p. 39) | White cell screening test before adjudicating. |
| Action–Reaction–Counteraction wargaming | AFDP 5-0, Ch 6 (p. 42–46) | Doctrinal basis for the turn structure. |
| Modified five-paragraph order | AFDP 5-0, App. E (p. 83–84) | Phase I OPORD template. |
| Commander's intent and mission command principles | AFDP 1-1, p. 8+ | Phase I OPORD and flight commander role. |
| CC-DC-DE | AFDP 1-1, p. 3–4 | Discussion of how teams delegated and organized themselves |
| JADO principles | AFDP 3-99, p. 1–2 | Encourage cross-domain (space/cyber/EMS) COAs. |

## Searching the text copies

```bash
grep -n -i "commander's intent" text/AFDP_1-1_Mission_Command_2023-08-14.txt
grep -n -i "feasible" text/AFDP_5-0_Planning.txt
```
