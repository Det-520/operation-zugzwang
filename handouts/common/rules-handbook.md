---
title: "Matrix Wargame — Player Rules Handbook"
subtitle: "AFROTC LLAB 12 · October 2026"
short: "Player Rules Handbook"
---

**Audience:** every player, REDFOR and BLUEFOR. Nothing in this handbook is secret. Released ASAP, before the scenario; scenario details in the examples are replaced with bracketed placeholders.

**You are expected to arrive at the LLAB having read, and knowing, everything in your read-ahead:** this handbook, the Scenario Brief, the Scenario Schedule, the Player Forms, and your team's documents. Your team's documents are secret, so don't show them to the other team.

*All countries, people, and events in this scenario are fictional. All military systems are real U.S. systems, described with unclassified, approximate capabilities.*

| Part | What it covers |
| --- | --- |
| **1. How to play** | The game in one page, the turn clock, and an example turn |
| **2. The rules in detail** | COAs, Pros and Cons, adjudication, requests, negotiation, roles, Slack channels, end of game |
| **3. Reference** | Doctrine cheat sheet and glossary |

<!-- pagebreak -->

## 1. How to play

### 1.1 The full game, briefly

1. **What this is.** A *matrix wargame*: there is no rulebook of unit stats. You win via arguments. Each turn your team proposes **one course of action (COA)** and gives **up to three reasons it will work**. The other team gives **up to three reasons it won't**. The **white cell** weighs the reasons, sets the odds, rolls the dice (with a computer program), and narrates what happens.
2. **Your side.** You are either **REDFOR** or **BLUEFOR**. Your team's documents give you your forces, your intel, and **three secret objectives**. Don't show the other team your objectives.
3. **One COA per turn.** A COA is *one* main action with a *measurable effect*, e.g. "[FIGHTER JET]s and an [EW AIRCRAFT] strike the [AIR DEFENSE] site near [CHOKEPOINT] **so that** [AIR DEFENSE UNIT] is destroyed and our ISR aircraft can operate over [STRAIT AREA]." You can use several assets in one COA (a strike package counts as one action), but you can't do two unrelated things. Everything else your forces do is background activity.
4. **Format of your COA (2 minutes):**

   > "Our COA: **[action]** in order to **[measurable effect]**. It will work because: **(1)** … **(2)** … **(3)** …"

5. **Format of your Cons (1 minute):**

   > "Their COA will fail or fall short because: **(1)** … **(2)** … **(3)** …"

6. **Good reasons** are specific and grounded in facts. They point to your assets' capabilities, the map, things that happened earlier in the game ("established facts"), and doctrine (tenets of airpower, principles of joint operations). Repeating a reason in new words earns nothing.
7. **Odds.** With no strong reasons either way, a COA succeeds on 7+ on two dice (58%). Each strong reason for it adds +1, and each strong reason against it subtracts 1. If a COA is obviously sound and unopposed, it succeeds without a roll. If a call is too contentious to count, the white cell may take a quick **estimative vote** on how likely it is instead (§2.7).
8. **RFIs and RFFs.** Each turn you may post **up to 3 requests in total** in your team's secret Slack channel, any mix of:
   a. **RFI (Request for Information):** a question about the situation.
   b. **RFF (Request for Forces):** a request for more assets or authorities from your national command. Reinforcements take time to arrive.

   Requests don't count as your COA, and there is no debate on them.
9. **Turn clock (15 minutes, run by a timer program).** See §1.2. **BLUEFOR always goes first.**
10. **Slack, not paper.** Slack is the written record, and you still brief out loud. Post your COA and Cons in your group's public channel, and your requests and any secret COA in your team's secret channel, where the white cell answers (§2.11).
11. **No interrupting.** It's a courtroom, not a debate. You speak in your slot and are silent in theirs. Raise only points of fact or procedure. **If you miss your slot, the point is lost.** There are no do-overs.
12. **Arguing about the other side is allowed.** You can argue *their* troops are tired or *their* radar has a gap. You cannot argue that a player-controlled actor *agrees* to something. Ask them in person instead.
13. **The point** is good decisions and good reasoning under pressure: plan, communicate, brief, defend your choices, and adapt.

