#!/bin/bash

echo "====================================="
echo "SideGuy Auto Link Injector"
echo "====================================="

REPORT="reports/auto-link-injected.txt"
> "$REPORT"

FILES=$(find . -name "*.html")

for file in $FILES
do

slug=$(basename "$file" .html)
words=$(echo "$slug" | tr '-' ' ')

links=""

for other in $FILES
do
    other_slug=$(basename "$other" .html)

    if [ "$file" != "$other" ]; then
        match=$(echo "$other_slug" | grep -i "$words")

        if [ ! -z "$match" ]; then
            links="$links<li><a href=\"/$other_slug.html\">$other_slug</a></li>"
        fi
    fi
done

if [ ! -z "$links" ]; then

block="<h3>Related Topics</h3><ul>$links</ul>"

# inject before closing body
sed -i "/<\/body>/i $block" "$file"

echo "Updated $file" >> "$REPORT"

fi

done

echo ""
echo "Auto linking complete."
echo "Report:"
echo "$REPORT"
