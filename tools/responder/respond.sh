#!/bin/bash

INPUT="logs/responder/classified.txt"
OUT="logs/responder/outbox.txt"

> "$OUT"

while IFS="|" read intent msg
do

response=""

if echo "$intent" | grep -q "pricing"; then
response="Got it — pricing can vary a lot depending on setup. Usually worth double-checking before committing. If you want, send details and I can sanity check it."
fi

if echo "$intent" | grep -q "decision"; then
response="Good question — this usually comes down to your specific setup and goals. I can break it down simply if you want."
fi

if echo "$intent" | grep -q "problem"; then
response="That sounds frustrating — usually there's a root cause that's not obvious at first. Happy to take a look if you want a second opinion."
fi

if echo "$intent" | grep -q "general"; then
response="Happy to help — what are you trying to figure out exactly?"
fi

final="$response Text PJ 773-544-1231 if you want a quick answer."

echo "$final" >> "$OUT"

done < "$INPUT"

echo "Responses ready → $OUT"
