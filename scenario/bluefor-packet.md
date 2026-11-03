# Operation Zugzwang — BLUEFOR Packet (Omak)

**Audience:** the BLUEFOR team and the white cell. **Never give this file to REDFOR.**
**Owner:** C/Nacanaynay · **Version:** 0.3 (20 Oct 2026) · Read `scenario/00-overview.md` first.

This packet holds your forces (including hidden ones the enemy doesn't know about), your outside-support options, your intelligence estimate, and your three secret objectives. Status tags work as defined in `RULES.md` §0. All numbers are **[PROPOSED]** unless tagged. That every asset is a U.S. system and that BLUEFOR can receive Asotin support are **[CANON]**.

---

## 1. Forces — Omak (NDF + PFA)

### 1.1 Conventions

- **Counter states:** Ready · Degraded (−1 when used) · Destroyed (removed).
- **Visibility:** *Visible* counters start on the central map. *Hidden* counters stay on your sheet until you use them or the enemy finds them (`RULES.md` §4.4).
- Capability notes are unclassified, approximate, and simplified for play.
- The NDF bought its U.S.-type equipment from Cosmopolis under the old treaty. Asotin-supplied items are also modeled as U.S. systems (a game convention).
- Your force is smaller and lower-end than REDFOR's. Your strength comes from starting conditions S-B3 (Home Ground), S-B4 (Asotin's Backing), and S-B5 (Supportive Population). See `scenario/00-overview.md` §5.2.

### 1.2 In place at start: 21 counters

| ID | Asset | Owner | Zone | Vis. | What it does | Key limitations (Con fodder) |
| --- | --- | --- | --- | --- | --- | --- |
| B-01 | **F-16C/D Fighting Falcon** squadron 1 (~12) | NDF | Z11 Omak City (Capital) | Visible | Multirole air defense and strike. Can also lay Quickstrike mines (B-11). | Outclassed by the F-22 and F-35, and by AWACS-supported forces. One main base makes it vulnerable. |
| B-02 | **F-16C/D Fighting Falcon** squadron 2 (~12) | NDF | Z11 | Visible | Same as B-01 | Same |
| B-03 | **F-15C Eagle** squadron (~12, older) | NDF | Z12 Interior | Visible | Air-superiority interceptor | Aging airframes. Spare parts came from Cosmopolis and are now cut off. |
| B-04 | **Patriot battalion PAT-1** (PAC-2) | NDF | Z10 Coast (covers the Narrows) | Visible | Denies the air over the Strait to non-stealthy aircraft. Can engage missiles. | Mobile but slow to relocate. Its radar emits when active, which the RC-135 can find. |
| B-05 | **Patriot battalion PAT-2** (PAC-2) | NDF | Z11 Omak City (Capital) | Visible | Protects Omak City and the main air base | Same |
| B-06 | **NASAMS** batteries (×3) plus **Stinger** teams | NDF | any Omak zone | **Hidden** | Pop-up threats that ambush low or slow aircraft (A-10, MQ-9, C-130J, helicopters) | Short to medium range |
| B-07 | **AN/FPS-117 early-warning radar** network | NDF | Z10–Z12 | Visible | Long-range detection and cueing for Patriot and fighters | Fixed sites. Can be jammed (EC-37B) and struck. |
| B-08 | **Harpoon Coastal Defense** battery CB-1 (~75 mi) | NDF | Z10 (west Narrows) | Visible | Holds shipping and warships in the Strait at risk | Needs targeting data from radar, drones, or the militia |
| B-09 | **Harpoon Coastal Defense** battery CB-2 | NDF | Z10 (east Narrows) | **Hidden** | Same | Same |
| B-10 | **HIMARS** battalion with **PrSM** (~500 km), Asotin-supplied missiles (Army system) | NDF | Z12 Interior | **Hidden** | **Can reach Camas.** Strikes bases, ports, and ships at anchor. Shoot-and-scoot. | Limited missiles (2–3 salvos per game). Launches are seen by Cosmopolis missile-warning satellites. Patriot on Camas can intercept. |
| B-11 | **Quickstrike naval mine** stockpile | NDF | Z10 | **Hidden** | Mines the Narrows. Can be dropped by F-16s or laid by boats. | REDFOR can clear mines, given time. Mining an international strait costs International Opinion. |
| B-12 | **Mark VI patrol boat** flotilla (~8) | NDF | Z10 / Z8 | Visible | Strait patrol, escort, interception, minelaying | Very vulnerable to A-10s, P-8s, and helicopters once found |
| B-13 | 1st Armored Brigade: **M1A1 Abrams, M2 Bradley** (Army) | NDF | Z11 | Visible | Defends Omak City (the capital) | Vulnerable to air attack in the open |
| B-14 | 2nd Armored Brigade: **M1A1, M2** (Army) | NDF | Z10 | Visible | Defends the coast and Fortune Harbor | Same |
| B-15 | Coastal Defense Brigade: **M777** howitzers, **Javelin** teams (Army) | NDF | Z10 | Visible | Anti-landing defense | Static |
| B-16 | Drone squadron: **MQ-9A Reaper** (~6) + **Switchblade 600** loitering munitions | NDF + PFA | Z12 | Visible | ISR for targeting (cues B-08 and B-10). Cheap precision strikes. | Easily shot down by fighters and Patriot |
| B-17 | **C-130H Hercules** airlift detachment | NDF | Z11 | Visible | Moves troops and supplies inside Omak. Receives airlifted Asotin supplies. | Vulnerable once REDFOR has air superiority |
| B-18 | **PFA maritime militia** (~40 armed civilian boats) | PFA | Z10 / Z8 | Visible | Harassment, minelaying, swarming, scouting. Blends in with civilian traffic. | Light weapons. Low training. Political cost if civilians are hit. |
| B-19 | **PFA militia brigades** (×3, ~15,000 fighters, with M4s, Javelins, and Stingers from NDF depots) | PFA | Z10–Z12 | Visible | Urban and rural defense. Makes ground incursions very costly (S-B3). Internal security. | Poor discipline. Abuses create backlash. |
| B-20 | **PFA Information Directorate** (state media and social media) | PFA | Z11 | Visible | Propaganda. Exploits the meddling scandal (moves International Opinion and Domestic Will). | Credibility drops if caught lying |
| B-21 | PFA "hacktivist" cyber cell | PFA | — | **Hidden** | Nuisance attacks, leaks, disruption of Camas and Cosmopolis civilian networks | Low sophistication. Attribution invites escalation. |

