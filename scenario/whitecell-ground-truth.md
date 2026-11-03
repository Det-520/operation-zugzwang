# Operation Zugzwang — White Cell: Ground Truth and Scoring Notes

**Audience:** ⚠️ **white cell only.**
**Owner:** C/Nacanaynay · **Version:** 0.3 (20 Oct 2026)

Each side's intelligence estimate (§2 of each packet) is deliberately **partly wrong**. This file records the truth so the white cell can answer RFIs consistently (`RULES.md` §4.4). It also explains how to score objectives that depend on information one side lacks.

---

## 1. Ground truth vs. what each side believes [PROPOSED]

| Topic | Truth | Where REDFOR's estimate is wrong | Where BLUEFOR's estimate is wrong |
| --- | --- | --- | --- |
| Omak air defenses | PAT-1 and PAT-2, plus **3 hidden NASAMS batteries and Stinger teams** (B-06) | Doesn't know the number or locations of the short-range systems | — |
| Omak coastal anti-ship missiles | **Two** Harpoon batteries: CB-1 (B-08, visible) and CB-2 (B-09, hidden, east Narrows) | Knows only CB-1 | — |
| Omak long-range strike | **B-10 exists.** HIMARS with Asotin-supplied PrSM, ~500 km. **Can reach Camas.** | Thinks it is unconfirmed (true, Cosmopolis never sold PrSM; Asotin supplied it) | — |
| Omak mines | A Quickstrike stockpile (B-11) | Underestimates it ("may have some") | — |
| Cosmopolis bombers | B-52H, B-1B, **and a hidden B-2A (R-18)** | — | Doesn't know about the B-2A |
| Cosmopolis special forces and cyber | Cyber teams (R-21) and AFSOC (R-22) exist, both hidden | — | Thinks they are "unknown" |
| Cosmopolis ground invasion | **Not imminent.** Ground forces need national approval that hasn't been given (R-37, R-38). | — | **Overestimates** the threat ("within days") |
| Latah | Logistics only (S-R3). No combat basing. | Slightly optimistic ("talks ongoing") | **Wrong**: thinks Latah will host bombers |
| Asotin | Arms (B-40) and intel (B-41) are routine. Personnel (B-42, B-43) come only under the conditions in the BLUEFOR packet §1.4. Asotin avoids direct war unless provoked. | Doesn't know the extent | **Overestimates** Asotin's commitment ("whatever is needed") |
| Sapphire loyalists | A small minority (S-B2) | **Overestimates** them ("significant sentiment") | — |

---

Each side's **intelligence products** (`handouts/redfor/intel/`, `handouts/bluefor/intel/`, one file per product) are raw reporting consistent with this table: some true, some misleading, some noise. Their key is in `handouts/whitecell/intel-and-injects.md` §3 **[PROPOSED]**.

## 2. Scoring notes [PROPOSED]

- **R3 "Cut Asotin out!":** "Asotin military personnel or Asotin-crewed units in Omak" means B-42 or B-43 has arrived. B-40 arms shipments and B-41 intel sharing alone do **not** fail R3.
- **R1 and B2 can both be achieved.** A negotiated reopening of the Strait that recognizes Omak's sovereignty satisfies both. Mouat's games work best when every actor can achieve something, and this gives the teams a reason to talk.
- **R2 vs. B1** are directly opposed through Regime Stability. Watch that track.
- Score at the end of the game (`RULES.md` §9.3), using the criteria tables in each packet's §3.

## 3. Objective status card [PROPOSED]

The four tracks (`scenario/00-overview.md` §5.1) and the map don't record everything the objectives check. The logger keeps an **objective status card** (`handouts/whitecell/forms.md` §2) for the rest and updates it in step 8 with the tracks, at no extra time cost. Changes go in the `track_changes` column of the log (`RULES.md` App. B).

**The card is white cell only.** It lists items that only the hidden objectives care about, so a card placed beside the public tracks would tell each team what the other is trying to do. Keep it with the logger, face down.

| Item | Records | Objectives |
| --- | --- | --- |
| Talks on Omak's government | None / formal talks begun / Omak agreed to new elections or the Sapphire president's return / Omak forced into power-sharing | R2, B1 |
| Strait arrangement | None / recognizes Omak's sovereignty / reopened on Cosmopolis's terms without Omak's agreement | B2 (R1 is scored on Strait Traffic) |
| Asotin shipments interdicted or turned back by diplomacy | Count, with turn | R3 |
| Asotin–Omak defense agreement signed | Yes / no, with turn | R3 |
| States recognizing Omak's government (besides Asotin) | Count, with names and turn | B3 |

Read the rest from the map at game end: who holds Omak City, who controls Omak's Strait coast, any Cosmopolis ground forces on Omak soil, and whether B-42 or B-43 has arrived.

A player agreement (`RULES.md` §6) changes the card only once both teams have confirmed it to the white cell. If they disagree about what they agreed, the negotiation log's "what each side thinks was agreed" column settles it.
