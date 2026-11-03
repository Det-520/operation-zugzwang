---
title: "Operation Zugzwang — White Cell Handbook"
subtitle: "Procedures and adjudication for lead adjudicators and loggers · AFROTC LLAB 12 · 12 November 2026"
short: "White Cell Handbook"
---

**WHITE CELL ONLY.** This handbook and the other white cell documents hold both sides' secrets, the injects, and the ground truth. **Never leave them where players can see them.**

*Fictional training scenario. All military systems are real U.S. systems, described with unclassified, approximate capabilities.*

<!-- pagebreak -->

## 0. What's Going On?

We are running a matrix wargame where GMC will play opposing teams (BLUEFOR and REDFOR) in a conflict and POC will be adjudicating (the white cell). Each turn, teams present their COAs, give pro arguments for why it would be successful and then give cons for the opposing team's COA. The white cell will then evaluate the arguments which become modifiers to a roll which determines if the COA was successful. White cell then delivers the outcomes accordingly.

<!-- pagebreak -->

## 1. POC Roles

The white cell is the neutral referee. It runs the clock, judges the arguments, rolls the dice, narrates the results, introduces fog and friction, and keeps the game on the rails. Each of the groups plays its own game at its own table, so each table has its own white cell consisting of at least three POC.

| Role | Job |
| --- | --- |
| **Lead adjudicator** | Runs the **timer program** and the **dice program**. Calls each step. Gives injects. Rules on every COA and RFF. **Final authority.** |
| **BLUEFOR logger** | Hears BLUEFOR's Phase I brief and Phase III FRAGO. Keeps the BLUEFOR placement form (White Cell Forms §4.2): planned COAs, hidden-counter locations, arrivals, and counters that changed. Moves BLUEFOR counters. Doesn't log every move. |
| **REDFOR logger** | Same for REDFOR (White Cell Forms §4.1) |

The white cell should work to be efficient and generally help teams stay within the bounds of the rules. As white cell, you are given lots of freedom:

- You make up the outcomes of a COA
- You can add injects as you please
- You determine which RFIs and RFFs are allowed (there is some guidance on how to respond)

Generally, you should be helpful in ensuring that teams understand the rules and ask clarifying questions. While the complexity of the rules may seem daunting, also know that it is the responsibility of teams to advocate for themselves: to point out the assets they have, argue the success and effects of a COA, remind white cell of triggers that are to their advantage, etc.

<!-- pagebreak -->

## 2. Before the game

### 2.1 Distribution

| Who | Gets |
| --- | --- |
| **Every player** | Player Rules Handbook · Scenario Brief · Scenario Schedule · Starting Conditions · Player Forms |
| **REDFOR players** | + REDFOR Commander's Read-Ahead · REDFOR Team Packet · REDFOR Order of Battle · REDFOR Intelligence Products |
| **BLUEFOR players** | + BLUEFOR Commander's Read-Ahead · BLUEFOR Team Packet · BLUEFOR Order of Battle · BLUEFOR Intelligence Products |
| **White cell** | Everything |

**Nobody on a team gets the other team's documents.** Teams and flight commanders should be assigned before distribution.

#### Distribution schedule

- **ASAP:** general rules information (Player Rules Handbook, Player Forms)
- **One week prior (over Canvas):** scenario information (Scenario Brief, Scenario Schedule, Starting Conditions, map)
- **24 hours prior (over email):** team assignments and team information

### 2.2 Prep checklist (before the LLAB)

The White Cell Checklist has the full list, from a week out to cleanup, in order.

- [ ] Everyone in the white cell has read **both** sides' intelligence products and the key (Intelligence and Injects §3), so you recognize a Pro built on a false report.
- [ ] The timer program and dice program work on the lead adjudicator's device. It should be shown on screen for all players to see.
- [ ] Printed: one **Print Packet** per table (`White Cell/Print Packet - One Table.pdf`). Its cover lists what is in it: the White Cell Checklist, White Cell Forms (score sheet, track board and markers, objective status card, both placement forms), starting-condition cue cards, counters, the map in letter tiles, both teams' player forms and request slips, and spare forms and slips at the back. Print the game pieces (counters, map, cue cards, track board) in colour and the rest in greyscale. For one large map, print `map-full.pdf` on a plotter (v10 or later, with Camas inside PrSM range).
- [ ] Counters printed and cut out: one set per table. It shows **both** sides' hidden assets, so keep it with the white cell. The HIDDEN counters stay in an envelope until they go on the map (§2.3).

