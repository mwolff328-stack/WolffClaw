#!/usr/bin/env python3
"""Enrich all SurvivorPulse Notion backlog tasks with descriptions, ACs, and test cases."""

import json
import time
import urllib.request
import urllib.error

import os
from pathlib import Path

def _load_notion_key() -> str:
    # 1. environment variable
    if val := os.environ.get("NOTION_API_KEY"):
        return val
    # 2. shared config file
    cfg = Path("~/.config/notion/api_key").expanduser()
    if cfg.exists():
        return cfg.read_text().strip()
    raise RuntimeError("Notion API key not found. Set NOTION_API_KEY or create ~/.config/notion/api_key")

API_KEY = _load_notion_key()
NOTION_VERSION = "2025-09-03"

def patch_page(page_id, properties):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    data = json.dumps({"properties": properties}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PATCH")
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Notion-Version", NOTION_VERSION)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, "OK"
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return e.code, body

def make_title(name):
    return {"title": [{"text": {"content": name}}]}

def make_rich_text(content):
    chunks = []
    while content:
        chunks.append({"text": {"content": content[:2000]}})
        content = content[2000:]
    return {"rich_text": chunks}

TASKS = [
    # ─── BATCH 1 ───────────────────────────────────────────────────────────────
    {
        "id": "35229ce5-833d-8119-9694-dacda656a8be",
        "name": "Portfolio Presets (14.2): Integrate presets with recommendation engine",
        "description": "Connects the portfolio preset configurations defined in task 14.1 to the CMEA recommendation engine so that selecting a preset actively influences which teams are recommended each week. When a user picks a preset (e.g., Conservative, Aggressive, Balanced), the engine applies that preset's risk tolerances and allocation weights at recommendation time. This closes the loop between preset storage and actual decision-making output.",
        "ac": "- Selecting a preset updates the recommendation engine's active parameters before generating picks\n- Preset parameters (risk tolerance, future-value weight, field-concentration limits) are correctly applied\n- Recommendations visibly differ between presets given identical pool inputs\n- Switching presets triggers a fresh recommendation recalculation without a page reload\n- A user with no preset selected falls back to documented default engine behavior\n- Preset selection persists across sessions and is restored on next login\n- API endpoint accepts preset_id as an optional recommendation parameter",
        "tests": "1. Select 'Conservative' preset -> verify recommendations favor higher-probability teams vs default\n2. Select 'Aggressive' preset -> verify recommendations weight future-value preservation differently\n3. Switch preset mid-session -> verify picks update immediately without full page reload\n4. Request recommendations with no preset set -> verify default behavior is unchanged\n5. Log out and log back in -> verify selected preset is restored\n6. Pass invalid preset_id to API -> verify 400 error with descriptive message"
    },
    {
        "id": "35229ce5-833d-8120-8b89-dc636f738255",
        "name": "Buyback Strategy (13.2): Implement buyback-aware strategy switching",
        "description": "Extends the recommendation engine to adjust strategy parameters based on whether an entry has used its buyback. An entry still on its first life should be recommended differently than one already bought back, since a bought-back entry has no safety net remaining. This task implements the conditional logic that detects buyback status and routes to the appropriate strategy profile.",
        "ac": "- System correctly detects buyback status for each entry from the pool model (added in 13.1)\n- Entries that have used their buyback receive a more conservative strategy profile automatically\n- Entries that have not used their buyback receive the standard strategy profile\n- Strategy switching is transparent to the user via a visible indicator or tooltip\n- Pools with no buyback rules are unaffected by this logic\n- Multiple entries in the same pool with different buyback states receive different recommendations\n- Behavior is unit-tested for both bought-back and non-bought-back entry states",
        "tests": "1. Entry with buyback available -> verify standard strategy applies\n2. Entry after buyback used -> verify strategy profile shifts to conservative\n3. Pool with no buyback rule -> verify no strategy change occurs for any entry\n4. Two entries in same pool, one bought back and one not -> verify each gets correct profile\n5. Toggle buyback status in test data -> verify strategy updates dynamically"
    },
    {
        "id": "35229ce5-833d-81c5-82a1-eac5c58855a6",
        "name": "Notification System (12.1): Design notification event system",
        "description": "Defines the architecture and event taxonomy for the SurvivorPulse notification system before any implementation begins. This design task identifies which events trigger notifications (pick deadlines, weekly results, recommendation availability, auth events), the supported delivery channels (email via Postmark, in-app), and the data model for per-user notification preferences. The output is a design document and schema definition.",
        "ac": "- Event taxonomy covers at minimum: pick deadline reminder, weekly result posted, recommendation ready, account created, password reset\n- Notification preference schema supports opt-in/out at event-type granularity per user and per pool\n- Delivery channels (email via Postmark, in-app) are both supported in the schema\n- Data model for notification_preferences table is fully defined with column types and constraints\n- Design addresses deduplication to prevent double-sends\n- Design document is reviewed and stored in the repo before implementation tasks begin",
        "tests": "1. Review design doc -> verify all core event types are covered with trigger conditions\n2. Schema review -> verify opt-in/out supported at event-type level\n3. Schema review -> verify email and in-app channels can be toggled independently\n4. Schema review -> verify deduplication key is defined to prevent duplicate sends\n5. Schema review -> verify pool-level preference override of user-level default is supported"
    },
    {
        "id": "35229ce5-833d-81d3-a07c-f78860ee9935",
        "name": "Strategy-to-Context (10.1): Build context matching engine",
        "description": "Builds an engine that maps a user's current survivor pool context (week number, entries alive, pool size, elimination rate, buyback status) to an appropriate strategy profile. Rather than requiring users to manually select strategies, the engine infers the right approach from observable signals, improving decision quality particularly for less experienced players. The engine outputs a strategy recommendation with a rationale string.",
        "ac": "- Engine accepts context inputs: week number, entries_alive, pool_size, field_size, buyback_used\n- Engine outputs a strategy label (aggressive, balanced, conservative) and a rationale string\n- Mapping logic is configurable via a strategy matrix, not hardcoded magic numbers\n- Engine handles edge cases: week 1, final week, single entry remaining, empty pool\n- Output includes a confidence_score or weighted_signal breakdown\n- All input parameters are validated; invalid inputs return clear error messages\n- Unit tests cover at least 10 representative context scenarios",
        "tests": "1. Early season, many entries alive, large field -> verify 'aggressive' or 'balanced' returned\n2. Late season, single entry alive, small field -> verify 'conservative' returned\n3. Large field (500+) vs small field (20) with same week/entries -> verify different strategies\n4. Week 1 with no historical data -> verify graceful fallback to default\n5. buyback_used=true in late season -> verify strategy is more conservative than buyback_used=false\n6. Pass null/missing week number -> verify validation error returned\n7. Verify rationale string is human-readable and references the key inputs"
    },
    {
        "id": "35229ce5-833d-815d-b46b-ec325908599e",
        "name": "Pool Structure Analysis (8.2): Optimize backtester for parameter sweep",
        "description": "Implements performance optimizations for the backtester when running parameter sweeps across many pool configurations, as designed in task 8.1. Optimizations include parallelization of independent simulation runs, result caching for repeated configurations, and progressive result streaming so users see partial results before the full sweep completes. Correctness must be maintained throughout.",
        "ac": "- A parameter sweep of 100 configurations completes within 30 seconds on standard hardware\n- Results are streamed progressively; first results appear within 5 seconds of sweep start\n- Identical configurations are cached and not recomputed on subsequent runs in the same session\n- Optimization does not alter the correctness of any individual simulation result\n- Memory usage stays below 512MB during a 100-config sweep\n- Cache invalidation occurs correctly when underlying data (spreads, results) changes",
        "tests": "1. Run 100-config sweep -> verify it completes within 30 seconds\n2. Run same sweep twice -> verify second run is measurably faster due to caching\n3. Change one input parameter -> verify only the affected configs are recomputed\n4. Compare optimized vs non-optimized results for 10 configs -> verify identical outputs\n5. Monitor memory during 100-config sweep -> verify peak stays below 512MB\n6. Update spread data -> verify cache is invalidated and results refresh correctly"
    },

    # ─── BATCH 2 ───────────────────────────────────────────────────────────────
    {
        "id": "35229ce5-833d-816b-884c-e4c7b65ed56b",
        "name": "ROI Analysis (4.3): Implement preset pool profiles",
        "description": "Adds a set of preset pool profiles (e.g., Small Field, Large Field, High-Entry-Fee, Low-Entry-Fee) to the ROI analysis module, allowing users to quickly model expected returns without manually entering every pool parameter. Presets are pre-configured with common pool structures observed in the market. Users can select a preset as a starting point and then override individual parameters.",
        "ac": "- At least 4 preset pool profiles are defined and selectable in the ROI UI\n- Each preset pre-fills all required pool parameters (field_size, entry_fee, payout_structure)\n- Users can override any preset parameter after selection\n- Preset selection is reflected in the ROI calculation output immediately\n- Preset definitions are stored in a config file, not hardcoded in UI components\n- Custom parameter overrides are preserved if user switches between presets",
        "tests": "1. Select 'Large Field' preset -> verify field_size, fee, and payout fields are pre-filled\n2. Modify one parameter after preset selection -> verify ROI recalculates with override value\n3. Switch presets -> verify all parameters update to new preset values\n4. Add new preset to config -> verify it appears in UI without code changes\n5. Verify at least 4 presets cover meaningfully different pool structures"
    },
    {
        "id": "35229ce5-833d-81a7-9a2b-c301946a7a33",
        "name": "ROI Analysis (4.2): Build ROI calculator frontend",
        "description": "Builds the frontend interface for the ROI analysis module, connecting to the calculation engine built in task 4.1. The UI allows users to input pool parameters (field size, entry fee, number of entries, payout structure) and view expected ROI, variance, and break-even probability in a clear, actionable format. This is a core value-demonstration feature for the product.",
        "ac": "- User can input all required pool parameters via a form (field_size, entry_fee, entries, payout_structure)\n- ROI result displays expected value, variance, and break-even probability\n- Results update in real-time or on form submit without full page reload\n- Input validation prevents nonsensical values (negative fees, zero entries)\n- UI is responsive and functions correctly on mobile viewports\n- Results are visually distinct between positive-EV and negative-EV scenarios\n- Error states from the calculation engine are surfaced to the user with clear messages",
        "tests": "1. Fill all required fields -> verify ROI result renders correctly\n2. Enter negative entry fee -> verify validation error appears\n3. Resize to mobile viewport -> verify form and results remain usable\n4. Submit with all valid inputs -> verify result matches expected calculation from engine tests\n5. Enter edge case (1 entry, 1 person pool) -> verify graceful result\n6. Simulate API error -> verify user sees error message, not a blank screen"
    },
    {
        "id": "35229ce5-833d-814b-ad16-e73db26c3fb7",
        "name": "Anti-Dilution (16.1): Audit current personalization in recommendation engine",
        "description": "Audits the existing recommendation engine to identify where personalization logic exists, where it is absent, and where field-level correlation dilution risks occur when many users receive the same top picks. The goal is to understand the current state before designing anti-dilution mechanisms. Output is an audit report documenting findings and specific code locations.",
        "ac": "- Audit covers all code paths that generate pick recommendations\n- Report identifies which parameters are currently personalized per user vs shared across all users\n- Report identifies top-N team recommendations that could cause field concentration if widely adopted\n- Code locations for each finding are documented with file path and line number references\n- Report includes a severity ranking for each dilution risk found\n- Audit is documented and stored in the repo before any anti-dilution design begins",
        "tests": "1. Review audit report -> verify all recommendation code paths are covered\n2. Verify report identifies at least one field concentration risk scenario\n3. Verify each finding includes a specific file/line reference\n4. Verify severity rankings are defined and applied consistently\n5. Cross-check report findings against actual code -> verify no major paths were missed"
    },
    {
        "id": "35229ce5-833d-81d9-a72f-eae02e85a769",
        "name": "Correlation Risk Score (15.1): Build correlation score calculation",
        "description": "Builds the algorithm that calculates a correlation risk score across a user's portfolio of entries. The score reflects how exposed the overall portfolio is to a single game outcome -- if multiple entries pick the same team in the same week, a loss cascades across all of them. The calculation should produce a per-portfolio score and per-pick contribution scores to guide rebalancing decisions.",
        "ac": "- Algorithm calculates a portfolio-level correlation risk score (0-100 scale or equivalent)\n- Algorithm calculates per-pick contribution to overall correlation risk\n- Identical picks across multiple entries in the same week produce a high correlation score\n- Fully diversified picks across entries produce a low correlation score\n- Score updates when picks are added, changed, or removed\n- Algorithm is unit-tested with known inputs and expected outputs\n- Performance: score calculation completes in under 200ms for portfolios of up to 20 entries",
        "tests": "1. Portfolio with all entries picking same team in week 5 -> verify high correlation score\n2. Portfolio with fully diversified picks across all entries -> verify low correlation score\n3. Add a pick that duplicates an existing one -> verify score increases appropriately\n4. Remove a duplicated pick -> verify score decreases\n5. Run calculation on portfolio with 20 entries, 18 weeks -> verify completes in under 200ms\n6. Verify per-pick contribution scores sum to total portfolio score within rounding tolerance"
    },
    {
        "id": "35229ce5-833d-8144-ba9d-de40368470f7",
        "name": "Portfolio Presets (14.1): Define preset configurations in code",
        "description": "Defines the initial set of portfolio preset configurations as structured data in the codebase. Each preset encapsulates a named risk/strategy profile (e.g., Conservative, Balanced, Aggressive) with specific parameter values for the recommendation engine. This is the foundational task that enables task 14.2 (integration with the engine) and future preset management features.",
        "ac": "- At least 3 presets are defined: Conservative, Balanced, Aggressive\n- Each preset includes named parameters for risk_tolerance, future_value_weight, field_concentration_limit\n- Preset definitions are stored in a dedicated config file (not scattered in component code)\n- Presets are typed with a TypeScript interface\n- Default preset is clearly designated\n- Preset schema is documented in a comment block or README section",
        "tests": "1. Import preset config -> verify at least 3 presets load without errors\n2. Inspect Conservative preset -> verify it has more conservative values than Aggressive\n3. Check TypeScript compilation -> verify no type errors on preset definitions\n4. Modify a preset value in config -> verify change is reflected without touching engine code\n5. Verify default preset is defined and accessible programmatically"
    },

    # ─── BATCH 3 ───────────────────────────────────────────────────────────────
    {
        "id": "35229ce5-833d-814c-a045-e65c1d443e8e",
        "name": "Buyback Strategy (13.1): Add buyback parameters to pool model",
        "description": "Extends the pool data model to include buyback-related configuration fields, enabling the system to understand and store a pool's buyback rules. Fields include whether buybacks are allowed, the buyback cost, and the maximum number of buybacks permitted per entry. This is a prerequisite for task 13.2 (buyback-aware strategy switching).",
        "ac": "- Pool model includes fields: buyback_allowed (boolean), buyback_cost (number), max_buybacks_per_entry (integer)\n- Schema migration is created and runs cleanly on existing data without errors\n- API endpoints for pool creation and update accept and persist buyback parameters\n- API returns buyback fields in pool read responses\n- Existing pools without buyback rules default to buyback_allowed=false with no data loss\n- TypeScript pool interface is updated to reflect new fields",
        "tests": "1. Create pool with buyback_allowed=true, cost=50, max=1 -> verify all fields persisted\n2. Create pool without buyback fields -> verify defaults to buyback_allowed=false\n3. Update existing pool to add buyback -> verify fields update correctly\n4. Read pool via API -> verify buyback fields present in response\n5. Run migration on existing test DB -> verify no existing pool records are corrupted"
    },
    {
        "id": "35229ce5-833d-8136-8c10-cddbcb08d91f",
        "name": "Pool Structure Analysis (8.1): Design simulation parameter sweep",
        "description": "Designs the approach for running parameter sweeps across different pool configurations in the backtester. This is the design task for the pool structure analysis feature, defining which parameters to sweep (field size, entry count, payout structures, week ranges), the output format for sweep results, and the data structures that will power the optimization in task 8.2.",
        "ac": "- Design document specifies all sweepable parameters and their valid ranges\n- Output format for sweep results is defined (JSON schema or TypeScript interface)\n- Design identifies which parameters can be swept in parallel vs must be sequential\n- Data structures for storing and comparing sweep results are documented\n- Design is reviewed and stored in the repo before implementation begins in 8.2",
        "tests": "1. Review design doc -> verify at least 5 sweepable parameters are defined with ranges\n2. Review output schema -> verify it captures sweep config and result for each run\n3. Review parallelization plan -> verify independent parameters are correctly identified\n4. Review data structures -> verify results from multiple sweeps can be compared"
    },
    {
        "id": "35229ce5-833d-815c-80ee-cc9995552271",
        "name": "ROI Analysis (4.1): Build ROI calculation engine",
        "description": "Builds the backend engine that calculates expected ROI for survivor pool entries given pool parameters (field size, entry fee, number of entries, payout structure) and win probability assumptions. The engine should produce expected value, variance, and break-even probability as outputs. This is the calculation foundation for all ROI analysis features.",
        "ac": "- Engine accepts: field_size, entry_fee, entries_count, payout_structure, win_probability_per_week\n- Engine outputs: expected_value (currency), variance, break_even_probability (0-1)\n- Calculations are mathematically correct against known survivor pool EV formulas\n- Engine handles edge cases: single entry, 100% win probability, zero-payout pool\n- All inputs are validated with descriptive error messages for out-of-range values\n- Unit tests cover at least 5 distinct pool configurations with known expected outputs",
        "tests": "1. Standard large-field pool (500 entries, $100 fee, top-3 payout) -> verify EV is positive\n2. Single entry pool -> verify calculation handles trivially\n3. 0% win probability -> verify EV equals negative entry fee\n4. 100% win probability -> verify EV equals full payout\n5. Invalid input (negative field_size) -> verify descriptive validation error\n6. Compare output to manual calculation for a specific known scenario"
    },
    {
        "id": "35229ce5-833d-812a-8648-e5554277394d",
        "name": "Back Tester Integration (3.1): Analyze Back Tester codebase for portability",
        "description": "Analyzes the existing standalone Back Tester codebase to assess how its core simulation logic can be extracted and integrated into the SurvivorPulse backend. The goal is to understand what can be reused, what needs to be refactored, and what the integration path looks like. Output is an analysis document with a recommended integration approach and effort estimate.",
        "ac": "- Analysis covers all major modules in the Back Tester codebase\n- Document identifies which modules are directly portable vs require refactoring\n- Document identifies external dependencies that need to be resolved for integration\n- Integration approach is recommended with at least two options evaluated\n- Effort estimate is provided per option\n- Analysis is stored in the repo before any integration work begins",
        "tests": "1. Review analysis doc -> verify all major Back Tester modules are covered\n2. Verify at least 2 integration options are evaluated with pros/cons\n3. Verify effort estimates are included per option\n4. Verify external dependency list is complete\n5. Cross-check analysis against actual Back Tester codebase structure"
    },
    {
        "id": "35229ce5-833d-8138-8f72-c858c21cacae",
        "name": "IA Overhaul (1.10): Implement pool-level historical data management view",
        "description": "Implements a view within each pool that allows users to review, edit, and manage historical pick and result data across all previous weeks of the pool. This is important for pools that were manually set up mid-season or that have data inconsistencies. Users need to be able to correct historical entries without breaking current-week calculations.",
        "ac": "- Pool hub includes a 'Historical Data' section or tab accessible to pool owners\n- All past weeks' picks and results are displayed in a structured table or timeline\n- Pool owner can edit a historical pick (team selection) for any past week\n- Pool owner can manually mark a historical result as win/loss\n- Edits to historical data trigger recalculation of any derived analytics\n- Edit actions are logged with timestamp and user for audit purposes\n- Non-owner members can view but not edit historical data",
        "tests": "1. Navigate to pool historical data view -> verify all past weeks appear\n2. Edit a historical pick as pool owner -> verify change persists and analytics update\n3. Mark a historical result as win -> verify portfolio stats recalculate\n4. Attempt to edit as non-owner -> verify edit controls are not visible or are disabled\n5. Edit data -> verify audit log entry is created with timestamp\n6. Pool with no prior history -> verify view renders cleanly with empty state"
    },

    # ─── BATCH 4 ───────────────────────────────────────────────────────────────
    {
        "id": "35229ce5-833d-817e-8b77-df5e0281a8d3",
        "name": "IA Overhaul (1.9): Implement season selector and cross-season navigation",
        "description": "Adds a season selector to the app that allows users to navigate between different NFL seasons and access their pools, picks, and analytics for each season. This enables year-over-year analysis and ensures historical data remains accessible as new seasons are added. Season context should persist across navigation within the app.",
        "ac": "- Season selector is accessible from the main navigation or dashboard\n- All seasons with user data appear as selectable options\n- Selecting a season filters pools, entries, and analytics to that season\n- Active season context is displayed clearly in the UI\n- Cross-season navigation does not lose the user's current season context without confirmation\n- Default season is the current/active NFL season\n- Season selector gracefully handles users with data in only one season",
        "tests": "1. User with data in 2024 and 2025 seasons -> verify both appear in selector\n2. Select 2024 season -> verify pools and picks displayed are for 2024\n3. Navigate away and back -> verify season selection is preserved\n4. New user with only one season -> verify selector shows that season as default\n5. Select current (active) season -> verify live recommendations and analytics are shown\n6. Switch season while viewing entry analytics -> verify analytics update to selected season"
    },
    {
        "id": "35229ce5-833d-81ca-85ff-c41f3ddc42ff",
        "name": "IA Overhaul (1.8): Implement eliminated pool/entry access and editing",
        "description": "Ensures that pools and entries that have been eliminated (all entries knocked out) remain accessible for viewing and editing in the app. Previously eliminated pools should not disappear from the UI; users need to review their picks and results for post-season analysis. Editing should be limited to admin corrections, not active pick selection.",
        "ac": "- Eliminated pools appear in a separate 'Eliminated' section or with a clear status indicator\n- All picks, results, and analytics for eliminated pools are viewable\n- Pool owners can correct data in eliminated pools (same permissions as historical data editing)\n- Eliminated entries cannot have active picks set for future weeks\n- Navigation to an eliminated pool does not generate errors or broken states\n- Elimination status is clearly communicated (badge, label, or status indicator)",
        "tests": "1. Pool where all entries are eliminated -> verify pool still appears in My Pools\n2. Navigate into eliminated pool -> verify all past picks and results are readable\n3. Attempt to submit a new pick on an eliminated entry -> verify action is blocked\n4. Edit historical data in eliminated pool as owner -> verify edit succeeds\n5. Eliminated pool shows correct status badge/indicator in pool list"
    },
    {
        "id": "35229ce5-833d-81c7-a406-de55cda54a42",
        "name": "IA Overhaul (1.7): Design and implement week-by-week temporal navigation",
        "description": "Adds week-by-week navigation controls to pool and entry views, allowing users to step through the season chronologically and see how picks, standings, and analytics looked at each specific point in time. This temporal navigation is critical for post-game analysis and for understanding how risk evolved over the season.",
        "ac": "- Week navigation controls (prev/next arrows, week selector dropdown) appear on pool and entry views\n- Selecting a past week shows the state of picks, standings, and analytics as of that week\n- Current week is the default view when navigating to any pool or entry\n- Navigation to future weeks (not yet played) is disabled or shows empty state\n- Week navigation state is reflected in the URL for shareability\n- Analytics update correctly when navigating between weeks",
        "tests": "1. Navigate to pool view -> verify current week is default\n2. Click 'prev week' -> verify view updates to prior week's picks and standings\n3. Use week selector dropdown to jump to week 1 -> verify correct data displayed\n4. Click 'next week' at current week -> verify button is disabled or future state is shown\n5. Copy URL at week 5 view -> verify navigating to that URL shows week 5 data\n6. Navigate weeks on entry with some eliminated entries -> verify elimination state shows correctly"
    },
    {
        "id": "35029ce5-833d-81f5-b219-ca91ba9db7d3",
        "name": "Design System (2.5): Cross-browser and responsive QA pass",
        "description": "Performs a systematic quality assurance pass across all major app screens to verify the design system implementation is consistent, correct, and responsive across supported browsers and viewport sizes. Covers Chrome, Firefox, Safari, and mobile viewports. Issues found are documented and resolved before this task is marked done.",
        "ac": "- All major screens tested in Chrome, Firefox, and Safari\n- All major screens tested at 320px, 768px, 1024px, and 1440px viewport widths\n- No layout breakage, overflow, or truncation issues on any tested viewport\n- Dark theme renders correctly across all browsers\n- All interactive elements (buttons, inputs, dropdowns) are functional in all tested browsers\n- Bug report documenting all issues found and resolved is stored in the repo",
        "tests": "1. Load dashboard in Chrome, Firefox, Safari -> verify consistent appearance\n2. Resize to 320px width -> verify no horizontal scroll and all content accessible\n3. Test all form inputs at mobile viewport -> verify usability\n4. Verify dark theme tokens render consistently across browsers\n5. Check all modal dialogs in Safari -> verify they open, close, and are scrollable"
    },
    {
        "id": "35029ce5-833d-8130-994c-cafd3084a8ab",
        "name": "Design System (2.4): Restyle data display components (score cards, analytics, charts)",
        "description": "Applies the SurvivorPulse design system tokens and visual language to all data display components including score cards, analytics panels, and charts. These components are data-dense and require careful attention to typography hierarchy, color usage for status (win/loss/at-risk), and readability in both light and dark contexts.",
        "ac": "- All score cards use design system tokens for spacing, typography, and color\n- Win/loss/at-risk states use the defined semantic color system (not arbitrary hex values)\n- Charts use the design system color palette with accessible contrast ratios\n- Analytics panels have consistent header, body, and footer structure\n- All data display components render correctly in dark mode\n- No hardcoded color values remain in restyled components",
        "tests": "1. Inspect score card component -> verify no hardcoded hex colors\n2. Render win state and loss state -> verify they use correct semantic colors from design tokens\n3. Verify chart colors meet WCAG AA contrast ratio\n4. Enable dark mode -> verify all data display components remain readable\n5. Compare before/after screenshots -> verify visual consistency across components"
    },

    # ─── BATCH 5 ───────────────────────────────────────────────────────────────
    {
        "id": "35029ce5-833d-8157-9da6-c4a687d66082",
        "name": "Design System (2.3): Restyle core UI components (buttons, cards, inputs, tables, modals)",
        "description": "Applies the SurvivorPulse design system to all core UI components -- buttons, cards, form inputs, tables, and modal dialogs. These are the foundational building blocks used throughout the application, so consistency here ripples across the entire product. All component variants (sizes, states, themes) must be updated.",
        "ac": "- All button variants (primary, secondary, destructive, ghost) use design tokens\n- Form inputs (text, select, checkbox, radio) use design system focus states and sizing\n- Cards use standardized padding, border-radius, and shadow tokens\n- Tables use consistent row/header styling with design system typography\n- Modal dialogs use design system overlay, container, and header/footer styles\n- All interactive states (hover, focus, disabled) are defined and consistent\n- No inline styles or hardcoded values remain in restyled components",
        "tests": "1. Render all button variants -> verify visual consistency and correct token usage\n2. Tab through a form -> verify focus states are visible and consistent\n3. Render table with 50 rows -> verify row striping and header are styled correctly\n4. Open and close a modal -> verify overlay, animation, and close button work\n5. Toggle dark mode -> verify all components adapt correctly\n6. Run accessibility audit -> verify focus management in modals"
    },
    {
        "id": "35029ce5-833d-812a-b2a0-e7a6adecdb0a",
        "name": "Design System (2.2): Apply dark theme and typography to main app shell",
        "description": "Applies the SurvivorPulse dark theme color palette and typography system to the main application shell, including the top navigation bar, sidebar, main content area background, and global text styles. This task establishes the visual foundation that all subsequent component restyling builds on.",
        "ac": "- App shell background, surface, and border colors use design token variables\n- Global typography (font family, size scale, weight scale, line heights) is set via CSS variables\n- Navigation bar and sidebar use correct dark theme tokens\n- Theme applies consistently across all routes\n- No light-mode colors remain in the shell-level styles\n- Typography scale is documented and accessible (minimum 16px body text)",
        "tests": "1. Load app -> verify dark background and correct surface colors are applied\n2. Navigate between 3+ routes -> verify shell styling is consistent\n3. Inspect computed styles -> verify CSS variables are used, not hardcoded hex values\n4. Measure body text size -> verify minimum 16px\n5. Verify navigation bar and sidebar render with correct dark theme"
    },
    {
        "id": "35029ce5-833d-8112-8787-cfb074c4dd7c",
        "new_name": "Design System (2.1): Extract design tokens from Back Tester DESIGN.md",
        "description": "Extracts the visual design tokens (colors, typography, spacing, shadow, border-radius) documented in the Back Tester's DESIGN.md into a structured token file usable by the SurvivorPulse frontend. This establishes the canonical design token source for the entire application design system.",
        "ac": "- All color tokens from Back Tester DESIGN.md are extracted and defined in a tokens file\n- Typography tokens (font family, size scale, weight, line height) are defined\n- Spacing tokens (padding/margin scale) are defined\n- Shadow and border-radius tokens are defined\n- Tokens are structured as CSS custom properties or a JS/TS design token object\n- Token file is importable by all frontend components\n- Token names are semantic (e.g., color-surface-primary, not color-gray-900)",
        "tests": "1. Review token file -> verify all color categories from DESIGN.md are represented\n2. Import token file in a component -> verify no import errors\n3. Check token naming -> verify names are semantic and follow a consistent pattern\n4. Verify CSS variable output can be applied globally via :root\n5. Cross-reference tokens against DESIGN.md -> verify no tokens were missed"
    },
    {
        "id": "35029ce5-833d-8195-86a3-c07294d3e102",
        "new_name": "IA Overhaul (1.6): Implement dashboard/home screen",
        "description": "Implements the main dashboard/home screen as defined in the IA wireframes (task 1.3). The dashboard serves as the landing page after login, providing an at-a-glance view of active pools, this week's recommended picks, upcoming deadlines, and portfolio health indicators. It should orient the user immediately without requiring them to dig through subpages.",
        "ac": "- Dashboard displays all active pools with current status (entries alive, current week)\n- Dashboard shows this week's top recommended picks per pool\n- Upcoming pick deadlines are surfaced with time remaining\n- Portfolio health indicators (correlation risk, overall win rate) are visible\n- Empty state is handled gracefully for new users with no pools\n- Dashboard loads within 2 seconds on a standard connection\n- Responsive layout works correctly at tablet and mobile viewports",
        "tests": "1. Login with active pools -> verify all pools appear with correct status\n2. Login with no pools -> verify helpful empty state with CTA to create first pool\n3. Verify recommended picks section shows current week recommendations\n4. Verify deadlines section shows correct time remaining\n5. Load dashboard and measure time -> verify under 2 seconds\n6. View at 768px viewport -> verify layout adapts without overlap or truncation"
    },
    {
        "id": "35029ce5-833d-81c8-80c0-c2297c3fb442",
        "new_name": "IA Overhaul (1.5): Re-route existing pages into new IA structure",
        "description": "Updates all existing application routes to fit within the new information architecture structure defined in tasks 1.2 and 1.3 and implemented in task 1.4. This involves updating route paths, ensuring redirects from old URLs work correctly, and verifying that all internal navigation links resolve to the new routes.",
        "ac": "- All existing routes are updated to match the new IA structure\n- Legacy URLs redirect to new URLs with 301 redirects (or client-side equivalents)\n- All internal navigation links and programmatic router.push() calls use new routes\n- Deep links to specific pools, entries, or weeks resolve correctly\n- No broken navigation paths exist in the post-migration app\n- Route changes are documented in a migration notes file",
        "tests": "1. Navigate to each major section using old URLs -> verify redirect to new URL occurs\n2. Click every navigation link in the app -> verify no 404 or broken routes\n3. Deep-link to a specific pool entry -> verify correct page loads\n4. Verify browser back/forward navigation works correctly on new routes\n5. Check all router.push() calls in codebase -> verify they use new route paths"
    },

    # ─── BATCH 6 ───────────────────────────────────────────────────────────────
    {
        "id": "35029ce5-833d-8154-8280-c22102eb2f0c",
        "new_name": "IA Overhaul (1.4): Implement new navigation shell",
        "description": "Implements the new top-level navigation shell as designed in tasks 1.2 and 1.3. This includes the main nav bar, sidebar structure, and routing framework that all other pages will hang off of. The navigation shell establishes the visual and structural foundation for the overhauled IA.",
        "ac": "- New navigation shell is rendered on all authenticated routes\n- Top-level navigation items from the IA design are implemented and functional\n- Active route is visually indicated in the navigation\n- Navigation shell is responsive (collapses to hamburger/drawer on mobile)\n- Navigation items link to correct routes (even if destination pages are stubs)\n- Shell renders without errors when no pools exist for the user",
        "tests": "1. Log in -> verify new navigation shell renders\n2. Click each top-level nav item -> verify navigation occurs without errors\n3. Active route -> verify correct nav item is highlighted\n4. Resize to mobile -> verify navigation collapses and hamburger/drawer appears\n5. Open drawer -> verify navigation items are tappable and functional"
    },
    {
        "id": "35029ce5-833d-8181-bf34-f4f8c0d95f60",
        "new_name": "IA Overhaul (1.3): Wireframe key screens (dashboard, pool hub, analysis hub)",
        "description": "Creates wireframes for the three core screens in the new information architecture: the dashboard (home), the pool hub (per-pool management view), and the analysis hub (recommendations and analytics). Wireframes define layout, content hierarchy, and component placement without full visual design. They serve as the blueprint for implementation tasks.",
        "ac": "- Wireframes created for dashboard, pool hub, and analysis hub screens\n- Each wireframe includes desktop and mobile layouts\n- Content hierarchy is defined (what appears above the fold, primary CTAs)\n- Navigation patterns are shown (breadcrumbs, tabs, back navigation)\n- Wireframes are reviewed and approved before implementation begins\n- Wireframe files are stored in the repo (Figma link or image files)",
        "tests": "1. Review dashboard wireframe -> verify it shows pools, picks, deadlines, and portfolio health\n2. Review pool hub wireframe -> verify it covers entries, picks, and pool settings\n3. Review analysis hub wireframe -> verify it covers recommendations and analytics views\n4. Verify mobile layouts are included for all three screens\n5. Verify wireframes are accessible to developers in the repo"
    },
    {
        "id": "35029ce5-833d-816d-8119-e132f35cd855",
        "new_name": "IA Overhaul (1.2): Define new top-level navigation structure",
        "description": "Defines the new top-level information architecture and navigation structure for SurvivorPulse, addressing the UX problems identified in the audit (task 1.1). This produces a documented navigation map that identifies primary sections, hierarchy, and user flows. It is the prerequisite for all wireframing and implementation tasks in the IA Overhaul epic.",
        "ac": "- Navigation structure document defines all top-level sections and their sub-pages\n- User flows for the three primary jobs (set up a pool, make a pick, review recommendations) are mapped\n- Document addresses the UX problems identified in the task 1.1 audit\n- Navigation structure is reviewed and approved before wireframing begins\n- Document is stored in the repo",
        "tests": "1. Review nav structure doc -> verify all major app sections are defined\n2. Verify three primary user flows are mapped end-to-end\n3. Cross-reference with audit findings -> verify each audit issue has a resolution in the new structure\n4. Review with a fresh-eyes test user -> verify structure is intuitive"
    },
    {
        "id": "35029ce5-833d-81b7-baa4-c6b84d32d50b",
        "new_name": "IA Overhaul (1.1): Audit current page inventory and user flows",
        "description": "Documents the current state of the SurvivorPulse application by cataloging all existing pages, their routes, their purpose, and the current user flows for key tasks. This audit identifies navigation problems, orphaned pages, redundant flows, and missing states that need to be addressed in the IA overhaul. It is the foundation for all subsequent IA Overhaul tasks.",
        "ac": "- All existing pages and routes are cataloged with their current URL path and purpose\n- User flows for at least 3 primary tasks are mapped (create pool, make weekly pick, view recommendations)\n- UX problems and friction points are documented for each flow\n- Orphaned or unused pages are identified\n- Audit document is reviewed and stored in the repo before any redesign work begins",
        "tests": "1. Review audit doc -> verify all known app pages are listed\n2. Verify three primary flows are mapped step-by-step\n3. Verify each flow documents at least one friction point or improvement opportunity\n4. Cross-check audit against app routes -> verify no major pages were missed"
    },
    {
        "id": "35029ce5-833d-818a-8ec2-db7888c92a08",
        "new_name": "Season Data (5.1): 2026 Season Data Pipeline Readiness",
        "description": "Ensures all data pipeline components are ready to ingest, process, and serve 2026 NFL season data before the season begins in September 2026. This includes verifying that all scheduled jobs, data sources, transformations, and database schemas are prepared for the new season. Any schema changes, new team additions, or rule changes for 2026 are addressed here.",
        "ac": "- All scheduled data ingestion jobs are updated and tested for 2026 season compatibility\n- Database schemas support 2026 season data without migration errors\n- Spread data, game schedule, and team data sources are verified for 2026\n- Any rule changes (schedule format, team relocations) are handled in the pipeline\n- Pipeline readiness is verified with a dry-run using mock 2026 week 1 data\n- Checklist of all pipeline components with verified/unverified status is documented",
        "tests": "1. Run dry-run with mock 2026 week 1 data -> verify data flows through all pipeline stages\n2. Verify spread refresh job runs and populates 2026 game data correctly\n3. Verify team roster and schedule data reflects 2026 season format\n4. Run all DB migrations -> verify no errors on existing data\n5. Verify backtester can access 2026 season data after pipeline readiness completion"
    },

    # ─── BATCH 7 ───────────────────────────────────────────────────────────────
    {
        "id": "35029ce5-833d-8110-84f3-d985a3aba5da",
        "new_name": "Infrastructure (6.1): Onboarding Email Sequence Hooks",
        "description": "Implements the backend hooks that trigger the onboarding email sequence when a new user registers. When a user signs up, the system should enqueue a series of timed onboarding emails via Postmark that introduce key features and help users complete their first pool setup. This task covers the trigger logic and email scheduling, not the email content itself.",
        "ac": "- New user registration event triggers the onboarding sequence enrollment\n- Onboarding emails are scheduled at defined intervals post-registration (e.g., day 0, day 2, day 5)\n- Each scheduled email is associated with a specific template identifier\n- Users who complete first-pool setup before a scheduled email receive a modified or skipped email\n- Unsubscribe handling is respected (no emails to users who have opted out)\n- Email delivery is logged with status (sent, failed, skipped) per user",
        "tests": "1. Register new user -> verify onboarding sequence is enqueued with correct schedule\n2. Complete first pool setup -> verify appropriate follow-up emails are skipped or modified\n3. Unsubscribe user -> verify no onboarding emails are sent\n4. Check email logs after trigger -> verify each email has delivery status recorded\n5. Simulate Postmark delivery failure -> verify error is logged and retry is scheduled"
    },
    {
        "id": "35029ce5-833d-81e1-92c8-de381c05e9c7",
        "new_name": "Auth & Accounts (9.1): Founding Member Launch Flow (Stripe)",
        "description": "Implements the Founding Member subscription flow using Stripe, giving early users access to a special discounted or lifetime pricing tier before the public launch. This includes creating the Stripe price, building the checkout flow, handling webhooks for subscription activation, and displaying Founding Member status in the user's account.",
        "ac": "- Founding Member Stripe price is created and active\n- Users can access the Founding Member checkout flow from the pricing or signup page\n- Successful Stripe checkout creates and activates a subscription in the database\n- Stripe webhooks correctly handle checkout.session.completed and customer.subscription.created events\n- Founding Member status is visible in user account/profile page\n- Founding Member access gates the same features as the full subscription\n- Failed or abandoned checkouts are handled gracefully with clear user messaging",
        "tests": "1. Complete Founding Member checkout with test card -> verify subscription is activated\n2. Use Stripe test card for declined payment -> verify user sees clear error and is not charged\n3. Simulate webhook for checkout.session.completed -> verify subscription record created in DB\n4. Log in post-purchase -> verify Founding Member badge/status appears in account\n5. Access a subscription-gated feature -> verify Founding Member user has access\n6. Abandon checkout midway -> verify user is not charged and is redirected appropriately"
    },
    {
        "id": "35029ce5-833d-8133-bf39-f77c60a75db5",
        "new_name": "Marketing (17.1): Waitlist/Email Capture on Landing Page",
        "description": "Implements an email capture and waitlist signup form on the SurvivorPulse public landing page, allowing interested visitors to register their interest before or during the launch period. Captured emails are stored in the database and/or synced to an email marketing tool for subsequent campaign communications.",
        "ac": "- Landing page includes a prominent email capture form with a clear value proposition\n- Submitted emails are stored in the database with a source tag\n- Confirmation message or redirect is shown after successful submission\n- Duplicate email submissions are handled gracefully (no error, silent dedup)\n- Submitted emails are accessible to admins for export or campaign use\n- Form is mobile-friendly and accessible\n- Basic bot protection (honeypot or rate limiting) is implemented",
        "tests": "1. Submit valid email on landing page -> verify stored in DB and confirmation shown\n2. Submit same email twice -> verify no duplicate created and no error shown\n3. Submit invalid email format -> verify validation error shown\n4. Submit on mobile viewport -> verify form is usable\n5. Check DB after 5 test submissions -> verify all emails present with source tag\n6. Rapidly submit 10 times -> verify rate limiting triggers"
    },
    {
        "id": "35029ce5-833d-81d8-859b-c1ab9dd252ca",
        "new_name": "Infrastructure (6.2): Referral Tracking System",
        "description": "Builds a referral tracking system that assigns unique referral codes to users and tracks signups that originated from those codes. This enables word-of-mouth growth tracking and provides the infrastructure for future referral incentive programs. Each referral code is tied to the referring user's account and the conversion is logged.",
        "ac": "- Each user has a unique referral code generated on account creation\n- Referral code is shareable via a copy-link feature in account settings\n- Signups that use a referral code are linked to the referring user in the database\n- Referral conversion count is visible to users in their account\n- Referral codes are case-insensitive and URL-safe\n- Referral tracking survives users registering on a different device (cookie or URL param)\n- Self-referrals are detected and not counted",
        "tests": "1. Register new user -> verify referral code is generated and visible\n2. Use referral link to sign up new user -> verify referral conversion is logged\n3. Referring user logs in -> verify their referral count incremented\n4. Attempt self-referral -> verify not counted as conversion\n5. Use referral code in uppercase -> verify case-insensitive match works\n6. Sign up via referral on different device -> verify referral still tracked"
    },
    {
        "id": "34529ce5-833d-803a-a001-caec779fc18f",
        "new_name": "Marketing (17.2): Revamp Public Website",
        "description": "Redesigns and rebuilds the SurvivorPulse public-facing website to clearly communicate the product's value proposition to the target audience of serious survivor pool players. The revamped site should drive signups and demonstrate the product's unique CMEA and correlation risk management capabilities with minimal jargon.",
        "ac": "- Homepage clearly states the primary value proposition in the hero section\n- Key features (CMEA, correlation risk, ROI analysis) are explained with visuals or demos\n- Pricing section is present and up to date\n- Clear primary CTA (sign up, start free trial, or join waitlist) is prominent throughout\n- Site is mobile-responsive and loads within 3 seconds (LCP)\n- SEO meta tags (title, description, OG tags) are set on all pages\n- Old site content is fully replaced; no placeholder or lorem ipsum text remains",
        "tests": "1. Load homepage -> verify hero CTA is immediately visible above the fold\n2. Verify mobile rendering at 375px -> verify no layout breaks\n3. Measure LCP on homepage -> verify under 3 seconds\n4. Inspect page source -> verify title, description, and OG tags are set\n5. Review all copy -> verify no placeholder or lorem ipsum text exists\n6. Test all CTA buttons -> verify they navigate to correct destination"
    },

    # ─── BATCH 8 ───────────────────────────────────────────────────────────────
    {
        "id": "33d29ce5-833d-8146-89d3-ee1daa1810e5",
        "new_name": "Marketing (17.3): Editorial Pass: Rationale Copy (perPickReasonByTeamId)",
        "description": "Reviews and rewrites the rationale copy generated for each team pick recommendation stored in perPickReasonByTeamId. The current copy may be generic, technical, or unclear to non-expert users. This editorial pass ensures rationale text is concise, readable, and compelling -- making recommendations feel trustworthy and actionable rather than algorithmic.",
        "ac": "- All team rationale strings in perPickReasonByTeamId are reviewed\n- Copy is written at an accessible reading level (no unexplained jargon)\n- Each rationale is 1-3 sentences and directly explains why the team is recommended\n- Rationale references at least one concrete signal (spread, historical performance, or matchup factor)\n- Updated copy is committed and deployed\n- No two teams have identical rationale strings",
        "tests": "1. Review 10 random rationale strings -> verify none are generic or template-like\n2. Check all rationale strings for readability (no unexplained acronyms or formulas)\n3. Verify each rationale references at least one specific signal\n4. Check for duplicate rationale strings -> verify none exist\n5. User test: show 5 rationale strings to a non-expert -> verify they understand the pick reasoning"
    },
    {
        "id": "33c29ce5-833d-81a9-91e9-c1ab0a72678e",
        "new_name": "Fix (20.1): Independent path pWinNow ordering and correlated loss math in portfolioRecommendation.ts",
        "description": "Fixes two related bugs in portfolioRecommendation.ts: incorrect ordering of independent-path picks by pWinNow, and incorrect correlated loss math when multiple entries share the same pick. These bugs cause the recommendation engine to produce suboptimal orderings and incorrect risk assessments for correlated portfolios.",
        "ac": "- Independent-path picks are correctly ordered by descending pWinNow after the fix\n- Correlated loss probability is calculated correctly when multiple entries share the same team pick\n- Fixed behavior is verified against known correct outputs from manual calculation\n- Unit tests are added covering both the ordering and correlated loss scenarios\n- No regression to previously passing tests",
        "tests": "1. Run recommendation with 3 independent-path entries -> verify picks ordered by descending pWinNow\n2. Run recommendation with 2 entries picking same team -> verify correlated loss math is correct\n3. Run existing unit test suite -> verify all previously passing tests still pass\n4. Edge case: single entry portfolio -> verify no ordering or math errors\n5. Compare pre-fix vs post-fix output on a known test case -> verify expected improvement"
    },
    {
        "id": "33529ce5-833d-812b-b096-ec1d831db682",
        "new_name": "Refactor (21.1): Rename PlayoffCandidate Interface to SurvivorCandidate",
        "description": "Renames the PlayoffCandidate TypeScript interface to SurvivorCandidate throughout the codebase to better reflect the product's domain terminology. The current name implies football playoffs, which is misleading -- the interface represents candidates for survivor pool selection, not playoff participants. This is a pure refactor with no behavior changes.",
        "ac": "- All occurrences of PlayoffCandidate interface name are renamed to SurvivorCandidate\n- All import statements referencing PlayoffCandidate are updated\n- TypeScript compilation succeeds with zero errors after the rename\n- No test file or runtime behavior is changed\n- A brief code comment documents why the rename was made (for future reference)",
        "tests": "1. Run TypeScript compiler -> verify zero errors after rename\n2. Run grep for 'PlayoffCandidate' -> verify zero occurrences remain\n3. Run full test suite -> verify all tests pass with no failures\n4. Check that SurvivorCandidate is used consistently wherever picks are evaluated"
    },
    {
        "id": "33529ce5-833d-81c1-94e3-c43fe5f05ce1",
        "new_name": "Mobile (23.1): Mobile App",
        "description": "Designs and builds a native or PWA mobile application for SurvivorPulse, enabling users to manage their survivor pools, submit picks, and view recommendations on iOS and Android. Mobile is a critical channel for pick submission since deadlines often hit while users are away from their computers. The approach (React Native, PWA, or hybrid) should be defined before implementation begins.",
        "ac": "- Approach decision (PWA vs native) is documented and approved before build begins\n- Core user flows are mobile-native: view picks, submit pick, view recommendations, view standings\n- Push notifications for pick deadlines are supported\n- App is available on iOS App Store and/or Google Play Store (or installed as PWA)\n- App performance: cold start under 3 seconds on mid-range devices\n- Authentication is persistent (user stays logged in across app restarts)\n- App supports offline viewing of last-synced data",
        "tests": "1. Install app on iOS -> verify app launches and user can log in\n2. Submit weekly pick from mobile -> verify pick is saved and visible on web\n3. Enable deadline notification -> verify push notification arrives before deadline\n4. Kill app and reopen -> verify user remains authenticated\n5. Go offline -> verify last-synced recommendations are viewable\n6. Test on mid-range Android device -> verify cold start under 3 seconds"
    },
    {
        "id": "33529ce5-833d-811a-8f03-f60e4b5e6fc2",
        "new_name": "Auth & Accounts (9.2): Allow Free Subscriptions for Select Users",
        "description": "Implements the ability for admins to grant free subscription access to specific users without requiring payment. This is needed for early testers, partners, beta users, and promotional arrangements. Free subscriptions should have the same feature access as paid subscriptions and should not expire unless explicitly revoked.",
        "ac": "- Admin can grant a free subscription to any user via the admin panel or API\n- Free subscriptions grant identical feature access as paid tier\n- Free subscription status is visible in the user's account\n- Admin can view a list of all users with free subscriptions\n- Admin can revoke a free subscription, which downgrades the user to free tier\n- Free subscriptions do not trigger Stripe billing\n- Audit log records who granted the free subscription and when",
        "tests": "1. Admin grants free subscription to test user -> verify user has full feature access\n2. Granted user checks account page -> verify free subscription status is shown\n3. Admin views free subscription list -> verify test user appears\n4. Admin revokes free subscription -> verify user loses premium access\n5. Verify Stripe is not charged for free subscription grant\n6. Check audit log -> verify grant and revoke events are logged with admin user ID"
    },

    # ─── BATCH 9 ───────────────────────────────────────────────────────────────
    {
        "id": "33529ce5-833d-812d-8f65-fb4a1793b317",
        "new_name": "Infrastructure (6.3): Send Weekly Email: Recommended Picks",
        "description": "Implements an automated weekly email that sends each active subscriber their recommended picks for the upcoming week, sent each week on a configured schedule (e.g., Wednesday morning after game spreads are available). The email includes the top recommended teams per entry with brief rationale, delivered via Postmark.",
        "ac": "- A cron job or scheduled function sends the weekly recommendations email on the configured schedule\n- Email is sent only to active subscribers with at least one active pool entry\n- Email content includes recommended team per entry with brief rationale\n- Postmark template is used with proper header, CTA, and unsubscribe footer\n- Users who have opted out of recommendation emails do not receive them\n- Email delivery status is logged per user per week\n- Failed sends are retried once before being logged as failed",
        "tests": "1. Trigger weekly email job -> verify email is sent to all qualifying users\n2. Verify user with no active entries does not receive the email\n3. Unsubscribe a user -> verify they are excluded from the send\n4. Inspect delivered email -> verify it contains team recommendations and rationale\n5. Simulate Postmark send failure -> verify retry logic and failed status is logged\n6. Run job twice in the same week -> verify no duplicate emails are sent"
    },
    {
        "id": "33529ce5-833d-8154-a672-d496ba1e04e0",
        "new_name": "Marketing (17.4): Add Documentation and FAQs",
        "description": "Creates and publishes product documentation and a FAQ section covering how SurvivorPulse works, how to use key features (CMEA, correlation scoring, ROI analysis), and answers to common survivor pool questions. Documentation should be accessible from the product and from the public website and should reduce support burden.",
        "ac": "- Documentation covers at minimum: getting started, pool setup, entry management, reading recommendations, understanding correlation scores\n- FAQ section addresses at least 10 common questions\n- Documentation is accessible from both the app (help link) and the public website\n- All content is written at an accessible level for non-expert users\n- Documentation can be updated without a code deploy (managed via CMS or markdown)\n- No placeholder or unfinished content is published",
        "tests": "1. Navigate to help/docs from inside app -> verify documentation loads\n2. Navigate to FAQ from public website -> verify FAQ section is accessible\n3. Review all docs pages -> verify no placeholder or lorem ipsum text\n4. Test on mobile -> verify documentation is readable without horizontal scroll\n5. Update one doc section -> verify it can be changed without a full redeploy\n6. Review FAQ -> verify at least 10 questions are answered"
    },
    {
        "id": "33529ce5-833d-8172-917d-f65678d77ce3",
        "new_name": "DevOps (7.1): Disable NFL Spread Refresh Scheduler After Playoffs",
        "description": "Implements logic to automatically disable or suspend the NFL spread refresh scheduled job at the end of the NFL postseason, preventing unnecessary API calls and data storage during the offseason. The scheduler should re-enable automatically when a new season's data becomes available, or have a clear manual enable process.",
        "ac": "- Spread refresh scheduler detects end of NFL season (no more scheduled games) and disables itself\n- Disabled state is logged and visible in admin monitoring\n- Re-enable process is documented (manual trigger or automatic on new season data)\n- No unnecessary API calls are made to spread data sources during the offseason\n- Scheduler behavior is configurable (enable/disable) via an admin setting without a code deploy",
        "tests": "1. Set current date to post-Super Bowl with no games scheduled -> verify scheduler disables\n2. Check logs after automatic disable -> verify disable event is logged\n3. Verify no spread refresh API calls in logs during disabled period\n4. Admin manually re-enables scheduler -> verify it resumes on next scheduled run\n5. Set season start date -> verify scheduler auto-enables if configured to do so"
    },
    {
        "id": "33529ce5-833d-8179-be8c-d0c21ac18822",
        "new_name": "Marketing (17.5): SEO Optimization",
        "description": "Optimizes the SurvivorPulse public website for search engine visibility, targeting keywords relevant to serious survivor pool players. This includes on-page optimization (meta tags, headers, content), technical SEO (sitemap, robots.txt, Core Web Vitals), and structured data. Goal is to rank for survivor pool strategy and tool searches.",
        "ac": "- Meta titles and descriptions are set on all public pages with target keywords\n- H1/H2 heading hierarchy is correct and keyword-optimized on key pages\n- XML sitemap is generated and submitted to Google Search Console\n- robots.txt is correctly configured\n- Core Web Vitals (LCP, CLS, FID) pass at Good threshold\n- Structured data (JSON-LD) is added to key pages\n- Internal linking structure supports crawlability",
        "tests": "1. Inspect homepage source -> verify title, description, and OG tags are set\n2. Run Google Lighthouse -> verify all Core Web Vitals pass at Good threshold\n3. Check robots.txt -> verify it allows crawling of key pages\n4. Submit sitemap to Search Console -> verify accepted with no errors\n5. Run structured data test -> verify no errors on JSON-LD markup"
    },

    # ─── BATCH 10 ──────────────────────────────────────────────────────────────
    {
        "id": "33529ce5-833d-819e-9f64-cfd18aadd350",
        "new_name": "Admin (18.1): Show Read-Only NFL Games & Spreads to Non-Admin Users",
        "description": "Makes NFL game schedules and spread data visible to all authenticated users (not just admins) in a read-only format. Currently this data is admin-only, which prevents users from seeing the raw inputs that drive recommendations. Exposing it transparently builds trust and helps users verify recommendation logic.",
        "ac": "- All authenticated users can view the current week's NFL games and spreads\n- Data is read-only; non-admin users cannot edit or refresh spreads\n- Data is displayed in a clear, scannable table or list format\n- Spreads are shown with relevant context (home/away, favorite/underdog)\n- Data source and last-updated timestamp are visible\n- View is accessible from the analysis hub or a dedicated games page",
        "tests": "1. Log in as non-admin -> verify NFL games and spreads are visible\n2. Attempt to edit a spread as non-admin -> verify edit is blocked\n3. Verify last-updated timestamp is displayed\n4. Admin updates a spread -> verify non-admin sees updated value\n5. View on mobile -> verify games table is readable without horizontal scroll"
    },
    {
        "id": "33529ce5-833d-81b4-8ac6-eca4c8c34760",
        "new_name": "Admin (18.2): Show Yahoo Pick Popularity Data to Non-Admin Users",
        "description": "Exposes Yahoo survivor pool pick popularity data (percentage of the field picking each team this week) to all authenticated users in a read-only view. This data is currently admin-only but is a highly valuable input for avoiding field concentration and making contrarian picks. Showing it improves the product's analytical depth.",
        "ac": "- All authenticated users can view Yahoo pick popularity percentages for the current week\n- Data is read-only for non-admin users\n- Popularity data is displayed alongside game and spread data for context\n- Data source and last-updated timestamp are visible\n- Missing or stale data is clearly indicated rather than silently hidden\n- View is integrated into the analysis hub or games view",
        "tests": "1. Log in as non-admin -> verify Yahoo popularity percentages are visible\n2. Attempt to edit popularity data as non-admin -> verify blocked\n3. Data is stale (more than 24h) -> verify staleness indicator is shown\n4. No popularity data available for a game -> verify graceful empty state\n5. Verify popularity data appears alongside spread data in the same view"
    },
    {
        "id": "33529ce5-833d-81b6-bc32-e435c5c7dbd4",
        "new_name": "DevOps (7.2): Send Test Emails with Filter-Friendly Subject Lines",
        "description": "Updates the test email sending functionality to use subject lines that are unlikely to trigger spam filters or be misclassified as production emails. Test emails should be clearly identifiable as tests without containing patterns that commonly trigger spam filters. This improves deliverability testing reliability.",
        "ac": "- Test emails use a subject line prefix that identifies them as tests (e.g., [TEST])\n- Test subject lines do not contain all-caps words, excessive punctuation, or spam trigger phrases\n- Test email sender address or reply-to is distinguishable from production\n- Test email sending is gated to admin or dev environments only\n- Documentation notes the test vs production subject line distinction",
        "tests": "1. Send test email -> verify subject line includes [TEST] prefix\n2. Run subject line through spam checker tool -> verify no high-risk flags\n3. Attempt to send test email as non-admin -> verify blocked\n4. Verify test email cannot be triggered in production environment config"
    },
    {
        "id": "33529ce5-833d-81bb-8e31-cff8ace635c8",
        "new_name": "Auth & Accounts (9.3): Add User Settings Features",
        "description": "Builds a user settings page where users can manage their account preferences, including notification preferences, display preferences, email address, password, and connected accounts. This is a foundational account management feature that reduces friction for users who want to customize their experience.",
        "ac": "- User settings page is accessible from account menu\n- User can update email address (with re-verification flow)\n- User can change password (current password required)\n- User can configure notification preferences (which emails to receive)\n- User can set display preferences (e.g., time zone)\n- Settings are persisted and take effect immediately\n- All form validations provide clear error messages",
        "tests": "1. Navigate to settings -> verify all sections are present\n2. Change email address -> verify verification email sent to new address\n3. Change password with wrong current password -> verify error shown\n4. Toggle off recommendation emails -> verify user excluded from next weekly send\n5. Update timezone -> verify event times display in new timezone\n6. Submit invalid email format -> verify validation error"
    },
    {
        "id": "33529ce5-833d-81bf-98fe-df856c464b71",
        "new_name": "Infrastructure (6.4): Add Google Analytics / Adobe Analytics",
        "description": "Integrates Google Analytics 4 (or Adobe Analytics) into the SurvivorPulse application to track user behavior, feature adoption, and conversion events. This data is essential for understanding which features drive engagement, where users drop off, and how effectively the product converts visitors to subscribers.",
        "ac": "- GA4 (or Adobe Analytics) tracking code is installed on all pages\n- Key conversion events are tracked: registration, subscription start, first pool created, first pick submitted\n- Page views are tracked with route changes in the SPA\n- Personal data (email, user ID) is not sent to analytics without proper anonymization\n- Analytics data is visible in the dashboard within 24 hours of implementation\n- Implementation is gated by user consent where required (GDPR/CCPA)",
        "tests": "1. Install analytics and navigate app -> verify page views appear in GA4 real-time\n2. Complete registration flow -> verify registration event fires\n3. Subscribe -> verify subscription event fires with correct value\n4. Inspect analytics payload -> verify no PII (email) is sent without anonymization\n5. Verify consent gate works correctly before tracking starts"
    },

    # ─── BATCH 11 ──────────────────────────────────────────────────────────────
    {
        "id": "33529ce5-833d-81cf-8106-d204ff15916d",
        "new_name": "Admin (18.3): Add Admin Feature to Update Spreads Manually",
        "description": "Adds an admin interface for manually updating or overriding NFL game spreads when the automated data source provides incorrect or delayed data. Admins should be able to edit the spread for any game in the current week without triggering a full data refresh. Manual overrides should be logged for auditing.",
        "ac": "- Admin panel includes a spread management section for the current week's games\n- Admin can edit the spread value for any individual game\n- Manual override is clearly flagged in the database (is_manual_override field)\n- Override is logged with admin user ID, timestamp, old value, and new value\n- Automated spread refresh does not overwrite manual overrides (or prompts admin before doing so)\n- Non-admin users cannot access the spread edit feature",
        "tests": "1. Admin edits spread for a game -> verify new value is saved\n2. Check database -> verify is_manual_override=true and audit log entry created\n3. Trigger automated spread refresh after manual override -> verify override is preserved\n4. Non-admin attempts to access spread edit -> verify blocked\n5. Admin overrides a spread -> verify change is reflected in user-facing data immediately"
    },
    {
        "id": "33529ce5-833d-8109-8886-d0b0975648e7",
        "new_name": "Pool Mgmt (11.1): Weekly Checklist Feature Per Pool",
        "description": "Adds a per-pool weekly checklist that helps users stay on top of their survivor pool obligations each week. The checklist includes tasks like reviewing recommendations, setting picks for each entry, and verifying pick submission before the deadline. Checklist state resets each week and tracks completion per entry.",
        "ac": "- Each pool has a weekly checklist visible to the pool owner/member\n- Default checklist items include: review recommendations, set pick for each entry, confirm submission\n- Completed checklist items are marked with a visual indicator\n- Checklist resets automatically at the start of each new week\n- Checklist completion percentage is visible on the dashboard\n- Custom checklist items can be added by the pool owner",
        "tests": "1. Navigate to active pool -> verify weekly checklist is visible\n2. Submit a pick -> verify corresponding checklist item auto-marks as complete\n3. Advance to next week -> verify checklist resets\n4. Dashboard view -> verify checklist completion percentage is shown\n5. Add custom checklist item -> verify it appears and can be checked off"
    },
    {
        "id": "33529ce5-833d-810a-a823-f519973e2196",
        "new_name": "Marketing (17.6): Update Homepage Screenshots",
        "description": "Replaces outdated screenshots on the SurvivorPulse marketing site and app store listings with current, high-quality screenshots that reflect the current product UI and key features. Screenshots are a key trust signal for prospective users evaluating the product.",
        "ac": "- All screenshots on the public website are updated to show the current UI\n- Screenshots showcase key features: dashboard, recommendations, correlation scoring\n- Screenshots are high-resolution (at least 1440x900 for web, app store dimensions for mobile)\n- Alt text is set on all screenshot images for accessibility and SEO\n- Screenshots do not contain any test data, placeholder content, or internal user information",
        "tests": "1. Review all marketing site screenshots -> verify they show current UI (no old design)\n2. Inspect screenshot images -> verify minimum 1440x900 resolution\n3. Check alt text on all screenshots -> verify descriptive alt text is set\n4. Verify no screenshots contain test user data or internal information"
    },
    {
        "id": "33529ce5-833d-810b-9944-da79bbf969ad",
        "new_name": "UX/Design (1.11): Add Feedback Drawer to Each Page",
        "description": "Implements a persistent feedback drawer or button accessible on every page of the application, allowing users to submit contextual feedback about their current view. Feedback is tagged with the page/route and submitted user context, making it actionable for product development. This is a lightweight always-on feedback channel.",
        "ac": "- Feedback trigger (button or tab) is visible on every authenticated page\n- Clicking the trigger opens a drawer with a short feedback form (rating + freetext)\n- Submitted feedback is tagged with current route, user ID, and timestamp\n- Feedback is stored in a database table accessible to admins\n- Feedback drawer does not obscure critical page content when closed\n- Submission shows a thank-you confirmation",
        "tests": "1. Open any page -> verify feedback trigger is visible\n2. Open feedback drawer -> verify form contains rating and freetext fields\n3. Submit feedback -> verify thank-you message shown and drawer closes\n4. Check database -> verify feedback record includes route, user ID, and timestamp\n5. Admin views feedback list -> verify submission appears with full context\n6. Verify closed drawer does not obstruct navigation or content"
    },
    {
        "id": "33529ce5-833d-811e-9472-e11788fd8214",
        "new_name": "Pool Mgmt (11.2): Import/Link Pool",
        "description": "Allows users to import or link an existing survivor pool from an external platform (e.g., Yahoo, ESPN, or a manual import via CSV) so that their external pool is tracked within SurvivorPulse. This reduces setup friction for users who already have active pools on other platforms.",
        "ac": "- User can initiate an import/link flow from the My Pools page\n- At minimum, manual CSV or form-based import of pool structure is supported\n- Imported pool data includes: field size, entry count, current week, picks made to date\n- User is shown a confirmation of what will be imported before committing\n- Import errors (malformed data, missing required fields) are reported clearly\n- Imported pool appears in My Pools after successful import",
        "tests": "1. Import a valid pool via CSV -> verify pool appears in My Pools\n2. Review import confirmation screen -> verify it shows correct pool details before commit\n3. Import CSV with missing required field -> verify descriptive error shown\n4. Import malformed CSV -> verify graceful error, no partial data imported\n5. Imported pool -> verify it can be used for recommendations after import"
    },

    # ─── BATCH 12 ──────────────────────────────────────────────────────────────
    {
        "id": "33529ce5-833d-8158-a22a-f7f6c14b15b1",
        "new_name": "Pool Mgmt (11.3): Copy Pool",
        "description": "Adds the ability for users to duplicate an existing pool configuration to create a new pool with the same settings. This is useful for users who run the same pool structure year after year or who want to experiment with modified settings without affecting an active pool. The copy includes pool settings but not historical picks or results.",
        "ac": "- User can copy any pool they own from the pool settings or pool list\n- Copied pool inherits all configuration settings from the source pool\n- Historical picks, results, and entries are NOT copied\n- User is prompted to name the new pool before creation\n- Copied pool is created as a new Backlog-status pool (not active)\n- Copy operation is atomic: it either fully succeeds or fails with no partial state",
        "tests": "1. Copy an existing pool -> verify new pool appears with same settings\n2. Check copied pool -> verify no historical picks or results are present\n3. Verify copied pool is in draft/setup state, not active\n4. Copy pool and rename -> verify new name is saved correctly\n5. Simulate copy failure -> verify no partial pool record is created"
    },
    {
        "id": "33529ce5-833d-8179-b9c8-d4a5ceeb7167",
        "new_name": "Pool Mgmt (11.4): Add Calculation Settings Feature",
        "description": "Exposes pool-level calculation settings to users, allowing them to configure how the recommendation engine weights different factors (win probability, future value, field concentration) for their specific pool. Different pools may warrant different weighting strategies, and this feature gives power users direct control over the calculation parameters.",
        "ac": "- Pool settings page includes a calculation settings section\n- Settings expose at minimum: win probability weight, future value weight, field concentration sensitivity\n- Settings are saved per pool and applied when generating recommendations for that pool\n- Default values are pre-filled and reflect the current engine defaults\n- User can reset to defaults with a single action\n- Changes to calculation settings trigger a recommendation recalculation",
        "tests": "1. Open pool calculation settings -> verify weight sliders or inputs are present\n2. Increase future value weight -> verify recommendations change accordingly\n3. Reset to defaults -> verify original values are restored\n4. Save settings -> verify they persist after page reload\n5. Verify default values match the documented engine defaults"
    },
    {
        "id": "33529ce5-833d-8190-9d55-db6b27392be2",
        "new_name": "Pool Mgmt (11.5): Lock Edit Pool After Season Ends",
        "description": "Automatically locks pool configuration editing when the NFL season ends, preventing accidental modifications to the historical record of a completed pool. Pool owners should still be able to view all data but not change pool settings or structure after the season is over. Admin override should be available.",
        "ac": "- Pool edit controls are disabled automatically when the NFL season end date passes\n- Locked pools display a clear visual indicator and explanation\n- Pool data (picks, results, analytics) remains fully viewable when locked\n- Admins can override the lock to edit a pool if needed\n- Lock state is persisted in the database\n- Lock triggers for both fully completed and eliminated pools at season end",
        "tests": "1. Set season end date to past -> verify pool edit controls are disabled\n2. Attempt to submit pool settings change on locked pool -> verify blocked\n3. View locked pool -> verify all historical data is still readable\n4. Admin overrides lock -> verify edit controls become available\n5. Verify locked indicator (badge or message) is visible to pool owner"
    },
    {
        "id": "33529ce5-833d-819f-87e7-db483bcc12f1",
        "new_name": "Pool Mgmt (11.6): Add Filtering and Favorites to My Pools Page",
        "description": "Enhances the My Pools page with filtering and favorites functionality to help users with multiple pools quickly navigate to what matters most. Filters should cover status (active, eliminated, completed), season, and pool type. Favorites allow users to pin their most important pools to the top of the list.",
        "ac": "- My Pools page includes filter controls for status, season, and pool type\n- User can mark any pool as a favorite\n- Favorited pools appear at the top of the list or in a dedicated favorites section\n- Filter state persists across page refreshes\n- Filtering works correctly when combined (e.g., active + 2025 season)\n- Empty state is shown when filters return no matching pools",
        "tests": "1. Filter by status 'active' -> verify only active pools appear\n2. Combine filters (active + 2025) -> verify correct subset shown\n3. Mark pool as favorite -> verify it appears at top of list\n4. Reload page -> verify filter state and favorites are preserved\n5. Apply filter that matches no pools -> verify empty state message is shown"
    },
    {
        "id": "33529ce5-833d-81bb-b1d8-f83a70bf0912",
        "new_name": "UX/Design (1.12): Add Team Detail Drawer to Entry Analytics",
        "description": "Adds a detail drawer that opens when a user clicks on a team in their entry analytics view, surfacing team-specific data relevant to survivor pool decisions: season record, remaining schedule difficulty, current spread, and this team's pick history for the user. This replaces navigation away from the current view with an in-context panel.",
        "ac": "- Clicking any team name or logo in entry analytics opens a detail drawer\n- Drawer displays: team record, remaining schedule, current week spread, user's pick history for this team\n- Drawer can be closed without losing the current analytics view state\n- Drawer is accessible on mobile (bottom sheet or full-screen overlay)\n- Drawer loads team data without a full page reload\n- Teams with no remaining schedule show appropriate messaging",
        "tests": "1. Click team in entry analytics -> verify drawer opens with team data\n2. Verify drawer shows team record, spread, and pick history\n3. Close drawer -> verify entry analytics view is unchanged\n4. Open drawer on mobile -> verify it renders as bottom sheet or full overlay\n5. Click team with no remaining games -> verify graceful empty state in drawer"
    },

    # ─── BATCH 13 ──────────────────────────────────────────────────────────────
    {
        "id": "33529ce5-833d-81c4-a72d-cd1fe1f2f036",
        "new_name": "UX/Design (1.13): Implement Unsaved Changes Alert",
        "description": "Adds a browser-native or custom unsaved changes alert that warns users before they navigate away from a form or settings page with unsaved edits. This prevents accidental data loss when users click away from pool setup, entry editing, or settings forms without saving.",
        "ac": "- Unsaved changes alert appears when user attempts to navigate away from a form with edits\n- Alert gives user option to stay (continue editing) or leave (discard changes)\n- Alert triggers for pool settings, entry settings, and calculation settings forms\n- Alert does not trigger when there are no unsaved changes\n- Alert works on both browser back/forward navigation and in-app link clicks\n- Alert is suppressed after successful save",
        "tests": "1. Edit pool settings and click nav link without saving -> verify alert appears\n2. Choose 'stay' in alert -> verify user remains on form with changes intact\n3. Choose 'leave' in alert -> verify user navigates away and changes are discarded\n4. Save form and click nav link -> verify no alert shown\n5. Open form without making changes and navigate away -> verify no alert shown\n6. Trigger browser back button with unsaved changes -> verify alert appears"
    },
    {
        "id": "33529ce5-833d-811b-bf3f-c11ba238317f",
        "new_name": "Refactor (21.2): Refactor NFL Regular Season Pools for 2026",
        "description": "Refactors the NFL regular season pool logic to ensure compatibility with the 2026 NFL season, addressing any hardcoded season assumptions, week counts, schedule formats, or team data that would break as the codebase moves from 2025 to 2026. This should also improve the generalizability of the season pool model for future years.",
        "ac": "- All hardcoded references to the 2025 season are replaced with configurable values\n- Week count and schedule format are driven by configuration, not hardcoded constants\n- Pool model correctly handles the 2026 regular season (18 weeks, current team list)\n- Existing 2025 pool data is not affected by the refactor\n- All tests pass after refactor with no behavior regressions\n- Code is documented where season-specific assumptions exist",
        "tests": "1. Create a 2026 regular season pool -> verify it uses correct 18-week structure\n2. Run full test suite -> verify no regressions\n3. Grep for hardcoded year values -> verify 2025 references are removed\n4. Load existing 2025 pool -> verify no data loss or display errors"
    },
    {
        "id": "33529ce5-833d-8132-846f-d301157829cd",
        "new_name": "Pool Mgmt (11.7): Pool Schedule Types: Regular, Regular+Playoffs, Playoffs-Only",
        "description": "Adds support for three distinct pool schedule types: Regular Season only (weeks 1-18), Regular Season plus Playoffs, and Playoffs-only. Different survivor pools have different scopes, and the product needs to correctly support each type by adjusting available weeks, team eligibility, and recommendation logic accordingly.",
        "ac": "- Pool creation includes a schedule type selector (Regular, Regular+Playoffs, Playoffs-Only)\n- Each schedule type restricts the available weeks for pick selection appropriately\n- Recommendation engine accounts for schedule type when calculating future value\n- Existing pools default to Regular Season type without data loss\n- Schedule type is displayed in pool details and settings\n- Switching schedule type on an existing pool requires confirmation (may affect existing picks)",
        "tests": "1. Create Regular Season pool -> verify only weeks 1-18 available for picks\n2. Create Playoffs-Only pool -> verify only playoff weeks are available\n3. Create Regular+Playoffs pool -> verify all weeks are available\n4. Load existing pool with no schedule type -> verify it defaults to Regular Season\n5. Switch schedule type on active pool -> verify confirmation prompt appears\n6. Verify recommendations respect schedule type when computing future value"
    },
    {
        "id": "33529ce5-833d-8137-b22e-c93283016f3c",
        "new_name": "Analytics (19.1): Incorporate Futures Data",
        "description": "Integrates NFL futures market data (Super Bowl odds, conference championship odds, win totals) into the SurvivorPulse analytics engine as additional signals for team strength evaluation. Futures prices reflect long-term market consensus on team quality and are a useful complement to weekly spreads for survivor pool decision-making.",
        "ac": "- Futures data is ingested from a defined data source on a defined schedule\n- Super Bowl odds and/or win totals are available per team\n- Futures data is incorporated into the recommendation engine as a configurable signal\n- Futures data is displayed alongside spread data in the team detail view\n- Data staleness is tracked and displayed (futures don't update daily)\n- Missing futures data for a team is handled gracefully",
        "tests": "1. Ingest futures data -> verify Super Bowl odds appear for all 32 teams\n2. Enable futures signal in engine -> verify recommendations shift compared to spread-only\n3. Check team detail drawer -> verify futures data is displayed\n4. Simulate missing futures for one team -> verify recommendation engine handles gracefully\n5. Verify futures data source and last-updated timestamp are accessible"
    },
    {
        "id": "33529ce5-833d-815b-8729-c63728f691e6",
        "new_name": "Analytics (19.2): Incorporate Polymarket Data",
        "description": "Integrates Polymarket prediction market data for NFL game outcomes into the SurvivorPulse analytics engine. Polymarket prices represent crowd wisdom on win probability and can complement or diverge from sportsbook spreads in informative ways. This adds a market-based signal alongside the existing spread-based probability calculations.",
        "ac": "- Polymarket win probability data is fetched for current-week NFL games via API\n- Data is refreshed on a defined schedule (at minimum daily during the week)\n- Polymarket probabilities are displayed in the team and game data views\n- Engine can optionally weight Polymarket data as a signal alongside spreads\n- Divergence between Polymarket and spread-implied probability is surfaced as an insight\n- API rate limits and error handling are implemented",
        "tests": "1. Fetch Polymarket data -> verify win probabilities appear for each game\n2. Compare Polymarket vs spread-implied probability -> verify divergence is calculated\n3. Enable Polymarket signal -> verify recommendations change vs spread-only mode\n4. Simulate Polymarket API timeout -> verify graceful fallback (show spread-only data)\n5. Verify refresh schedule runs and updates data within expected window"
    },

    # ─── BATCH 14 ──────────────────────────────────────────────────────────────
    {
        "id": "33529ce5-833d-8176-8952-d6260cc4b32e",
        "new_name": "Fix (20.2): Regular Season Bug for Entering Previous Week Picks",
        "description": "Fixes a bug that prevents users from correctly entering or editing picks for previous weeks during the regular season. This affects users who are setting up pools mid-season or correcting historical data. The fix should allow previous-week pick entry without corrupting current-week state.",
        "ac": "- Users can enter picks for any past week without errors\n- Previous-week pick entry does not overwrite or corrupt current-week picks\n- Saved previous-week picks are correctly reflected in analytics and standings\n- Fix is covered by a regression test that verifies previous-week entry\n- No regression to current-week pick submission behavior",
        "tests": "1. Enter pick for week 3 while in week 10 -> verify pick is saved correctly\n2. Verify current week picks are unchanged after previous-week edit\n3. Check analytics after previous-week entry -> verify standings recalculate correctly\n4. Run regression test for previous-week pick entry -> verify passes\n5. Submit current-week pick after editing previous week -> verify normal flow works"
    },
    {
        "id": "33529ce5-833d-8192-b800-e8838e12befd",
        "new_name": "Algorithm (22.1): Path-Aware Multi-Pick Selection Algorithm",
        "description": "Develops an algorithm that selects optimal team picks across multiple entries by accounting for future path dependencies -- specifically, which teams will still be available in future weeks given current pick commitments. A path-aware approach avoids locking out strong future options by over-picking popular teams early in the season.",
        "ac": "- Algorithm accepts current picks for all entries and remaining available teams per entry\n- Algorithm outputs an optimal pick slate for the current week that preserves future path diversity\n- Future path analysis looks ahead at least 3 weeks\n- Algorithm handles portfolios of 1-20 entries\n- Performance: calculation completes in under 5 seconds for 20-entry portfolios\n- Algorithm is documented with explanation of the path optimization logic\n- Unit tests cover portfolios with and without path constraints",
        "tests": "1. Run on 5-entry portfolio -> verify picks avoid exhausting high-value teams too early\n2. Run on single-entry portfolio -> verify behavior matches simpler algorithm\n3. Test with heavily constrained portfolio (most top teams already used) -> verify valid picks returned\n4. Run on 20-entry portfolio -> verify completes within 5 seconds\n5. Compare path-aware vs naive algorithm output -> verify path-aware produces demonstrably better future value"
    },
    {
        "id": "33529ce5-833d-81a6-8e48-c2f385fb11b7",
        "new_name": "Analytics (19.3): Improve Pick Analytics: Division, QB Matchups, Line Movement",
        "description": "Enhances the pick analytics feature with three additional analytical dimensions: divisional game context (teams often underperform against division rivals), QB matchup quality (a team's QB vs the opposing defense), and line movement (how the spread has shifted since opening). These signals give users richer context for evaluating recommendations.",
        "ac": "- Divisional game flag is displayed on all relevant matchups\n- Historical divisional game performance (win rate for favorites) is shown as context\n- QB matchup rating or indicator is displayed per game\n- Line movement (opening spread vs current spread) is shown with directional indicator\n- All three signals are available in the team detail drawer and game list view\n- Data sources for each signal are documented",
        "tests": "1. Identify divisional matchup in schedule -> verify divisional flag is shown\n2. Verify historical divisional win rate for favorites is displayed\n3. Check QB matchup indicator for a game with a notable mismatch -> verify indicator reflects the mismatch\n4. Verify line movement shows opening and current spread with direction arrow\n5. Open team detail drawer -> verify all three signals appear in context"
    },
    {
        "id": "33529ce5-833d-81be-9506-d49a4dea1544",
        "new_name": "Algorithm (22.2): Update Regular Season Algorithm for Week 18 Nuances",
        "description": "Updates the survivor pool recommendation algorithm to account for Week 18 NFL regular season nuances: teams with playoff positions clinched may rest starters, lines are often misleading, and historical upset rates differ significantly from earlier weeks. The algorithm should flag Week 18 games where rest/motivation factors create elevated upset risk.",
        "ac": "- Algorithm detects Week 18 and applies modified risk parameters\n- Teams with clinched playoff positions are flagged as potential rest candidates\n- Recommendation rationale for Week 18 picks explicitly references rest/motivation risk\n- Historical Week 18 upset rate data is used in probability adjustments\n- Users receive an in-app warning when making Week 18 picks about elevated volatility\n- Algorithm changes are documented and configurable",
        "tests": "1. Run recommendations for Week 18 -> verify risk parameters differ from Week 10\n2. Identify a team with clinched playoff position -> verify rest risk flag appears\n3. Check recommendation rationale for a Week 18 pick -> verify it mentions rest/motivation context\n4. Verify in-app Week 18 warning appears when accessing Week 18 picks\n5. Compare Week 18 probability adjustments against historical upset data"
    },
    {
        "id": "33529ce5-833d-81c9-86d0-d0b393e3fd15",
        "new_name": "Auth & Accounts (9.4): Implement Email Service: Registration, Sign-In, Forgot Password",
        "description": "Implements transactional email delivery for all core authentication flows using Postmark: account registration confirmation, magic link or password-based sign-in email, and forgot password reset flow. This is a prerequisite for reducing reliance on any third-party auth providers and ensuring a branded, reliable auth email experience.",
        "ac": "- Registration sends a confirmation email with a verification link\n- Email verification is required before account access is granted\n- Sign-in flow supports email-based magic link or password reset initiation\n- Forgot password sends a reset link with a short expiry (15-60 minutes)\n- Expired reset links return a clear error and prompt user to request a new link\n- All auth emails use Postmark with branded templates\n- Email delivery failures are logged and surfaced to the user",
        "tests": "1. Register new account -> verify confirmation email is received within 60 seconds\n2. Click verification link -> verify account is activated\n3. Request forgot password -> verify reset email received with working link\n4. Use expired reset link -> verify error shown and option to request new link\n5. Simulate Postmark delivery failure -> verify user sees error and can retry\n6. Verify all emails use branded templates (not generic Postmark defaults)"
    },

    # ─── BATCH 15 ──────────────────────────────────────────────────────────────
    {
        "id": "33529ce5-833d-81e4-8ff2-df3d5d026eaa",
        "new_name": "Analytics (19.4): Universal Composite and Overall Grading System",
        "description": "Builds a universal composite grading system that aggregates all available signals (spread-implied probability, futures, Polymarket, pick popularity, divisional context) into a single letter or numeric grade per team per week. This composite grade simplifies decision-making for users who don't want to evaluate each signal individually and gives the product a distinctive, opinionated output.",
        "ac": "- Each team receives a composite grade (A-F or 0-100) per week\n- Grade is calculated from a weighted combination of all available signals\n- Weighting methodology is documented and transparent to users\n- Grade is prominently displayed in recommendations and game list views\n- Grade explanation is available (what signals drove the grade)\n- Grade updates when underlying signal data changes\n- Grade calculation is unit-tested with known inputs",
        "tests": "1. View recommendations -> verify each team has a composite grade displayed\n2. Click grade -> verify explanation shows contributing signals and weights\n3. Update a signal (e.g., spread changes) -> verify grade recalculates\n4. Verify teams with strong consensus across signals receive highest grades\n5. Unit test grade calculation with 5 known input sets -> verify expected grades output"
    },
    {
        "id": "33529ce5-833d-8190-b455-f9844a66a5fb",
        "new_name": "DevOps (7.3): CI/CD Cleanup: signup-edge-cases test file",
        "description": "Cleans up the signup-edge-cases test file in the CI/CD pipeline that is causing test failures, flakiness, or pipeline noise. The file may have outdated tests, incorrect mocks, or tests that are no longer relevant. The goal is a clean, passing CI pipeline with reliable test coverage for signup edge cases.",
        "ac": "- signup-edge-cases test file passes consistently in CI without flakiness\n- Outdated or irrelevant tests are removed or updated\n- All remaining tests have clear descriptions and test meaningful behavior\n- CI pipeline run time is not increased by this cleanup\n- No previously tested behaviors are left uncovered after cleanup",
        "tests": "1. Run CI pipeline 3 times -> verify signup-edge-cases tests pass consistently\n2. Review remaining tests -> verify each tests a distinct, meaningful edge case\n3. Verify CI pipeline duration is same or shorter after cleanup\n4. Identify any removed tests -> verify their coverage is maintained elsewhere or was unnecessary"
    },
    {
        "id": "33529ce5-833d-8192-90d4-cc656f531106",
        "new_name": "Infrastructure (6.5): SubscriptionGuard Static-Link Cleanup",
        "description": "Removes or refactors hardcoded static links within the SubscriptionGuard component that have become stale or incorrect as the app's routing structure evolved. Static links in guards are a maintenance liability; this cleanup replaces them with dynamic route references or configuration-driven values.",
        "ac": "- All static links in SubscriptionGuard are replaced with route constants or dynamic lookups\n- No hardcoded URL strings remain in the SubscriptionGuard component\n- All existing guard redirect behaviors are preserved\n- TypeScript compilation succeeds with no errors after cleanup\n- All auth and subscription guard tests pass after cleanup",
        "tests": "1. Grep SubscriptionGuard for hardcoded URLs -> verify none remain\n2. Test subscription-gated route as non-subscriber -> verify redirect still works\n3. Test subscription-gated route as subscriber -> verify access granted\n4. Run TypeScript compiler -> verify zero errors\n5. Run full auth/subscription test suite -> verify all tests pass"
    },
    {
        "id": "33529ce5-833d-81ac-bd2c-c1dea8990441",
        "new_name": "Marketing (17.7): CA1 Reframe: Field Concentration Risk Narrative",
        "description": "Rewrites the marketing narrative around field concentration risk (CA1) to make it more compelling and accessible to a non-technical survivor pool audience. The current framing may be too technical or abstract. The reframed narrative should connect directly to the pain point: losing because you picked the same team as half the field.",
        "ac": "- New narrative is written and approved\n- Narrative uses plain language and avoids unexplained statistical terms\n- Narrative connects to a concrete survivor pool scenario most players have experienced\n- Updated copy is applied to relevant marketing materials (website, email, in-app onboarding)\n- Narrative is reviewed by at least one non-expert test reader before publishing",
        "tests": "1. Review new narrative -> verify no unexplained jargon\n2. Show narrative to 2 non-expert readers -> verify they understand the concept\n3. Check website and in-app copy -> verify updated narrative is live\n4. Compare old vs new narrative -> verify new version is more concrete and less abstract"
    },
    {
        "id": "33529ce5-833d-81d9-86d6-d2832296ca98",
        "new_name": "Marketing (17.8): Reddit Outreach for CMEA Prototype Validation",
        "description": "Executes a targeted Reddit outreach campaign in relevant survivor pool and fantasy football communities to gather feedback on the CMEA (coordinated multi-entry allocation) concept and validate that it resonates with the target audience. Posts should be educational and community-oriented, not promotional, to generate authentic engagement.",
        "ac": "- Target subreddits are identified and documented (e.g., r/sportsbook, r/fantasyfootball, r/nfl)\n- At least 2 posts are published in appropriate subreddits\n- Posts are educational/discussion-oriented, not direct product promotions\n- Engagement metrics are tracked (upvotes, comments, DMs)\n- Key feedback themes from comments are documented\n- No subreddit rules are violated; posts are not removed by mods",
        "tests": "1. Verify posts are live and not removed by moderators\n2. Check engagement after 48h -> verify at least 5 meaningful comments received\n3. Document key themes from community feedback\n4. Verify posts do not violate subreddit self-promotion rules\n5. Review DMs received -> verify any product interest leads are captured"
    },
    {
        "id": "33529ce5-833d-81e5-b6ed-d60e96248869",
        "new_name": "Marketing (17.9): Offseason Plan: Portfolio Positioning Update",
        "description": "Develops and executes the offseason marketing and positioning plan for SurvivorPulse, bridging the gap between the end of the current NFL season and the start of the 2026 season. The plan should maintain brand presence, grow the waitlist, and position the product for a strong September 2026 launch.",
        "ac": "- Offseason content calendar is defined (topics, formats, channels, cadence)\n- Positioning statement for 2026 launch is finalized and approved\n- At least one offseason content piece is published per month during the offseason\n- Waitlist growth target for the offseason is defined and tracked\n- Plan includes a pre-season launch sequence (June-August 2026)\n- Plan is documented and stored in Notion for reference",
        "tests": "1. Review offseason plan doc -> verify content calendar, positioning, and launch sequence are all defined\n2. Verify monthly content pieces are published on schedule\n3. Track waitlist growth monthly -> verify progress toward target\n4. Review pre-launch sequence -> verify it includes email, social, and product readiness milestones"
    },
]

# ─── EXECUTION ─────────────────────────────────────────────────────────────────
total = len(TASKS)
successful = 0
failed = []

for i, task in enumerate(TASKS):
    props = {}
    if "new_name" in task:
        props["Item"] = make_title(task["new_name"])
    props["Description"] = make_rich_text(task["description"])
    props["Acceptance Criteria"] = make_rich_text(task["ac"])
    props["Test Cases"] = make_rich_text(task["tests"])

    display_name = task.get("new_name", task.get("name", task["id"]))
    status, resp = patch_page(task["id"], props)

    if status == 200:
        print(f"[{i+1}/{total}] ✅  {display_name[:80]}")
        successful += 1
    elif status == 429:
        print(f"[{i+1}/{total}] ⏳  Rate limited, waiting 10s...")
        time.sleep(10)
        status2, resp2 = patch_page(task["id"], props)
        if status2 == 200:
            print(f"[{i+1}/{total}] ✅  {display_name[:80]} (retry OK)")
            successful += 1
        else:
            print(f"[{i+1}/{total}] ❌  {display_name[:80]} -> {status2}: {resp2[:200]}")
            failed.append((i+1, display_name, status2))
    else:
        print(f"[{i+1}/{total}] ❌  {display_name[:80]} -> {status}: {resp[:200]}")
        failed.append((i+1, display_name, status))

    # Rate limiting: small delay between each call, longer every 5
    if (i + 1) % 5 == 0:
        time.sleep(2)
    else:
        time.sleep(0.4)

print(f"\n{'='*60}")
print(f"Done. {successful}/{total} tasks updated successfully.")
if failed:
    print(f"\nFailed tasks ({len(failed)}):")
    for num, name, code in failed:
        print(f"  [{num}] {name[:60]} -> HTTP {code}")
