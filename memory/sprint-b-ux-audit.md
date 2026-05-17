# SurvivorPulse — Sprint B UI/UX Audit
**Auditor:** Deb the Designer  
**Date:** 2026-05-16  
**Environment:** Replit dev (Vite HMR, dark mode)  
**Primary URL audited:** `/pools/a1b2c3d4-2023-4000-8000-000000000023`  
**Audit method:** Source-level code review via Vite dev server (React/TSX, CSS, routing); live render not available — interactive states flagged where live review is recommended.

---

## App Stack Summary

| Layer | Technology |
|---|---|
| Framework | React 18 + Vite |
| Routing | Wouter (client-side SPA) |
| Data fetching | TanStack Query |
| Styling | Tailwind CSS 3.x + custom `--sp-*` CSS variables |
| Components | shadcn/ui (Card, Badge, Button, Select, Dialog, etc.) |
| Icons | Lucide React |
| Fonts | Inter (UI), JetBrains Mono (data/code) |
| Mode | Dark mode enforced globally via `<html class="dark">` |

---

## Section 1: Overall Layout & Information Hierarchy

### What I Found
The authenticated shell (`AppShell`) delivers a clean three-zone layout: **fixed sidebar** (desktop), **sticky top bar**, and **main content area**. Mobile gets a **5-tab bottom nav** instead of the sidebar. This is a solid foundation that mirrors professional tools like Linear or Notion.

The Pool Detail page (`/pools/:id`) is the core power screen. Its hierarchy is:

```
TopBar (56px sticky)
  └── AppBreadcrumb → ProfileMenu → current week pill
Main Content (scrollable)
  └── PageHeader (pool name + breadcrumb)
  └── HistoricalDataReminderBanner (conditional)
  └── Pool Description (conditional)
  └── Entry Workspace Card (primary CTA zone)
       └── Entry selector dropdown
       └── EntryPicksWorkspaceContainer
  └── Recommendations (Sparkles icon)
  └── [Pool Entries section — HIDDEN with `{false && ...}`]
```

### Issues
- **Hierarchy imbalance (medium):** The "Entry Workspace" card gets `border-2 border-primary/20 shadow-lg ring-1 ring-primary/10` — strong visual affordance — but the recommendation section below it uses a plain Card. The visual emphasis is almost backwards for first-time users: the entry selector is admin-level plumbing, while recommendations are the core value proposition.
- **Dead code visible in codebase (quick fix):** `{false && (...)}` for the Pool Entries section is developer smell. This block is never rendered. Remove it or move to a feature flag.
- **No page-level `<title>` for authenticated pages (medium):** Only the landing page sets `document.title`. All authenticated pages will show the default app title in browser history, tabs, and bookmarks. Power users managing multiple pools in multiple tabs will have no differentiation.

---

## Section 2: Navigation & Wayfinding

### Sidebar (Desktop)
The sidebar has three sections:
- **Command Center:** This Week, Portfolio, Pools
- **My Entries:** Scrollable list with pool/entry grouping; expand/collapse global toggle; resize handle
- **Tools:** (fetched from `useSidebarData`)

The "My Entries" resize handle is clever but **undiscoverable** — no visual affordance beyond a 1px handle. The global expand/collapse toggle uses `Eye`/`EyeOff` icons, which is non-standard (typically used for visibility, not tree collapse).

### Mobile Bottom Tabs
Five tabs: This Week | Portfolio | Pools | **Entries** (opens sheet) | **More** (opens drawer).

The mixed tab behavior — three navigate, two open overlays — is a pattern risk. Users expect all bottom tabs to navigate. The "Entries" label especially implies navigation.

### Breadcrumbs
TopBar has `AppBreadcrumb`. Pool detail uses a full shadcn `<Breadcrumb>` with Pools → Pool Name. This is correct.

