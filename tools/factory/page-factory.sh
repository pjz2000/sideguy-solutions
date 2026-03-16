#!/usr/bin/env bash

INPUT="$1"
TEMPLATE="tools/factory/page-template.html"

if [ -z "$INPUT" ]; then
echo "Usage:"
echo "bash tools/factory/page-factory.sh manifest.csv"
exit 0
fi

if [ ! -f "$INPUT" ]; then
echo "Manifest not found: $INPUT"
exit 0
fi

echo ""
echo "Running SideGuy Page Factory"
echo "Manifest: $INPUT"
echo ""

COUNT=0
CREATED=0
SKIPPED=0

tail -n +2 "$INPUT" | while IFS=',' read page_type slug title parent_hub vertical locality intent notes
do

COUNT=$((COUNT+1))

PAGE="pages/${slug}.html"

if [ -f "$PAGE" ]; then
SKIPPED=$((SKIPPED+1))
continue
fi

sed \
-e "s/{{TITLE}}/$title/g" \
-e "s/{{SLUG}}/$slug/g" \
-e "s/{{HUB}}/$parent_hub/g" \
"$TEMPLATE" > "$PAGE"

CREATED=$((CREATED+1))

echo "created $PAGE"

done

echo ""
echo "Factory complete."
echo ""
