#!/bin/bash

echo "Injecting decision blocks..."

FILES=$(find . -name "*.html")

for file in $FILES
do

if grep -Ei "cost|price|best|vs" "$file" > /dev/null
then

sed -i "/<\/body>/i \
<div style=\"background:#e8fff3;padding:20px;border-radius:12px;margin-top:40px;\">\
<h2>Need a Second Opinion?</h2>\
<p>If you're comparing options or unsure what to do next, send it over.</p>\
<p><strong>Text PJ: 773-544-1231</strong></p>\
<p>Clarity before cost.</p>\
</div>" "$file"

echo "Updated: $file"

fi

done

echo "Decision blocks injected."
