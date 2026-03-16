#!/bin/bash

INPUT="manifests/future/future-topic-queue.csv"
OUT="logs/future-clusters.txt"

echo "Future Cluster Map" > "$OUT"

tail -n +2 "$INPUT" | while IFS=',' read slug title
do
echo "future-page: $slug" >> "$OUT"
done

echo "Future clusters mapped."
