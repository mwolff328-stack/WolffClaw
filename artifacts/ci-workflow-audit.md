# CI Workflow Audit — SurvivorPulse

**Date:** 2026-04-09
**Workflows audited:**
- `pre-publish.yml` — Pre-Publish Gate
- `release-guardian.yml` — Release Guardian – Clean Install Proof

---

## 1. Step-by-Step Comparison

| # | Pre-Publish Gate | Release Guardian |
|---|---|---|
| Trigger | `push: main` | `push: main` + `workflow_dispatch` (optional SHA) |
| Timeout | 45 min | 30 min |
| **Setup** | | |
| S1 | Checkout | Checkout |
| S2 | _(n/a)_ | Checkout requested SHA *(workflow_dispatch only)* |
| S3 | Setup Node 22 | Setup Node 22.x |
| S4 | Clean install (`npm ci`) | Clean install (`npm ci`) |
| S5 | Install postgres client tools | Install postgres client tools |
| S6 | Verify Postgres ready | Verify Postgres healthy |
| S7 | _(n/a)_ | Confirm DB connectivity (`select 1`) |
| S8 | Push schema (`drizzle-kit push --force`) | Push schema (`drizzle-kit push --force`) |
| S9 | Seed NFL teams (full 32-team SQL block) | Seed NFL teams (full 32-team SQL block) |
| S10 | Generate `TEST_RUN_ID` | _(n/a)_ |
| **Test suites** | | |
| T1 | Stage 1: Unit tests (`npm run test:unit`) | Step A: Unit tests (`npx vitest run --config vitest.config.ts`) |
| T2 | Stage 2a: Integration core (`npm run test:integration:core`) | Step B: Integration core (`npx vitest run --config vitest.integration.core.config.ts`) |
| T3 | Stage 2b: Integration slow — full mode (`npm run test:integration:slow:full`) | Step C: Integration slow (`npx vitest run --config vitest.integration.slow.config.ts`) |
| T4 | Stage 2c: Start server (live `npm run dev` on port 5000) | _(n/a)_ |
| T5 | Stage 2c: HTTP integration tests (7 auth endpoint test files) | _(n/a)_ |
| T6 | Stage 2c: Stop server | _(n/a)_ |
| T7 | Stage 3: E2E tests (`npm run test:e2e:project`) | Step D: E2E tests (`npx vitest run --config vitest.e2e.config.ts`) |
| **Unique gates** | | |
| U1 | Stage 4a: Module boundary check (`npx tsx scripts/check-module-boundaries.ts`) | _(n/a)_ |
| U2 | Stage 4b: Test-data cleanup (`npm run test:cleanup`) | _(n/a)_ |
| U3 | Stage 4c: Verify no test pools remain (`npm run test:verify-clean`) | _(n/a)_ |
| U4 | _(n/a)_ | Step E: Tripwire — `canonicalSpreadBadgeGuardrail.tripwire.test.ts` |
| U5 | _(n/a)_ | Step F: Canonical Spread Contract — `canonicalSpreadContract.test.ts` |
| U6 | _(n/a)_ | Step G: CA1 Postmortem — `ca1/tests/phase5/ca1-postmortem.test.ts` |
| U7 | _(n/a)_ | Block committed `.skip` / `.only` (governance grep gate) |
| **Summary** | | |
| Z1 | Summary (`if: always()`) | Summary (`if: always()`) |

---

## 2. Exact Duplicates vs Unique Gates

### Exact or near-exact duplicates (shared infrastructure)

These steps are functionally identical — same commands, same service config, same SQL:

- Postgres 16 service definition (image, env, ports, health options) — **word-for-word identical**
- `npm ci` clean install
- Install postgres client tools (`sudo apt-get install -y postgresql-client`)
- Verify Postgres ready (same retry loop)
- `drizzle-kit push --force`
- Seed NFL teams (same 32-team SQL block — **exact duplicate**)
- `NODE_ENV: test`, `TZ: America/Los_Angeles`, `DATABASE_URL`, `POSTGRES_URL`, `TEST_DATABASE_URL`, `ALLOW_NONLOCAL_TEST_DB`, `REPLIT_DOMAINS`, `TEST_INTEGRATION_FAST: "0"`, `TEST_DISABLE_NETWORK: "1"`

### Same test suites, different invocation style

All four core test suites run in both workflows but Pre-Publish uses `npm run` script aliases while Release Guardian calls `npx vitest run --config` directly. They target the same vitest config files — behavior is equivalent.

| Suite | Pre-Publish invocation | Release Guardian invocation |
|---|---|---|
| Unit | `npm run test:unit` | `npx vitest run --config vitest.config.ts` |
| Integration core | `npm run test:integration:core` | `npx vitest run --config vitest.integration.core.config.ts` |
| Integration slow | `npm run test:integration:slow:full` | `npx vitest run --config vitest.integration.slow.config.ts` |
| E2E | `npm run test:e2e:project` | `npx vitest run --config vitest.e2e.config.ts` |

**Important env difference:** Pre-Publish sets `RUN_DB_REGRESSION_TESTS=1` and `RUN_SIGNUP_EDGE_CASES=1`, which unlock ~197 additional tests that are silently skipped in Release Guardian. The suites overlap in name but Pre-Publish runs a materially larger test corpus.

### Unique to Pre-Publish Gate

