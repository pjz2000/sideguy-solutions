#!/usr/bin/env bash

########################################
# SIDEGUY SWARM v2 — INTELLIGENCE ONLY
# Analyzes data, identifies targets
# DOES NOT modify pages automatically
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

DATE=$(date +"%Y-%m-%d-%H%M")

DATA_FILE="data/gsc.csv"
LOG_DIR="docs/swarm-logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/intelligence-v2-$DATE.md"

echo "# 🧠 Swarm Intelligence v2 — $DATE" > "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "**Mode:** Observation only (no automatic edits)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

########################################
# 1. VALIDATE DATA SOURCE
########################################

if [ ! -f "$DATA_FILE" ]; then
  echo "❌ Missing data/gsc.csv" | tee -a "$LOG_FILE"
  echo "" >> "$LOG_FILE"
  echo "## Next Steps" >> "$LOG_FILE"
  echo "1. Export GSC data to data/gsc.csv" >> "$LOG_FILE"
  echo "2. Format: query,clicks,impressions,ctr,position" >> "$LOG_FILE"
  exit 1
fi

echo "✓ Found GSC data file" | tee -a "$LOG_FILE"
TOTAL_ROWS=$(tail -n +2 "$DATA_FILE" | wc -l)
echo "  └─ $TOTAL_ROWS queries in dataset" | tee -a "$LOG_FILE"
echo "" >> "$LOG_FILE"

########################################
# 2. ANALYZE TOP PERFORMING QUERIES
########################################

echo "📊 Analyzing top queries by clicks..." | tee -a "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "## Top 20 Queries by Clicks" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "| Rank | Query | Clicks | Impressions | CTR | Position |" >> "$LOG_FILE"
echo "|------|-------|--------|-------------|-----|----------|" >> "$LOG_FILE"

TOP_QUERIES=$(tail -n +2 "$DATA_FILE" | sort -t, -k2 -nr | head -n 20)

RANK=1
while IFS=, read -r query clicks impressions ctr position; do
  printf "| %2d | %-50s | %6s | %8s | %5s | %5s |\n" \
    "$RANK" "$query" "$clicks" "$impressions" "$ctr" "$position" >> "$LOG_FILE"
  RANK=$((RANK + 1))
done <<< "$TOP_QUERIES"

echo "" >> "$LOG_FILE"

########################################
# 3. MATCH QUERIES TO EXISTING PAGES
########################################

echo "🔍 Matching queries to existing pages..." | tee -a "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "## Query → Page Matches" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

MATCHES=0
NO_MATCHES=0

while IFS=, read -r query clicks impressions ctr position; do
  # Normalize query for filename matching
  NORMALIZED=$(echo "$query" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  
  # Look for matching HTML files
  FOUND_PAGES=$(find . -maxdepth 1 -name "*${NORMALIZED}*.html" 2>/dev/null)
  
  if [ -n "$FOUND_PAGES" ]; then
    echo "### ✓ \"$query\" ($clicks clicks)" >> "$LOG_FILE"
    echo "**Existing pages:**" >> "$LOG_FILE"
    while IFS= read -r page; do
      PAGE_NAME=$(basename "$page")
      echo "- [\`$PAGE_NAME\`]($PAGE_NAME)" >> "$LOG_FILE"
    done <<< "$FOUND_PAGES"
    echo "" >> "$LOG_FILE"
    MATCHES=$((MATCHES + 1))
  else
    echo "### ⚠ \"$query\" ($clicks clicks)" >> "$LOG_FILE"
    echo "**No matching page found**" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    NO_MATCHES=$((NO_MATCHES + 1))
  fi
done <<< "$TOP_QUERIES"

########################################
# 4. OPPORTUNITY ANALYSIS
########################################

echo "## Opportunity Summary" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "- **Queries with existing pages:** $MATCHES" >> "$LOG_FILE"
echo "- **Queries missing pages:** $NO_MATCHES" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

########################################
# 5. RECOMMENDATIONS (HUMAN REVIEW)
########################################

echo "## Recommendations for Human Review" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

if [ $MATCHES -gt 0 ]; then
  echo "### Optimize Existing Pages" >> "$LOG_FILE"
  echo "Pages already exist for $MATCHES top queries. Consider:" >> "$LOG_FILE"
  echo "1. Review content quality and freshness" >> "$LOG_FILE"
  echo "2. Ensure H1/title tags match search intent" >> "$LOG_FILE"
  echo "3. Add specific cost/timing information if missing" >> "$LOG_FILE"
  echo "4. Check mobile experience" >> "$LOG_FILE"
  echo "" >> "$LOG_FILE"
fi

if [ $NO_MATCHES -gt 0 ]; then
  echo "### Create New Content (Manual)" >> "$LOG_FILE"
  echo "$NO_MATCHES queries lack dedicated pages. For each:" >> "$LOG_FILE"
  echo "1. Verify search intent matches SideGuy mission" >> "$LOG_FILE"
  echo "2. Write unique, helpful content (not templates)" >> "$LOG_FILE"
  echo "3. Follow inline CSS pattern from existing pages" >> "$LOG_FILE"
  echo "4. Test on mobile before deploying" >> "$LOG_FILE"
  echo "" >> "$LOG_FILE"
fi

########################################
# 6. SAFETY REMINDER
########################################

echo "## ⚠️ Safety Reminders" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "- This script does **not** modify any pages automatically" >> "$LOG_FILE"
echo "- Review GSC data context before making content decisions" >> "$LOG_FILE"
echo "- Avoid bulk generation — each page needs unique value" >> "$LOG_FILE"
echo "- Reference \`SIDEGUY_CORE.md\` for philosophy alignment" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

########################################
# 7. OUTPUT RESULTS
########################################

echo "" | tee -a "$LOG_FILE"
echo "✅ Intelligence report complete" | tee -a "$LOG_FILE"
echo "📄 Report saved: $LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Next: Review report and decide on 3-5 pages to improve manually."
