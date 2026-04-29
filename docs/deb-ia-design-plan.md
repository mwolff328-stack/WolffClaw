# SurvivorPulse: Information Architecture Direction & Design System Application Plan

**Author:** Deb the Designer
**Date:** 2026-04-28
**Status:** Direction document for review

---

## Section 1: Information Architecture Direction

### 1.1 Current IA Problems

The app was built feature-by-feature, and it shows. The IA has accreted rather than been designed. Here are the structural problems:

**Pool-centric hierarchy forces unnecessary drilling.**
The current model is: Pools list > Pool detail > Entry > Entry analytics. A user managing 10 entries across 5 pools has to drill into each pool separately, then into each entry, to do the one thing they actually care about: making their picks for the week. The pool is a container, not the primary object of attention. The entry is.

**Analytics are buried behind navigation.**
The entry analytics dashboard (core metrics, pool dynamics, future planning) is the product's core value. But it lives 3 clicks deep: Pools > Pool > Entry > Analytics. The most important thing is the hardest to reach.

**Disconnected analytical views.**
Pool dynamics, portfolio diversification, coordinated allocation, and backtesting are separate pages/views with no connective tissue. A user can't easily flow from "what does SurvivorPulse recommend?" to "how does this interact with my other entries?" to "what does history say about this strategy?" The analytical engine is powerful but fragmented.

**No portfolio-level view.**
The app has no single screen that answers "across all my entries and pools, what is my total risk posture this week?" Portfolio Diversification Mode and Coordinated Allocation exist as features, but they're not surfaced as a primary organizing concept. For a product positioned as a "portfolio-level risk management engine," this is a critical gap.

**Flat top nav with no hierarchy.**
The header has: logo, My Pools button, Admin button, Account dropdown. There's no sidebar, no persistent navigation, no way to quickly switch between pools or entries. Once inside a pool, the breadcrumb is the only way back.

**Mobile experience is an afterthought.**
The current layout is desktop-first with a hamburger menu. For a product where users might be checking picks on Sunday morning from their phone, mobile needs to be a first-class flow, not a responsive fallback.

**Route structure reflects code organization, not user tasks.**
Routes like `/pools/:poolId/entries/:entryId/analytics` and `/pools/:poolId/data-management` map to developer concepts. Users think in tasks: "set my picks," "check my recommendations," "see my risk."

### 1.2 Proposed IA Model

**Shift from pool-centric to entry-centric with portfolio overlay.**

The fundamental reframe: the primary object is the **entry**, not the pool. Pools are configuration/context. Entries are where the action happens. And the portfolio view across all entries is where the product's unique value lives.

**Three-tier model:**

```
TIER 1: COMMAND CENTER (portfolio-level)
  - Weekly picks workspace (all entries, one screen)
  - Portfolio risk dashboard (correlation, exposure, diversification)
  - Recommendations overview (top picks across all entries)

TIER 2: ENTRY WORKSPACE (entry-level)
  - Entry analytics (core metrics, drilldowns)
  - Pick history and status
  - Pool dynamics for this entry's pool
  - Future planning

TIER 3: CONFIGURATION & REFERENCE
  - Pool management (create, edit, settings, data import)
  - Backtesting / historical analysis
  - Account & subscription
  - Admin (if applicable)
```

### 1.3 Primary Navigation Structure

**Persistent left sidebar (collapsible on mobile) + contextual top bar.**

```
SIDEBAR (persistent)
-----------------------------------------
[SP logo]  SurvivorPulse

COMMAND CENTER
  This Week            ← weekly picks + recs
  Portfolio            ← risk dashboard
  
MY ENTRIES
  Entry 1 (Pool A)     ← direct entry access
  Entry 2 (Pool A)
  Entry 3 (Pool B)
  ...
  + Add Entry

TOOLS
  Back Tester          ← historical analysis
  Games & Spreads      ← reference data

SETTINGS
  Pools                ← pool config/management
  Account
-----------------------------------------
[Week 14 selector]     ← bottom of sidebar, always visible
```

**Top bar (contextual):**
- Shows current context: entry name, pool name, week
- Contains entry-level actions: submit pick, view analytics, pool dynamics
- Week selector also accessible here for quick switching

**Key decisions:**
- Entries listed directly in nav, not nested under pools. This is the biggest IA change. Users manage entries, not pools.
- Week selector is persistent and global. Changing the week updates all views.
- "This Week" is the default landing page. Not "My Pools."
- Pool management moves to Settings tier. You configure pools rarely. You use entries constantly.