### 1.2 The turn clock

Each turn is **15 minutes** of real time and about **3 days** of game time. **Both teams' COAs take place simultaneously across the 3-day window.**

| Step | Clock | Time | Who | What happens |
| --- | --- | --- | --- | --- |
| **Prepare** | 0:00–5:00 | 5:00 | Both teams | Pick this turn's COA. Post up to 3 RFIs/RFFs in your team channel. Negotiate if you want (§2.6, ≤ 2:00). Last turn's RFI answers are in your team channel at the start. |
| Requests close | 5:00 | — | Both teams | The white cell counts your first 3 request posts. No debate. |
| **BLUEFOR COA + Pros** | 5:00–7:00 | 2:00 | BLUEFOR briefer | Brief aloud: action, measurable effect, up to 3 reasons. Post the same COA in the group channel by 7:00. |
| **REDFOR COA + Pros** | 7:00–9:00 | 2:00 | REDFOR briefer | Brief aloud: action, measurable effect, up to 3 reasons. Post the same COA in the group channel by 9:00. |
| Prepare Cons | 9:00–11:00 | 2:00 | Both teams | Huddle to pick up to 3 Cons against the enemy's COA |
| **REDFOR Cons** on BLUEFOR's COA | 11:00–12:00 | 1:00 | REDFOR | Up to 3 reasons BLUEFOR's COA fails or has costs. Post them in the group channel by 12:00. |
| **BLUEFOR Cons** on REDFOR's COA | 12:00–13:00 | 1:00 | BLUEFOR | Up to 3 reasons REDFOR's COA fails or has costs. Post them in the group channel by 13:00. |
| **White cell resolves** | 13:00–15:00 | 2:00 | White cell | Rolls, narrates, rules on RFFs, moves counters and tracks, maybe an inject |

### 1.3 Example turn

*Scenario details are replaced with bracketed placeholders such as [FIGHTER JET].*

**BLUEFOR COA (2:00):** "[NAVY] [PATROL BOAT]s and the [MILITIA GROUP] maritime militia, covered by our [COASTAL MISSILE BATTERY], establish an armed maritime exclusion and inspection zone across [CHOKEPOINT], **in order to** move [SHIPPING TRACK] from Restricted to **Closed**. It works because: (1) [CHOKEPOINT] is only ~[XX] miles wide and sits inside our ~[XX]-mile [ANTI-SHIP MISSILE] umbrella, so REDFOR surface ships can't escort freighters through safely; (2) the militia's [NUMBER] armed boats blend in with coastal traffic and swarm any ship that tries to run [CHOKEPOINT], which gives us *surprise* and *mass*; (3) closing [CHOKEPOINT] pressures [REDFOR NATION]'s economy and its [MORALE TRACK] without us firing first on [REDFOR NATION] warships."

**REDFOR COA (2:00):** "A strike package of [FIGHTER JET]s and an [EW AIRCRAFT], refueled by [TANKER]s, strikes [AIR DEFENSE UNIT] covering [CHOKEPOINT], **in order to** destroy [AIR DEFENSE UNIT] and open the air over [STRAIT AREA] for our ISR. It works because: (1) the [FIGHTER JET] is a stealth aircraft built to penetrate integrated air defenses; (2) [EW AIRCRAFT] jamming cuts [AIR DEFENSE UNIT] off from its early-warning radar network, which is *synergistic effects*; (3) the war just started, which gives us *surprise*, because [AIR DEFENSE UNIT] hasn't had time to relocate."

**REDFOR Cons on BLUEFOR (1:00):** "(1) Our [SIGINT AIRCRAFT], [MARITIME PATROL AIRCRAFT], and [RECON DRONE]s have been watching [CHOKEPOINT] since Phase I and will track patrol boat formations and holds. (2) Shutting down [CHOKEPOINT] by threatening merchant shipping will turn [OPINION TRACK] against [BLUEFOR NATION]."

