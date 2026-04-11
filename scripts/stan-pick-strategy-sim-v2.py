#!/usr/bin/env python3
"""
Stan the Scout: 2025 NFL Survivor Pool Pick Strategy Simulation — Round 2

Constrained versions that apply a minimum win probability floor before scoring.
Also includes the original Pure Win Probability as baseline for comparison.

Strategies:
1. Pure Win Probability (baseline)
2a. Leverage with 60% Floor - leverage score but only teams with winProb >= 0.60
2b. Weighted Blend - 0.7 * winProb + 0.3 * (1 - pickShare/100)
2c. Tiered - pick from top 10 by winProb, then choose lowest ownership
2d. Leverage with 55% Floor - slightly more permissive floor
2e. Weighted Blend (80/20) - heavier on win prob: 0.8 * winProb + 0.2 * (1 - pickShare/100)
2f. Anti-Chalk Top-5 - from top 5 by winProb per entry, pick the one with lowest ownership
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
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  WARN: Failed to fetch {url}: {e}", file=sys.stderr)
        return None


def fetch_games(week):
    url = f"{BASE_URL}/api/games?season={SEASON}&scheduleType=regular&week={week}"
    return fetch_json(url)


def fetch_dynamics(week):
    url = f"{BASE_URL}/api/pools/{POOL_ID}/dynamics/comprehensive?week={week}&season={SEASON}&scheduleType=regular"
    return fetch_json(url)


def build_week_data(games, dynamics):
    if not games or not dynamics:
        return []

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
            "outcome": home_outcome,
        })
        teams.append({
            "teamId": away_id,
            "winProbability": awp,
            "pickShare": pick_shares.get(away_id, 0),
            "opponent": home_id,
            "spread": -home_spread if home_spread is not None else None,
            "outcome": away_outcome,
        })
    return teams


# ─── Scoring Functions ──────────────────────────────────────────────────────

def score_pure_win_prob(team, _all_teams, _future_data, _available):
    """Strategy 1: Pure win probability."""
    return team["winProbability"]


def score_leverage_floor_60(team, _all_teams, _future_data, _available):
    """Strategy 2a: Leverage with 60% win prob floor."""
    wp = team["winProbability"]
    if wp < 0.60:
        return -1  # filtered out
    ps = max(team["pickShare"], 0.1)
    return wp / (ps / 100)


def score_leverage_floor_55(team, _all_teams, _future_data, _available):
    """Strategy 2d: Leverage with 55% win prob floor."""
    wp = team["winProbability"]
    if wp < 0.55:
        return -1
    ps = max(team["pickShare"], 0.1)
    return wp / (ps / 100)


def score_weighted_blend_70_30(team, _all_teams, _future_data, _available):
    """Strategy 2b: 0.7 * winProb + 0.3 * (1 - pickShare/100)."""
    wp = team["winProbability"]
    anti_chalk = 1 - team["pickShare"] / 100
    return 0.7 * wp + 0.3 * anti_chalk


def score_weighted_blend_80_20(team, _all_teams, _future_data, _available):
    """Strategy 2e: 0.8 * winProb + 0.2 * (1 - pickShare/100)."""
    wp = team["winProbability"]
    anti_chalk = 1 - team["pickShare"] / 100
    return 0.8 * wp + 0.2 * anti_chalk


def score_tiered_top10(team, _all_teams, _future_data, available):
    """
    Strategy 2c: Tiered approach.
    Only consider top 10 teams by winProb (from available pool).
    Among those, pick lowest ownership.
    Score = 1000 if in top 10 by winProb (with tiebreaker on low ownership), else -1.
    """
    # Sort available teams by winProb to find top 10
    sorted_avail = sorted(available, key=lambda t: t["winProbability"], reverse=True)
    top10_ids = set(t["teamId"] for t in sorted_avail[:10])
    
    if team["teamId"] not in top10_ids:
        return -1
    
    # Among top 10: primary = winProb (inverted slightly), secondary = lowest ownership
    # We want lowest ownership to win, so: high winProb bonus + anti-chalk
    wp = team["winProbability"]
    anti_chalk = 1 - team["pickShare"] / 100
    return wp * 0.01 + anti_chalk  # winProb as tiny tiebreaker, ownership dominates


def score_antichalk_top5(team, _all_teams, _future_data, available):
    """
    Strategy 2f: Anti-Chalk Top-5.
    From the top 5 teams by winProb that are available, pick lowest ownership.
    """
    sorted_avail = sorted(available, key=lambda t: t["winProbability"], reverse=True)
    top5_ids = set(t["teamId"] for t in sorted_avail[:5])
    
    if team["teamId"] not in top5_ids:
        return -1
    
    wp = team["winProbability"]
    anti_chalk = 1 - team["pickShare"] / 100
    return wp * 0.001 + anti_chalk  # ownership dominates within top 5


# ─── Simulation ─────────────────────────────────────────────────────────────

def simulate_strategy(strategy_name, score_fn, all_week_data, all_future_data):
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
                "week": week, "picks": [], "eliminations": [],
                "alive_count": len(alive), "note": "No data"
            })
            continue

        if not alive:
            results["weeks"].append({
                "week": week, "picks": [], "eliminations": [],
                "alive_count": 0, "note": "All eliminated"
            })
            continue

        future = {w: d for w, d in all_future_data.items() if w > week}

        # Greedy assignment
        assigned_this_week = set()
        picks = {}
        alive_sorted = sorted(alive)

        for i in alive_sorted:
            # Build available pool for this entry
            available = [t for t in teams 
                        if t["teamId"] not in assigned_this_week 
                        and t["teamId"] not in used_teams[i]]
            
            # Score all available teams
            for t in available:
                t["_score"] = score_fn(t, teams, future, available)
            
            # Filter out negative scores (below floor)
            viable = [t for t in available if t["_score"] >= 0]
            
            if not viable:
                # Fallback: if all teams below floor, pick highest winProb from available
                viable = sorted(available, key=lambda t: t["winProbability"], reverse=True)
            else:
                viable = sorted(viable, key=lambda t: t["_score"], reverse=True)
            
            if viable:
                best = viable[0]
                assigned_this_week.add(best["teamId"])
                used_teams[i].add(best["teamId"])
                picks[i] = best

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
                    "score": round(p.get("_score", 0), 4),
                    "outcome": outcome or "Pending",
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
            results["final_elimination_week"] = f"Survived (entries alive: {len(alive)})"
        else:
            for wr in reversed(results["weeks"]):
                if wr.get("eliminations"):
                    results["final_elimination_week"] = wr["week"]
                    break

    return results


def print_results(results_list):
    print("\n" + "=" * 80)
    print("STRATEGY COMPARISON — ROUND 2: CONSTRAINED APPROACHES")
    print("2025 NFL SURVIVOR POOL (5 ENTRIES)")
    print("=" * 80)

    for r in results_list:
        print(f"\n{'─' * 70}")
        print(f"Strategy: {r['strategy']}")
        print(f"Final elimination: Week {r['final_elimination_week']}")
        print(f"Total entry-weeks survived: {r['total_entry_weeks_survived']} / {NUM_ENTRIES * TOTAL_WEEKS}")
        print()

        for w in r["weeks"]:
            if not w["picks"]:
                continue
            week_num = w["week"]
            alive = w["alive_count"]
            for p in w["picks"]:
                elim_mark = " ** ELIM" if p["outcome"] == "Loss" else ""
                print(f"    W{week_num:2d} {p['entry']}: {p['team']:4s} (wp={p['winProb']:.0%}, own={p['pickShare']:5.1f}%, score={p['score']:.3f}) -> {p['outcome']}{elim_mark}")
            if w["eliminations"]:
                print(f"    ** Week {week_num} eliminations: {w['eliminations']}")
            print()

    # Summary table
    print(f"\n{'=' * 90}")
    print("SUMMARY")
    print(f"{'=' * 90}")
    print(f"{'Strategy':<45} {'Last Elim':<12} {'Entry-Wks':<12} {'Rate':<8} {'Avg WP of Picks'}")
    print(f"{'─' * 45} {'─' * 12} {'─' * 12} {'─' * 8} {'─' * 16}")
    
    for r in results_list:
        rate = r["total_entry_weeks_survived"] / (NUM_ENTRIES * TOTAL_WEEKS) * 100
        # Calculate average win probability of all picks made
        all_wps = []
        for w in r["weeks"]:
            for p in w["picks"]:
                all_wps.append(p["winProb"])
        avg_wp = sum(all_wps) / len(all_wps) if all_wps else 0
        
        # Calculate average ownership of picks
        all_owns = []
        for w in r["weeks"]:
            for p in w["picks"]:
                all_owns.append(p["pickShare"])
        avg_own = sum(all_owns) / len(all_owns) if all_owns else 0
        
        print(f"{r['strategy']:<45} Wk {str(r['final_elimination_week']):<8} {r['total_entry_weeks_survived']:<12} {rate:<8.1f} {avg_wp:.1%} wp / {avg_own:.1f}% own")


def main():
    print("Stan the Scout — Round 2: Loading 2025 season data...")
    print()

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

    print(f"\r  Loaded {len(all_week_data)} weeks of data.          ")
    print()

    strategies = [
        ("1. Pure Win Probability (baseline)", score_pure_win_prob),
        ("2a. Leverage + 60% Floor", score_leverage_floor_60),
        ("2b. Weighted Blend (70/30)", score_weighted_blend_70_30),
        ("2c. Tiered Top-10 (lowest ownership)", score_tiered_top10),
        ("2d. Leverage + 55% Floor", score_leverage_floor_55),
        ("2e. Weighted Blend (80/20)", score_weighted_blend_80_20),
        ("2f. Anti-Chalk Top-5", score_antichalk_top5),
    ]

    results = []
    for name, fn in strategies:
        print(f"  Simulating: {name}...")
        r = simulate_strategy(name, fn, all_week_data, all_future_data)
        results.append(r)

    print_results(results)


if __name__ == "__main__":
    main()