### Issues
- **Sidebar resize handle has no keyboard alternative (medium/accessibility):** No `keyboard` shortcut or resize via keyboard. WCAG 2.1 requires that pointer gestures have a keyboard equivalent.
- **`Eye`/`EyeOff` for tree expand/collapse is semantically wrong (quick fix):** Use `ChevronDown`/`ChevronUp` or `Expand`/`Collapse` iconography. Eye implies "show/hide" not "open/close all."
- **Mixed tab behavior (medium):** "Entries" and "More" open overlays; the other three navigate. Consider an alternative affordance — maybe a sheet-trigger icon rather than a primary bottom tab — or make all tabs navigate.
- **No active highlight logic for Pools tab (quick fix):** The `MobileBottomTabs` checks `location === tab.href || location.startsWith(tab.href + "?")` but `/pools/a1b2c3d4...` would match `/pools` prefix — worth verifying the logic doesn't produce false positives.
- **EntryPickRow links to `/analytics` route that was removed (high):** `EntryPickRow.tsx` links to `/pools/${poolId}/entries/${entryId}/analytics`. The router comment says: "EntryAnalyticsDashboard import removed (Sprint B F3/F10) — analytics route now redirects to /pools/:poolId?entry=:entryId". This should be verified: are These links dead? If so, every entry card on the "This Week" page links to a broken route.

---

## Section 3: Typography & Visual Design

### Fonts
- **Inter** as primary UI font — excellent choice. Variable font weight (100–900), optical sizing (14–32). Modern and legible.
- **JetBrains Mono** for data/code — professional. Used in `code, kbd, samp, pre` by default. Appropriate for a data-dense tool.

### Type Scale Issues
There's a **two-system inconsistency** throughout the codebase:

```tsx
// System A — raw values (newer pattern, e.g., this-week.tsx)
<h1 className="text-[24px] font-bold tracking-[-0.704px]" style={{ color: 'var(--sp-text-primary)' }}>
<p className="text-[14px]" style={{ color: 'var(--sp-text-secondary)', marginTop: '4px' }}>

// System B — Tailwind utilities (older pattern, e.g., pool-detail.tsx)
<h1 className="text-2xl font-bold text-foreground mb-4">
<p className="text-muted-foreground">
```

This split means visual rhythm varies across pages. Some headings have letter-spacing, others don't. Some use `text-[24px]` (explicit px), others `text-2xl` (rem-based). Mixing these creates inconsistency when browser font size preferences change.

### Color Tokens
The app has two parallel color systems:
1. **Tailwind semantic** (`text-foreground`, `bg-muted`, `border-border`) — from shadcn/ui
2. **Custom `--sp-*` tokens** (`var(--sp-text-primary)`, `var(--sp-brand-accent)`, `var(--sp-surface-hover)`)

I couldn't directly fetch the `:root` variable declarations, but the usage is clearly mixed between old (Tailwind) and new (sp-prefixed) patterns. This creates drift risk.

### Issues
- **Typography two-system problem (medium lift):** Standardize on one approach. Recommend migrating to the `--sp-*` token system throughout since it's newer and more explicit. Create a typography utility class set (`.heading-1`, `.body-md`, etc.) rather than raw inline styles.
- **`tracking-[-0.704px]`  is an oddly specific value (quick fix):** This looks like it was copied from Figma. Define it as a Tailwind config value or a named token so it's intentional and consistent.
- **`font-weight: 510` and `font-weight: 590` appear via inline styles (quick fix):** These variable font weights (`font-[510]`, `font-[590]`) are used in a few components. Document them — they're valid for variable fonts but unusual, and inconsistent with the rest of the font weight scale.

---

## Section 4: Component Quality

### Buttons
Using shadcn/ui `Button` with variants `default`, `outline`, `ghost`, `destructive`. Generally consistent. Size variants `sm`/`icon` used appropriately.

### Cards
Standard shadcn `Card`/`CardHeader`/`CardContent`. The Entry Workspace uses a heavily modified version: `border-2 border-primary/20 shadow-lg ring-1 ring-primary/10 bg-primary/[0.02]`. The CardHeader gets `bg-primary/5 border-b border-primary/10`. This works visually but is high specificity and would be hard to theme.

### Selects / Dropdowns
**The pick entry UI uses `<Select>` (180px width) for team selection.** This is a major UX bottleneck:
- 32 NFL teams in a scrollable dropdown is friction-heavy for a data analyst
- The dropdown shows "Used: N times" inline but disables used teams — good, but hard to scan
- 180px is too narrow for long team names with usage counts

### Tables / Pick History
The picks history table uses weeks as columns. For an 18-week regular season, this produces a very wide table. No sticky first column or frozen headers were observed in the code reviewed.

### Badges
Used well: `"default"` for Alive, `"destructive"` for Eliminated. Grade badges use letter grades (A/B/C). The `badge-safe` class is used in `EntryPickRow` — appears to be a custom utility class not from shadcn.

