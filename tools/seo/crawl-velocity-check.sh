#!/bin/bash

# ============================================================
# SideGuy Crawl Velocity Check
# Run after each GSC export or winner loop pass.
# Reads git log + gsc-winners.json to report crawl signals.
# ============================================================

echo ""
echo "========================================"
echo "  SIDEGUY CRAWL VELOCITY CHECK"
echo "  $(date '+%Y-%m-%d %I:%M%p %Z')"
echo "========================================"
echo ""

DATE=$(date +"%Y-%m-%d")
WINNERS="data/gsc-winners.json"
CRAWL_REPORT="docs/reports/crawl-velocity.md"

# ── 1. URLs updated today ─────────────────────────────────────
echo "--- URLS UPDATED TODAY ($DATE) ---"
echo ""
UPDATED=$(git log --since="$DATE 00:00:00" --name-only --pretty=format:"" | \
          grep "\.html$" | sort -u)

if [ -z "$UPDATED" ]; then
  echo "  No HTML files committed today yet."
else
  echo "$UPDATED" | while read f; do
    echo "  ✅ $f"
  done
fi
echo ""

# ── 2. Commit count today ────────────────────────────────────
COMMIT_COUNT=$(git log --since="$DATE 00:00:00" --oneline | wc -l | tr -d ' ')
echo "  Commits today: $COMMIT_COUNT"
echo ""

# ── 3. URLs ranking top 10 (from gsc-winners.json) ───────────
echo "--- URLS RANKING TOP 10 (from gsc-winners.json) ---"
echo ""
if [ -f "$WINNERS" ]; then
  python3 - <<'PYEOF'
import json

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

top10 = [w for w in winners if w.get("position", 999) <= 10]
top10_sorted = sorted(top10, key=lambda x: x.get("position", 999))

if top10_sorted:
    for w in top10_sorted:
        print(f"  pos {w['position']:>5.2f}  |  {w.get('impressions',0):>4} impr  |  {w['query']}")
        print(f"           {w['page']}")
        print()
else:
    print("  No winners currently in top 10 position.")
    print()
PYEOF
else
  echo "  WARNING: $WINNERS not found. Run GSC export first."
  echo ""
fi

# ── 4. URLs refreshed from GSC data ──────────────────────────
echo "--- URLS REFRESHED FROM GSC DATA ---"
echo ""
if [ -f "$WINNERS" ]; then
  python3 - <<'PYEOF'
import json
from pathlib import Path

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

today = __import__('datetime').date.today().isoformat()
refreshed = [w for w in winners if w.get("pulled_date") == today]

if refreshed:
    for w in refreshed:
        page = w["page"].lstrip("/")
        exists = "✅" if Path(page).exists() else "⚠️  (file not found at ./" + page + ")"
        print(f"  {exists}  {w['query']}")
        print(f"      {w['page']}  ·  pos {w.get('position')}  ·  {w.get('impressions',0)} impr")
        print()
else:
    print("  No winners with today's pulled_date in gsc-winners.json.")
    print()
PYEOF
fi

# ── 5. Pages likely to attract recrawl ───────────────────────
echo "--- PAGES LIKELY TO ATTRACT RECRAWL ---"
echo ""
python3 - <<'PYEOF'
import json
import subprocess
from pathlib import Path
from datetime import date

today = date.today().isoformat()

# Get files modified in git today
result = subprocess.run(
    ["git", "log", f"--since={today} 00:00:00", "--name-only", "--pretty=format:"],
    capture_output=True, text=True
)
modified_today = set(
    line.strip() for line in result.stdout.splitlines()
    if line.strip().endswith(".html")
)

# Load winners
winners = []
if Path("data/gsc-winners.json").exists():
    with open("data/gsc-winners.json") as f:
        winners = json.load(f)

winner_pages = {w["page"].lstrip("/") for w in winners}

# Score each URL
print("  Score = modified_today(+3) + in_top10(+2) + in_winner_feed(+1) + has_impressions(+1)")
print()

all_candidates = set(modified_today) | winner_pages
scored = []
for page in all_candidates:
    score = 0
    reasons = []
    pos = None
    impr = None

    if page in modified_today:
        score += 3
        reasons.append("modified today")

    for w in winners:
        if w["page"].lstrip("/") == page:
            impr = w.get("impressions", 0)
            pos = w.get("position", 999)
            score += 1
            reasons.append("in winner feed")
            if impr and impr > 0:
                score += 1
                reasons.append(f"{impr} impr")
            if pos and pos <= 10:
                score += 2
                reasons.append(f"pos {pos}")
            break

    scored.append((score, page, reasons, pos, impr))

scored.sort(key=lambda x: -x[0])

for score, page, reasons, pos, impr in scored:
    tag = "🔥" if score >= 5 else "✅" if score >= 3 else "📋"
    pos_str = f"pos {pos}" if pos else ""
    print(f"  {tag} score={score}  /{page}")
    print(f"      {', '.join(reasons)}")
    print()
PYEOF

# ── 6. Sitemap freshness check ────────────────────────────────
echo "--- SITEMAP LASTMOD CHECK ---"
echo ""
for sm in sitemap.xml sitemap-longtail.xml public/sitemap-money.xml; do
  if [ -f "$sm" ]; then
    LAST=$(grep -o '<lastmod>[^<]*</lastmod>' "$sm" | tail -1 | sed 's/<[^>]*>//g')
    COUNT=$(grep -c '<url>' "$sm" 2>/dev/null || echo "?")
    echo "  $sm — $COUNT URLs — latest lastmod: $LAST"
  fi
done
echo ""

# ── 7. Append scan to crawl-velocity.md ──────────────────────
python3 - <<'PYEOF'
import json
import subprocess
from datetime import datetime
from pathlib import Path

now = datetime.now().strftime("%Y-%m-%d %H:%M PDT")
today = datetime.now().strftime("%Y-%m-%d")

# Commits today
result = subprocess.run(
    ["git", "log", f"--since={today} 00:00:00", "--oneline"],
    capture_output=True, text=True
)
commits = len([l for l in result.stdout.splitlines() if l.strip()])

# HTML files modified
result2 = subprocess.run(
    ["git", "log", f"--since={today} 00:00:00", "--name-only", "--pretty=format:"],
    capture_output=True, text=True
)
html_files = sorted(set(
    l.strip() for l in result2.stdout.splitlines()
    if l.strip().endswith(".html")
))

# Winners
winners = []
if Path("data/gsc-winners.json").exists():
    with open("data/gsc-winners.json") as f:
        winners = json.load(f)

entry  = f"\n---\n\n## Crawl Velocity Scan — {now}\n\n"
entry += f"- **Commits today:** {commits}\n"
entry += f"- **HTML files modified:** {len(html_files)}\n"
entry += f"- **Winner feed entries:** {len(winners)}\n\n"

if html_files:
    entry += "**Modified today:**\n"
    for f in html_files:
        entry += f"- {f}\n"
    entry += "\n"

if winners:
    entry += "**Winner feed positions:**\n"
    entry += "| Query | Position | Impressions |\n"
    entry += "|---|---|---|\n"
    for w in sorted(winners, key=lambda x: x.get("position", 999)):
        entry += f"| {w.get('query')} | {w.get('position')} | {w.get('impressions',0)} |\n"
    entry += "\n"

with open("docs/reports/crawl-velocity.md", "a") as f:
    f.write(entry)

print(f"Appended scan to docs/reports/crawl-velocity.md")
PYEOF

echo ""
echo "========================================"
echo "  CRAWL VELOCITY CHECK COMPLETE"
echo "========================================"
echo ""
