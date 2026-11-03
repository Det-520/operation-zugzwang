# Matrix Wargame Rules — Source of Truth

**Owner:** C/Nacanaynay
**Scenario this game runs:** Operation Zugzwang (see `scenario/README.md`)
**Event logistics** (schedule, rooms, groups, POC staffing): `LLAB-SETUP.md`
**Rules version:** 0.2 (draft, 20 Oct 2026)

This is the single authoritative rule set for the wargame: how a turn works, how moves are argued, and how they are adjudicated. If another document (team packet, slide, handout) disagrees with this one, this one wins, and the other document should be fixed.

Three parts, three jobs (full file map in `AGENTS.md`):

| Document | Holds |
| --- | --- |
| `RULES.md` (this one) | The matrix wargame mechanics: turn structure and timing, COAs, adjudication, requests, injects |
| `scenario/` | The world being played: actors, forces, map, starting conditions, objectives, injects, split by audience |
| `LLAB-SETUP.md` | The event that hosts the game: schedule, rooms, groups and teams, flight commanders, POC staffing, evaluation, materials |

---

## 0. How to read this document

### Status tags

| Tag | Meaning |
| --- | --- |
| **[CANON]** | Decided by the designer (C/Nacanaynay), either in the original planning notes or in `update-notes.txt`. Do not change without the designer's approval. |
| **[PROPOSED]** | A drafted rule that fills a gap. It is usable as written but has not been explicitly approved. |
| **[OPEN]** | A decision the designer still has to make (§11). |

A rule with no tag inherits the tag of its section heading.

### Document map

| Part | Who needs it |
| --- | --- |
| §1 Player Quick-Start | **Everyone.** This is all a GMC cadet must know to play. |
| §2–§7 Full rules | Players who want detail, plus the white cell |
| §8 White Cell Adjudication Guide | White cell |
| §9 Game roles | Everyone |
| §10 Worked example turn | Everyone (read it before the game) |
| §11 Open decisions | Designer |
| Appendices | Phase I brief format, placement form, probability table, doctrine crosswalk, glossary |

---

## 1. Player Quick-Start (read this if you read nothing else)

1. **What this is.** A *matrix wargame*: there is no rulebook of unit stats. You win arguments, not dice-math puzzles. Each turn your team proposes **one course of action (COA)** and gives **up to three reasons it will work**. The other team gives **up to three reasons it won't**. The **white cell** weighs the reasons, sets the odds, rolls the dice (with a computer program), and narrates what happens.
2. **Your side.** You are either **REDFOR** or **BLUEFOR**. Your team packet gives you your forces, your intel, and **three secret objectives**. Don't show the other team your objectives.
3. **One COA per turn.** A COA is *one* main action with a *measurable effect*, e.g. "F-35As and an EC-37B strike the PAT-1 Patriot site near the Narrows **so that** PAT-1 is destroyed and our ISR aircraft can operate over the Strait." You can use several assets in one COA (a strike package counts as one action), but you can't do two unrelated things. Everything else your forces do is background activity.
4. **Format of your COA (2 minutes):**
   > "Our COA: **[action]** in order to **[measurable effect]**. It will work because: **(1)** … **(2)** … **(3)** …"
5. **Format of your Cons (1 minute):**
   > "Their COA will fail or fall short because: **(1)** … **(2)** … **(3)** …"
6. **Good reasons** are specific and grounded in facts. They point to your assets' capabilities, the map, things that happened earlier in the game ("established facts"), and doctrine (tenets of airpower, principles of joint operations). Repeating a reason in new words earns nothing.
7. **Odds.** With no strong reasons either way, a COA succeeds on 7+ on two dice (58%). Each strong reason for it adds +1, and each strong reason against it subtracts 1. If a COA is obviously sound and unopposed, it succeeds without a roll.
8. **RFIs and RFFs.** Each turn you may hand the white cell **up to 3 written requests in total**, any mix of:
   - **RFI (Request for Information):** a question about the situation.
   - **RFF (Request for Forces):** a request for more assets or authorities from your national command. Reinforcements take time to arrive.
   Requests don't count as your COA, and there is no debate on them.
9. **Turn clock (15 min, run by a timer program):** prepare 5 → BLUEFOR COA 2 → REDFOR COA 2 → prepare Cons 2 → REDFOR Cons 1 → BLUEFOR Cons 1 → white cell resolves 2. BLUEFOR always goes first.
10. **No interrupting.** It's a courtroom, not a debate. You speak in your slot and are silent in theirs. Raise only points of fact or procedure. **If you miss your slot, the point is lost.** There are no do-overs.
11. **Arguing about the other side is allowed.** You can argue *their* troops are tired or *their* radar has a gap. You cannot argue that a player-controlled actor *agrees* to something. Ask them in person instead.
12. **The point** is good decisions and good reasoning under pressure: plan, communicate, brief, defend your choices, and adapt.

