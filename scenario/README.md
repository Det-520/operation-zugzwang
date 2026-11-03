# Operation Zugzwang — Scenario Index

**Owner:** C/Nacanaynay · **Version:** 0.3 (20 Oct 2026)

The scenario is split by **audience**, so a team packet is just a set of files and nothing has to be cut out by hand. The rules are in `RULES.md`, and the event logistics are in `LLAB-SETUP.md`.

## Files

| File | Contents | REDFOR | BLUEFOR | White cell |
| --- | --- | :---: | :---: | :---: |
| `00-overview.md` | BLUF, background, map and zones, actors, tracks, starting conditions, timing, ROE | ✅ | ✅ | ✅ |
| `redfor-packet.md` | REDFOR forces (incl. hidden), RFF pool, intel estimate, secret objectives | ✅ | ❌ | ✅ |
| `bluefor-packet.md` | BLUEFOR forces (incl. hidden), mobilization and Asotin pools, intel estimate, secret objectives | ❌ | ✅ | ✅ |
| `whitecell-injects.md` | Kickoff inject, inject pool, Tekoa actor notes | ❌ | ❌ | ✅ |
| `whitecell-ground-truth.md` | The truth behind each side's intel estimate, scoring notes | ❌ | ❌ | ✅ |
| `data/assets.csv` | Every counter as one row, for printing counters and checking consistency | ❌ | ❌ | ✅ |

`data/assets.csv` mirrors the force tables in the two packets. **The packets are the source of truth.** After editing a force table, update the CSV and run `python3 tools/check_assets.py` to confirm the two still match. Then run `python3 tools/make_counters.py` to rebuild the printable counters (`handouts/whitecell/counters.pdf` for both sides, plus one-side sheets in `handouts/redfor/` and `handouts/bluefor/`). Printing instructions are in `LLAB-SETUP.md` §8.

## Building team packets (≥ 24 h before the LLAB)

The printable documents are in `handouts/`, and the distribution list is in `handouts/whitecell/handbook.md` §2.1. The table below lists the design files they come from.

| Packet | Contents |
| --- | --- |
| **Common (both teams)** | `RULES.md` (§1 Quick-Start first), `scenario/00-overview.md`, `references/doctrine/AFDP_3-0_One_Pager.pdf`, `references/doctrine/AFDP_5-0_One_Pager.pdf`, `references/doctrine/AFDP_1-1_Placemat.pdf` |
| **REDFOR** | Common + `scenario/redfor-packet.md` + `handouts/redfor/intel/` (distributed ≥ 24 h ahead) |
| **BLUEFOR** | Common + `scenario/bluefor-packet.md` + `handouts/bluefor/intel/` (distributed ≥ 24 h ahead) |
| **White cell** | Everything |

## Open decisions (scenario)

Settled in `update-notes.txt` and recent reviews (now CANON): owner, the Sapphire president fled to Cosmopolis, Asotin is a peer adversary of Cosmopolis that backs the PFA, all assets are American, REDFOR has more assets, BLUEFOR has defender, population, and Asotin advantages, and Omak's capital is named **Omak City** (with port **Fortune Harbor** and seized ship **MV *Fortune's Promise***), and there is no GRAYFOR actor (Tekoa is a white-cell actor).

| ID | Decision | Draft assumes |
| --- | --- | --- |
| S1 | Final wording of the six secret objectives (packets §3) | As drafted |
| S2 | How far Asotin will escalate (the B-42 and B-43 conditions) | As in `bluefor-packet.md` §1.4 |
| S4 | Map distances and zone layout (`00-overview.md` §3). **Resolved:** the map is v10 (`map/maps/strait_map_v10_full.pdf`) at 100 mi per grid square, with Camas moved southwest into PrSM range. The distance table in `00-overview.md` §3.3 was re-measured from it. | None. Replace the v9 PDFs in `FINALIZED/` when convenient. |
| S6 | Kickoff inject wording, and who "fires first" | `whitecell-injects.md` §1 |
| S7 | Balance check: 15 REDFOR counters in theater plus 7 at home vs. 21 BLUEFOR counters plus advantages S-B3 to S-B5 | Needs a POC run-through |
| S8 | The intelligence products (RI-01 to RI-15, BI-01 to BI-15) and their key: whether the hints at hidden assets and objectives are too strong or too weak | As drafted in `handouts/` |
