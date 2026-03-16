#!/usr/bin/env bash

FILE="$1"

if [ ! -f "$FILE" ]; then
echo "Manifest missing"
exit 0
fi

echo "Validating manifest..."

tail -n +2 "$FILE" | while IFS=',' read type slug title parent vertical locality intent notes
do

if [ -z "$slug" ] || [ -z "$title" ]; then
echo "WARNING missing fields: $slug"
fi

if [[ "$slug" =~ [A-Z] ]]; then
echo "WARNING uppercase slug: $slug"
fi

done

echo "Validation complete."
