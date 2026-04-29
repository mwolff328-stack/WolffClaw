---
name: Advanced Strategy Modes - Implementation Requirements
description: Three new scoring modes for the simulation engine: coordinated diversification, adaptive blend, scarcity-aware
type: project
date: 2026-04-13
---

# Advanced Strategy Modes - Requirements

## Mode 1: Coordinated Diversification (Anti-Correlation)

### Concept
Instead of greedily assigning the best team to each entry independently, maximize pick DIVERSITY across entries within each week. This is the core CMEA thesis: if all entries pick the same team and it loses, all entries die together.

### Algorithm
For each week:
1. Build the candidate pool (all 32 teams, scored by current strategy config)
2. Instead of giving Entry 1 the #1 team, Entry 2 the #2 team, etc.:
   - Maximize the number of DISTINCT teams picked across all entries
   - Among feasible diverse assignments, optimize total score
   - In practice: for N entries, pick the N teams that maximize diversity while maintaining acceptable quality
3. The key constraint: NO two entries pick the same team in the same week (this is already enforced). The difference from current greedy: instead of always giving the alphabetically-first entry the best team, distribute picks to minimize correlation risk.

### Implementation Approach
Instead of greedy top-down assignment, use a "round-robin" or "balanced" assignment:
- Sort candidates by score
- Assign Entry 1 the #1 team, Entry 2 the #3 team, Entry 3 the #5 team, etc. (skip-one pattern)
- This ensures entries aren't all clustered on adjacent-ranked teams

Or more sophisticated: solve a simple assignment problem where the objective is `max(sum_of_scores) + lambda * diversity_bonus` where diversity_bonus measures how spread out the picks are across the win probability spectrum.

### StrategyConfig Addition
Add `coordinatedDiversification: boolean` flag. When true, the assignment uses the diversified algorithm instead of greedy.

## Mode 2: Adaptive Blend (Season-Phase-Aware)

### Concept
Shift strategy weights across the season. Early season: emphasize win probability (survive the easy weeks safely). Late season: shift toward contrarian/pick share (field has thinned, need edge over remaining opponents).

### Algorithm
For each week, compute adjusted weights based on week number:
```
progressFactor = (week - 1) / 17  // 0.0 for Week 1, 1.0 for Week 18

adjustedWpWeight = wpWeight * (1 - progressFactor * adaptiveStrength) 
adjustedPsWeight = psWeight + (wpWeight * progressFactor * adaptiveStrength)
// Basically: transfer weight from WP to PS as season progresses
```

`adaptiveStrength` controls how much shifting occurs:
- 0.0 = no adaptation (same weights all season)  
- 0.5 = moderate shift (by Week 18, half of WP weight transferred to PS)
- 1.0 = full shift (by Week 18, WP weight → 0, all weight in PS)

### StrategyConfig Addition
Add `adaptiveBlend: boolean` and `adaptiveStrength: number` (0-1, default 0.5).

## Mode 3: Scarcity-Aware

### Concept
Dynamically increase future value weight when an entry's remaining usable teams drops below a threshold. As teams get "used up" through the season, preserving good future options becomes more critical.

### Algorithm
For each entry, each week:
1. Count remaining usable teams = 32 - (teams already used by this entry)
2. Compute scarcity factor:
   ```
   remainingTeams = 32 - usedTeamCount
   scarcityThreshold = 20  // configurable
   if (remainingTeams < scarcityThreshold) {
     scarcityFactor = 1 - (remainingTeams / scarcityThreshold)  // 0 at threshold, 1 at 0 remaining
   } else {
     scarcityFactor = 0
   }
   ```
3. Boost future value weight dynamically:
   ```
   effectiveFvWeight = fvWeight + scarcityBoost * scarcityFactor
   // Reduce other weights proportionally to maintain sum = 100
   ```

### StrategyConfig Addition
Add `scarcityAware: boolean`, `scarcityThreshold: number` (default 20), `scarcityBoost: number` (default 15, max FV boost when at zero remaining teams).

## Implementation Notes

All three modes modify the scoring/assignment logic in `assignIndependentPicks`. They should be:
- Toggleable via StrategyConfig flags
- Composable (can combine adaptive + scarcity-aware, for example)
- Available as strategy template presets
- Included in the per-entry optimization grid

### New Templates to Add
- "Coordinated Diversification (70/30)" — 70/30 Blend + coordinatedDiversification
- "Adaptive Blend (70/30 → 30/70)" — starts 70/30, ends 30/70 by Week 18
- "Scarcity-Aware (70/30)" — 70/30 Blend + scarcity-aware with default thresholds
- "Full Strategy (70/30 + Adaptive + Scarcity)" — all three combined

### New Per-Entry Optimization Scenarios
- "Coordinated Diversification: All entries 70/30 + diversified"
- "Adaptive + Diversified: Entries use adaptive blend with diversified assignment"
- "Mixed Advanced: Half entries diversified, half scarcity-aware"