---

## 2. Game structure

### 2.1 Phases [CANON]

| Phase | Turns | What happens |
| --- | --- | --- |
| **Phase I – Planning** | none | Teams study intel, plan, and file up to 4 RFIs and RFFs (due at minute 12). They end by briefing their plan to their logger (§2.3). **No COAs.** |
| **Kickoff inject** | — | The lead adjudicator announces the war has begun (`scenario/whitecell-injects.md` §1). |
| **Phase II** | Turns 1–4 | Full turns (§2.2) |
| **Phase III – Planning & FRAGO** | none | After Debrief 1, the Phase III–IV flight commander takes command. Teams plan and end with a 1-minute FRAGO brief to the logger (§2.4). **No COAs.** |
| **Phase IV** | Turns 5–7 | Full turns (§2.2) |

- **[CANON] Game time:** each turn represents **about 3 days** of in-game time, so 7 turns cover about 3 weeks of conflict. Phase I covers the final days of crisis before the shooting starts. The white cell keeps timelines realistic. Moving forces 8,000 miles takes turns, not minutes (`scenario/00-overview.md` §6).
- Real-world clock times and the debriefs between phases are in `LLAB-SETUP.md`.

### 2.2 The turn [CANON]

One turn is "a turn in the chess sense": each side acts once, and **both COAs take place simultaneously across the 3-day turn window**. **Target: 15 minutes**, kept by a **timer program** the lead adjudicator runs.

| # | Step | Time | Who | Notes |
| --- | --- | --- | --- | --- |
| 1 | Prepare | 5 min | Both teams | Choose this turn's COA, write RFIs and RFFs, negotiate (§6). The white cell hands back answers to last turn's RFIs at the start of this step. |
| 2 | Submit RFIs/RFFs | — | Both teams → white cell | Written slips, handed over at the end of Prepare. No debate. |
| 3 | BLUEFOR COA + Pros | 2 min | BLUEFOR briefer | Format in §3.2 |
| 4 | REDFOR COA + Pros | 2 min | REDFOR briefer | |
| 5 | Prepare Cons | 2 min | Both teams | |
| 6 | REDFOR Cons → BLUEFOR COA | 1 min | REDFOR | |
| 7 | BLUEFOR Cons → REDFOR COA | 1 min | BLUEFOR | |
| 8 | White cell resolves | 2 min | White cell | Adjudicate both COAs (§4). Rule on RFFs. Update the map and tracks. Possibly deliver an inject. |

- **[CANON] Fixed order.** BLUEFOR always briefs first and REDFOR second, every turn. The order never switches.
- **[CANON] Simultaneous execution.** Although BLUEFOR briefs first, both teams' COAs happen at the same time in game terms. REDFOR, briefing second, **may** react to BLUEFOR's COA, which is realistic. It **may not** simply negate it ("their strike doesn't happen") or preempt BLUEFOR's roll. Negating is what Cons are for; a counter-move is resolved as an interacting or opposed COA (§4.2).

### 2.3 Phase I – Planning [CANON]

- Teams arrive having read the rules, scenario brief, and their team's intelligence products (distributed ≥ 24 hours prior). During Phase I (18 minutes), they organize their team, build a plan, and file RFIs and RFFs to posture forces before the war starts.
- **[CANON] Phase I request limit:** up to **4 requests in total** (RFIs and RFFs combined), **submitted by minute 12** (6 minutes before Phase I ends) so the white cell can adjudicate them while loggers hear the OPORD briefs. The white cell hands back answers and rulings after the kickoff inject, before Turn 1 begins. Phase I RFFs follow normal arrival timing (`scenario/00-overview.md` §6), counted from Turn 1.
- In the last 3 minutes (minutes 15–18) each team gives an **oral brief** of its plan to its own logger, **organized like a five-paragraph OPORD**: Situation, Mission, Execution, Sustainment, Command & Signal (AFDP 5-0 App. E; see App. A). No written OPORD is expected.
- **Planned COAs.** The brief may name **up to 3 planned COAs** in intended sequence for Phase II, e.g. "Turn 1: X; Turn 2: Y; Turn 3: Z". The logger writes them down. When a team later executes a planned COA *substantially as briefed, and the situation still supports it*, the white cell adds **+1 (Planned)**. If events make a planned COA invalid (the target is gone, the resources were lost, or the enemy forced a reaction), the bonus is lost. Recognizing that and adapting is the point.
- Phase I has **no COAs**. The first COAs come in Turn 1, after the kickoff inject.