### 2.3 Table setup

**Tracks** (beside the map)

| Track | Start position |
| --- | --- |
| Strait Traffic | **Open**. It moves to **Restricted** when you read the kickoff inject. |
| International Opinion | **−1** |
| Cosmopolis Domestic Will | **3** |
| Omak Regime Stability | **4** |

**Objective status card** (White Cell Forms §3): blank, **face down with the logger**. Each logger also keeps its side's **placement form** (§4) face down. Never put it beside the tracks, because it shows what the secret objectives look for.

**Starting-condition cue cards** (face up, visible to both teams): S-R1 to S-R4, S-B1 to S-B5.

#### Counters on the central map (visible only)

| Zone | REDFOR | BLUEFOR |
| --- | --- | --- |
| Z1 Cosmopolis (off-map box) | R-16, R-17, R-19, R-20 | |
| Z6 Camas | R-01 to R-14 | |
| Z9 East Approach | R-15 | |
| Z8 Narrows / Z10 Coast | | B-12, B-18 (patrol and militia boats) |
| Z10 Omak Coast | | B-04 (PAT-1), B-08 (CB-1), B-14, B-15 |
| Z11 Omak City (Capital) | | B-01, B-02, B-05 (PAT-2), B-13, B-17, B-20 |
| Z12 Omak Interior | | B-03, B-16 |
| Z10–Z12 (spread) | | B-07 (radar network), B-19 (militia brigades) |

**Hidden counters stay off the map**, on the owning team's sheet and on the Master Asset List:

| Side | Hidden counter | Where |
| --- | --- | --- |
| REDFOR | R-18 B-2A Spirit | Z1 Cosmopolis |
| REDFOR | R-21 Cyber mission teams | Z1 (acts remotely) |
| REDFOR | R-22 AFSOC MC-130J + Special Tactics | Z1 |
| BLUEFOR | B-06 NASAMS ×3 + Stingers | **BLUEFOR chooses the zones in Phase I. The logger marks them on the placement form.** |
| BLUEFOR | B-09 Harpoon CB-2 | Z10, east Narrows |
| BLUEFOR | B-10 HIMARS with PrSM | Z12 Interior |
| BLUEFOR | B-11 Quickstrike mines | Z10 |
| BLUEFOR | B-21 PFA hacktivist cyber cell | No zone (acts remotely) |

A hidden counter goes on the map under three conditions:

- **Found** by a successful ISR COA
- **Used** by its owner
  - If a team mentions a hidden asset in a COA or argument, it is revealed, whether or not the COA had its intended effect.
- **Disclosed** by an inject (e.g. I-06)

<!-- pagebreak -->

## 3. Master schedule of phases