### Dialogs / Modals
The "Enter Picks" modal (`PreviousWeekPicksModal`) is implemented as a **full-screen page takeover** using `fixed inset-0 z-50 bg-background overflow-auto` with its own `<Header>` and `<Footer>` rendered inside. This is heavyweight and breaks the mental model of a modal. It effectively navigates to a new "page" without changing the URL.

### Issues
- **Team selection via dropdown is the wrong pattern (major redesign):** For the core action of picking a team, replace the `<Select>` with a searchable combobox or a card/chip grid. Power users want to scan all options at a glance and keyboard-navigate quickly. The current dropdown is tolerable for 1–2 picks but poor for multi-pick weeks.
- **"Enter Picks" full-screen modal is a navigation anti-pattern (medium lift):** Either make it a true dialog with a contained scroll area, or convert it to a dedicated page with URL routing (`/pools/:id/picks`). The current hybrid approach (no URL change, full-screen overlay) creates back-button confusion.
- **Pick history table needs sticky column (medium):** For multi-week views, the entry name/week column should be sticky on scroll. Live review recommended to confirm whether horizontal scroll works on mobile.
- **Entry Workspace description text is stale (quick fix):** "View and manage your pool entries, make picks, and track your progress throughout the season." — This is the pool-level description. The Entry Workspace card's own subtitle says "Manage picks for your selected entry directly here." One of these is redundant.

---

## Section 5: Mobile-Friendliness / Responsiveness

### What I Can Infer from Code

**Positive signals:**
- `AppShell` uses `max-md:!ml-0` to reset sidebar margin on mobile — correct
- Main content has `pb-[calc(56px+max(16px,env(safe-area-inset-bottom)))]` — excellent safe area handling for iPhone notches
- MobileBottomTabs uses `env(safe-area-inset-bottom)` — correct
- Many components use `sm:flex-row` / `flex-col` responsive patterns
- Mobile bottom tabs: 56px height with `minWidth: "44px", minHeight: "44px"` for touch targets — meets minimum

**Risk signals:**
- The pick entry `Select` trigger is `w-[180px]` — fixed width, will overflow narrow screens if multiple picks per week are shown side by side in `flex-wrap gap-4`
- The picks history table (weeks as columns) has no observed horizontal scroll container
- The Entry Workspace `CardHeader` uses `flex-wrap items-center justify-between` — good, but the content could stack awkwardly at narrow widths with long entry names
- `max-w-7xl` on pool detail: fine for desktop, but on mobile the `px-4 sm:px-6 lg:px-8` padding is appropriate

### Issues
- **Fixed-width pick dropdowns in flex-wrap (medium):** `w-[180px]` selectors in a wrapping flex row may cause odd wrapping at certain breakpoints. Live review needed.
- **Picks history table mobile scroll (medium):** Confirm horizontal scroll container exists; add `overflow-x-auto` wrapper if missing.
- **Touch targets on sidebar section headers (quick fix):** The `+` add-pool link in the sidebar header is `w-5 h-5` (20px) — below the WCAG 44px minimum. The global expand toggle is also 20px. These are sidebar-only (desktop), but worth flagging.

---

## Section 6: Accessibility

### Positive Signals
- Sidebar `<nav>` has `aria-label="Main navigation"` — correct
- Mobile bottom tabs `<nav>` has `aria-label="Main navigation"` — correct (though having two elements with the same label is an issue — see below)
- Hamburger button has `aria-label={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}` — good, dynamic label
- My Entries toggle button has `aria-label` that updates — good
- `<html lang="en" class="dark">` — correct lang attribute

