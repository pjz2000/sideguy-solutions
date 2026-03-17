#!/bin/bash

echo "Running SideGuy Link Booster"

TARGET_DIR="factory"
LOG="docs/booster/link-booster-log.txt"

echo "Link Booster Run $(date)" > $LOG
echo "" >> $LOG

# Get top authority pages from opportunity engine
TOP="docs/opportunity/top-opportunities.txt"

if [ ! -f "$TOP" ]; then
  echo "Run opportunity engine first."
  exit
fi

# Get factory pages
FACTORY_PAGES=$(find . -type f -path "*factory*.html" | head -50)

while read line
do

PAGE=$(echo "$line" | awk -F '|' '{print $2}' | xargs)

if [ -f "$PAGE" ]; then

echo "Boosting from $PAGE" >> $LOG

BLOCK="<div style='margin:30px 0;padding:16px;border-radius:12px;background:#0f172a;color:white;'>
<h3>Related Guides</h3><ul>"

for TARGET in $FACTORY_PAGES
do
SLUG=$(basename $TARGET)
BLOCK="$BLOCK<li><a href=\"$SLUG\" style='color:#38bdf8;'>$SLUG</a></li>"
done

BLOCK="$BLOCK</ul></div>"

sed -i "s#</body>#$BLOCK</body>#" "$PAGE"

fi

done < "$TOP"

echo ""
echo "Link boosting complete."
echo "Log:"
echo $LOG