**BLUEFOR Cons on REDFOR (1:00):** "(1) [AIR DEFENSE SYSTEM] is a mobile system, and our Phase I brief said we'd relocate [AIR DEFENSE UNIT] at the outbreak of war. (2) [REDFOR AIR BASE]-based fighters have to fly ~[XXX] miles each way, so they depend on tankers."

**White cell resolution (2:00):**

- **BLUEFOR exclusion zone.** Pros 1 and 2 are strong (+2). Pro 3 is about the *effect*, not about success, so it counts 0 here. REDFOR Con 1 is strong (−1), because the maritime ISR presence is an established fact. REDFOR Con 2 is about *consequences*, so it doesn't change the odds but will shape the outcome. Closing [CHOKEPOINT] with patrol boats and coastal missiles was a planned COA in BLUEFOR's Phase I brief and is still valid (+1). The COA needs [NAVY] and [MILITIA GROUP] forces to work together, so starting condition [DISUNITY CONDITION] applies (−1). **Net +1.** The program rolls 6, and 6 + 1 = **7, a Partial success.** The exclusion zone is declared and shipping halts, moving [SHIPPING TRACK] to **Closed**, but REDFOR [MARITIME PATROL AIRCRAFT]s and SIGINT tracked the patrol boats' patrol sectors and radar handoffs (now an established fact). [OPINION TRACK] moves 1 toward [REDFOR NATION].
- **REDFOR strike.** Pros 1 and 2 are strong (+2). BLUEFOR Con 1 is strong (−1), because the relocation was briefed before the war, and it cancels REDFOR Pro 3 (surprise counts 0). BLUEFOR Con 2 is true, but the [TANKER]s are part of the package, so it counts 0. **Net +1.** The program rolls 9, and 9 + 1 = **10, a Success.** [AIR DEFENSE UNIT] is caught relocating and is **Destroyed**.
- **Ongoing effect** announced: "Exclusion zone in [CHOKEPOINT]": −1 to any COA moving shipping through [STRAIT AREA] until the coastal threat and patrol boats are suppressed.

**What to take from it:** specific Pros win, the best Cons attack the reasons rather than the goal, a good Phase I plan pays off, and Cons about *consequences* still matter even when they don't change the roll.

<!-- pagebreak -->

## 2. The rules in detail

### 2.1 The turn

- The steps and times are in §1.2. One turn is "a turn in the chess sense": each side acts once.
- **Fixed order.** BLUEFOR always briefs first and REDFOR second, every turn. The order never switches.
- **Simultaneous execution.** Both COAs happen at the same time across the 3-day turn window, because both are briefed before either is resolved. REDFOR, briefing second, **may react** to BLUEFOR's COA, which is realistic. It **may not** simply negate it ("their strike doesn't happen") or prevent BLUEFOR's COA from being rolled. Negating is what Cons are for; a counter-move is resolved as an interacting or opposed COA (§2.7).

### 2.2 Courses of action

**A COA has two parts.**

1. **Action:** who does what, where, and with which assets.
2. **Measurable effect:** what will be true on the map or tracks if it succeeds. Examples: "[AIR DEFENSE UNIT] destroyed," "[SHIPPING TRACK] moves to Open," "[REGIONAL ALLY] grants combat basing," "[BLUEFOR NATION] [STABILITY TRACK] −1."

**One action per turn.** The action can be big ("mobilize the [RESERVE FORCES]") or a multi-asset package ("[FIGHTER JET] + [TANKER] + [EW AIRCRAFT] strike package"), but it must serve **one** effect. Two unrelated things are two COAs. Pick one. Choosing priorities is the point.

**Think beyond kinetic.** Diplomatic, information, cyber, space, economic, logistics, and deception COAs are all valid and are often stronger. Use **DIME** (Diplomatic, Informational, Military, Economic) and **PMESII** (Political, Military, Economic, Social, Information, Infrastructure) as checklists.

