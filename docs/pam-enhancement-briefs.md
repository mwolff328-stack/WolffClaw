# SurvivorPulse Enhancement Briefs

**Author:** Pam the Product Owner
**Date:** April 28, 2026
**Version:** 1.1
**Last updated:** April 29, 2026
**Context:** 9 major enhancements evaluated against the V1 launch target of September 4, 2026 (NFL Week 1)
**Changelog:** v1.1 -- Updated #1 (IA Overhaul) with founder feedback on historical data access, week-by-week navigation, eliminated entity access, and season selection. Added cross-reference note to #7 (Multi-Entry Forecasting).
**Companion docs:** `survivorpulse-product-dev-plan-2026.md`, `memory/stan-roi-analysis.md`, `memory/stan-roi-gaps-analysis.md`

---

## Table of Contents

1. [Information Architecture Overhaul](#1-information-architecture-overhaul)
2. [Design System Unification](#2-design-system-unification)
3. [Back Tester Integration](#3-back-tester-integration)
4. [ROI Analysis Feature](#4-roi-analysis-feature)
5. [Pool & Entry Advisor](#5-pool--entry-advisor)
6. [Multi-Pool Optimization](#6-multi-pool-optimization)
7. [Multi-Entry Forecasting](#7-multi-entry-forecasting)
8. [Pool Structure Analysis](#8-pool-structure-analysis)
9. [Platform Integration (Splash Sports etc.)](#9-platform-integration-splash-sports-etc)
10. [Dependency Graph](#dependency-graph)
11. [Recommended Build Sequence](#recommended-build-sequence)
12. [Risk Assessment](#risk-assessment)

---

## 1. Information Architecture Overhaul

**Priority:** P1

**Problem being solved:**
The current IA was built incrementally as features were added. Users face two core workflows -- (a) managing entries/picks across pools, and (b) accessing analysis/recommendations to inform those picks -- but the navigation doesn't reflect this mental model. As more features ship (back tester, ROI calculator, pool advisor), the existing structure will become increasingly confusing. This needs to be solved before adding new features, not after.

Additionally, the current IA has no clear path for viewing or editing historical data. Users cannot navigate to eliminated pools or entries, access previous weeks' pick data in temporal context, or switch between seasons. There is no week-by-week navigation, no way to scope data to a specific point in time, and no mechanism to view or manage entries after elimination. These are core workflows for any serious survivor pool player managing data across weeks and seasons.

**Target user:**
All SurvivorPulse users, from single-pool casuals to multi-pool power users running 10-50 entries across multiple pools.

**Proposed solution (high level):**
Redesign the app's top-level navigation and page hierarchy around two primary modes:
- **My Pools & Entries** -- the management hub. Create pools, add entries, make picks, track status, view elimination state. Everything about "what I'm doing."
- **Analysis & Tools** -- the intelligence hub. Recommendations engine, back tester, ROI calculator, pool advisor, pick analytics. Everything about "what should I do."

A persistent context bar shows the user's active pool/entry selection so analysis tools can be applied to specific pools without navigating away. Dashboard/home screen provides a glanceable summary of both modes.

Critical additions based on founder feedback:
- **Week-by-week navigation:** A global week selector scopes all views to the selected week's data and prior weeks only. Users see entry status, picks, recommendations, and portfolio state as of that week. Subsequent week data is excluded from the view. However, if a user edits historical data (e.g., changes a past pick), the change propagates forward to all subsequent weeks.
- **Eliminated entity access:** Pools and entries remain fully accessible after elimination. They are visually distinguished (dimmed, badge, strikethrough, or similar treatment) but never hidden or disabled. Users can view and edit all data for eliminated pools and entries.
- **Season selector:** A season selector in the navigation allows users to switch between current and previous seasons. Loading a past season shows that season's pools, entries, picks, and results.
- **Pool-level historical data view:** Each pool has a dedicated view for managing historical data: alive/eliminated entries, pick history per entry, pool-level stats, and weekly results. This is the answer to "where do I see and update my pool's historical data."

**MVP scope:**
- Audit current page inventory and user flows
- Define new top-level navigation structure (2-3 primary sections max)
- Wireframe key screens: dashboard, pool management hub, analysis hub
- Implement new navigation shell and re-route existing pages into it
- Add persistent pool/entry context selector
- Redirect or deprecate old routes
- **Week-by-week navigation** with global week selector that scopes all data views to selected week and prior weeks only
- **Eliminated pool/entry access and editing** -- eliminated entities remain fully interactive, visually distinguished but not hidden or disabled
- **Season selector** in navigation allowing users to switch between current and historical seasons
- **Pool-level historical data management view** showing alive/eliminated entries, pick history, and pool data per pool

**Out of scope (for this release):**
- New features (those are separate briefs)
- Mobile-specific responsive redesign (follow desktop-first, ensure it works on mobile)
- User research/testing with external users (use founder judgment + competitor analysis)
- Onboarding flow redesign (handle separately post-launch)
- Cross-season analytics or season comparison tools
- Bulk data migration between seasons
- Automated historical data reconciliation with external platforms

**Success metrics:**
- Users can reach any existing feature in 2 clicks or fewer from dashboard
- Zero orphan pages or dead-end navigation states
- New features (back tester, ROI calc, advisor) have an obvious home in the IA before they're built
- Founder confirms the structure "makes sense" in a walkthrough
- Users can access any previous week's data within 2 clicks from the current view
- Eliminated pools and entries remain fully viewable and editable (no functionality removed on elimination)
- Season switching loads the correct historical context with all associated pools, entries, and picks
- Week selector correctly scopes data: selected week and prior only, with no data leakage from subsequent weeks

**Dependencies:**
- None. This is foundational and should be done first.
- Informs where enhancements #2-9 live in the app.

**Deadline/timing constraint:**
Must be complete before Back Tester Integration (#3) and ROI Analysis (#4) begin frontend work. Target: design complete by June 15, implementation complete by July 15.

**Open questions:**
- Should "My Pools" and "Analysis" be tabs, sidebar sections, or separate top-level pages?
- How does the pool context selector work when a user has 5+ pools with 10 entries each? Needs a compact, scannable pattern.
- Do we need a dedicated "Settings/Account" section in the top nav, or is it fine as a profile menu item?
- What is the right dashboard density? Glanceable summary vs detailed status?
- How far back should season history go? All seasons in the system, or limit to the last 3?
- Should historical week views be read-only by default with an explicit "edit" toggle, or always editable?
- When a user edits a past week's pick, how does that affect recommendations in subsequent weeks? Recalculate on-demand, batch recalculate, or flag as stale?

**V1 Pre-Launch vs Post-Launch:** **V1 Pre-Launch (required)**
Without this, every new feature added makes the app harder to use. The IA is the skeleton that everything else hangs on. Shipping new features into a broken IA creates more UX debt than it solves. Do this first.

---

## 2. Design System Unification

**Priority:** P1

**Problem being solved:**
The main SurvivorPulse app and the Back Tester prototype have divergent visual languages. The Back Tester has a polished, modern design system (dark theme, Inter Variable + JetBrains Mono, indigo-violet brand palette, IBM Carbon-inspired status tokens) that tested well with users. The main app looks different, creating a fragmented brand experience. As the Back Tester gets integrated (#3), the visual mismatch becomes a product-quality problem.

**Target user:**
All users. Design consistency builds trust, especially for a paid product handling financial decisions.

**Proposed solution (high level):**
Extract the Back Tester's design system (documented in DESIGN.md in the SurvivorPulse-BackTesting-Prototype repo) into a shared design token/component library. Apply it to the main SurvivorPulse app. This includes:
- Color palette (dark theme primary, indigo-violet brand)
- Typography (Inter Variable for UI, JetBrains Mono for data/numbers)
- Component patterns (cards, buttons, inputs, status indicators using IBM Carbon tokens)
- Spacing, elevation, and motion conventions
- Data visualization style (charts, gauges, heatmaps)

**MVP scope:**
- Extract design tokens from Back Tester DESIGN.md into a shared config (Tailwind theme extension or CSS custom properties)
- Apply dark theme and typography to main app shell (nav, layout, backgrounds)
- Restyle core UI components: buttons, cards, inputs, selects, tables, modals
- Restyle data display components: score cards, recommendation panels, analytics views
- Apply status token system (IBM Carbon: green/yellow/red/blue) to all status indicators
- Ensure shadcn/ui components are themed consistently

**Out of scope (for this release):**
- New component creation (only restyle existing ones)
- Animation/motion system beyond basic transitions
- Design system documentation site (internal Storybook etc.)
- Marketing site design (that's SPP-58, separate track)

**Success metrics:**
- Visual parity between main app and Back Tester -- a user moving between them sees one product, not two
- All color values, font stacks, and spacing values come from shared tokens (no hardcoded one-offs)
- Dark theme renders correctly across all existing pages
- Passes WCAG AA contrast requirements on all text elements

**Dependencies:**
- Best done alongside or immediately after IA Overhaul (#1), since restructured pages need restyling anyway
- Back Tester DESIGN.md must be reviewed and confirmed as the canonical source

**Deadline/timing constraint:**
Core restyling should be complete before Back Tester Integration (#3) ships, so the integrated experience is visually coherent. Target: July 31.

**Open questions:**
- Does the dark theme work for all data visualization types currently in the main app, or do some charts need redesigned color palettes?
- Should we support a light theme toggle, or commit to dark-only for V1?
- How much of the shadcn/ui component library needs custom theming vs works out of the box with Tailwind config changes?

**V1 Pre-Launch vs Post-Launch:** **V1 Pre-Launch (required)**
A paid product with inconsistent design erodes trust. This is especially critical because the Back Tester (which has the good design) is the primary marketing/conversion tool. Users who convert from the Back Tester and land in a visually different main app will feel a quality drop. Unacceptable for a product charging $79-$499/season.

---

## 3. Back Tester Integration

**Priority:** P1

**Problem being solved:**
The Back Tester is currently a standalone app at a separate URL (survivorpulse-backtester-prototype.replit.app). It's the strongest conversion tool SP has -- 5 seasons of data, 7+ strategies, optimization engine, interactive tutorial. But it's disconnected from the main product. Users who love the Back Tester have no seamless path into the paid product. And paying users can't access backtesting within their workflow.

**Target user:**
- Prospective users evaluating SP (conversion funnel)
- Paying subscribers who want to backtest strategies before applying them to live pools

**Proposed solution (high level):**
Bring the Back Tester into the main SurvivorPulse app as a first-class feature under the Analysis & Tools section (per IA redesign). Two modes:
- **Free/gated mode:** The current access-gated experience (SURVIVOR2026 code, name/email capture) becomes the primary free trial funnel. Lives at a public route like `/backtester` or `/tools/backtester`.
- **Subscriber mode:** Full access without gates. Connected to the user's actual pool configurations -- backtest using your real pool parameters (entry count, buyback rules, etc.) instead of generic settings.

**MVP scope:**
- Port Back Tester React components into the main app codebase
- Integrate with shared design system tokens (#2)
- Place within IA structure (#1) under Analysis & Tools
- Maintain existing functionality: 5 seasons, 7+ strategies, configurable weights, 1-50 entries, buyback toggle, "Find Best Strategy," performance visualization
- Preserve the 17-step tutorial and feedback system
- Free users: gated access (email capture), limited to preset configurations
- Subscribers: full access, ability to load pool parameters from their actual pools
- Shared database: Back Tester uses the same historical data already in the production DB (confirmed -- 5 seasons loaded)

**Out of scope (for this release):**
- New strategy types beyond the existing 7+
- Adding 2026 season data to backtester (that's a data pipeline task)
- Custom strategy builder (users define their own weight blends)
- Backtester API for programmatic access
- A/B testing different gating strategies

**Success metrics:**
- Back Tester is accessible within the main app at a permanent route
- Free users complete email capture at >= current conversion rate
- Subscribers can load their pool parameters into backtester within 2 clicks
- Page load time for backtester within main app is within 500ms of standalone version
- Tutorial and feedback systems function identically

**Dependencies:**
- IA Overhaul (#1) -- needs to know where the Back Tester lives in navigation
- Design System Unification (#2) -- Back Tester components should use shared tokens (though they already have the right design, so this is more about the surrounding shell)
- Historical data already in production DB (confirmed available)

**Deadline/timing constraint:**
Should ship before the pre-season marketing push (Phase 3, July 1). The Back Tester is a key conversion tool -- it needs to be inside the product before heavy marketing drives traffic. Target: July 15.

**Open questions:**
- Should the standalone Back Tester URL redirect to the main app, or remain as a separate entry point?
- How do we handle existing users who bookmarked the standalone URL?
- What pool parameters should auto-populate from subscriber pool configs? (Entry count, buyback, pool size?)
- Should free-tier backtester access be time-limited or feature-limited?

**V1 Pre-Launch vs Post-Launch:** **V1 Pre-Launch (required)**
The Back Tester is SP's best acquisition tool. It must be inside the product before the marketing push hits. A disconnected standalone app that doesn't lead into the paid product is a leaky funnel. This directly impacts revenue.

---

## 4. ROI Analysis Feature

**Priority:** P1

**Problem being solved:**
Users considering SP need to answer: "Will this tool pay for itself?" Right now, that requires them to do their own math. Stan's ROI research (stan-roi-analysis.md) proves the answer is definitively yes for most pool types, but the data is locked in internal research docs. A live calculator turns that research into a self-serve sales tool that closes the value question before the user even talks to us.

**Target user:**
- Prospective users evaluating whether SP is worth the subscription cost
- Existing subscribers validating their decision or optimizing their pool portfolio

**Proposed solution (high level):**
A live ROI calculator. User inputs their pool parameters, and the tool outputs expected SP advantage, dollar surplus, and subscription payback analysis.

**Inputs:**
- Pool size (number of players)
- Entry fee
- Number of entries the user plans to run
- Rake percentage (0% for private, user enters for platform pools)
- Buyback enabled? (yes/no, and if yes, which weeks)
- Prize structure (WTA, top-3 split, tiered)

**Outputs:**
- Expected SP survival advantage (%) at their entry count
- Expected dollar surplus per season vs naive play
- Subscription payback period (how many seasons to recoup sub cost, typically <1)
- Break-even entry count for raked pools
- Comparison table: naive vs SP expected returns
- Confidence range (best/median/worst season from 5-year data)

**MVP scope:**
- Input form with the 6 parameters above
- Calculation engine using Stan's lookup tables (Section 8 of ROI analysis) and interpolation for entry counts between tested values (5, 10, 20, 50)
- Results display: dollar surplus, ROI %, subscription payback, confidence range
- Preset pool profiles (Circa, DraftKings Main, typical $100 private pool) for one-click scenarios
- "Share your ROI" -- generate a shareable summary link or image
- Place within Analysis & Tools section per IA

**Out of scope (for this release):**
- Live connection to user's actual pool outcomes
- Multi-pool aggregate ROI (that's Pool & Entry Advisor, #5)
- Custom strategy selection (calculator uses "best SP strategy" for given entry count)
- Tiered payout precision modeling (use approximate correction factors from gaps analysis)
- Monte Carlo simulation (use lookup table interpolation instead)

**Success metrics:**
- Users who interact with ROI calculator convert to paid at 2x+ the rate of non-interactors
- Calculator results match Stan's research figures within 5% tolerance
- Average time to complete a calculation: <30 seconds
- Preset pool profiles used by 50%+ of calculator users (validates they lower friction)

**Dependencies:**
- Stan's ROI research (stan-roi-analysis.md) -- completed, data available
- Stan's gaps analysis (stan-roi-gaps-analysis.md) -- completed, tiered correction factors available
- IA Overhaul (#1) -- needs a home in navigation
- No dependency on Back Tester Integration (#3) or Design System (#2), though should use shared tokens

**Deadline/timing constraint:**
High-value conversion tool. Should be live before the pre-season push begins. Target: July 15. Can ship as a standalone page even if IA overhaul is still in progress.

**Open questions:**
- Should the ROI calculator be available to free users (as a sales tool) or gated behind subscription?
  - **Recommendation:** Free. This is a sales tool. Gating it defeats the purpose.
- How do we handle the 2/5 seasons where SP underperforms? Show full confidence range, or just the average?
  - **Recommendation:** Show full range. Transparency builds trust. "SP wins 3 of 5 seasons, with a strong positive average" is honest and still compelling.
- Should we show competitor comparison (SP vs PoolGenius expected returns)?
  - **Recommendation:** No. We don't have reliable data on competitor performance, and comparative claims invite legal scrutiny.
- Field composition adjustment: Should we let users input "how sophisticated is your pool?" or use defaults?
  - **Recommendation:** Use smart defaults based on pool type (private = 2-5% smart field, DK = 10%, Circa = 15%). Advanced toggle for users who want to adjust.

**V1 Pre-Launch vs Post-Launch:** **V1 Pre-Launch (strongly recommended)**
This is the single highest-impact conversion tool after the Back Tester. It answers the #1 objection ("Is it worth the money?") with personalized, data-backed math. Every day this isn't live during the marketing push is lost conversions.

---

## 5. Pool & Entry Advisor

**Priority:** P2

**Problem being solved:**
Users in multiple pools face a non-obvious optimization problem: given a fixed budget, how many entries should they run in each pool? A $100 WTA no-rake pool with 50 players has very different ROI math than a DraftKings $100 pool with 18,000 entries and 15% rake. Users either spread too thin (too many entries in bad pools) or concentrate too much (miss diversification across pool types). Stan's research shows SP's advantage grows with entry count, but there's a practical budget constraint.

**Target user:**
Multi-pool power users. The core ICP who plays in 2-5 pools simultaneously with 10-50 total entries across them.

**Proposed solution (high level):**
An advisory tool that takes the user's budget and available pools, then recommends optimal entry allocation. Builds on ROI Analysis (#4) by applying it across a portfolio of pools rather than a single pool.

**Inputs:**
- Total budget for the season
- List of pools the user is considering (each with: entry fee, size, rake, buyback, prize structure)
- Or: pool presets (Circa, DK Main, DK Mini, private WTA)

**Outputs:**
- Recommended number of entries per pool
- Expected total surplus across all pools
- Comparison: user's current allocation vs recommended allocation
- Marginal value of the next entry in each pool (helps decide where the next dollar goes)
- Warning flags for pools where the user is likely -EV even with SP

**MVP scope:**
- Input form for budget + pool list (manual entry or presets)
- Allocation algorithm using ROI lookup tables and marginal analysis
- Results: recommended entries per pool, total expected surplus, comparison view
- "Add another pool" flow for users discovering new pool opportunities

**Out of scope (for this release):**
- Automatic pool discovery (finding pools the user doesn't know about)
- Real-time odds integration for pool-specific recommendations
- Multi-season optimization (optimizing across a 3-year horizon)
- Social features (see what other SP users are entering)

**Success metrics:**
- Users who use the advisor enter 20%+ more total entries than users who don't (indicating they found pools worth entering)
- Advisor recommendations align with Stan's ROI model within 5%
- Average session time with advisor: 2-5 minutes (engaged but not frustrated)

**Dependencies:**
- ROI Analysis (#4) -- the advisor is essentially multi-pool ROI analysis. Cannot build without the ROI calculation engine.
- Pool Structure Analysis (#8) -- the advisor needs to understand how pool parameters affect strategy. Can ship MVP without #8 by using simplified heuristics, but full version needs it.
- IA Overhaul (#1) -- needs a home in the Analysis & Tools section

**Deadline/timing constraint:**
Nice-to-have for V1 launch but not blocking. If ROI Analysis (#4) ships by July 15, this could ship by August 15 in MVP form. More likely a strong post-launch feature for the first update cycle.

**Open questions:**
- How do we handle correlation between pools? (If two pools have overlapping field composition, entries in both are less diversified than the tool implies.)
- Should the advisor recommend specific strategies per pool, or just entry counts?
  - **Recommendation for MVP:** Entry counts only. Strategy recommendation is Multi-Entry Forecasting (#7).
- How do we validate the advisor's recommendations without live season data?

**V1 Pre-Launch vs Post-Launch:** **Post-Launch (V1.1)**
The ROI calculator (#4) handles the single-pool value question. Multi-pool optimization is a power-user feature that can ship in the first post-launch update. Trying to ship both by September 4 risks both being half-baked.

---

## 6. Multi-Pool Optimization

**Priority:** P2

**Problem being solved:**
Different pools have different rules (buyback vs not, different field sizes, different prize structures, WTA vs tiered). Optimal strategy changes based on these parameters. A user running 10 entries in a no-buyback WTA pool and 10 entries in a buyback tiered pool should NOT use the same strategy for both. Currently, SP doesn't differentiate recommendations by pool structure.

**Target user:**
Power users in 2+ pools with different rule sets. Circa players who also play DraftKings. Users in both private and platform pools.

**Proposed solution (high level):**
Extend the recommendation engine to accept pool-specific parameters and produce pool-specific strategy recommendations. Each pool the user creates gets strategy weights optimized for that pool's structure. Cross-pool coordination ensures the user's total portfolio is diversified, not just each individual pool.

**MVP scope:**
- Pool parameter capture: buyback rules, prize structure (WTA/tiered), field size, rake
- Per-pool strategy weight recommendations based on pool parameters
- Cross-pool entry correlation analysis: flag when entries across pools are picking the same teams (reducing diversification)
- Dashboard view showing per-pool and aggregate portfolio health

**Out of scope (for this release):**
- Automatic rule detection from platform integration (#9)
- Real-time adjustment during the season based on field behavior
- Game-theoretic modeling (adjusting based on what other smart players are doing)

**Success metrics:**
- Users with 2+ pools receive differentiated strategy recommendations per pool
- Cross-pool correlation alerts fire when >50% of entries across pools share the same pick in a given week
- Users who use cross-pool coordination have higher aggregate entry-weeks than users who don't

**Dependencies:**
- Pool Structure Analysis (#8) -- this is the research foundation. Without understanding how pool parameters change optimal strategy, multi-pool optimization is guesswork.
- ROI Analysis (#4) -- needed for the value-per-pool calculation that drives allocation
- Pool & Entry Advisor (#5) -- closely related; the advisor says "how many entries" and this says "what strategy for each"
- Existing Pool Dynamics Engine and Portfolio Diversification Mode (already built)

**Deadline/timing constraint:**
Requires research (#8) to be completed first. Not feasible for V1 launch unless Pool Structure Analysis is fast-tracked. Realistic target: V1.1 or V1.2 (October-November 2026, mid-season update).

**Open questions:**
- How much does optimal strategy actually change between pool types? Stan's research shows buyback amplifies SP Conservative's edge, but we need more granular data on field size impact and prize structure impact.
- Is cross-pool coordination computationally feasible at 50+ total entries across 5 pools? (Combinatorial complexity concern.)
- Should this be automatic (SP just does it) or advisory (SP recommends, user decides)?

**V1 Pre-Launch vs Post-Launch:** **Post-Launch (V1.2)**
This requires Pool Structure Analysis (#8) as a prerequisite, which itself is research-heavy. Even if the research is done by launch, the engineering to implement per-pool optimization is significant. Ship the recommendation engine with pool-agnostic optimization for V1; add pool-specific tuning post-launch when the research is solid.

---

## 7. Multi-Entry Forecasting

**Priority:** P2

**Problem being solved:**
Users running multiple entries want to answer: "If I follow SP's recommendations this week, what are the likely outcomes for my portfolio?" Currently, SP recommends picks but doesn't show projected scenarios. A user with 10 entries has no way to see: "If I pick Team A on 6 entries and Team B on 4 entries, what's my expected survival distribution after this week? What about after 3 weeks?"

**Target user:**
Multi-entry users (10+ entries) who want to understand the risk profile of their portfolio before committing picks.

**Proposed solution (high level):**
A scenario modeling tool that takes the user's current entries, proposed picks, and outputs probability distributions for portfolio outcomes. Shows: expected entries surviving, worst-case scenarios, best-case scenarios, and comparison between different pick allocations.

**Inputs:**
- User's current entry portfolio (which entries are alive, what teams have been used)
- Proposed pick allocation for the current week (which team on which entries)
- Optional: projected picks for 2-3 weeks ahead

**Outputs:**
- Expected entries surviving after this week (distribution, not just point estimate)
- Portfolio risk visualization: correlation map showing which entries live/die together
- Scenario comparison: "Pick A on 6, Pick B on 4" vs "Pick A on 5, Pick B on 3, Pick C on 2"
- Multi-week projection: if you follow SP's path for the next 3 weeks, expected portfolio state

**MVP scope:**
- Single-week forecast: input proposed picks, see survival probability distribution
- Portfolio correlation view: which entries are correlated (same pick = correlated fate)
- Side-by-side scenario comparison (2 scenarios)
- Based on existing win probability data + SP's scoring model

**Out of scope (for this release):**
- Full-season simulation (computationally expensive, diminishing accuracy beyond 3-4 weeks)
- Field-aware modeling (adjusting for what other players might pick)
- Real-time odds movement integration during the pick window
- Automated "best scenario" optimization (that's the existing recommendation engine's job)

> **Note (cross-reference #1 IA Overhaul):** The week-by-week navigation added in #1 directly affects how users access forecasting for previous weeks. When a user navigates to a past week via the global week selector, the forecasting view should show the forecast as it existed at that point in time (picks proposed, survival projections based on data available that week). If historical picks are edited via #1's temporal editing feature, forecasting should reflect the updated data on-demand. Coordinate with #1's temporal scoping rules during implementation.

**Success metrics:**
- Users who use forecasting before committing picks have 10%+ higher week-over-week survival rate
- Average scenario comparisons per user per week: 2-3 (indicates engagement without decision paralysis)
- Forecasted survival probabilities match actual outcomes within 15% tolerance over a full season

**Dependencies:**
- Existing recommendation engine and win probability data (built)
- Pool Dynamics Engine (built -- needed for field survival estimates)
- Portfolio Diversification Mode (built -- provides correlation logic)
- No hard dependency on other enhancements, though IA Overhaul (#1) determines where it lives

**Deadline/timing constraint:**
Valuable during the live season. Does NOT need to be ready for launch -- it only becomes relevant once picks are being made (Week 1+). Could ship as a Week 2-3 update. Target: September 15-30 (early-season update).

**Open questions:**
- How far ahead is multi-week forecasting useful? Beyond 2-3 weeks, prediction accuracy degrades significantly.
- Should forecasting show dollar-value-at-risk (connecting to ROI data), or just survival probabilities?
  - **Recommendation:** Both. Show survival probability as the primary metric, with optional dollar overlay for users who've configured their pool's prize info.
- How do we visualize 10-50 entry scenarios without overwhelming the UI?

**V1 Pre-Launch vs Post-Launch:** **Post-Launch (V1.1, target Week 2-3)**
This feature only becomes relevant once the season starts and users are making live picks. Shipping it before Week 1 adds no value. Use the pre-launch window to build core features; ship forecasting as the first in-season update. This also creates a "new feature" announcement moment during the season.

---

## 8. Pool Structure Analysis

**Priority:** P2

**Problem being solved:**
SP's current strategy recommendations don't account for pool-specific parameters beyond entry count and buyback. But pool structure matters significantly: a 50-player WTA pool rewards different strategies than a 500-player tiered payout pool. Field size, prize structure, buyback rules, and weekly vs season-long elimination all change optimal play. Without this research, the Pool & Entry Advisor (#5) and Multi-Pool Optimization (#6) are built on incomplete foundations.

**Target user:**
Internal -- this is a research initiative that powers user-facing features (#5, #6). Indirectly benefits all multi-pool users.

**Proposed solution (high level):**
Research project (Stan-led) that produces a Pool Structure Impact Model: a structured dataset showing how each pool parameter affects optimal strategy selection, expected survival rates, and dollar returns.

**Research questions:**
1. How does field size (20 vs 100 vs 1,000 vs 14,000) change optimal strategy weights?
2. How does prize structure (WTA vs top-3 vs tiered) change the value of late-week survival vs early consistency?
3. Quantify buyback impact on strategy selection (Stan's gaps analysis has partial data)
4. How does weekly elimination vs season-long elimination change strategy?
5. What is the interaction effect between field size and buyback?

**MVP scope:**
- Simulation study: run backtester across varying pool parameters (field size: 20, 50, 100, 500, 5000, 14000; prize: WTA, top-3, tiered; buyback: none, Wk1-3, Wk1-5)
- Output: Pool Structure Impact Matrix -- a lookup table mapping pool parameters to recommended strategy weights and expected advantage
- Integrate findings into recommendation engine as configurable parameters

**Out of scope (for this release):**
- Live pool data collection (watching real pool outcomes)
- Game-theoretic equilibrium modeling
- Platform-specific tuning (Circa-specific, DK-specific optimizations)

**Success metrics:**
- Pool Structure Impact Matrix covers the top 6 pool archetypes from Stan's ROI research
- Recommendation engine can accept pool parameters and adjust strategy weights accordingly
- Backtester validates that pool-specific strategies outperform pool-agnostic strategies by measurable margin

**Dependencies:**
- Existing backtester and simulation engine (built)
- Stan's ROI research and gaps analysis (completed -- provides partial buyback data)
- No dependency on other enhancements; this is a research input to #5 and #6

**Deadline/timing constraint:**
Research should be completed before Pool & Entry Advisor (#5) and Multi-Pool Optimization (#6) are built. If those are post-launch, this research has until October 2026. If we want MVP advisor for V1, research needs to finish by July 15.

**Open questions:**
- Is the existing backtester simulation engine fast enough to run the full parameter sweep, or does it need optimization?
- How do we validate simulated pool structure effects without live data from real pools of varying structures?
- Should field size impact be modeled as continuous or bucketed (small/medium/large/mega)?

**V1 Pre-Launch vs Post-Launch:** **Post-Launch (research track)**
This is foundational research, not a user-facing feature. It powers post-launch features (#5, #6). Start the research in parallel with V1 dev, but don't block V1 on it. Target completion: August 2026, available for post-launch feature development.

---

## 9. Platform Integration (Splash Sports etc.)

**Priority:** P3

**Problem being solved:**
Users in existing survivor pools on platforms like Splash Sports, DraftKings, Yahoo, or RunYourPool must manually re-enter their pool details, entries, and pick history into SP. This creates friction at signup (users must duplicate data) and during the season (users must keep two systems in sync). Every manual step is a churn risk.

**Target user:**
Users who already play in pools on established platforms. This is the majority of the addressable market -- very few users are running pools from scratch.

**Proposed solution (high level):**
Build integrations with major survivor pool platforms to import/sync:
- Pool configuration (size, rules, entry fee, prize structure)
- User's entries and pick history
- Weekly results (eliminations, wins)
- Optionally: field-level data (public picks, elimination rates)

Start with the highest-value integration (likely Splash Sports or RunYourPool based on market share), then expand.

**MVP scope:**
- Research phase: identify available APIs, scraping feasibility, and partnership opportunities for top 3-5 platforms
- Build one integration (highest-value platform) with:
  - Pool import: user connects their account, SP pulls pool details
  - Entry sync: SP imports the user's entries and pick history
  - Weekly results import: SP pulls elimination/survival data after each week
- Manual CSV/data upload as fallback for platforms without API access

**Out of scope (for this release):**
- Write-back (submitting picks TO the platform from SP)
- Real-time sync during pick windows
- Platform-specific UI (DK-themed view, etc.)
- Integrations with more than 1-2 platforms

**Success metrics:**
- Connected users complete onboarding 2x faster than manual-entry users
- Weekly sync accuracy: 99%+ (entries/picks match between SP and source platform)
- Churn rate for connected users is 30%+ lower than manual users (hypothesis)
- At least one platform integration live by mid-season 2026

**Dependencies:**
- Pool management system (existing, being refactored in SPP-7)
- IA Overhaul (#1) -- pool import flow needs to fit in the management hub
- No dependency on other enhancements

**Deadline/timing constraint:**
Not required for launch. Most valuable once users are actively playing (mid-season). Platform partnerships take time to establish. Target: V1.1 or V1.2 (October-November 2026).

**Open questions:**
- Which platform has the best API access or scraping feasibility? Needs technical research.
- Are platforms hostile to third-party integrations? (DraftKings likely is; smaller platforms may be more open.)
- Should we pursue official partnerships or build unofficial integrations?
  - **Recommendation:** Start unofficial (scraping/API reverse engineering for research), then approach for partnership once we have users to offer as leverage.
- Is OAuth-based account linking feasible, or do we need credential-based access?
- Legal considerations around scraping platform data?

**V1 Pre-Launch vs Post-Launch:** **Post-Launch (V1.2+)**
Platform integrations require external dependencies (API access, partnerships, legal review) that are unpredictable in timeline. The V1 product works without them -- users enter pool data manually. Ship V1 with manual entry, then add integrations as a major post-launch value-add that reduces friction for the growing user base.

---

## Dependency Graph

```
                    ┌──────────────────────────┐
                    │  1. IA Overhaul           │
                    │  (Foundation - do first)  │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼───────────────┐
                    │  2. Design System         │
                    │  Unification              │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼───────────────┐
                    │  3. Back Tester           │
                    │  Integration              │
                    └──────────────────────────┘

    ┌──────────────────────────┐
    │  8. Pool Structure       │
    │  Analysis (Research)     │◄─── Can start in parallel
    └──────────┬───────────────┘
               │
               │ informs
               ▼
    ┌──────────────────────────┐     ┌──────────────────────────┐
    │  4. ROI Analysis         │────►│  5. Pool & Entry Advisor │
    │  Feature                 │     └──────────┬───────────────┘
    └──────────────────────────┘                │
                                                │
                                     ┌──────────▼───────────────┐
                                     │  6. Multi-Pool           │
                                     │  Optimization            │
                                     └──────────────────────────┘

    ┌──────────────────────────┐
    │  7. Multi-Entry          │     (Independent - needs only
    │  Forecasting             │      existing engine)
    └──────────────────────────┘

    ┌──────────────────────────┐
    │  9. Platform Integration │     (Independent - external
    │  (Splash Sports etc.)    │      dependency driven)
    └──────────────────────────┘
```

**Key dependency chains:**
- **Chain A (UX Foundation):** #1 IA Overhaul → #2 Design System → #3 Back Tester Integration
- **Chain B (Advisory Suite):** #4 ROI Analysis → #5 Pool & Entry Advisor → #6 Multi-Pool Optimization
- **Research Input:** #8 Pool Structure Analysis feeds into #5 and #6
- **Independent:** #7 Multi-Entry Forecasting, #9 Platform Integration

---

## Recommended Build Sequence

### Phase 1: UX Foundation (May - July 2026) -- V1 Pre-Launch

| Order | Enhancement | Start | Ship | Notes |
|-------|-------------|-------|------|-------|
| 1 | **IA Overhaul** (#1) | May 15 | July 15 | Design: May 15-Jun 15. Build: Jun 15-Jul 15. |
| 2 | **Design System Unification** (#2) | June 1 | July 31 | Token extraction: Jun 1-15. Restyling: Jun 15-Jul 31. Overlaps with IA build. |
| 3 | **ROI Analysis Feature** (#4) | June 15 | July 15 | Can parallelize with IA build. Uses existing research data. |
| 4 | **Back Tester Integration** (#3) | July 1 | August 1 | Starts after IA shell is in place. |

### Phase 2: Research (June - August 2026) -- Parallel Track

| Order | Enhancement | Start | Ship | Notes |
|-------|-------------|-------|------|-------|
| R1 | **Pool Structure Analysis** (#8) | June 1 | August 15 | Stan runs simulations in parallel with dev work. No Felix dependency. |

### Phase 3: Post-Launch Features (September - November 2026)

| Order | Enhancement | Target | Notes |
|-------|-------------|--------|-------|
| 5 | **Multi-Entry Forecasting** (#7) | Sep 15-30 | First in-season update. High user impact. |
| 6 | **Pool & Entry Advisor** (#5) | Oct 15 | Uses ROI engine + pool structure research. |
| 7 | **Multi-Pool Optimization** (#6) | Nov 15 | Builds on advisor + pool structure research. |
| 8 | **Platform Integration** (#9) | Nov-Dec | External dependency timeline. Start research in August. |

### Rationale

1. **IA first** because every other enhancement needs a home in the navigation. Building features into a broken IA creates rework.
2. **Design system alongside IA** because restyling pages that are being restructured is more efficient than restyling, then restructuring.
3. **ROI calculator in parallel** because it's data-driven (Stan's research is done), relatively small engineering scope, and is the highest-impact conversion tool after the Back Tester.
4. **Back Tester integration after IA shell** because it needs to slot into the new navigation structure.
5. **Pool Structure Analysis runs on a research track** that doesn't compete for Felix's time.
6. **Post-launch features ordered by user impact and dependency readiness.**

---

## Risk Assessment

### Items that might not make V1

| Enhancement | V1 Risk Level | Primary Risk | Mitigation |
|-------------|---------------|-------------|------------|
| **#1 IA Overhaul** | **Medium** | Design iteration could stall. Felix is the bottleneck and already has SPP-7, SPP-8, SPP-12, SPP-15, SPP-16 on his plate. | Timebox design to 4 weeks. If IA build slips past July 15, ship minimal nav restructure (just top-level sections) and polish post-launch. |
| **#2 Design System** | **Medium** | Scope creep -- "just restyle one more component" can balloon. Dark theme may surface unexpected rendering issues. | Define explicit component list for V1 restyling. Accept 80% coverage for launch; polish remainder post-launch. |
| **#3 Back Tester Integration** | **Low-Medium** | Porting React components between codebases is usually straightforward but can surface dependency conflicts. | Start with an iframe embed as fallback if component porting takes too long. Not ideal but functional. |
| **#4 ROI Analysis** | **Low** | Calculation logic is straightforward (lookup table + interpolation). UI is a form + results display. | Smallest engineering scope of the V1 enhancements. Could be built in 1-2 sprints. |
| **#5 Pool & Entry Advisor** | **High (for V1)** | Depends on ROI engine + pool structure research. Multi-pool optimization logic is complex. | Defer to post-launch. Do not attempt for V1. |
| **#6 Multi-Pool Optimization** | **Very High (for V1)** | Requires #5 + #8 as prerequisites. Research-heavy. | Firm post-launch. V1.2 at earliest. |
| **#7 Multi-Entry Forecasting** | **High (for V1)** | Only useful once season starts. Building it pre-launch means it sits unused until Week 1. | Ship as first in-season update. Start dev in August for September delivery. |
| **#8 Pool Structure Analysis** | **N/A (research)** | Simulation parameter sweep may take longer than expected. | Start early (June). Stan can run this without competing for Felix time. |
| **#9 Platform Integration** | **Very High (for V1)** | External dependencies (API access, legal). Unpredictable timeline. | Firm post-launch. Start platform research in August. |

### Overall V1 Enhancement Budget

Given that Felix is already committed to the existing dev plan (SPP-7, SPP-8, SPP-11, SPP-12, SPP-15, SPP-16, SPP-58, referral system, data pipeline), adding 4 enhancements to V1 is aggressive. The realistic V1 enhancement scope is:

**Confident V1 ships:**
- #4 ROI Analysis (small scope, high impact)

**Likely V1 ships (if IA design stays on track):**
- #1 IA Overhaul (may ship as 80% version)
- #2 Design System (may ship as 80% version)

**Stretch for V1:**
- #3 Back Tester Integration (depends on #1 and #2 being substantially done)

**Firm post-launch:**
- #5, #6, #7, #8, #9

If Felix capacity becomes the binding constraint, **prioritize the existing dev plan (Tier 1 must-ship items) over these enhancements.** A working product with imperfect IA beats a beautiful shell with missing core features.

---

*This document is a living brief. Update as requirements crystallize and research completes.*
