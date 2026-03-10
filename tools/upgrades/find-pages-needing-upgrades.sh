#!/bin/bash

echo "SideGuy Page Upgrade Detector"
echo "------------------------------"

echo ""
echo "Pages missing FAQ schema:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'FAQPage' \
| wc -l

echo ""
echo "Pages missing command center links:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'command-center' \
| wc -l

echo ""
echo "Pages missing knowledge hub links:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'knowledge-hub' \
| wc -l

echo ""
echo "Possible thin pages (under 300 words):"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 -P4 awk '
  FNR==1 { words=0 }
  { gsub(/<[^>]+>/," "); words += NF }
  ENDFILE { if (words < 300) thin++ }
  END { print thin+0 }
' 2>/dev/null | awk '{s+=$1} END {print s+0}'

echo ""
echo "Upgrade scan complete."
