#!/usr/bin/env bash

########################################
# SIDEGUY WEEKLY GSC AUTOPILOT
# Automates the weekly cluster intelligence workflow
########################################

# This script should be run weekly after downloading fresh GSC data
# It will:
# 1. Check for fresh GSC data (warn if data is old)
# 2. Run cluster intelligence analysis
# 3. Generate summary report
# 4. Notify operator of top opportunities

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

DATE="$(date +"%Y-%m-%d-%H%M%S")"
HUMAN_DATE="$(date +"%Y-%m-%d %H:%M:%S")"

DATA_DIR="$PROJECT_ROOT/docs/gsc"
PAGES_FILE="$DATA_DIR/gsc_pages.csv"
QUERIES_FILE="$DATA_DIR/gsc_queries.csv"

LOG_DIR="$PROJECT_ROOT/docs/cluster-intelligence/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/weekly-autopilot-$DATE.log"

echo "========================================" | tee "$LOG_FILE"
echo "🔄 SIDEGUY WEEKLY GSC AUTOPILOT" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "Run time: $HUMAN_DATE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

########################################
# STEP 1: VERIFY GSC DATA FRESHNESS
########################################

echo "📊 Checking GSC data freshness..." | tee -a "$LOG_FILE"

if [ ! -f "$PAGES_FILE" ]; then
  echo "❌ ERROR: Missing gsc_pages.csv" | tee -a "$LOG_FILE"
  echo "" | tee -a "$LOG_FILE"
  echo "ACTION REQUIRED:" | tee -a "$LOG_FILE"
  echo "1. Go to Google Search Console" | tee -a "$LOG_FILE"
  echo "2. Performance > Pages > Export" | tee -a "$LOG_FILE"
  echo "3. Save as: docs/gsc/gsc_pages.csv" | tee -a "$LOG_FILE"
  exit 1
fi

if [ ! -f "$QUERIES_FILE" ]; then
  echo "❌ ERROR: Missing gsc_queries.csv" | tee -a "$LOG_FILE"
  echo "" | tee -a "$LOG_FILE"
  echo "ACTION REQUIRED:" | tee -a "$LOG_FILE"
  echo "1. Go to Google Search Console" | tee -a "$LOG_FILE"
  echo "2. Performance > Queries > Export" | tee -a "$LOG_FILE"
  echo "3. Save as: docs/gsc/gsc_queries.csv" | tee -a "$LOG_FILE"
  exit 1
fi

# Check file ages (warn if older than 7 days)
PAGES_AGE=$(find "$PAGES_FILE" -mtime +7 2>/dev/null | wc -l)
QUERIES_AGE=$(find "$QUERIES_FILE" -mtime +7 2>/dev/null | wc -l)

if [ "$PAGES_AGE" -gt 0 ] || [ "$QUERIES_AGE" -gt 0 ]; then
  echo "⚠️  WARNING: GSC data is older than 7 days" | tee -a "$LOG_FILE"
  echo "   Consider downloading fresh data for best results" | tee -a "$LOG_FILE"
else
  echo "✅ GSC data is fresh (< 7 days old)" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"

########################################
# STEP 2: RUN CLUSTER INTELLIGENCE
########################################

echo "🧠 Running cluster intelligence analysis..." | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Run the driver (captures output)
DRIVER_OUTPUT=$("$PROJECT_ROOT/cluster-intelligence-driver.sh" 2>&1)
DRIVER_EXIT_CODE=$?

if [ $DRIVER_EXIT_CODE -ne 0 ]; then
  echo "❌ ERROR: Cluster intelligence failed" | tee -a "$LOG_FILE"
  echo "$DRIVER_OUTPUT" | tee -a "$LOG_FILE"
  exit 1
fi

echo "✅ Cluster intelligence complete" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

########################################
# STEP 3: EXTRACT KEY METRICS
########################################

echo "📈 Extracting key metrics..." | tee -a "$LOG_FILE"

# Find latest cluster files
LATEST_CLUSTERS=$(find "$PROJECT_ROOT/docs/cluster-intelligence" -name "clusters-*.csv" -type f | sort | tail -n 1)
LATEST_MISSING=$(find "$PROJECT_ROOT/docs/cluster-intelligence" -name "missing-pages-*.csv" -type f | sort | tail -n 1)
LATEST_OPPS=$(find "$PROJECT_ROOT/docs/cluster-intelligence" -name "opportunities-*.csv" -type f | sort | tail -n 1)

if [ -z "$LATEST_CLUSTERS" ]; then
  echo "⚠️  WARNING: Could not find cluster analysis output" | tee -a "$LOG_FILE"
