# SurvivorPulse — DESIGN.md Shortlist

**Prepared by:** Deb the Designer  
**Date:** 2026-04-09  
**Source collection:** VoltAgent/awesome-design-md (58 systems reviewed, 10 evaluated in depth)

---

## Evaluation Summary

SurvivorPulse needs a design system that carries the weight of a financial terminal, not a sports pick 'em app. The brief is clear: Bloomberg terminal meets sports analytics. That means dark mode by default, information-dense layouts, typography that holds up at 12px in a table cell, and a tone of institutional precision rather than consumer delight.

I reviewed 10 design systems in depth — pulling the full DESIGN.md for each via `npx getdesign@latest`. Below are the top 5, followed by what I looked at and why it didn't make the cut.

---

## Top 5 Shortlist

---

### 1. Linear

**One-liner:** Ultra-minimal dark-mode-native engineering tool; information hierarchy through luminance, not color.

**Why it fits SurvivorPulse:**  
Linear is designed for power users who live in the product all day managing complex systems — the same mindset as a serious multi-entry survivor player tracking correlation across 10 entries. The near-black canvas (`#08090a`) and luminance stacking model (surfaces lighten as elevation increases) create a natural hierarchy for multi-panel dashboards without visual noise. The indigo-violet accent is the only chromatic color in the system, which means status colors for risk (danger, success, warning) have full semantic real estate to work with and won't clash with the brand accent.

**Strengths:**
- True dark-mode-first — not a "dark theme option," darkness is the native medium
- Inter Variable with OpenType features `"cv01", "ss03"` — engineered specifically for geometric legibility; excellent at 12–13px in dense tables
- Semi-transparent white borders (`rgba(255,255,255,0.05–0.08)`) create structure without visual noise — perfect for the dense pick grids and correlation matrices SurvivorPulse needs
- Luminance elevation model: `rgba(255,255,255, 0.02 → 0.04 → 0.05)` for surfaces — allows seamless panel-in-panel dashboard nesting
- Radix UI primitives confirmed in the design system (same layer as shadcn) — the component vocabulary maps directly to SurvivorPulse's Tailwind + shadcn stack
- Berkeley Mono for code/data labels; tightly paired with Inter for numeric displays
- Weight 510 (between Regular and Medium) is Linear's signature — creates confident UI labels without yelling
- Toolbar button patterns, command palette, badge/pill system all translate directly to: week selectors, team quick-pick, entry status tags
- Brand accent (`#5e6ad2` / `#7170ff`) sits naturally in the blue-violet range — analytical, trust-coded, not aggressive

**Weaknesses/gaps:**
- No explicit data table or chart component defined in DESIGN.md — you'll need to build those components from the card/border primitives
- The 510 font weight is an Inter Variable feature — verify your version of Inter Variable supports fractional weights; fall back to 500 otherwise
- Berkeley Mono is a paid font; substitute `ui-monospace` or `JetBrains Mono` for numeric data cells
- Linear's minimal interaction states (ghost buttons at near-zero opacity) may need amplification for high-stakes user actions (submitting picks, confirming entry selections)

**Elements that translate directly:**
- The toolbar button (`rgba(255,255,255,0.05)` bg, 2px radius, 12px Inter 510) → week/pool filter controls
- Badge/pill system (transparent bg, `1px solid #23252a`, 9999px radius) → entry status tags ("Live", "Eliminated", "Safe")
- Card surface model (`rgba(255,255,255,0.02)` + `1px solid rgba(255,255,255,0.08)`) → pick distribution panel, risk exposure card
- Quaternary text (`#62666d`) → de-emphasized historical data, footnotes, data source timestamps
- Command palette design (12px radius, multi-layer shadow, 16px Inter search input) → quick-entry search or team lookup

**Install:** `npx getdesign@latest add linear.app`

---

### 2. IBM (Carbon Design System)

**One-liner:** Enterprise analytics gold standard; the most rigorously documented system in the dataset for data-dense, dual-theme UI.

**Why it fits SurvivorPulse:**  
IBM's Carbon Design System is purpose-built for complex data products — dashboards, analytics suites, monitoring tools. It has the most complete documented token architecture of any system reviewed, with explicit dark theme tokens (`--cds-layer-01`, `--cds-text-primary`, etc.). IBM Plex Sans was specifically designed to be readable at small sizes in technical/data contexts — it's the same font used in IBM's own data visualization platform. The 8px grid with micro-tracking at small sizes (0.16px at 14px, 0.32px at 12px) solves the dense table legibility problem by default.

