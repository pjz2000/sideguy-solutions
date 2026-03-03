#!/bin/bash
set -e

echo "⚡ SideGuy Page Builder"

cd "$(git rev-parse --show-toplevel)"

# Ensure authority dirs exist
mkdir -p hubs pillars sitemaps

# 1. Build leaf pages from manifest
python3 scripts/build-pages.py

# 2. Build authority hubs and pillar pages
python3 scripts/build-authority.py

# 3. Regenerate all sitemaps + sitemap_index.xml
python3 scripts/generate-sitemap.py

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