#### Special cases

| Case | Rule |
| --- | --- |
| **Big projects** | Take **at most 3 successful COAs**, e.g. building a coalition or standing up a dispersed ACE network. The white cell states the number up front. |
| **Protected and hidden things** | Need successful COAs to find or get through them, **no more than 3 layers**. Example: a hidden mobile SAM must first be **found** (ISR COA), then **struck**. |
| **Long-term COAs** | If the effect can't finish within one turn's 3 days, success means it **has started and continues** until someone stops it. |
| **Announcements** | Press statements and declarations are free. Your briefer can add a one-sentence public statement in the COA slot. A statement with a measurable effect ("…in order to raise [OPINION TRACK] by 1") *is* a COA. |

### 2.3 Pros and Cons

**Pros** are up to 3 reasons your COA will work, stated in your COA slot. **Cons** are up to 3 reasons the other team's COA will fail, be ineffective, or have minimal impact, stated in your Cons slot. The same quality rules apply to both.

Strong reasons are **specific**, **relevant**, and **grounded**. They draw on:

- **Established facts:** anything in the briefings, or anything created by an earlier successful COA. These are the strongest reasons. Building on the story is rewarded.
- **Asset capabilities and limitations** listed in the order of battle. Every asset has a stated limitation. Those are your Cons.
- **Reasonable assumptions**, e.g. "trained aircrews outperform untrained militia." Unreasonable assumptions ("the militia shoots down a high-flying [AIRCRAFT] with rifles") count for nothing.
- **Doctrine**, e.g. "This applies *mass* and *surprise* (principles of joint operations) and *concentration* (tenet of airpower)." Citing doctrine correctly and specifically counts. Name-dropping it doesn't.

Weak, vague, or duplicate reasons are worth 0. Three weak reasons are worse than one strong one, because you used up the time.

**Cons about consequences** ("that strike will cause civilian casualties and outrage") don't argue that the action fails. They argue it has **costs**. The white cell uses them to shape the *outcome* (side effects, track changes), not the odds.

**The white cell's four questions.** Before you give a reason, check it the way the white cell will:

1. **Is it true?** An established fact, a listed capability, or a reasonable assumption.
2. **Is it relevant** to *this* action and *this* effect?
3. **Is it new,** not a restatement of a reason already given?
4. **Does it matter?** Would a real commander care?

Four yeses make a strong reason (±1). One that is decisive on its own can be ±2.

**Intelligence reports are not established facts.** Your intel products may be wrong. A Pro built on a report counts only as far as the report is believable, so confirm important reports with an RFI or an ISR COA first.

### 2.4 Secret COAs

- Use these for **misdirection or conditional traps** only, e.g. decoy SAM sites, a honeypot network, booby-trapped port facilities. Don't use them for ordinary actions you'd simply rather hide.
- Each team may make **one secret COA per phase**.
- Post it in your team channel with a **precise trigger** (template in the Player Forms), and announce aloud "We are making a secret COA." That is your COA for the turn. The other team can't give Cons against something it can't see.
- The white cell resolves it **when the trigger occurs**. A trigger written too loosely doesn't fire. Precision is your job.

### 2.5 Arguing about other actors

| Actor | Can you argue about it? |
| --- | --- |
| Your own forces | Yes. That's normal. |
| The opposing team's forces | **Yes.** Argue about their morale, readiness, maintenance, gaps. You can't give them orders. |
| A **player-controlled** actor's *decisions* (the other team) | **No.** You can't argue "BLUEFOR agrees to a ceasefire." Ask them in person during Prepare. If they agree, it happens. |
| **White-cell-controlled** actors (other nations, populations, pirates, the press, weather) | Yes, through COAs. The white cell adjudicates. |

### 2.6 Negotiation

