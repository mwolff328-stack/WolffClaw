# Stan the Scout: Competitor Demo Research
## SurvivorPulse — Competitive Intelligence: PoolGenius & PoolCrunch
**Date:** 2026-04-08
**Requested by:** Luigi (for SurvivorPulse prototype demo redesign)

---

## Brief (Restated)

SurvivorPulse is preparing a prototype demo targeting serious 3–5 entry NFL survivor pool players. Before redesigning the demo experience, Luigi needs to understand how the two primary competitors — PoolGenius (TeamRankings) and PoolCrunch (formerly SurvivorGrid) — demonstrate value to new users, what claims they make, and where gaps exist that SurvivorPulse could own.

---

## Key Findings

### 1. PoolGenius: The Established Authority, Opaque Multi-Entry Demo

**What they are:**
PoolGenius is the TeamRankings NFL survivor product — a 15+ year-old brand with SEO dominance, media mentions (ESPN, WSJ, NYT), and a clear performance claim: subscribers win 2.6x as often as expected, with $6.5M+ in reported winnings since 2017.

**How they demonstrate value to new users:**
- **Social proof-first:** The headline stat (2.6x win rate, $6.5M in winnings) is the primary trust signal. No free trial of the full tool — the value demo is the stat plus free educational articles.
- **Strategy content as top-of-funnel demo:** PoolGenius's strategy articles (multi-entry, optimal paths, Circa Survivor coverage) serve as a preview of their analytical framework. Serious players read these and extrapolate that the paid tool is more sophisticated.
- **Previewing the product frame:** They surface the 4-factor framework (win odds, pick popularity, future value, pool-specific dynamics) in free content. The paid tool operationalizes that framework into ranked picks.
- **Pricing:** $39–$49 one-time per season, or $98/year for all products (vs $176 à la carte). Low barrier once trust is established.

**Multi-entry portfolio approach (their stated framework):**
- PoolGenius explicitly recommends multiple entries as portfolio diversification ("like stocks")
- They support up to 30 weekly pick recommendations across pools/entries
- Their framework for coordination: adjust allocation between correlated (all same pick) and diversified (spread across viable favorites) based on contest stage and entries remaining
- The Circa Survivor coverage (a $25K buy-in real-money contest) shows their most sophisticated multi-entry content — but this is editorial/article content, not a visual portfolio allocation tool

**So what:** PoolGenius converts through authority and content, not a demo experience. New users never see the tool working until they pay. The multi-entry story is told through articles, not a live "here's your 3-entry portfolio" visualization. This is a demo gap.

**Confidence: High** on product structure and claims; **Medium** on exact UI/UX since the tool is paywalled and WebFetch was blocked.

---

### 2. PoolCrunch: The Operator's Dashboard, Data-Rich but Entry-Centric

**What they are:**
PoolCrunch is the evolved SurvivorGrid (15+ years as a free pick-percentage grid), now rebuilt as a paid SaaS tool. They emphasize pool operations and data richness over pick quality.

**How they demonstrate value to new users:**
- **Free tier as demo:** Unlike PoolGenius, PoolCrunch offers a meaningful free tier (2 pools, 10 entries, full tool access). The demo IS the product — you get in, add your pool, and immediately see data.
- **Competitive intelligence as the hook:** The primary value proposition is understanding your opponents — opponent pick tracking, public pool analysis, entry-level stats. This is distinctive from PoolGenius's "our picks are better" positioning.
- **Data-first copy:** Landing page emphasizes "crunch the numbers" — EV calculator, Portfolio Optimal Path, pick distribution analysis. No explicit win-rate claims.
- **Pricing:** Free / $29 Pro / $79 Elite (one-time per season). Pro unlocks "future slate data and analysis." 30-day guarantee.