### 2.4 Phase III – Planning and FRAGO [CANON]

- **Command handover and FRAGO.** After Turn 4 and Debrief 1, the **Phase III–IV flight commander** takes command for the 8 minutes of Phase III (`LLAB-SETUP.md` §3). In the last minute of Phase III, the new flight commander gives a **1-minute oral Fragmentary Order (FRAGO)** to the team's logger: updated Commander's Intent and **up to 2 new planned COAs for Phase IV (Turns 5–7)**, which earn the same **+1 (Planned)** bonus when executed as briefed.

---

## 3. Courses of action (arguments)

### 3.1 What a COA is [CANON frame; detail PROPOSED]

- **[CANON]** Each turn each team presents one COA with **up to 3 reasons** it will work or be especially effective (Pros).
- A COA has two parts:
  1. **Action:** who does what, where, and with which assets.
  2. **Measurable effect:** what will be true on the map or tracks if it succeeds. Examples: "PAT-1 destroyed," "Strait Traffic moves to Open," "Latah grants combat basing," "Omak Regime Stability −1."
- **One action per turn.** The action can be big ("mobilize the PFA militia brigades") or a multi-asset package ("F-35A + KC-46 + EC-37B strike package"), but it must serve **one** effect. Two unrelated things are two COAs. Pick one. Choosing priorities is the point.
- Not every COA has to be kinetic. Diplomatic, information, cyber, space, economic, logistics, and deception COAs are all valid and are often stronger. Think **DIME** (Diplomatic, Informational, Military, Economic) and **PMESII** (Political, Military, Economic, Social, Information, Infrastructure).
- **Big projects** take **at most 3 successful COAs**, e.g. building a coalition or standing up a dispersed ACE network. The white cell states the number up front.
- **Protected and hidden things** need successful COAs to find or get through them, with **no more than 3 layers**. Example: a hidden mobile SAM must first be **found** (ISR COA), then **struck**.
- **Long-term COAs** are allowed. If an argued effect can't finish within one turn's 3 days, success means it **has started and continues** until someone stops it.
- **Announcements** (press statements, declarations) are free. A briefer can add a one-sentence public statement to the COA slot. A statement with a measurable effect ("…in order to raise International Opinion by 1") *is* a COA.

### 3.2 Pros (reasons it will work) [PROPOSED]

- Up to **3**, stated during the COA slot.
- Strong Pros are **specific**, **relevant**, and **grounded**. They draw on:
  - **Established facts:** anything in the briefings, or anything created by an earlier successful COA. These are the strongest Pros. Building on the story is rewarded.
  - **Asset capabilities** listed in the scenario order of battle.
  - **Reasonable assumptions**, e.g. "trained aircrews outperform untrained militia." Unreasonable assumptions ("the militia shoots down the stealth bomber with rifles") count for nothing until someone has argued them into existence.
  - **Doctrine**, e.g. "This applies *mass* and *surprise* (principles of joint operations) and *concentration* (tenet of airpower)." Citing doctrine correctly and specifically counts. Name-dropping it doesn't.
- Weak, vague, or duplicate reasons are worth 0. Three weak Pros are worse than one strong one, because the briefer used up the time.
- **[PROPOSED] Intelligence products are not established facts.** Each side's intel products (`handouts/redfor/intel/`, `handouts/bluefor/intel/`, one file per product) are deliberately a mix of true, misleading, and irrelevant reports. A reason built on one counts only as far as the report is believable. The white cell judges it against ground truth, and confirming a report with an RFI or ISR COA makes it stronger.

### 3.3 Cons (reasons it won't work)

- **[CANON]** The opposing team gives **up to 3** reasons the COA will fail, be ineffective, or have minimal impact.
- **[PROPOSED]** The same quality rules apply.
- **[PROPOSED] Cons about consequences** ("that strike will cause civilian casualties and outrage") don't argue the action fails. They argue it has **costs**. The white cell treats them as shaping the *outcome* (side effects, track changes) rather than as −1s against success.

### 3.4 Secret COAs [CANON]

- Use these for **misdirection or conditional traps** only, e.g. decoy SAM sites, a honeypot network, booby-trapped port facilities. Do not use them for ordinary actions you'd simply rather hide.
- Each team may make **one secret COA per phase** (Phase II and Phase IV).
- To make one, write it on a slip with a **precise trigger**, hand it to the white cell, and announce "We are making a secret COA." That is your COA for the turn. The other team can't give Cons against something it can't see.
- The white cell resolves it **when the trigger occurs** and applies its own judgment in place of Cons. A trigger written too loosely doesn't fire. Precision is the player's job.

