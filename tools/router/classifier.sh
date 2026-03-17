#!/bin/bash

INPUT="logs/router/raw-leads.txt"
OUT="logs/router/classified-leads.txt"

> "$OUT"

while read line
do

category="general"

if echo "$line" | grep -Ei "hvac|ac|air" > /dev/null; then
category="hvac"
fi

if echo "$line" | grep -Ei "solar|battery|ev" > /dev/null; then
category="energy"
fi

if echo "$line" | grep -Ei "stripe|payment|fees" > /dev/null; then
category="payments"
fi

if echo "$line" | grep -Ei "ai|automation" > /dev/null; then
category="ai"
fi

echo "$category | $line" >> "$OUT"

done < "$INPUT"

echo "Classified leads → $OUT"