| Clock | Min | Phase / Block | White cell actions |
| --- | --- | --- | --- |
| **1345–1403** | **18** | **Phase I – Planning** | |
| 1345–1357 | 12 | • Team planning & requests | Read the Phase I opening script. Start the 18-minute timer. Teams organize and plan using their pre-read intelligence products. |
| **1357** | — | • **Phase I request cutoff (min 12)** | **Collect up to 4 requests (RFIs/RFFs combined) per team.** Lead adjudicator writes answers and rulings during the next 6 minutes while teams rehearse and brief. |
| 1357–1400 | 3 | • Brief rehearsal | Teams finalize their five-paragraph OPORD brief. Lead adjudicator finishes answering Phase I requests. |
| 1400–1403 | 3 | • Phase I OPORD briefs (last 3 min) | Each logger hears its own team's oral five-paragraph OPORD brief and writes its **planned COAs** (up to 3, Turns 1–3) and, for BLUEFOR, the **B-06 NASAMS zones** on the placement form (White Cell Forms §4). |
| **1403–1405** | **2** | **Kickoff inject** | Read the kickoff inject (Intelligence and Injects §4.1). Move Strait Traffic to **Restricted**. Hand back Phase I RFI answers and RFF rulings. |
| **1405–1505** | **60** | **Phase II: Turns 1–4** | Run four 15-minute turns (§4): · **Turn 1:** 1405–1420 · **Turn 2:** 1420–1435 · **Turn 3:** 1435–1450 · **Turn 4:** 1450–1505 *(S-R1 bites on Camas strikes unless resupplied)* |
| **1505–1512** | **7** | **Debrief 1** | Phase I–II flight commanders lead it. Hand command to the **Phase III–IV flight commanders** afterward. |
| **1512–1520** | **8** | **Phase III: Planning and FRAGO** | **1512–1519 (7 min):** Phase IV planning under the new flight commander. · **1519–1520 (last 1 min):** Each logger hears the new flight commander's **1-minute oral FRAGO** and writes **up to 2 new planned COAs for Phase IV (Turns 5–7)** on the placement form. |
| **1520–1605** | **45** | **Phase IV: Turns 5–7** | Run three 15-minute turns (§4): · **Turn 5:** 1520–1535 · **Turn 6:** 1535–1550 · **Turn 7:** 1550–1605 |
| **1605–1612** | **7** | **End of game & Debrief 2** | State the end state and score objectives (§8). Phase III–IV flight commanders lead Debrief 2. |

### 3.1 Scripts

Read these aloud, word for word or close to it.

#### Phase I opening (1345)

> "Welcome to Operation Zugzwang. Your intelligence suggests that an attack is imminent. You have 18 minutes to organize your team, synthesize your intelligence, and build a plan. You may submit up to four requests, RFIs or RFFs, due at minute 12—six minutes before the end of the phase. In the last three minutes you will brief your plan to your logger as a five-paragraph order, including up to three planned COAs. There are no COAs in Phase I. Your time starts now."

#### Phase I minute 12 call (1357)

> "Six minutes left in Phase I. Hand in your Phase I request slips now—up to four per team. You have three minutes to rehearse before you brief your logger."

#### Turn start

> "Turn [N]. Prepare, five minutes. Your RFI answers are on the table. Requests are due when the timer ends."

#### Phase III Planning and FRAGO call (1519)

> "One minute left in Phase III. Phase III–IV flight commanders, brief your one-minute FRAGO and up to two Phase IV planned COAs to your logger now."

#### End of game (1605)

> "That was the final turn. Here is where things stand." Then read the tracks and key map facts, and score (§8).

## 4. Running a turn

### 4.1 Turn steps and timing checklist (15:00 per turn)

| Step | Turn Clock | Duration | Lead adjudicator says or does |
| --- | --- | --- | --- |
| **Prepare** | 0:00–5:00 | 5:00 | Start the timer. Hand out last turn's RFI answers. Authorize parleys (≤ 2 min) on request. |
| Collect slips | 5:00 | — | Up to **3** requests per team. Refuse any extra. |
| **BLUEFOR COA** | 5:00–7:00 | 2:00 | "BLUEFOR, your COA." No interruptions. |
| **REDFOR COA** | 7:00–9:00 | 2:00 | "REDFOR, your COA." |
| Prepare Cons | 9:00–11:00 | 2:00 | "Two minutes to prepare Cons." Note the Pros you'll accept while they huddle. |
| **REDFOR Cons** | 11:00–12:00 | 1:00 | "REDFOR, your Cons on BLUEFOR's COA." |
| **BLUEFOR Cons** | 12:00–13:00 | 1:00 | "BLUEFOR, your Cons on REDFOR's COA." |
| **Resolve** | 13:00–15:00 | 2:00 | Resolve both COAs simultaneously (§5). Rule on RFFs and announce arrivals. State ongoing effects. Deliver an inject (optional, at most one). Loggers move counters and tracks and update the placement forms. |

**End-of-turn track checks** (do these every turn, in step 8)

