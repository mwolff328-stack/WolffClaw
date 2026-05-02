#!/usr/bin/env bash
# install-hooks.sh — Install git hooks from scripts/hooks/ into .git/hooks/
# Run once after cloning or when hooks are updated.
#
# Usage: bash scripts/install-hooks.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_SRC="$REPO_ROOT/scripts/hooks"
HOOKS_DEST="$REPO_ROOT/.git/hooks"

if [ ! -d "$HOOKS_SRC" ]; then
  echo "ERROR: hooks source directory not found: $HOOKS_SRC"
  exit 1
fi

if [ ! -d "$HOOKS_DEST" ]; then
  echo "ERROR: .git/hooks not found — are you in a git repo?"
  exit 1
fi

echo "Installing git hooks from scripts/hooks/ → .git/hooks/"
echo ""

installed=0
for hook in "$HOOKS_SRC"/*; do
  name=$(basename "$hook")
  dest="$HOOKS_DEST/$name"

  if [ -f "$dest" ] && ! diff -q "$hook" "$dest" &>/dev/null; then
    echo "  Updating:  $name"
  elif [ ! -f "$dest" ]; then
    echo "  Installing: $name"
  else
    echo "  Up to date: $name"
    continue
  fi

  cp "$hook" "$dest"
  chmod +x "$dest"
  (( installed++ )) || true
done

echo ""
if [ "$installed" -gt 0 ]; then
  echo "✓ $installed hook(s) installed."
else
  echo "✓ All hooks already up to date."
fi
