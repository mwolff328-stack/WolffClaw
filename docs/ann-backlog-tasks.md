# SurvivorPulse Enhancement Backlog Tasks

**Author:** Ann the Analyst
**Date:** April 28, 2026
**Version:** 1.0
**Input sources:** Pam's Enhancement Briefs (9), Additional Features (3), Competitive Moat Features (4), Stan's Research
**Launch target:** August 15, 2026 (V1), with post-launch phases through December 2026

---

## Summary

- **Total features:** 16
- **Total tasks:** 131
- **Size distribution:** S: 38 | M: 54 | L: 30 | XL: 9
- **V1 Pre-Launch tasks:** 76
- **Post-Launch tasks:** 55
- **Critical path length:** ~14 weeks (May 1 to Aug 15)

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
9. [Platform Integration](#9-platform-integration)
10. [Strategy-to-Context Matching Framework](#10-strategy-to-context-matching-framework)
11. [Mobile App (PWA)](#11-mobile-app-pwa)
12. [Notification System](#12-notification-system)
13. [Buyback-Aware Strategy Engine](#13-buyback-aware-strategy-engine)
14. [Portfolio Architecture Presets](#14-portfolio-architecture-presets)
15. [Correlated Elimination Risk Score](#15-correlated-elimination-risk-score)
16. [Personalization Anti-Dilution](#16-personalization-anti-dilution)

---

## 1. Information Architecture Overhaul

**Description:** Redesign app navigation and page hierarchy around two primary modes: My Pools & Entries (management hub) and Analysis & Tools (intelligence hub). Foundational work that determines where all other features live.

**V1 Pre-Launch** | Sprint Group: A (Foundation)

### Tasks

#### 1.1 Audit current page inventory and user flows
- **Size:** S
- **Category:** UX/Design
- **Dependencies:** None
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the existing SurvivorPulse app, when Deb audits all routes and pages, then a complete page inventory document exists listing every route, its purpose, and current navigation path
  - Given the page inventory, when user flows are mapped, then the top 5 user journeys (create pool, make picks, view recommendations, manage entries, view analytics) are documented with step counts
  - Given the audit is complete, then dead-end states, orphan pages, and redundant routes are flagged

#### 1.2 Define new top-level navigation structure
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 1.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the page audit, when the new IA is designed, then there are 2-3 primary navigation sections maximum
  - Given the new structure, when mapped against all 16 planned features, then every feature has an obvious home in the navigation
  - Given the new structure, when evaluated against the 2-click rule, then any existing feature is reachable in 2 clicks or fewer from the dashboard
  - Given the new structure, then a persistent pool/entry context selector pattern is specified

#### 1.3 Wireframe key screens: dashboard, pool hub, analysis hub
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 1.2
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the approved IA structure, when wireframes are produced, then dashboard, pool management hub, and analysis hub have lo-fi wireframes
  - Given the wireframes, when reviewed, then the pool/entry context selector is visible and functional in the wireframes
  - Given the wireframes, then empty states, loading states, and error states are represented
  - Given the wireframes, when a walkthrough is conducted with the founder, then he confirms the structure "makes sense"

#### 1.4 Implement new navigation shell
- **Size:** L
- **Category:** UX/Design
- **Dependencies:** 1.3, 2.1 (design tokens)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the approved wireframes, when the navigation shell is built, then the top-level navigation renders the new structure with working route switching
  - Given the new shell, when all existing pages are rendered within it, then no page loses functionality
  - Given the navigation shell, when tested on mobile viewport (375px), then navigation remains usable without horizontal scroll
  - Given the shell, then a persistent pool/entry context selector component exists and maintains state across page transitions

#### 1.5 Re-route existing pages into new IA structure
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 1.4
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the new navigation shell, when all existing pages are remapped, then every page lives under the correct section (Pools & Entries or Analysis & Tools)
  - Given old routes, when accessed, then they redirect to the new route with 301 redirects
  - Given the remapping is complete, then zero orphan pages or dead-end navigation states exist
  - Given the remapping, when the top 5 user journeys from audit 1.1 are retested, then each completes in fewer steps than before

#### 1.6 Implement dashboard/home screen
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 1.5
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a logged-in user with pools, when they land on the dashboard, then they see a glanceable summary of active pools, entry status, and upcoming deadlines
  - Given the dashboard, when analysis tools have new recommendations, then a summary card links to the analysis hub
  - Given a new user with no pools, then the dashboard shows an onboarding prompt to create their first pool
  - Given the dashboard, when loaded, then it renders in under 2 seconds with all data populated

#### 1.7 Design and implement week-by-week temporal navigation
- **Size:** L
- **Category:** UX/Design + Frontend
- **Dependencies:** 1.4 (nav shell), 1.2 (nav structure)
- **Agent:** Felix (backend), Deb (frontend)
- **Acceptance Criteria:**
  - Given the global week selector, when a user selects a previous week, then all views (This Week, Entry Workspace, Portfolio) display data scoped to that week and prior weeks only
  - Given a previous week is selected, then recommendations, picks, and portfolio data reflect only what was known as of that week (not subsequent weeks' data)
  - Given a user edits entry data (e.g., changes a pick) in a historical week and saves, then subsequent weeks reflect that change (e.g., updated remaining team availability, updated pick history)
  - Given the week selector, then the current week is clearly indicated and easily returnable to

#### 1.8 Implement eliminated pool/entry access and editing
- **Size:** M
- **Category:** UX/Design + Frontend
- **Dependencies:** 1.4 (nav shell)
- **Agent:** Felix (backend), Deb (frontend)
- **Acceptance Criteria:**
  - Given a pool where all entries are eliminated, when the user navigates to that pool, then the pool is fully accessible with all data viewable and editable
  - Given an eliminated entry, when the user clicks it in the sidebar or any list, then the entry workspace opens with full functionality (not a read-only or limited view)
  - Given eliminated entries, then they are visually distinguished (grayed/strikethrough with elimination week shown) but all actions (edit pick, view recommendations, view analytics) remain available
  - Given the sidebar entry list, then eliminated entries are shown (not hidden) and are interactive

#### 1.9 Implement season selector and cross-season navigation
- **Size:** L
- **Category:** UX/Design + Frontend + Backend
- **Dependencies:** 1.4 (nav shell), 1.7 (week navigation)
- **Agent:** Felix (backend + data model), Deb (frontend)
- **Acceptance Criteria:**
  - Given the navigation, when a season selector is displayed, then users can switch between available seasons (e.g., 2025, 2026)
  - Given a season switch, then the sidebar updates to show that season's pools and entries
  - Given a season switch, then the Command Center (This Week, Portfolio) displays data for the selected season
  - Given previous season data, then pools, entries, picks, and analytics are fully viewable and editable
  - Given the season selector, then the current active season is clearly indicated

#### 1.10 Implement pool-level historical data management view
- **Size:** M
- **Category:** UX/Design + Frontend
- **Dependencies:** 1.4 (nav shell), 1.8 (eliminated access)
- **Agent:** Felix (backend), Deb (frontend)
- **Acceptance Criteria:**
  - Given a pool, when the user navigates to pool settings/detail, then a "History" or "Data" section shows all entries (alive and eliminated) with their full pick history
  - Given the pool history view, then each entry shows: status (alive/eliminated + week), all picks by week, and current data (recommendations, analytics) for the selected week
  - Given the pool history view, then the user can edit any entry's data (picks, status) with changes propagating forward
  - Given the pool history view, then it works for both current and previous season pools

---

## 2. Design System Unification

**Description:** Extract the Back Tester's design system (dark theme, Inter Variable + JetBrains Mono, indigo-violet palette, IBM Carbon status tokens) into a shared token library and apply to the main app.

**V1 Pre-Launch** | Sprint Group: A (Foundation, overlaps with IA)

### Tasks

#### 2.1 Extract design tokens from Back Tester DESIGN.md
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** None
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the Back Tester DESIGN.md, when tokens are extracted, then a shared Tailwind theme extension file exists with color palette, typography, spacing, elevation, and motion values
  - Given the token file, when imported by both main app and back tester, then both compile without errors
  - Given the tokens, then CSS custom properties are generated as a fallback for non-Tailwind contexts
  - Given the token extraction, then a mapping document exists showing which Back Tester token maps to which main app element

#### 2.2 Apply dark theme and typography to main app shell
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 2.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the shared tokens, when applied to the main app, then the background, text, and navigation use the dark theme palette
  - Given the typography tokens, when applied, then Inter Variable is used for UI text and JetBrains Mono for data/numbers across all pages
  - Given the dark theme, when all existing pages are rendered, then no text falls below WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text)

#### 2.3 Restyle core UI components
- **Size:** L
- **Category:** UX/Design
- **Dependencies:** 2.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the shared tokens, when buttons, cards, inputs, selects, tables, and modals are restyled, then each matches the Back Tester visual language
  - Given the restyled components, when rendered across all existing pages, then no layout breakage occurs
  - Given shadcn/ui components, when the Tailwind theme is applied, then components adopt the design system without per-component overrides where possible
  - Given the restyled components, then all interactive states (hover, focus, disabled, active) use token-defined values

#### 2.4 Restyle data display components
- **Size:** L
- **Category:** UX/Design
- **Dependencies:** 2.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given score cards, recommendation panels, and analytics views, when restyled, then they match Back Tester data visualization patterns
  - Given the IBM Carbon status token system (green/yellow/red/blue), when applied to all status indicators in the main app, then every status uses the correct token
  - Given data visualization components (charts, gauges), when rendered in dark theme, then all colors are legible and distinguishable
  - Given the restyled data components, then all color values come from shared tokens with zero hardcoded one-offs

#### 2.5 Cross-browser and responsive QA pass
- **Size:** S
- **Category:** UX/Design
- **Dependencies:** 2.2, 2.3, 2.4
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the restyled app, when tested on Chrome, Firefox, Safari, and Edge, then no visual regressions exist
  - Given the restyled app, when tested at 375px, 768px, and 1440px viewports, then layout is functional at all breakpoints
  - Given the testing, then a QA report documents any remaining issues with severity ratings

---

## 3. Back Tester Integration

**Description:** Port the standalone Back Tester app into the main SurvivorPulse app as a first-class feature under Analysis & Tools. Free/gated mode for prospects, full mode for subscribers.

**V1 Pre-Launch** | Sprint Group: B (Core Features)

### Tasks

#### 3.1 Analyze Back Tester codebase for portability
- **Size:** S
- **Category:** Infrastructure
- **Dependencies:** None
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the Back Tester repo, when analyzed, then a portability report lists all React components, their dependencies, and integration complexity (easy/medium/hard)
  - Given the analysis, then shared dependencies between main app and Back Tester are identified with version compatibility notes
  - Given the analysis, then a migration plan (component port vs iframe fallback) is documented with estimated effort

#### 3.2 Port Back Tester React components into main app
- **Size:** XL
- **Category:** Infrastructure
- **Dependencies:** 3.1, 1.4 (nav shell), 2.1 (design tokens)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the migration plan, when Back Tester components are ported, then all 7+ strategy types, configurable weights, and advanced modes function identically to the standalone app
  - Given the ported components, when the 17-step tutorial is executed, then all steps complete without errors
  - Given the ported components, when the feedback system is triggered, then submissions reach Notion via the existing proxy
  - Given the integration, then page load time is within 500ms of the standalone version

#### 3.3 Implement free/gated access mode
- **Size:** M
- **Category:** Auth & Accounts
- **Dependencies:** 3.2
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given an unauthenticated user, when they access /tools/backtester, then they see the access gate (email capture) before full access
  - Given the access gate, when a user submits name and email, then the data is captured and the user gets full free-tier backtester access
  - Given free-tier access, when the user attempts to use subscriber features (load pool params), then a subscription upsell is shown

#### 3.4 Implement subscriber mode with pool parameter loading
- **Size:** M
- **Category:** Core Engine
- **Dependencies:** 3.2
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a logged-in subscriber with pools, when they access the backtester, then no access gate is shown
  - Given the subscriber mode, when the user clicks "Load Pool Parameters," then their pool's entry count, buyback rules, and pool size pre-populate the backtester config
  - Given loaded pool parameters, when "Find Best Strategy" is run, then results reflect the user's specific pool configuration
  - Given subscriber mode, then switching between pools updates backtester parameters without page reload

#### 3.5 Set up redirects from standalone Back Tester URL
- **Size:** S
- **Category:** DevOps
- **Dependencies:** 3.2
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the standalone URL (survivorpulse-backtester-prototype.replit.app), when accessed, then the user is redirected to the main app's backtester route
  - Given existing bookmarks to the standalone URL, when followed, then state is not lost (access gate status preserved if possible)
  - Given the redirect, then the standalone app displays a "We've moved" notice for users with JS disabled

---

## 4. ROI Analysis Feature

**Description:** Live ROI calculator that takes pool parameters and outputs expected SP advantage, dollar surplus, and subscription payback analysis using Stan's research data.

**V1 Pre-Launch** | Sprint Group: B (Core Features, can parallelize with IA build)

### Tasks

#### 4.1 Build ROI calculation engine
- **Size:** M
- **Category:** Core Engine
- **Dependencies:** None
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given Stan's lookup tables (Section 8 of ROI analysis), when the calculation engine is built, then it produces expected survival advantage, dollar surplus, and ROI % for any combination of pool size, entry fee, entry count (1-50), rake (0-20%), buyback (yes/no), and prize structure (WTA/top-3/tiered)
  - Given entry counts between tested values (5, 10, 20, 50), when calculated, then the engine uses linear interpolation and results are within 5% of Stan's research figures
  - Given a tiered payout pool, when calculated, then the 1.5-1.8x late-season survival amplification factor from Stan's gaps analysis is applied
  - Given a field composition adjustment, when smart field % is specified, then the engine adjusts expected advantage accordingly (default: 2-5% private, 10% DK, 15% Circa)

#### 4.2 Build ROI calculator frontend
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 4.1, 2.1 (design tokens)
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the ROI engine, when the frontend is built, then users see an input form with: pool size, entry fee, entry count, rake %, buyback toggle, and prize structure selector
  - Given the form, when submitted, then results display: dollar surplus, ROI %, subscription payback period, and confidence range (best/median/worst season)
  - Given the results, then a comparison table shows naive vs SP expected returns side by side
  - Given the calculator, when average completion is measured, then it takes under 30 seconds end to end

#### 4.3 Implement preset pool profiles
- **Size:** S
- **Category:** UX/Design
- **Dependencies:** 4.2
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the ROI calculator, when preset buttons are displayed, then Circa ($1000, 14000 players, 2% rake, tiered), DraftKings Main ($100, 18000 players, 15% rake, tiered), and typical $100 private pool (50 players, 0% rake, WTA) are available
  - Given a preset click, when the form populates, then all 6 input fields are filled with accurate values for that pool type
  - Given presets, when tracked, then usage analytics show which presets are selected

#### 4.4 Build "Share your ROI" feature
- **Size:** S
- **Category:** Marketing/Content
- **Dependencies:** 4.2
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given ROI results, when "Share" is clicked, then a shareable link or image is generated with the user's specific ROI summary
  - Given the share link, when opened by another user, then the ROI calculator loads with the same parameters pre-filled
  - Given the share image, then it includes the SurvivorPulse brand, dollar surplus, and ROI % in a social-media-ready format

#### 4.5 Integrate ROI calculator into IA
- **Size:** S
- **Category:** UX/Design
- **Dependencies:** 4.2, 1.4
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the IA structure, when the ROI calculator is placed, then it lives under Analysis & Tools and is accessible in 2 clicks from dashboard
  - Given the navigation, when a user is on the ROI calculator, then the breadcrumb and active nav state are correct
  - Given free users, when they access the ROI calculator, then it is fully available (not gated -- this is a sales tool)

---

## 5. Pool & Entry Advisor

**Description:** Advisory tool that takes user's budget and available pools, then recommends optimal entry allocation across pools. Extends ROI Analysis to multi-pool portfolio optimization.

**Post-Launch (V1.1, target October 2026)** | Sprint Group: D

### Tasks

#### 5.1 Build allocation algorithm
- **Size:** L
- **Category:** Core Engine
- **Dependencies:** 4.1 (ROI engine), 8.4 (pool structure matrix -- can use simplified heuristics without)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a user's total budget and list of pools (each with entry fee, size, rake, buyback, prize structure), when the algorithm runs, then it produces recommended entry counts per pool that maximize total expected surplus
  - Given the algorithm, when marginal analysis is computed, then the marginal value of the next entry in each pool is output
  - Given the algorithm, when a pool is -EV even with SP, then a warning flag is attached to that pool
  - Given the algorithm output, when compared to Stan's ROI model, then recommendations align within 5%

#### 5.2 Build advisor input form
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 5.1, 2.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the advisor, when the form loads, then users can input total budget and add 1-10 pools with parameters (manual entry or presets)
  - Given the form, when "Add another pool" is clicked, then a new pool row appears without page reload
  - Given existing subscriber pools, when "Import my pools" is clicked, then pool parameters auto-populate from user's saved pools

#### 5.3 Build advisor results display
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 5.1, 5.2
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given advisor results, when displayed, then per-pool entry recommendations, total expected surplus, and marginal value per pool are shown
  - Given results, when a comparison toggle is available, then users see "your current allocation vs recommended" side by side
  - Given results, then -EV pools are visually flagged with a warning indicator

#### 5.4 Integrate buyback ROI recommendation
- **Size:** S
- **Category:** Core Engine
- **Dependencies:** 5.1, 13.1
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a pool with buyback enabled, when the advisor runs, then it always recommends exercising buyback with the expected ROI per buyback shown
  - Given buyback pools, when factored into the allocation, then the cost of buyback entries is included in the budget calculation
  - Given the recommendation, then the rationale cites the 4.15 EW/buyback at n=10 finding

---

## 6. Multi-Pool Optimization

**Description:** Extend the recommendation engine to produce pool-specific strategy recommendations and cross-pool coordination based on pool parameters (buyback, prize structure, field size).

**Post-Launch (V1.2, target November 2026)** | Sprint Group: E

### Tasks

#### 6.1 Build pool parameter capture system
- **Size:** M
- **Category:** Pool Mgmt
- **Dependencies:** None (can start anytime)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given pool creation/edit, when the form is shown, then users can specify: buyback rules (window), prize structure (WTA/tiered/top-3), field size, and rake %
  - Given pool parameters, when saved, then they persist in the database and are available to the recommendation engine
  - Given existing pools without parameters, then smart defaults are applied (private = 0% rake, WTA; platform = heuristic based on pool name)

#### 6.2 Implement per-pool strategy weight recommendations
- **Size:** L
- **Category:** Core Engine
- **Dependencies:** 6.1, 8.4 (pool structure matrix), 13.2 (buyback-aware switching)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a user with 2+ pools with different rule sets, when recommendations are generated, then each pool receives strategy weights optimized for its parameters
  - Given a buyback pool and a non-buyback pool, when recommendations are compared, then strategy weights differ meaningfully (per Stan's research)
  - Given per-pool recommendations, when the user views them, then the rationale explains why strategies differ between pools

#### 6.3 Implement cross-pool entry correlation analysis
- **Size:** L
- **Category:** Analytics
- **Dependencies:** 6.2
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a user with entries across multiple pools, when correlation analysis runs, then the system identifies entries picking the same team across pools
  - Given >50% of entries across pools sharing the same pick in a week, then a correlation alert fires
  - Given cross-pool correlation, when team overlap is detected, then an alternative diversified pick is suggested
  - Given cross-pool team usage, then the system tracks shared team inventory across all pools to prevent future conflicts

#### 6.4 Build multi-pool dashboard view
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 6.2, 6.3
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given a user with multiple pools, when they view the dashboard, then per-pool strategy health and aggregate portfolio health are displayed
  - Given correlation alerts, when active, then they surface on the dashboard with severity indicators
  - Given the dashboard, then the user can drill into any pool for detailed per-pool strategy analysis

---

## 7. Multi-Entry Forecasting

**Description:** Scenario modeling tool showing probability distributions for portfolio outcomes based on proposed picks. Lets multi-entry users understand risk before committing.

**Post-Launch (V1.1, target Week 2-3 of 2026 season)** | Sprint Group: D

### Tasks

#### 7.1 Build single-week forecast engine
- **Size:** L
- **Category:** Core Engine
- **Dependencies:** None (uses existing win probability data + scoring model)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a user's entry portfolio and proposed pick allocation, when the forecast runs, then it outputs a probability distribution for entries surviving the week
  - Given the forecast, when displayed, then expected entries surviving, best-case, and worst-case scenarios are shown
  - Given the engine, when compared to actual outcomes over a full season, then forecasted survival probabilities match within 15% tolerance

#### 7.2 Build portfolio correlation visualization
- **Size:** M
- **Category:** Analytics
- **Dependencies:** 7.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given a user's proposed picks, when the correlation view renders, then entries with the same pick are visually grouped showing correlated fate
  - Given the visualization, when 10-50 entries are displayed, then the UI remains scannable without overwhelming the user
  - Given correlation, then a numerical correlation score is shown (e.g., "34% correlated")

#### 7.3 Build scenario comparison UI
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 7.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the forecasting tool, when a user creates 2 scenarios with different pick allocations, then a side-by-side comparison view renders
  - Given the comparison, then expected survival, correlation, and risk metrics are displayed for each scenario
  - Given the comparison, then a clear "Scenario A is recommended because..." summary explains the difference

#### 7.4 Build multi-week projection
- **Size:** L
- **Category:** Core Engine
- **Dependencies:** 7.1
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the forecast engine, when 2-3 weeks of projected picks are input, then a multi-week portfolio state projection is generated
  - Given the projection, when displayed, then expected portfolio state per week is shown as a declining survival curve
  - Given the projection accuracy, then a disclaimer notes that accuracy degrades beyond 2-3 weeks
  - Given the projection, then dollar-value-at-risk overlay is available for users who have configured pool prize info

---

## 8. Pool Structure Analysis

**Description:** Research initiative (Stan-led) producing a Pool Structure Impact Model showing how pool parameters affect optimal strategy. Powers features #5 and #6.

**Pre-Launch (Research track, parallel)** | Sprint Group: R (Research)

### Tasks

#### 8.1 Design simulation parameter sweep
- **Size:** S
- **Category:** Core Engine
- **Dependencies:** None
- **Agent:** Stan
- **Acceptance Criteria:**
  - Given the research questions (field size, prize structure, buyback, elimination type), when the parameter sweep is designed, then the full matrix is documented: field sizes (20, 50, 100, 500, 5000, 14000) x prize structures (WTA, top-3, tiered) x buyback configs (none, Wk1-3, Wk1-5)
  - Given the sweep design, then estimated computation time and resource requirements are documented
  - Given the design, then the output schema for the Pool Structure Impact Matrix is specified

#### 8.2 Optimize backtester for parameter sweep
- **Size:** M
- **Category:** Infrastructure
- **Dependencies:** 8.1
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the parameter sweep requirements, when backtester performance is tested, then it can complete the full sweep within 48 hours of compute time
  - Given performance constraints, when optimization is applied, then parallelization or batching is implemented to hit the time target
  - Given the optimization, then results are output in the specified schema from 8.1

#### 8.3 Execute simulation study
- **Size:** L
- **Category:** Core Engine
- **Dependencies:** 8.2
- **Agent:** Stan
- **Acceptance Criteria:**
  - Given the optimized backtester, when the full parameter sweep is run, then results for all combinations (6 field sizes x 3 prize x 3 buyback = 54 configurations) are produced
  - Given the results, then each configuration has recommended strategy weights and expected advantage documented
  - Given the results, then rake impact is explicitly modeled showing break-even entry counts per rake level

#### 8.4 Produce Pool Structure Impact Matrix
- **Size:** M
- **Category:** Core Engine
- **Dependencies:** 8.3
- **Agent:** Stan
- **Acceptance Criteria:**
  - Given the simulation results, when the matrix is produced, then it covers the top 6 pool archetypes (Circa, DK Main, DK Mini, typical private WTA, mid-size tiered, large buyback)
  - Given the matrix, when used by the recommendation engine, then strategy weights can be looked up by pool parameters
  - Given the matrix, when validated against existing backtester results, then pool-specific strategies outperform pool-agnostic strategies by a measurable margin
  - Given the matrix, then interaction effects between field size and buyback are documented

---

## 9. Platform Integration

**Description:** Build integrations with survivor pool platforms (Splash Sports, RunYourPool, DraftKings, Yahoo) for pool import, entry sync, and weekly results.

**Post-Launch (V1.2+, target November-December 2026)** | Sprint Group: F

### Tasks

#### 9.1 Research platform API/scraping feasibility
- **Size:** M
- **Category:** Infrastructure
- **Dependencies:** None
- **Agent:** Stan
- **Acceptance Criteria:**
  - Given the top 5 survivor pool platforms, when research is conducted, then a feasibility report documents: API availability, scraping complexity, ToS restrictions, and partnership viability for each
  - Given the report, then platforms are ranked by integration feasibility and user base overlap with SP's ICP
  - Given the report, then legal risks of scraping are documented with mitigation recommendations

#### 9.2 Build CSV/manual data upload fallback
- **Size:** M
- **Category:** Pool Mgmt
- **Dependencies:** None
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a user with a pool on an unsupported platform, when they use the CSV upload, then pool config, entry list, and pick history are imported
  - Given a CSV upload, when the data is parsed, then validation catches common format errors and prompts correction
  - Given a successful upload, then imported data appears in the user's pool management hub immediately

#### 9.3 Build first platform integration (highest-value)
- **Size:** XL
- **Category:** Infrastructure
- **Dependencies:** 9.1, 9.2
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the highest-value platform identified in 9.1, when integration is built, then users can connect their account and SP pulls pool details, entries, and pick history
  - Given a connected account, when a new week completes, then SP imports elimination/survival data automatically
  - Given the sync, when compared to platform data, then accuracy is 99%+ for entries and picks
  - Given the integration, then connected users complete onboarding 2x faster than manual-entry users

#### 9.4 Build integration management UI
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 9.3
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given a user in pool settings, when they click "Connect Platform," then an OAuth or credential flow starts for the supported platform
  - Given a connected integration, when the user views connection status, then last sync time, sync health, and manual re-sync button are displayed
  - Given the UI, when a sync error occurs, then a clear error message with resolution steps is shown

---

## 10. Strategy-to-Context Matching Framework

**Description:** Recommend optimal portfolio architecture based on user's specific context (entry count, pool parameters, buyback rules, risk preference). Named presets auto-recommended based on user's setup.

**V1 Pre-Launch (core logic) / Post-Launch (advanced matching)** | Sprint Group: B/C

### Tasks

#### 10.1 Build context matching engine
- **Size:** M
- **Category:** Core Engine
- **Dependencies:** None
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a user's entry count, pool parameters (buyback, field size), and optional risk preference, when the matching engine runs, then it returns the optimal portfolio architecture preset with rationale
  - Given entry count 1-5, then "Balanced Core" (all 70/30 Blend) is recommended
  - Given entry count 6-15, then "Core/Satellite" (60% blend + 40% EV) is recommended
  - Given entry count 16-30, then "Role Portfolio" (5-role diversification) is recommended
  - Given entry count 31+, then "Safety/Contrarian" (two-bucket) is recommended

#### 10.2 Build context intake UI
- **Size:** S
- **Category:** UX/Design
- **Dependencies:** 10.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given a new or existing user, when they set up a pool, then a brief context questionnaire captures entry count, buyback rules, and risk preference (conservative/balanced/aggressive)
  - Given the questionnaire, when submitted, then the matching engine returns a recommendation immediately
  - Given existing pools, when the user's context changes (adds entries), then the recommendation updates automatically

#### 10.3 Build recommendation display with rationale
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 10.1, 10.2
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given a portfolio architecture recommendation, when displayed, then the preset name, description, role assignments, and research-backed rationale are shown
  - Given the display, when the user clicks "Why this architecture?", then the explanation cites specific research findings (e.g., "+25 entry-weeks at n=10" for Core/Satellite)
  - Given the display, then the user can accept the recommendation or manually override with a different preset

#### 10.4 Integrate context matching with recommendation engine
- **Size:** L
- **Category:** Core Engine
- **Dependencies:** 10.1, 14.2 (portfolio presets implementation)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a user who accepts a portfolio architecture recommendation, when weekly picks are generated, then the recommendation engine uses the selected architecture's role assignments
  - Given the integration, when entry roles are set (core vs satellite vs contrarian etc.), then each entry's scoring function matches its assigned role
  - Given the integration, when pool parameters change, then the recommendation engine re-evaluates the architecture

---

## 11. Mobile App (PWA)

**Description:** Progressive Web App mobile experience leveraging the existing React app. Core flows: weekly pick management, recommendation review, portfolio risk alerts, notifications.

**Post-Launch (V1.1)** | Sprint Group: D

### Tasks

#### 11.1 Implement PWA manifest and service worker
- **Size:** M
- **Category:** Infrastructure
- **Dependencies:** 1.4 (nav shell), 2.1 (design tokens)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the main app, when a PWA manifest is added, then the app is installable on iOS and Android home screens
  - Given the service worker, when implemented, then core app shell and recent data are cached for offline access
  - Given the PWA, when installed, then it launches in standalone mode without browser chrome
  - Given the manifest, then the app icon, splash screen, and theme color use the SurvivorPulse brand

#### 11.2 Optimize core flows for mobile viewport
- **Size:** L
- **Category:** UX/Design
- **Dependencies:** 11.1, 1.5 (IA complete)
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the mobile viewport (375px-428px), when the pick management flow is used, then all actions (view recommendations, select picks, confirm) are completable with thumb-friendly tap targets (min 44px)
  - Given the recommendation review flow on mobile, then score cards, pick comparisons, and rationale are readable without horizontal scroll
  - Given the portfolio dashboard on mobile, then entry status summary and risk alerts are glanceable on a single screen
  - Given mobile navigation, then bottom tab bar or drawer navigation replaces the desktop sidebar

#### 11.3 Implement push notifications (web push)
- **Size:** M
- **Category:** Infrastructure
- **Dependencies:** 11.1, 12.1 (notification system)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the PWA, when push notification permission is granted, then the user receives browser push notifications for critical alerts
  - Given a push notification, when tapped, then it deep-links to the relevant screen (pick deadline, risk alert, results)
  - Given notification preferences, when configured, then users can enable/disable categories independently

#### 11.4 Performance optimization for mobile
- **Size:** M
- **Category:** Infrastructure
- **Dependencies:** 11.2
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the mobile PWA, when tested on a mid-range device, then initial load time is under 3 seconds on 4G
  - Given the app, when navigating between core flows, then transitions complete in under 300ms
  - Given the service worker cache, then subsequent loads are under 1 second
  - Given Lighthouse mobile audit, then performance score is 80+

---

## 12. Notification System

**Description:** Email and SMS notifications for weekly pick recommendations, wrap-ups, portfolio risk alerts, season milestones, and pool deadline reminders. Uses Postmark for email, SMS provider TBD.

**V1 Pre-Launch (email) / Post-Launch (SMS)** | Sprint Group: C

### Tasks

#### 12.1 Design notification event system
- **Size:** M
- **Category:** Infrastructure
- **Dependencies:** None
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the notification requirements, when the event system is designed, then event types are defined: weekly_recommendations, weekly_wrapup, risk_alert, season_milestone, deadline_reminder, pick_confirmation
  - Given the event system, then each event type has a defined trigger condition, payload schema, and delivery channel(s)
  - Given the system, then a notification preferences table allows per-user per-event-type enable/disable and channel selection (email/SMS/push)
  - Given the system, then rate limiting prevents notification spam (max 3 notifications per day per user unless critical)

#### 12.2 Build email notification templates (Postmark)
- **Size:** M
- **Category:** Marketing/Content
- **Dependencies:** 12.1, 2.1 (design tokens)
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given each notification event type, when an email template is created, then it uses the SurvivorPulse dark theme brand and renders correctly in Gmail, Apple Mail, and Outlook
  - Given the weekly recommendations template, then it includes: top recommended picks, confidence scores, and a direct link to the pick management page
  - Given the risk alert template, then it includes: correlation score, affected entries, and recommended action
  - Given all templates, then each has a plain-text fallback and unsubscribe link

#### 12.3 Implement email delivery pipeline
- **Size:** M
- **Category:** Infrastructure
- **Dependencies:** 12.1, 12.2
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a notification event, when triggered, then the Postmark API sends the appropriate email within 5 minutes
  - Given delivery, when tracked, then open rates, click rates, and bounce rates are logged per event type
  - Given a failed delivery, when Postmark returns an error, then the event is retried up to 3 times with exponential backoff
  - Given the pipeline, then it handles 1000+ concurrent notification sends without timeout

#### 12.4 Build notification preferences UI
- **Size:** S
- **Category:** UX/Design
- **Dependencies:** 12.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given a logged-in user, when they access notification preferences, then each event type is listed with toggle switches for email (and SMS when available)
  - Given the preferences, when toggled, then the change is saved immediately and affects the next notification
  - Given the UI, then default preferences (all email on, all SMS off) are set for new users

#### 12.5 Research and select SMS provider
- **Size:** S
- **Category:** Infrastructure
- **Dependencies:** None
- **Agent:** Rita
- **Acceptance Criteria:**
  - Given the SMS requirement, when providers are evaluated, then a recommendation document compares Twilio, AWS SNS, and MessageBird on: cost per message, deliverability, API ease, and compliance (TCPA)
  - Given the recommendation, then a provider is selected with estimated monthly cost at 100, 500, and 5000 users

#### 12.6 Implement SMS delivery pipeline
- **Size:** M
- **Category:** Infrastructure
- **Dependencies:** 12.5, 12.1
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the selected SMS provider, when integrated, then critical notifications (risk alerts, deadline reminders) can be sent via SMS
  - Given SMS delivery, when a user has opted in and provided a phone number, then messages deliver within 60 seconds
  - Given SMS content, then each message is under 160 characters with a link to the full notification in-app
  - Given SMS compliance, then opt-in confirmation, opt-out (STOP), and TCPA compliance are implemented

---

## 13. Buyback-Aware Strategy Engine

**Description:** Pool-type-aware recommendation switching. When a pool has buyback enabled, the entire strategy engine shifts. Neither PoolGenius nor PoolCrunch distinguishes between buyback/non-buyback in recommendations.

**V1 Pre-Launch** | Sprint Group: B (Core Features)

### Tasks

#### 13.1 Add buyback parameters to pool model
- **Size:** S
- **Category:** Pool Mgmt
- **Dependencies:** None
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given pool creation/edit, when the user toggles "Buyback Enabled," then a buyback window field appears (Wk1-3, Wk1-5, custom)
  - Given the buyback parameters, when saved, then they are stored in the pool record and accessible to the recommendation engine
  - Given existing pools, then a migration adds buyback fields with default "none"

#### 13.2 Implement buyback-aware strategy switching
- **Size:** L
- **Category:** Core Engine
- **Dependencies:** 13.1
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a pool with buyback enabled, when recommendations are generated, then strategy weights shift to favor SP Conservative 65/25/10 (per Stan's research showing it wins at ALL entry counts with buyback)
  - Given a pool without buyback, when recommendations are generated, then the default strategy weights are used (unchanged from current behavior)
  - Given the switch, when a user views recommendations, then the rationale explains the buyback-driven strategy difference
  - Given entry count n=10 with Wk1-3 buyback, then the system recommends exercising buyback with expected 4.15 EW/buyback cited

#### 13.3 Build buyback recommendation display
- **Size:** S
- **Category:** UX/Design
- **Dependencies:** 13.2
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given a buyback pool, when recommendations are viewed, then a prominent "Buyback Recommended" banner shows with expected ROI per buyback
  - Given the display, when the user is within the buyback window, then the recommendation is highlighted with urgency ("Buyback window closes after Week 3")
  - Given the display, then the "always exercise buyback" recommendation includes the positive ROI data point from Stan's research

#### 13.4 Backtest validation of buyback-aware switching
- **Size:** M
- **Category:** Core Engine
- **Dependencies:** 13.2
- **Agent:** Stan
- **Acceptance Criteria:**
  - Given the buyback-aware engine, when backtested against 5 seasons, then buyback-aware strategy selection outperforms buyback-agnostic selection for buyback pools
  - Given the validation, then the performance delta matches Stan's original research within 10% tolerance
  - Given the validation results, then a summary document is produced for marketing use

---

## 14. Portfolio Architecture Presets

**Description:** Named portfolio architecture presets (Balanced Core, Core/Satellite, Role Portfolio, Safety/Contrarian) that users select or receive as auto-recommendation. Research-backed entry role assignments.

**V1 Pre-Launch** | Sprint Group: B (Core Features)

### Tasks

#### 14.1 Define preset configurations in code
- **Size:** M
- **Category:** Core Engine
- **Dependencies:** None
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the 4 research-backed presets, when defined, then each has: name, entry count range, role distribution (% per role), and scoring function per role
  - Given "Balanced Core" (1-5 entries), then all entries use 70/30 Blend scoring
  - Given "Core/Satellite" (6-15 entries), then 60% entries use 70/30 Blend and 40% use SP Production EV
  - Given "Role Portfolio" (16-30 entries), then 5 roles at 20% each: safety (90/10), blend (70/30), contrarian (50/50), FV preserver, EV maximizer
  - Given "Safety/Contrarian" (31+ entries), then 50% use 85/15 and 50% use 55/45

#### 14.2 Integrate presets with recommendation engine
- **Size:** L
- **Category:** Core Engine
- **Dependencies:** 14.1
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a user who selects a preset, when weekly recommendations are generated, then each entry receives picks based on its assigned role's scoring function
  - Given Core/Satellite at n=10, when recommendations are generated, then core entries (6) receive safer picks and satellite entries (4) receive higher-contrarian picks
  - Given the integration, when backtested, then preset-driven recommendations match or exceed the research results from stan-differentiated-scoring-research.md
  - Given the integration, then entry role assignments persist week-to-week and are visible in the entry management view

#### 14.3 Build preset selection and visualization UI
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 14.1, 2.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the pool setup flow, when presets are presented, then each shows: name, recommended entry range, visual role distribution diagram, and research-backed performance claim
  - Given the visualization, when a user selects Core/Satellite, then their entries are color-coded by role (core = blue, satellite = orange) across all views
  - Given the preset selector, when entry count changes, then the recommended preset updates with explanation
  - Given any preset, when "Why this works" is clicked, then research findings (with entry-week improvements) are displayed

#### 14.4 Build custom architecture mode
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 14.2, 14.3
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given a user who doesn't want a preset, when they select "Custom," then they can assign individual roles to each entry
  - Given custom mode, then available roles match the 5 research-tested roles (safety, blend, contrarian, FV, EV)
  - Given a custom configuration, then the system validates role distribution and warns if it diverges significantly from tested configurations
  - Given custom mode, then the performance comparison against presets is shown in real-time

---

## 15. Correlated Elimination Risk Score

**Description:** A named, visible "Correlation Score" shown on the portfolio dashboard every week. Makes the invisible portfolio risk visible with an emotional, visceral metric.

**V1 Pre-Launch** | Sprint Group: C

### Tasks

#### 15.1 Build correlation score calculation
- **Size:** M
- **Category:** Analytics
- **Dependencies:** None (uses existing Portfolio Diversification Mode logic)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a user's entries and proposed picks for the week, when the correlation score is calculated, then a percentage (0-100%) represents how correlated their entries' fates are
  - Given entries all picking the same team, then correlation score is 100%
  - Given fully diversified entries with no team overlap, then correlation score approaches 0%
  - Given the calculation, then an uncoordinated baseline score is computed for comparison (what a random pick set would produce)

#### 15.2 Build correlation score dashboard widget
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 15.1, 2.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the portfolio dashboard, when the correlation widget renders, then the current week's correlation score is displayed prominently with a gauge or visual indicator
  - Given a high correlation score (>70%), then the widget displays red with "High Risk" label
  - Given a low correlation score (<30%), then the widget displays green with "Well Diversified" label
  - Given the widget, then the uncoordinated baseline is shown for comparison ("Your portfolio: 23% correlated vs 67% for uncoordinated picks")

#### 15.3 Build correlation alert system
- **Size:** S
- **Category:** Analytics
- **Dependencies:** 15.1, 12.1 (notification events)
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given a correlation score spike above a threshold (default 70%), when detected, then an alert is generated in the notification system
  - Given the alert, then it identifies which entries are correlated and suggests diversification moves
  - Given the alert, then it fires when picks are saved (not just on page view) to catch pre-submission risk

#### 15.4 Build week-over-week correlation trend
- **Size:** S
- **Category:** Analytics
- **Dependencies:** 15.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given correlation scores computed weekly, when the trend view renders, then a sparkline or mini chart shows correlation over the last 4 weeks
  - Given the trend, when correlation is increasing, then a "trending up" indicator warns the user
  - Given historical correlation data, then it persists per-pool for season-long analysis

---

## 16. Personalization Anti-Dilution

**Description:** Technical and marketing feature making SurvivorPulse's personalized recommendations visible and weaponizing PoolGenius's structural inability to offer personalized multi-entry coordination.

**V1 Pre-Launch (marketing); Post-Launch (technical deep integration)** | Sprint Group: C

### Tasks

#### 16.1 Audit current personalization in recommendation engine
- **Size:** S
- **Category:** Core Engine
- **Dependencies:** None
- **Agent:** Felix
- **Acceptance Criteria:**
  - Given the existing recommendation engine, when audited, then a document confirms which inputs are user-specific (entry history, pool composition, remaining team availability)
  - Given the audit, then any gaps where recommendations are NOT personalized are identified
  - Given the audit, then a "personalization depth" metric is defined (e.g., "recommendations use 5 user-specific inputs")

#### 16.2 Build personalization visibility layer
- **Size:** M
- **Category:** UX/Design
- **Dependencies:** 16.1, 2.1
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given a recommendation, when displayed, then a "Personalized for you" badge is visible with expandable detail showing which personal factors influenced the recommendation
  - Given the detail view, then factors listed include: your remaining teams, your entry history, your pool's field size, your portfolio architecture, and your pool's buyback status
  - Given two different users in the same pool, when they view recommendations, then the displayed factors differ to demonstrate personalization

#### 16.3 Create anti-dilution marketing copy and assets
- **Size:** M
- **Category:** Marketing/Content
- **Dependencies:** 16.1
- **Agent:** Sky
- **Acceptance Criteria:**
  - Given the anti-dilution positioning, when marketing copy is created, then it includes: competitive comparison (without naming competitors), personalization value proposition, and the subscriber dilution argument
  - Given the copy, then variations exist for: website hero section, ROI calculator sidebar, social media, and email campaigns
  - Given the copy, then it cites the research finding that recommendations are computed against user-specific factors with zero subscriber-to-subscriber dilution
  - Given the assets, then a visual infographic contrasts "one-size-fits-all" vs "personalized portfolio intelligence"

#### 16.4 Implement in-app competitive comparison module
- **Size:** S
- **Category:** Marketing/Content
- **Dependencies:** 16.2
- **Agent:** Deb
- **Acceptance Criteria:**
  - Given the pricing or subscription page, when the comparison module renders, then it shows SP's personalization advantage without naming specific competitors (e.g., "Most tools give all subscribers the same picks...")
  - Given the module, then it includes a concrete example: "With 10 entries, your picks are coordinated across YOUR specific remaining teams, not a generic leaderboard"
  - Given the module, then it links to the ROI calculator for personalized value proof

---

## Critical Path Analysis

The critical path to August 15 V1 launch runs through:

```
Week 1-2 (May 1-14):
  [1.1] IA Audit (S) + [2.1] Token Extraction (M) + [13.1] Buyback Params (S) + [14.1] Preset Configs (M) + [8.1] Sim Design (S)

Week 3-4 (May 15-28):
  [1.2] IA Nav Structure (M) + [4.1] ROI Engine (M) + [15.1] Correlation Calc (M)

Week 5-6 (Jun 1-14):
  [1.3] Wireframes (M) + [2.2] Dark Theme (M) + [4.2] ROI Frontend (M) + [13.2] Buyback Switching (L)

Week 7-8 (Jun 15-28):
  [1.4] Nav Shell Build (L) + [2.3] Core Components (L) + [14.2] Preset Engine (L) + [12.1] Notification Events (M)

Week 9-10 (Jul 1-14):
  [1.5] Re-route Pages (M) + [2.4] Data Components (L) + [3.1] BT Analysis (S) + [10.1] Context Engine (M) + [12.2] Email Templates (M)

Week 11-12 (Jul 15-28):
  [3.2] BT Component Port (XL) + [1.6] Dashboard (M) + [15.2] Correlation Widget (M) + [12.3] Email Pipeline (M)

Week 13-14 (Jul 29-Aug 11):
  [3.3-3.5] BT Gating/Subscriber/Redirects (M+M+S) + [2.5] QA Pass (S) + [16.2] Personalization UI (M)

Week 15 (Aug 12-15):
  Final integration testing, bug fixes, launch prep
```

**Critical chain:** IA Overhaul (1.1-1.6) -> Back Tester Integration (3.2-3.5) is the longest dependency chain at ~12 weeks. If IA design (1.1-1.3) takes longer than 6 weeks, Back Tester integration is at risk.

**New tasks 1.7-1.10 fit within Sprint Group A/B timeline:** Task 1.8 (eliminated access, M) can start early alongside nav shell backend work. Tasks 1.7 (week navigation, L) and 1.10 (pool history, M) need the nav shell (1.4) first, placing them in Sprint Group B. Task 1.9 (season selector, L) depends on week navigation (1.7), placing it in Sprint Group B/C.

**Parallel tracks that don't block critical path:**
- ROI Analysis (4.x) -- can ship independently
- Buyback Engine (13.x) -- backend-only until UI hooks
- Portfolio Presets (14.x) -- backend-only until UI hooks
- Correlation Score (15.x) -- backend-only until dashboard
- Notification System (12.x, email only) -- independent
- Pool Structure Research (8.x) -- Stan-only, no Felix dependency
- Personalization Marketing (16.3) -- Sky-only, no engineering

---

## Dependency Map Across All 16 Features

```
LEGEND: --> hard dependency | -.-> soft/optional dependency

[1.1 IA Audit] --> [1.2 Nav Structure] --> [1.3 Wireframes] --> [1.4 Nav Shell] --> [1.5 Re-route] --> [1.6 Dashboard]
                                                                    |
                                                                    +--> [1.7 Week Navigation] --> [1.9 Season Selector]
                                                                    +--> [1.8 Eliminated Access] --> [1.10 Pool History]
                                                                    |
[2.1 Tokens] --> [2.2 Dark Theme] --> [2.3 Core UI] --> [2.4 Data UI] --> [2.5 QA]
     |                                                                       
     +--> [All frontend tasks use tokens]

[1.4 Nav Shell] + [2.1 Tokens] + [3.1 BT Analysis] --> [3.2 BT Port] --> [3.3 Free Gate] + [3.4 Subscriber Mode] + [3.5 Redirects]

[4.1 ROI Engine] --> [4.2 Frontend] --> [4.3 Presets] + [4.4 Share] + [4.5 IA Integration]
     |
     +--> [5.1 Allocation Algo] --> [5.2 Advisor Form] + [5.3 Results] + [5.4 Buyback Rec]
                                        |
                                        +--> [6.2 Per-Pool Weights] --> [6.3 Cross-Pool] --> [6.4 Dashboard]

[7.1 Forecast Engine] --> [7.2 Correlation Viz] + [7.3 Scenario Compare] + [7.4 Multi-Week]

[8.1 Sim Design] --> [8.2 Optimize BT] --> [8.3 Execute Sim] --> [8.4 Impact Matrix]
     |
     8.4 -.-> [5.1] + [6.2]

[9.1 Platform Research] --> [9.3 First Integration] --> [9.4 Integration UI]
[9.2 CSV Upload] (independent)

[10.1 Context Engine] --> [10.2 Intake UI] + [10.3 Display]
[10.1] + [14.2] --> [10.4 Engine Integration]

[11.1 PWA] --> [11.2 Mobile Optimize] --> [11.4 Performance]
[11.1] + [12.1] --> [11.3 Push Notifications]

[12.1 Event System] --> [12.2 Email Templates] + [12.3 Email Pipeline] + [12.4 Preferences UI]
[12.5 SMS Research] --> [12.6 SMS Pipeline]
[12.1] --> [15.3 Correlation Alerts]

[13.1 Buyback Params] --> [13.2 Strategy Switching] --> [13.3 Display] + [13.4 Validation]
[13.2] --> [6.2]

[14.1 Preset Configs] --> [14.2 Engine Integration] --> [14.3 Selection UI] + [14.4 Custom Mode]

[15.1 Correlation Calc] --> [15.2 Dashboard Widget] + [15.3 Alert System] + [15.4 Trend]

[16.1 Personalization Audit] --> [16.2 Visibility Layer] + [16.3 Marketing Copy]
[16.2] --> [16.4 Comparison Module]
```

---

## Risk Items

### Undersized tasks
| Task | Concern | Mitigation |
|---|---|---|
| 3.2 BT Component Port (XL) | Could be underestimated if dependency conflicts arise | Prepare iframe fallback plan; start with most complex component first to surface issues early |
| 14.2 Preset Engine Integration (L) | Modifying recommendation engine core logic is risky | Requires thorough backtesting validation; build behind feature flag |
| 13.2 Buyback Strategy Switching (L) | Changes fundamental engine behavior based on pool type | Build as a strategy modifier layer, not core rewrite; extensive unit testing required |

### Unclear requirements
| Task | Issue | Resolution |
|---|---|---|
| 1.2 Nav Structure | Open question: tabs vs sidebar vs top-level pages | Deb to present 2-3 options in wireframes; founder decides |
| 1.3 Dashboard density | Open question: glanceable vs detailed | Deb to wireframe both; default to glanceable for V1, add detail toggle post-launch |
| 6.3 Cross-pool correlation | Combinatorial complexity at 50+ entries across 5 pools | Felix to prototype computation feasibility before full build; may need approximation algorithm |
| 12.5 SMS provider | Provider not yet selected | Rita researches before Felix builds; selection must happen by July 1 for post-launch SMS |

### Temporal data scoping complexity
| Task | Concern | Mitigation |
|---|---|---|
| 1.7 Week-by-week temporal navigation (L) | Displaying data "as of" a specific week while allowing edits that propagate forward is non-trivial. Requires either event-sourced data model, snapshot-per-week storage, or computed temporal views. Forward-propagation of edits (e.g., changing a Week 3 pick updates Weeks 4+ remaining team availability) adds significant data model complexity. | Spike on data model approach early in Sprint Group B. Consider event-sourcing pattern where edits create new events that recompute downstream state. Define clear rules for what "propagates forward" vs what is week-locked. |

### Research-dependent tasks
| Task | Dependency | Risk |
|---|---|---|
| 5.1 Allocation Algorithm | 8.4 Pool Structure Matrix | Can ship MVP with simplified heuristics; full version needs research |
| 6.2 Per-Pool Strategy Weights | 8.4 Pool Structure Matrix | Cannot build meaningfully without research; firm post-launch |
| 8.3 Simulation Study | Backtester performance | May take longer than expected; start early (June) |

### Capacity risks
| Agent | V1 Load | Concern |
|---|---|---|
| Felix | ~30 tasks across existing SPP backlog + 16 new enhancement tasks | Highest bottleneck risk. Existing SPP-7, SPP-8, SPP-12, SPP-15, SPP-16, SPP-58 are must-ship. Enhancement tasks must not crowd these out. |
| Deb | ~20 tasks across IA, design system, and UI work | Heavy front-end load. Needs to sequence IA design (weeks 1-6) before switching to component work. |
| Stan | ~8 tasks (research + validation) | Independent track. No capacity conflict with Felix. |

---

## Sprint Groupings

### Sprint Group A: Foundation (May 1 - June 14)
**Goal:** IA designed and approved, design tokens extracted, buyback and preset backend started

| Task | Agent | Size |
|---|---|---|
| 1.1 IA Audit | Deb | S |
| 1.2 Nav Structure | Deb | M |
| 1.3 Wireframes | Deb | M |
| 2.1 Token Extraction | Deb | M |
| 8.1 Sim Design | Stan | S |
| 13.1 Buyback Params | Felix | S |
| 14.1 Preset Configs | Felix | M |
| 15.1 Correlation Calc | Felix | M |
| 16.1 Personalization Audit | Felix | S |
| 4.1 ROI Engine | Felix | M |
| 1.8 Eliminated Access (backend) | Felix | M |

### Sprint Group B: Core Build (June 15 - July 14)
**Goal:** Nav shell built, design system applied, ROI live, back tester analysis done, buyback engine working

| Task | Agent | Size |
|---|---|---|
| 1.4 Nav Shell | Felix | L |
| 1.5 Re-route Pages | Felix | M |
| 2.2 Dark Theme | Deb | M |
| 2.3 Core UI Components | Deb | L |
| 2.4 Data Components | Deb | L |
| 4.2 ROI Frontend | Deb | M |
| 4.3 ROI Presets | Deb | S |
| 3.1 BT Analysis | Felix | S |
| 13.2 Buyback Switching | Felix | L |
| 14.2 Preset Engine | Felix | L |
| 10.1 Context Engine | Felix | M |
| 12.1 Notification Events | Felix | M |
| 8.2 Optimize BT | Felix | M |
| 1.7 Week Navigation | Felix + Deb | L |
| 1.10 Pool History | Felix + Deb | M |

### Sprint Group B/C: Cross-boundary (starts B, may extend into C)

| Task | Agent | Size |
|---|---|---|
| 1.9 Season Selector | Felix + Deb | L |

### Sprint Group C: Integration & Polish (July 15 - August 11)
**Goal:** Back tester integrated, dashboard live, notifications wired, correlation score visible, personalization marketed

| Task | Agent | Size |
|---|---|---|
| 3.2 BT Component Port | Felix | XL |
| 3.3 Free Gate | Felix | M |
| 3.4 Subscriber Mode | Felix | M |
| 3.5 Redirects | Felix | S |
| 1.6 Dashboard | Felix | M |
| 2.5 QA Pass | Deb | S |
| 4.4 Share ROI | Felix | S |
| 4.5 ROI in IA | Felix | S |
| 13.3 Buyback Display | Deb | S |
| 14.3 Preset UI | Deb | M |
| 15.2 Correlation Widget | Deb | M |
| 15.3 Correlation Alerts | Felix | S |
| 12.2 Email Templates | Deb | M |
| 12.3 Email Pipeline | Felix | M |
| 12.4 Preferences UI | Deb | S |
| 10.2 Context Intake UI | Deb | S |
| 10.3 Recommendation Display | Deb | M |
| 16.2 Personalization Layer | Deb | M |
| 16.3 Marketing Copy | Sky | M |
| 16.4 Comparison Module | Deb | S |
| 13.4 Buyback Validation | Stan | M |
| 8.3 Execute Sim Study | Stan | L |

### Sprint Group D: Post-Launch V1.1 (September - October 2026)
**Goal:** Mobile PWA, multi-entry forecasting, pool advisor MVP, SMS notifications

| Task | Agent | Size |
|---|---|---|
| 7.1 Forecast Engine | Felix | L |
| 7.2 Correlation Viz | Deb | M |
| 7.3 Scenario Compare | Deb | M |
| 7.4 Multi-Week Projection | Felix | L |
| 5.1 Allocation Algo | Felix | L |
| 5.2 Advisor Form | Deb | M |
| 5.3 Advisor Results | Deb | M |
| 5.4 Buyback Rec | Felix | S |
| 11.1 PWA Manifest | Felix | M |
| 11.2 Mobile Optimize | Deb | L |
| 11.3 Push Notifications | Felix | M |
| 11.4 Mobile Performance | Felix | M |
| 10.4 Context-Engine Integration | Felix | L |
| 14.4 Custom Architecture | Deb | M |
| 15.4 Correlation Trend | Deb | S |
| 8.4 Impact Matrix | Stan | M |
| 12.5 SMS Research | Rita | S |
| 12.6 SMS Pipeline | Felix | M |

### Sprint Group E: Post-Launch V1.2 (November - December 2026)
**Goal:** Multi-pool optimization, platform integration

| Task | Agent | Size |
|---|---|---|
| 6.1 Pool Param Capture | Felix | M |
| 6.2 Per-Pool Weights | Felix | L |
| 6.3 Cross-Pool Correlation | Felix | L |
| 6.4 Multi-Pool Dashboard | Deb | M |
| 9.1 Platform Research | Stan | M |
| 9.2 CSV Upload | Felix | M |
| 9.3 First Platform Integration | Felix | XL |
| 9.4 Integration UI | Deb | M |

---

## Size Distribution Summary

| Size | Count | Typical Effort |
|---|---|---|
| S | 38 | 1-2 days |
| M | 54 | 3-5 days |
| L | 30 | 1-2 weeks |
| XL | 9 | 2-3 weeks |
| **Total** | **131** | |

## Agent Assignment Summary

| Agent | Task Count | V1 Pre-Launch | Post-Launch |
|---|---|---|---|
| Felix | 62 | 40 | 22 |
| Deb | 48 | 32 | 16 |
| Stan | 10 | 6 | 4 |
| Sky | 1 | 1 | 0 |
| Rita | 2 | 0 | 2 |

---

*This document is the source of truth for all SurvivorPulse enhancement task breakdown. Update as requirements crystallize, research completes, and sprint progress is made.*
