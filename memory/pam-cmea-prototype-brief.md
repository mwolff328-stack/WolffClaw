---
name: CMEA Prototype Redesign — Product Brief
description: Pam's product brief for the SurvivorPulse CMEA Prototype demo redesign, prioritizing the three demo moments based on competitive intelligence
type: project
date: 2026-04-08
---

# CMEA Prototype Redesign — Product Brief

**Author:** Pam (Product Owner)
**Date:** 2026-04-08
**Status:** Approved — ready for Ann → Felix

---

## Problem Statement

Sophisticated multi-entry Survivor pool players — the kind running 3–10 entries in $25K+ buy-in contests — are coordinating their portfolios today with spreadsheets, gut feel, and ad hoc methods because no existing tool actually treats their entries as a unified portfolio. PoolGenius and PoolCrunch both operate on a per-entry, per-subscriber basis: PoolGenius recommends the same pick to 50,000+ subscribers (explicitly collapsing its own EV), and PoolCrunch's "Optimal Path" is per-group independent planning, not cross-entry coordination. Neither product ever shows a player "here are your N entries this week, here is why each is picking something different, and here is how correlated your elimination risk is." SurvivorPulse's CMEA Prototype must prove, in the first 30 seconds of a demo, that it solves this problem in a way competitors structurally cannot replicate.

---

## Target User / ICP

The target user is a Circa Survivor-level player: sophisticated, multi-entry, high-stakes. They are running 3–10 entries in contests with meaningful buy-ins ($25K+) and already think in portfolio terms — they are not being introduced to the concept, they are looking for a tool that operationalizes it. They know PoolGenius and PoolCrunch by name, have likely paid for both, and feel the gap between what those tools offer and what they actually need to run a coordinated multi-entry strategy.

---

## Success Criteria

A demo is considered working when all of the following are true:

1. **First-screen clarity**: A player landing on the prototype can identify all of their entries, their assigned picks for the current week, and the rationale for each pick — without clicking anything — within 15 seconds.
2. **Correlated risk legibility**: A player can state the correlation risk of their portfolio (what happens if one game goes wrong) in plain language after seeing Moment 2 for the first time, without any explanation from a salesperson.
3. **Differentiation recall**: In a post-demo debrief, a player can articulate why SurvivorPulse is different from PoolGenius without being prompted — specifically referencing the personalization/dilution contrast.
4. **Demo completion rate**: A guided demo can be completed in under 5 minutes covering all three moments without the presenter needing to explain the underlying algorithm.
5. **"I need this" response**: At least 7 of 10 Circa-level players shown the demo express a clear intent signal (verbal, written, or behavioral) that they would use or pay for this tool.

---

## Scope

### IN Scope

- **Unified portfolio pick slate (Moment 1)**: Side-by-side view of all N entries showing assigned team, week number, and per-entry rationale for the pick. This is the above-the-fold, first-thing-seen surface.
- **Correlated elimination risk (Moment 2)**: Named metric and visual showing how correlated the portfolio is this week. Contrast display vs. an uncoordinated baseline (all entries same team).
- **Personalization story (Moment 3)**: Explicit copy and UI moment contrasting SurvivorPulse's per-user coordination with PoolGenius's subscriber-dilution model.
- Front-end and UX changes only — React/Vite/TypeScript SPA, using existing live API at survivorpulse.com.
- Using existing API response fields only: `allocation[]`, `independentPicks[]`, `coordinatedSurvivalProbability`, `independentSurvivalProbability`, `portfolioSurvivalDelta`, `duplicateTeamsAvoided[]`, `yahooPickPct` per entry, `perPickReasonByTeamId` per entry, `outcome` per entry, `pWinNow` per entry, `overallScore100` per entry.

### OUT of Scope

- Season-long survival replay as a primary demo vehicle — deprioritized, may exist but is not the hero flow.
- Per-week survival probability math as a hero metric — supporting context only, not the lead.
- Backend algorithm changes of any kind.
- New API endpoints — if the data does not exist in the current API response, it does not appear in the demo.
- Statistical literacy prerequisites — the demo must work for a player who does not want to think about math.
- Mobile optimization (desktop demo context assumed).

---

## Sequencing

**Build Moment 1 first.**

The unified portfolio pick slate is the foundational surface. Without it, Moments 2 and 3 have nothing to anchor to — both the correlation risk and the personalization contrast only land if the player has already seen that their entries are being treated differently from each other. Moment 1 is also the clearest competitive differentiator: neither PoolGenius nor PoolCrunch shows this view at all. It is the fastest path to "I have never seen this before" from a Circa-level player.

**Then Moment 2.**

Once entries are visible side by side, correlation risk becomes a natural "so what does this mean for my exposure?" extension. The contrast with an uncoordinated baseline (all entries on same team) is only meaningful after the player has seen that their coordinated slate already differs.

**Then Moment 3.**

The personalization story is a coda — it lands hardest after the player has experienced Moments 1 and 2 and is already forming a "why is this different" question in their head. It is a one-sentence answer to a question the demo has already made them ask.

---

## Open Questions for Mike

Before Felix begins any build work, the following need answers:

1. **Entry count for demo**: Should the demo default to a specific number of entries (e.g., 5) for the prototype, or should it reflect whatever the live API returns? Is there a "canonical demo account" with a specific entry set?
2. **Correlation metric naming**: Is "correlated elimination risk" the working name for the metric, or is there an existing internal term (e.g., from the algorithm or prior demos) that should be used instead?
3. **Baseline for contrast**: For the uncoordinated player contrast in Moment 2, should the baseline be computed from actual field ownership data (yahooPickPct), or should it be a simplified "all entries same team" hypothetical for demo clarity?
4. **Rationale copy ownership**: The `perPickReasonByTeamId` field — is the copy in that field already demo-quality, or does it need editorial review/rewrite before it surfaces in the UI?
5. **Eliminated entries in demo**: If some entries in the demo dataset are already eliminated, should those entries appear in the Moment 1 slate (grayed out)? Or should the demo dataset be constrained to a week where all entries are live?
6. **PoolGenius contrast copy**: Is there legal/marketing approval needed before naming PoolGenius explicitly in the UI for a demo context, or is that cleared?
