# SurvivorPulse Back Tester — Sprint B UX Design Direction

**Author:** Deb the Designer
**Date:** 2026-05-04
**Sprint:** B (Core Features — Back Tester Integration)
**Tasks covered:** 3.2–3.4 (UX layer), design tasks in 3.x series
**Status:** Ready for Felix handoff

---

## 1. Navigation & Routing

### Placement in the Nav

Back Tester lives under **TOOLS** in the persistent left sidebar — exactly as specified in the Sprint 2 IA design:

```
SIDEBAR
─────────────────────────────────────────
COMMAND CENTER
  This Week
  Portfolio

MY ENTRIES
  [entry list]

TOOLS
  Back Tester          ← here
  Games & Spreads

SETTINGS
  Pools
  Account
─────────────────────────────────────────
```

**Menu item design:**

| State | Rendering |
|---|---|
| Subscriber (default) | "Back Tester" — plain label, no badge |
| Subscriber (new/unvisited) | "Back Tester" + `NEW` badge (info blue `#78a9ff`, disappears after first visit, 30 days post-launch only) |
| Non-subscriber | "Back Tester" — dimmed label (`--sp-text-quaternary`), lock icon (`🔒`), no route access |

Non-subscriber sidebar item is **visible but locked** — clicking it triggers the paywall, not a 404. This is intentional: it signals value without hiding the feature.

### Route Structure

```
/tools/backtester                  → SeasonReplayView (main entry point)
/tools/backtester?season=2024      → Pre-loaded with season param
/tools/backtester?poolId=:id       → Pre-loaded with pool params (subscriber only)
```

No sub-routes needed. The Back Tester is a single-page tool. Query params carry optional preload context. This keeps the URL shareable and bookmarkable.

**Legacy standalone URL redirect:** `survivorpulse-backtester-prototype.replit.app` → 301 to `/tools/backtester`.

### Discovery Path

Users reach Back Tester via:
1. Sidebar nav (primary)
2. Deep link from recommendations: "Historical performance →" on any entry recommendation card opens `/tools/backtester?team=BUF&week=14&season=2026` (future enhancement, not Sprint B scope)
3. Onboarding tooltip on first Dashboard visit (post-launch, not Sprint B scope)

---

## 2. Entry Points & Subscriber Gating

### Non-Subscriber Paywall

When a non-subscriber clicks the locked "Back Tester" sidebar item, they land on the paywall state of `/tools/backtester`. This is **not** a separate page — it's a conditional render within the Back Tester route.

**Paywall layout:**

```
┌─────────────────────────────────────────────────┐
│                                                   │
│   [Back Tester icon — muted/blurred]              │
│                                                   │
│   Back Tester                                     │
│   Replay 5+ years of NFL seasons to validate      │
│   your pick strategies before you commit.         │
│                                                   │
│   ┌─────────────────────────────────────────┐     │
│   │  [Blurred preview of SeasonReplayView]  │     │
│   │  [UI visible but not interactive]       │     │
│   └─────────────────────────────────────────┘     │
│                                                   │
│   Subscriber feature                              │
│                                                   │
│   [Upgrade to Subscriber →]   [Learn more]        │
│                                                   │
└─────────────────────────────────────────────────┘
```