- [ ] Strait Traffic **Closed** → Domestic Will **−1**.
- [ ] Any track at a trigger value? Apply it (§6.2).
- [ ] Turn 4 or later and Camas not resupplied → S-R1's −1 applies to Camas-based strikes.
- [ ] Any RFF arriving this turn → place its counter. It acts next turn.
- [ ] Any secret COA trigger met → resolve it now.

### 4.2 Keeping order

- **It's a courtroom.** Players speak only in their slot. Accept only points of fact or procedure. "You had your slot" ends most disputes.
- **Late objections** (after the slot, or after the roll) **are not considered**. Results are never re-run.
- **Laundry lists.** Count only the first three reasons and only one action. If a COA tries to do two unrelated things, tell the briefer to pick one, or pick the first.
- **Behind schedule?** Shorten **Prepare** (to 4:00, then 3:00). **Never cut the Cons.**
- **Players out of bounds?** Kill the COA outright, or deliver I-13, a bounding directive.
- **Simultaneous execution and REDFOR reacting to BLUEFOR.** Both COAs take place simultaneously across the 3-day turn window. REDFOR, briefing second, may react to BLUEFOR's COA, which is realistic. However, REDFOR **may not simply negate** BLUEFOR's COA ("their strike doesn't happen") or prevent BLUEFOR's roll. Negating is what Cons are for; a counter-move is resolved as an **Interacting** or **Directly Opposed** COA (§5.3).

<!-- pagebreak -->

## 5. Adjudication

### 5.1 Procedure for each COA

1. **Check feasibility:** time (3 days), space, and assets the team actually has. If it fails, rule it **impossible** (no roll) or **scope it down**. Say so in one sentence.
2. **Auto-success?** No credible Cons, or an overwhelming case → **Success** without a roll.
3. **Count modifiers:** Cap the net at **±4**.
4. **Roll 2d6** in the dice program, add the modifiers, and read the band.
5. **Narrate** in one or two sentences. It may also be helpful to name the deciding Pro or Con.
6. Successful results become **established facts**.

#### Argument to Modifier Reference

| Modifier | Value |
| --- | --- |
| Each **strong** accepted Pro | +1 (one exceptionally compelling Pro may be +2) |
| Each **strong** accepted Con | −1 (one exceptionally compelling Con may be −2) |
| Weak, vague, or duplicate reason | 0 |
| **Planned** COA, executed as briefed in Phase I or Phase III FRAGO and still valid (check the placement form) | +1 |
| Each starting condition or ongoing effect that applies (§6) | ±1 |
| An asset in the COA is **Degraded** | −1 |

#### Outcome Reference

| Total | Result | Typical outcome |
| --- | --- | --- |
| **≤ 3** | **Critical failure** | Fails, and something goes wrong: losses, exposure (a hidden counter revealed), backlash, a track moves against the actor |
| **4–6** | **Failure** | No meaningful effect. A risky combat action may leave its assets **Degraded**. |
| **7–8** | **Partial success** | Happens, but limited or at a cost: the target is **Degraded** instead of Destroyed, or there are own losses or a political cost |
| **9–11** | **Success** | Happens as argued |
| **≥ 12** | **Exceptional success** | As argued, plus a bonus: an extra effect, a new established fact, or a track moves in the actor's favor |

#### Probability Card

| Net modifier | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Natural roll needed | 11+ | 10+ | 9+ | 8+ | 7+ | 6+ | 5+ | 4+ | 3+ |
| Chance of at least Partial | 8% | 17% | 28% | 42% | 58% | 72% | 83% | 92% | 97% |

### 5.2 Judging a reason in seconds

Ask four questions. **Four yeses = strong (±1).** Decisive on its own = ±2. Anything else = 0.

1. **Is it true?** An established fact, a listed capability or limitation, or a reasonable assumption.
2. **Is it relevant** to *this* action and *this* effect?
3. **Is it new,** not a restatement of a reason already counted?
4. **Does it matter?** Would a real commander care?

#### Common calls

