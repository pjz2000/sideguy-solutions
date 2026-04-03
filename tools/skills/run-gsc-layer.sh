#!/bin/bash
# ============================================================
# SideGuy Skill Launcher: GSC Reality Layer
# Runs the full GSC winner loop — parse, update, rebuild cards,
# run watchtower, run crawl velocity, bump version, commit.
# See docs/skills/gsc-reality-layer.md for full doctrine.
# ============================================================

set -e

echo ""
echo "========================================"
echo "  GSC REALITY LAYER — SKILL LAUNCHER"
echo "  $(date '+%Y-%m-%d %I:%M%p %Z')"
echo "========================================"
echo ""

# ── STEP 1: Check prerequisites ───────────────────────────────
if [ ! -f "data/gsc-winners.json" ]; then
  echo "ERROR: data/gsc-winners.json not found."
  echo "Update it from your latest GSC export before running this skill."
  echo "See: docs/skills/gsc-reality-layer.md — Step 2"
  exit 1
fi

echo "✅ gsc-winners.json found"
python3 -c "import json; d=json.load(open('data/gsc-winners.json')); print(f'   {len(d)} winners loaded')"
echo ""

# ── STEP 2: Rebuild homepage trending cards ───────────────────
echo "--- Rebuilding homepage trending cards ---"
python3 tools/homepage-builder/update_trending_cards.py
echo ""

# ── STEP 3: Run page1 watchtower ─────────────────────────────
echo "--- Running page1 watchtower ---"
bash tools/seo/page1-watchtower.sh
echo ""

# ── STEP 4: Run crawl velocity check ─────────────────────────
echo "--- Running crawl velocity check ---"
bash tools/seo/crawl-velocity-check.sh
echo ""

# ── STEP 5: Version bump prompt ───────────────────────────────
echo "--- Version bump ---"
CURRENT=$(grep -o 'GSC layer v[0-9]*' index.html | tail -1)
echo "Current: $CURRENT"
CURRENT_NUM=$(echo "$CURRENT" | grep -o '[0-9]*$')
NEXT_NUM=$((CURRENT_NUM + 1))
DATE_STR=$(date '+%B %-d, %Y')
TIME_STR=$(date '+%-I:%M%p %Z')

echo "Bumping to: GSC layer v${NEXT_NUM} — ${DATE_STR} · ${TIME_STR}"
echo ""

# Perform the version bump in index.html
python3 - <<PYEOF
import re
from pathlib import Path

html = Path("index.html").read_text()
import datetime
now = datetime.datetime.now()
date_str = now.strftime("%B %-d, %Y")
time_str = now.strftime("%-I:%M%p PDT")

# Find current version number
m = re.search(r'GSC layer v(\d+)', html)
if not m:
    print("ERROR: Could not find GSC layer version in index.html")
    exit(1)

current = int(m.group(1))
new_v = current + 1

# Replace the timestamp line
old_pattern = re.compile(
    r'(April|January|February|March|May|June|July|August|September|October|November|December)'
    r'\s+\d{1,2},\s+\d{4}\s+[·•]\s+[\d:apmPAM]+\s+PDT\s+[•·]\s+GSC layer v\d+'
)
new_str = f"{date_str} · {time_str} • GSC layer v{new_v}"
result, count = old_pattern.subn(new_str, html)
if count == 0:
    print("WARNING: Could not find version timestamp pattern. Manual bump needed.")
else:
    Path("index.html").write_text(result)
    print(f"✅ Bumped to GSC layer v{new_v} — {date_str} · {time_str}")
PYEOF

echo ""

# ── STEP 6: Commit everything ─────────────────────────────────
echo "--- Committing ---"
DATE_COMPACT=$(date +"%Y-%m-%d")

git add index.html data/gsc-winners.json docs/reports/page1-watchtower.md docs/reports/crawl-velocity.md 2>/dev/null
git add -A -- "problems/*.html" 2>/dev/null || true

git diff --cached --quiet && echo "Nothing new to commit." || \
git commit -m "feat: gsc reality layer pass — ${DATE_COMPACT}

- Trending cards rebuilt from gsc-winners.json
- Watchtower scan logged
- Crawl velocity scan logged
- Version bumped

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

echo ""
echo "========================================"
echo "  GSC REALITY LAYER COMPLETE"
echo "  Next: git push (if ready to deploy)"
echo "========================================"
echo ""
