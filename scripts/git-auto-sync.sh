#!/usr/bin/env bash
# git-auto-sync.sh — Hourly workspace sync for WolffClaw
# Commits local changes, pulls remote, pushes. Detects conflicts and aborts cleanly.

set -euo pipefail

WORKSPACE="/Users/mrwolff/.openclaw/workspace"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TIMESTAMP_TAG="sync-$(date -u +"%Y%m%d-%H%M%S")"
LOG_PREFIX="[git-auto-sync $TIMESTAMP]"

cd "$WORKSPACE"

echo "$LOG_PREFIX Starting sync..."

# 1. Check for uncommitted changes and commit them
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "$LOG_PREFIX Changes detected, staging and committing..."
  git add -A

  # Pre-commit hook will catch sensitive data; if it fails, abort
  if ! git commit -m "auto-sync: $TIMESTAMP"; then
    echo "$LOG_PREFIX ERROR: Commit failed (pre-commit hook may have blocked sensitive data)."
    echo "NOTIFY:CONFLICT:Pre-commit hook blocked the commit. Check for sensitive data in staged files."
    exit 1
  fi

  # Tag the sync commit
  git tag "$TIMESTAMP_TAG" 2>/dev/null || true
  echo "$LOG_PREFIX Committed and tagged: $TIMESTAMP_TAG"
else
  echo "$LOG_PREFIX No local changes to commit."
fi

# 2. Fetch remote
echo "$LOG_PREFIX Fetching remote..."
git fetch origin

# 3. Check if we need to pull
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null || echo "")

if [ -z "$REMOTE" ]; then
  echo "$LOG_PREFIX WARNING: Could not determine remote HEAD. Skipping pull."
elif [ "$LOCAL" != "$REMOTE" ]; then
  MERGE_BASE=$(git merge-base HEAD "$REMOTE" 2>/dev/null || echo "")

  if [ "$MERGE_BASE" = "$LOCAL" ]; then
    # Remote is ahead, fast-forward
    echo "$LOG_PREFIX Remote has new commits. Pulling..."
    git pull --ff-only origin main 2>/dev/null || git pull --ff-only origin master 2>/dev/null || {
      echo "$LOG_PREFIX WARNING: Fast-forward pull failed. Attempting rebase..."
      if ! git pull --rebase origin main 2>/dev/null && ! git pull --rebase origin master 2>/dev/null; then
        # Rebase conflict detected
        git rebase --abort 2>/dev/null || true
        echo "$LOG_PREFIX ERROR: Merge conflict detected during pull."
        echo "NOTIFY:CONFLICT:Merge conflict detected pulling from remote. Manual resolution required."
        exit 2
      fi
    }
  elif [ "$MERGE_BASE" = "$REMOTE" ]; then
    # Local is ahead, just push
    echo "$LOG_PREFIX Local is ahead of remote. Will push."
  else
    # Diverged — attempt rebase
    echo "$LOG_PREFIX Branches have diverged. Attempting rebase..."
    if ! git pull --rebase origin main 2>/dev/null && ! git pull --rebase origin master 2>/dev/null; then
      git rebase --abort 2>/dev/null || true
      echo "$LOG_PREFIX ERROR: Merge conflict detected during rebase."
      echo "NOTIFY:CONFLICT:Branches diverged and rebase failed. Manual resolution required."
      exit 2
    fi
  fi
fi

# 4. Push
echo "$LOG_PREFIX Pushing to remote..."
if git push origin HEAD --tags 2>&1; then
  echo "$LOG_PREFIX Sync complete."
else
  echo "$LOG_PREFIX ERROR: Push failed."
  echo "NOTIFY:CONFLICT:Push to remote failed. Check SSH keys and remote access."
  exit 3
fi

echo "$LOG_PREFIX Done. Tagged: $TIMESTAMP_TAG"