| Gate | What it does |
|---|---|
| `TEST_FAST_OPTIMIZER=1` env | Enables fast optimizer path |
| `RUN_DB_REGRESSION_TESTS=1` | Unlocks ~197 additional DB regression tests |
| `RUN_SIGNUP_EDGE_CASES=1` | Unlocks signup edge-case test group |
| `Generate TEST_RUN_ID` | Scopes test-data for targeted cleanup |
| Stage 2c (HTTP integration) | Starts live dev server, runs 7 auth endpoint test files against `localhost:5000` |
| Stage 4a: Module boundary check | Static analysis via `scripts/check-module-boundaries.ts` |
| Stage 4b: Test-data cleanup | Removes scoped test data by `TEST_RUN_ID` |
| Stage 4c: Verify no test pools remain | Asserts DB is clean after cleanup |

### Unique to Release Guardian

| Gate | What it does |
|---|---|
| `workflow_dispatch` trigger | Allows manual run against any arbitrary commit SHA |
| Checkout requested SHA | Conditionally checks out a non-HEAD commit |
| Confirm DB connectivity | Extra `select 1` sanity check before schema push |
| Step E: Tripwire test | `canonicalSpreadBadgeGuardrail.tripwire.test.ts` — likely a sentinel that fails if a specific invariant breaks |
| Step F: Canonical Spread Contract | `canonicalSpreadContract.test.ts` — contract test for canonical spread logic |
| Step G: CA1 Postmortem | `ca1/tests/phase5/ca1-postmortem.test.ts` — regression test from a past incident |
| Governance gate | Greps all test files for committed `.skip` / `.only` and blocks the run if found |

---

## 3. Consolidation Options

### Option A: Consolidate into one workflow

Merge everything into a single workflow with the `workflow_dispatch` trigger. All unique gates from both workflows run sequentially.

**Pros:**
- One file to maintain
- Single pass through shared infrastructure (one Postgres setup, one seed)
- Unified notification surface

**Cons:**
- Runtime would be ~55–65 min (Pre-Publish is already 45 min, adding Release Guardian's unique gates adds more)
- A failure in the governance grep gate or a tripwire blocks the entire run — even if ship-critical tests passed
- Harder to reason about: Pre-Publish is a "ship gate," Release Guardian is a "contract/governance gate" — mixing them obscures that distinction
- `workflow_dispatch` with a SHA input on a merged workflow is awkward: you'd be running HTTP integration tests and cleanup against an arbitrary SHA, which may have side effects

**Verdict:** Not recommended.

### Option B: Keep separate workflows, extract shared steps into a composite action

Create `.github/actions/ci-db-setup/action.yml` — a composite action that encapsulates:
- Install postgres client tools
- Verify Postgres ready
- Push schema
- Seed NFL teams

Both workflows call `uses: ./.github/actions/ci-db-setup` instead of repeating the 4 steps inline.

Additionally, standardize the test suite invocation style. Pre-Publish should switch from `npm run test:unit` aliases to `npx vitest run --config` (or vice versa) to make both workflows read consistently.

**Pros:**
- 32-team SQL seed block is the biggest duplication — extracted once, updated in one place
- Separate workflows retain distinct responsibilities and failure semantics
- Release Guardian retains `workflow_dispatch` cleanly
- Each workflow has its own timeout tuned to actual runtime
- Adding a new test environment var (e.g., new regression gate) only requires adding it to the relevant workflow

**Cons:**
- Two workflows still exist — two places to add notification steps, etc.
- Composite action is a new concept to maintain

**Verdict:** Recommended (see section 5).

### Option C: Keep fully separate, no refactor, add notification steps only

Minimal intervention — leave both workflows as-is, just add notification steps.

**Pros:** Zero risk of breaking existing CI behavior
**Cons:** 32-team seed block and DB setup steps remain duplicated in two places; next time schema setup changes you touch two files

**Verdict:** Acceptable short-term if resources are constrained. Defer the composite action extraction to a later sprint.

---

## 4. Tradeoffs Summary

| Dimension | Option A (Consolidate) | Option B (Composite action) | Option C (Status quo) |
|---|---|---|---|
| Runtime | ~60 min combined | Unchanged (45 + 30 min, parallel) | Unchanged |
| Failure isolation | Poor — one failure blocks all gates | Good — each workflow fails independently | Good |
| `workflow_dispatch` on arbitrary SHA | Awkward | Clean (Release Guardian keeps it) | Clean |
| Duplication | Eliminated | Seed + DB setup extracted | Full duplication |
| Maintainability | One file, complex conditionals | Two files, DRY infrastructure | Two files, WET |
| Risk | High — requires careful merge | Low — additive composite action | None |

---

## 5. Recommendation

**Keep both workflows. Extract shared DB infrastructure into a composite action. Standardize test invocation style.**

Rationale:

The two workflows serve different purposes and should fail independently. Pre-Publish Gate is the ship gate — if it fails, nothing ships. Release Guardian is the contract/governance gate — it validates invariants and coding standards. Conflating them into one workflow makes both harder to reason about and increases the blast radius of any single failure.

The concrete actions:

1. **Create `.github/actions/ci-db-setup/action.yml`** — composite action with four steps: install postgres client, verify Postgres healthy, push schema, seed NFL teams. Both workflows replace their 4 duplicate steps with one `uses` call.

2. **Standardize test invocation** — both workflows should use `npx vitest run --config <file>` directly instead of mixing `npm run` aliases and direct vitest calls. This makes the workflows self-documenting (the config file name is visible) and removes the indirection through `package.json` scripts.

3. **Add `TEST_FAST_OPTIMIZER`** to Release Guardian if it is relevant to the test harness (currently missing).

4. **Add notification steps** to both workflows (see `ci-notification-spec.md`).

The `workflow_dispatch` SHA input stays in Release Guardian only — it is not needed in Pre-Publish, and running HTTP integration tests + cleanup against an arbitrary historical SHA is not a safe pattern.

---

*Authored by Rita the Relay for SurvivorPulse CI pipeline review.*