### 3.5 Arguing about actors [PROPOSED]

| Actor type | Can you argue about it? |
| --- | --- |
| Your own forces | Yes. That's normal. |
| The opposing team's forces | **Yes.** Argue about their morale, readiness, maintenance, gaps. You can't give them orders. |
| A **player-controlled** actor's *decisions* (the other team) | **No.** You can't argue "Omak agrees to a ceasefire." Ask them in person during Prepare. If they agree, it happens. |
| **White-cell-controlled** actors (non-player nations, populations, pirates, the press, weather) | Yes, through COAs ("A diplomatic delegation persuades Latah to grant basing because…"). The white cell adjudicates. |

---

## 4. Adjudication [CANON: white cell decides, dice by computer program; method PROPOSED]

**[CANON]** The white cell makes the final decision on probability of success and outcomes. **[CANON]** Dice are rolled with a **computer program**, not physical dice. The procedure below is **[PROPOSED]**. It uses Mouat's *weighted probability* method (2d6, 7+), the fastest method and the one he recommends for instructor-led games with junior students. The white cell needs it to resolve two COAs in 2 minutes.

### 4.1 Procedure (per COA)

1. **Screen.** Is the COA feasible within the turn's time, space, and the assets the team actually has (AFDP 5-0's "Feasible" test)? If not, the white cell rules it **impossible** (no roll) or **scopes it down** to what is feasible. Say so in one sentence.
2. **Automatic success?** If there were no credible Cons, or the case is overwhelming, it **succeeds without a roll**. Treat the result as **Success** (9–11 band). Mouat: sensible arguments should succeed unless challenged.
3. **Count modifiers** (cap the net total at **±4**):

   | Modifier | Value |
   | --- | --- |
   | Each **strong** accepted Pro | +1 (a single exceptionally compelling Pro may be +2) |
   | Each **strong** accepted Con | −1 (a single exceptionally compelling Con may be −2) |
   | Weak, vague, or duplicate reason | 0 |
   | **Planned** COA executed as briefed in Phase I (or Phase III FRAGO) and still valid | +1 |
   | **Starting conditions or ongoing effects** that apply (`scenario/00-overview.md` §5) | ±1 each, as listed |
   | Asset used in the COA is **Degraded** | −1 |

4. **Roll 2d6 in the dice program**, add the modifiers, and read the band:

   | Modified total | Result | Meaning |
   | --- | --- | --- |
   | **≤ 3** | **Critical failure** | Fails, and something goes wrong: losses, exposure, a backlash, a track moves against the actor. |
   | **4–6** | **Failure** | Doesn't happen, or has no meaningful effect. Assets may be Degraded if it was a risky combat action. |
   | **7–8** | **Partial success** | Happens, but limited or at a cost. Example: target Degraded instead of Destroyed, or success with own losses or a political cost. |
   | **9–11** | **Success** | Happens as argued. |
   | **≥ 12** | **Exceptional success** | Happens, plus a bonus. Example: an extra effect, a new established fact the team can build on, or a track moves in its favor. |

5. **Narrate in one or two sentences**, giving the reason for the result (the winning Pro or Con). Pros and Cons are valuable here because they explain *why* something failed.
6. Successful results become **established facts**. Loggers don't log every COA. They keep only the placement form (App. B).

### 4.2 Interacting COAs [CANON: simultaneous COAs; resolution PROPOSED]

Both COAs are briefed before either is resolved, so **they happen simultaneously across the 3-day turn window**. Because REDFOR briefs second, REDFOR's COA cannot prevent BLUEFOR's COA from being rolled; instead, a reactive move is resolved as an interacting or directly opposed COA.