### 1.4 Key User Flows Redesigned

#### Flow A: "I want to set up my pools and entries for the week"

**Current:** Pools > Pool > see entries > click entry > modal/page for pick > repeat per entry per pool.

**Proposed:** Land on "This Week" command center.

```
THIS WEEK (command center)
-----------------------------------------
WEEK 14 · Pick Deadline: Sun 1:00 PM ET

┌─────────────────────────────────────────┐
│ ENTRIES NEEDING PICKS (3 of 8)          │
│                                         │
│ Entry "Alpha" (Yahoo Main)              │
│   Recommended: BUF (A grade, 72% win)   │
│   [Select Pick ▼]  [Submit]             │
│                                         │
│ Entry "Bravo" (CBS Pro)                 │
│   Recommended: DET (A- grade, 68% win)  │
│   [Select Pick ▼]  [Submit]             │
│                                         │
│ Entry "Charlie" (Yahoo Main)            │
│   Recommended: PHI (B+ grade, 65% win)  │
│   [Select Pick ▼]  [Submit]             │
│                                         │
│ ── PICKS SUBMITTED (5 of 8) ──────────  │
│ Entry "Delta" → KC ✓                   │
│ Entry "Echo" → BUF ✓                   │
│ ...                                     │
│                                         │
│ [Submit All Remaining]                  │
└─────────────────────────────────────────┘

┌─ PORTFOLIO ALERT ───────────────────────┐
│ ⚠ 3 entries picking BUF this week.      │
│ Correlation risk: HIGH (0.72)           │
│ [View Portfolio →]                      │
└─────────────────────────────────────────┘
```

One screen. All entries. Recommendations inline. Portfolio risk surfaced proactively. Pick submission without leaving the page.

#### Flow B: "I want to see SurvivorPulse's recommendations for my entries"

**Current:** Pool > Entry > Analytics > scroll to recommendations > repeat per entry.

**Proposed:** From "This Week," each entry shows its top recommendation. Click the recommendation to expand a detail panel (right drawer or inline expansion) with:

- Full core metrics table for that entry
- Top 3 alternative picks with grades
- Key risk factors (popularity, future value trade-offs)
- "Why this pick?" explanation

The entry-level analytics dashboard remains available via sidebar click for the full analytical deep-dive (pool dynamics, all 32 teams, future planning). But the 80% case (see recommendation, understand it, submit) lives on the command center.

#### Flow C: "I want to understand my portfolio's risk exposure"

**Current:** No single view exists. User has to mentally aggregate across entries.

**Proposed:** "Portfolio" in sidebar opens the portfolio risk dashboard.

```
PORTFOLIO RISK DASHBOARD
-----------------------------------------
WEEK 14 · 8 entries across 3 pools

┌─ CORRELATION MATRIX ────────────────────┐
│ [Visual grid: entries vs entries]        │
│ Highlights overlapping picks and         │
│ correlated exposure                      │
└─────────────────────────────────────────┘

┌─ TEAM CONCENTRATION ────────────────────┐
│ BUF: 3 entries (37.5%)  ████████ HIGH   │
│ KC:  2 entries (25.0%)  █████   MEDIUM  │
│ DET: 1 entry  (12.5%)  ██      LOW     │
│ PHI: 1 entry  (12.5%)  ██      LOW     │
│ BAL: 1 entry  (12.5%)  ██      LOW     │
└─────────────────────────────────────────┘

┌─ COORDINATED ALLOCATION ────────────────┐
│ Suggested re-allocation to reduce        │
│ correlation while maintaining EV:        │
│                                          │
│ Move "Echo" from BUF → DET              │
│ Portfolio risk: 0.72 → 0.41             │
│ [Apply Suggestions]                      │
└─────────────────────────────────────────┘

┌─ SEASON OUTLOOK ────────────────────────┐
│ Teams used across portfolio (heatmap)    │
│ Future scarcity warnings                 │
│ Projected survival curves                │
└─────────────────────────────────────────┘
```

This view does not exist today. It should be the product's signature screen. It's the thing no spreadsheet can do.

#### Flow D: "I want to explore historical backtesting data"

**Current:** Back Tester is a separate prototype app.

**Proposed:** "Back Tester" lives in the Tools section of the sidebar. It opens within the same app shell but with its own layout optimized for data exploration. The design system is already shared (it originated there), so visual continuity is automatic.

