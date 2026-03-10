#!/bin/bash

# =========================================
# SIDEGUY — WEAK PAGE DETECTOR
# =========================================
# Run: ./tools/health/weak-page-detector.sh
# Read-only. Outputs counts only.
# =========================================

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

echo "SideGuy Weak Page Detector"
echo "--------------------------"
echo "Root: $ROOT"
echo ""

echo "1. Pages missing meta description"
grep -rL 'name="description"' --include="*.html" --max-depth=1 . | wc -l

echo ""
echo "2. Pages missing H1"
grep -rL '<h1' --include="*.html" --max-depth=1 . | wc -l

echo ""
echo "3. Pages missing canonical tag"
grep -rL 'rel="canonical"' --include="*.html" --max-depth=1 . | wc -l

echo ""
echo "4. Pages missing OG title"
grep -rL 'og:title' --include="*.html" --max-depth=1 . | wc -l

echo ""
echo "5. Pages missing Text PJ contact"
grep -rL '773-544-1231' --include="*.html" --max-depth=1 . | wc -l

echo ""
echo "6. Possible thin pages (under 300 words)"
# Fast: use awk to strip tags and count words in one pass per file
find . -maxdepth 1 -name "*.html" -print0 \
  | xargs -0 -P4 awk '
    BEGIN { thin=0 }
    FNR==1 { words=0; file=FILENAME }
    { gsub(/<[^>]+>/," "); words += NF }
    ENDFILE { if (words < 300) thin++ }
    END { print thin }
  ' 2>/dev/null | awk '{s+=$1} END {print s}'

echo ""
echo "7. Pages not in sitemap.xml"
# Fast: extract filenames from sitemap, compare against actual files
if [ -f sitemap.xml ]; then
  IN_SITEMAP=$(grep -oP '(?<=<loc>)[^<]+' sitemap.xml | grep -oP '[^/]+\.html$' | sort -u)
  find . -maxdepth 1 -name "*.html" -printf "%f\n" | sort -u \
    | comm -23 - <(echo "$IN_SITEMAP") \
    | wc -l
else
  echo "  (sitemap.xml not found — skipping)"
fi

echo ""
echo "8. Pages newer than sitemap"
find . -maxdepth 1 -name "*.html" -newer sitemap.xml | wc -l

echo ""
echo "Health check complete."
