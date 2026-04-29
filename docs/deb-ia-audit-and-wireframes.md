# SurvivorPulse: IA Audit, Navigation Design & Wireframes

**Author:** Deb the Designer
**Date:** 2026-04-28
**Tasks:** 1.1 (Page Audit), 1.2 (Navigation Structure), 1.3 (Wireframes)
**Status:** Complete — Ready for founder review

---

## Table of Contents

1. [Task 1.1 — Current Page Inventory & User Flow Audit](#task-11--current-page-inventory--user-flow-audit)
2. [Task 1.2 — New Top-Level Navigation Structure](#task-12--new-top-level-navigation-structure)
3. [Task 1.3 — Wireframes: Key Screens](#task-13--wireframes-key-screens)

---

---

# Task 1.1 — Current Page Inventory & User Flow Audit

## 1.1.1 Active Route Inventory

The app uses **Wouter** (lightweight routing) with a V1 router (`router-v1.tsx`). The V2 router is deprecated and unused.

### Public Routes (no auth required)

| Route | Component | Purpose |
|---|---|---|
| `/` | Landing (if unauth) / Redirect to /pools (if auth) | Entry point |
| `/docs` | DocsPage | Documentation |
| `/signup` | Signup | Account registration |
| `/login` | Login | Authentication |
| `/forgot-password` | ForgotPassword | Password reset request |
| `/reset-password` | ResetPassword | Password reset flow |
| `/terms` | Terms | Terms of service |
| `/privacy` | Privacy | Privacy policy |
| `/founding-full` | FoundingFull | Founding member promo (unprotected) |

### Authenticated Routes (require login, no subscription)

| Route | Component | Purpose |
|---|---|---|
| `/account` | AccountPage | Account & subscription management |
| `/settings` | Settings | User settings |
| `/start` | Start | Post-signup onboarding step |
| `/welcome` | Welcome | Welcome screen |
| `/stripe-success` | StripeSuccess | Stripe subscription success handler |
| `/stripe/success` | StripeSuccess | Stripe success (alternate path) |
| `/stripe-cancel` | StripeCancel | Stripe subscription cancel |
| `/stripe/cancel` | StripeCancel | Stripe cancel (alternate path) |

### Subscriber Routes (require login + active subscription)

| Route | Component | Purpose | Current Nav Path |
|---|---|---|---|
| `/pools` | Pools | Primary pools listing | Header → My Pools |
| `/pools/v1` | Pools | Duplicate of /pools (redundant) | Not linked in nav |
| `/pools/create` | PoolForm | Create a new pool | /pools → button |
| `/pools/edit/:id` | PoolForm | Edit existing pool | /pools/:poolId → action |
| `/pools/games-and-spreads` | Games (readOnly) | Reference data for subscribers | Not linked in nav |
| `/pools/:poolId` | PoolDetail | Pool overview, entries, picks | /pools → click pool card |
| `/pools/:poolId/details` | PoolDetail | Pool detail (duplicate pattern) | Redundant |
| `/pools/:poolId/analytics` | AnalyticsDashboard | Pool-level analytics | /pools/:poolId → Analytics tab |
| `/pools/:poolId/entries/:entryId/analytics` | EntryAnalyticsDashboard | Entry analytics, recommendations | /pools/:poolId → click entry |
| `/pools/:poolId/entries/:entryId/playoffs` | EntryAnalyticsDashboard | Playoff entry analytics | Not linked (seasonal) |
| `/pools/:poolId/entries/:entryId/picks` | **REDIRECT → /pools/:poolId** | ⚠ Dead route — redirects away | N/A |
| `/pools/:poolId/data-management` | DataManagement | Data import/management per pool | /pools/:poolId → Data tab |
| `/dashboard` | Dashboard | Dashboard screen | ⚠ Not reachable (auth redirect goes to /pools) |

### Admin Routes (require login + admin role)

| Route | Component | Purpose |
|---|---|---|
| `/admin` | AdminHub | Admin control panel |
| `/admin/games-and-spreads` | Games | Games/spreads data management |
| `/admin/data-import` | DataImport | Bulk data import tool |
| `/admin/users` | UserManagement | User account administration |
| `/admin/users/:userId/pools` | UserPools | Impersonate / view user pools |
| `/admin/auth-events` | AuthEventsPage | Auth event audit log |
| `/admin/waitlist` | Waitlist | Waitlist management |
| `/admin/stripe-webhook-health` | StripeWebhookHealth | Stripe integration monitoring |
| `/admin/coordinated-allocation` | CoordinatedAllocationPage | CMEA allocation visualization |

---

## 1.1.2 Page Component Inventory (Full)

**Total: 43 page components** across main, admin, v2, and deprecated directories.

### Active Pages (in use by router-v1.tsx)

| Component File | Route(s) | Status |
|---|---|---|
| `landing.tsx` | `/` (unauth) | Active |
| `login.tsx` | `/login` | Active |
| `signup.tsx` | `/signup` | Active |
| `forgot-password.tsx` | `/forgot-password` | Active |
| `reset-password.tsx` | `/reset-password` | Active |
| `terms.tsx` | `/terms` | Active |
| `privacy.tsx` | `/privacy` | Active |
| `docs.tsx` | `/docs` | Active |
| `founding-full.tsx` | `/founding-full` | Active |
| `pools.tsx` | `/pools`, `/pools/v1` | Active (duplicate route) |
| `pool-form.tsx` | `/pools/create`, `/pools/edit/:id` | Active |
| `pool-detail.tsx` | `/pools/:poolId`, `/pools/:poolId/details` | Active (duplicate route) |
| `analytics-dashboard.tsx` | `/pools/:poolId/analytics` | Active |
| `entry-analytics-dashboard.tsx` | `/pools/:poolId/entries/:entryId/analytics`, `.../playoffs` | Active |
| `data-management.tsx` | `/pools/:poolId/data-management` | Active |
| `games.tsx` | `/pools/games-and-spreads`, `/admin/games-and-spreads` | Active (dual use) |
| `dashboard.tsx` | `/dashboard` | ⚠ Active but unreachable (see flags) |
| `settings.tsx` | `/settings` | Active |
| `account.tsx` | `/account` | Active |
| `start.tsx` | `/start` | Active |
| `welcome.tsx` | `/welcome` | Active |
| `stripe-success.tsx` | `/stripe-success`, `/stripe/success` | Active (duplicate paths) |
| `stripe-cancel.tsx` | `/stripe-cancel`, `/stripe/cancel` | Active (duplicate paths) |
| `not-found.tsx` | `*` (catch-all) | Active |
| `admin/admin-hub.tsx` | `/admin` | Active |
| `admin/auth-events.tsx` | `/admin/auth-events` | Active |
| `admin/coordinated-allocation.tsx` | `/admin/coordinated-allocation` | Active |
| `admin/stripe-webhook-health.tsx` | `/admin/stripe-webhook-health` | Active |
| `admin/user-management.tsx` | `/admin/users` | Active |
| `admin/user-pools.tsx` | `/admin/users/:userId/pools` | Active |
| `admin/waitlist.tsx` | `/admin/waitlist` | Active |
| `admin/data-import.tsx` | `/admin/data-import` | Active |

### Orphan / Deprecated Pages (not routed in V1)

| Component File | Status | Notes |
|---|---|---|
| `analytics.tsx` | ⚠ Orphan | Not routed. Appears to be an earlier analytics version. |
| `picks-management.tsx` | ⚠ Orphan | Not routed. Legacy V2 picks editor. |
| `playoff-entry-dashboard.tsx` | ⚠ Orphan | Not routed. Superseded by entry-analytics-dashboard with playoffs param. |
| `pools-hub.tsx` | ⚠ Orphan | V2 pools hub, not routed in V1. |
| `v2-playground.tsx` | ⚠ Orphan | V2 experiment, not routed. |
| `entry-dashboard-v2.tsx` | ⚠ Orphan | Not routed. V2 entry dashboard. |
| `v2/pool-detail.tsx` | ⚠ Orphan | Not routed in V1. |
| `v2/pools.tsx` | ⚠ Orphan | Not routed in V1. |
| `v2-deprecated/V2Layout.tsx` | Deprecated | Not routed. |
| `v2-deprecated/entry-analysis.tsx` | Deprecated | Not routed. |
| `v2-deprecated/entry-dashboard.tsx` | Deprecated | Not routed. |
| `v2-deprecated/pool-command-center.tsx` | Deprecated | Not routed. |
| `v2-deprecated/pool-dashboard.tsx` | Deprecated | Not routed. |
| `v2-deprecated/pools-hub.tsx` | Deprecated | Not routed. |

---

## 1.1.3 Current Navigation Architecture

The app has a **flat sticky top header** (`Header.tsx`). There is no sidebar. Navigation is minimal:

```
┌────────────────────────────────────────────────────────────┐
│  [SP Logo]    [My Pools]    [Admin ▼]    [Account ▼]       │
└────────────────────────────────────────────────────────────┘
```

**Account dropdown:**
- Account Settings → /account
- Sign Out

**Mobile:** Hamburger menu that slides in the same links vertically.

**Deep navigation (inside pools) is breadcrumb-only.** Once inside a pool, the user sees a breadcrumb trail and content tabs (Analytics, Data Management). There is no way to quickly jump to another pool or entry without navigating back to /pools first.

---

## 1.1.4 Top 5 User Journeys — Current State

### Journey 1: Create a Pool

**Goal:** User wants to set up a new survivor pool.

| Step | Action | Screen | Route |
|---|---|---|---|
| 1 | Land on app (authenticated) | Redirect | `/` → `/pools` |
| 2 | See pools list | Pools page | `/pools` |
| 3 | Click "Create Pool" | Pool form | `/pools/create` |
| 4 | Fill form, submit | Pool created | `/pools` |
| 5 | Find new pool, click it | Pool detail | `/pools/:poolId` |
| 6 | Add entries | Pool detail (modal/inline) | `/pools/:poolId` |

**Step count: 6**
**Pain points:** No post-creation "what's next" guidance. Adding entries requires finding the new pool in the list and knowing to interact with the pool detail page.

---

### Journey 2: Make a Pick for an Entry

**Goal:** User wants to submit their pick for this week.

| Step | Action | Screen | Route |
|---|---|---|---|
| 1 | Land on app (authenticated) | Redirect | `/` → `/pools` |
| 2 | See pools list | Pools page | `/pools` |
| 3 | Click into a pool | Pool detail | `/pools/:poolId` |
| 4 | Identify the entry needing a pick | Pool detail | `/pools/:poolId` |
| 5 | Interact with pick UI (inline on pool detail) | Pool detail | `/pools/:poolId` |

**Step count: 5** (but must repeat for each pool and each entry)
**Pain points:** If user has 3 pools with 4 entries each, they must navigate to each pool separately. No unified "all entries needing picks" view. The `/pools/:poolId/entries/:entryId/picks` route REDIRECTS AWAY — any direct link to a pick page fails silently.

---

### Journey 3: View Recommendations for an Entry

**Goal:** User wants to see SurvivorPulse's recommendation for what team to pick.

| Step | Action | Screen | Route |
|---|---|---|---|
| 1 | Land on app (authenticated) | Redirect | `/` → `/pools` |
| 2 | See pools list | Pools page | `/pools` |
| 3 | Click into a pool | Pool detail | `/pools/:poolId` |
| 4 | Click into an entry | Entry analytics | `/pools/:poolId/entries/:entryId/analytics` |
| 5 | Scroll to recommendations section | Entry analytics | (same page) |

**Step count: 5** (per entry — must repeat for each entry in each pool)
**Pain points:** Analytics are the core product value but live 4 clicks deep. No way to see all recommendations across all entries at once. Each entry requires a separate navigation path.

---

### Journey 4: Manage Entries Across Pools

**Goal:** User wants to see the status of all their entries (alive/eliminated) and update info.

| Step | Action | Screen | Route |
|---|---|---|---|
| 1 | Land on app (authenticated) | Redirect | `/` → `/pools` |
| 2 | See pools list | Pools page | `/pools` |
| 3 | Click into Pool A | Pool detail | `/pools/:poolAId` |
| 4 | See entries for Pool A | Pool detail | (same page) |
| 5 | Navigate back | Pools list | `/pools` |
| 6 | Click into Pool B | Pool detail | `/pools/:poolBId` |
| 7 | See entries for Pool B | Pool detail | (same page) |

**Step count: 7** (per additional pool — grows linearly with pool count)
**Pain points:** There is no cross-pool entry view. Status aggregation across pools is mentally manual. No portfolio-level view anywhere in the app.

---

### Journey 5: View Pool Analytics

**Goal:** User wants to understand pool dynamics, chalk risk, leverage metrics.

| Step | Action | Screen | Route |
|---|---|---|---|
| 1 | Land on app (authenticated) | Redirect | `/` → `/pools` |
| 2 | See pools list | Pools page | `/pools` |
| 3 | Click into a pool | Pool detail | `/pools/:poolId` |
| 4 | Click Analytics tab | Pool analytics | `/pools/:poolId/analytics` |
| 5 | OR navigate to entry analytics | Entry analytics | `/pools/:poolId/entries/:entryId/analytics` |

**Step count: 4–5**
**Pain points:** Pool analytics and entry analytics are separate destinations. Pool dynamics (a pool-level metric) and entry analytics (an entry-level view) are disconnected. No way to correlate pool dynamics data with entry recommendations without switching pages.

---

## 1.1.5 Flagged Issues: Dead-Ends, Orphans, Redundancies

### Dead-End States

| Issue | Details |
|---|---|
| **`/dashboard` is unreachable** | `dashboard.tsx` is registered at `/dashboard` but `HomeRoute` redirects authenticated users to `/pools`, never `/dashboard`. The dashboard component exists but users cannot reach it through normal navigation. |
| **`/pools/:poolId/entries/:entryId/picks` is a dead route** | This route is registered in router-v1.tsx but immediately redirects to `/pools/:poolId`. Any bookmarks or links to this path send users somewhere they didn't intend. |
| **No post-pick-submission next step** | After submitting a pick from pool detail, the user is left on the same pool detail screen with no clear "you're done, here's what to do next" path. |
| **`/welcome` floats after onboarding** | The welcome screen has no clear CTA back to the main app flow after first visit. |

### Orphan Pages

| Page | Issue |
|---|---|
| `analytics.tsx` | Registered in the file system, never routed. May conflict with `analytics-dashboard.tsx` naming. |
| `picks-management.tsx` | V2 remnant. Contains pick management UI that was never wired to V1 routing. |
| `playoff-entry-dashboard.tsx` | Not routed; the entry analytics dashboard handles playoffs via query parameter instead. |
| `pools-hub.tsx` | V2 concept (hub navigation pattern) never implemented in V1. |
| `v2-playground.tsx` | Development artifact with no route. |

### Redundant Routes

| Redundancy | Routes | Impact |
|---|---|---|
| Duplicate pool entry points | `/pools` and `/pools/v1` both render `Pools` component | Two routes for one page; `/pools/v1` serves no distinct purpose |
| Duplicate pool detail routes | `/pools/:poolId` and `/pools/:poolId/details` both render `PoolDetail` | Confusing — same page, two URLs |
| Duplicate Stripe success/cancel routes | `/stripe-success` and `/stripe/success` (same for cancel) | Harmless but messy; pick one canonical path |
| Admin games duplicated in subscriber path | `/admin/games-and-spreads` and `/pools/games-and-spreads` | Same component (`games.tsx`), different guard contexts |

### Structural Gaps (Missing Views)

| Gap | Impact |
|---|---|
| **No cross-pool entry view** | Users with 5+ pools must drill into each separately to check all entries |
| **No portfolio risk view** | The product's signature value (portfolio-level risk management) has no dedicated screen |
| **No "this week" aggregated picks screen** | Users must navigate to each pool individually to make picks |
| **No back tester in main app** | Back tester is a separate standalone app; no integration |
| **No ROI calculator** | No tool to help users evaluate subscription value |
| **No global week context** | Week selection is page-specific; no persistent global week state visible in nav |
| **No historical data management view per pool** | No consolidated view of alive/eliminated entries, picks history, or status timeline for a pool across weeks |
| **No way to navigate to previous weeks with scoped entry data** | Cannot select a past week and see entry data (recommendations, picks, portfolio) as of that week only, without subsequent week data bleeding in |
| **No cross-season access to pools/entries** | Previous seasons are not accessible; once a season ends, that data is effectively archived and invisible |
| **No way to edit eliminated entries or pools** | Eliminated entries and pools become dead ends; users cannot view or edit historical data for them |

---

---

# Task 1.2 — New Top-Level Navigation Structure

## 2.1 Design Principles (Approved)

1. **Entry-centric, not pool-centric.** Entries are the primary object. Pools are configuration context.
2. **Three tiers:** Command Center (portfolio-level) → Entry Workspace (entry-level) → Configuration & Reference.
3. **Persistent left sidebar** with entries listed directly (not nested under pools).
4. **2-click rule:** Any feature reachable in 2 clicks from dashboard.
5. **"This Week" is the default landing page** (not "My Pools").
6. **Settings/Account in profile menu**, not top nav.
7. **25+ entries:** Entries collapsible by pool in sidebar.

---

## 2.2 Final Navigation Structure

### Desktop Sidebar (Persistent Left)

```
┌────────────────────────────────┐
│  ⬡ SurvivorPulse              │  ← logo + app name
│                                │
│  COMMAND CENTER                │  ← structural label (uppercase)
│  ◆ This Week                  │  ← default landing; /week
│  ◇ Portfolio                  │  ← risk dashboard; /portfolio
│                                │
│  MY ENTRIES                    │  ← structural label
│  ▸ POOL A  (3 entries)        │  ← collapsible pool group
│    · Alpha  ●                 │  ← entry (● = alive)
│    · Bravo  ●                 │
│    · Charlie ✕                │  ← (✕ = eliminated)
│  ▸ POOL B  (2 entries)        │  ← collapsible
│    · Delta  ●                 │
│    · Echo   ●                 │
│  ─────────────────────         │
│  + Add Entry                   │  ← add entry CTA
│                                │
│  TOOLS                         │  ← structural label
│  ⊙ Back Tester                │  ← /backtester
│  ≡ ROI Calculator             │  ← /tools/roi
│  ◎ Pool Advisor               │  ← /tools/advisor (post-launch)
│  ⊞ Games & Spreads            │  ← /games
│                                │
│  SETTINGS                      │  ← structural label
│  ⊙ Pools                      │  ← /pools (pool mgmt/config)
│                                │
│─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│  [WEEK 14 ▼]                   │  ← global week selector (bottom)
└────────────────────────────────┘
```

### Top Bar (Contextual — Changes Per View)

```
┌──────────────────────────────────────────────────────────────┐
│  [Context: Entry "Alpha" · Pool A · Week 14]   [⊙ Profile ▼] │
└──────────────────────────────────────────────────────────────┘
```

**Profile dropdown contains:**
- Account Settings → `/account`
- Subscription → `/account#subscription`
- Notification Preferences → `/account#notifications`
- Admin Panel (if admin) → `/admin`
- Sign Out

---

## 2.3 All 16 Features Mapped to Navigation

| # | Feature | Navigation Home | Route | Notes |
|---|---|---|---|---|
| 1 | **IA Overhaul** | Foundation (this doc) | N/A | This task IS the output |
| 2 | **Design System Unification** | Global (token layer) | N/A | Applied across all views |
| 3 | **Back Tester Integration** | TOOLS → Back Tester | `/backtester` | Free/gated mode |
| 4 | **ROI Analysis Feature** | TOOLS → ROI Calculator | `/tools/roi` | Free (sales tool) |
| 5 | **Pool & Entry Advisor** | TOOLS → Pool Advisor | `/tools/advisor` | Post-launch V1.1 |
| 6 | **Multi-Pool Optimization** | COMMAND CENTER → Portfolio | `/portfolio#optimization` | Embedded in portfolio view |
| 7 | **Multi-Entry Forecasting** | COMMAND CENTER → This Week | `/week#forecast` | Inline panel on This Week |
| 8 | **Pool Structure Analysis** | Internal/Research | N/A | Powers engine, not user-facing |
| 9 | **Platform Integration** | SETTINGS → Pools | `/pools/:poolId/settings#integrations` | Import flow in pool settings |
| 10 | **Strategy-to-Context Matching** | MY ENTRIES (entry workspace) | `/entries/:entryId#strategy` | Part of entry workspace |
| 11 | **Mobile App (PWA)** | Bottom tab bar (mobile) | All routes | Mobile variant of sidebar |
| 12 | **Notification System** | Profile Menu → Notifications | `/account#notifications` | Preferences in account |
| 13 | **Buyback-Aware Strategy Engine** | MY ENTRIES (entry workspace) | `/entries/:entryId` | Recommendation panel shows buyback rationale |
| 14 | **Portfolio Architecture Presets** | COMMAND CENTER → Portfolio | `/portfolio#presets` | Preset selector on portfolio view |
| 15 | **Correlated Elimination Risk Score** | COMMAND CENTER → Portfolio | `/portfolio` | Correlation widget (prominent) |
| 16 | **Personalization Anti-Dilution** | MY ENTRIES (entry workspace) | `/entries/:entryId` | "Personalized for you" badge on recommendation |
| 17 | **Historical Data Management** | SETTINGS → Pools → Pool History + Entry Workspace (historical weeks) | `/pools/:poolId/settings#history`, `/entries/:entryId?week=8`, `/week?season=2025` | Pool-level timeline, per-week entry editing, cross-season access |

---

## 2.4 Route Map (Proposed)

```
/                      → Redirect: /week (auth) | Landing page (unauth)
/week                  → This Week command center [DEFAULT LANDING]
/portfolio             → Portfolio risk dashboard
/entries/:entryId      → Entry workspace (analytics, picks, pool dynamics)

/backtester            → Back Tester (free/gated | subscriber)
/tools/roi             → ROI Calculator (free)
/tools/advisor         → Pool & Entry Advisor (post-launch)
/games                 → Games & Spreads reference

/pools                 → Pool management list
/pools/create          → Create pool
/pools/:poolId/settings → Pool settings & data management

/account               → Account & subscription & notification preferences

# Season-scoped and historical routes
/week?season=2025      → This Week command center for a previous season
/portfolio?season=2025 → Portfolio dashboard for a previous season
/entries/:entryId?week=8 → Entry workspace scoped to a specific historical week
/entries/:entryId?season=2025 → Entry workspace for a previous season's entry
/pools/:poolId/settings#history → Pool history view (entry timeline, picks history)

# Note: All pool and entry routes work regardless of elimination status.
# An eliminated entry at /entries/:entryId is fully functional — not a dead end.
# Season and week query params scope the view; omitting them defaults to current.

/admin/*               → Admin routes (unchanged)
/login                 → Login
/signup                → Signup
/forgot-password       → Password reset request
/reset-password        → Password reset
/terms                 → Terms
/privacy               → Privacy
```

### Redirect Map (Old → New)

```
/pools                               → /pools (unchanged — pool mgmt, not the landing)
/pools/v1                            → /pools (de-duplicate)
/pools/:poolId                       → /week (or /pools/:poolId/settings for admin)
/pools/:poolId/details               → /pools/:poolId/settings
/pools/:poolId/entries/:entryId/analytics → /entries/:entryId
/pools/:poolId/entries/:entryId/playoffs  → /entries/:entryId?season=playoffs
/pools/:poolId/entries/:entryId/picks     → /week (was already a redirect)
/pools/:poolId/analytics             → /portfolio?pool=:poolId
/pools/:poolId/data-management       → /pools/:poolId/settings#data
/pools/games-and-spreads             → /games
/dashboard                           → /week
/admin/coordinated-allocation        → /portfolio (or keep in admin for now)
/stripe-success                      → /stripe-success (keep; de-duplicate /stripe/success)
/stripe-cancel                       → /stripe-cancel (keep; de-duplicate /stripe/cancel)
```

---

## 2.5 Two-Click Verification

Verifying every feature is reachable in ≤ 2 clicks from the `/week` dashboard:

| Feature/Page | Path from /week | Click Count |
|---|---|---|
| View portfolio risk | Click "Portfolio" in sidebar | 1 |
| Open an entry workspace | Click entry name in sidebar | 1 |
| Open Back Tester | Click "Back Tester" in TOOLS | 1 |
| Open ROI Calculator | Click "ROI Calculator" in TOOLS | 1 |
| View Games & Spreads | Click "Games & Spreads" in TOOLS | 1 |
| Pool management | Click "Pools" in SETTINGS | 1 |
| Create new pool | Click "Pools" → "Create Pool" button | 2 |
| Edit pool settings | Click "Pools" → click pool | 2 |
| Account settings | Click profile avatar → "Account Settings" | 2 |
| Notification preferences | Click profile avatar → "Notification Preferences" | 2 |
| Subscription management | Click profile avatar → "Subscription" | 2 |
| Admin panel | Click profile avatar → "Admin Panel" | 2 |
| Pool Advisor | Click "Pool Advisor" in TOOLS | 1 |
| Correlation risk score | Click "Portfolio" in sidebar | 1 |
| Portfolio presets | Click "Portfolio" → presets section | 1–2 |
| Multi-entry forecasting | Already on "This Week" (inline) | 0 |
| Entry-level buyback rec | Click entry in sidebar | 1 |
| Personalization badge | Click entry in sidebar | 1 |
| Platform integration | Click "Pools" → pool → Integrations tab | 2 |

**All 16 features: ✅ Reachable in ≤ 2 clicks.**

---

## 2.6 Persistent Pool/Entry Context Selector Pattern

**Problem:** When a user navigates to Tools (Back Tester, ROI Calculator), the tool should know which pool they're analyzing without requiring re-entry.

**Solution: Global context selector in the top bar.**

```
┌──────────────────────────────────────────────────────────────┐
│  Context: [2026 ▼]  [Pool A ▼]  [Entry: Alpha ▼]  [Wk 14 ▼] │
└──────────────────────────────────────────────────────────────┘
```

**Behavior:**
- Selecting a pool/entry from the sidebar automatically updates the top bar context.
- Tools read context via URL query params (`?pool=poolAId&entry=entryId&season=2026&week=14`) for shareability.
- "This Week" and "Portfolio" views show ALL entries (context selector reads "All Pools / All Entries").
- When drilling into a single entry workspace, context narrows to that entry.
- Week selector changes are global and persistent (stored in user preferences).
- **Season context** appears as the first element in the context bar. Changing it updates the entire app: sidebar, content, week selector range, and available pools/entries.
- **Historical week indicator:** When viewing a past week (not the current NFL week), the context bar shows a yellow/amber highlight with "Historical View" label and a quick-return link to the current week.
- **Eliminated entry context:** When viewing an eliminated entry, the context bar shows the elimination status (e.g., "✕ Eliminated Wk 8") but all controls remain functional for viewing and editing historical data.

---

## 2.7 Sidebar Entry Grouping: 25+ Entries

**Pattern: Collapsible pool groups with entry status indicators.**

```
MY ENTRIES
▾ POOL A — Yahoo Main  (5 alive / 7 total)
    · Alpha      ●  ALIVE
    · Bravo      ●  ALIVE
    · Charlie    ✕  WK 8
    · Delta      ●  ALIVE  ← needs pick
    · Echo       ●  ALIVE  ← needs pick
    · Foxtrot    ✕  WK 11
    · Golf       ●  ALIVE
▸ POOL B — CBS Pro  (3 alive / 4 total)  ← collapsed
▸ POOL C — Circa  (1 alive / 2 total)   ← collapsed
▸ POOL D — DK Main  (2 alive / 2 total) ← collapsed
──────────────
+ Add Entry
```

**Rules:**
- Pools with entries needing picks this week: **auto-expanded**.
- Pools fully submitted or all eliminated: **auto-collapsed** (but NOT hidden).
- Each entry shows: name, status dot (● alive / ✕ eliminated + week), and a pick-needed badge if relevant.
- **Eliminated entries remain fully clickable and navigable.** Clicking an eliminated entry opens its Entry Workspace where the user can view pick history, review recommendations as of any historical week, and edit entry data. They are not read-only tombstones.
- **Eliminated pools (all entries eliminated) remain visible** in the sidebar. The pool group header shows "0 alive / N total" and can be expanded to access individual eliminated entries.
- Sidebar is scrollable. Up to 50+ entries supported.
- On very long lists (30+ entries), a search/filter bar appears at the top of the MY ENTRIES section.
- Pool group headers show: pool name, alive count / total count.

---

## 2.8 Mobile Navigation Pattern

**Mobile uses a bottom tab bar** (not a sidebar) because the sidebar doesn't translate to mobile thumb zones.

```
┌─────────────────────────────────────────────┐
│  Main content area                          │
│                                             │
│                                             │
└─────────────────────────────────────────────┘
┌─────┬──────────┬────────────┬──────────────┐
│  ◆  │    ◇     │    ⬡       │     ≡        │
│This │Portfolio │  Entries   │    More      │
│Week │          │            │              │
└─────┴──────────┴────────────┴──────────────┘
```

**Tab definitions:**
- **This Week** → `/week`
- **Portfolio** → `/portfolio`
- **Entries** → Entries list (bottom sheet that slides up showing all entries)
- **More** → Drawer containing: Back Tester, ROI Calculator, Pool Advisor, Games & Spreads, Pools (Settings), Account, Admin, Sign Out

**Entry detail views** on mobile open as bottom sheets sliding up over the current view, preserving context.

---

---

# Task 1.3 — Wireframes: Key Screens

> **Conventions:**
> - `[ ]` = interactive element (button, input, dropdown)
> - `[ TEXT ]` = button
> - `[INPUT]` = text input field
> - `▼` = dropdown
> - `●` = alive status indicator
> - `✕` = eliminated status indicator
> - `⚠` = warning/alert indicator
> - `★` = grade indicator
> - `---` = section divider
> - `░░░` = loading skeleton
> - `···` = truncated content

---

## Wireframe 1: "This Week" Command Center

**Route:** `/week`
**Default landing page for authenticated subscribers.**
**Data sources:** See annotations.

---

### 1A — This Week: Loaded State (Desktop)

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Context: All Pools · All Entries · [WEEK 14 ▼]  [👤 ▼] ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║                  ║                                                          ║
║  COMMAND CENTER  ║  WEEK 14  ·  Pick Deadline: Sun Nov 17, 1:00 PM ET      ║
║  ◆ This Week     ║  ┌──────────────────────────────────────────────────┐   ║
║  ◇ Portfolio     ║  │ NEEDS YOUR PICK  3 of 7 alive entries           │   ║
║                  ║  │                                                  │   ║
║  MY ENTRIES      ║  │ Entry "Alpha" · Pool A – Yahoo Main              │   ║
║  ▾ POOL A (5/7)  ║  │   ★ A  RECOMMENDED: BUF BILLS                   │   ║
║    · Alpha  ●    ║  │   Win prob 72%  ·  Popularity 34%  ·  Grade A   │   ║
║    · Bravo  ●    ║  │   [Select Pick ▼ BUF]       [Submit Pick]        │   ║
║    · Delta  ●    ║  │   [View full analysis →]                         │   ║
║    · Echo   ●    ║  │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │   ║
║    · Golf   ●    ║  │ Entry "Delta" · Pool A – Yahoo Main              │   ║
║    · Charlie ✕   ║  │   ★ A-  RECOMMENDED: DET LIONS                  │   ║
║    · Foxtrot ✕   ║  │   Win prob 68%  ·  Popularity 18%  ·  Grade A-  │   ║
║  ▸ POOL B (3/4)  ║  │   [Select Pick ▼ DET]       [Submit Pick]        │   ║
║  ▸ POOL C (1/2)  ║  │   [View full analysis →]                         │   ║
║  ─────────────── ║  │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │   ║
║  + Add Entry     ║  │ Entry "Bravo" · Pool A – Yahoo Main              │   ║
║                  ║  │   ★ B+  RECOMMENDED: PHI EAGLES                  │   ║
║  TOOLS           ║  │   Win prob 65%  ·  Popularity 22%  ·  Grade B+  │   ║
║  ⊙ Back Tester  ║  │   [Select Pick ▼ PHI]       [Submit Pick]        │   ║
║  ≡ ROI Calc     ║  │   [View full analysis →]                         │   ║
║  ⊞ Games        ║  │                              [Submit All (3)]     │   ║
║                  ║  └──────────────────────────────────────────────────┘   ║
║  SETTINGS        ║                                                          ║
║  ⊙ Pools        ║  ┌──────────────────────────────────────────────────┐   ║
║                  ║  │ PICKS SUBMITTED  4 of 7 entries                 │   ║
║  [2026 ▼]        ║  │ Entry "Echo"  → KC Chiefs  ✓  Grade A-          │   ║
║  [WEEK 14 ▼]     ║  │ Entry "Golf"  → BAL Ravens ✓  Grade B+          │   ║
╚══════════════════╣  │ Entry "Delta2"→ DET Lions  ✓  Grade A-          │   ║
                   ║  │ Entry "Foxtrot2"→ BUF Bills ✓ Grade A  [Change] │   ║
                   ║  └──────────────────────────────────────────────────┘   ║
                   ║                                                          ║
                   ║  ┌──────────────────────────────────────────────────┐   ║
                   ║  │ ⚠ PORTFOLIO ALERT                               │   ║
                   ║  │ 3 entries are picking BUF Bills this week.      │   ║
                   ║  │ Correlation risk: HIGH  (0.71)                  │   ║
                   ║  │ Tip: Move "Alpha" or "Foxtrot2" to DET or PHI   │   ║
                   ║  │ [View Portfolio Risk →]                          │   ║
                   ║  └──────────────────────────────────────────────────┘   ║
                   ║                                                          ║
                   ╚══════════════════════════════════════════════════════════╝

DATA SOURCES:
  · Entry list & status     → GET /api/entries (existing)
  · Win probabilities        → GET /api/recommendations (existing optimizer)
  · Popularity %             → GET /api/pool-dynamics (existing)
  · Grades                   → shared/grading/ (existing)
  · Correlation risk score   → NEW ENDPOINT: GET /api/portfolio/correlation-score
  · Pick submission          → POST /api/entries/:entryId/picks (existing, verify)

WEEK NAVIGATION BEHAVIOR:
  · When user changes week selector to a historical week (e.g., Week 8):
    - "NEEDS YOUR PICK" section disappears (can't submit picks for past weeks)
    - Instead shows "WEEK 8 PICKS" with what was picked that week
    - Recommendations shown are as of Week 8 (not current Week 14 recs)
    - A yellow banner appears: "⚠ Viewing Week 8 (Historical) [Return to current →]"
  · Entry data is scoped to the selected week and prior weeks only
  · If user edits a pick in Week 8, the system recalculates Weeks 9-14
    (remaining teams, portfolio state, etc.) and shows a confirmation dialog
```

---

### 1B — This Week: Empty State (No Pools)

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Context: No pools yet  ·  [WEEK 14 ▼]          [👤 ▼] ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║  COMMAND CENTER  ║                                                          ║
║  ◆ This Week     ║     ┌──────────────────────────────────────────┐        ║
║  ◇ Portfolio     ║     │                                          │        ║
║                  ║     │  ⬡                                       │        ║
║  MY ENTRIES      ║     │                                          │        ║
║  (none yet)      ║     │  You don't have any pools or entries     │        ║
║                  ║     │  set up yet.                             │        ║
║  + Add Entry     ║     │                                          │        ║
║                  ║     │  SurvivorPulse works best when you add   │        ║
║  TOOLS           ║     │  your pools and entries so recommendations│       ║
║  ⊙ Back Tester  ║     │  are personalized to your specific teams, │       ║
║  ≡ ROI Calc     ║     │  history, and pool dynamics.             │        ║
║  ⊞ Games        ║     │                                          │        ║
║                  ║     │  [+ Create Your First Pool]              │        ║
║  SETTINGS        ║     │  or                                      │        ║
║  ⊙ Pools        ║     │  [Explore the Back Tester first →]       │        ║
║                  ║     │                                          │        ║
║  ─────────────── ║     └──────────────────────────────────────────┘        ║
║  [WEEK 14 ▼]     ║                                                          ║
╚══════════════════╩══════════════════════════════════════════════════════════╝
```

---

### 1C — This Week: Loading State

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Context: ░░░░░░░░░░  ·  [WEEK ░░ ▼]          [👤 ▼] ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║  COMMAND CENTER  ║                                                          ║
║  ◆ This Week     ║  ┌──────────────────────────────────────────────────┐   ║
║  ◇ Portfolio     ║  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   ║
║                  ║  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ░░░  │   ║
║  MY ENTRIES      ║  │                                                  │   ║
║  ░░░░░░░░░░░░░░  ║  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   ║
║  ░░░░░░░░░░░░░░  ║  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ░░░░░░░░░░░░  │   ║
║  ░░░░░░░░░░░░░░  ║  │                                                  │   ║
║                  ║  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   ║
║  + Add Entry     ║  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░  ░░░░░░░░░░░░░░░  │   ║
╚══════════════════╩══════════════════════════════════════════════════════════╝
```

---

### 1D — This Week: Error State

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Context: Error loading  ·  [WEEK 14 ▼]        [👤 ▼] ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║  COMMAND CENTER  ║                                                          ║
║  ◆ This Week     ║  ┌──────────────────────────────────────────────────┐   ║
║  ◇ Portfolio     ║  │  ⚠ Unable to load recommendations               │   ║
║                  ║  │                                                  │   ║
║  MY ENTRIES      ║  │  There was a problem fetching data for           │   ║
║  ▸ POOL A (5/7)  ║  │  Week 14. Your picks may be unavailable.        │   ║
║  ▸ POOL B (3/4)  ║  │                                                  │   ║
║                  ║  │  If the deadline is approaching, go directly     │   ║
║  + Add Entry     ║  │  to your pool platform to submit picks.          │   ║
║                  ║  │                                                  │   ║
║  TOOLS           ║  │  [Retry]    [View My Entries →]                 │   ║
║  ⊙ Back Tester  ║  │                                                  │   ║
║  ≡ ROI Calc     ║  └──────────────────────────────────────────────────┘   ║
╚══════════════════╩══════════════════════════════════════════════════════════╝
```

---

### 1E — This Week: All Picks Submitted (Complete State)

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Context: All Pools  ·  [WEEK 14 ▼]            [👤 ▼] ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║  COMMAND CENTER  ║                                                          ║
║  ◆ This Week     ║  WEEK 14  ·  All picks submitted ✓                      ║
║  ◇ Portfolio     ║                                                          ║
║                  ║  ┌──────────────────────────────────────────────────┐   ║
║  MY ENTRIES      ║  │ ✓ ALL PICKS IN  7 of 7 entries                  │   ║
║  ▾ POOL A (5/7)  ║  │ Pick window closes in 18h 32m                   │   ║
║    · Alpha  ●    ║  │                                                  │   ║
║    · Bravo  ●    ║  │ Entry "Alpha"  → BUF Bills  ✓  Grade A          │   ║
║    · Delta  ●    ║  │ Entry "Bravo"  → PHI Eagles ✓  Grade B+         │   ║
║    · Echo   ●    ║  │ Entry "Delta"  → DET Lions  ✓  Grade A-         │   ║
║    · Golf   ●    ║  │ Entry "Echo"   → KC Chiefs  ✓  Grade A-         │   ║
║    · Charlie ✕   ║  │ Entry "Golf"   → BAL Ravens ✓  Grade B+         │   ║
║    · Foxtrot ✕   ║  │ [Change Pick] available until deadline          │   ║
║  ▸ POOL B (3/4)  ║  └──────────────────────────────────────────────────┘   ║
║  ▸ POOL C (1/2)  ║                                                          ║
║                  ║  ┌──────────────────────────────────────────────────┐   ║
║  + Add Entry     ║  │ PORTFOLIO THIS WEEK                             │   ║
║                  ║  │ Correlation risk: MEDIUM  (0.43)  ░░░░░░░░░░   │   ║
║  TOOLS           ║  │ 3 pools · 7 entries · $750 at stake             │   ║
║  ⊙ Back Tester  ║  │ [View full portfolio →]                         │   ║
║  ≡ ROI Calc     ║  └──────────────────────────────────────────────────┘   ║
╚══════════════════╩══════════════════════════════════════════════════════════╝
```

---

## Wireframe 2: Portfolio Risk Dashboard

**Route:** `/portfolio`
**The product's signature screen. Does not exist today.**
**This screen is the primary value proposition for multi-entry users.**

---

### 2A — Portfolio Dashboard: Loaded State (Desktop)

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Portfolio Overview  ·  [WEEK 14 ▼]            [👤 ▼] ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║                  ║                                                          ║
║  COMMAND CENTER  ║  PORTFOLIO  —  Week 14  ·  3 pools  ·  7 alive entries ║
║  ◆ This Week     ║                                                          ║
║  ◇ Portfolio     ║  ┌──────────────────┬──────────────┬──────────────────┐ ║
║                  ║  │ ALIVE ENTRIES    │ CORRELATION  │ EV THIS WEEK     │ ║
║  MY ENTRIES      ║  │  7 / 10          │   ★ 0.43     │  +$247 projected │ ║
║  ▾ POOL A (5/7)  ║  │  (3 eliminated)  │  MEDIUM RISK │  (based on probs)│ ║
║    · Alpha  ●    ║  └──────────────────┴──────────────┴──────────────────┘ ║
║    · Bravo  ●    ║                                                          ║
║    · Delta  ●    ║  ┌──────────────────────────────────────────────────┐   ║
║    · Echo   ●    ║  │ TEAM CONCENTRATION  —  Week 14 picks             │   ║
║    · Golf   ●    ║  │                                                  │   ║
║    · Charlie ✕   ║  │  BUF BILLS      ███████████████████  3 entries  │   ║
║    · Foxtrot ✕   ║  │                 43%  ·  HIGH RISK                │   ║
║  ▸ POOL B (3/4)  ║  │                                                  │   ║
║  ▸ POOL C (1/2)  ║  │  DET LIONS      ██████████            2 entries  │   ║
║                  ║  │                 29%  ·  MEDIUM                   │   ║
║  + Add Entry     ║  │                                                  │   ║
║                  ║  │  PHI EAGLES     █████                 1 entry    │   ║
║  TOOLS           ║  │                 14%  ·  LOW                      │   ║
║  ⊙ Back Tester  ║  │                                                  │   ║
║  ≡ ROI Calc     ║  │  KC CHIEFS      █████                 1 entry    │   ║
║  ⊞ Games        ║  │                 14%  ·  LOW                      │   ║
║                  ║  └──────────────────────────────────────────────────┘   ║
║  SETTINGS        ║                                                          ║
║  ⊙ Pools        ║  ┌──────────────────────────────────────────────────┐   ║
║                  ║  │ CORRELATED ELIMINATION RISK                     │   ║
║  ─────────────── ║  │                                                  │   ║
║  [WEEK 14 ▼]     ║  │  ┌────────────────────────────────────────┐     │   ║
╚══════════════════╣  │  │  Correlation Score:  43%  MEDIUM       │     │   ║
                   ║  │  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░       │     │   ║
                   ║  │  │  Baseline (uncoordinated): 67%         │     │   ║
                   ║  │  │  Your savings: 24pp better than random │     │   ║
                   ║  │  └────────────────────────────────────────┘     │   ║
                   ║  │                                                  │   ║
                   ║  │  Week-over-week trend:  ↗  (was 38% last week)  │   ║
                   ║  │  Trend: WORSENING — review BUF concentration    │   ║
                   ║  │                                                  │   ║
                   ║  │  [View coordinated allocation suggestions →]    │   ║
                   ║  └──────────────────────────────────────────────────┘   ║
                   ║                                                          ║
                   ║  ┌──────────────────────────────────────────────────┐   ║
                   ║  │ COORDINATED ALLOCATION SUGGESTIONS              │   ║
                   ║  │                                                  │   ║
                   ║  │  To reduce correlation from 43% → ~27%:         │   ║
                   ║  │                                                  │   ║
                   ║  │  · Move "Alpha" (Pool A)  BUF → DET             │   ║
                   ║  │    New correlation: 0.31  ·  EV impact: -0.3%   │   ║
                   ║  │    [Apply this change]                           │   ║
                   ║  │                                                  │   ║
                   ║  │  · Move "Echo" (Pool B)   BUF → PHI             │   ║
                   ║  │    New correlation: 0.27  ·  EV impact: -0.5%   │   ║
                   ║  │    [Apply this change]                           │   ║
                   ║  │                                                  │   ║
                   ║  │  [Apply All Suggestions]                         │   ║
                   ║  └──────────────────────────────────────────────────┘   ║
                   ║                                                          ║
                   ║  ┌──────────────────────────────────────────────────┐   ║
                   ║  │ SEASON PERFORMANCE                              │   ║
                   ║  │                                                  │   ║
                   ║  │  Total entries started: 10  ·  Alive: 7 (70%)   │   ║
                   ║  │  Total invested: $750  ·  Season: Week 14/18    │   ║
                   ║  │                                                  │   ║
                   ║  │  Teams used (by pool):                          │   ║
                   ║  │  Pool A: KC·BUF·DET·PHI·BAL·LAR·GB             │   ║
                   ║  │  Pool B: KC·BUF·PHI·CIN                         │   ║
                   ║  │  Pool C: BUF·DET                                 │   ║
                   ║  │                                                  │   ║
                   ║  │  Future scarcity: ⚠ BUF used in 3/3 pools      │   ║
                   ║  │  Remaining premium teams: DET·PHI·BAL·SF·CIN    │   ║
                   ║  └──────────────────────────────────────────────────┘   ║
                   ║                                                          ║
                   ║  ┌──────────────────────────────────────────────────┐   ║
                   ║  │ PORTFOLIO ARCHITECTURE                          │   ║
                   ║  │ Current preset: Core/Satellite  (n=10 entries)  │   ║
                   ║  │ 6 core entries (blend)  ·  4 satellite (EV)     │   ║
                   ║  │ [Change Architecture →]                         │   ║
                   ║  └──────────────────────────────────────────────────┘   ║
                   ╚══════════════════════════════════════════════════════════╝

DATA SOURCES:
  · Entry status                → GET /api/entries (existing)
  · Team concentration          → derived from this week's picks across entries
  · Correlation score           → NEW ENDPOINT: GET /api/portfolio/correlation-score
  · Allocation suggestions      → NEW ENDPOINT: GET /api/portfolio/allocation-suggestions
  · Season performance / teams used → NEW ENDPOINT: GET /api/portfolio/season-summary
  · Portfolio architecture      → NEW: stored on user record / pool config
  · EV this week                → existing optimizer score data
```

---

### 2B — Portfolio Dashboard: Empty State (No Picks Submitted)

```
┌──────────────────────────────────────────────────────────────┐
│ PORTFOLIO  —  Week 14  ·  3 pools  ·  7 entries             │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ CORRELATION RISK  —  Awaiting picks                    │  │
│  │                                                        │  │
│  │  Submit your picks on This Week to see your           │  │
│  │  portfolio's correlation risk score for Week 14.      │  │
│  │                                                        │  │
│  │  [Go to This Week →]                                   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  SEASON PERFORMANCE  (available regardless)                  │
│  [season summary shown as above]                             │
└──────────────────────────────────────────────────────────────┘
```

---

### 2C — Portfolio Dashboard: All Entries Eliminated

```
┌──────────────────────────────────────────────────────────────┐
│ PORTFOLIO  —  SEASON COMPLETE  ·  All entries eliminated     │
│                                                              │
│  FINAL PERFORMANCE                                           │
│  Survived through: Week 14 (average)                        │
│  Best entry: "Echo" survived 16 weeks                       │
│  Total invested: $750  ·  Recovered: $0                     │
│                                                              │
│  SP vs naive:  Your entries averaged 2.3 weeks longer       │
│  than field average for this pool type.                     │
│                                                              │
│  NEXT STEPS                                                  │
│  [Run Backtester for next season →]                         │
│  [Update pool entries for next year →]                      │
└──────────────────────────────────────────────────────────────┘
```

---

## Wireframe 3: Entry Workspace

**Route:** `/entries/:entryId`
**Per-entry deep dive: analytics, recommendations, pool dynamics, history.**

---

### 3A — Entry Workspace: Loaded State (Desktop)

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Entry: Alpha  ·  Pool A – Yahoo Main  ·  [WK 14 ▼]    ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║                  ║                                                          ║
║  COMMAND CENTER  ║  ENTRY WORKSPACE  —  "Alpha"                            ║
║  ◆ This Week     ║  Pool A – Yahoo Main  ·  Week 14  ●  ALIVE              ║
║  ◇ Portfolio     ║                                                          ║
║                  ║  ┌──── TABS ─────────────────────────────────────────┐  ║
║  MY ENTRIES      ║  │ [Recommendations]  [Pick History]  [Pool Dynamics] │  ║
║  ▾ POOL A (5/7)  ║  │                   [Future Planning]                │  ║
║  → · Alpha  ●    ║  └────────────────────────────────────────────────────┘  ║
║    · Bravo  ●    ║                                                          ║
║    · Delta  ●    ║  ── RECOMMENDATIONS TAB ─────────────────────────────   ║
║    · Echo   ●    ║                                                          ║
║    · Golf   ●    ║  ┌──────────────────────────────────────────────────┐   ║
║    · Charlie ✕   ║  │ TOP RECOMMENDATION  —  Week 14                  │   ║
║    · Foxtrot ✕   ║  │                                                  │   ║
║  ▸ POOL B (3/4)  ║  │  ★★★  BUF BILLS                                 │   ║
║  ▸ POOL C (1/2)  ║  │  Overall Grade: A  ·  Composite Score: 91/100   │   ║
║                  ║  │                                                  │   ║
║  + Add Entry     ║  │  Win Probability:   72%   ████████████████░░░   │   ║
║                  ║  │  Popularity:        34%   ████████░░░░░░░░░░░   │   ║
║  TOOLS           ║  │  Future Value:      0.82  ████████████████░░░   │   ║
║  ⊙ Back Tester  ║  │  Leverage Score:    0.58  ████████████░░░░░░░   │   ║
║  ≡ ROI Calc     ║  │                                                  │   ║
║  ⊞ Games        ║  │  ✓ Personalized for you                         │   ║
║                  ║  │  › Teams used by this entry: KC, LAR, PHI, GB  │   ║
║  SETTINGS        ║  │  › BUF not yet used  ·  High remaining value   │   ║
║  ⊙ Pools        ║  │  › Pool field: 34% picking BUF (moderate chalk) │   ║
║                  ║  │                                                  │   ║
║  ─────────────── ║  │  [Select BUF →]  [View full breakdown →]        │   ║
║  [WEEK 14 ▼]     ║  └──────────────────────────────────────────────────┘   ║
╚══════════════════╣                                                          ║
                   ║  ┌──────────────────────────────────────────────────┐   ║
                   ║  │ ALTERNATIVE PICKS                               │   ║
                   ║  │                                                  │   ║
                   ║  │  #2  DET LIONS     Grade: A-  Score: 87/100     │   ║
                   ║  │      Win prob: 68%  ·  Popularity: 18%          │   ║
                   ║  │      Trade-off: 4pp less likely to win,         │   ║
                   ║  │      but 16pp less popular (better leverage)    │   ║
                   ║  │      [Select DET →]                              │   ║
                   ║  │                                                  │   ║
                   ║  │  #3  PHI EAGLES    Grade: B+  Score: 79/100     │   ║
                   ║  │      Win prob: 65%  ·  Popularity: 22%          │   ║
                   ║  │      Trade-off: BYE week next week — consider   │   ║
                   ║  │      saving PHI for Wk 15 matchup vs DAL        │   ║
                   ║  │      [Select PHI →]                              │   ║
                   ║  │                                                  │   ║
                   ║  │  #4  BAL RAVENS    Grade: B   Score: 74/100     │   ║
                   ║  │      Win prob: 62%  ·  Popularity: 28%          │   ║
                   ║  │      [Select BAL →]                              │   ║
                   ║  │                                                  │   ║
                   ║  │  [See all 32 teams →]                           │   ║
                   ║  └──────────────────────────────────────────────────┘   ║
                   ║                                                          ║
                   ║  ┌──────────────────────────────────────────────────┐   ║
                   ║  │ CURRENT PICK  —  Week 14                        │   ║
                   ║  │                                                  │   ║
                   ║  │  Selected: BUF BILLS                            │   ║
                   ║  │  Status: Saved (not yet submitted)              │   ║
                   ║  │                                                  │   ║
                   ║  │  [Change Pick ▼]          [Submit Pick]          │   ║
                   ║  └──────────────────────────────────────────────────┘   ║
                   ╚══════════════════════════════════════════════════════════╝

DATA SOURCES:
  · Entry status/history      → GET /api/entries/:entryId (existing)
  · Recommendations           → GET /api/recommendations (existing optimizer, entry-scoped)
  · Metrics table             → GET /api/recommendations (coreScore100, compositeScore100, etc.)
  · "Personalized for you" data → NEW: expose personalization inputs from optimizer
  · Alternative picks         → existing recommendations (ranked list)
  · Pick submission           → POST /api/entries/:entryId/picks (existing)
```

---

### 3B — Entry Workspace: Pick History Tab

```
── PICK HISTORY TAB ──────────────────────────────────────────

┌──────────────────────────────────────────────────────────────┐
│ PICK HISTORY  —  Entry "Alpha"  ·  Pool A – Yahoo Main      │
│                                                              │
│ WK  TEAM        RESULT    GRADE  WIN PROB  POPULARITY        │
│ ──  ──────────  ────────  ─────  ────────  ──────────        │
│  1  KC CHIEFS   WIN ✓     A-     71%       41%               │
│  2  BUF BILLS   WIN ✓     A      74%       38%               │
│  3  DET LIONS   WIN ✓     A      69%       22%               │
│  4  PHI EAGLES  WIN ✓     B+     67%       29%               │
│  5  GB PACKERS  WIN ✓     B      64%       18%               │
│  6  LAR RAMS    WIN ✓     B+     66%       24%               │
│  7  BAL RAVENS  WIN ✓     B+     68%       31%               │
│  8  BYE WEEK   (no game)  —      —         —                 │
│  9  MIN VIKINGS WIN ✓     B      63%       19%               │
│ 10  CIN BENGALS WIN ✓     A-     70%       26%               │
│ 11  SF 49ERS    WIN ✓     A      73%       44%               │
│ 12  CLE BROWNS  LOSS ✗    D+     48%       12%               │  ← ✕ eliminated
│                                                              │
│  ···  Entry eliminated in Week 12 — reactivated via buyback  │
│                                                              │
│ 13  DET LIONS   WIN ✓     A-     67%       19%               │
│ 14  (pending)   —         —      —         —                 │
│                                                              │
│ Teams remaining (not yet used):                              │
│ BUF · HOU · DAL · TEN · MIA · IND · ARI · ATL · CAR ···    │
└──────────────────────────────────────────────────────────────┘
```

---

### 3C — Entry Workspace: Empty State (New Entry, No Picks)

```
── RECOMMENDATIONS TAB ───────────────────────────────────────

┌──────────────────────────────────────────────────────────────┐
│ Entry "NewEntry"  ·  Pool B – CBS Pro  ·  Week 1            │
│                                                              │
│  Welcome to your first week!                                │
│                                                              │
│  SurvivorPulse has analyzed all 32 NFL teams for Week 1     │
│  and generated personalized recommendations based on:       │
│  · Win probabilities                                        │
│  · Field popularity (what others are picking)              │
│  · Future team value (preserving options for later weeks)   │
│  · Your pool's specific dynamics                            │
│                                                              │
│  TOP RECOMMENDATION  —  Week 1                              │
│  [Recommendation card shown as in 3A above]                 │
└──────────────────────────────────────────────────────────────┘
```

---

### 3D — Entry Workspace: Eliminated Entry State (Fully Interactive)

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Entry: Charlie  ·  Pool A – Yahoo Main  ·  [WK 14 ▼]  ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║  MY ENTRIES      ║  ENTRY WORKSPACE  —  "Charlie"                          ║
║  ▾ POOL A (5/7)  ║  Pool A – Yahoo Main  ·  ✕  ELIMINATED — Week 8        ║
║    · Alpha  ●    ║                                                          ║
║    → · Charlie ✕ ║  ┌──────────────────────────────────────────────────┐   ║
║                  ║  │ ✕ ELIMINATED — Week 8                             │   ║
║                  ║  │ Pick: CLE Browns (loss vs PIT)                   │   ║
║                  ║  │                                                  │   ║
║                  ║  │ This entry's data remains fully editable.        │   ║
║                  ║  │ Use the week selector to navigate to any week    │   ║
║                  ║  │ and view/edit picks and recommendations.          │   ║
║                  ║  │                                                  │   ║
║                  ║  │ PERFORMANCE SUMMARY                              │   ║
║                  ║  │ Survived: 7 of 18 weeks  ·  Grade avg: B+       │   ║
║                  ║  │ SP recommended: CIN Bengals (you overrode)       │   ║
║                  ║  │                                                  │   ║
║                  ║  │ ┌──── TABS ──────────────────────────────────┐  │   ║
║                  ║  │ │ [Pick History] [Recommendations] [Edit Data] │  │   ║
║                  ║  │ └────────────────────────────────────────────┘  │   ║
║                  ║  │                                                  │   ║
║                  ║  │ [View full pick history →]                       │   ║
║                  ║  │ [Edit historical picks →]                        │   ║
║                  ║  │ [Use in next season →]                           │   ║
║                  ║  └──────────────────────────────────────────────────┘   ║
╚══════════════════╩══════════════════════════════════════════════════════════╝

KEY DESIGN NOTES:
  · Eliminated entries are NOT read-only. All tabs remain functional.
  · "Edit Data" tab allows changing picks, status, and other historical data.
  · Week selector in sidebar still works — user can navigate to any week
    this entry was alive and see recommendations/portfolio as of that week.
  · Visual treatment: dimmed header bar, strikethrough on status, but all
    controls are interactive and functional.
```

---

### 3E — Entry Workspace: Historical Week View (Week Navigation)

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Entry: Alpha  ·  Pool A  ·  [WK 8 ▼] ⚠ HISTORICAL   ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║                  ║  ┌──────────────────────────────────────────────────┐   ║
║  COMMAND CENTER  ║  │ ⚠ VIEWING HISTORICAL WEEK                        │   ║
║  ◆ This Week     ║  │ You are viewing Week 8 data for this entry.     │   ║
║  ◇ Portfolio     ║  │ Recommendations and portfolio data reflect       │   ║
║                  ║  │ Weeks 1–8 only. No data from Weeks 9–14 shown.  │   ║
║  MY ENTRIES      ║  │ [Return to current week (14) →]                 │   ║
║  ▾ POOL A (5/7)  ║  └──────────────────────────────────────────────────┘   ║
║  → · Alpha  ●    ║                                                          ║
║    · Bravo  ●    ║  ENTRY WORKSPACE — "Alpha" — Week 8 View               ║
║                  ║  Pool A – Yahoo Main  ·  ● ALIVE (as of Week 8)         ║
║                  ║                                                          ║
║                  ║  ┌──── TABS ────────────────────────────────────────┐  ║
║                  ║  │ [Recommendations] [Pick History] [Pool Dynamics]   │  ║
║                  ║  │                  [Future Planning]                  │  ║
║                  ║  └────────────────────────────────────────────────────┘  ║
║                  ║                                                          ║
║                  ║  —— RECOMMENDATIONS TAB (Week 8 context) ——————————   ║
║                  ║                                                          ║
║                  ║  ┌──────────────────────────────────────────────────┐   ║
║  ─────────────── ║  │ WEEK 8 RECOMMENDATION (as of that week)         │   ║
║  [2026 ▼]        ║  │                                                  │   ║
║  [◁  WK 8   ▷]  ║  │  ★ A-  RECOMMENDED: CIN BENGALS                 │   ║
║                  ║  │  Win prob 70%  ·  Popularity 26%  ·  Grade A-  │   ║
║                  ║  │                                                  │   ║
║                  ║  │  YOUR PICK: CLE Browns                          │   ║
║                  ║  │  (You overrode the recommendation)               │   ║
║                  ║  │  [Edit Pick ▼ CLE]  [Save — propagates to Wk9+] │   ║
║                  ║  │                                                  │   ║
║                  ║  │  Teams used (Wk 1–7): KC, BUF, DET, PHI, GB,   │   ║
║                  ║  │  LAR, BAL                                        │   ║
║                  ║  │  Teams remaining (as of Wk 8): 25 teams          │   ║
║                  ║  └──────────────────────────────────────────────────┘   ║
╚══════════════════╩══════════════════════════════════════════════════════════╝

KEY DESIGN NOTES:
  · All entry data is scoped to Week 8 and prior weeks ONLY
  · No information from Weeks 9–14 appears (no future picks, no later recs)
  · Recommendations shown are what SP recommended in Week 8, not current recs
  · "Edit Pick" with save triggers forward propagation:
    - Confirmation dialog: "Changing this pick will update remaining teams
      for Weeks 9–14. Continue?"
    - After save, subsequent weeks recalculate available teams
  · Portfolio tab (if viewed) shows portfolio state as of Week 8
  · Yellow/amber historical banner is always visible when not on current week
```

---

## Wireframe 4: Sidebar Navigation

**The sidebar is the primary persistent navigation element on desktop.**

---

### 4A — Sidebar: Expanded State (Desktop, Full Width)

```
┌──────────────────────────────────────┐
│  ⬡  SurvivorPulse              [⇤]  │  ← collapse button
├──────────────────────────────────────┤
│                                      │
│  COMMAND CENTER                      │  ← structural label (uppercase, muted)
│  ◆  This Week              ← active │  ← active state (left border accent)
│  ◇  Portfolio                        │
│                                      │
├──────────────────────────────────────┤
│                                      │
│  MY ENTRIES                    [+]  │  ← structural label + add entry
│                                      │
│  ▾  POOL A – Yahoo Main      (5/7)  │  ← pool group (expanded; click to collapse)
│     · Alpha                    ●    │  ← entry row: name + status dot
│     · Bravo             ⚠ PICK      │  ← ⚠ = needs pick badge
│     · Delta             ⚠ PICK      │
│     · Echo                     ●    │
│     · Golf                     ●    │
│     · Charlie               ✕ WK8  │  ← eliminated: show week
│     · Foxtrot               ✕ WK11 │
│                                      │
│  ▸  POOL B – CBS Pro         (3/4)  │  ← pool group (collapsed; click to expand)
│                                      │
│  ▸  POOL C – Circa           (1/2)  │
│                                      │
│  ──────────────────────────────────  │
│  + Add Entry                         │
│                                      │
├──────────────────────────────────────┤
│                                      │
│  TOOLS                               │
│  ⊙  Back Tester                      │
│  ≡  ROI Calculator                   │
│  ⊞  Games & Spreads                  │
│                                      │
├──────────────────────────────────────┤
│                                      │
│  SETTINGS                            │
│  ⊙  Pools                            │
│                                      │
├──────────────────────────────────────┤
│  [2026 ▼]                            │  ← season selector
│  [◁  WEEK 14  ▷]                    │  ← week selector (prev/current/next)
└──────────────────────────────────────┘

**Eliminated entries behavior:**
- Eliminated entries (marked with ✕) remain **fully clickable and interactive** in the sidebar
- Clicking an eliminated entry opens its Entry Workspace with full pick history, recommendations as of that week, and editing capability
- Eliminated entries are visually dimmed/muted but never hidden or disabled
- Pool groups with all entries eliminated remain visible and expandable

**Season selector behavior:**
- Default shows current season (e.g., `[2026 ▼]`)
- Dropdown lists all seasons the user has data for (e.g., 2026, 2025, 2024)
- Switching seasons changes the **entire app context**: sidebar repopulates with that season's pools/entries, command center shows that season's data, week selector scopes to that season's weeks
- A visual indicator (e.g., muted banner or badge) appears when viewing a past season to prevent confusion

WIDTH: 260px
ACTIVE ITEM: left 2px accent bar (indigo-violet)
STATUS DOTS: ● green (alive), ✕ red/muted (eliminated), ⚠ amber (needs pick)
POOL GROUPS: pool name + alive/total count; click header to toggle
```

---

### 4B — Sidebar: Collapsed State (Icon-Only Mode)

```
┌────────┐
│  ⬡    │  ← logo
│  [⇥]  │  ← expand button
├────────┤
│        │
│  ◆    │  ← This Week (active)
│  ◇    │  ← Portfolio
│        │
├────────┤
│        │
│  ⊙    │  ← Entries (pool icon, shows entry count badge)
│  [7]  │    badge = total alive entries
│        │
├────────┤
│        │
│  ⊙    │  ← Back Tester
│  ≡    │  ← ROI Calculator
│  ⊞    │  ← Games & Spreads
│        │
├────────┤
│  ⊙    │  ← Pools
│        │
├────────┤
│  14   │  ← week number only
└────────┘

WIDTH: 52px
HOVER: tooltip with label ("This Week", "Portfolio", etc.)
ALL ENTRIES ICON: shows a badge with alive entry count
```

---

### 4C — Sidebar: Long Entry List (25+ Entries, Scrollable)

```
┌──────────────────────────────────────┐
│  ⬡  SurvivorPulse              [⇤]  │
├──────────────────────────────────────┤
│  COMMAND CENTER                      │
│  ◆  This Week                        │
│  ◇  Portfolio                        │
├──────────────────────────────────────┤
│  MY ENTRIES  [🔍]              [+]  │  ← search appears at 10+ entries
│                                      │
│  [🔍 Search entries···]             │  ← filter input
│                                      │
│  ▾  POOL A – Yahoo Main     (8/10)  │
│     · Alpha                    ●    │
│     · Bravo             ⚠ PICK      │
│     · Charlie                  ●    │
│     · Delta                    ●    │
│     · Echo                     ●    │
│     · Foxtrot                  ●    │
│     · Golf                     ●    │
│     · Hotel             ⚠ PICK      │
│     · India             ✕ WK6       │
│     · Juliet            ✕ WK9       │
│                                      │
│  ▾  POOL B – CBS Pro        (5/8)  │  ← auto-expanded (has pending picks)
│     · Kilo              ⚠ PICK      │
│     ···  5 more entries              │  ← collapsed sub-list if >5
│     [ Show all 8 entries ]          │
│                                      │
│  ▸  POOL C – Circa         (3/3)    │  ← collapsed (no pending picks)
│  ▸  POOL D – DK Main       (4/7)   │  ← collapsed
│  ▸  POOL E – OfficePool    (2/4)   │  ← collapsed
│                                      │
│  ──────────────────────────────────  │
│  + Add Entry                         │
│              ↕ scrollable            │
├──────────────────────────────────────┤
│  TOOLS  /  SETTINGS  /  WEEK SELECTOR│  ← pinned to bottom
└──────────────────────────────────────┘

SCROLL BEHAVIOR:
  · MY ENTRIES section scrolls independently
  · TOOLS, SETTINGS, WEEK SELECTOR are always visible (pinned)
  · Max visible entries before scroll: ~12
  · Search filters across all entries and pool names
```

---

### 4D — Sidebar: Mobile Variant (Bottom Tab Bar)

```
Full-screen content area
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                   Main content area                         │
│                   (scrollable)                              │
│                                                             │
│                                                             │
│                                                             │
│                                                             │
│                                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
┌────────────┬───────────────┬───────────────┬───────────────┐
│     ◆      │       ◇       │      ⬡        │      ≡        │
│ This Week  │   Portfolio   │   Entries     │     More      │
│  [3 picks] │               │   [7 alive]   │               │
└────────────┴───────────────┴───────────────┴───────────────┘

BADGE RULES:
  · "This Week" badge: count of entries needing picks
  · "Entries" badge: count of alive entries
  · "More" badge: only if there are admin alerts

"More" drawer (slides up from bottom):
┌─────────────────────────────────────────────────────────────┐
│  ≡ More                                              [✕]    │
│ ─────────────────────────────────────────────────────────── │
│  ⊙  Back Tester                                            │
│  ≡  ROI Calculator                                         │
│  ⊞  Games & Spreads                                        │
│ ─────────────────────────────────────────────────────────── │
│  ⊙  Pool Settings                                          │
│ ─────────────────────────────────────────────────────────── │
│  👤  Account & Subscription                                │
│  🔔  Notification Preferences                              │
│  ⊙  Admin Panel   (if admin)                              │
│ ─────────────────────────────────────────────────────────── │
│  Sign Out                                                   │
└─────────────────────────────────────────────────────────────┘

HEIGHT: 72px (bottom bar)
SAFE AREA: respects iOS/Android home indicator padding
TAP TARGET: min 44×44px per WCAG 2.5.5
```

---

### 4E — "Entries" Tab on Mobile (Bottom Sheet)

When user taps "Entries" tab, a bottom sheet slides up:

```
[drag handle]
┌─────────────────────────────────────────────────────────────┐
│  MY ENTRIES  ·  7 alive of 10 total              [+ Add]    │
│  [🔍 Search···]                                             │
│ ─────────────────────────────────────────────────────────── │
│  ▾  POOL A – Yahoo Main    (5 need picks)                   │
│     Alpha          ⚠ PICK NEEDED      →                    │
│     Bravo          ⚠ PICK NEEDED      →                    │
│     Delta          ● ALIVE            →                    │
│     Echo           ● ALIVE            →                    │
│     Golf           ● ALIVE            →                    │
│     Charlie        ✕ WK 8             →                    │
│     Foxtrot        ✕ WK 11            →                    │
│ ─────────────────────────────────────────────────────────── │
│  ▸  POOL B – CBS Pro                                        │
│  ▸  POOL C – Circa                                          │
└─────────────────────────────────────────────────────────────┘

Tapping an entry row navigates to /entries/:entryId
The bottom sheet closes on navigation
```

---

## Wireframe 5: Pool History View

**Route:** `/pools/:poolId/settings#history`
**Accessed from:** SETTINGS > Pools > Pool detail > History tab
**Shows consolidated historical data for all entries in a pool across all weeks.**

---

### 5A — Pool History: Entry Timeline & Picks (Desktop)

```
╔══════════════════╦══════════════════════════════════════════════════════════╗
║  ⬡ SurvivorPulse ║  Pool: Yahoo Main  ·  Settings  ·  History        [👤 ▼] ║
╠══════════════════╬══════════════════════════════════════════════════════════╣
║                  ║                                                          ║
║  COMMAND CENTER  ║  POOL HISTORY — Yahoo Main                               ║
║  ◆ This Week     ║  Season: [2026 ▼]   Week: [All ▼]                        ║
║  ◇ Portfolio     ║                                                          ║
║                  ║  ┌──── TABS ────────────────────────────────────────┐  ║
║  MY ENTRIES      ║  │ [Settings]  [Data Mgmt]  [Integrations] [History] │  ║
║  ▾ POOL A (5/7)  ║  └────────────────────────────────────────────────────┘  ║
║    ...            ║                                                          ║
║                  ║  ┌──────────────────────────────────────────────────┐   ║
║  SETTINGS        ║  │ ENTRY STATUS TIMELINE                            │   ║
║  ⊙ Pools         ║  │                                                  │   ║
║                  ║  │ Entry    W1  W2  W3  W4  W5  W6  W7  W8 .. W14 │   ║
║  ─────────────── ║  │ Alpha    ●   ●   ●   ●   ●   ●   ●   ●      ●   │   ║
║  [2026 ▼]        ║  │ Bravo    ●   ●   ●   ●   ●   ●   ●   ●      ●   │   ║
║  [◁  WK 14  ▷]  ║  │ Charlie  ●   ●   ●   ●   ●   ●   ●   ✕  ... ✕   │   ║
║                  ║  │ Delta    ●   ●   ●   ●   ●   ●   ●   ●      ●   │   ║
║                  ║  │ Foxtrot  ●   ●   ●   ●   ●   ✕   ✕   ✕  ... ✕   │   ║
║                  ║  │                                                  │   ║
║                  ║  │ ● = alive  ✕ = eliminated  Click cell to edit   │   ║
║                  ║  └──────────────────────────────────────────────────┘   ║
║                  ║                                                          ║
║                  ║  ┌──────────────────────────────────────────────────┐   ║
║                  ║  │ PICKS HISTORY                                    │   ║
║                  ║  │                                                  │   ║
║                  ║  │ Entry    W1   W2   W3   W4   W5  ... W14       │   ║
║                  ║  │ Alpha    KC   BUF  DET  PHI  GB      (pend)    │   ║
║                  ║  │ Bravo    BUF  KC   PHI  DET  BAL     (pend)    │   ║
║                  ║  │ Charlie  DET  PHI  BAL  KC   MIN ... ✕ WK8     │   ║
║                  ║  │ Delta    PHI  DET  KC   BUF  BAL     (pend)    │   ║
║                  ║  │ Foxtrot  BAL  MIN  BUF  KC   ✕  ... ✕ WK5     │   ║
║                  ║  │                                                  │   ║
║                  ║  │ Click any cell to view/edit that entry-week.     │   ║
║                  ║  │ Edits propagate forward to subsequent weeks.     │   ║
║                  ║  │                                                  │   ║
║                  ║  │ [Edit Picks]   [Export CSV]                     │   ║
║                  ║  └──────────────────────────────────────────────────┘   ║
║                  ║                                                          ║
║                  ║  ┌──────────────────────────────────────────────────┐   ║
║                  ║  │ POOL SUMMARY                                     │   ║
║                  ║  │ Total entries: 7  ·  Alive: 5  ·  Eliminated: 2  │   ║
║                  ║  │ Avg survival: 11.2 weeks                         │   ║
║                  ║  │ SP recommendation follow rate: 71%               │   ║
║                  ║  └──────────────────────────────────────────────────┘   ║
╚══════════════════╩══════════════════════════════════════════════════════════╝

DATA SOURCES:
  · Entry status by week   → GET /api/pools/:poolId/entries (with historical week data)
  · Picks by week          → GET /api/pools/:poolId/picks-history (NEW ENDPOINT)
  · Pool summary stats     → derived from entry data
```

---

## Wireframe 6: Season Selector Behavior

**Demonstrates what happens when a user switches from the current season to a previous season.**

---

### 6A — Season Switch: From 2026 to 2025

```
STEP 1: User clicks season selector [2026 ▼]

┌──────────────────────────────────────────┐
│  ...                                     │
│  SETTINGS                                │
│  ⊙  Pools                                │
│                                          │
├──────────────────────────────────────────┤
│  ┌──────────────┐                        │
│  │ ★ 2026       │  ← current (active)     │
│  │   2025       │                          │
│  │   2024       │                          │
│  └──────────────┘                        │
│  [◁  WEEK 14  ▷]                          │
└──────────────────────────────────────────┘


STEP 2: User selects 2025. Entire sidebar and content changes:

┌──────────────────────────────────────────┐
│  ⬡ SurvivorPulse                         │
│                                          │
│  ⚠ VIEWING SEASON 2025 (ARCHIVED)         │  ← prominent banner
│  [Switch to current season (2026) →]     │
│                                          │
│  COMMAND CENTER                          │
│  ◆ This Week (Season Complete)            │
│  ◇ Portfolio                              │
│                                          │
│  MY ENTRIES (2025)                       │  ← labeled with season
│  ▸ OLD POOL X – Yahoo  (2/5)             │  ← 2025's pools
│  ▸ OLD POOL Y – CBS    (0/3)             │  ← fully eliminated
│  ▸ OLD POOL Z – Circa  (1/2)             │
│                                          │
│  TOOLS                                   │
│  ⊙ Back Tester                            │
│  ≡ ROI Calculator                         │
│  ⊞ Games & Spreads                        │
│                                          │
│  SETTINGS                                │
│  ⊙ Pools                                  │
│                                          │
│  [2025 ▼]                                │  ← shows 2025
│  [◁  WK 18  ▷]                            │  ← last week of 2025 season
└──────────────────────────────────────────┘

CONTENT AREA (This Week for 2025):
┌──────────────────────────────────────────────────────────────┐
│  SEASON 2025 — COMPLETE                                          │
│                                                                  │
│  This season has ended. All data is viewable and editable.       │
│  Use the week selector to navigate to any week in 2025.          │
│                                                                  │
│  SEASON SUMMARY                                                  │
│  Entries: 10 total  ·  3 survived to final week                  │
│  Pools: 3  ·  Total invested: $650  ·  Won: $1,200              │
│  SP recommendation follow rate: 68%                              │
│                                                                  │
│  [View 2025 Portfolio →]  [Compare to 2026 →]                    │
└──────────────────────────────────────────────────────────────┘

KEY DESIGN NOTES:
  · Switching seasons is a full context change — sidebar, content, and
    selectors all update to reflect the selected season's data
  · Archived seasons show a prominent visual indicator (banner, dimmed
    chrome, or "ARCHIVED" badge) to prevent confusion
  · All data remains editable in past seasons (picks, entry status, etc.)
  · Week selector auto-sets to the last week of the past season
  · "Switch to current season" link is always visible for quick return
  · Pools with 0 alive entries in past seasons still show (not hidden)
```

---

## Summary: Key Design Decisions

| Decision | Rationale |
|---|---|
| Sidebar, not top nav | Supports the rich MY ENTRIES list; top nav can't accommodate 25+ entries |
| Entries listed directly in sidebar | Eliminates the pool-drill navigation pattern; entries are the primary object |
| "This Week" as default landing | The 80% use case is "make picks this week" — this should be zero clicks away |
| Portfolio as second Command Center item | Portfolio risk is the product's differentiated value; it must be 1 click from anywhere |
| Week selector pinned to sidebar bottom | Week context affects all views; it must persist globally, not per-page |
| Season selector near week selector | Season context affects the entire app; switching seasons changes sidebar, content, and available weeks |
| Eliminated entries remain interactive | Eliminated entries are visually dimmed but fully clickable, editable, and navigable. They are not tombstones. |
| Historical week view scopes data correctly | Navigating to a past week shows only data from that week and prior. No future data leaks into the view. |
| Historical edits propagate forward | Changing a pick in Week 8 recalculates Weeks 9+ (remaining teams, portfolio state). User confirms before save. |
| Previous seasons are fully accessible | Archived seasons are browsable and editable via the season selector. No data is lost or hidden after season end. |
| Pool history view for consolidated data | Per-pool timeline of entry status and picks across all weeks, accessible from pool settings. |
| Tools section separate from Command Center | Back Tester, ROI calc, etc. are analytical aids, not weekly workflows |
| Settings/Pools at bottom of sidebar | Pool management is infrequent configuration; shouldn't compete with daily workflows |
| Profile menu for Account/Subscription/Notifications | These are account-level settings used rarely — profile dropdown is the standard pattern |
| Pool groups auto-expand when picks needed | Reduces friction on pick deadline day; surface what matters right now |
| Search bar appears at 10+ entries | Progressive disclosure — don't show search UI until it's needed |
| Mobile bottom tabs (not sidebar) | Sidebar doesn't translate to mobile thumb zones; bottom tabs are the mobile-native pattern |

---

*Deliverable complete. Ready for founder review.*
*Next steps: 1.4 (Navigation Shell Build) awaits approval of this document.*