Key integration: from any recommendation in the main app, a "Historical performance" link opens the Back Tester filtered to the relevant team/week/scenario.

#### Flow E: "I want to see my ROI and optimize my entry allocation"

**Current:** No dedicated view. Entry status (alive/eliminated) is visible per-entry, but there's no aggregate performance or allocation optimization.

**Proposed:** Portfolio dashboard includes a "Season Performance" panel:

```
SEASON PERFORMANCE
-----------------------------------------
Total entries: 10
Alive: 7 (70%)
Eliminated: 3
Total invested: $750
Projected return (based on pool sizes): $2,800
Current ROI: +273% (projected)

ENTRY ALLOCATION EFFICIENCY
Pool A (3 entries, $150 invested)
  Alive: 2/3 · EV: +$340
Pool B (4 entries, $400 invested)
  Alive: 3/4 · EV: +$1,200
Pool C (3 entries, $200 invested)
  Alive: 2/3 · EV: +$180

OPTIMIZATION INSIGHT
"Your highest-ROI pool is Pool B. Consider
 allocating more entries there next season."
```

### 1.5 Information Hierarchy

**Level 1: What needs my attention right now?**
- Entries needing picks this week
- Pick deadline countdown
- Portfolio risk alerts (high correlation, concentrated exposure)
- Entry status changes (elimination, survival)

**Level 2: What should I do about it?**
- Recommendations with grades and reasoning
- Coordinated allocation suggestions
- Alternative picks with trade-off analysis

**Level 3: Why should I trust this recommendation?**
- Core metrics (win probability, popularity, EV, composite score)
- Pool dynamics (leverage, field survival, chalk risk)
- Future value analysis (scarcity, flexibility, best week index)

**Level 4: How is my season going overall?**
- Portfolio risk posture
- Season performance and ROI
- Teams used / remaining availability

**Level 5: Reference and configuration**
- Historical backtesting data
- Pool settings and data management
- Games, spreads, and raw data
- Account and subscription

### 1.6 Mobile-First Considerations

The "This Week" command center is the mobile hero screen. It should be designed mobile-first, then expanded for desktop.

**Mobile priorities:**
1. See all entries needing picks, with recommendations, in a vertical scroll
2. Submit picks with minimal taps (ideally: see recommendation > confirm > done)
3. See portfolio alerts inline (not on a separate page)
4. Swipe between entries for detail views

**Mobile navigation:**
- Bottom tab bar (4 tabs): This Week | Portfolio | Entries | More
- "More" opens: Back Tester, Pools, Account, Admin
- Entry detail views slide up as bottom sheets on mobile

**What to deprioritize on mobile:**
- Full correlation matrix (show simplified concentration bars instead)
- 32-team core metrics table (show top 5 + "see all" expandable)
- Pool dynamics deep-dive (available but not prominent)

---

## Section 2: Design System Application Plan

### 2.1 Current State vs Target

**Current main app design:**
- shadcn/ui default theme (slate-based dark mode)
- `#0C1017` header background, `#1a1f2e` borders
- Green accent `#AECC41` for primary CTAs (lime green, consumer-app feel)
- Standard Tailwind font stack (no Inter Variable, no JetBrains Mono)
- No OpenType features, no uppercase structural labels
- shadcn default weight system (400/500/600/700)
- No systematic status color tokens (ad-hoc color usage)
- No surface elevation system (using opaque hex values)

**Target (Back Tester design system):**
- `#08090a` canvas, luminance-based elevation
- Inter Variable + JetBrains Mono
- Indigo-violet brand palette (`#5e6ad2` / `#7170ff`)
- IBM Carbon status tokens
- Sentry uppercase label pattern
- Semi-transparent borders and surfaces
- Max weight 590, signature weight 510

**The gap is significant.** These are different design languages. The current app looks like a generic SaaS dashboard. The target looks like a Bloomberg terminal for survivor pools. The migration is not cosmetic; it redefines the product's personality.

### 2.2 Migration Strategy: Incremental (Recommended)

**Big bang is too risky.** The app is in active development with real users. A full redesign pause would stall feature work for weeks. Instead:

**Phase 1: Foundation tokens (1 week, Size S)**
- Replace CSS custom properties with design system tokens
- Update `tailwind.config.ts` with new color palette, spacing, radius, and font scales
- Add Inter Variable and JetBrains Mono font loading
- Create `theme.css` with all token definitions from DESIGN.md
- No visual changes yet. Just wire up the token layer.