| Situation | Call |
| --- | --- |
| A Pro about the *effect* ("closing the Strait hurts their economy") | 0 toward success. It explains why the COA matters, not why it works. |
| A Con about *consequences* ("civilian casualties will cause outrage") | 0 toward success, but **shape the outcome** with it: side effects and track moves |
| A Con that a Pro already answered, or vice versa | They cancel. Count neither. |
| A reason that names doctrine but doesn't explain how it applies | 0 |
| A reason built on something that happened earlier in the game | Usually strong. Reward building on the story. |
| A reason built on an **intelligence product** | Check the key (Intelligence and Injects §3). A **true** report can be strong, and stronger if the team confirmed it. A **false or misleading** report counts 0, and acting on it can make the COA fail in an instructive way. |
| A Pro relying on a hidden asset's capability the briefer hasn't revealed | The COA uses the asset, so it is revealed. Place the counter. |
| A Con relying on information the team shouldn't have | 0. Teams argue from their own intel. |
| An interaction nobody mentioned (BLUEFOR dispersed the SAMs REDFOR struck) | Fold it into the modifiers anyway. A well-timed counter-move is a strong Pro or Con even if unspoken. |

### 5.3 Interacting COAs (simultaneous execution)

Both COAs happen simultaneously across the 3-day turn window. Because REDFOR briefs second, REDFOR's COA cannot preempt BLUEFOR from rolling; instead, resolve interactions using one of these three cases:

