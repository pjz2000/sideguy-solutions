#!/bin/bash

FILE="logs/router/routed-leads.txt"

echo ""
echo "SideGuy Deal Dashboard"
echo "----------------------"

if [ ! -f "$FILE" ]; then
echo "No leads yet."
exit
fi

echo ""
cat "$FILE"

echo ""
echo "Counts:"
cut -d'→' -f2 "$FILE" | sort | uniq -c
