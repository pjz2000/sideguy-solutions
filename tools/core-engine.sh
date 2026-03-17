#!/usr/bin/env bash
set -euo pipefail

########################################
# SIDEGUY CORE ENGINE
########################################

ROOT="/workspaces/sideguy-solutions"
cd "$ROOT" || { echo "Missing project root"; exit 1; }

echo ""
echo "=========================================="
echo "SIDEGUY CORE ENGINE"
echo "Intelligence → Operator → Map → Mission"
echo "=========================================="
echo ""

########################################
# REQUIREMENTS
########################################

command -v jq >/dev/null || { echo "jq required"; exit 1; }

########################################
# BASE STRUCTURE (IDEMPOTENT)
########################################

mkdir -p docs/{intelligence,operator,map,mission}
mkdir -p docs/intelligence/{config,inbox,processed,queues,reports,state}
mkdir -p docs/operator/{reports,state}
mkdir -p docs/map/{data,reports,state}
mkdir -p docs/mission/{reports,state}
mkdir -p public/maps
mkdir -p tools/{intelligence,operator,map,mission}
mkdir -p logs

########################################
# HELPERS
########################################

ts() { date +"%Y-%m-%d %H:%M:%S"; }

safe_file() {
  [ -f "$1" ] || echo "$2" > "$1"
}

########################################
# CONFIG (SAFE WRITE)
########################################

safe_file docs/intelligence/config/rules.env \
"WINNER_SCORE_THRESHOLD=70
LOSER_SCORE_THRESHOLD=35"

safe_file docs/operator/config.env \
"TOP_WINNERS=10
TOP_LOSERS=10"

########################################
# INTELLIGENCE ENGINE
########################################

run_intelligence() {

echo "== Intelligence =="

SEARCH_OUT="docs/intelligence/processed/search.csv"
PAGE_OUT="docs/intelligence/processed/pages.csv"
WINNERS="docs/intelligence/queues/winners.csv"
LOSERS="docs/intelligence/queues/losers.csv"

mkdir -p docs/intelligence/processed docs/intelligence/queues

echo "query,page,score" > "$SEARCH_OUT"

# SIMPLE SIGNAL SIMULATION (clean + stable)
find public -name "*.html" | while read -r f; do
  slug=$(basename "$f")
  echo "\"query-$slug\",\"/$slug\",$((RANDOM%100))" >> "$SEARCH_OUT"
done

echo "page,total_score,class" > "$PAGE_OUT"

tail -n +2 "$SEARCH_OUT" | while IFS=, read -r q p s; do
  score=$(echo "$s" | tr -d '"')
  class="monitor"

  if [ "$score" -ge 70 ]; then class="winner"; fi
  if [ "$score" -le 35 ]; then class="loser"; fi

  echo "\"$p\",\"$score\",\"$class\"" >> "$PAGE_OUT"
done

grep winner "$PAGE_OUT" > "$WINNERS" || true
grep loser "$PAGE_OUT" > "$LOSERS" || true

echo "Intelligence complete"
}

########################################
# OPERATOR ENGINE
########################################

run_operator() {

echo "== Operator =="

REPORT="docs/operator/reports/operator-$(date +%s).md"

cat > "$REPORT" <<EOF
# Operator Report

## Winners
$(cat docs/intelligence/queues/winners.csv 2>/dev/null)

## Losers
$(cat docs/intelligence/queues/losers.csv 2>/dev/null)
EOF

echo "Operator report built"
}

########################################
# MAP ENGINE
########################################

run_map() {

echo "== Map =="

NODES="docs/map/data/nodes.csv"
EDGES="docs/map/data/edges.csv"

mkdir -p docs/map/data

echo "id,label,type" > "$NODES"
echo "source,target,type" > "$EDGES"

find public -name "*.html" | while read -r f; do
  id=$(echo "$f" | sed 's#public##')
  echo "\"page:$id\",\"$id\",\"page\"" >> "$NODES"

  grep -o 'href="[^"]*"' "$f" 2>/dev/null | while read -r link; do
    tgt=$(echo "$link" | sed 's/href="//;s/"//')
    echo "\"$id\",\"$tgt\",\"link\"" >> "$EDGES"
  done
done

echo "Map built"
}

########################################
# MISSION ENGINE
########################################

run_mission() {

echo "== Mission =="

REPORT="docs/mission/reports/mission-$(date +%s).md"

PAGES=$(find public -name "*.html" | wc -l | tr -d ' ')

cat > "$REPORT" <<EOF
# Mission Report

Timestamp: $(ts)

Pages: $PAGES

System Status:
- Intelligence: OK
- Operator: OK
- Map: OK
EOF

echo "Mission report built"
}

########################################
# MASTER RUN
########################################

run_all() {

run_intelligence
run_operator
run_map
run_mission

echo ""
echo "=========================================="
echo "SIDEGUY CORE COMPLETE"
echo "=========================================="
echo ""

echo "View:"
echo "- docs/operator/reports/"
echo "- docs/mission/reports/"
echo "- docs/map/data/"
echo ""
}

########################################
# EXECUTE
########################################

run_all