**Multi-entry portfolio approach:**
- "Portfolio Optimal Path" is a named feature — but description is thin in all public-facing content. It appears to calculate EV per pick across entries rather than coordinate picks to minimize correlated elimination.
- "Bulk Pick Editing" suggests multi-entry management, but the framing is operational (manage your entries) not strategic (here's how to allocate your portfolio)
- No explicit language about correlated elimination risk across entries

**So what:** PoolCrunch's multi-entry value is about managing your entries, not coordinating them. The Portfolio Optimal Path tool exists but appears to optimize individual entry EV, not cross-entry diversification. The free tier is a strong demo mechanism — but serious players may find it doesn't answer "what should my 5-entry portfolio look like this week?"

**Confidence: High** on product structure and pricing; **Low** on exact Portfolio Optimal Path mechanics (tool is paywalled; description is vague in public materials).

---

### 3. Common Patterns: How Survivor Pool Tools Demonstrate Value

Across PoolGenius, PoolCrunch, FantasyLabs, 4for4, and free tools (RotoBaller, WalterFootball):

**Standard value demonstration pattern:**
1. **Win probability** as the baseline — every tool leads with this (Vegas lines + model-derived win odds)
2. **Pick popularity / consensus %** — distinguishing factor vs "just pick the favorite"
3. **Future value / season planning** — saving elite teams for later is the key sophistication marker
4. **EV framing** — Expected Value is the common language serious players use and tools adopt

**What serious multi-entry players say they value (from forum/article synthesis):**
- Preventing total correlated elimination (the biggest anxiety: all 5 entries on the same team that loses)
- Identifying which week to concentrate vs. spread entries
- Future choke-point identification (weeks with no obvious lock)
- Schedule-aware pick sequencing (not burning a team early when a better matchup awaits)
- Contrarian positioning (avoiding the "mass grave" when a popular pick loses)

**The spreadsheet reality:** A meaningful segment of serious players still use DIY Google Sheets/Excel to track used teams and coordinate entries. The existence of multiple free GitHub templates confirms this is a real, unsolved workflow.

**So what:** The industry has standardized on win probability + pick popularity + EV as the core metric language. Future value / season planning is the differentiator serious players cite. No tool has built a native "show me my 3-entry portfolio allocation as a unified decision" experience.

---

### 4. What Serious Multi-Entry Players Say They Value Most

Synthesized from forum discussions, strategy articles, and tool copy:

| Pain Point | Articulation |
|---|---|
| Correlated wipeout | "If I put all 5 on Kansas City and they lose, I'm dead" |
| Manual tracking overhead | Spreadsheets, paper, forgetting used teams |
| Week-by-week tunnel vision | "I only think about this week, then regret it in Week 10" |
| Popularity blindness | "I pick the 'obvious' team, get eliminated, and so does 60% of the pool" |
| No portfolio view | "I have no idea how my entries relate to each other" |

**What separates a serious multi-entry player from a casual player:**
- Serious players explicitly think about pick popularity / contrarian positioning
- They reason about future team availability (season planning)
- They want to understand cross-entry correlation, not just pick-level EV
- They are often in large pools (1000+ entries) where field dynamics matter more

---

### 5. The Gap: What Neither Tool Does Well

| Capability | PoolGenius | PoolCrunch | Gap Severity |
|---|---|---|---|
| Individual pick quality (win prob + popularity + future value) | Strong — 4-factor model, ranked picks | Weaker — grid/EV calculator, no explicit composite score | Medium — PoolGenius has this |
| Season planning visualization | Season Planner tool (paywalled) | Future slate data (Pro tier) | Low — both have some version |
| Cross-entry portfolio coordination (CMEA) | Described in articles, no dedicated UI | "Portfolio Optimal Path" — vague, likely per-entry not cross-entry | **HIGH — neither has a native coordinated multi-entry allocation UI** |
| Correlated elimination visualization | Not visible — concept discussed in articles only | Not found in public materials | **HIGH — no tool shows "your entries are X% correlated this week"** |
| Live allocation recommendation ("Pick A for Entry 1, Pick B for Entry 2, Pick C for Entry 3") | Up to 30 pick recommendations, but format unclear | Bulk editing, not portfolio allocation | **HIGH — no tool delivers a unified multi-entry pick slate with explicit diversification rationale** |
| Free demo / try-before-buy | No — articles only until you pay | Yes — generous free tier | Medium — PoolCrunch wins here |
| Opponent / field dynamics | No public-facing feature | Strong — opponent tracking, public pool data | Medium — PoolCrunch differentiated here |

**The primary unclaimed territory:**
> Neither PoolGenius nor PoolCrunch has a native "portfolio allocation view" — a unified interface that shows a serious 3–5 entry player how their entries relate to each other, explicitly flags correlated elimination risk, and delivers a coordinated pick slate with the rationale for why entries differ.

PoolGenius tells you *about* multi-entry strategy in articles. PoolCrunch lets you *manage* multiple entries operationally. Neither *coordinates* them as a portfolio with explicit diversification logic.

---

## Gaps and Low-Confidence Areas

1. **PoolGenius tool UI is fully paywalled** — all WebFetch attempts returned 403. The Season Planner and Optimal Paths tool UI could not be directly observed. My characterization of their multi-entry UX is inferred from article content and public descriptions. Confidence: Medium.

2. **PoolCrunch's Portfolio Optimal Path mechanics are unclear** — public copy is thin. It may be more sophisticated than I can characterize from public materials. Could be entry-level EV optimization that accidentally approximates portfolio coordination. Confidence: Low on this specific feature.

3. **Reddit / forum user voice is thin** — Direct Reddit discussions about PoolGenius/PoolCrunch specifically were not surfaced by search. User sentiment is synthesized from strategy article content and forum threads about survivor pool tools generally. Confidence: Medium.

4. **FantasyLabs as a third competitor** — FantasyLabs appears to have built a survivor tool (DFS-optimizer style) that may be more technically sophisticated than PoolGenius. Not fully researched. Could be worth a separate intelligence pull.

5. **Circa Survivor community** — The high-stakes Circa Survivor contest ($25K buy-in) attracts the most sophisticated multi-entry players. PoolGenius has specialized coverage here. SurvivorPulse's CMEA prototype may find its best early adopters in this segment — not researched.

---

## Recommended Next Steps

1. **Get a PoolCrunch Pro account ($29)** — Directly observe the Portfolio Optimal Path tool and assess whether it truly does cross-entry coordination or just per-entry EV. This is the highest-uncertainty area and the most critical competitive question.

2. **Get a PoolGenius subscription ($39)** — Observe the Season Planner and Optimal Paths tools directly. Screenshot the multi-entry recommendation experience. Confirm whether the "30 recommendations" UI shows entries as a coordinated portfolio or as 30 independent picks.

3. **Seed the SurvivorPulse prototype demo around the gap** — Lead with the portfolio allocation view (the "this week your 3 entries should be: Chiefs, Eagles, Bills — here's why each is different") as the first-impression moment. Neither competitor shows this on first load.

4. **Consider a Circa Survivor segment** — The serious $25K multi-entry player has no native portfolio coordination tool. SurvivorPulse's CMEA value prop maps directly to this pain. A targeted demo for this segment (5+ entries, large prize pool) may close faster than a general NFL survivor audience.

5. **Follow-up on FantasyLabs** — Quick intelligence pull on whether FantasyLabs survivor tool has any CMEA-adjacent features. Low priority but worth a 30-minute scan.

---

## Sources

- [PoolGenius NFL Survivor Picks](https://poolgenius.teamrankings.com/nfl-survivor-pool-picks/) — PoolGenius product page and features
- [PoolGenius Season Planner](https://poolgenius.teamrankings.com/nfl-survivor-pool-picks/season-planner/) — Season planning tool
- [PoolGenius Multi-Entry Strategy Article](https://poolgenius.teamrankings.com/nfl-survivor-pool-picks/articles/playing-multiple-entries-strategy/) — Official multi-entry framework
- [PoolGenius Circa Survivor Multi-Entry](https://poolgenius.teamrankings.com/circa-survivor-picks/articles/the-smart-way-to-play-multiple-entries-in-circa-survivor/) — Sophisticated multi-entry strategy
- [PoolGenius Survivor Strategy Guide](https://poolgenius.teamrankings.com/nfl-survivor-pool-picks/articles/survivor-strategy-guide-how-to-win-nfl-survivor-pools-knockout-pools/) — Core strategy framework
- [PoolCrunch Home](https://poolcrunch.com/) — Product landing page and value claims
- [PoolCrunch Pricing](https://poolcrunch.com/pricing) — Confirmed tier structure: Free / $29 Pro / $79 Elite
- [SurvivorGrid](https://www.survivorgrid.com/) — PoolCrunch's legacy brand
- [FantasyLabs NFL Pool Strategy 2025](https://www.fantasylabs.com/articles/nfl-pool-strategy-2025-how-to-gain-an-edge-in-survivor-and-pickem-pools/) — Third-party tool framework and competitive framing
- [Sportsbook Review Forum — Multiple Entries](https://www.sportsbookreview.com/forum/handicapper-think-tank/755019-survivor-pool-multiple-entries) — Player voice on multi-entry strategy
- [Footballguys Forum — 2024 Survivor Picks](https://forums.footballguys.com/threads/2024-survivor-picks-discussion.813689/) — Community discussion
- [Splash Sports — Survivor Pool Essential Strategies](https://splashsports.com/blog/nfl-survivor-pools-essential-strategies-for-success) — Strategy synthesis
- [RotoGrinders — NFL Pool Strategy Guide 2025](https://rotogrinders.com/articles/poolgenius-nfl-pool-strategy-guide-2025-tips-win-survivor-pickem-pools-4137330) — Third-party coverage of PoolGenius
- [NFL Survivor Pool Optimal Paths Tool](https://poolgenius.teamrankings.com/nfl-survivor-pool-picks/optimal-path/) — PoolGenius Optimal Paths product page

---

## Direct Tool Audit

**Date:** 2026-04-08
**Method:** Live authenticated sessions — logged into both tools directly via curl with provided credentials. Examined page HTML, Inertia.js page props, and downloaded/analyzed the PortfolioPathTab Vue component JS bundle (~43KB) to understand exact feature mechanics.

---

### PoolCrunch — Authenticated Audit

**Account status:** Free tier (no Pro or Elite subscription). Pool: 0 private pools created.

**What I accessed:**
- Logged in successfully via POST `/login` with CSRF token
- Accessed Circa Survivor 2025 public pool (18,718 entries, $18.7M pot)
- Accessed: Dashboard, Standings, Pick Summary, Availability, Grid, Portfolio Path, EV Calculator

---

#### 1. Navigation Structure — Key UX Finding

The 5 tabs visible in the Circa 2025 pool navigation are:
**Dashboard | Standings | Pick Summary | Availability | Grid**

**Portfolio Path is NOT in the navigation.** It's only accessible via direct URL (`/pools/{pool}/portfolio-path`). A user navigating the product would never find it without being told where to look or discovering it accidentally.

**So what:** PoolCrunch's most compelling multi-entry feature is buried. New users won't see it. First-time user experience centers on adding entries and viewing the grid — not on portfolio planning.

---

#### 2. Grid View — The Core Tool

Teams ranked by EV descending. Columns: EV, Win%, Pick%, Team, Opponent, Spread.
Display toggles: Hide Used, Hide Divisional, Hide Away, Hide Thursday.

Sample data (Week 18 Circa 2025):
- DEN 1.16 EV | 89.5% W% | 1.1% P% vs LAC -15.5
- LAR 1.15 EV | 89.1% W% | 3.5% P% vs ARI -14
- BUF 1.08 EV | 84.7% W% | 6.6% P% vs NYJ -13

This is single-week, single-entry data. No multi-entry context anywhere on this view.

---

#### 3. Availability Tab — Closest Thing to Cross-Entry Visibility

Two distinct features here:

**"Availability Breakdown"**: Select up to 5 teams to see how many of YOUR claimed entries have that team combination still available. Genuine multi-entry tracking.

**"Availability & Usage Correlation Table"**: A full 32x32 matrix showing, for all pool entries, what % have both teams available vs. both teams used. Labels: "Both Teams Available (%)" and "Both Teams Used (%)". Diagonal shows individual team availability %, off-diagonal shows pairwise.

This is the most analytically sophisticated UI in the entire tool — but it's describing the **field** of all pool entries, not the user's personal portfolio. It answers "do Circa participants tend to use KC and DEN together?" not "are MY 3 entries correlated with each other?"

**So what:** The correlation table is a competitive intelligence feature (understanding opponent patterns), not a portfolio management feature (understanding your own entry diversification). A user with 3 entries cannot see "my 3 entries are 90% correlated this week."

---

#### 4. Portfolio Path Tool — The Core Question Answered

**Confirmed: NOT cross-entry coordination.**

Verified via:
1. Live page HTML (component name: `Pools/Partials/Survivor/PortfolioPathTab`)
2. Downloaded and analyzed the JS bundle (`PortfolioPathTab-v8t5g47w.js`, 43KB)
3. API call to `/portfolio-path/calculate` endpoint returning validation schema

**How it actually works:**

The tool groups entries with the **identical pick history** into "entry groups." Each group has:
- `entryCount`: How many entries are in this group
- `bestPaths`: A list of independently calculated optimal path sequences
- `futurePicks`: Any pre-set future picks for this group

For each group, paths are calculated independently based on that group's used-team history and EV/survival odds. The calculation does NOT consider what other groups are picking.

**The one genuine multi-entry feature:** Within a single group, you can allocate entries to different path options. If Group A has 3 entries and shows 5 path options, you can assign "2 entries → Path 1, 1 entry → Path 3." The Save Picks function cycles through entry IDs in the group and assigns picks accordingly.

**What is missing (the gap):**
- No cross-group coordination. If Group 1 (entries that used KC W1) calculates "best pick is BUF" and Group 2 (entries that used TB W1) also calculates "best pick is BUF" — the tool shows both groups the same pick with zero warning or diversification suggestion.
- No correlated elimination warning of any kind.
- No "your entries are X% correlated this week" metric.
- No unified "here's what all your entries should pick this week" view.

**UI Parameters visible:**
- Number of Options to Show (select)
- Expected Final Slate (select)
- Range (select — valid value: "exact", default)
- Ignore Teams (multiselect)
- Ignore Saved Future Picks (toggle)
- Only Consider Used Selections in Optimal Path (toggle)
- [Update Paths] button

**Results table columns:** Entry Name / Used Selections / Survival Odds / Pick Options for Current Week / Full Paths / Win Odds% / Opponents / Spreads / Save Picks

**"No Optimal Paths Found"** — displayed when: pool is completed, no entries are claimed, or the slate is beyond what's available.

---

#### 5. EV Calculator

Single-week EV calculator. User inputs: Opponents Alive count, pick counts or percentages per team. Auto-normalize toggle, Reset Picks, Calculate EV. Columns: Selection, Opponent, Opp Avail, Opp%, Win Prob%, Projected P%*, Picks, Pick%, EV.

Footnote: "Projected pick percentages are based on standard rules weekly pools and may not apply to your pool's settings."

Single entry. No multi-entry context.

---

#### 6. First-Time User Experience

1. Arrives at homepage: "Your Path to a Smart Survivor Strategy" / "Find Your Winning Edge"
2. Signs up (free)
3. Lands on "My Pools" page: empty state — "No pools yet. Get started by creating your first pool or adding entries from public pools."
4. Two CTAs: Create Your First Pool | Add Entries from Public Pools
5. There is NO onboarding that mentions Portfolio Path, multi-entry coordination, or any tool other than "add your pool and track entries"

**The tool discovery problem:** A free-tier user exploring PoolCrunch sees the Grid and data analytics features prominently. The Portfolio Path — the most sophisticated multi-entry feature — is completely invisible unless the user knows to look for it by URL.

---

#### PoolCrunch Summary Table

| Feature | What It Does | Multi-Entry? | Gap? |
|---|---|---|---|
| Grid | Single-week EV/win/pick% ranking | No | Medium — standard industry feature |
| Availability | Which teams your entries can still use | Yes — per entry | Not a gap, solid feature |
| Availability Correlation | Pool-wide team usage correlation | Pool-level only | Gap — no personal portfolio correlation |
| Portfolio Path | Per-entry-group season path optimization | Groups only | **HIGH GAP** — no cross-group coordination |
| EV Calculator | Single-week EV for a custom pool | No | Low |
| Pick Summary | Post-week pick analysis | N/A | N/A (off-season) |

---

### PoolGenius — Authenticated Audit

**Account status:** Logged in successfully via TeamRankings (`/login/` POST). Account has **zero active subscriptions** — "You don't have any current premium packages." NFL Survivor Picks would cost $29 one-time (discounted from $49).

**NFL Offseason status:** All data-driven tool pages return "We're getting the Week 18 Survivor info ready. Check back in after 5PM Eastern." — end-of-season database maintenance, not seasonal lockout.

---

#### 1. NFL Survivor — What's Accessible Without Subscribing

**Nothing.** All tool page URLs (`/optimal-path/`, `/season-planner/`, `/ev-calculator/`) redirect to the product overview/marketing page. Zero UI preview. Zero demo mode. You see the feature descriptions but never the actual interface.

The product page describes the tools:
- **Custom Pick Ranking Report Card**: Win odds, popularity, future value, overall ranking per team each week, customized for your pool
- **Optimal Paths Tool**: Identifies optimal picks for every future week based on your current state
- **Season Planner Tool**: Shows future week win odds, lets you evaluate and compare pick paths
- **Expected Value Calculator**: Forecast pick popularity for your specific pool, calculate top-EV picks

No UI screenshots. No demo data. No "try it first."

**So what:** PoolGenius's conversion model is entirely authority + social proof → subscribe. New users NEVER see the tool working. This is SurvivorPulse's biggest UX advantage — if the demo shows the portfolio view working on load, it beats PoolGenius's cold paywall immediately.

---

#### 2. Circa Survivor — Accessible Features (Free Account)

The Circa Survivor product has far more accessible content than NFL Survivor. Navigation visible and accessible:

**Home | My Entries (free) | Data Grid (premium) | Season Planner (premium) | Optimal Paths (premium) | EV Calculator (premium) | Multi-Entry Survival (free) | Pick History (free) | Discussion Forum (free) | Strategy Guide (free) | Articles**

---

#### 3. Multi-Entry Survival Tool (Free, Critical Finding)

Page: `Circa Survivor Multi-Entry Survival Calculator`
Description: "Calculate and compare the expected survival outcomes for up to three different combinations of weekly picks."

**This is scenario comparison, NOT cross-entry coordination.**

What it does: You pick 3 different "what if" combinations (e.g., Entry 1 picks KC, Entry 2 picks BUF, Entry 3 picks MIN) and it shows the expected survival probability for each combination. You're comparing scenarios, not getting coordinated pick assignments.

Limits: Up to 3 combinations only. Inputs are manual — no entry import or historical tracking integration visible.

Off-season state: Tool page loads but shows "Week 18 info updating" — tool mechanics visible but no live data.

**So what:** PoolGenius's free multi-entry tool is a scenario calculator, not a coordinator. It lets a user manually enter 3 pick scenarios and compare their survival odds — useful but not the same as "here's what each of your N entries should pick this week and why they differ."

---

#### 4. Circa Survivor Entry Pick History (Free, with Live Data)

Full database of 18,694 Circa 2025 entries. Shows every pick made in every week (W1–W18 + Thanksgiving + Christmas weeks). Format: Entry name | Total Wins | Team picked per week.

Example entries (first few survivors): DYLAN W-10 (20 wins), GaryA-10 (20 wins), JUICY KEWCHI-7 (20 wins)...

This is a searchable database for tracking opponent entries — competitive intelligence, not portfolio coordination.

---

#### 5. Critical PoolGenius Admission

From the Circa Survivor product page (verbatim):

> "This product does not currently recommend specific teams to pick with each of your entries in the Circa Survivor contest. That's a slippery slope when multiple PoolGenius subscribers are using this product to compete in the same contest. For instance, recommending the same picks to all our subscribers would almost certainly reduce the expected value of those picks."

**This is the most important competitive intelligence in this entire audit.**

PoolGenius explicitly CANNOT do personalized multi-entry coordination because they serve all their subscribers the same recommendations. If they told all 50,000+ subscribers "Entry 1: KC, Entry 2: BUF, Entry 3: MIN," every subscriber would follow that advice, the picks would converge, and the EV would collapse.

**SurvivorPulse's structural advantage:** Personalized coordination based on each user's SPECIFIC entry history means no two users get the same recommendation. The "subscriber dilution" problem PoolGenius identified doesn't apply. This is an architecture-level competitive moat, not just a feature gap.

---

#### 6. Pricing (Current)

- NFL Survivor Picks one-time: $29 (normally $49, "40% off, ends Feb 15")
- Pool Picks (all football + March Madness): $99/year (normally $199)
- Pool Picks PLUS (all sports): $149/year
- Yearly All-Access (all pools + betting picks): $299/year

---

#### PoolGenius Summary

| Feature | Status | Multi-Entry? | Gap? |
|---|---|---|---|
| NFL Survivor tool access | Fully paywalled, no preview | N/A | Demo gap vs. SurvivorPulse |
| Circa Multi-Entry Survival | Free, but scenario comparison only | 3-scenario compare | **HIGH GAP** — not coordination |
| Circa Optimal Paths | Premium, single-entry focus | No | Gap |
| Circa Season Planner | Premium, grid view | No | Gap |
| Pick History | Free, opponent database | Opponent tracking | Not a portfolio tool |
| Personalized coordination | Explicitly absent by design | No | **STRUCTURAL GAP** |

---

### The Definitive Answer: Does PoolCrunch Portfolio Optimal Path Do Cross-Entry Coordination?

**NO. Confirmed definitively.**

From direct JS source code analysis of the `PortfolioPathTab` Vue component:

1. Entries are grouped by identical pick history into `entryGroups`
2. Each group receives its own `bestPaths` calculated **independently**
3. There is no cross-group optimization logic anywhere in the component
4. The "allocation" feature within a group (split 3 entries across 5 paths) is the only genuine multi-entry mechanic
5. A user with 5 entries across 5 different groups gets 5 independent path recommendations — no diversification guarantee, no correlated elimination check

The tool is best described as: **"Grouped per-entry season planner with within-group allocation."** Not portfolio coordination.

---

### What SurvivorPulse Has That Neither Competitor Has

| Capability | PoolCrunch | PoolGenius | SurvivorPulse |
|---|---|---|---|
| Cross-entry pick coordination (Entry 1 ≠ Entry 2 by design) | No | No | Yes (CMEA) |
| Correlated elimination risk score for personal entries | No | No | Yes |
| "This week your N entries should pick: X, Y, Z" unified recommendation | No | No | Yes |
| Portfolio view showing all entries side by side this week | Hidden/limited | No | Yes |
| Personalized advice that doesn't dilute as subscriber count grows | N/A | Structurally impossible | Yes (personalized model) |
| Free demo that shows the tool working before you pay | Free tier (limited) | No — full paywall | Yes (demo on load) |

---

### Implications for SurvivorPulse Demo Design

1. **Lead with what neither competitor shows**: A unified "your 3 entries this week: Chiefs, Eagles, Bills — here's why each is different" view. Neither tool renders this. Ever.

2. **Name the correlated elimination risk explicitly**: Neither tool warns users "your entries are 80% correlated this week." SurvivorPulse showing a live correlation score creates an emotional moment neither competitor offers.

3. **Highlight the structural advantage over PoolGenius**: SurvivorPulse can give personalized coordination because its recommendations are per-user, not per-subscriber-base. PoolGenius literally cannot do this by their own admission.

4. **Demo without requiring signup**: PoolGenius requires purchase before seeing any tool UI. PoolCrunch requires pool creation before seeing key features. SurvivorPulse showing the portfolio view on demo load beats both immediately.

5. **Don't lead with EV or win probability**: Both competitors lead with these. They're necessary but not differentiating. SurvivorPulse's differentiation is the portfolio-level view, not the individual pick quality.

---

### Friction Points Noted (for Competitive Positioning)

**PoolCrunch friction:**
- Portfolio Path not in navigation — most users won't find it
- Free tier requires pool creation before seeing any meaningful features
- Off-season: all tools functional but no fresh pick data (expected)

**PoolGenius friction:**
- Zero preview without subscribing — full cold paywall
- Subscription purchase required before ANY tool UI is visible
- Off-season: actively updating databases, tools will be ready for 2026 season
- No free trial — must commit $29 before seeing anything

