#!/usr/bin/env bash

INPUT="${1:-manifests/wiki/wiki-queue.csv}"
CHUNK="${2:-250}"
OUT_DIR="${3:-manifests/wiki/chunks}"

mkdir -p "$OUT_DIR"

HEADER=$(head -n 1 "$INPUT")

tail -n +2 "$INPUT" | split -l "$CHUNK" - "$OUT_DIR/wiki_chunk_"

for f in "$OUT_DIR"/wiki_chunk_*
do
TMP="$f.csv"

{
echo "$HEADER"
cat "$f"
} > "$TMP"

rm "$f"

done

echo "Queue split complete"
