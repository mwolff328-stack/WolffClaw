# SurvivorPulse Competitive Moat Analysis

**Authors:** Stan the Scout + Pam the Product Owner
**Date:** 2026-04-28
**Purpose:** Identify competitive gaps Mike's 9 enhancement ideas do NOT cover, plus additional features to build a defensible moat.
**Priority:** P1 (SurvivorPulse)

---

## Part 1: Gaps Not Covered by Mike's 9 Items

Mike's 9 enhancements focus on: UX overhaul (#1), backtester integration (#2-3), ROI calculator (#4), entry/pool advisory (#5-6), multi-entry forecasting (#7), pool structure analysis (#8), and platform integration (#9). These are strong. But they leave the following competitive moat gaps uncovered.

---

### Gap 1: Buyback-Aware Strategy Engine
**Priority:** Critical Moat
**Protects against:** PoolGenius, PoolCrunch, DIY spreadsheets, new entrants

**The gap:** Mike's 9 items assume a single recommendation engine. But buyback pools fundamentally change the optimal strategy. SP Conservative 65/25/10 wins at ALL entry counts when buybacks are available, while it loses at all entry counts without them. At n=10 with Wk1-3 buyback, SP Conservative more than doubles performance (82 -> 165 entry-weeks). Neither PoolGenius nor PoolCrunch distinguishes between buyback and non-buyback pool types in their recommendations.

**Feature:** Pool-type-aware recommendation switching. When a user marks their pool as "buyback enabled" (with window size), the entire strategy engine shifts. The app should also always recommend exercising the buyback (positive ROI across every strategy and entry count tested, up to 4.15 EW/buyback at n=10).

**Research basis:** stan-buyback-research.md (492 runs, 12 strategies x 4 entry counts x 3 buyback configs). Winner changes at every entry count when buybacks are introduced.

---

### Gap 2: Portfolio Architecture Presets (Core/Satellite, Role-Based)
**Priority:** Critical Moat
**Protects against:** PoolGenius (subscriber dilution), PoolCrunch (per-group not cross-entry), DIY spreadsheets

**The gap:** Mike's items address entry optimization and forecasting but don't explicitly call out the portfolio architecture layer -- the research-proven framework where different entries serve different strategic roles. Core/Satellite at n=10 produces 101 entry-weeks vs 76 for 70/30 Blend (+33%), the largest single-strategy improvement found across all 11 research rounds. This is the product's deepest algorithmic moat.

**Feature:** Named portfolio architecture presets that users select (or auto-recommended based on entry count):
- **Balanced Core** (1-5 entries): All entries on 70/30 Blend
- **Core/Satellite** (6-15 entries): 60% blend core + 40% EV-maximizing satellites
- **Role Portfolio** (16-30 entries): 5-role diversification (safety, blend, contrarian, FV, EV)
- **Safety/Contrarian** (31+ entries): Two-bucket design, lowest efficiency decay at scale

Each preset visualizes the role assignment so users understand WHY entries differ.

**Research basis:** stan-differentiated-scoring-research.md (Round 7, 144 runs). Core/Satellite +25 vs 70/30 Blend at n=10, lowest variance (SD=1.7). stan-entry-scale-research.md confirms portfolio-size-aware strategy switching is essential.

---

### Gap 3: Correlated Elimination Risk Score (Real-Time)
**Priority:** Critical Moat
**Protects against:** PoolGenius, PoolCrunch, DIY spreadsheets, ALL competitors

**The gap:** From the competitor demo audit: "Neither PoolGenius nor PoolCrunch has... an interface that shows a serious 3-5 entry player how their entries relate to each other, explicitly flags correlated elimination risk, and delivers a coordinated pick slate with the rationale for why entries differ." Mike's #7 (Multi-Entry Forecasting) covers outcome projections, but not the live, per-week correlated risk metric.

**Feature:** A named, visible "Correlation Score" shown on the portfolio dashboard every week. Example: "Your entries are 23% correlated this week" (good) vs "Your entries are 87% correlated -- high risk" (bad). Contrast display against an uncoordinated baseline. This is an emotional, visceral feature -- the moment a player sees "87% correlated," they feel the danger.

**Research basis:** stan-competitor-demo-research.md (direct audit of both tools). pam-cmea-prototype-brief.md (Moment 2 design). PoolCrunch's Availability Correlation Table tracks the FIELD, not the user's personal portfolio. PoolGenius has nothing.

---

### Gap 4: Personalization Anti-Dilution Architecture (Marketing + Technical Moat)
**Priority:** Critical Moat
**Protects against:** PoolGenius specifically (their structural weakness)

