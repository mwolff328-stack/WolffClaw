#!/usr/bin/env python3
"""
Stan the Scout: 2025 NFL Survivor Pool Pick Strategy Simulation

Simulates 4 pick strategies across the full 2025 NFL season for a 5-entry pool.
Uses actual game outcomes and Yahoo pick popularity data from the SurvivorPulse API.

Strategies:
1. Pure Win Probability - pick highest winProbability each week
2. Leverage Score - pick highest winProbability / pickShare ratio
3. Survival Equity - maximize expected survival edge over the field
4. Future Value Preservation - penalize using high-value future teams early
"""

import urllib.request
import json
import sys
from collections import defaultdict

BASE_URL = "https://survivorpulse.com"
POOL_ID = "04e2471b-6498-4a59-8a95-c0dc50221457"
SEASON = 2025
TOTAL_WEEKS = 18
NUM_ENTRIES = 5


def fetch_json(url, timeout=20):
    """Fetch JSON from URL with timeout."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  WARN: Failed to fetch {url}: {e}", file=sys.stderr)
        return None


def fetch_games(week):
    """Fetch game data for a specific week."""
    url = f"{BASE_URL}/api/games?season={SEASON}&scheduleType=regular&week={week}"
    return fetch_json(url)


def fetch_dynamics(week):
    """Fetch team dynamics (pick share, win prob) for a specific week."""
    url = f"{BASE_URL}/api/pools/{POOL_ID}/dynamics/comprehensive?week={week}&season={SEASON}&scheduleType=regular"
    return fetch_json(url)


def build_week_data(games, dynamics):
    """
    Combine games + dynamics into a list of team dicts for one week.
    Each team has: teamId, winProbability, pickShare, opponent, spread,
    homeScore, awayScore, homeTeam, awayTeam, completed, outcome.
    """
    if not games or not dynamics:
        return []

    # Build pickShare lookup from dynamics
    pick_shares = {}
    for t in dynamics.get("teamDynamics", []):
        pick_shares[t["teamId"]] = t.get("pickShare", 0)

    teams = []
    for g in games:
        hs = g.get("homeScore")
        as_ = g.get("awayScore")
        completed = g.get("completed", False)
        hwp = float(g["homeWinProbability"]) if g.get("homeWinProbability") else 0
        awp = float(g["awayWinProbability"]) if g.get("awayWinProbability") else 0
        home_spread = float(g["homeSpread"]) if g.get("homeSpread") else None

        # Determine outcomes (ties = loss in survivor)
        home_outcome = None
        away_outcome = None
        if completed and hs is not None and as_ is not None:
            home_outcome = "Win" if hs > as_ else "Loss"
            away_outcome = "Win" if as_ > hs else "Loss"

        home_id = g["homeTeamId"]
        away_id = g["awayTeamId"]

        teams.append({
            "teamId": home_id,
            "winProbability": hwp,
            "pickShare": pick_shares.get(home_id, 0),
            "opponent": away_id,
            "spread": home_spread,
            "homeScore": hs,
            "awayScore": as_,
            "homeTeam": home_id,
            "awayTeam": away_id,
            "completed": completed,
            "outcome": home_outcome,
        })
        teams.append({
            "teamId": away_id,
            "winProbability": awp,
            "pickShare": pick_shares.get(away_id, 0),
            "opponent": home_id,
            "spread": -home_spread if home_spread is not None else None,
            "homeScore": hs,
            "awayScore": as_,
            "homeTeam": home_id,
            "awayTeam": away_id,
            "completed": completed,
            "outcome": away_outcome,
        })
    return teams


# ─── Scoring Functions ──────────────────────────────────────────────────────

def score_pure_win_prob(team, _all_teams, _future_data):
    """Strategy 1: Pure win probability."""
    return team["winProbability"]


def score_leverage(team, _all_teams, _future_data):
    """
    Strategy 2: Leverage Score.
    winProbability / (pickShare / 100).
    Higher = more value per unit of field exposure.
    Teams with 0 pickShare get a small floor to avoid division by zero.
    """
    ps = max(team["pickShare"], 0.1)  # floor at 0.1%
    return team["winProbability"] / (ps / 100)


def score_survival_equity(team, all_teams, _future_data):
    """
    Strategy 3: Survival Equity.
    Measures expected advantage over the field.
    
    When I pick team T:
    - If T wins (prob = wp): I survive. My edge = fraction of field eliminated
      by OTHER teams losing. Approximated by: sum of pickShare for all non-T teams
      that are expected to lose = sum(pickShare * (1 - wp)) for teams != T.
      But my real edge is: I'm alive AND some fraction of the field died on chalk.
    
    Simplified: winProb * (1 - pickShare/100) gives "unique survival" - the probability
    I survive AND I'm not correlated with the herd. This naturally penalizes chalk picks.
    
    More precisely:
    survivalEquity = wp * (1 - ps/100) + (1 - chalkWp) * (ps_chalk/100) * wp
    
    The second term captures the bonus when the most popular pick loses.
    Simplified to: wp * (1 - ps/100 + chalkFailBonus)
    """
    wp = team["winProbability"]
    ps = team["pickShare"]
    
    # Find the chalk (most popular) team
    chalk = max(all_teams, key=lambda t: t["pickShare"])
    chalk_ps = chalk["pickShare"]
    chalk_wp = chalk["winProbability"]
    
    # Base: survive uniquely
    unique_survival = wp * (1 - ps / 100)
    
    # Bonus: when chalk fails, field shrinks massively, I gain if I'm alive
    # Only applies if I'm NOT the chalk pick
    chalk_fail_bonus = 0
    if team["teamId"] != chalk["teamId"]:
        chalk_fail_bonus = wp * (1 - chalk_wp) * (chalk_ps / 100)
    
    return unique_survival + chalk_fail_bonus


def score_future_value(team, all_teams, future_data):
    """
    Strategy 4: Future Value Preservation.
    
    Penalizes using a team now if that team has high value in future weeks.
    Value now = leverage score this week.
    Cost = max leverage score this team would have in any future week.
    
    Net score = current_leverage - discount * max_future_leverage
    
    This encourages "save premium teams for when they're more valuable."
    """
    ps = max(team["pickShare"], 0.1)
    current_leverage = team["winProbability"] / (ps / 100)
    
    # Look up future value for this team
    future_max = 0
    team_id = team["teamId"]
    for fw_teams in future_data.values():
        for ft in fw_teams:
            if ft["teamId"] == team_id:
                fps = max(ft["pickShare"], 0.1)
                future_lev = ft["winProbability"] / (fps / 100)
                future_max = max(future_max, future_lev)
    
    # Discount factor: how much to penalize burning future value
    # 0.3 means "I'll accept 30% less now to save this team for later"
    discount = 0.3
    return current_leverage - discount * future_max


# ─── Simulation ─────────────────────────────────────────────────────────────

def simulate_strategy(strategy_name, score_fn, all_week_data, all_future_data):
    """
    Simulate a 5-entry survivor pool using the given scoring function.
    Returns a dict with results per week.
    """
    entries = [f"Entry {i+1}" for i in range(NUM_ENTRIES)]
    alive = set(range(NUM_ENTRIES))
    used_teams = [set() for _ in range(NUM_ENTRIES)]
    results = {
        "strategy": strategy_name,
        "weeks": [],
        "final_elimination_week": None,
        "total_entry_weeks_survived": 0,
    }

    for week in range(1, TOTAL_WEEKS + 1):
        teams = all_week_data.get(week, [])
        if not teams:
            results["weeks"].append({
                "week": week,
                "picks": [],
                "eliminations": [],
                "alive_count": len(alive),
                "note": "No data"
            })
            continue

        if not alive:
            results["weeks"].append({
                "week": week,
                "picks": [],
                "eliminations": [],
                "alive_count": 0,
                "note": "All eliminated"
            })
            continue

        # Build future data (only weeks after current)
        future = {w: d for w, d in all_future_data.items() if w > week}

        # Score all teams
        for t in teams:
            t["_score"] = score_fn(t, teams, future)

        scored_teams = sorted(teams, key=lambda t: t["_score"], reverse=True)

        # Greedy assignment
        assigned_this_week = set()
        picks = {}
        alive_sorted = sorted(alive)

        for i in alive_sorted:
            for t in scored_teams:
                tid = t["teamId"]
                if tid not in assigned_this_week and tid not in used_teams[i]:
                    assigned_this_week.add(tid)
                    used_teams[i].add(tid)
                    picks[i] = t
                    break

        # Evaluate outcomes
        week_picks = []
        eliminations = []
        for i in alive_sorted:
            p = picks.get(i)
            if p:
                outcome = p["outcome"]
                week_picks.append({
                    "entry": entries[i],
                    "team": p["teamId"],
                    "winProb": round(p["winProbability"], 3),
                    "pickShare": round(p["pickShare"], 1),
                    "score": round(p["_score"], 4),
                    "outcome": outcome or "Pending",
                    "spread": p.get("spread"),
                })
                if outcome == "Loss":
                    alive.discard(i)
                    eliminations.append(entries[i])
                else:
                    results["total_entry_weeks_survived"] += 1

        results["weeks"].append({
            "week": week,
            "picks": week_picks,
            "eliminations": eliminations,
            "alive_count": len(alive),
        })

        if not alive and results["final_elimination_week"] is None:
            results["final_elimination_week"] = week

    if results["final_elimination_week"] is None:
        if alive:
            results["final_elimination_week"] = "Survived all 18 weeks"
        else:
            # Find last week with elimination
            for wr in reversed(results["weeks"]):
                if wr.get("eliminations"):
                    results["final_elimination_week"] = wr["week"]
                    break

    return results


def print_results(results_list):
    """Print a comparison summary of all strategies."""
    print("\n" + "=" * 80)
    print("STRATEGY COMPARISON: 2025 NFL SURVIVOR POOL (5 ENTRIES)")
    print("=" * 80)

    for r in results_list:
        print(f"\n{'─' * 60}")
        print(f"Strategy: {r['strategy']}")
        print(f"Final elimination: Week {r['final_elimination_week']}")
        print(f"Total entry-weeks survived: {r['total_entry_weeks_survived']} / {NUM_ENTRIES * TOTAL_WEEKS}")
        print()

        for w in r["weeks"]:
            if not w["picks"]:
                continue
            week_num = w["week"]
            alive = w["alive_count"]
            picks_str = ", ".join(
                f"{p['entry']}: {p['team']} ({p['winProb']:.0%} wp, {p['pickShare']}% own, score={p['score']:.2f}) -> {p['outcome']}"
                for p in w["picks"]
            )
            elim_str = f" ** ELIMINATED: {w['eliminations']}" if w["eliminations"] else ""
            print(f"  W{week_num:2d} [{alive} alive] {picks_str}{elim_str}")

    # Summary table
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"{'Strategy':<35} {'Last Elim Week':<16} {'Entry-Weeks Survived':<22} {'Survival Rate'}")
    print(f"{'─' * 35} {'─' * 16} {'─' * 22} {'─' * 14}")
    for r in results_list:
        rate = r["total_entry_weeks_survived"] / (NUM_ENTRIES * TOTAL_WEEKS) * 100
        print(f"{r['strategy']:<35} Week {str(r['final_elimination_week']):<11} {r['total_entry_weeks_survived']:<22} {rate:.1f}%")


def main():
    print("Stan the Scout: Loading 2025 season data...")
    print()

    # Fetch all games and dynamics data
    all_week_data = {}
    all_future_data = {}

    for week in range(1, TOTAL_WEEKS + 1):
        sys.stdout.write(f"\r  Fetching week {week}/{TOTAL_WEEKS}...")
        sys.stdout.flush()

        games = fetch_games(week)
        dynamics = fetch_dynamics(week)
        teams = build_week_data(games, dynamics)

        if teams:
            all_week_data[week] = teams
            all_future_data[week] = teams
        else:
            print(f"\n  WARNING: No data for week {week}")

    print(f"\r  Loaded {len(all_week_data)} weeks of data.          ")
    print()

    # Run all 4 strategies
    strategies = [
        ("1. Pure Win Probability", score_pure_win_prob),
        ("2. Leverage Score (WP / Ownership)", score_leverage),
        ("3. Survival Equity", score_survival_equity),
        ("4. Future Value Preservation", score_future_value),
    ]

    results = []
    for name, fn in strategies:
        print(f"  Simulating: {name}...")
        r = simulate_strategy(name, fn, all_week_data, all_future_data)
        results.append(r)

    print_results(results)


if __name__ == "__main__":
    main()
