#!/bin/bash

TECH="signals/tech-signals.txt"
BUSINESS="signals/business-signals.txt"
OUT="logs/future-radar.txt"

echo "SideGuy Future Radar Scan" > "$OUT"
echo "" >> "$OUT"

echo "Tech Signals:" >> "$OUT"
cat "$TECH" >> "$OUT"

echo "" >> "$OUT"

echo "Business Signals:" >> "$OUT"
cat "$BUSINESS" >> "$OUT"

echo ""
echo "Future radar complete."
