#!/bin/bash

echo "SideGuy Money Page Detector"

FILES=$(find . -name "*.html")

for file in $FILES
do

if grep -Ei "cost|price|best|vs|repair|quote" "$file" > /dev/null
then
echo "💰 High Intent: $file"
fi

done
