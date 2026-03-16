#!/usr/bin/env bash

ROOT="${1:-.}"
STAMP=$(date "+%Y-%m-%d %H:%M:%S")

REPORT="logs/command-center/command-center-report.txt"

mkdir -p logs/command-center

echo "SideGuy Command Center Report" > "$REPORT"
echo "Generated: $STAMP" >> "$REPORT"
echo >> "$REPORT"


echo "====================================" >> "$REPORT"
echo "1. SIGNAL SCAN (Future Opportunities)" >> "$REPORT"
echo "====================================" >> "$REPORT"
echo >> "$REPORT"

if [ -f tools/intelligence/signal-engine.sh ]; then
  bash tools/intelligence/signal-engine.sh "$ROOT" >> "$REPORT" 2>&1
else
  echo "Signal engine not installed." >> "$REPORT"
fi


echo >> "$REPORT"
echo "====================================" >> "$REPORT"
echo "2. AUTHORITY FLYWHEEL SCAN" >> "$REPORT"
echo "====================================" >> "$REPORT"
echo >> "$REPORT"

if [ -f tools/intelligence/flywheel-engine.sh ]; then
  bash tools/intelligence/flywheel-engine.sh "$ROOT" >> "$REPORT" 2>&1
else
  echo "Flywheel engine not installed." >> "$REPORT"
fi


echo >> "$REPORT"
echo "====================================" >> "$REPORT"
echo "3. PAGE PRIORITY SCAN" >> "$REPORT"
echo "====================================" >> "$REPORT"
echo >> "$REPORT"

if [ -f tools/intelligence/priority-engine.sh ]; then
  bash tools/intelligence/priority-engine.sh "$ROOT" >> "$REPORT" 2>&1
else
  echo "Priority engine not installed." >> "$REPORT"
fi


echo >> "$REPORT"
echo "====================================" >> "$REPORT"
echo "4. SITE METRICS" >> "$REPORT"
echo "====================================" >> "$REPORT"
echo >> "$REPORT"

pages=$(find "$ROOT" -maxdepth 1 -type f -name "*.html" | wc -l | tr -d ' ')

echo "Total HTML pages: $pages" >> "$REPORT"

links=$(find "$ROOT" -maxdepth 1 -name "*.html" -exec grep -oh 'href="[^"]*\.html"' {} \; 2>/dev/null | wc -l | tr -d ' ')
echo "Total internal links: $links" >> "$REPORT"

avg_links=$(echo "$links $pages" | awk '{ if ($2>0) printf "%.2f", $1/$2; else print "0" }')
echo "Average links per page: $avg_links" >> "$REPORT"


echo >> "$REPORT"
echo "====================================" >> "$REPORT"
echo "NEXT OPERATOR ACTIONS" >> "$REPORT"
echo "====================================" >> "$REPORT"
echo >> "$REPORT"

echo "1. Build 1-3 new pages from signal engine." >> "$REPORT"
echo "2. Strengthen weak pages from flywheel scan." >> "$REPORT"
echo "3. Expand clusters around dominant topics." >> "$REPORT"
echo "4. Improve internal linking density." >> "$REPORT"


echo
echo "SideGuy Command Center Report Generated"
echo
echo "Open:"
echo "$REPORT"
