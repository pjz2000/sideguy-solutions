#!/bin/bash
set -e

echo "⚡ SideGuy Page Builder"

cd "$(git rev-parse --show-toplevel)"

python3 scripts/build-pages.py

# Only commit if there are new/changed files
if [[ -n $(git status --porcelain) ]]; then
  git config --global user.name "sideguy-autobuilder"
  git config --global user.email "builder@sideguy.ai"
  git add .
  git commit -m "🤖 Auto-built SideGuy pages [$(date -u +%Y-%m-%dT%H:%M:%SZ)]"
  git push
  echo "✅ Pages committed and pushed."
else
  echo "ℹ️  No new pages to commit."
fi