- During **Prepare**, your flight commander (or a delegate) may ask the lead adjudicator for a **parley** with the other team. It lasts **up to 2 minutes**, taken out of Prepare.
- Whatever the players agree in person **happens**, with no roll. Examples: prisoner exchanges, a local ceasefire, an agreement to open talks, a deal to let shipping through.
- Agreements are not self-enforcing. You may break one, but the broken deal becomes an **established fact** that others can use in Pros and Cons, and the white cell may move tracks.

### 2.7 How the white cell decides

The white cell makes the final decision. It works through each COA like this:

1. **Screen.** Is the COA feasible within 3 days, the map, and the assets you actually have? If not, it is ruled **impossible** (no roll) or **scoped down**.
2. **Automatic success.** If there were no credible Cons, or the case is overwhelming, it **succeeds without a roll**.
3. **Count modifiers** (net total capped at **±4**):

   | Modifier | Value |
   | --- | --- |
   | Each **strong** Pro | +1 (an exceptional one may be +2) |
   | Each **strong** Con | −1 (an exceptional one may be −2) |
   | Weak, vague, or duplicate reason | 0 |
   | **Planned** COA executed as briefed and still valid | +1 |
   | Starting conditions or ongoing effects that apply (Scenario Brief §6) | ±1 each |
   | An asset used in the COA is **Degraded** | −1 |

4. **Roll 2d6** in the dice program, add the modifiers, and read the result:

   | Total | Result | Meaning |
   | --- | --- | --- |
   | **≤ 3** | **Critical failure** | Fails, and something goes wrong: losses, exposure, backlash, a track moves against you. |
   | **4–6** | **Failure** | Doesn't happen, or has no meaningful effect. Assets may be Degraded if it was a risky combat action. |
   | **7–8** | **Partial success** | Happens, but limited or at a cost (e.g. target Degraded instead of Destroyed). |
   | **9–11** | **Success** | Happens as argued. |
   | **≥ 12** | **Exceptional success** | Happens, plus a bonus: an extra effect, a new established fact, or a track moves in your favor. |

5. **Narrate.** The white cell gives the result and the reason in a sentence or two. Successful results become **established facts**.

#### Your odds at a glance

| Net modifier | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Natural roll needed | 11+ | 10+ | 9+ | 8+ | 7+ | 6+ | 5+ | 4+ | 3+ |
| Chance of at least Partial | 8% | 17% | 28% | 42% | 58% | 72% | 83% | 92% | 97% |

**When COAs interact or collide.** Both COAs happen simultaneously across the 3-day turn window. If one affects the other's odds (e.g. BLUEFOR disperses SAMs while REDFOR strikes them), the white cell folds that into the modifiers. If both teams' COAs can't both succeed (e.g. both try to seize the same port), the program rolls for each side, each adds its own modifiers, and the higher total wins. A tie is a stalemate: both are Partial.

**Estimative vote.** When a call is contentious (both teams keep arguing, or the call is too close to count), the lead adjudicator may announce an **estimative vote** instead of counting modifiers. Each white cell member shows 1–5 fingers for how likely your COA is to work, the white cell takes the median, and the dice program rolls against it. If it happens, it's a **Success**; if not, a **Failure**. It takes about 10 seconds, and the result is final like any other.

| Vote (median) | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| Meaning | Remote | Unlikely | Even chance | Likely | Almost certain |
| Chance it happens | 8% (11+) | 28% (9+) | 50% | 72% (6+) | 92% (4+) |

The arguments still matter: the white cell members vote on how strong your Pros and the other team's Cons were.

**No recalculation.** An objection raised late (after its slot, or after the roll) **is not considered**, and a result is not re-run once announced.

### 2.8 Counters and fog of war

