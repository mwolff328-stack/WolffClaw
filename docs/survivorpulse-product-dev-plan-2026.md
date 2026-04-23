# SurvivorPulse Product Development Plan: 2026 Season Launch

**Version:** 1.0
**Date:** April 23, 2026
**Owner:** Luigi (orchestrator) / Pam (product direction) / Ann (requirements) / Felix (build)
**Companion document:** `docs/survivorpulse-sales-marketing-plan-2026.md`
**Status:** Draft for founder review

---

## Executive summary

This plan defines what SurvivorPulse V1 ships with by September 4, 2026 (NFL Week 1), organized into milestones that align with the marketing plan's phases. The goal: every marketing claim is backed by a shipped capability. Nothing gets promised publicly that isn't production-ready.

---

## 1. Current product state (as of April 23, 2026)

### What's built and working

**Main platform (survivorpulse.com):**
- Full-stack app: React 18 + Vite + Tailwind/shadcn frontend, Node/Express + TypeScript backend, Drizzle ORM on Neon Postgres
- Recommendation engine: composite 0-100 score blending win probability (ESPN FPI), betting spreads, pick popularity (Yahoo), contrarian value, future option value
- Pool Dynamics Engine: field survival baseline, chalk risk, leverage, expected equity, pool leverage intensity
- Portfolio Diversification Mode: coordinates picks across multiple entries to minimize correlated elimination risk
- Playoff Survivor Engine: multi-pick, percentile grading, portfolio diversification mode
- CMEA analytics unification (shipped March 24, 2026)
- Custom email/password auth with sessions, CSRF, rate limiting
- Stripe subscriptions with founding member cap (50)
- Postmark transactional email
- Elimination detection and tracking
- Admin dashboard
- 2,400+ unit tests, 180+ integration tests
- Hosted on Replit

**Backtesting prototype (separate app, survivorpulse-backtester-prototype.replit.app):**
- Standalone React + Vite + TypeScript app
- 5 seasons of historical data (2021-2025) loaded into production DB
- 7 strategy types, configurable weights, advanced modes (Coordinated Diversification, Adaptive Blend, Scarcity-Aware)
- Per-entry strategy assignment, 1-50 entries, buyback toggle
- "Find Best Strategy" optimization (27+ strategies)
- Performance Summary visuals (delta gauges, survival timeline, entry survival heatmap)
- Access gate (SURVIVOR2026) with name/email capture
- 17-step interactive tutorial
- Feedback system (5 progressive questions, Notion proxy)
- 306 tests passing
- Live and deployed

### What's partially built / in progress

| Item | Status | Notion ID |
|---|---|---|
| CMEA Prototype Redesign (3 Demo Moments) | In Progress (Moments 1-3 Done, parent still open) | SPP-53 |
| CMEA Prototype Frontend | In Progress | SPP-1 |
| CI/CD Cleanup: signup-edge-cases test file | In Progress | SPP-2 |

### Key gaps for V1 launch

Based on the Notion Product Backlog (V1 Pre-Launch items), these are the critical capabilities not yet shipped:

**Launch-blocking (High Priority, V1 Pre-Launch):**

| ID | Item | Category | Why it matters |
|---|---|---|---|
| SPP-7 | Refactor NFL Regular Season Pools for 2026 | Core Engine | Cannot run 2026 season without this |
| SPP-8 | Pool Schedule Types: Regular, Regular+Playoffs, Playoffs-Only | Pool Mgmt | Core product flexibility for different pool formats |
| SPP-11 | Fix: Regular Season Bug for Entering Previous Week Picks | Core Engine | Data integrity bug |
| SPP-12 | Path-Aware Multi-Pick Selection Algorithm | Core Engine | Core CMEA capability - ensures pick allocation considers full-season path |
| SPP-15 | Implement Email Service: Registration, Sign-In, Forgot Password | Auth & Accounts | Cannot onboard users without proper email flows |
| SPP-16 | Universal Composite and Overall Grading System | Analytics | Core value prop - unified scoring that users see |
| SPP-58 | Revamp Public Website | Marketing/Content | The storefront for all marketing traffic |

**Important but not launch-blocking (Medium Priority, V1 Pre-Launch):**

