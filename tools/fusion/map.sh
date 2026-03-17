#!/usr/bin/env bash
# Maps high-value leads to deal categories

INPUT="logs/responder/high-value.txt"
OUTPUT="docs/fusion/deal-map.txt"

if [ ! -f "$INPUT" ]; then
  echo "No high-value leads at $INPUT — run high-value.sh first"
  exit 0
fi

{ echo "--- Deal Map: $(date) ---"; } > "$OUTPUT"

while IFS= read -r line; do
  if   echo "$line" | grep -qiE "hvac|ac|heat|furnace|cooling";  then echo "$line → HVAC DEAL"     >> "$OUTPUT"
  elif echo "$line" | grep -qiE "solar|panel|battery|powerwall"; then echo "$line → SOLAR DEAL"    >> "$OUTPUT"
  elif echo "$line" | grep -qiE "roof|shingle|leak|gutter";      then echo "$line → ROOFING DEAL"  >> "$OUTPUT"
  elif echo "$line" | grep -qiE "plumb|pipe|drain|toilet|water"; then echo "$line → PLUMBING DEAL" >> "$OUTPUT"
  elif echo "$line" | grep -qiE "tesla|ev|charger|electric car"; then echo "$line → EV DEAL"       >> "$OUTPUT"
  elif echo "$line" | grep -qiE "payment|stripe|charge|invoice"; then echo "$line → PAYMENTS DEAL" >> "$OUTPUT"
  else                                                                 echo "$line → GENERAL"        >> "$OUTPUT"
  fi
done < "$INPUT"

echo "Deal map written → $OUTPUT"
