#!/bin/bash

echo "=== BUILDING SIDEGUY REASONING MAP ==="

INPUT="data/reasoning/reasoning-seeds.csv"
OUTPUT="docs/reasoning/reasoning-graph-report.md"

if [ ! -f "$INPUT" ]; then
  echo "Missing reasoning seeds."
  exit 1
fi

TOTAL=$(tail -n +2 "$INPUT" | wc -l | tr -d ' ')

cat > "$OUTPUT" <<REPORT
# Reasoning Graph Report

Generated: $(date)

## Total Relationships
$TOTAL

## Suggested Expansion Logic
- highest priority escalation nodes
- monetization bottlenecks
- missing calculator opportunities
- strongest white-label opportunities
- local trust gaps
- outbound nurture routes
- best new hub candidates
REPORT

echo "Reasoning graph report written to $OUTPUT"
