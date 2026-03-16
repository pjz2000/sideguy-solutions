#!/bin/bash

SIGNALS="signals/tech-signals.txt"
MODIFIERS="manifests/future/future-modifiers.txt"
OUT="manifests/future/future-topic-queue.csv"

echo "slug,title" > "$OUT"

while read signal
do

while read mod
do

slug="$signal-$mod"
title="$signal $mod"

echo "$slug,$title" >> "$OUT"

done < "$MODIFIERS"

done < "$SIGNALS"

echo "Future topic queue created."