**Why it fits SurvivorPulse:**  
This is the design system that would give SurvivorPulse instant credibility as a serious analytical tool, not a consumer picks app. The rectangular buttons with 0px radius, the bottom-border input pattern, the systematic gray scale — these are signals that serious professionals recognize from Bloomberg, financial terminals, and enterprise dashboards. "Governance-grade, reproducible, deterministic" is exactly what Carbon communicates.

**Strengths:**
- Fully documented dual-mode theme system (Gray 10 light / Gray 100 dark) with semantic CSS tokens — switch modes without rewriting any component logic
- IBM Plex Sans Light (300) at display sizes creates genuine typographic authority; Plex Mono handles data cells natively
- Micro-tracking at small sizes (0.16px at 14px Body Short) is a deliberate readability enhancement for dense, information-heavy layouts
- 0px radius buttons communicate financial/analytical precision — exactly the right signal for a risk management product
- Bottom-border input pattern (not boxed) is the standard financial-UI form pattern, familiar to the target ICP
- Rigorous 8px grid = every spacing decision is principled; dashboards composed from these tokens look intentional
- Complete status/semantic color vocabulary: Red 60 for danger, Green 50 for success, Yellow 30 for warning, Blue 60 for info — maps perfectly to risk states in survivor entries
- Gray 100 dark theme: `#161616` bg → `#262626` cards → `#393939` elevated surfaces — three clean levels of panel hierarchy

**Weaknesses/gaps:**
- IBM Plex Sans is a Google Fonts / open source font but requires explicit loading setup; fallback is Helvetica Neue which reads differently at scale
- 0px button radius may feel too clinical for a sports-adjacent product; you'll want to allow yourself a 4–6px radius in the custom overrides
- Carbon's actual component library (React Carbon Components) uses a separate installation path from shadcn/Tailwind — you'll use Carbon as design inspiration and implement components in your own Tailwind/shadcn stack, not adopt the Carbon component library directly
- The design system skews heavily toward light mode in the marketing page; dark theme tokens exist but you need to consult the Carbon Design System docs (not just this DESIGN.md) for the complete dark palette

**Elements that translate directly:**
- Gray 10 / Gray 100 layered surfaces → pick distribution table rows (alternating Gray 10 / white in light; Gray 80/90 in dark)
- IBM Plex Mono at 14px 0.16px tracking → numeric data cells (pick counts, survival rates, implied probabilities)
- Body Short 01 (14px, 400, line-height 1.29) → the most data-dense text style in the system; use for table cell content
- Support colors (Red 60 `#da1e28`, Green 50 `#24a148`, Yellow 30 `#f1c21b`) → entry health indicators
- Caption 01 (12px, 400, 0.32px tracking) → data footnotes, pool metadata, timestamp labels

**Install:** `npx getdesign@latest add ibm`

---

### 3. Sentry

**One-liner:** Dark IDE aesthetic with data-dense dashboard DNA; the most directly analogous product context in the dataset.

**Why it fits SurvivorPulse:**  
Sentry is literally an error monitoring dashboard — complex multi-entry views, time-series data, status states, dense tables, and a user base of technical professionals who need information fast. That's almost exactly the SurvivorPulse use case. The deep purple-black palette (`#1f1633`) creates a sense of focused immersion rather than generic darkness. The four-tier uppercase label system (buttons, captions, labels, micro-text all using `text-transform: uppercase` with 0.2px letter-spacing) is perfect for the structured data hierarchy in a survivor tool: WEEK 14 | TEAM | STATUS | REMAINING.

**Strengths:**
- Deep purple-black backgrounds (`#1f1633`, `#150f23`) — warm-tinted darkness that reads as premium rather than cold
- Uppercase label system with 0.2px tracking throughout — creates strong structural scannability in dense views; ideal for week headers, pool labels, pool count
- Lime-green accent (`#c2ef4e`) for maximum-visibility signals (use sparingly for "you must act now" CTAs like submit picks deadline)
- Inset shadow on buttons creates tactile pressed-state feedback — important for high-stakes actions (confirming picks)
- Frosted glass effect (`blur(18px) saturate(180%)`) → overlay panels, pick confirmation modals
- Rubik UI font handles small sizes well across a wide weight range; clear distinction between body (400), navigation (500), titles (600), CTAs (700)
- Monaco monospace → data values, correlation coefficients, probability percentages in data cells
- The "dark IDE aesthetic without feeling cold" brief is the exact balance SurvivorPulse needs — analytical but not sterile

**Weaknesses/gaps:**
- "Dammit Sans" is a proprietary display font and should be entirely replaced — substitute Inter Variable or IBM Plex Sans for SurvivorPulse's display headings; it's hero-only anyway
- The lime-green accent (`#c2ef4e`) is very distinctive/branded to Sentry — use it at maximum as a single "action required" signal, not as a general brand color
- Coral/pink accents (`#ffb287`, `#fa7faa`) have no analog in SurvivorPulse's language; either re-purpose as semantic states or drop entirely
- The "irreverent brand voice" embedded in the design (big expressive display font, vibrant accents) needs to be toned to analytical; the structure is right, the personality needs overriding

