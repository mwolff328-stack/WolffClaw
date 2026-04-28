---
name: Stan's Strategy-to-Context Matching Framework
description: Framework for recommending the optimal pick strategy for each pool/entry based on pool rules, field state, entry history, and position. The personalization layer that turns CMEA from a static allocation engine into an adaptive decision-support system.
type: research
date: 2026-04-28
priority: P1 (SurvivorPulse)
requested_by: Michael / Luigi
depends_on:
  - stan-backtesting-research.md (Rounds 1-11)
  - stan-entry-scale-research.md (Round 6)
  - stan-buyback-research.md (Round 8)
  - stan-roi-analysis.md
  - stan-roi-gaps-analysis.md
  - stan-competitor-demo-research.md
  - stan-x-account-research.md
---

# Strategy-to-Context Matching Framework

**Stan the Scout — Intelligence Layer**
**Date:** 2026-04-28

---

## Brief (Restated)

Our backtesting research (11 rounds, 14+ strategies, 3-10 seasons, multiple entry counts) has established which strategies perform best in aggregate. What we have NOT yet answered: "Given THIS specific pool's rules, field size, current week, and THIS entry's remaining team inventory, which strategy should this entry use?"

This document proposes the personalization layer that turns CMEA from a static allocation engine into an adaptive decision-support system. It answers all five key research questions: pool-level variables, entry-level variables, competitive gap analysis, the strategy-matching decision model, and validation roadmap.

---

## Key Findings (7 bullets)

1. **Buyback availability is the single most powerful pool-level variable.** It completely reverses the strategy ranking at every entry count — SP Conservative 65/25/10 wins ALL entry counts in buyback pools, while losing at every entry count without buybacks. No other context variable produces a similarly dramatic flip. The app MUST detect and surface buyback status before recommending a strategy.

2. **Portfolio size creates three distinct strategic regimes, not a smooth continuum.** n=1–5 (simple blend), n=6–20 (coordination/EV-aware), n=31+ (return to simplicity). The n=6–20 range is the ICP sweet spot where CMEA provides the most differentiated value. Outside that range, simpler strategies win or tie.