**Design details:**
- Background: blurred snapshot of the actual Back Tester UI at ~10% opacity (not a fake screenshot — actual render with `filter: blur(8px) opacity(0.1)`)
- The paywall card itself sits at `--sp-elevated` (#191a1b) surface elevation, `rounded-xl` (12px), `shadow-sp-dialog`
- "Subscriber feature" label: uppercase structural label, `--sp-text-tertiary`, `letter-spacing: 0.08em`
- Primary CTA: brand button `bg-brand` (#5e6ad2), "Upgrade to Subscriber"
- Secondary CTA: ghost button, "Learn more" → `/account` or pricing section
- No email capture form. Email is already part of the SP auth flow.

**Teaser/preview state:** The blurred render is the teaser. No interactive demo, no restricted mode. The product is subscriber-only and the blur communicates what's behind the gate without giving it away for free. This is cleaner than a time-limited trial and easier to build.

### Subscriber Flow

Subscribers navigating to `/tools/backtester` see the full `SeasonReplayView` immediately — zero friction. No interstitial, no gate, no "welcome" step.

If arriving via a pool parameter link (`?poolId=:id`), the `PoolConfigPanel` pre-populates with that pool's configuration. A dismissible info banner at the top of the config panel reads:

```
Pool parameters loaded from [Pool Name]. You can adjust them below.
```

This banner uses the info token: `--sp-info-subtle` background, `--sp-info-text` text, `--sp-info-border` border.

---

## 3. Component Adaptation Notes

### SeasonReplayView.tsx (668 lines — main orchestrator)

**Role:** Top-level page component. Composes all other Back Tester components.

**Changes needed:**
- Remove the `AccessGate` wrapper. Subscriber check happens at the route level (see Section 2). `SeasonReplayView` can assume the user is authorized.
- Remove any standalone app chrome (custom header, nav, footer). The SP nav shell provides all of this.
- Wrap the full component in `<main className="sp-backtester-layout">` for scoped CSS if needed.
- Ensure it mounts cleanly within the sidebar layout at both collapsed (64px sidebar) and expanded sidebar widths. No fixed-width assumptions.

**No structural changes to the component logic.** It's the orchestrator; its internal composition stays intact.

---

### PoolConfigPanel.tsx (1068 lines — largest component, needs refactor)

**Role:** Strategy builder UI. The user's primary configuration surface.

**Refactor plan:** Break into logical sub-forms. Suggested decomposition:

| Sub-component | Responsibility | Size estimate |
|---|---|---|
| `PoolBasicsForm` | Pool size, entry count, buyback rules | ~150 lines |
| `StrategyTypeSelector` | Strategy template picker (14 templates + ScenarioControls) | ~200 lines |
| `WeightingPanel` | Weight sliders, advanced weight configuration | ~200 lines |
| `SeasonSelector` | Season year + week range | ~80 lines |
| `PoolParamLoader` | Subscriber-only: load from existing pool | ~100 lines |
| `PoolConfigPanel` (shell) | Composes above, manages shared state | ~150 lines |

**Why this matters:**
- Current 1068-line file is a maintenance liability and makes mobile responsiveness hard to retrofit
- Sub-forms can stack vertically on mobile without the entire panel becoming unmanageable
- `PoolParamLoader` can be conditionally rendered only for subscribers — clean subscriber/non-subscriber split without conditional logic scattered throughout the giant file

**Design notes:**
- Each sub-form is a collapsible accordion section using `rounded-lg` cards at `--sp-elevated` surface
- Section headers use the structural label treatment: uppercase, `--sp-text-tertiary`, `letter-spacing: 0.08em`
- Collapsed state shows a summary line of current config values so users can see their setup at a glance without expanding

---

### PerformanceSummaryVisual.tsx (525 lines — CSS charts, sidebar width constraints)

**Role:** Survival curve charts and cumulative uplift visualization using CSS (no chart library).

**Critical constraint:** Uses CSS `height` percentages and `position: absolute` for chart rendering. Must work at SP sidebar widths:
- Sidebar collapsed: 64px (content area is viewport width minus 64px)
- Sidebar expanded: varies (design doc specifies ~240px expanded width, so content area is viewport width minus 240px)

**Changes needed:**

1. **Audit all fixed-width assumptions.** Any element with a hardcoded `width` in px that assumes a full-viewport layout must be converted to percentage or `calc()` values.

2. **Chart container:** Wrap the visual in a container that responds to sidebar state. Use a CSS custom property on the layout root:
   ```css
   .sp-backtester-layout {
     --sidebar-width: 64px; /* updated via JS when sidebar expands */
   }
   ```
   Charts reference `var(--sidebar-width)` in `calc()` expressions rather than using fixed widths.

3. **Minimum viable width:** Define a minimum content area width of 600px for the visual. If the viewport is narrower (e.g., small laptop with expanded sidebar), the chart area gets a horizontal scrollbar rather than breaking its proportions. This is a graceful degradation, not a mobile solution.

4. **Test matrix:**
   - 1440px viewport, sidebar collapsed ✓
   - 1440px viewport, sidebar expanded ✓
   - 1024px viewport, sidebar collapsed ✓
   - 1024px viewport, sidebar expanded (minimum viable width check) ✓
   - 768px viewport (tablet, deferred to post-Sprint-B) ⚠

---

### TutorialOverlay.tsx (564 lines — 17-step DOM-positioned tutorial)

**Role:** Tutorial overlay using `getBoundingClientRect()` to position callouts over real component IDs.

**Critical constraint:** All ported component `id` attributes must be **preserved exactly** from the standalone prototype. If any `id` changes during porting, tutorial positioning breaks silently.

**Strategy:**

1. **Audit all `id` dependencies in `TutorialOverlay.tsx` before porting begins.** Extract a complete list of DOM IDs the tutorial references. This is a Felix pre-flight check but Deb must validate the list against final component renders.

2. **ID preservation contract:** No component in the Back Tester port may rename an `id` attribute without updating `TutorialOverlay.tsx` simultaneously. Document this in a `BACKTESTER_ID_CONTRACT.md` file in the component directory.

3. **Positioning adjustment for sidebar layout:** The standalone prototype had no sidebar. `getBoundingClientRect()` values will shift left by `--sidebar-width` pixels in the SP layout. The overlay positioning logic must account for this offset. Before Sprint B build begins, Felix should audit whether the tutorial uses viewport-relative or element-relative coordinates. If viewport-relative, all `left` values need `+ sidebarWidth` correction.

4. **Tutorial trigger:** In the standalone app, the tutorial launched automatically (access gate flow). In SP, trigger it via an explicit "Start Tutorial" button in the Back Tester header area. First-time subscribers get a dismissible banner: "New to Back Tester? [Take the tour →]". The tutorial is never forced.

---

### ScenarioControls.tsx (450 lines — mode toggles + 14 strategy templates)

**Role:** Manual vs. optimize mode switcher, strategy template selector.

**Changes needed:** Minimal. The component logic is self-contained.

**Design notes:**
- The toggle switch (manual vs. optimize) uses `--sp-brand-accent` (#7170ff) for the active state, consistent with all other SP toggle controls
- Strategy template chips: `rounded-full`, `--sp-surface-secondary` (#28282c) background, `--sp-brand-accent` border on selected state
- No structural changes required

---

### AccessGate Replacement

The standalone `AccessGate` component (email capture form) is **fully deprecated** in the SP integration.

Replacement mapping:

| Standalone behavior | SP behavior |
|---|---|
| Unauthenticated user → email capture form | User cannot reach `/tools/backtester` (redirect to `/login`) |
| Email submitted → full Back Tester access | N/A — access is subscriber-only |
| Subscriber → skip gate | Subscriber → full access, no gate rendered |
| Non-subscriber but authenticated → N/A | Non-subscriber → paywall render (see Section 2) |

The `AccessGate` component should not be ported. It can be deleted from the Back Tester component tree after port verification.

---

## 4. Design Tokens & Style Consistency

### Applicable Tokens (all from `deb-design-tokens.md`)

**Surfaces:**
- Page canvas: `--sp-canvas` (#08090a) — Back Tester page background
- Config panel: `--sp-panel` (#0f1011) — left config panel sidebar if used
- Cards / containers: `--sp-elevated` (#191a1b) — config sections, results panels
- Hover fill: `--sp-surface-hover` (rgba(255,255,255,0.04))
- Selected fill: `--sp-surface-active` (rgba(255,255,255,0.05))

**Typography:**
- All UI labels: Inter Variable, weight 510 (`font-ui`)
- Section headers: uppercase, weight 590, `letter-spacing: 0.08em` (structural label treatment)
- Numeric data in results: JetBrains Mono, `font-feature-settings: "tnum"` for tabular alignment
- Max weight: 590 — no 700+ anywhere

**Borders:**
- Card edges: `--sp-border-subtle` (rgba(255,255,255,0.05))
- Inputs, standard containers: `--sp-border-standard` (rgba(255,255,255,0.08))

**Interactive:**
- Primary CTA (Run simulation, Optimize): `--sp-brand-primary` (#5e6ad2)
- Active states, links: `--sp-brand-accent` (#7170ff)
- Focus ring: `shadow-sp-focus`

### Survival Curve Color Mapping

The Back Tester's survival curves visualize multiple strategies simultaneously. Color assignment must:
1. Be distinguishable on `--sp-canvas` background
2. Use DESIGN.md palette only — no one-off colors
3. Reserve IBM Carbon status colors for actual status (eliminated, safe, at-risk) — not for decorative series differentiation

**Recommended survival curve palette:**

| Series | Color | Token | Notes |
|---|---|---|---|
| Strategy 1 (primary) | `#7170ff` | `--sp-brand-accent` | Brightest — user's selected strategy |
| Strategy 2 | `#78a9ff` | `--sp-info-text` | Info blue — secondary comparison |
| Strategy 3 | `#6fdc8c` | `--sp-success-text` | Success green — positive contrast |
| Strategy 4 | `#f1c21b` | `--sp-warning-text` | Warning yellow — caution read |
| Strategy 5 | `#ff8389` | `--sp-danger-text` | Danger red — worst performer visual |
| Strategy 6+ | `--sp-text-tertiary` dashed | `#8a8f98` | Additional strategies muted |
| Baseline/Random | `--sp-text-quaternary` dashed | `#62666d` | Reference line, not a strategy |

**Rule:** Survival curves never use solid IBM Carbon status colors for background fills. Curves are stroke-only or stroke + very subtle area fill at 8% opacity. Full status color fills are reserved for eliminated/alive status badges in the results panel.

**Cumulative uplift chart:** Positive uplift uses `--sp-success-text` (#6fdc8c), negative uses `--sp-danger-text` (#ff8389). The zero baseline is `--sp-border-emphasis` (#23252a).

### New Tokens Needed

No new tokens are required. The existing token set from `deb-design-tokens.md` covers all Back Tester surfaces. If the survival curve palette above is formalized as utility classes, add to `@layer components`:

```css
.bt-curve-1 { stroke: #7170ff; }
.bt-curve-2 { stroke: #78a9ff; }
.bt-curve-3 { stroke: #6fdc8c; }
.bt-curve-4 { stroke: #f1c21b; }
.bt-curve-5 { stroke: #ff8389; }
.bt-curve-muted { stroke: #8a8f98; stroke-dasharray: 4 4; }
.bt-curve-baseline { stroke: #62666d; stroke-dasharray: 6 3; }
```

---

## 5. Responsive & Mobile Considerations

### Back Tester Mobile Strategy: Desktop-First, Graceful Degradation for Sprint B

The Back Tester is a data-dense analytical tool. A full mobile implementation (touch-friendly controls, reflow of the config panel, mobile-optimized charts) is a post-Sprint-B effort. For Sprint B, the target is:

**Support:** Desktop (1024px+) with sidebar collapsed or expanded.

**Graceful degradation (768px–1023px, tablet):**
- Config panel collapses to a drawer (bottom sheet or left slide-in)
- Charts reflow to minimum viable width (600px) with horizontal scroll if needed
- Tutorial overlay is disabled on touch/small viewports (banner only: "For full tutorial, use desktop")
- Core functionality (run simulation, view results) must work — it should not be broken, just cramped

**Not supported (Sprint B):** Mobile phone viewports (<768px). If a user lands on mobile, show a polite "Back Tester is optimized for desktop. For the best experience, use a larger screen." banner above the tool. Do not hide the tool — let them try.

### Critical Breakpoints to Test

| Breakpoint | Priority | Expectation |
|---|---|---|
| 1440px, sidebar collapsed | P0 | Full feature, pixel-perfect |
| 1440px, sidebar expanded | P0 | Full feature, verify chart reflow |
| 1280px, sidebar collapsed | P0 | Full feature |
| 1280px, sidebar expanded | P0 | Full feature, chart minimum width check |
| 1024px, sidebar collapsed | P1 | Functional — may be tighter but usable |
| 1024px, sidebar expanded | P1 | May trigger minimum width scroll |
| 768px, tablet | P2 | Graceful degradation acceptable |
| 375px, mobile | P3 | "Desktop recommended" banner, tool accessible but not optimized |

---

## 6. Sprint B Design Tasks (Backlog Items)

```
[Nav] (3.2a): Add "Back Tester" to sidebar TOOLS section with subscriber gate state — S — locked icon + dimmed style for non-subscribers, normal for subscribers

[Nav] (3.2b): Implement NEW badge on Back Tester nav item (30-day post-launch window, first-visit dismissal) — S — use info blue badge token

[Paywall] (3.3a): Design and implement paywall state for /tools/backtester — non-subscriber conditional render — M — blurred preview + upgrade CTA, no email capture

[Paywall] (3.3b): Subscriber paywall bypass — direct render of SeasonReplayView with zero friction — S — route-level subscriber check

[Component] (3.2c): Remove AccessGate wrapper from SeasonReplayView; integrate SP subscriber auth check at route level — S — delete AccessGate from port

[Component] (3.2d): Audit and document all TutorialOverlay DOM ID dependencies; create BACKTESTER_ID_CONTRACT.md — S — must happen before any component porting

[Component] (3.2e): Port SeasonReplayView into SP nav shell — remove standalone chrome, ensure sidebar-aware layout — M

[Component] (3.2f): Refactor PoolConfigPanel into 5 sub-form components (PoolBasicsForm, StrategyTypeSelector, WeightingPanel, SeasonSelector, PoolParamLoader) — L — PoolParamLoader is subscriber-only conditional

[Component] (3.2g): Port PerformanceSummaryVisual with sidebar-width-aware chart layout; test at all 8 breakpoints — M — sidebar CSS var approach, minimum 600px chart width

[Component] (3.2h): Adjust TutorialOverlay positioning for sidebar layout offset; add sidebarWidth correction to viewport-relative coordinates — M — verify before vs after with sidebar at 64px and expanded

[Component] (3.2i): Port ScenarioControls; apply SP brand token to toggle and template chip active states — S

[Component] (3.2j): Port remaining medium-complexity components (PortfolioSlate, AvailableTeamsTable, EntryCard, CorrelationRiskPanel, CoordinatedVsUncoordinatedContrast, WeeklyDrillDownModal, SideBySideComparison, WeekRow, WeekSelector, SeasonSummaryBar, OptimizationResults) — L — batch port, SP token audit each

[Subscriber] (3.4a): Implement pool parameter loading via PoolParamLoader — pre-populate PoolConfigPanel from subscriber's pool data — M — API call + info banner

[Subscriber] (3.4b): Pool switcher in PoolParamLoader — switching pools re-populates config without page reload — S

[Tutorial] (3.2k): Replace automatic tutorial launch with opt-in "Start Tutorial" button + first-visit banner — S — never force tutorial

[Design] (3.2l): Define and implement survival curve color classes (.bt-curve-1 through .bt-curve-muted, .bt-curve-baseline) as CSS utility layer — S

[QA] (3.2m): Cross-breakpoint visual QA pass — all 8 breakpoints from Section 5 test matrix — M — produce QA report with screenshots
```

---

## 7. Design Deliverables (Handoff to Felix for Phase D)

Felix starts Phase D (display components) after Deb delivers:

### Required Before Felix Starts

1. **PoolConfigPanel sub-form spec** (3.2f)
   Deliverable: Component breakdown document listing each sub-form, its fields, collapsed-state summary format, and accordion interaction spec. Does not need to be a Figma file — a detailed markdown spec is sufficient given the existing DESIGN.md token system.

2. **Paywall state spec** (3.3a)
   Deliverable: Written spec covering: layout structure, blur treatment implementation approach, card content copy, CTA button copy, link destinations. Include the exact CSS for the blur effect. Felix should not have to make design decisions here.

3. **Tutorial trigger redesign** (3.2k)
   Deliverable: Written spec for the "Start Tutorial" button placement (where in the Back Tester header), the first-visit banner copy, and the dismiss behavior. One paragraph, no wireframe needed.

4. **Survival curve color spec** (3.2l)
   Deliverable: The CSS utility class block from Section 4 of this document. Ready to paste into `@layer components`.

5. **Breakpoint test matrix sign-off** (Section 5)
   Deliverable: Confirmation that Felix should treat the 8 breakpoints in Section 5 as the test requirement, with P0 being fully pixel-perfect and P3 being the "desktop recommended" banner.

### Handoff Format

All deliverables are markdown documents in `docs/`. No Figma required — the design system is fully specified in token form and the existing Back Tester prototype is the visual reference. Felix's job is to port and adapt; Deb's spec provides the constraints and delta from the standalone version.

Deb reviews Felix's implementation at each component milestone against:
- Token usage (no hardcoded colors or one-offs)
- ID preservation contract (tutorial overlay safety)
- Sidebar-width chart behavior at all P0 breakpoints
- Subscriber gate logic (paywall vs. direct access)

---

*Produced by Deb the Designer — Sprint B: Back Tester Integration UX Direction*
*Token reference: `docs/deb-design-tokens.md` | IA reference: `docs/deb-ia-design-plan.md` | Backlog: `docs/ann-backlog-tasks.md`*