**Phase 2: Shell and navigation (1-2 weeks, Size M)**
- Replace Header component with sidebar navigation (per new IA)
- Implement new layout shell: sidebar + top bar + content area
- Apply canvas/panel/elevated surface tokens to layout containers
- Implement week selector as persistent nav element
- This is the biggest breaking change. Do it once, do it right.

**Phase 3: Core components (2-3 weeks, Size L)**
- Migrate shadcn/ui components to use design system tokens:
  - Buttons (ghost default, brand primary, destructive)
  - Cards and panels (transparent surfaces, semi-transparent borders)
  - Inputs and forms
  - Tables (uppercase headers, JetBrains Mono data cells)
  - Badges (status badges with Carbon color tokens)
  - Dropdowns, dialogs, sheets
- Apply uppercase label pattern to all section headers and table headers
- Switch all numeric displays to JetBrains Mono

**Phase 4: Page-by-page migration (2-3 weeks, Size L)**
- Migrate pages in priority order:
  1. "This Week" command center (new page, built from scratch with design system)
  2. Portfolio risk dashboard (new page, built from scratch)
  3. Entry analytics dashboard (migrate existing, highest-traffic page)
  4. Pool detail page (migrate existing)
  5. Pools list page (migrate existing)
  6. Auth flows (login, signup, password reset)
  7. Settings, account, admin pages
  8. Landing page (last, may need separate marketing treatment)

**Phase 5: Polish and mobile (1-2 weeks, Size M)**
- Mobile-specific layouts and bottom tab navigation
- Animation and transition polish
- Accessibility audit (contrast ratios with dark theme)
- Command palette implementation
- Performance optimization (font loading, token tree-shaking)

### 2.3 Component Inventory

**Exists in shadcn/ui, needs token migration (low effort):**
- Button, Input, Label, Textarea, Checkbox, Switch, Radio Group
- Select, Dropdown Menu, Context Menu, Menubar
- Dialog, Alert Dialog, Sheet, Drawer, Popover, Tooltip
- Accordion, Collapsible, Tabs, Carousel
- Table, Pagination, Scroll Area
- Toast, Toaster, Progress, Skeleton, Separator
- Form, Calendar, Badge, Avatar
- Breadcrumb, Navigation Menu, Command, Hover Card

**Exists in app, needs redesign (medium effort):**
- `Header.tsx` - Replace with sidebar nav + top bar
- `Layout.tsx` - Complete restructure for sidebar layout
- `PoolCard.tsx` - Redesign as entry card with left accent bar
- `RecommendationCard.tsx` - Redesign with design system data typography
- `PageHeader.tsx` - Integrate into new top bar pattern
- `WeekSelector.tsx` - Redesign as design system week nav
- `SeverityBadge.tsx` - Map to Carbon status badge pattern
- `MetricBar.tsx` - Redesign with design system tokens
- All `entry-analytics/` components (CoreMetricsTable, PoolDynamicsTable, etc.)

**New components needed (high effort):**
- Sidebar navigation component with collapsible sections
- Bottom tab bar (mobile navigation)
- Entry card with status accent bar (per DESIGN.md spec)
- Pick grid / team selection tiles
- Correlation matrix visualization
- Team concentration bars
- Portfolio risk summary cards
- "This Week" command center layout
- Pick submission inline component
- Recommendation expansion panel
- Command palette (Cmd+K)

**Design system primitives to build:**
- Surface token utility classes (`surface-canvas`, `surface-panel`, `surface-elevated`)
- Text token utility classes (`text-primary`, `text-secondary`, `text-tertiary`, `text-quaternary`)
- Status badge component (live, safe, at-risk, eliminated, pending)
- Structural label component (uppercase + tracking)
- Data cell component (JetBrains Mono, tabular-nums)
- Data table wrapper with design system styling
- Border token utilities (`border-subtle`, `border-standard`, `border-emphasis`)

### 2.4 Risk Areas

**1. shadcn/ui compatibility (Medium risk)**
shadcn/ui components use CSS custom properties extensively. The design system tokens need to map cleanly to shadcn's expected variable names, or we'll need to override at the component level. The `--background`, `--foreground`, `--primary`, `--border` etc. variables should be remapped to design system values in `theme.css`.