- **Independent COAs** (different places or effects): resolve each normally, BLUEFOR's first.
- **Interacting COAs** (one affects the other's odds, e.g. BLUEFOR disperses its SAMs while REDFOR strikes them): fold the interaction into the modifiers. A well-timed counter-move is a strong Pro or Con even if nobody said it out loud.
- **Directly opposed COAs** (both can't succeed, e.g. both sides try to seize the same port): use an **opposed roll**. The program rolls 2d6 for each side, each side adds its own modifiers, and the higher total wins. On a tie, both are **Partial**, the situation stays contested, and the white cell describes a stalemate.

### 4.3 Time pressure

- **[PROPOSED]** If the 2 minutes run out, the lead adjudicator makes the call on the spot. Resolving fast matters more than resolving perfectly.
- **[PROPOSED] Contentious calls** happen when both teams keep arguing. Don't debate. Either make the call, or take a 10-second **estimative vote**: each white cell member shows fingers (1 = remote … 5 = almost certain), the white cell takes the **median**, and rolls against it (App. C).
- **[CANON] No recalculation.** Because the timing is strict, an objection raised late (after its slot, or after the roll) **is not considered**, and a result is not re-run once announced.

### 4.4 Fog of war [CANON: white cell introduces fog of war; mechanics PROPOSED]

- Opponent assets marked **hidden** in the scenario stay off the central map until found by a successful ISR COA, revealed by their own use, or disclosed by an inject. Mentioning a hidden asset in a COA or in a Pro or Con counts as using it, whether or not the COA succeeds (finalized White Cell Handbook §2.3).
- **RFI answers** reflect what your existing intelligence would plausibly know. That may be incomplete, uncertain ("unknown"), or wrong if the enemy has succeeded at deception. RFIs never reveal the enemy's secret objectives or secret COAs.
- **Injects** (§7) add friction: weather, civilian events, leaks, third-party moves.

---

## 5. Requests: RFIs and RFFs [CANON: limit of 3 combined per turn; Phase I: 4 due at minute 12]

| | RFI – Request for Information | RFF – Request for Forces |
| --- | --- | --- |
| Purpose | Ask what your side knows: enemy disposition, weather, a third party's stance, civilian situation | Ask your national command for more assets or authorities |
| Limit | **Up to 3 requests per turn in total, RFIs and RFFs combined** (Phase I: 4 due at minute 12, see §2.3) | (shared with RFIs) |
| Format | One question per slip, ≤ 1 sentence | Asset (from the scenario's RFF pool or a free-text request), destination, and purpose |
| Counts as COA? | No | No |
| Debate? | No | No |
| White cell response | Short written answer, delivered at the start of the next Prepare step | Approve, approve partially, or deny, with the **arrival turn** (`scenario/00-overview.md` §6). National politics shape approval (scenario tracks, e.g. Domestic Will). |

- **[PROPOSED]** Forces that arrive by RFF **do nothing on the turn they arrive** unless the scenario timing table says otherwise. Their arrival is announced and their counters placed during white cell resolution.
- **[PROPOSED]** A big RFF (a carrier strike group, a ground brigade, new authorities like permission to strike Omak City, the enemy capital) is a **political** decision. The white cell may deny it, or demand a successful COA first to build the case.

---

## 6. Negotiation and diplomacy between teams [PROPOSED]

- During **Prepare**, a team's flight commander (or a delegate) may request a **parley** with the opposing team. The lead adjudicator authorizes it, and it lasts **≤ 2 min**, taken out of Prepare.
- Whatever the players agree in person **happens** (no roll). Examples: prisoner exchanges, a local ceasefire, an agreement to open talks, a deal to let shipping through.
- Agreements are not self-enforcing. Breaking one is allowed, but it is an **established fact** that others can use in Pros and Cons (credibility and legitimacy), and the white cell may move tracks.
- Agreements aren't written down. If the sides later dispute what was agreed, the lead adjudicator decides.

---

## 7. Injects [CANON: white cell may deliver injects; content in scenario]

- The **kickoff inject** starts the war at the end of Phase I. It is **[CANON]** in function, and its wording is in `scenario/whitecell-injects.md` §1.
- **[PROPOSED]** The lead adjudicator may deliver **at most one inject per turn**, during the resolve step. Injects should (a) add fog and friction, (b) force teams to adapt their plan, or (c) **bound behavior** that is going off the rails. Example: "Cosmopolis's legislature passes a resolution forbidding strikes on Omak City (Omak's capital)" **[CANON tool]**.
- **[CANON]** No event cards. Random events come only through white cell injects.
- **[PROPOSED] Consequence management:** at the end of each resolve step, the white cell states ongoing effects (refugees, burning port, market panic). Ongoing effects persist and can give ±1 to related COAs **until a successful COA removes them**.

---

## 8. White Cell Adjudication Guide [PROPOSED unless tagged]

### 8.1 Lead adjudicator checklist (per turn)

1. Start the timer program for Prepare (5:00). Hand out RFI answers from last turn.
2. Collect request slips at the end of Prepare (≤ 3 per team).
3. Call the BLUEFOR COA (2:00), then the REDFOR COA (2:00). Don't allow interruptions.
4. Start the Cons prep (2:00). Call REDFOR Cons (1:00), then BLUEFOR Cons (1:00).
5. Resolve each COA: screen → auto-success? → modifiers → dice program → narrate.
6. Rule on RFFs and announce arrivals. State ongoing effects. Deliver an inject (optional).
7. Loggers move the map counters and tracks and update the placement forms. Start the next turn.

### 8.2 Judging reasons quickly

Ask four questions about each reason:

1. **Is it true?** It must be an established fact, a listed capability, or a reasonable assumption.
2. **Is it relevant** to *this* action and *this* effect?
3. **Is it new,** not a restatement of another reason already counted?
4. **Does it matter?** Would a real commander care?

Four yeses make it strong (±1). An exceptional reason, one that is decisive by itself, is ±2. Otherwise it's 0.

### 8.3 Doctrinal yardsticks (use them, and name them out loud in narration so cadets learn them)

- **COA validity (AFDP 5-0):** Feasible, Acceptable (risk vs. gain), Suitable (meets intent and objectives), Distinguishable, Complete. A COA that fails *Feasible* doesn't get rolled. One that fails *Acceptable* may succeed, but with a heavy cost.
- **Tenets of airpower (AFDP 3-0):** mission command, flexibility and versatility, synergistic effects, persistence, concentration, priority, balance.
- **Principles of joint operations (AFDP 3-0 / JP 3-0):** objective, offensive, mass, maneuver, economy of force, unity of command, security, surprise, simplicity, restraint, perseverance, legitimacy (plus unity of effort, as AFDP 3-0 lists it).
- **USAF core functions (AFDP 3-0):** Air Superiority, Global Precision Attack, Rapid Global Mobility, Global ISR, Command and Control.
- **ACE (AFDP 3-0 App. C):** dispersal to a network of smaller locations complicates enemy targeting, but it needs C2, logistics, and base defense to work.

### 8.4 Keeping the game on the rails

- **Over-reach** ("we invade and take Omak City this turn"): scope it down to what is feasible in 3 days with the assets on hand, or rule it impossible.
- **Laundry lists:** hold teams to 3 reasons and one action.
- **Off-the-rails behavior [CANON tool]:** use an inject that sets a national directive restricting it, or kill the COA outright.
- **Dominant players and nit-picking:** courtroom rules. "You had your slot." Move on.
- **[CANON] Behind schedule:** shorten **Prepare** (e.g. to 4 min). **Never cut the Cons**, which are where the learning happens.
- **[CANON] Late objections:** not recalculated (§4.3). Move on.

### 8.5 Several tables at once

If the game runs at several tables simultaneously, every white cell uses this document and the scenario document unchanged. They should agree beforehand on how generous to be with auto-success and on how big a single COA can be, so the tables stay comparable.

---

## 9. Game roles

### 9.1 Players (REDFOR and BLUEFOR teams)

- **[CANON]** Each team has an assigned **flight commander**. Who is assigned and when command changes hands is set in `LLAB-SETUP.md`.
- **[CANON]** **The team builds the rest of its own structure** during Phase I: who handles operations, intel, logistics, briefing, and so on. The rules don't prescribe staff roles.
- **[CANON]** Players **may use computers and AI** during play. The decisions and the briefs must still be the team's own.

### 9.2 White cell [CANON]

| Role | Per game | Job |
| --- | --- | --- |
| **Lead adjudicator** | 1 | Runs the timer program, gives injects, runs the dice program, final adjudication authority |
| **BLUEFOR logger** | 1 | Receives the BLUEFOR Phase I brief and Phase III FRAGO. Keeps the BLUEFOR placement form (App. B). Moves BLUEFOR counters. |
| **REDFOR logger** | 1 | Same for REDFOR |

### 9.3 End of game [PROPOSED]

After the final turn's resolution, the white cell states the end state (map and tracks) and scores each team's three objectives as Achieved, Partial, or Not achieved, using the criteria in §3 of each team packet (`scenario/redfor-packet.md`, `scenario/bluefor-packet.md`). The loggers record the result.

---

## 10. Worked example turn (Operation Zugzwang, Turn 1) [PROPOSED, illustrative]

*Asset IDs refer to the visible force tables in `scenario/redfor-packet.md` and `scenario/bluefor-packet.md`. These numbers are an illustration, not a prediction.*

**BLUEFOR COA (2:00):** "NDF Mark VI patrol boats (B-12) and the PFA maritime militia (B-18), covered by Harpoon coastal-defense battery CB-1 (B-08), establish an armed maritime exclusion and inspection zone across the Narrows, **in order to** move Strait Traffic from Restricted to **Closed**. It works because: (1) the Narrows are only ~25 miles wide and sit completely inside CB-1's ~75-mile anti-ship missile umbrella, so REDFOR surface ships can't escort freighters through safely; (2) the militia's 40 armed boats blend in with coastal traffic and swarm any ship that tries to run the Narrows, giving us *surprise* and *mass*; (3) closing the Strait pressures Cosmopolis's economy and its Domestic Will without us firing first on Cosmopolis warships."

**REDFOR COA (2:00):** "A strike package of F-35As (R-01) and an EC-37B Compass Call (R-10), refueled by KC-46s (R-05), strikes Patriot battalion PAT-1 (B-04) covering the Narrows, **in order to** destroy PAT-1 and open the air over the Strait for our ISR. It works because: (1) the F-35A is a stealth aircraft built to penetrate integrated air defenses; (2) Compass Call jamming cuts PAT-1 off from its early-warning radar network (B-07), which is *synergistic effects*; (3) the kickoff inject gives us *surprise*, because PAT-1 hasn't had time to relocate."

**REDFOR Cons → BLUEFOR (1:00):** "(1) Our RC-135 (R-07), P-8A (R-14), and MQ-9s (R-09) have been watching the Narrows since Phase I and will track patrol boat formations and holds. (2) Shutting down an international strait by threatening merchant shipping will turn International Opinion against Omak."

**BLUEFOR Cons → REDFOR (1:00):** "(1) Patriot is a mobile system, and our Phase I brief said we'd relocate PAT-1 at the outbreak of war. (2) Camas-based fighters have to fly ~620 miles each way, so they depend on tankers."

**White cell resolution (2:00):**

- **BLUEFOR maritime exclusion zone:**
  - Pros 1 and 2 are strong (+2). Pro 3 is about effect, not success, so it counts 0 here.
  - REDFOR Con 1 is strong (−1), because the maritime ISR presence is an established fact. REDFOR Con 2 is about consequences, so it doesn't affect success but will shape the outcome.
  - Closing the Narrows with patrol boats and CB-1 was a planned COA in BLUEFOR's Phase I brief and is still valid (+1).
  - The COA needs NDF boats/missiles and PFA militia to work together, so starting condition S-B1 *A House Divided* applies (−1).
  - Net **+1**. Program rolls 6; 6 + 1 = **7 → Partial success.** The exclusion zone is declared and shipping halts, moving Strait Traffic to **Closed**, but REDFOR P-8s and SIGINT tracked the patrol boats' patrol sectors and radar handoffs (established fact). Consequence: International Opinion moves 1 toward Cosmopolis.
- **REDFOR strike:**
  - Pros 1 and 2 are strong (+2).
  - BLUEFOR Con 1 is strong (−1), because the relocation was briefed before the war, and it cancels REDFOR Pro 3 (surprise counts 0).
  - BLUEFOR Con 2 is true, but the KC-46s are part of the package, so it counts 0.
  - Net **+1**. Program rolls 9; 9 + 1 = **10 → Success.** PAT-1 is caught during relocation and **Destroyed**. Counter removed.
- **RFFs:** REDFOR's request for an additional KC-46A detachment (R-31) is approved, arriving Turn 2.
- **Ongoing effect:** "Exclusion zone in the Narrows": −1 to any COA moving shipping through the Strait until the coastal threat and patrol boats are suppressed.

---

## 11. Open decisions for the designer

Settled (now CANON): owner, 3-day turns, fixed BLUEFOR-first order, simultaneous COAs within a turn, computer dice, timer program, oral five-paragraph Phase I brief, 4 combined Phase I requests due at minute 12, Phase III 1-minute FRAGO with up to 2 planned COAs, 3 combined requests per turn, no COAs in Phase I, secret COAs, cut Prepare not Cons, no late recalculation, flight-commander-only role assignment, POC jobs, no debrief content in the rules, no event cards, no GRAYFOR actor, the term FRAGO (not FRAGORD), loggers keep a placement form instead of logging every move, and the v10 map with Camas inside PrSM range.

Still open:

| ID | Decision | Draft assumes |
| --- | --- | --- |
| O1 | Adjudication details: the five result bands and the ±4 modifier cap (§4.1) | As written |
| O4 | Team-to-team parleys during Prepare (§6) | Allowed, ≤ 2 min |
| O5 | Estimative-vote fallback for contentious calls (§4.3) | Optional |

---

## Appendix A — Phase I brief and Phase III FRAGO formats (AFDP 5-0 App. E) [CANON: format; outline PROPOSED]

**Phase I brief:** an **oral** brief to the team's logger, ≤ 3 minutes (minutes 15–18 of Phase I). Nothing written is required. The logger notes the planned COAs.

```text
1. SITUATION   Enemy: what we think they will do (most likely / most dangerous).
               Friendly: our key assets and where they are.
2. MISSION     WHO does WHAT, WHEN, WHERE, and WHY (one sentence).
3. EXECUTION   a. Commander's intent — purpose, end state, acceptable risk.
               b. Concept of operations — how we get there, in phases.
               c. Planned COAs (up to 3): Turn 1 … Turn 2 … Turn 3 …
               d. Coordinating instructions — restraints and ROE we operate under.
4. SUSTAINMENT RFFs submitted, basing, what we're short of.
5. COMMAND & SIGNAL  How our team is organized; who decides and who briefs.
```

**Phase III FRAGO (in the last minute of Phase III):** an **oral** brief by the new Phase III–IV flight commander to the logger, ≤ 1 minute.

```text
1. SITUATION UPDATE  What changed in Phase II (key losses, tracks, enemy actions).
2. UPDATED INTENT    Adjusted purpose, end state, and acceptable risk for Phase IV.
3. PLANNED COAs      Up to 2 new planned COAs for Phase IV (Turns 5–7).
```

## Appendix B — Placement form (one per side) [PROPOSED]

Each logger keeps one placement form for its side (`handouts/whitecell/forms.md` §4). It records where things are **now**, not a history. Loggers don't log every COA, roll, or move. The form holds:

- the planned COAs from the Phase I brief (Turns 1–3) and the Phase III FRAGO (up to 2, Turns 5–7), each ticked when executed as briefed (for the +1 in §4.1);
- each hidden counter's zone, the turn it was revealed, and its state (BLUEFOR's B-06 zones are chosen in Phase I);
- approved RFFs, with the turn each arrives and where it is placed;
- visible counters that have moved, been Degraded, or been Destroyed since the starting setup.

When something changes, cross out the old entry and write the new one. Ongoing effects and big-project progress go on the public track board (`handouts/whitecell/forms.md` §2).

## Appendix C — Probability cheat sheet (2d6, need modified total ≥ 7)

| Net modifier | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Natural roll needed | 11+ | 10+ | 9+ | 8+ | 7+ | 6+ | 5+ | 4+ | 3+ |
| Chance of at least Partial success | 8% | 17% | 28% | 42% | 58% | 72% | 83% | 92% | 97% |

**Estimative vote → target (for §4.3):** 1 = Remote (10%, needs 11+ on 2d6) · 2 = Unlikely (30%, 9+) · 3 = Even chance (50%) · 4 = Likely (70%, 6+) · 5 = Almost certain (90%, 4+). These match Mouat's cheat card. The dice program can also roll a straight percentage.

## Appendix D — Doctrine crosswalk (game mechanic → doctrine)

| Game element | Doctrine | File |
| --- | --- | --- |
| Turn structure (COA → Cons → resolution) | Action–Reaction–Counteraction wargaming | AFDP 5-0 Ch 6, p. 43–44 |
| White cell COA screening | COA validity: Feasible, Acceptable, Suitable, Distinguishable, Complete | AFDP 5-0 Ch 5, p. 39 |
| Phase I brief | Modified five-paragraph order | AFDP 5-0 App. E |
| Commander's intent in the Phase I brief | Mission command principles; CC-DC-DE | AFDP 1-1 |
| Pros and Cons vocabulary | Tenets of airpower; principles of joint operations | AFDP 3-0 Ch 1; JP 3-0 |
| Asset tags | Five USAF core functions | AFDP 3-0 |
| Basing and dispersal COAs | Agile Combat Employment | AFDP 3-0 App. C |
| Phase I competition → war | Competition continuum | AFDP 3-0; AFDP 3-99 |
| Cross-domain COAs (space, cyber, EMS) | JADO principles | AFDP 3-99 |
| Overall method | Matrix games, Pros/Cons system | Mouat, *Practical Advice on Matrix Games* v15 (`references/PracticalAdviceOnMatrixGames.pdf`) |

## Appendix E — Glossary

| Term | Meaning |
| --- | --- |
| **COA** | Course of action: the one action a team argues for each turn |
| **Pro / Con** | Reason for or against a COA's success |
| **Established fact** | Anything in the briefings or created by a successful COA. It stays true until another COA changes it. |
| **Reasonable assumption** | Something any professional would accept without proof (trained troops beat untrained ones) |
| **RFI / RFF** | Request for Information / Request for Forces |
| **Inject** | A white cell event that changes the situation |
| **White cell** | The neutral control group: adjudicator and loggers |
| **REDFOR / BLUEFOR** | The two opposing player sides |
| **Counter** | A printed piece on the central map representing an asset or effect |
| **Track** | A numeric marker beside the map for something abstract (opinion, stability) |
| **Degraded / Destroyed** | Asset states. A Degraded asset gives −1 when used. A Destroyed one is removed. |
| **DIME / PMESII** | Instruments of power / dimensions of effect. A checklist for non-kinetic ideas. |

## Appendix F — Notes for AI agents

See `AGENTS.md` for the file map, editing rules, secrecy rules, and ID conventions.