### 1.3 RFF pool: national mobilization

| ID | Asset | Arrives | Approval notes |
| --- | --- | --- | --- |
| B-30 | NDF reserve mobilization: 2 infantry brigades | N+1 | Routine. Costs Omak economically (the white cell may move Regime Stability −1 if it is repeated). |
| B-31 | PFA volunteer surge (militia +1 brigade) | N+1 | Routine, thanks to the supportive population. Can worsen S-B1 friction (white cell judgment). |
| B-32 | Requisitioned civilian shipping and ferries | N+1 | Logistics, decoys, minelaying platforms |

### 1.4 RFF pool: Asotin support (S-B4)

| ID | Asset | Arrives | Approval notes |
| --- | --- | --- | --- |
| B-40 | **Arms shipment**: Stinger, Javelin, Harpoon reloads, PAC-2 interceptors, F-16 spare parts | N+2 | **Routine.** Arrives via the West Approach or by air. REDFOR can try to interdict it with a COA. |
| B-41 | **Intel sharing**: satellite imagery and signals intelligence | N+1 | **Routine.** Your RFIs about Camas and naval movements get fuller answers. |
| B-42 | **Patriot PAC-3 battery with Asotin "volunteer" crews** | N+3 | International Opinion ≤ −1 **or** a REDFOR strike on an Asotin shipment. Escalation: Cosmopolis Domestic Will reacts. |
| B-43 | **Asotin "volunteer" F-16 Block 70 squadron** | N+3 | International Opinion ≤ −2. Major escalation. The white cell may inject a Cosmopolis–Asotin crisis. |

---

## 2. Intelligence estimate (what Omak believes)

*The estimate may be incomplete or wrong. Use RFIs and ISR COAs to confirm. All visible REDFOR counters are on the central map.*

- **Cosmopolis bombers:** Cosmopolis can strike from home with B-52s and B-1s.
- **Cosmopolis special forces and cyber:** unknown.
- **Ground invasion:** Cosmopolis is likely planning a ground invasion within days.
- **Latah:** is Cosmopolis's ally and will host its bombers.
- **Asotin:** has promised arms, intel, and "whatever is needed."
- **Sapphire loyalists:** a few disloyal officers may remain in the NDF.

---

## 3. Secret objectives [CANON: 3 objectives, defensive; wording PROPOSED]

The white cell scores these at the end of the game (`RULES.md` §9.3).

| # | Objective | Achieved | Partial | Not achieved |
| --- | --- | --- | --- | --- |
| B1 | **"Survive!"** | The Indigo/PFA government holds Omak City (the capital) and Regime Stability ≥ 2 | The government survives but Stability ≤ 1, or it is forced into a power-sharing deal | The government has fallen |
| B2 | **"Keep the Strait ours!"** | Omak controls its southern shore, no Cosmopolis ground forces are on Omak soil, **and** any Strait arrangement recognizes Omak's sovereignty | Cosmopolis holds only a limited coastal foothold, **or** the Strait reopens on Cosmopolis's terms without Omak's agreement | Cosmopolis controls Omak's Strait coast |
| B3 | **"Win the world's sympathy!"** *(long-term)* | International Opinion ≤ −2, **or** the government is formally recognized by at least two states besides Asotin | International Opinion −1 or 0 | International Opinion ≥ +1 |