**The gap:** PoolGenius explicitly admits they CANNOT do personalized multi-entry coordination: "This product does not currently recommend specific teams to pick with each of your entries... That's a slippery slope when multiple PoolGenius subscribers are using this product to compete in the same contest." This is an architecture-level weakness, not a feature gap. Mike's 9 items don't call out the need to build and market this structural advantage explicitly.

**Feature:** Two components:
1. **Technical:** Every recommendation is computed against the user's specific entry history, pool composition, and remaining team availability. No two users ever get the same recommendation. This already exists in the algorithm but needs to be made visible and marketable.
2. **Marketing:** Explicit competitive positioning: "Unlike tools that give 50,000 subscribers the same picks (collapsing EV for everyone), SurvivorPulse generates personalized recommendations for YOUR entries. Your strategy never dilutes."

**Research basis:** stan-competitor-demo-research.md (PoolGenius's own admission, verbatim quote). stan-x-account-research.md (market validation).

---

### Gap 5: Season Planning Visualization with Choke Point Alerts
**Priority:** Strong Differentiator
**Protects against:** PoolGenius (has basic season planner), PoolCrunch (future slate data only), DIY spreadsheets

**The gap:** Mike's items cover backtesting (#2-3) and pool structure (#8) but don't address the forward-looking season planning view with cross-entry awareness. Both competitors have basic season planners, but neither accounts for: (a) your specific entry history across all entries, (b) upcoming "choke weeks" where no obvious favorites exist, or (c) how your remaining team inventory maps to future matchup quality.

**Feature:** A visual season map showing:
- Weeks color-coded by difficulty (choke points in red)
- Per-entry team availability overlaid on the map
- Alerts: "Warning: Entries 3 and 7 will both need BUF in Week 14 -- only one can use it"
- Cross-entry team assignment planning for future weeks

This is the strategic planning layer that converts SurvivorPulse from a weekly pick tool into a season-long portfolio manager.

**Research basis:** stan-competitor-demo-research.md (both competitors have basic versions but none cross-entry). stan-backtesting-research.md (future value research, Rounds 4-5, shows FV matters more at higher entry counts).

---

### Gap 6: Live Season Scorecard / Results Transparency
**Priority:** Strong Differentiator
**Protects against:** All competitors (none publish live, auditable results)

**The gap:** All SurvivorPulse performance claims are simulation-based. PoolGenius claims "$7.1M+ in subscriber winnings since 2017" and "29% of subscribers win at least one pool prize per year." These are self-reported, aggregated, and unauditable. No competitor publishes live, week-by-week, verifiable strategy results. Mike's 9 items don't include a results transparency feature.

**Feature:** A public "Season Scorecard" that:
- Shows SurvivorPulse-recommended picks vs actual outcomes each week
- Tracks simulated portfolio performance in real-time against naive baseline
- Is fully auditable -- picks are published BEFORE game results
- Optionally includes anonymized, consented user results

This converts backtesting claims into live proof and builds trust that no competitor currently offers. Even 10 weeks of live data changes the credibility story from "backtested simulation" to "verified live results."

**Research basis:** stan-roi-analysis.md (Section 12: "No actual win-rate data from live pools -- all figures are simulated, not from real money results. Live validation is the key credibility unlock."). stan-roi-gaps-analysis.md (Section 4: "No live pool validation").

---

### Gap 7: Community Intelligence Layer (Opponent Modeling)
**Priority:** Strong Differentiator
**Protects against:** PoolCrunch (has basic opponent tracking), new entrants

**The gap:** PoolCrunch's strongest differentiation is opponent intelligence (opponent pick tracking, public pool analysis). Mike's 9 items don't include a community/opponent intelligence feature. While SurvivorPulse uses Yahoo pick popularity data, there's no explicit feature for understanding your specific pool's opponent behavior.

**Feature:** Pool-specific opponent modeling:
- Import opponent picks from supported platforms (Splash, Yahoo, ESPN)
- "Your pool is 40% chalk-heavy -- contrarian plays have higher EV here"
- Track opponent elimination patterns to estimate remaining field strength
- Pool dynamics dashboard: field size over time, elimination velocity, remaining competition quality

This is especially valuable for private pools where public pick data doesn't apply.

**Research basis:** stan-competitor-demo-research.md (PoolCrunch Availability Correlation Table, opponent tracking). stan-roi-gaps-analysis.md ("Field composition unknown -- what percentage of real survivor pool players use analytical tools?").

---

### Gap 8: Circa Survivor Specialization
**Priority:** Strong Differentiator
**Protects against:** SurvivorSweat (operational layer), PoolGenius (Circa-specific tools)

**The gap:** The Circa Survivor contest ($1,000/entry, 10-entry max, $15M+ prize pool) represents the highest-value ICP segment. Players there spend $1,000-$10,000 per season with zero coordination tooling. PoolGenius has Circa-specific articles and a Multi-Entry Survival Calculator (3-scenario comparison only). SurvivorSweat provides proxy/operational services but no portfolio strategy. Mike's items mention Splash integration (#9) but not Circa-specific features.

**Feature:** A dedicated "Circa Mode" with:
- Circa-specific pick popularity data (their weekly pick reveals are public)
- 10-entry max portfolio optimization (the exact sweet spot where Core/Satellite dominates)
- Circa prize structure modeling (tiered/split payouts, not WTA)
- Late-season survival premium calculations (SP entries past Week 14 at 2x naive rate in tiered pools = 1.5-1.8x dollar advantage amplification)
- Integration with SurvivorSweat for proxy pick submission

**Research basis:** stan-x-account-research.md (SurvivorSweat as Tier 1 partnership target, Circa community analysis). stan-roi-gaps-analysis.md (tiered payout correction: Circa estimate +$1,600-$2,000/season vs flat $1,077). stan-roi-analysis.md (Circa pricing supports $499/season Elite tier).

---

### Gap 9: Automated Strategy Switching by Season Phase
**Priority:** Nice to Have
**Protects against:** Sophisticated DIY players, new entrants

**The gap:** Research shows that optimal strategy weights shift across the season. SP's Adaptive Blend (90/10 early -> 50/50 late) is the overall n=10 winner across 5 seasons (144 EW). But this transition is hardcoded. Mike's items don't address dynamic, in-season strategy adaptation.

**Feature:** Automatic mid-season strategy rebalancing based on:
- Current elimination rate vs historical average
- Remaining team quality across entries
- Season phase (early/mid/late affects optimal WP/contrarian weighting)
- Entry health assessment: "3 of your 10 entries have depleted strong teams -- switching to conservative mode for those entries"

**Research basis:** stan-5season-backtesting.md (Adaptive Blend dominates at n=10 by adapting weights). stan-differentiated-scoring-research.md (Dynamic Rebalancing SD=0.5 at n=10 -- most consistent strategy, adjusts weights based on observed outcomes).

---

### Gap 10: Divisional Game Risk Toggle
**Priority:** Nice to Have
**Protects against:** DIY spreadsheets, PoolGenius (no filter options)

**The gap:** While Round 9 and Round 11 research showed divisional filters are statistically null at the aggregate level (p=0.824), there's a narrow use case: at n=20 with "Avoid Div Soft," some strategies gained +5-7 entry-weeks. This is a user-facing toggle, not a default. Neither competitor offers it.

**Feature:** Optional "Divisional Game Caution" toggle (off by default) with disclosure: "Historically, divisional games show similar upset rates to non-divisional games. This filter slightly deprioritizes divisional matchups as a tiebreaker for mid-size portfolios. Use at your own discretion."

**Research basis:** stan-game-context-research.md (Round 9), 10-season validation (Round 11). Net finding: not a default, but defensible as an optional user preference for the analytically curious.

---

### Gap 11: Content/Education Engine
**Priority:** Nice to Have (but high strategic value)
**Protects against:** PoolGenius (their content/SEO moat is their primary acquisition channel)

**The gap:** PoolGenius's #1 competitive advantage is not their tool -- it's their content. 15+ years of SEO-dominant strategy articles, media mentions (ESPN, WSJ, NYT), and a $7.1M performance claim. Mike's #3 (Automated Content System) is a 90-day priority, but it's not specifically mapped to SurvivorPulse content. None of Mike's 9 items address the educational content layer within the product itself.

**Feature:** In-app educational content that:
- Explains the "why" behind every recommendation ("This pick has 72% win probability but only 8% pick share -- if it wins, 92% of the field spent their pick on someone else")
- Publishes backtesting-derived strategy insights as blog/help content
- Creates a "Survivor Pool Academy" section with the research findings (entry scaling, portfolio architecture, buyback strategy)
- Uses the 5,100+ simulation runs as credibility fuel

**Research basis:** stan-competitor-demo-research.md (PoolGenius converts through authority/content, not demo). stan-backtesting-research.md (massive content asset potential identified). All research files contain "Content Asset Potential" sections with specific article titles.

---

## Part 2: Strengthening/Modifying Mike's 9 Items

### Item #4 (ROI Analysis) -- STRENGTHEN
The ROI calculator should incorporate both gap closures from stan-roi-gaps-analysis.md:
1. **Tiered payout correction:** For Circa/DK pools, late-season survival advantage amplifies dollar returns by 1.5-1.8x. The calculator should show both flat and tiered estimates.
2. **Field composition adjustment:** The calculator should let users estimate what % of their pool uses analytical tools, and adjust expected advantage accordingly (10-15% smart field -> ~9-10% SP advantage vs 10.77% against fully naive field).

### Item #5 (Pool & Entry Advisor) -- STRENGTHEN
Should integrate the buyback ROI finding: always recommend buyback exercise. SP Conservative at n=10 generates 4.15 entry-weeks per buyback used. The advisor should factor pool buyback rules into its entry count recommendation.

### Item #6 (Multi-Pool Optimization) -- STRENGTHEN
Cross-pool optimization should account for team overlap across pools. If a user is in a Circa pool AND a DK pool AND a private pool, their team usage is shared across all three. No competitor tracks cross-pool team coordination.

### Item #8 (Pool Structure Analysis) -- STRENGTHEN
Should explicitly model rake impact. Stan's research shows SP at n=10 in a 10% rake pool shifts entry ROI from -$10/entry (naive) to approximately break-even. In 15% rake pools, positive EV requires n=35+. Users should see: "This pool's rake means you need X entries to be +EV."

---

## Part 3: Priority Ranking

### Critical Moat (must build to be defensible)
1. **Buyback-Aware Strategy Engine** -- Complete strategy shift based on pool type. Neither competitor does this.
2. **Portfolio Architecture Presets** -- The algorithmic core. +33% improvement at n=10 with Core/Satellite.
3. **Correlated Elimination Risk Score** -- The emotional hook that no competitor has. Makes the invisible visible.
4. **Personalization Anti-Dilution** -- Not a feature to build, but a positioning/marketing asset to weaponize. PoolGenius structurally cannot compete here.

### Strong Differentiator (builds significant advantage)
5. **Season Planning with Choke Point Alerts** -- Converts weekly tool into season-long manager.
6. **Live Season Scorecard** -- The single biggest credibility unlock. Converts simulation claims to proof.
7. **Community Intelligence / Opponent Modeling** -- Fills the gap PoolCrunch partly owns.
8. **Circa Survivor Specialization** -- Targets the highest-value ICP segment directly.

### Nice to Have (incremental advantage)
9. **Automated Strategy Switching by Phase** -- Sophisticated, research-backed, but complex to implement.
10. **Divisional Game Risk Toggle** -- Minimal impact, but signals analytical depth.
11. **Content/Education Engine** -- High strategic value for acquisition, but not a product moat per se.

---

## Part 4: Competitive Protection Matrix

| Feature | vs PoolGenius | vs PoolCrunch | vs DIY Spreadsheets | vs New Entrants |
|---------|--------------|---------------|--------------------|-----------------| 
| Buyback-Aware Engine | Yes | Yes | Yes | Yes |
| Portfolio Architecture | Yes (structural) | Yes (structural) | Yes | Yes |
| Correlation Risk Score | Yes | Yes | Yes | Yes |
| Anti-Dilution Positioning | Yes (their weakness) | Partial | N/A | Yes |
| Season Planning + Choke Points | Partial (they have basic) | Partial | Yes | Yes |
| Live Scorecard | Yes | Yes | Yes | Yes |
| Opponent Modeling | Yes | Partial (they have basic) | Yes | Partial |
| Circa Specialization | Partial (they have articles) | Yes | Yes | Yes |
| Strategy Phase Switching | Yes | Yes | Yes | Partial |
| Div Game Toggle | Yes | Yes | Yes | Partial |
| Content Engine | Partial (they own SEO) | Yes | N/A | Yes |

---

## Summary

Mike's 9 items are focused on UX, analytics integration, and platform expansion -- all necessary for a viable product. The gaps identified here form a second layer: the **strategic intelligence moat** that makes SurvivorPulse structurally harder to replicate.

The critical four (Buyback Engine, Portfolio Architecture, Correlation Score, Anti-Dilution) are not features competitors can bolt on. They require the entire recommendation engine to be built differently from the ground up -- which SurvivorPulse already has. The job now is to surface that advantage in the product and marketing.

PoolGenius's moat is content/SEO. PoolCrunch's moat is data/operations. SurvivorPulse's moat must be **personalized portfolio intelligence** -- the only tool that treats your entries as a coordinated portfolio, adapts to your pool type, and never dilutes your edge by giving the same advice to everyone.

---

*Analysis by Stan the Scout (Intelligence) and Pam the Product Owner (Product Strategy)*
*Research basis: 11 research files, ~5,100 simulation runs, 2 competitor audits, 17 X account profiles*