| ID | Item | Category | Why it matters |
|---|---|---|---|
| SPP-13 | Improve Pick Analytics: Division, QB Matchups, Line Movement | Analytics | Depth of analysis for serious users |
| SPP-14 | Update Regular Season Algorithm for Week 18 Nuances | Core Engine | Edge case handling |
| SPP-23 | Lock Edit Pool After Season Ends | Pool Mgmt | Data integrity |
| SPP-25 | Add Team Detail Drawer to Entry Analytics | UX/Design | Better user experience |
| SPP-26 | Implement Unsaved Changes Alert | UX/Design | UX polish |
| SPP-49/37 | Add Google Analytics | Infrastructure | Track marketing effectiveness |

**Nice-to-have (Low Priority, V1 Pre-Launch):**

| ID | Item | Notes |
|---|---|---|
| SPP-51 | Rename PlayoffCandidate Interface to SurvivorCandidate | Tech debt |
| SPP-39/38 | Admin: Manual Spread Update | Admin tooling |
| SPP-42/35 | Test Email: Filter-Friendly Subject Lines | DevOps |
| SPP-43/31 | Disable NFL Spread Refresh Scheduler Post-Playoffs | DevOps |
| SPP-3 | SubscriptionGuard Static-Link Cleanup | Tech debt |
| SPP-18 | Update Homepage Screenshots | After website revamp |

### Content/marketing items in product backlog

| ID | Item | Status |
|---|---|---|
| SPP-4 | CA1 Reframe: Field Concentration Risk Narrative | On Hold |
| SPP-5 | Reddit Outreach for CMEA Prototype Validation | Backlog |
| SPP-6 | Offseason Plan: Portfolio Positioning Update | Backlog |
| SPP-57 | Editorial Pass: Rationale Copy | Backlog |
| SPP-58 | Revamp Public Website | Backlog |

---

## 2. V1 feature scope (what ships by September 4)

### Tier 1: Must-ship (launch blockers)

These must be production-ready before any paying user touches the product.

| Feature | Owner | Est. Size | Ship by |
|---|---|---|---|
| Refactor NFL Regular Season Pools for 2026 (SPP-7) | Felix | L | June 15 |
| Pool Schedule Types (SPP-8) | Ann (spec) + Felix (build) | L | June 30 |
| Fix: Previous Week Picks Bug (SPP-11) | Felix | S | May 15 |
| Path-Aware Multi-Pick Selection (SPP-12) | Ann (spec) + Felix (build) | XL | July 15 |
| Email Service: Registration, Sign-In, Forgot Password (SPP-15) | Ann (spec) + Felix (build) | L | June 15 |
| Universal Composite and Overall Grading System (SPP-16) | Ann (spec) + Felix (build) | L | July 15 |
| Revamp Public Website (SPP-58) | Paige (strategy) + Sky (copy) + Deb (design) + Felix (build) | L | June 30 |
| Google Analytics (SPP-49) | Felix | S | May 31 |
| Editorial Pass: Rationale Copy (SPP-57) | Sky | M | June 15 |

### Tier 2: Should-ship (significant value, not blocking)

| Feature | Owner | Est. Size | Ship by |
|---|---|---|---|
| Improve Pick Analytics (SPP-13) | Ann (spec) + Felix (build) | M | August 1 |
| Week 18 Algorithm Update (SPP-14) | Felix | M | August 15 |
| Lock Edit Pool After Season (SPP-23) | Felix | S | August 1 |
| Team Detail Drawer (SPP-25) | Deb (design) + Felix (build) | M | August 1 |
| Unsaved Changes Alert (SPP-26) | Felix | S | July 15 |

### Tier 3: Deferred to post-launch

Everything else in the backlog marked "Post-Launch" stays post-launch. Additionally, these V1 Pre-Launch items are deferred:
- SPP-51 (rename interface) - cosmetic
- SPP-39/38 (manual spread admin) - admin only
- SPP-42/35 (test email subjects) - minor
- SPP-43/31 (scheduler cleanup) - offseason only
- SPP-3 (subscription guard cleanup) - tech debt

### New items needed (not yet in backlog)

| Feature | Why | Owner | Est. Size | Ship by |
|---|---|---|---|---|
| Referral tracking system | Marketing plan requires referral links, attribution, reward fulfillment | Ann (spec) + Felix (build) + Rita (automation) | L | July 15 |
| Waitlist/email capture on landing page | Foundation for email marketing | Paige + Felix | M | May 15 |
| Founding member launch flow (Stripe) | Enable $49 founding tier with 50-slot cap | Felix | M | June 30 |
| Onboarding email sequence hooks | Trigger welcome + drip emails on signup events | Rita + Felix | M | July 1 |
| 2026 season data pipeline readiness | Odds API, Yahoo pick data, ESPN FPI ingestion for 2026 | Felix | M | August 15 |

