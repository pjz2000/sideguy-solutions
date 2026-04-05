#!/bin/bash

echo "=== BUILDING COMPOUND INTELLIGENCE REPORT ==="

INPUT="data/compound/reuse-patterns.csv"
OUTPUT="docs/compound/compound-report.md"

if [ ! -f "$INPUT" ]; then
  echo "Missing reuse patterns."
  return 1 2>/dev/null || true
fi

TOTAL=$(tail -n +2 "$INPUT" | wc -l | tr -d ' ')

cat > "$OUTPUT" <<REPORT
# Compound Intelligence Report

Generated: $(date)

## Total Reusable Patterns
$TOTAL

## Highest Leverage Reuse Paths
- HVAC → home services
- payments → billing systems
- airport → human navigation
- betting → pricing intelligence
- local trust → all geo pages
- escalation → all client OS builds
REPORT

echo "Compound report written to $OUTPUT"
