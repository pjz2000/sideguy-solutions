#!/usr/bin/env bash

########################################
# SIDEGUY CLUSTER INTELLIGENCE DRIVER v1
# combine GSC → run intelligence → preview outputs
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
DATA_DIR="$PROJECT_ROOT/docs/gsc"
OUT_DIR="$PROJECT_ROOT/docs/cluster-intelligence"
DATE="$(date +"%Y-%m-%d-%H%M%S")"

cd "$PROJECT_ROOT" || exit

mkdir -p "$DATA_DIR" "$OUT_DIR"

########################################
# INPUT FILES
########################################

PAGES_FILE="$DATA_DIR/gsc_pages.csv"
QUERIES_FILE="$DATA_DIR/gsc_queries.csv"
COMBINED_FILE="$DATA_DIR/query-pages.csv"

########################################
# PRECHECK
########################################

echo "---------------------------------------"
echo "🧠 CLUSTER INTELLIGENCE DRIVER"
echo "---------------------------------------"
echo "Project: $PROJECT_ROOT"
echo "Date:    $DATE"
echo ""

if [ ! -f "$PAGES_FILE" ]; then
  echo "❌ Missing: $PAGES_FILE"
  exit 1
fi

if [ ! -f "$QUERIES_FILE" ]; then
  echo "❌ Missing: $QUERIES_FILE"
  exit 1
fi

########################################
# COMBINE FILES → query-pages.csv
# Expected columns:
# page,query,clicks,impressions,ctr,position
########################################

echo "🔧 Combining GSC files → query-pages.csv..."

# GSC exports have different structures:
# Pages: "Top pages","Clicks","Impressions","CTR","Position"
# Queries: "Top queries","Clicks","Impressions","CTR","Position"
# We need to merge them into: page,query,clicks,impressions,ctr,position

echo "page,query,clicks,impressions,ctr,position" > "$COMBINED_FILE"

# Read queries file and extract data
# Skip header, clean quotes, convert CTR % to decimal
tail -n +2 "$QUERIES_FILE" | while IFS=',' read -r query clicks impressions ctr position rest; do
  # Clean quotes
  query=$(echo "$query" | sed 's/"//g')
  clicks=$(echo "$clicks" | sed 's/"//g')
  impressions=$(echo "$impressions" | sed 's/"//g')
  ctr=$(echo "$ctr" | sed 's/"//g' | sed 's/%//g')
  position=$(echo "$position" | sed 's/"//g')
  
  # Find matching page from pages file (if exists)
  page=""
  # For now, use the query as the page identifier since we don't have perfect mapping
  # This is a limitation of having separate files
  
  # Convert CTR from percentage to decimal (if it's a number)
  if [[ "$ctr" =~ ^[0-9.]+$ ]]; then
    ctr=$(awk "BEGIN {printf \"%.4f\", $ctr/100}")
  else
    ctr="0"
  fi
  
  # Default: assume page doesn't exist yet (this is what we want to detect)
  page="$query"
  
  # Write cleaned row
  echo "$page,$query,$clicks,$impressions,$ctr,$position" >> "$COMBINED_FILE"
done

echo "✅ Combined file created:"
echo "   $COMBINED_FILE"
echo ""

########################################
# RUN CLUSTER INTELLIGENCE
########################################

if [ ! -f "$PROJECT_ROOT/_cluster_intelligence.sh" ]; then
  echo "❌ Missing script: _cluster_intelligence.sh"
  echo "Make sure it's in project root"
  exit 1
fi

echo "🚀 Running cluster intelligence..."

bash "$PROJECT_ROOT/_cluster_intelligence.sh"

echo ""
echo "✅ Cluster intelligence complete"
echo ""

########################################
# FIND OUTPUT FILES
########################################

echo "📂 Searching outputs..."

CLUSTER_DIR=$(find "$PROJECT_ROOT/docs" -type d -name "cluster-intelligence" | head -n 1)

if [ -z "$CLUSTER_DIR" ]; then
  echo "⚠️ Could not locate cluster-intelligence output folder"
else
  echo "📁 Output folder:"
  echo "   $CLUSTER_DIR"
  echo ""
fi

########################################
# PREVIEW: MISSING PAGES (KEY FILE)
########################################

MISSING_FILE=$(find "$PROJECT_ROOT/docs" -name "missing-pages-*.csv" | sort | tail -n 1)

if [ -n "$MISSING_FILE" ]; then
  echo "🔥 TOP MISSING PAGE OPPORTUNITIES:"
  echo "---------------------------------------"

  head -n 20 "$MISSING_FILE"

  echo ""
  echo "Full file:"
  echo "  $MISSING_FILE"
else
  echo "⚠️ No missing-pages file found yet"
fi

########################################
# CLEANUP
########################################

# Temp files are no longer used in current version

########################################
# FINISH
########################################

echo ""
echo "---------------------------------------"
echo "🧠 DRIVER COMPLETE"
echo "---------------------------------------"
echo ""
echo "Next move:"
echo "1. Open missing-pages CSV"
echo "2. Pick top 10–20"
echo "3. Build pages from REAL demand"
echo ""
echo "This = SideGuy signal engine activated 🚀"
echo ""