---

## 3. Development timeline aligned to marketing phases

### Phase 1: Foundation (April 23 - May 31)

**Marketing needs from product:** Landing page with email capture. Backtesting data for content. CA1 asset.

| Week | Dev milestone | Enables marketing... |
|---|---|---|
| Apr 23-May 4 | Fix Previous Week Picks Bug (SPP-11). Deploy waitlist/email capture. Set up Google Analytics. | Landing page goes live. Conversion tracking active. |
| May 5-18 | Begin 2026 Season Refactor (SPP-7). Begin Email Service (SPP-15). Editorial pass on rationale copy starts. | Backtesting content can reference "coming 2026 season support." |
| May 19-31 | Continue SPP-7, SPP-15. GA live and tracking. | Phase 1 metrics visible in analytics. |

**What marketing CAN say in Phase 1:**
- All backward-looking claims (backtesting data, chalk collapse analysis, portfolio theory)
- "Coming for the 2026 season"
- "Join the waitlist"
- Everything about the backtesting prototype (it's live and working)

**What marketing CANNOT say in Phase 1:**
- "Manage your 2026 entries now" (2026 season not supported yet)
- "Sign up and start using it" (email service not ready)
- Specific feature claims about features not yet shipped

### Phase 2: Authority Building (June 1 - June 30)

**Marketing needs from product:** Public website revamp. Email flows working. Product demo-able for content.

| Week | Dev milestone | Enables marketing... |
|---|---|---|
| Jun 1-15 | Ship 2026 Season Refactor (SPP-7). Ship Email Service (SPP-15). Ship rationale copy editorial pass (SPP-57). Begin Pool Schedule Types (SPP-8). Begin Path-Aware Multi-Pick (SPP-12). | "2026 season ready" messaging. Sign-up flows work. Demo copy is polished. |
| Jun 16-30 | Ship Public Website Revamp (SPP-58). Ship Pool Schedule Types (SPP-8). Ship Founding Member Launch Flow. Begin Universal Composite (SPP-16). Begin referral tracking. | Marketing has a credible public website to drive traffic to. Founding member signup possible. |

**What marketing CAN say in Phase 2 (cumulative):**
- Everything from Phase 1
- "2026 season ready" (after SPP-7 ships)
- "Sign up now" (after SPP-15 ships)
- "Multiple pool format support" (after SPP-8 ships)
- Product demo content using polished rationale copy
- CMEA deep dive with real product screenshots

**What marketing CANNOT say in Phase 2:**
- Claims about path-aware optimization (SPP-12 still in progress)
- Claims about the universal grading system (SPP-16 still in progress)

### Phase 3: Pre-Season Push (July 1 - August 15)

**Marketing needs from product:** Full feature set marketable. Product stable for founding members. Referral system live.

| Week | Dev milestone | Enables marketing... |
|---|---|---|
| Jul 1-15 | Ship Path-Aware Multi-Pick (SPP-12). Ship Universal Composite (SPP-16). Ship Referral Tracking. Ship Onboarding Email Hooks. Ship Unsaved Changes Alert (SPP-26). | Full CMEA capability marketable. Referral program live. Onboarding automated. |
| Jul 16-Aug 1 | Ship Pick Analytics Improvements (SPP-13). Ship Team Detail Drawer (SPP-25). Ship Lock Edit Pool (SPP-23). | Richer product demo content. UX polished for paying users. |
| Aug 1-15 | Ship Week 18 Algorithm Update (SPP-14). Ship 2026 Data Pipeline. QA pass on all Tier 1 and Tier 2 features. | Product is fully ready for the season. All marketing claims validated. |

**What marketing CAN say in Phase 3 (cumulative):**
- Everything from Phase 1-2
- "Full path-aware portfolio allocation" (after SPP-12 ships)
- "Universal grading across all picks" (after SPP-16 ships)
- "Refer a friend" program (after referral system ships)
- Full product demo content with all V1 features visible

### Phase 4: Launch Window (August 16 - September 4)

**Marketing needs from product:** Product is live, stable, and handling real users. Zero critical bugs.

| Week | Dev milestone | Enables marketing... |
|---|---|---|
| Aug 16-Sep 4 | Bug fixes only. Performance monitoring. User support. 2026 season data flowing. | Full launch messaging with confidence. All claims backed by production product. |

**Freeze policy:** No new features after August 15. Only bug fixes and stability improvements. Marketing can make any claim about shipped features.

---

## 4. Product-marketing alignment matrix

This is the single source of truth for what marketing can claim and when.

| Marketing claim | Required feature(s) | Ship date | Marketable from |
|---|---|---|---|
| "Portfolio risk management for survivor pools" | Existing CMEA engine | Shipped | Now |
| "Backtested across 5 NFL seasons" | Backtesting prototype | Shipped | Now |
| "Coordinates picks across multiple entries" | Portfolio Diversification Mode | Shipped | Now |
| "Identifies correlated elimination risk" | Correlated Elimination Risk Panel (SPP-55) | Shipped | Now |
| "2026 season ready" | 2026 Season Refactor (SPP-7) | June 15 | June 15 |
| "Sign up and create your account" | Email Service (SPP-15) | June 15 | June 15 |
| "Supports regular season, playoffs, and combined pools" | Pool Schedule Types (SPP-8) | June 30 | July 1 |
| "Path-aware pick allocation across your full season" | Path-Aware Multi-Pick (SPP-12) | July 15 | July 15 |
| "Universal grading system for every pick decision" | Universal Composite (SPP-16) | July 15 | July 15 |
| "Refer a friend and earn rewards" | Referral Tracking System | July 15 | July 15 |
| "Deep pick analytics: division matchups, line movement" | Pick Analytics Improvements (SPP-13) | August 1 | August 1 |
| "Full 2026 season launch" | All Tier 1 + data pipeline | August 15 | August 16 |

---

## 5. Development team allocation

| Agent | Focus areas | Phase |
|---|---|---|
| **Pam** | V1 scope decisions, roadmap sequencing, feature prioritization | All phases (advisory) |
| **Ann** | Detailed requirements for SPP-8, SPP-12, SPP-16, referral system | Phase 1-2 (requirements ahead of build) |
| **Felix** | All build work. Primary focus: SPP-7, SPP-11, SPP-15, SPP-8, SPP-12, SPP-16 | All phases |
| **Deb** | Website revamp design, Team Detail Drawer, UX polish | Phase 1-2 (design), Phase 3 (polish) |
| **Vlad** | QA pass on all Tier 1 and Tier 2 features before marketing claims go live | Phase 2-3 (validation) |
| **Rita** | Referral automation, onboarding email hooks, data pipeline automation | Phase 2-3 |

**Constraint:** Felix is the bottleneck. Work must be sequenced to avoid context-switching. Ann delivers requirements 2+ weeks ahead of Felix's build window.

---

## 6. Risk register

| Risk | Impact | Mitigation |
|---|---|---|
| SPP-12 (Path-Aware Multi-Pick) takes longer than estimated | High - core differentiator delayed | Ann front-loads spec. Felix starts June 1. If behind by July 1, scope down to 80% solution. |
| SPP-7 (2026 Refactor) reveals unexpected complexity | High - cascading delay to everything | Start immediately. Timebox to 3 weeks. |
| Website revamp blocks on design iteration | Medium - delays all inbound marketing | Paige delivers wireframes by May 15. Deb delivers design by June 1. Felix builds June 1-30. |
| Email service integration with Postmark is more complex than expected | Medium - can't onboard users | Felix starts by May 5. Fallback: simplified flow first, polish later. |
| Data pipeline for 2026 season not ready by August 15 | Critical - product literally doesn't work | Felix confirms Odds API and Yahoo data contracts by July 1. Test ingestion by July 15. |

---

## 7. Governance

- **Feature freeze:** August 15. No new features after this date.
- **QA gate:** Vlad validates all Tier 1 features before founding member launch (Phase 3). All Tier 2 features validated before Week 1.
- **Marketing-product sync:** Luigi reviews product milestone completion bi-weekly and updates the alignment matrix. Marketing tasks that depend on unshipped features remain blocked.
- **Scope changes:** Any change to V1 scope requires Pam's recommendation and founder approval.

---

*This plan is a living document. Updated bi-weekly alongside the marketing plan.*