### Issues
- **Two `<nav aria-label="Main navigation">` elements (medium):** Sidebar and MobileBottomTabs both declare `aria-label="Main navigation"`. Screen readers will announce two navigation landmarks with identical names. Differentiate them: "Sidebar navigation" vs. "Mobile navigation" or "Primary navigation" vs. "Secondary navigation."
- **Hover interactions implemented via JS `onMouseEnter`/`onMouseLeave` style changes (medium):** Several interactive elements (sidebar buttons, TopBar hamburger, EntryPickRow) use inline JS event handlers to change `style` on hover rather than CSS `:hover`. This means hover states don't apply when using keyboard focus — keyboard users get no visual focus indicator beyond browser default outline. Add `:focus-visible` styles via CSS.
- **Color-only status indicators in EntryPickRow (medium):** The alive/eliminated status dot is `w-2 h-2 rounded-full` colored green or red. Color alone without text is insufficient for colorblind users. The Badge already shows "Alive"/"Eliminated" text on the pool detail entry list, but on the This Week page EntryPickRow only uses the dot + the badge elsewhere.
- **`<Select>` trigger for picks has no accessible label in some contexts (medium):** The `<label className="text-xs ...">Pick {pickNumber}</label>` is adjacent but not formally associated with the Select via `htmlFor`/`id` relationship. Use the `id` prop on SelectTrigger and `htmlFor` on Label.
- **ARIA roles for pick status states (medium):** When picks are saved successfully, the toast fires but there's no live region update on the picks table to announce the change to screen readers. Consider `aria-live="polite"` on the picks save feedback area.
- **`role` for interactive cards (quick fix):** Some `<div>` elements with `onClick`/`cursor-pointer` (like entry rows in the collapsed Pool Entries view) are missing `role="button"` and `tabIndex={0}`.

---

## Section 7: Empty / Loading / Error States

### Loading States
Multiple loading patterns coexist:
1. **Full-page spinner** (`animate-spin rounded-full h-12 w-12 border-b-2 border-primary`) — used for pool loading, auth check
2. **Skeleton** (`<Skeleton>`) — used in `ThisWeekPage` with a `LoadingSkeleton` component  
3. **Inline spinner** (`h-6 w-6`) — used inside the ExpandedEntryPicks section

The inconsistency is jarring. `ThisWeekPage` has a thoughtful skeleton that preserves layout. `PoolDetail` has a full-screen centered spinner. This implies different development vintages.

### Empty States
- `ThisWeekPage`: Has dedicated `<EmptyState>` and `<AllSubmittedState>` components — excellent
- `PoolDetail` (no entries): "No entries yet. Be the first to join this pool!" — contextual and actionable
- `PortfolioPage`: **"Portfolio correlation view is coming soon."** — This is a placeholder for a core feature. No CTA, no estimated timeline, no workaround. For a paid product, this is a trust/value signal gap.
- No entry selected in Entry Workspace: "Select an entry above to manage picks." or "Loading entry data..." — minimal but functional

### Error States
- API errors use `toast({ title: "Error", description: error.message, variant: "destructive" })` — consistent pattern
- No observed **error boundary** components in the reviewed files. If a child component throws, the whole AppShell would crash without a graceful fallback.
- `PoolDetail` pool-not-found state: Shows breadcrumb + centered "Pool Not Found" message — good but no CTA to navigate back to pools list

### Issues
- **Portfolio page is a stub (major):** This appears in both the sidebar Command Center and the mobile bottom tabs as a first-class destination. Arriving there to find "coming soon" is a significant experience gap for a paying user. Add a proper empty-state with context ("Portfolio analysis aggregates all your entries across pools. Check back when the season begins.") or remove it from primary navigation.
- **Loading states inconsistent across pages (medium):** Standardize on skeleton loading for all content areas. Reserve the spinner for button/action pending states. The This Week page skeleton is the right model to replicate.
- **No error boundary (medium):** Add a top-level `<ErrorBoundary>` around the main content area. Display a friendly error state with a "Reload" action rather than a blank crash.
- **Pool-not-found missing CTA (quick fix):** Add a `<Link href="/pools">← Back to My Pools</Link>` button on the not-found state.

---

## Section 8: Branding Consistency

### Overall Impression
The visual identity is clearly intentional: dark mode, Inter + JetBrains Mono, a custom `--sp-*` token system, `sp-card` utility classes, and structured component patterns. The "SurvivorPulse" brand is analytics-forward and professional.

### What's Consistent
- Dark mode enforced globally
- Lucide icons used throughout (no mixed icon library)
- shadcn/ui as the base component system
- Custom `--sp-*` color tokens for the newer UI surfaces

### What's Not Consistent
- **Old pages use Tailwind semantic tokens; new pages use `--sp-*`** — creates visual drift between pages built in different sprints
- **Some components have raw hardcoded colors** — e.g., `text-amber-500` for warning icons in several places vs. `var(--sp-warning-text)` in others
- **`bg-primary/[0.02]`** — fractional opacity value on the Entry Workspace card is unusual (2% opacity). This likely results in near-invisible differentiation from the base background.
- **TopBar height `56px` and MobileBottomTabs height `56px`** match — good consistency
- **The `PromptPanel` component** (an admin-only dev tool) is mounted in the main `App.tsx` provider tree, meaning it's bundled into every user's session. This is a production hygiene issue.