**2. Inter Variable font loading (Low risk)**
Inter Variable with `"cv01", "ss03"` needs to be loaded with the correct OpenType features enabled globally. If the variable font file doesn't include these features, the aesthetic breaks. Need to verify the font file includes the required feature tables. JetBrains Mono is straightforward.

**3. Color contrast in dark theme (Medium risk)**
The design system uses very dark surfaces (`#08090a`) and some text colors may not meet WCAG AA contrast ratios. Key concern: `--text-quaternary` (#62666d) on `--surface-canvas` (#08090a) has a contrast ratio of approximately 3.5:1, which fails AA for normal text. Need to audit and potentially adjust quaternary/tertiary text colors or restrict their usage to decorative/non-essential content.

**4. Navigation IA change is disruptive (High risk)**
Moving from pool-centric to entry-centric navigation changes every URL structure. Need redirect mapping for existing bookmarks and shared links. Also, users with muscle memory for the current flow will need onboarding.

**Mitigation:** Ship behind a feature flag. Allow users to opt in during a transition period. Set up 301 redirects from old URL patterns.

**5. Mobile sidebar on small screens (Medium risk)**
The sidebar navigation pattern doesn't translate directly to mobile. The proposed bottom tab bar is a different navigation paradigm. Need to ensure both patterns stay in sync and that the sidebar collapse/expand on tablet breakpoints feels smooth.

**6. Performance: two font families (Low risk)**
Loading Inter Variable + JetBrains Mono adds ~100-150KB (WOFF2). Use `font-display: swap` and preload the primary font. Consider subsetting JetBrains Mono to digits + common symbols only (saves ~60% of file size).

**7. Lime green (#AECC41) to indigo (#5e6ad2) brand shift (Medium risk)**
The current primary CTA color is lime green. The design system uses indigo-violet. This changes the entire visual identity. Landing page, marketing materials, and any external-facing assets need to be updated in concert. The change is correct (indigo reads as analytical/institutional; lime green reads as casual/consumer), but it needs to be deliberate and communicated.

### 2.5 Estimated Scope

| Phase | Description | Size | Estimated Effort |
|-------|------------|------|-----------------|
| Phase 1 | Foundation tokens, fonts, `theme.css` | S | 1 week |
| Phase 2 | Shell, sidebar navigation, new layout | M | 1-2 weeks |
| Phase 3 | Core component migration (shadcn + custom) | L | 2-3 weeks |
| Phase 4 | Page-by-page migration (7-8 pages + 2 new) | L | 2-3 weeks |
| Phase 5 | Mobile, polish, accessibility, command palette | M | 1-2 weeks |
| **Total** | | **XL** | **7-11 weeks** |

**Parallelization opportunity:** Phase 1 unblocks Phases 2 and 3, which can run in parallel if different developers handle shell vs components. Phase 4 depends on both 2 and 3. Phase 5 is a polish pass on everything.

**Recommended sequencing for a single developer:**
Phase 1 > Phase 2 > Phase 3 (buttons + tables first, then forms + dialogs) > Phase 4 (new pages first, then migrations) > Phase 5.

**Critical path items:**
1. Font loading and token layer (blocks everything)
2. Sidebar navigation + layout shell (blocks page migrations)
3. "This Week" command center (new page, highest impact, can be built early as showcase)

---

## Appendix: Route Map (Proposed)

```
/                           → Redirect to /week (authenticated) or landing
/week                       → This Week command center
/portfolio                  → Portfolio risk dashboard
/entries/:entryId           → Entry workspace (analytics)
/entries/:entryId/picks     → Pick submission (or inline on /week)
/backtester                 → Historical backtesting tool
/games                      → Games & spreads reference
/pools                      → Pool management list
/pools/create               → Create pool
/pools/:poolId/settings     → Pool settings & data management
/account                    → Account & subscription
/admin/*                    → Admin routes (unchanged)
/login, /signup, etc.       → Auth routes (unchanged)
```

**Redirect map (old to new):**
```
/pools/:poolId                          → /pools/:poolId/settings (or /week)
/pools/:poolId/entries/:entryId/analytics → /entries/:entryId
/pools/:poolId/entries/:entryId/picks    → /entries/:entryId/picks
/pools/:poolId/analytics                 → /entries/:entryId (first entry in pool)
/pools/:poolId/data-management           → /pools/:poolId/settings
/dashboard                               → /week
```
