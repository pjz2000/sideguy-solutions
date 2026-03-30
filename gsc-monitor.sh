#!/usr/bin/env bash

########################################
# SIDEGUY GSC MONITOR
# Check GSC data freshness & alert
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

DATE="$(date +"%Y-%m-%d %H:%M:%S")"

echo "=========================================="
echo "📊 SIDEGUY GSC DATA MONITOR"
echo "=========================================="
echo "Check time: $DATE"
echo ""

########################################
# DATA LOCATIONS
########################################

# Primary GSC data sources
GSC_QUERIES="$PROJECT_ROOT/docs/gsc/gsc_queries.csv"
GSC_PAGES="$PROJECT_ROOT/docs/gsc/gsc_pages.csv"

# Alternative data location (manual exports)
DATA_GSC="$PROJECT_ROOT/data/gsc.csv"
DATA_GSC_EXPORT="$PROJECT_ROOT/data/gsc-export.csv"

########################################
# CHECK FRESHNESS
########################################

check_file_freshness() {
  local file=$1
  local label=$2
  
  if [ ! -f "$file" ]; then
    echo "❌ $label: NOT FOUND"
    return 1
  fi
  
  # Get file modification time
  local mod_time=$(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file" 2>/dev/null)
  local now=$(date +%s)
  local age_seconds=$((now - mod_time))
  local age_days=$((age_seconds / 86400))
  local age_hours=$(((age_seconds % 86400) / 3600))
  
  # File date
  local file_date=$(date -r "$file" "+%Y-%m-%d %H:%M" 2>/dev/null || date -j -r "$file" "+%Y-%m-%d %H:%M" 2>/dev/null)
  
  # Color-coded status
  if [ $age_days -eq 0 ]; then
    echo "✅ $label: TODAY ($file_date) — ${age_hours}h old"
  elif [ $age_days -le 3 ]; then
    echo "🟢 $label: ${age_days} days old ($file_date)"
  elif [ $age_days -le 7 ]; then
    echo "🟡 $label: ${age_days} days old ($file_date) — Consider updating"
  else
    echo "🔴 $label: ${age_days} days old ($file_date) — UPDATE NEEDED"
  fi
  
  return 0
}

echo "📂 Checking data locations..."
echo ""

# Check all data sources
check_file_freshness "$GSC_QUERIES" "GSC Queries (docs/gsc)"
check_file_freshness "$GSC_PAGES" "GSC Pages (docs/gsc)"
check_file_freshness "$DATA_GSC" "GSC Export (data/gsc.csv)"
check_file_freshness "$DATA_GSC_EXPORT" "GSC Export (data/gsc-export.csv)"

echo ""
echo "=========================================="

########################################
# SHOW TOP QUERIES (If Available)
########################################

if [ -f "$DATA_GSC_EXPORT" ]; then
  echo "🔍 TOP 5 PERFORMING PAGES (Last Export):"
  echo ""
  
  # Show top 5 pages by clicks
  head -6 "$DATA_GSC_EXPORT" | tail -5 | awk -F',' '{
    sub(/^https:\/\/[^\/]+\//, "", $1);
    printf "  • %s\n    %s clicks, %s impressions (pos %.1f)\n\n", $1, $3, $4, $6
  }'
  
  echo "=========================================="
fi

########################################
# RECOMMENDATIONS
########################################

echo ""
echo "💡 WHAT TO DO NEXT:"
echo ""

# Count files older than 7 days
old_count=0
[ -f "$GSC_QUERIES" ] && [ $(find "$GSC_QUERIES" -mtime +7 2>/dev/null | wc -l) -gt 0 ] && ((old_count++))
[ -f "$GSC_PAGES" ] && [ $(find "$GSC_PAGES" -mtime +7 2>/dev/null | wc -l) -gt 0 ] && ((old_count++))

if [ $old_count -gt 0 ]; then
  echo "⚠️  Data is stale. Update GSC data:"
  echo ""
  echo "   1. Open: https://search.google.com/search-console"
  echo "   2. Performance > Queries > Export"
  echo "   3. Save as: docs/gsc/gsc_queries.csv"
  echo "   4. Performance > Pages > Export"
  echo "   5. Save as: docs/gsc/gsc_pages.csv"
  echo ""
  echo "   Then run: ./weekly-gsc-autopilot.sh"
else
  echo "✅ Data looks fresh!"
  echo ""
  echo "   • Run cluster analysis: ./weekly-gsc-autopilot.sh"
  echo "   • Review top queries: cat data/gsc-export.csv | head -20"
  echo "   • Check zero-click keywords for optimization"
fi

echo ""
echo "=========================================="
echo "📅 Next recommended update: $(date -d '+7 days' '+%A, %B %d' 2>/dev/null || date -v+7d '+%A, %B %d' 2>/dev/null)"
echo "=========================================="