### Issues
- **Unified design token migration needed (medium lift):** Define a single source of truth for all color/spacing tokens. Deprecate the Tailwind semantic token usage for anything custom. Document which tokens map to which visual concept.
- **Remove PromptPanel from production bundle (medium):** Code-split or conditionally import the `PromptPanel` so it's excluded from non-admin production builds.
- **`text-amber-500` should be `var(--sp-warning-*)` (quick fix):** Multiple instances of `text-amber-500` for warning icons across pool-detail.tsx and elsewhere. Standardize to the token.

---

## Section 9: Specific UX Issues & Friction Points

### 1. Team Selection UX on Pick Entry (Critical)
The core action of the entire product — picking a team — is implemented as a `<Select>` dropdown. For a tool targeting data-driven power users:
- 32+ teams in a scrollable dropdown with no search
- Used teams are disabled but still listed (good) but hard to scan quickly
- Fixed 180px width truncates long names
- Multi-pick weeks show multiple dropdowns side-by-side — cognitive load stacks

**Recommended alternative:** A searchable combobox (Radix Command component) or an inline card grid with team abbreviations and color-coded usage indicators.

### 2. "Enter Picks" Full-Page Modal is Disorienting
`PreviousWeekPicksModal` renders its own `<Header>` and `<Footer>` inside a `fixed inset-0` overlay. It's not a dialog — it's a fake page. No URL change means back button doesn't close it. The breadcrumb inside the modal shows the correct location, but URL-bar confusion persists.

### 3. Inline vs. Modal Picks Workflow Confusion
There are two pick entry workflows:
1. **Entry Workspace (inline)** — on pool detail page, shown inline with a `<Select>` per week
2. **PreviousWeekPicksModal** — full-screen takeover for "enter picks" action

These appear to be parallel implementations with overlapping functionality. The `EntryPicksWorkspaceContainer` (which powers the inline workspace) is also used inside the modal. Why does the same pool detail page have both? The relationship between them is unclear.

### 4. Excessive Production Logging in Recommendations Fetch
The pool dashboard recommendations query (`useQuery` in pool-detail.tsx) contains ~20 `console.log` statements logging full request/response payloads. These should be removed before production or gated behind a debug flag. They expose API response shapes and could slow down devtools.

### 5. Portfolio Page is Navigation Dead-End
Portfolio appears in sidebar, mobile tabs, and presumably is a destination users would navigate to looking for cross-pool risk analysis. It currently shows a card with a TrendingUp icon and "coming soon" text. No action, no workaround. This should be deprioritized in navigation until it exists.

### 6. Historical Week Viewing UX
The app supports viewing any past week via the sidebar week selector. When viewing historically, a banner appears ("Viewing historical Week X. Pick submission is disabled."). This is helpful but:
- The banner appears inside `AppShell` at the top of the content area, not in the TopBar — it could be missed
- The "Submit" buttons presumably become disabled, but it's unclear whether they show a disabled state or disappear entirely

---

## Section 10: Quick Wins vs. Larger Redesign Work

### Quick Wins (< 1 day each)
| # | Issue | Effort |
|---|---|---|
| QW1 | Fix `Eye`/`EyeOff` icons → `ChevronDown`/`ChevronUp` for My Entries expand toggle | 30 min |
| QW2 | Add `document.title` updates for all authenticated page routes | 1 hr |
| QW3 | Remove `{false && ...}` dead code block from pool-detail | 15 min |
| QW4 | Standardize `text-amber-500` → `var(--sp-warning-*)` token across files | 1 hr |
| QW5 | Add "Back to My Pools" CTA on pool-not-found state | 30 min |
| QW6 | Remove console.log statements from recommendations query (or gate behind flag) | 1 hr |
| QW7 | Associate `<Label htmlFor>` with `<SelectTrigger id>` in pick entry form | 30 min |
| QW8 | Add `role="button" tabIndex={0}` to clickable `<div>` elements | 1 hr |
| QW9 | Differentiate the two `<nav aria-label="Main navigation">` elements | 30 min |
| QW10 | Add Pool-not-found back-link CTA | 20 min |

