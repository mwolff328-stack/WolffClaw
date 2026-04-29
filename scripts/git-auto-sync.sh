#!/usr/bin/env bash
# git-auto-sync.sh — Hourly multi-repo workspace sync
# Commits local changes, pulls remote, pushes. Detects conflicts and aborts cleanly.
# Also discovers new repos on the machine.

set -euo pipefail

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TIMESTAMP_TAG="sync-$(date -u +"%Y%m%d-%H%M%S")"
LOG_PREFIX="[git-auto-sync $TIMESTAMP]"

# ── Repo registry ──────────────────────────────────────────────
# All repos to sync. Each must have a remote named "origin".
REPOS=(
  "/Users/mrwolff/.openclaw/workspace"
  "/Users/mrwolff/.claude"
  "/Users/mrwolff/.openclaw/workspace-deb"
  "/Users/mrwolff/.openclaw/workspace/stan"
  "/Users/mrwolff/.openclaw/workspace-smuggs"
  "/Users/mrwolff/bubba-workspace"
  "/Users/mrwolff/Projects/SurvivorPulse"
  "/Users/mrwolff/Projects/SurvivorPulse-BackTesting-Prototype"
)

# Repos to skip during discovery (already tracked or intentionally excluded)
SKIP_DISCOVERY=(
  "/Users/mrwolff/Projects/everything-claude-code"
)

ERRORS=()
SYNCED=()
DISCOVERED=()

# ── Sync one repo ──────────────────────────────────────────────
sync_repo() {
  local repo="$1"
  local name
  name=$(basename "$repo")

  if [ ! -d "$repo/.git" ]; then
    echo "$LOG_PREFIX SKIP $name: not a git repo"
    return 0
  fi

  cd "$repo"

  # Check for origin remote
  if ! git remote get-url origin &>/dev/null; then
    echo "$LOG_PREFIX SKIP $name: no origin remote"
    return 0
  fi

  local branch
  branch=$(git branch --show-current 2>/dev/null || echo "main")
  [ -z "$branch" ] && branch="main"

  echo "$LOG_PREFIX [$name] Starting sync on branch $branch..."

  # 1. Commit local changes
  # Handle nested git repos: use --ignore-errors to skip problematic paths
  if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null || [ -n "$(git ls-files --others --exclude-standard 2>/dev/null)" ]; then
    echo "$LOG_PREFIX [$name] Changes detected, staging and committing..."
    git add -A 2>/dev/null || git add --ignore-errors -A 2>/dev/null || true

    if ! git commit -m "auto-sync: $TIMESTAMP" 2>&1; then
      echo "$LOG_PREFIX [$name] ERROR: Commit failed (pre-commit hook may have blocked sensitive data)."
      ERRORS+=("$name: commit blocked by pre-commit hook")
      return 1
    fi

    git tag "${TIMESTAMP_TAG}-${name}" 2>/dev/null || true
    echo "$LOG_PREFIX [$name] Committed and tagged: ${TIMESTAMP_TAG}-${name}"
  else
    echo "$LOG_PREFIX [$name] No local changes."
  fi

  # 2. Fetch remote
  echo "$LOG_PREFIX [$name] Fetching..."
  if ! git fetch origin 2>&1; then
    echo "$LOG_PREFIX [$name] WARNING: Fetch failed. Skipping pull."
    ERRORS+=("$name: fetch failed")
    return 1
  fi

  # 3. Pull if needed
  local local_head remote_head
  local_head=$(git rev-parse HEAD 2>/dev/null)
  remote_head=$(git rev-parse "origin/$branch" 2>/dev/null || echo "")

  if [ -n "$remote_head" ] && [ "$local_head" != "$remote_head" ]; then
    local merge_base
    merge_base=$(git merge-base HEAD "$remote_head" 2>/dev/null || echo "")

    if [ "$merge_base" = "$local_head" ]; then
      echo "$LOG_PREFIX [$name] Pulling remote changes..."
      if ! git pull --ff-only origin "$branch" 2>&1; then
        if ! git pull --rebase origin "$branch" 2>&1; then
          git rebase --abort 2>/dev/null || true
          echo "$LOG_PREFIX [$name] ERROR: Merge conflict."
          ERRORS+=("$name: merge conflict during pull")
          return 1
        fi
      fi
    elif [ "$merge_base" != "$remote_head" ]; then
      echo "$LOG_PREFIX [$name] Branches diverged. Attempting rebase..."
      if ! git pull --rebase origin "$branch" 2>&1; then
        git rebase --abort 2>/dev/null || true
        echo "$LOG_PREFIX [$name] ERROR: Merge conflict during rebase."
        ERRORS+=("$name: merge conflict (diverged branches)")
        return 1
      fi
    fi
  fi

  # 4. Push
  echo "$LOG_PREFIX [$name] Pushing..."
  if git push origin HEAD --tags 2>&1; then
    echo "$LOG_PREFIX [$name] Sync complete."
    SYNCED+=("$name")
  else
    echo "$LOG_PREFIX [$name] ERROR: Push failed."
    ERRORS+=("$name: push failed")
    return 1
  fi
}

