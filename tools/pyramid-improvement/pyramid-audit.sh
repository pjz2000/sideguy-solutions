#!/usr/bin/env bash

echo ""
echo "SideGuy Pyramid Audit"
echo "---------------------"

find . -name "*.html" | while read page
do

links=$(grep -o "<a " "$page" | wc -l)
words=$(wc -w < "$page")

echo "$page | links:$links | words:$words"

done
