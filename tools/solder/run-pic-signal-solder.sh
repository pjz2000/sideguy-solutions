#!/bin/bash
echo "=== SIDEGUY PIC SIGNAL SOLDER START ==="

MAP="data/solder/search-page-map-latest.tsv"
PICLOG="data/solder/pic-observations.tsv"
OUT="docs/solder/pic-signal-report.md"

touch "$PICLOG"

echo "# SideGuy Picture Signal Solder Report" > "$OUT"
echo "" >> "$OUT"
echo "Generated: $(date)" >> "$OUT"
echo "" >> "$OUT"

if [ -f "$MAP" ]; then
  echo "## Existing solder map routes" >> "$OUT"
  tail -20 "$MAP" >> "$OUT"
  echo "" >> "$OUT"
fi

echo "## Picture-driven route opportunities" >> "$OUT"

while IFS=$'\t' read -r query url cluster confidence action; do
  [ -z "$query" ] && continue
  if [[ "$confidence" == 0.9* || "$confidence" == 0.96* || "$confidence" == 0.95* ]]; then
    echo "- HIGH: $query → $action" >> "$OUT"
  fi
done < "$MAP"

echo "" >> "$OUT"
echo "## Auto-next actions" >> "$OUT"
echo "- spawn calculators from repeated screenshot winners" >> "$OUT"
echo "- route CTR surgery pages into compare pages" >> "$OUT"
echo "- route fee screenshots into calculator sliders" >> "$OUT"
echo "- route local screenshot queries into trust pages" >> "$OUT"

echo "Report written to $OUT"