# ── Discover new repos ─────────────────────────────────────────
discover_repos() {
  echo "$LOG_PREFIX Scanning for new repos..."

  local known_set=""
  for r in "${REPOS[@]}" "${SKIP_DISCOVERY[@]}"; do
    known_set="$known_set|$r"
  done

  while IFS= read -r gitdir; do
    local repo_path
    repo_path=$(dirname "$gitdir")

    # Skip known repos
    if echo "$known_set" | grep -qF "|$repo_path"; then
      continue
    fi

    # Skip nested .git dirs (inside node_modules, etc.)
    if echo "$repo_path" | grep -qE 'node_modules|\.Trash|/\.|vendor|cache'; then
      continue
    fi

    # Check if it has a remote
    local has_remote="no"
    if cd "$repo_path" 2>/dev/null && git remote get-url origin &>/dev/null; then
      has_remote="yes"
    fi

    DISCOVERED+=("$repo_path (remote: $has_remote)")
    echo "$LOG_PREFIX DISCOVERED: $repo_path (has remote: $has_remote)"
  done < <(find /Users/mrwolff -maxdepth 3 -name ".git" -type d 2>/dev/null | sort)
}

# ── Main ───────────────────────────────────────────────────────
echo "$LOG_PREFIX ============================================"
echo "$LOG_PREFIX Starting multi-repo sync (${#REPOS[@]} repos)"
echo "$LOG_PREFIX ============================================"

for repo in "${REPOS[@]}"; do
  sync_repo "$repo" || true
  echo ""
done

discover_repos
echo ""

# ── Summary ────────────────────────────────────────────────────
echo "$LOG_PREFIX ============================================"
echo "$LOG_PREFIX SUMMARY"
echo "$LOG_PREFIX Synced: ${#SYNCED[@]}/${#REPOS[@]} repos"
if [ ${#SYNCED[@]} -gt 0 ]; then
  for s in "${SYNCED[@]}"; do
    echo "$LOG_PREFIX   OK: $s"
  done
fi

if [ ${#ERRORS[@]} -gt 0 ]; then
  echo "$LOG_PREFIX ERRORS (${#ERRORS[@]}):"
  for e in "${ERRORS[@]}"; do
    echo "$LOG_PREFIX   FAIL: $e"
  done
  echo "NOTIFY:CONFLICT:Git sync errors in ${#ERRORS[@]} repo(s): $(IFS='; '; echo "${ERRORS[*]}")"
fi

if [ ${#DISCOVERED[@]} -gt 0 ]; then
  echo "$LOG_PREFIX NEW REPOS FOUND (${#DISCOVERED[@]}):"
  for d in "${DISCOVERED[@]}"; do
    echo "$LOG_PREFIX   NEW: $d"
  done
  echo "NOTIFY:DISCOVERY:Found ${#DISCOVERED[@]} new repo(s) not in sync list: $(IFS='; '; echo "${DISCOVERED[*]}")"
fi

echo "$LOG_PREFIX Done. Tag prefix: $TIMESTAMP_TAG"
