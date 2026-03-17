#!/bin/bash

INPUT="logs/router/classified-leads.txt"
OUT="logs/router/routed-leads.txt"

> "$OUT"

while IFS="|" read category lead
do

destination="PJ"

if echo "$category" | grep -q "hvac"; then
destination="HVAC_PARTNER"
fi

if echo "$category" | grep -q "energy"; then
destination="ENERGY_PARTNER"
fi

if echo "$category" | grep -q "payments"; then
destination="PAYMENTS_SETUP"
fi

if echo "$category" | grep -q "ai"; then
destination="AI_GUIDANCE"
fi

echo "$category → $destination → $lead" >> "$OUT"

done < "$INPUT"

echo "Routing complete → $OUT"