- **Counter states:** **Ready** · **Degraded** (−1 when used) · **Destroyed** (removed).
- **Visible** counters start on the central map, where both teams can see them.
- **Split counters.** An asset spread over several zones has one counter per part, lettered after its ID. For example, the PFA militia brigades are B-19a, B-19b, and B-19c, one each in Z10, Z11, and Z12. Each part moves, is found, and is Degraded or Destroyed on its own, and a strike on a zone touches only the parts in it. Name one part ("B-19b") or the whole asset ("B-19", meaning every part).
- **Hidden** counters stay on your team sheet. The enemy doesn't know about them until they are found by a successful ISR COA, revealed by their own use, or disclosed by an inject. Mentioning a hidden asset in a COA or in a Pro or Con counts as using it, whether or not the COA succeeds. Once a hidden counter is used, it goes on the map.
- **RFI answers** reflect what your intelligence would plausibly know. They may be incomplete, uncertain ("unknown"), or wrong if the enemy has succeeded at deception. RFIs never reveal the enemy's secret objectives or secret COAs.
- **Injects** are events the white cell introduces, such as weather, civilian events, leaks, and third-party moves. There is at most one per turn. Injects may also set new national directives.
- **Ongoing effects** announced by the white cell ("burning port," "exclusion zone in [CHOKEPOINT]") persist and can give ±1 to related COAs until a successful COA removes them.

### 2.9 Requests: RFIs and RFFs

| | RFI – Request for Information | RFF – Request for Forces |
| --- | --- | --- |
| Purpose | Ask what your side knows: enemy disposition, weather, a third party's stance, the civilian situation | Ask your national command for more assets or authorities |
| Limit | **Up to 3 per turn, RFIs and RFFs combined** | Shared with RFIs |
| Format | One Slack message per request: one question, one sentence | Asset (from your RFF pool, or a free-text request), destination, and purpose |
| Answer | A short written answer in a thread under your post, by the start of the next Prepare | Approved, partly approved, or denied, with the **arrival turn** |

- Requests posted after Prepare ends aren't answered. Post them again next turn.
- Forces that arrive by RFF **do nothing on the turn they arrive** unless the timing table says otherwise.
- Forces that arrive by RFF go on **Z6 Camas** (REDFOR) or **Z11 Omak City** (BLUEFOR) unless your RFF names another destination.
- A big RFF (a [MAJOR FORMATION], or new authorities like permission to strike [ENEMY CAPITAL]) is a **political** decision. The white cell may deny it, or demand a successful COA first to build the case.

### 2.10 Roles

| Role | Who | Job |
| --- | --- | --- |
| **Flight commander** | Assigned | Leads the team, makes the final call, and briefs |
| **Everyone else** | Commander's choice | Operations, intel, logistics, briefing, and anything else your team decides it needs |
| **Lead adjudicator** | White cell | Runs the clock, the dice, and injects. Final authority. |
| **Loggers** | White cell (one per side) | Hear briefs and move counters |

You **may use computers** during play. The decisions and briefs must be your team's own.

### 2.11 Slack channels

- **Before the LLAB:** accept the Slack invitation that comes with your team assignment and join both of your channels:
  - your **group channel** (public), shared by both teams in your group and the white cell, for example `opz-group1-army`;
  - your **team channel** (secret), shared only by your team and your group's white cell, for example `opz-alpha-redfor`. The other team is never in it.
- **Bring a device.** At least one teammate keeps Slack open at the table. Pick a team member to post.
- **Group channel:** your COA and Pros (by the end of your COA slot) and your Cons (by the end of your Cons slot).
- **Team channel:** each RFI or RFF as its own message (during Prepare), and any secret COA. Never post secrets in the group channel.
- Copy-and-paste templates are in the Player Forms.
- **Speaking still counts.** Your briefer briefs out loud in your slot, and only what is said in the slot counts. The post is the written record the white cell reads while it adjudicates, so use asset IDs (R-01, B-19b). Reasons in the post that weren't said aloud add nothing.
- **What you get back:** RFI answers and RFF rulings in a thread under each request, in your team channel.
- **If Slack goes down,** write the same thing on a backup paper slip from the white cell and hand it over.
- Never share your team channel's contents where the other team can see them.

### 2.12 End of game