**Elements that translate directly:**
- Deep purple-black surfaces for the main dashboard shell — immediately reads "serious analytics platform"
- Uppercase label pattern (Rubik 14px weight 700, uppercase, 0.2px spacing) → column headers in pick distribution tables, pool metadata tags
- Status badge system → entry health (safe, at risk, eliminated)
- Frosted glass cards → modal overlays for confirming picks, viewing matchup details
- Inset-shadow primary buttons → the submit-picks action button

**Install:** `npx getdesign@latest add sentry`

---

### 4. Vercel

**One-liner:** Precision engineering aesthetic; Geist font system with tabular number support and shadow-as-border depth model.

**Why it fits SurvivorPulse:**  
Vercel's design system is built on a single principle: remove everything until only structure remains. This is exactly right for a data-dense dashboard where the user needs to process large amounts of information quickly. The shadow-as-border technique (`box-shadow: 0px 0px 0px 1px rgba(0,0,0,0.08)`) creates elegant panel separation without heavy visual lines. Most importantly, Vercel explicitly calls out tabular numbers (`tnum` OpenType feature) for captions — critical for numeric alignment in data columns like pick counts, survival rates, and implied probabilities.

**Why it fits SurvivorPulse:**  
The "Build → Preview → Ship" workflow accent colors (blue, pink, red) map cleanly to a survivor entry lifecycle: **Active → At Risk → Eliminated**. The design intention is the same — a user moving through distinct, high-stakes states with clear visual feedback at each step.

**Strengths:**
- Geist font (open source, free) with `tnum` tabular number support — numerals align in columns without width inconsistency; essential for data tables
- Shadow-as-border technique creates clean panel borders without visual weight — data comes first, structure is ambient
- Multi-layer shadow stacks for nuanced elevation hierarchy — ideal for nested dashboard panels
- Precision achromatic palette with three workflow accent colors (Blue `#0a72ef`, Pink `#de1d8d`, Red `#ff5b4f`) → maps to entry lifecycle states
- Aggressive negative letter-spacing at display sizes creates authoritative, compressed headlines
- Custom `--geist-*` token system (CSS custom properties) maps cleanly to Tailwind's arbitrary value system
- Light/dark mode by design (white canvas + near-black text with dark variants defined)

**Weaknesses/gaps:**
- Primarily designed as a light-mode system (white canvas) — dark adaptation is possible but needs explicit work; Vercel's own product dashboard is dark but the DESIGN.md skews marketing/light
- Geist is open source but still a custom font — adds a font loading step; ensure fallback (`Arial`) doesn't shift layouts
- Workflow accents (Ship Red, Preview Pink, Develop Blue) are metaphorically apt but named for Vercel's specific concepts — rename these tokens explicitly for SurvivorPulse's domain (Eliminated Red, At Risk Amber, Active Blue)
- The design system is minimalist-sparse rather than information-dense; you'll need to develop a higher-density variant of the spacing and typography scale for actual dashboard views vs. marketing pages

**Elements that translate directly:**
- Pill badges with `tnum` and tinted backgrounds → entry status tags with numeric data (e.g., "Entry 3 — Week 8")
- Shadow-as-border card containers → every panel in the main dashboard
- Workflow accent semantic colors → SurvivorPulse entry lifecycle: Active (Blue), At Risk (Pink/Amber), Eliminated (Red)
- Gray scale (Gray 100 `#171717` → Gray 50 `#fafafa`) → text hierarchy in data tables
- Multi-layer card shadow → elevated panels like "My Entries" overview widget

**Install:** `npx getdesign@latest add vercel`

---

### 5. PostHog

**One-liner:** Exact same Tailwind + shadcn/ui tech stack; IBM Plex Sans Variable; most directly portable component architecture.

**Why it fits SurvivorPulse:**  
PostHog is the only system in the dataset confirmed to run Tailwind CSS + Radix UI + shadcn/ui — the same exact frontend stack as SurvivorPulse. That means every component pattern in this DESIGN.md can be implemented in SurvivorPulse's codebase with near-zero adaptation overhead. IBM Plex Sans Variable (also used in IBM's Carbon system) is purpose-built for technical, data-heavy interfaces. The component architecture is dense and editorial — built for a product that users live in all day, reading long streams of analytical content.

**The major caveat:** PostHog's warm sage/olive aesthetic (parchment background `#fdfdf8`, olive text `#4d4f46`) is entirely wrong for SurvivorPulse's tone. This is a design system you'd adopt for its bones and completely re-skin. The palette swap from warm-sage to analytical-dark is non-trivial but the component structure underneath is exactly right.