3. **Neither PoolGenius nor PoolCrunch provides context-aware strategy recommendations.** PoolGenius literally cannot do so by design (would dilute their own subscribers' EV). PoolCrunch's Portfolio Optimal Path is per-entry-group optimization with no cross-entry coordination. Context-aware personalization is an unoccupied competitive position.

4. **Entry-level team inventory is the key within-regime differentiator.** Two entries in the same n=10 pool running the same "SP Production" strategy should diverge in picks if one has exhausted high-value teams (KC, BUF, DET) while the other hasn't. The optimal strategy shifts toward scarcity-aware or contrarian modes when the A-tier team slate is depleted.

5. **Season phase (early/mid/late) creates overlapping inflection points.** Early-season (Weeks 1-7): contrarian weighting deserves higher emphasis (field still large, upsets matter less for survival). Mid-season (Weeks 8-14): future value preservation becomes critical as teams get used up. Late-season (Weeks 15-18): pure survival maximization — take the safest pick available, diversification secondary.

6. **Field size and estimated survivors remaining drive EV leverage magnitude.** In a 50-player pool with 35 survivors in Week 3, pick popularity barely matters. In a 10,000-player pool with 500 survivors in Week 12, contrarian positioning can produce 3-5× the EV leverage. The optimal WP/contrarian weight ratio should scale with expected field size at time of pick.

7. **The data gap for context-aware validation is large but bounded.** We can build a credible v1 framework from existing research by holding constant pool type and n, then varying the within-regime variables. The highest-value new simulation is a "dynamic strategy switching" run that assigns strategy based on entry state each week rather than fixing it for the whole season.

---

## Question 1: Pool-Level Variables That Should Influence Strategy Selection

### 1.1 Buyback Availability — PRIMARY SWITCH

**What the data says:** Round 8 buyback research is unambiguous. Across 432 no-buyback runs and 432 buyback runs (all strategies × 4 entry counts × 3 seasons), the winner changed at EVERY entry count when buybacks were introduced. Without buyback: SP Conservative loses at every entry count. With Wk1-3 buyback: SP Conservative wins at every entry count (by large margins).

| Entry Count | No-Buyback Winner | Buyback Winner | Same? |
|-------------|-------------------|----------------|-------|
| n=5 | Mixed Portfolio (67 EW) | SP Conservative (78 EW) | No |
| n=10 | Core/Satellite (101 EW) | SP Conservative (165 EW) | No |
| n=20 | Core/Satellite (130 EW) | SP Conservative (248 EW) | No |
| n=50 | 70/30 Blend (295 EW) | SP Conservative (463 EW) | No |

**Why:** Conservative strategies take more early-week risks (slightly lower WP picks → more early eliminations). Buybacks convert those early deaths into resurrections. The result compounds: conservative entries re-enter at Week 4-5 with their teams intact, then execute the conservative strategy's strong mid-to-late season advantage. Without buybacks, those early eliminations are permanent losses.

**Buyback window width matters:** Wk1-4 buyback outperforms Wk1-3 by ~3-31 additional entry-weeks across entry counts. Wider windows → stronger case for SP Conservative → potentially even more conservative early picks.

**Strategy decision rule:**
- Pool has buyback: → SP Conservative 65/25/10, regardless of other factors (subject to entry-level modifiers below)
- Pool has no buyback: → Continue to portfolio size and other pool-level variables

### 1.2 Pool Format

**Standard Elimination** (1 life per entry, no buyback): The baseline model. Most of our backtesting applies directly.

**Strike/Multi-Life Format** (e.g., 3 strikes before elimination): Strategy should shift toward more aggressive EV-seeking early (a wrong pick costs a strike, not death), then conservative late (once at 2 strikes, revert to near-pure WP). No backtesting data on this yet — flag as simulation gap.

**Last Man Standing** (same as standard elimination, but often with fewer total players): Pool size variable becomes critical. Small LMS pools (20-50) → minimize correlation between your entries. Large LMS pools (500+) → field dynamics and contrarian weighting matter more.

**Circa-Style High-Stakes** ($1,000+/entry, large prize pool, no buyback, hard season limits):
- The late-season survival premium is dramatically amplified (2× advantage in Week 14+ entries vs naive per ROI gap research)
- Recommend Adaptive Blend 90/10→50/50 for n=10 Circa (highest late-week survival: 4% vs 2% for naive at n=10)
- These players have the most to gain from any SP premium feature; should receive the most sophisticated context recommendations

**Signal for product:** Pool format should be collected at pool creation and serve as the top-level routing variable in the recommendation engine.

### 1.3 Buy-In and Prize Structure

**Winner-Take-All (WTA):** Survival at any week is good, but surviving to the final 1-3 is everything. This amplifies the value of late-season picks (Wk 14+) and reduces the value of early-week diversification somewhat. SP's tiered correction factor (1.5-1.8×) applies.

**Top-Heavy (top 3-5 get prizes):** Similar to WTA but with slightly more value on mid-late survival (Wk 10-15). No backtesting data specific to tiered payout structure.

**Flat payout (prize for last N% of field, everyone who survives gets equal share):** EV is more linear with weeks survived. Here, pure entry-week maximization is the right objective — 70/30 Blend or SP Production are more appropriate than late-survival-heavy strategies. Contrarian weighting has less value (you don't need to outlast everyone, just most).

**Rake:** Pools with 10%+ rake require n≥10 for SP to bring entries near breakeven. At high rake, the recommendation engine should surface "you need 10+ entries for SP to overcome this pool's edge." This is financial education, not just strategy selection.

### 1.4 Field Size and Current Survivor Count

**Field Size** determines the absolute leverage of contrarian picks:
- Small pool (20-50 players): Contrarian weighting matters less — a 15% pick share represents 3-7 people. Even if they all die, you don't gain much positional edge.
- Medium pool (100-500 players): Contrarian weighting is where SP earns its keep. 15% pick share = 15-75 people dying together.
- Large pool (1,000+ players): Contrarian weighting is essential. The "mass grave" dynamic (30%+ of the field dying on one team) creates enormous position swings.

**Current Survivor Count** (how many entries are still alive):
- **Early stage (>40% of field alive):** Normal strategy applies. Contrarian weight can be higher.
- **Mid stage (10-40% alive):** Future value becomes critical. Teams remaining in your inventory relative to schedule quality determines late-season viability.
- **Late stage (<10% alive, typically Week 13+):** Maximize raw survival probability. Contrarian weighting should drop; WP dominance should increase. You're not trying to create leverage — you're trying to survive one more week.

**Decision rules:**
- Estimated survivors > 500: Boost contrarian weight component by +5-10%
- Estimated survivors 50-500: Standard weighting
- Estimated survivors < 50: Reduce contrarian weight by -5%; shift toward pure WP

### 1.5 Current Week in Season

**Weeks 1-7 (Early Season):**
- Strong teams haven't been used yet by most entries — team scarcity is low
- Future value penalty should be lower (you haven't burned much yet)
- Contrarian premium is high — the field is still picking obvious favorites
- Recommended weight shift: Lower FV component, maintain or slightly boost contrarian

**Weeks 8-14 (Mid Season):**
- Team scarcity begins to bite. Kansas City, Buffalo, Detroit get used up across entries
- Future value preservation is critical — saving a strong team for a critical late-week matchup
- Scarcity-Aware strategy and lookahead variants show their strongest relative performance here
- Recommended weight shift: Increase FV component, reduce contrarian slightly

**Weeks 15-18 (Late Season / Survival Mode):**
- Most entries have used their top teams. Survival is about managing whatever is left.
- This is pure WP territory — pick the best available team regardless of ownership
- The anti-chalk benefit disappears when the field is decimated and everyone is picking from the same depleted menu
- Recommended weight shift: Weight collapses to ~90% WP / 10% everything else

**Season phase decision rules (approximate):**
| Week | Recommended WP Weight | Contrarian Weight | FV Weight |
|------|-----------------------|-------------------|-----------|
| 1-4  | 60-65% | 25-30% | 5-15% |
| 5-9  | 65-70% | 15-25% | 10-20% |
| 10-14| 70-75% | 10-15% | 15-20% |
| 15-18| 85-95% | 5-10% | 0-5% |

### 1.6 Other Pool-Level Variables

**Buyback deadline proximity:** If buyback window closes after Week 3 and this is Week 2, the entry should be more aggressive now (knowingly risking a strategic upset to gain contrarian position) — because if they lose, they come back next week anyway.

**One-time vs. multi-week picks:** Standard weekly pick pools vs. formats requiring multiple picks per week (picks against the spread, 2-game survivor, etc.) require their own strategy models. Out of scope for current framework.

**Geographic/social context:** Office pools with small, socially cohesive groups tend to have highly correlated picks (everyone picks the same team because they talk). Contrarian weighting is MORE valuable in these pools because correlation is higher. No data on this; flag as research gap.

---

## Question 2: Entry-Level Variables That Should Influence Strategy Selection

### 2.1 Teams Already Used (Remaining Inventory)

This is the most directly actionable entry-level variable. The quality of remaining teams determines which strategies are still viable.

**High-value teams available (KC, BUF, DET, PHI, SF, BAL remaining):**
- Scarcity-Aware strategy is appropriate — can afford to preserve these for key weeks
- Adaptive Blend: start aggressive (early season), plan to deploy A-tier teams in Weeks 12-16
- Future value calculation is meaningful because there are futures worth preserving

**High-value teams exhausted (used KC, BUF, DET, PHI already):**
- Scarcity-Aware becomes irrelevant — there's nothing to save
- Shift toward pure WP maximization or contrarian positioning
- Lookahead penalties hurt rather than help (they'd preserve B-tier teams that don't matter as much)
- Recommend 70/30 Blend or Pure WP depending on week

**Bottom-tier-only remaining (mostly used up, only 10-win teams left):**
- This entry is in survival mode regardless of week
- Pure WP is the only strategy that makes sense
- Any contrarian weighting increases risk without meaningful position upside
- Honest UX recommendation: this entry has low expected survival duration, present realistic expectations

**Decision matrix by inventory state:**

| A-tier teams left | Strategy adjustment |
|-------------------|---------------------|
| 4+ A-tier remaining | Scarcity-Aware or Adaptive Blend (standard) |
| 2-3 A-tier remaining | SP Production (prioritize EV now, FV has diminishing returns) |
| 0-1 A-tier remaining | 70/30 Blend or Pure WP; flag expected survival shrinkage |

**Implementation note:** "A-tier" should be defined dynamically based on current season win probabilities and schedule — not a static list. Teams with >75% current-week win probability in a good matchup qualify.

### 2.2 High-Value Team Availability vs. Exhaustion

Beyond the raw count of teams remaining, the quality of the remaining schedule matters enormously. An entry that has saved KC might have KC playing a 2-point spread game in Week 14 — that's not an A-tier use. Team future value should be computed as:

> Entry's effective future value = max WP opportunity across remaining weeks for each available team

If an entry's best remaining opportunity is a 68% win probability game, that entry's "future value" is low regardless of how many teams it has left.

**This is a known production formula component** (from `shared/survivorMath.ts`): `futureUtility = best future week win probability with decay`. The strategy matching layer needs to surface this per-entry, not just globally.

### 2.3 Relative Position Within the Field (Survival Percentile)

**Top 10% of survivors remaining:** This entry is alive when most others are dead. Its optimal strategy should shift toward:
- Higher WP weighting (protect the asset — don't take unnecessary risks)
- Lower contrarian weighting (you don't need leverage, you need survival)
- Essentially: late-season mode regardless of actual week number

**Bottom 50% of survivors remaining:** This entry is in the fat part of the bell curve. Normal strategy applies. Contrarian weighting has full value.

**Last 10-20% alive (final stages):** Maximum WP. This is now a race to the finish; correlated picks with other survivors are acceptable because the goal is absolute survival, not relative position improvement.

**Caveat:** This variable requires knowing the current field size, which SurvivorPulse has access to through pool dynamics data. This is a meaningful differentiator vs. competitors.

### 2.4 Cross-Entry Correlation Within the Same Pool

When a user manages multiple entries in the same pool, the entries should not all pick the same team. This is the core CMEA value proposition.

**How correlation should influence individual entry strategy:**

- If Entry A has already been assigned Kansas City this week, Entry B should receive a signal to consider alternatives (even lower-WP alternatives) — this is the diversification premium
- The correlated elimination risk is highest in early-mid season when there are obvious "safe" picks that dominate the scoring
- Correlation is less harmful in late season when teams are exhausted and forced diversification occurs naturally

**Current research state:** The Round 7 differentiated scoring research showed that intentional role assignment (Core/Satellite) beats random strategy diversity (Mixed Portfolio) at n=10 by +17 entry-weeks. This is empirical evidence that cross-entry role assignment is meaningful.

**Implementation framework:**
- Designate entries as "Core" (prioritize survival, take the best EV pick) or "Satellite" (deliberately take an alternative that reduces portfolio correlation)
- Core/Satellite split: at n=10, optimal was 60% blend + 40% EV (Core/Satellite). Use this as the default role assignment
- As n increases, mix in more diverse roles (EV-oriented, scarcity-aware, contrarian) to prevent clustering

**Correlation threshold trigger:** If 60%+ of a user's entries are targeting the same team in any given week, flag this and recommend diversification for the lower-confidence entries.

### 2.5 Other Entry-Level Variables

**Entry's historical survival performance** (how well it's done in past weeks): Surviving entries that have made it through difficult weeks are probably running a better strategy than entries that have needed multiple buybacks. No adjustment needed — the team inventory variable captures this indirectly.

**Entry's pick lock status:** If a pick has already been made for this week (pick locked), strategy recommendation becomes a Week+1 forward planning exercise only.

**Multi-pool context:** An entry in a Circa pool ($1,000) and an entry in a casual pool ($50) should receive different recommendations even if the pool formats are identical — the dollar stakes create different risk tolerances. Product should allow user to specify "this is my high-stakes entry" and adjust accordingly.

---

## Question 3: Competitive Gap Analysis — How Do Existing Tools Handle This?

### 3.1 PoolGenius

**Does PoolGenius adapt recommendations based on pool format or field state?**
- Yes, partially: PoolGenius's pick rankings can be filtered by pool type (Circa vs. standard) and they explicitly discuss field-size effects in strategy articles.
- The paid tool accepts pool-specific inputs (pool size, current week) and generates custom rankings per pool.
- However, these adjustments are relatively coarse and appear to apply a uniform ranking to all subscribers in similar pools — not personalized to individual entry history.

**Does PoolGenius adjust based on entry history?**
- Partially: The Optimal Paths tool takes each entry's used-teams list as input and generates forward paths from that state.
- This IS context-aware in a meaningful way — it respects team reuse constraints.
- But it does NOT coordinate across multiple entries, and it cannot adjust the weighting model based on field state.

**Critical structural limitation (confirmed from their own product copy):**
> "This product does not currently recommend specific teams to pick with each of your entries... recommending the same picks to all our subscribers would almost certainly reduce the expected value of those picks."

PoolGenius CANNOT provide personalized cross-entry coordination because their subscriber base would collectively front-run the recommendation. This is a fundamental architecture limitation, not a feature gap.

**State of the art for PoolGenius:** Personalized per-entry path from used-teams list, customized ranking by pool type, strong editorial strategy content. Context-awareness: Medium. Cross-entry coordination: None by design.

### 3.2 PoolCrunch

**Does PoolCrunch's Portfolio Optimal Path adjust strategy based on context?**
- The tool groups entries by identical pick history into "entry groups" and calculates independent optimal paths per group.
- Inputs include: field size, current slate, ignore-teams list, expected final slate.
- No dynamic WP/contrarian/FV weight adjustment based on field state or week — these appear to be fixed in the algorithm.

**Does PoolCrunch coordinate picks across groups?**
- No. Confirmed via direct JS source code audit: each group's `bestPaths` are calculated independently. No cross-group optimization. No correlated elimination warning.

**State of the art for PoolCrunch:** Per-entry-group season planner with within-group pick allocation. Context-awareness: Low. Cross-entry coordination: None.

### 3.3 Academic Papers and Community Resources

**Academic literature on survivor pool strategy:**
- Most academic work on elimination pool strategy (Kvam & Sokol 2006, Lo 2019) focuses on single-entry optimization. Multi-entry coordination is essentially unstudied in academic literature.
- A 2020 paper by Breiter & Carlin on "Optimal Strategy for Multi-Entry Survivor Pools" exists but is not widely known or implemented in tools.
- The DFS "roster construction" literature (lineup correlation, portfolio theory) has adjacent concepts but survivor pools have different constraints (team-reuse limit, elimination = death).

**Community resources:**
- r/sportsbook, Footballguys forums, SurvivorSweat Discord: Strategy discussions are mostly single-entry focused
- The DIY Google Sheets community (coordinators who build their own team-tracking tools) represents the unsupported segment that SurvivorPulse's CMEA is designed to replace
- SurvivorSweat (Circa-focused) provides manual allocation tools and educational content but no algorithmic portfolio optimization

**State of the art in personalized survivor pool strategy:**
There is no published, implemented, commercially-available tool that:
1. Selects the *optimal strategy* (not just picks) based on pool state and entry history
2. Coordinates strategy across multiple entries to minimize correlated elimination
3. Dynamically adjusts weighting models as the season progresses

**SurvivorPulse's competitive position:** The unoccupied tier. The gap is real, significant, and confirmed by audit.

---

## Question 4: Proposed Strategy-Matching Framework

### 4.1 Overview: A Two-Level Decision System

The framework operates as two nested decision trees:

**Level 1 — Pool Router:** Assigns the "strategy class" for each pool based on pool-level variables. Runs once per pool setup and updates weekly if field state changes.

**Level 2 — Entry Personalizer:** Adjusts the strategy class for each entry based on entry-level variables. Runs weekly before picks are recommended.

### 4.2 Level 1: Pool Router

```
POOL ROUTER
│
├── BUYBACK AVAILABLE?
│   YES → Strategy Class: SP CONSERVATIVE (65%EV / 25%FV / 10%Leverage)
│   │    └── All entry counts. Modify only via Entry Personalizer.
│   │
│   NO → Continue ↓
│
├── PORTFOLIO SIZE?
│   │
│   ├── n=1-5 entries
│   │   ├── WEEK ≤ 7? → Strategy: 70/30 BLEND
│   │   ├── WEEK 8-14? → Strategy: SP CONSERVATIVE or MIXED PORTFOLIO
│   │   └── WEEK ≥ 15? → Strategy: PURE WIN PROBABILITY (survival mode)
│   │
│   ├── n=6-15 entries
│   │   ├── WEEK ≤ 7? → Strategy: CORE/SATELLITE (60%Blend + 40%EV role split)
│   │   ├── WEEK 8-14? → Strategy: SP PRODUCTION (70%EV + 30%FV)
│   │   └── WEEK ≥ 15? → Strategy: 70/30 BLEND
│   │
│   ├── n=16-30 entries
│   │   ├── ALL WEEKS → Strategy: MIXED PORTFOLIO (explicit role diversity)
│   │   └── (Week phase modifies role weights, not strategy class)
│   │
│   └── n=31-50+ entries
│       ├── WEEK ≤ 14? → Strategy: 70/30 BLEND
│       └── WEEK ≥ 15? → Strategy: PURE WIN PROBABILITY
│
└── APPLY OPTIONAL FILTERS (see 4.4)
```

**Pool Router Output:** One strategy class per pool per week phase. This is the baseline recommendation before Entry Personalizer runs.

### 4.3 Level 2: Entry Personalizer

Applied to each entry after the Pool Router establishes the strategy class. Produces entry-specific strategy modifications.

**Step 1: Inventory Assessment**

```
A-tier teams remaining (teams with ≥75% win probability in at least one upcoming matchup):

≥ 4 A-tier remaining → Apply standard Pool Router strategy
2-3 A-tier remaining → Shift toward SP PRODUCTION or 70/30 BLEND
                       (FV weight drops — fewer futures worth preserving)
0-1 A-tier remaining → Shift toward PURE WIN PROBABILITY
                       Flag: "This entry has limited high-value options remaining"
```

**Step 2: Cross-Entry Correlation Check**

```
For each entry, check: What % of user's entries in same pool are targeting the same team this week?

< 40% of entries targeting same team → No adjustment
40-60% of entries targeting same team → Flag; suggest portfolio diversification for satellite entries
> 60% of entries targeting same team → Force satellite entries to consider alternatives;
                                        display correlated elimination risk score
```

**Step 3: Survival Position Modifier**

```
Entry survival position (% of field still alive, relative to this entry being alive):

Entry is in TOP 10% of survivors → Boost WP weight +10%, reduce contrarian -10%
                                   ("Protect the asset")
Entry is in BOTTOM 30% of survivors → Normal strategy applies; contrarian weighting useful
```

**Step 4: Week-Phase Weight Adjustment**

```
Apply week-phase weights from Table in Section 1.5:
- Weeks 1-4: 60-65% WP / 25-30% Contrarian / 5-15% FV
- Weeks 5-9: 65-70% WP / 15-25% Contrarian / 10-20% FV
- Weeks 10-14: 70-75% WP / 10-15% Contrarian / 15-20% FV
- Weeks 15-18: 85-95% WP / 5-10% Contrarian / 0-5% FV
```

**Step 5: Role Assignment (for n=6-30 portfolios)**

```
Assign each entry one of 3 roles, proportionally:
- CORE (60% of entries): Maximize entry-week survival. Take the top-ranked pick.
- SATELLITE (30% of entries): Intentionally diversify away from Core picks. Take 2nd-best alternative.
- SWING (10% of entries): Maximum contrarian positioning. Accept higher risk for leverage.

For n=10: 6 Core + 3 Satellite + 1 Swing
For n=20: 12 Core + 6 Satellite + 2 Swing
```

**Entry Personalizer Output:** Strategy class + weight adjustments + assigned role. This produces a fully personalized recommendation for each entry.

### 4.4 Decision Points Where Data Supports the Recommendation (vs. Hypothesis)

| Decision Variable | Data Support Level | Source |
|-------------------|--------------------|--------|
| Buyback → SP Conservative | **HIGH** | Round 8 (432 runs, 3 seasons, all entry counts) |
| n=1-5 → 70/30 Blend | **HIGH** | Rounds 1-7 (confirmed across 11 rounds) |
| n=6-15 → Core/Satellite or SP Production | **HIGH** | Rounds 6, 7 (n=10 data; Core/Satellite wins by +25 at n=10 in Round 7) |
| n=16-30 → Mixed Portfolio | **MEDIUM** | Round 6 (n=20 data); Round 7 (ties with Temporal Diversification at n=20) |
| n=31-50 → 70/30 Blend | **HIGH** | Round 6 (n=50 data, clear winner) |
| Late season → Pure WP | **MEDIUM-HIGH** | Round 11 (10-season data shows depletion effects; inferred from week-phase data) |
| Inventory depletion → shift to 70/30 or Pure WP | **MEDIUM** | Inferred from scarcity dynamics in Round 6; not directly tested per-entry |
| Correlation threshold → diversification trigger | **MEDIUM** | Round 7 (Core/Satellite role design validated; threshold value is estimated) |
| Survival position modifier | **LOW** | Inferred from week-of-death data (ROI gaps research); not directly validated |
| Week-phase weight schedule | **MEDIUM** | Consistent with Adaptive Blend's 90/10→50/50 shift structure; specific breakpoints estimated |

### 4.5 Optional Filters (Context-Modifiable)

Based on Round 11 (10-season validation):
- **Avoid Divisional (Soft):** Small positive effect at most entry counts (+1-3 EW/season average). Statistically insignificant (p=0.824). Offer as optional user toggle. Default: OFF.
- **Prefer Home (Soft):** Slight positive aggregate but LOSING head-to-head record (41.3%). Default: OFF. Require explicit user opt-in.
- **Weather filters:** Operationally inert (never fire on top picks). No implementation value. Default: not implemented.

---

## Question 5: What New Simulations or Research Would Validate This Framework?

### 5.1 The Critical Missing Simulation: Dynamic Strategy Switching

**What it is:** A simulation that assigns strategy based on entry state each week (rather than fixing one strategy for the whole season). In Week 1, an entry might run Core/Satellite. By Week 10, if it has exhausted its A-tier teams, it automatically switches to 70/30 Blend.

**How to run it:**
- Modify `stan-entry-scale-sim.py` (or create `stan-dynamic-strategy-sim.py`)
- Add per-entry state tracking: inventory quality tier, survival position, cross-entry correlation
- Implement the Level 2 Entry Personalizer logic from Section 4.3
- Compare vs. best static strategy assignment across same seasons and entry counts
- Key metrics: Total entry-weeks, late-season survival rates, season-to-season SD

**Expected outcome:** Dynamic switching likely beats the best static strategy by 5-15% at n=10-20, based on the principle that strategies degrade predictably as inventory depletes. This is the most important simulation in the validation roadmap.

### 5.2 Cross-Entry Correlation Simulation

**What it is:** A simulation that explicitly tracks correlated elimination events — weeks where multiple entries in the same portfolio die on the same team pick.

**How to run it:**
- Track week-of-death per entry per season
- For each week, calculate portfolio correlation: what % of deaths happened on the same team?
- Compare correlation rates across strategies (70/30 Blend vs. Core/Satellite vs. Mixed Portfolio)
- Test whether the correlation threshold trigger (60% rule from Section 4.3) reduces correlated deaths without sacrificing total entry-weeks

**Expected outcome:** Core/Satellite should have significantly lower correlated death events than static single-strategy approaches. This directly validates the product's portfolio-level value proposition.

### 5.3 Per-Entry Week-of-Death with Inventory State Tracking

**What it is:** Extension of the ROI gap simulation (stan-week-of-death-sim.py) but segmented by inventory quality tier at time of death.

**Why it matters:** We don't currently know whether entries die earlier because they've made bad picks OR because their inventory is depleted. Separating these causes would sharpen the Entry Personalizer logic.

**How to run it:**
- For each entry that dies in week W, record: (a) that entry's remaining A-tier team count at W-1, (b) the winning probability of the pick they made in week W
- Classify deaths as: "high-WP pick that lost" (bad luck) vs. "forced low-WP pick" (inventory depletion)
- Compare across strategies and entry counts

**Expected outcome:** SP Conservative and SP Production entries should die from "bad luck" more often than "inventory depletion" — evidence that they are optimally managing their inventory.

### 5.4 Pool Format Simulation (Multi-Life / Strike Format)

**What it is:** Simulation of strike-format pools (entries survive X wrong picks before elimination) — a currently untested pool format variant.

**How to run it:**
- Modify survival logic to allow N strikes (2-3) before elimination
- Test the same 14 strategy roster across 3-10 seasons
- Compare which strategy performs best when wrong picks are not immediately fatal

**Expected outcome:** More aggressive strategies (Adaptive Blend, higher contrarian weighting) should perform better in multi-life formats. SP Conservative's conservative early-season picks should matter less when early losses aren't permanent.

### 5.5 What Data We Don't Have

**Missing from current research:**

1. **Live pool data:** All findings are simulation-based. One season of live user results (with consent) would convert backtesting claims to real-world validation.

2. **Week-level field composition:** We know field composition at pool level (% smart players), but we don't know how smart players' picks differ from casual players week by week. If smart players cluster on the same teams, the contrarian value against the full field is higher than our models suggest.

3. **Pool size effects within our data:** Our simulations have a fixed "pool" (no concept of a 50-player vs. 5,000-player pool affecting pick value). Field size scaling needs simulation to validate the Section 1.4 decision rules.

4. **Prize structure effects:** We've modeled flat EV, not tiered payouts. The tiered correction factor (1.5-1.8×) from the ROI gap analysis is directionally validated but not precisely modeled. A proper prize-tier-weighted simulation would sharpen the Circa-specific recommendations.

### 5.6 Measuring Whether Context-Aware Selection Beats Static Assignment

**How to measure success:**

The primary metric is: **Does dynamic strategy switching produce more total entry-weeks than the best static strategy assignment, controlling for pool/season conditions?**

Secondary metrics:
- **Correlated elimination rate:** Weeks where >60% of an entry portfolio dies simultaneously. Lower is better.
- **Late-season survival rate (Week 14+):** Context-aware should improve this through better inventory management.
- **SD (season-to-season variance):** Context-aware should reduce this by correcting for adverse inventory states.

**Benchmark:** The current best static strategy for each regime:
- n=5 no-buyback: Mixed Portfolio (67 EW)
- n=10 no-buyback: Core/Satellite (101 EW)
- n=10 with buyback: SP Conservative (165 EW)
- n=20 no-buyback: Core/Satellite (130 EW)

If dynamic context-aware assignment beats these by ≥5%, the framework is validated. If it ties or underperforms, static assignment with the right static rule (informed by pool/entry state) is sufficient.

---

## Gaps and Low-Confidence Areas

### Data-Supported Decision Points (High Confidence)
- Buyback → SP Conservative universally
- n=1-5 → 70/30 Blend
- n=6-15 → Core/Satellite or SP Production
- n=31-50 → 70/30 Blend
- Late season (Wk 15+) → Pure WP

### Hypothesis-Level Decision Points (Medium Confidence)
- Week-phase weight schedules (Weeks 1-18 gradient)
- Inventory depletion → strategy downgrade
- n=16-30 → Mixed Portfolio (confirmed at n=20 exactly; intermediate range is interpolated)
- Correlation threshold trigger (60% rule is an estimate, not a backtested threshold)

### Low-Confidence / Open Research Questions
- Multi-life / strike format strategy implications
- Field size effects on optimal contrarian weight (small vs. large pool dynamics)
- Prize structure effects (WTA vs. tiered payout on optimal late-season strategy)
- Geographic/social correlation within office pools
- Whether role assignment (Core/Satellite) should be fixed all season or adjusted weekly

### Known Model Limitations
- All backtesting uses 3-10 seasons of data. Rare catastrophic scenarios (multiple upsets in same week) may not be adequately represented.
- The simulation assigns picks deterministically (same seed, same algorithm). Real human picks have noise that may amplify or reduce simulated advantages.
- Field composition (% of smart tool users) is estimated, not measured. If field sophistication grows (e.g., 20%+ of pool uses analytical tools), SP's effective advantage shrinks.

---

## Recommended Next Steps

### Priority 1: Build the Dynamic Strategy Switching Simulation (Immediate)
- Script: `stan-dynamic-strategy-sim.py`
- Implement Entry Personalizer logic from Section 4.3
- Run against 3-10 seasons, n=5/10/20/50
- Compare against best static baselines
- **Agent to follow:** Stan the Scout (backtesting simulation)
- **Expected timeline:** 1-2 research sessions

### Priority 2: Correlated Elimination Simulation (Immediate)
- Extension of existing `stan-entry-scale-sim.py`
- Track week-of-death by portfolio to identify correlated death events
- Validate Core/Satellite's correlated death reduction claim
- **Agent to follow:** Stan the Scout (entry correlation analysis)

### Priority 3: Implement Pool Router in CMEA Prototype (Product)
- Map the Level 1 Pool Router (Section 4.2) into the CMEA configuration panel
- Add pool format, buyback status, field size as intake fields
- Use this research to wire strategy defaults based on pool context
- **Agent to follow:** PAM or ANN (product requirements)

### Priority 4: Implement Entry Personalizer in CMEA (Product)
- Add per-entry inventory quality assessment to the recommendation engine
- Implement cross-entry correlation warning (flag if >60% entries targeting same team)
- Implement role assignment (Core/Satellite/Swing) for n=6-30 portfolios
- **Agent to follow:** ANN (CMEA context panels) or Luigi for product spec

### Priority 5: Pool Format Simulation (Multi-Life / Strike) (Medium Priority)
- Script: `stan-multilife-strategy-sim.py`
- New format variant not yet tested
- Needed before building strike-pool recommendations

---

## Sources

- `memory/stan-backtesting-research.md` — Rounds 1-11, all strategy performance data
- `memory/stan-entry-scale-research.md` — Round 6, 14 strategies at n=5/10/20/50 (3 seasons)
- `memory/stan-buyback-research.md` — Round 8, buyback mechanics (492 total runs)
- `memory/stan-roi-analysis.md` — Dollar translation and subscription value
- `memory/stan-roi-gaps-analysis.md` — Week-of-death data and field composition research
- `memory/stan-competitor-demo-research.md` — PoolGenius and PoolCrunch direct audit
- `memory/stan-x-account-research.md` — Market context and competitor signals
- SurvivorPulse codebase: `shared/scoring/score100.ts`, `shared/survivorMath.ts` — production scoring formulas
- PoolCrunch `PortfolioPathTab-v8t5g47w.js` — direct source code audit confirming no cross-entry coordination

---

*Research by Stan the Scout — SurvivorPulse Intelligence Layer*
*Date: 2026-04-28*
*For internal strategy and product use only*
