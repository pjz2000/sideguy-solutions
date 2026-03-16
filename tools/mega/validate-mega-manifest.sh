#!/usr/bin/env bash

FILE="manifests/mega/million-engine.csv"

if [ ! -f "$FILE" ]; then
echo "Manifest not found."
exit 0
fi

echo "Validating manifest..."

tail -n +2 "$FILE" | while IFS=',' read type slug title vertical parent
do

if [ -z "$slug" ]; then
echo "WARNING empty slug"
fi

if [[ "$slug" =~ [A-Z] ]]; then
echo "WARNING uppercase slug: $slug"
fi

done

echo "Validation complete."