- **Independent** (different places or effects): resolve each normally, BLUEFOR's first.
- **Interacting** (one affects the other's odds): fold the interaction into the modifiers.
- **Directly opposed** (both can't succeed): **opposed roll**. Roll 2d6 for each side, each adds its own modifiers, and the higher total wins. A tie means both are **Partial**, the situation stays contested, and you describe a stalemate.

### 5.4 Special COA types

| Type | Handling |
| --- | --- |
| **Big project** (coalition, ACE network) | State up front how many successful COAs it needs, **at most 3**. ACE dispersal off Camas (S-R2) is 2. Track progress on the track board (White Cell Forms §2). |
| **Protected or hidden target** | At most 3 layers, e.g. *find* (ISR COA), then *strike*. A strike on a hidden counter nobody has found is impossible, or becomes an ISR COA. An intel product that points at a hidden asset is a good Pro for the *find* COA, not a substitute for it. |
| **Long-term COA** | Success means the effect **has started and continues** until someone stops it. Record it as an ongoing effect. |
| **Announcement** | Free, unless it claims a measurable effect. Then it is the team's COA. |
| **Secret COA** | One per team per phase. Keep the slip. Resolve when the trigger occurs, using your own judgment in place of Cons. **A loose trigger doesn't fire.** |
| **Arguing a player-controlled actor agrees** | Not allowed. Tell the team to ask in person (a parley). |
| **Persuading a white-cell actor** (Latah, Tekoa, Asotin, the press) | A normal COA. Use the ground truth (Intelligence and Injects §1) for how those actors really feel. |

### 5.5 Contentious calls

If both teams keep arguing, don't debate. Either **make the call**, or take a **10-second estimative vote**: each white cell member shows fingers, you take the **median**, and roll against it.

#### Estimative Vote Card

| Fingers | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| Meaning | Remote | Unlikely | Even chance | Likely | Almost certain |
| Roll needed on 2d6 | 11+ | 9+ | ≈ 50% (use the program's percentage roll) | 6+ | 4+ |

<!-- pagebreak -->

## 6. Starting conditions, tracks, and ongoing effects

### 6.1 Starting conditions: when to apply them

| ID | Name | Apply when | Effect | Removed by |
| --- | --- | --- | --- | --- |
| S-R1 | The 8,000-Mile Tail | A Camas-based strike COA on **Turn 4 or later** without resupply | −1 | A resupply COA, or R-33 arriving |
| S-R2 | Single Hub | A BLUEFOR strike on Camas succeeds | Affects **every** counter on Camas (can Degrade several) | ACE dispersal: 2 successful COAs |
| S-R3 | Latah Hesitates | REDFOR tries combat sorties from Latah | Not allowed | A diplomatic COA, or Opinion +3 |
| S-R4 | Legitimacy Deficit | A REDFOR COA relies on third-party cooperation while Opinion ≤ −1 | −1 | Opinion ≥ 0 |
| S-B1 | A House Divided | A BLUEFOR COA needs NDF **and** PFA forces together (check the owner column in the Master Asset List) | −1 | A "unified command" COA, or Stability 5 |
| S-B2 | Sapphire Loyalists | REDFOR argues defections or sabotage | Allowed, at −1 (S-B5) | A BLUEFOR counterintelligence COA removes the option |
| S-B3 | Home Ground | A BLUEFOR **defensive** COA in Z10–Z12 (defend, disperse, hide, repair, ambush) | +1 | Permanent |
| S-B4 | Asotin's Backing | BLUEFOR requests B-40 or B-41 | Routinely approved | Permanent |
| S-B5 | Supportive Population | A REDFOR COA relies on Omak civilians (SOF in Omak, loyalist uprisings, info ops aimed at Omak's public) | −1. Also: BLUEFOR RFIs about REDFOR activity inside Omak get full answers. | Stability ≤ 2 |

### 6.2 Track triggers

| Track | Trigger | What happens |
| --- | --- | --- |
| Strait Traffic | **Closed** at end of a turn | Domestic Will −1 (every turn it stays Closed) |
| International Opinion | **+3** | Latah grants full combat basing automatically (S-R3 removed) |
| International Opinion | **−3** | Asotin escalates its support. Consider unlocking B-42 or B-43 early, or I-07. |
| Domestic Will | **≥ 4** | Big REDFOR RFFs approved more readily (R-36 to R-39) |
| Domestic Will | **0** | Cosmopolis's legislature orders a ceasefire and negotiations |
| Regime Stability | **5** | S-B1 removed ("national unity") |
| Regime Stability | **≤ 2** | S-B5's −1 no longer applies |
| Regime Stability | **0** | The government collapses, and the NDF takes over as caretaker |

**Fixed track moves** from the rules of engagement:

| Event | Move |
| --- | --- |
| A COA result causes significant civilian casualties (REDFOR) | Opinion −1 **and** Domestic Will −1 |
| BLUEFOR strikes civilian targets on Camas or in Latah | Opinion +1 |
| BLUEFOR strikes Latah at all | Latah enters the war |
| BLUEFOR attacks neutral shipping | Opinion +1 |

### 6.3 Ongoing effects

At the end of each resolve step, state any **ongoing effects** in one line ("refugees on the coast road," "Fortune Harbor burning," "mines in the Narrows"). Each gives ±1 to related COAs **until a successful COA removes it**. Write them on the track board (White Cell Forms §2) so all players can see them.

<!-- pagebreak -->

## 7. Ruling on RFFs

Rule on RFFs during step 8 and tell the team the **arrival turn**. "N" is the turn of approval. Phase I RFFs count from Turn 1. Arriving forces **act the turn after** they arrive.

### REDFOR

| ID | Asset | Arrives | Approve when |
| --- | --- | --- | --- |
| R-30 | Additional F-35A squadron | N+1 | There is basing room. Camas is crowded without ACE, so consider a partial approval. |
| R-31 | Additional KC-46A | N+1 | Routine |
| R-32 | ACE package (RED HORSE, base kits) | N+1 | A host location exists (Latah, or Camas secondary fields) |
| R-33 | Sustainment package (lifts S-R1) | N+1 | Routine |
| R-34 | Mine countermeasures group (Navy) | N+2 | Routine |
| R-35 | Additional Patriot or THAAD (Army) | N+2 | Routine |
| R-36 | Carrier strike group (Navy) | N+2 | Domestic Will ≥ 3 |
| R-37 | Airborne infantry brigade (Army) | N+2 | Domestic Will ≥ 4, **or** a prior successful COA making the case for ground forces |
| R-38 | ARG/MEU (Marines) | N+3 | Same as R-37 |
| R-39 | Authorities (leadership strikes, engaging Asotin shipments) | N+0 | Political. Weigh Domestic Will and Opinion. Engaging Asotin risks unlocking B-42. |

### BLUEFOR

| ID | Asset | Arrives | Approve when |
| --- | --- | --- | --- |
| B-30 | NDF reserves: 2 infantry brigades | N+1 | Routine. If repeated, you may move Stability −1 (economic cost). |
| B-31 | PFA volunteer surge (+1 brigade) | N+1 | Routine. May worsen NDF–PFA friction. |
| B-32 | Requisitioned civilian shipping | N+1 | Routine |
| B-40 | Asotin arms shipment | N+2 | **Routine.** Arrives via the West Approach or by air. REDFOR may try to interdict it in transit. |
| B-41 | Asotin intel sharing | N+1 | **Routine.** Fuller RFI answers about Camas and naval movements from then on. |
| B-42 | Asotin PAC-3 battery, "volunteer" crews | N+3 | Opinion ≤ −1 **or** REDFOR has struck an Asotin shipment. Domestic Will reacts. |
| B-43 | Asotin "volunteer" F-16 Block 70 squadron | N+3 | Opinion ≤ −2. A major escalation. Consider a Cosmopolis–Asotin crisis inject. |

**Free-text RFFs** (not in a pool): judge them by realism, the timing table, and politics. A big request may need a successful COA first to build the case. **All assets must be U.S. systems.**

**Watch R3.** Opinion starts at −1, so B-42's condition is met from the start. If B-42 or B-43 arrives, REDFOR's objective R3 fails. That is a legitimate outcome, but make sure the conditions are really met when you approve.

## 8. End of game and scoring

After Turn 7's resolution:

1. **State the end state:** all four tracks, who controls Omak's coast, Cosmopolis ground forces on Omak soil (if any), Asotin personnel in Omak (if any), and any agreements reached.
2. **Score each objective** as Achieved, Partial, or Not achieved, using the tables below. Loggers record the results.

### REDFOR Objectives

| # | Objective | Achieved | Partial | Not achieved |
| --- | --- | --- | --- | --- |
| R1 | Open the Strait! | Strait Traffic Open | Restricted | Closed |
| R2 | Restore a friendly government in Omak! | Stability 0, **or** Omak agreed to new elections or the Sapphire president's return | Stability ≤ 1, **or** formal talks on Omak's government have begun | Stability ≥ 2 and no talks |
| R3 | Cut Asotin out! | No Asotin personnel or crewed units in Omak, **and** ≥ 1 Asotin shipment interdicted or turned back by diplomacy | No Asotin personnel or crewed units in Omak | Asotin personnel or crewed units in Omak, or an Asotin–Omak defense agreement |

### BLUEFOR Objectives

| # | Objective | Achieved | Partial | Not achieved |
| --- | --- | --- | --- | --- |
| B1 | Survive! | Government holds Omak City (the capital) and Stability ≥ 2 | Survives with Stability ≤ 1, or forced into power-sharing | Government has fallen |
| B2 | Keep the Strait ours! | Omak controls its southern shore, no Cosmopolis ground forces on Omak soil, **and** any Strait arrangement recognizes Omak's sovereignty | Limited Cosmopolis coastal foothold, **or** the Strait reopens on Cosmopolis's terms without Omak's agreement | Cosmopolis controls Omak's Strait coast |
| B3 | Win the world's sympathy! | Opinion ≤ −2, **or** formal recognition by ≥ 2 states besides Asotin | Opinion −1 or 0 | Opinion ≥ +1 |

### Scoring notes

- **R3:** "Asotin military personnel or crewed units in Omak" means **B-42 or B-43 has arrived**. B-40 arms and B-41 intel alone do **not** fail R3. Asotin transport aircrews who deliver cargo and leave (REDFOR product RI-12) don't count.
- **R1 and B2 can both be achieved.** A negotiated reopening of the Strait that recognizes Omak's sovereignty satisfies both. If the teams are talking, let them. That is the game working.
- **R2 vs. B1** are directly opposed through Regime Stability. Watch that track all game.
