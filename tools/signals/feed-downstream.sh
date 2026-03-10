#!/usr/bin/env bash

# =========================================
# STAGE 4: DOWNSTREAM FEEDER
# Routes page ideas into:
#   - trend radar signals
#   - problem engine ideas
#   - lattice child topics
# =========================================

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
IDEAS="$ROOT/docs/signals/page-ideas.txt"
TREND_SIGNALS="$ROOT/docs/trend-radar/trend-signals.txt"
PROBLEM_IDEAS="$ROOT/docs/problem-engine/problem-page-ideas.txt"
LATTICE_CHILDREN="$ROOT/docs/manifests/lattice/child-topics.txt"

if [ ! -f "$IDEAS" ]; then
  echo "Missing: $IDEAS — run generate-page-ideas.sh first"
  exit 1
fi

mkdir -p "$ROOT/docs/trend-radar" "$ROOT/docs/problem-engine" "$ROOT/docs/manifests/lattice"

echo ""
echo "Stage 4: Feeding downstream tools..."

# Feed trend radar: bucket names as emerging topics
echo "" >> "$TREND_SIGNALS"
echo "---- Signal Pipeline Import $(date) ----" >> "$TREND_SIGNALS"
awk -F'|' 'NR>0 {print $2}' "$IDEAS" | tr -d ' ' | sort -u | while read -r bucket; do
  [ -z "$bucket" ] && continue
  echo "$bucket" >> "$TREND_SIGNALS"
done

tr_added=$(sort -u "$TREND_SIGNALS" | wc -l)
echo "  → trend-signals.txt updated"

# Feed problem engine: core + cost page ideas
echo "" >> "$PROBLEM_IDEAS"
echo "# Signal pipeline import $(date)" >> "$PROBLEM_IDEAS"
grep '| core\|| cost' "$IDEAS" | awk -F'|' '{print $1}' | tr -d ' ' >> "$PROBLEM_IDEAS"

prob_added=$(grep -v '^#\|^$' "$PROBLEM_IDEAS" | wc -l)
echo "  → problem-page-ideas.txt updated ($prob_added total entries)"

# Feed lattice: extract short human-readable topic names from signal buckets
# Only adds clean 2-4 word topic names, NOT full slugs
echo "" >> "$LATTICE_CHILDREN"
echo "# Signal pipeline import $(date)" >> "$LATTICE_CHILDREN"
awk -F'|' 'NR>0 {print $2}' "$IDEAS" \
  | tr -d ' ' \
  | sort -u \
  | sed 's/-/ /g' \
  | grep -v '^\s*$' \
  >> "$LATTICE_CHILDREN"

echo "  → lattice/child-topics.txt updated (bucket names only)"
echo ""
echo "Stage 4: Downstream feeds complete."
