#!/bin/bash

INPUT="logs/responder/inbox.txt"
OUT="logs/responder/classified.txt"

> "$OUT"

while read line
do

intent="general"

if echo "$line" | grep -Ei "cost|price|quote" > /dev/null; then
intent="pricing"
fi

if echo "$line" | grep -Ei "best|vs|compare" > /dev/null; then
intent="decision"
fi

if echo "$line" | grep -Ei "broken|not working|issue" > /dev/null; then
intent="problem"
fi

echo "$intent | $line" >> "$OUT"

done < "$INPUT"

echo "Classified."