**Strengths:**
- Confirmed Tailwind CSS + Radix UI + shadcn/ui stack — zero component architecture translation needed
- IBM Plex Sans Variable with weight range 400–800 — same font as IBM Carbon, excellent data legibility
- Content-heavy editorial layout patterns designed for users spending extended sessions in the product
- Button interaction system uses opacity reduction + color accent shift — clean, professional hover states
- Dark near-black CTA (`#1e1f23`) is SurvivorPulse-appropriate; keep this, change everything else
- Badge/tag system at 13px weight 500–700 → entry labels, pool type tags
- Input styling maps directly to Tailwind's form plugin patterns

**Weaknesses/gaps:**
- Complete palette replacement required: warm sage → analytical dark (near-black surfaces, cool gray borders, blue-violet accent)
- Playful brand elements (hedgehog illustrations, quirky irreverence) must be ignored entirely — this is structure-borrowing only
- Orange hover accent (`#F54E00`) needs replacement with a cooler, more analytical accent color
- PostHog's design is primarily warm light-mode; full dark mode requires building from scratch using the component patterns, not the color tokens

**Elements that translate directly:**
- IBM Plex Sans Variable weight/size hierarchy → data table typography (keep identical, change colors)
- Dark primary button (`#1e1f23`, 6px radius) → SurvivorPulse's primary action buttons (submit picks, confirm entry)
- Category label system (uppercase 18px IBM Plex Sans 700) → section headers: "MY ENTRIES", "THIS WEEK", "PICK DISTRIBUTION"
- shadcn/ui component patterns already implemented → immediate access to full shadcn component set without integration work

**Install:** `npx getdesign@latest add posthog`

---

## Candidates Reviewed and Rejected

**Kraken** — The description "purple-accented dark UI, data-dense dashboards" is misleading. The actual DESIGN.md reveals a white/light background system (`#ffffff` primary surface) with Kraken Purple (`#7132f5`) as the accent. It's a trust-focused institutional design but light-mode-first and better suited for a consumer crypto trading landing page than a dense analytics dashboard.

**Revolut** — Strong fintech semantic token system (`--rui-*`) and a comprehensive status color vocabulary (danger, warning, teal, blue, deep-pink). But it's primary light mode, the hero font (Aeonik Pro) is proprietary and unavailable for external projects, and the universal pill-button system (9999px radius on everything) codes as consumer fintech rather than analytical tool.

**ClickHouse** — Genuinely analytics DNA and pure black dark mode. The neon yellow-green (`#faff69`) on black is striking but reads as "gaming/esports" rather than "financial analytics." Weight 900 Inter headlines are too aggressive for a dashboard product. Would send the wrong signal about the product's credibility to a serious multi-entry player managing real money.

**Cohere** — Enterprise AI platform with real analytical credibility. But it's a light-mode-first design (white canvas), uses proprietary custom fonts (CohereText, Unica77), and the signature 22px border radius creates a soft/approachable personality that works against SurvivorPulse's precision-tool identity. The purple hero sections are great, but they're full-width bands, not a dashboard component system.

**Revolut** — (see above)

---

## Deb's Recommendation: Linear

If it were my call, I'd start with **Linear**.

Here's why: Linear is the only system in this dataset that was designed from day one for expert users who live in the product managing complex, multi-dimensional information. That's the SurvivorPulse user. A serious 10-entry player isn't checking picks casually — they're analyzing correlation matrices, tracking pick distribution across pools, and making calculated decisions under time pressure. The interface should feel like it was built for them, not adapted from a consumer product.

The technical fit is also the strongest. Inter Variable is open source, widely available, and renders beautifully on every platform. The Tailwind + Radix UI alignment means shadcn components need no translation. The luminance stacking model for dark surfaces (subtle opacity steps rather than heavy color contrast) is exactly how you build a multi-panel dashboard without visual overwhelm.

The one thing I'd change immediately: swap Berkeley Mono for JetBrains Mono (free, excellent at small sizes) for numeric data cells, and explicitly define the status color vocabulary (entry health, risk indicators) using Linear's existing green and indigo as the foundation — adding semantic red/amber from a system-compatible cool palette.

**Recommendation:** Start with Linear's DESIGN.md as the base. Use IBM Carbon's dark theme token naming conventions to document the status/semantic colors. Borrow Sentry's uppercase label pattern for structural column headers. That combination would produce something genuinely distinctive.

---

*Design systems assessed: Linear, IBM Carbon, Sentry, Vercel, PostHog, Kraken, Revolut, Cohere, ClickHouse, Together AI (fetched but not included — similar analytical blueprint aesthetic to IBM but less component coverage)*
