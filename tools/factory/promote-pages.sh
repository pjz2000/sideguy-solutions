#!/bin/bash

SOURCE="pages/factory"
DEST="."
SITEMAP="sitemap.xml"

DATE=$(date +"%Y-%m-%d")
STAMP=$(date +"%Y-%m-%d %H:%M:%S")

LOG="logs/promotion/promote-$DATE.log"
REPORT="reports/promotion/promote-$DATE.md"

mkdir -p logs/promotion reports/promotion

echo "" >> "$LOG"
echo "=== SideGuy Promotion Run $STAMP ===" >> "$LOG"
echo "" >> "$LOG"

promoted=0
skipped=0

for page in "$SOURCE"/*.html
do
  slug=$(basename "$page")
  DESTFILE="$DEST/$slug"

  if [ -f "$DESTFILE" ]; then
    echo "SKIP existing: $slug" >> "$LOG"
    skipped=$((skipped+1))
    continue
  fi

  words=$(sed 's/<[^>]*>//g' "$page" | wc -w)

  if [ "$words" -lt 500 ]; then
    echo "SKIP thin page: $slug ($words words)" >> "$LOG"
    skipped=$((skipped+1))
    continue
  fi

  cp "$page" "$DESTFILE"
  echo "PROMOTED: $slug" >> "$LOG"
  promoted=$((promoted+1))

  if [ -f "$SITEMAP" ]; then
    sed -i "/<\/urlset>/i <url><loc>https://sideguysolutions.com/$slug</loc></url>" "$SITEMAP"
  fi
done

cat > "$REPORT" <<EOF2
# SideGuy Promotion Report

## Timestamp
$STAMP

## Source
$SOURCE

## Destination
$DEST

## Promoted Pages
$promoted

## Skipped Pages
$skipped

## Notes

Pages are promoted only if:

- page does not already exist
- word count >= 500

Promotion automatically:

- copies page to live root
- adds sitemap entry (if sitemap exists)

Recommended follow-up:

1. run publish gate
2. run flywheel engine
3. add internal links
4. strengthen hubs
EOF2

echo ""
echo "======================================"
echo "SIDEGUY PROMOTION COMPLETE"
echo "======================================"
echo ""
echo "Promoted: $promoted"
echo "Skipped:  $skipped"
echo ""
echo "Log:      $LOG"
echo "Report:   $REPORT"