After Turn 7 the white cell states the final map and tracks, then scores each team's three secret objectives as **Achieved**, **Partial**, or **Not achieved**. The two sides' objectives aren't always opposed, so it is possible for both teams to achieve something. Talking to the other team can pay off.

<!-- pagebreak -->

## 3. Reference

### 3.1 Doctrine cheat sheet

Cite these by name in your Pros and Cons, and say *how* they apply.

**Tenets of airpower** (AFDP 3-0)

| Tenet | In one line |
| --- | --- |
| Mission command | Centralized command, distributed control, decentralized execution: subordinates act on the commander's intent |
| Flexibility and versatility | Airpower can shift quickly between targets, missions, and theaters, and one asset can do many jobs |
| Synergistic effects | Coordinated forces produce effects greater than the sum of their parts |
| Persistence | Airpower can keep up pressure over time (tankers, ISR orbits, repeated strikes) |
| Concentration | Mass airpower at the decisive point and time. Don't spread it thin. |
| Priority | Limited assets go to the most important effects first |
| Balance | Weigh opportunity against risk and resources |

**Principles of joint operations** (AFDP 3-0, JP 3-0): **objective**, **offensive**, **mass**, **maneuver**, **economy of force**, **unity of command**, **security**, **surprise**, **simplicity**, **restraint**, **perseverance**, **legitimacy**, plus **unity of effort**.

**USAF core functions** (AFDP 3-0): Air Superiority (**AS**), Global Precision Attack (**GPA**), Rapid Global Mobility (**RGM**), Global ISR (**GISR**), Command and Control (**C2**).

**COA validity tests** (AFDP 5-0). The white cell screens every COA against these, so you should too:

| Test | Ask yourself |
| --- | --- |
| **Feasible** | Can we do it in 3 days with what we actually have, where it actually is? |
| **Acceptable** | Is the gain worth the risk and the cost? |
| **Suitable** | Does it move us toward our objectives? |
| **Distinguishable** | Is it really different from what we did last turn? |
| **Complete** | Does it say who, what, where, when, and why? |

**Agile Combat Employment (ACE)** (AFDP 3-0 App. C): dispersing to a network of smaller locations complicates enemy targeting, but it needs C2, logistics, and base defense to work.

**DIME** instruments of power: Diplomatic, Informational, Military, Economic. **PMESII** dimensions: Political, Military, Economic, Social, Information, Infrastructure. Run through both when you need a non-kinetic idea.

### 3.2 Glossary

| Term | Meaning |
| --- | --- |
| **COA** | Course of action: the one action a team argues for each turn |
| **Pro / Con** | A reason for or against a COA's success |
| **Established fact** | Anything in the briefings or created by a successful COA. It stays true until another COA changes it. |
| **Reasonable assumption** | Something any professional would accept without proof (trained troops beat untrained ones) |
| **RFI / RFF** | Request for Information / Request for Forces |
| **Inject** | A white cell event that changes the situation |
| **Estimative vote** | A quick white cell vote (1–5) on how likely a contentious COA is to work, rolled in the dice program instead of counting modifiers |
| **White cell** | The neutral control group: the lead adjudicator and loggers |
| **REDFOR / BLUEFOR** | The two opposing player sides |
| **Counter** | A printed piece on the map representing an asset or effect |
| **Track** | A marker beside the map for something abstract (opinion, stability) |
| **Ready / Degraded / Destroyed** | Asset states. A Degraded asset gives −1 when used. A Destroyed one is removed. |
| **Visible / Hidden** | Whether a counter is on the map for the enemy to see, or only on your team sheet |
| **DIME / PMESII** | Instruments of power / dimensions of effect. A checklist for non-kinetic ideas. |
| **ACE** | Agile Combat Employment: operating from a dispersed network of locations |
| **ISR** | Intelligence, surveillance, and reconnaissance |
| **HUMINT / SIGINT / IMINT / OSINT** | Intelligence from human sources / intercepted signals / imagery / open sources (news, social media) |
| **SOF** | Special operations forces |
| **SAM** | Surface-to-air missile |