else
  echo "" | tee -a "$LOG_FILE"
  echo "🎯 TOP 5 CLUSTERS BY IMPRESSION VOLUME:" | tee -a "$LOG_FILE"
  echo "---------------------------------------" | tee -a "$LOG_FILE"
  tail -n +2 "$LATEST_CLUSTERS" | head -n 5 | column -t -s, | tee -a "$LOG_FILE"
  echo "" | tee -a "$LOG_FILE"
fi

if [ -n "$LATEST_MISSING" ]; then
  MISSING_COUNT=$(tail -n +2 "$LATEST_MISSING" | wc -l)
  
  if [ "$MISSING_COUNT" -gt 0 ]; then
    echo "🔥 MISSING PAGE OPPORTUNITIES: $MISSING_COUNT pages identified" | tee -a "$LOG_FILE"
    echo "---------------------------------------" | tee -a "$LOG_FILE"
    tail -n +2 "$LATEST_MISSING" | head -n 10 | column -t -s, | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
    
    if [ "$MISSING_COUNT" -gt 10 ]; then
      echo "   ... and $((MISSING_COUNT - 10)) more opportunities" | tee -a "$LOG_FILE"
      echo "" | tee -a "$LOG_FILE"
    fi
  else
    echo "✅ No missing pages detected (all demand is covered)" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
  fi
fi

########################################
# STEP 4: GENERATE WEEKLY SUMMARY
########################################

SUMMARY_FILE="$PROJECT_ROOT/docs/cluster-intelligence/weekly-summary-$DATE.md"

cat > "$SUMMARY_FILE" <<SUMMARY_EOF
# SideGuy Weekly GSC Summary

**Date:** $HUMAN_DATE

---

## 📊 Cluster Analysis

$(tail -n +2 "$LATEST_CLUSTERS" | head -n 10 | while IFS=, read -r cluster queries impressions avg_pos top_query; do
  echo "- **$cluster:** $queries queries, $impressions impressions, avg position $avg_pos"
done)

---

## 🔥 Missing Page Opportunities

$(if [ "$MISSING_COUNT" -gt 0 ]; then
  tail -n +2 "$LATEST_MISSING" | head -n 10 | while IFS=, read -r page cluster intent geo reason; do
    echo "- **$page** (cluster: $cluster, intent: $intent)"
  done
else
  echo "No missing pages detected this week."
fi)

---

## 📁 Output Files

- Clusters: [\`${LATEST_CLUSTERS##*/}\`]($LATEST_CLUSTERS)
- Missing Pages: [\`${LATEST_MISSING##*/}\`]($LATEST_MISSING)
- Opportunities: [\`${LATEST_OPPS##*/}\`]($LATEST_OPPS)

---

## 🎯 Recommended Actions

1. **Review missing pages** — pick top 3-5 based on business priority
2. **Build high-intent pages** — focus on "decision" and "call" intent queries
3. **Monitor cluster movement** — compare to last week's analysis
4. **Update existing pages** — if clusters show declining performance

---

## Next Run

Schedule next analysis for: **$(date -d '+7 days' '+%Y-%m-%d')**

Download fresh GSC data 1-2 days before next run.

SUMMARY_EOF

echo "📝 Weekly summary generated: $SUMMARY_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

########################################
# STEP 5: FINAL OUTPUT
########################################

echo "========================================" | tee -a "$LOG_FILE"
echo "✅ WEEKLY AUTOPILOT COMPLETE" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "📁 Files generated:" | tee -a "$LOG_FILE"
echo "   - Weekly summary: $SUMMARY_FILE" | tee -a "$LOG_FILE"
echo "   - Full log: $LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "🎯 Next steps:" | tee -a "$LOG_FILE"

if [ "$MISSING_COUNT" -gt 0 ]; then
  echo "   1. Review missing pages: $LATEST_MISSING" | tee -a "$LOG_FILE"
  echo "   2. Pick top 3-5 opportunities based on:" | tee -a "$LOG_FILE"
  echo "      - Cluster strength (impressions)" | tee -a "$LOG_FILE"
  echo "      - Intent match (decision/call = higher value)" | tee -a "$LOG_FILE"
  echo "      - Business alignment" | tee -a "$LOG_FILE"
  echo "   3. Build pages using existing templates" | tee -a "$LOG_FILE"
else
  echo "   1. Monitor existing page performance" | tee -a "$LOG_FILE"
  echo "   2. Update underperforming pages" | tee -a "$LOG_FILE"
  echo "   3. Download fresh GSC data next week" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "🚀 SideGuy signal engine is running." | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

########################################
# OPTIONAL: COMMIT RESULTS TO GIT
########################################

# Uncomment to auto-commit results
# git add docs/cluster-intelligence/
# git commit -m "Weekly GSC autopilot: $HUMAN_DATE"
# echo "✅ Results committed to git" | tee -a "$LOG_FILE"

echo "Full log saved to: $LOG_FILE"