### Medium Lifts (1–3 days)
| # | Issue | Effort |
|---|---|---|
| M1 | Standardize loading states — skeleton everywhere, spinner for actions only | 2 days |
| M2 | Add top-level ErrorBoundary with graceful crash UI | 1 day |
| M3 | Keyboard focus styles for hover-JS-only interactive elements | 1 day |
| M4 | Mobile-audit picks table — add `overflow-x-auto` wrapper, verify fixed-width select wrapping | 1 day |
| M5 | Code-split PromptPanel out of main bundle | 0.5 day |
| M6 | Clarify inline vs. modal picks workflow — document or consolidate | 1 day |
| M7 | Convert `PreviousWeekPicksModal` to a routed page (`/pools/:id/picks/:entryId`) | 2 days |
| M8 | Sidebar resize handle: add keyboard shortcut or button alternative | 1 day |

### Major Redesigns (1 week+)
| # | Issue | Effort |
|---|---|---|
| R1 | Replace `<Select>` team picker with searchable combobox or card grid | 1 week |
| R2 | Unified design token migration (retire mixed Tailwind + sp-token system) | 1–2 weeks |
| R3 | Portfolio page: build the actual feature or rethink navigation hierarchy | 2–4 weeks |
| R4 | Typography standardization — single scale, token-based, consistent weights | 1 week |

---

## Top 10 Prioritized Recommendations

**Priority ranking based on user impact × implementation cost**

1. **🔴 Fix EntryPickRow analytics link** — The "This Week" page links entries to a removed route. Verify whether a redirect is in place; if not, this is a broken core flow. (Quick fix if redirect exists; medium if not.)

2. **🔴 Replace team picker `<Select>` with searchable combobox** — The core user action of the app is a friction point. For power users with 18 weeks of picks to manage, this matters most. (Major redesign, high ROI.)

3. **🟠 Consolidate or clarify pick entry workflows** — Two parallel implementations (inline workspace + full-screen modal) create user confusion. Decide on one canonical pick entry flow. (Medium lift.)

4. **🟠 Skeleton loading everywhere** — `ThisWeekPage` has it right. The pool detail page doesn't. Inconsistency signals unfinished product. Standardize skeleton loading across all data-fetching screens. (Medium lift.)

5. **🟠 Portfolio page: hide or build** — Surfacing a "coming soon" page in primary navigation (sidebar Command Center + mobile tab 2) undermines product confidence. Either build a minimum viable version or demote it from navigation. (Major for building; quick for hiding.)

6. **🟡 Keyboard accessibility for hover-only interactions** — Hover styles implemented in JavaScript don't apply on keyboard focus. Add `:focus-visible` CSS styles. This affects the entire sidebar, TopBar, and entry row components. (Medium lift.)

7. **🟡 Add error boundary** — No error boundary observed. A single unhandled exception in any component will crash the app. Add a top-level boundary with a recovery UI. (Medium lift, low risk.)

8. **🟡 `document.title` for authenticated pages** — Every page needs a meaningful browser title. This affects tab management and bookmarking — core workflows for power users with multiple pools. (Quick win.)

9. **🟡 Remove excessive console.logging from production** — The recommendations API call logs full request/response payloads. Gate behind a `DEBUG` env flag. (Quick win.)

10. **🟢 Differentiate nav landmark labels** — Two `<nav aria-label="Main navigation">` elements fail screen reader navigation. One-line fix with meaningful labels. (Quick win.)

---

## Audit Caveats

The following areas require **live browser review** to fully assess:

- **Actual rendered color values** for `--sp-*` variables (values not accessible from code inspection alone)
- **Z-index stacking** for modal overlays vs. sidebar vs. TopBar
- **Scroll behavior** in the picks history table on mobile
- **Touch target sizes** verified against actual rendered pixel dimensions
- **Animation/transition performance** (sidebar collapse, skeleton fade-in)
- **Pick workflow interaction states** — what happens visually when a team is selected, pick saved, entry eliminated
- **Recommendation section rendering** — the `Sparkles`-headed recommendation cards below the Entry Workspace
- **The PromptPanel component** — what it looks like and whether it's visible to non-admins

---

*Audit complete. Report written by Deb the Designer for SurvivorPulse Sprint B.*
