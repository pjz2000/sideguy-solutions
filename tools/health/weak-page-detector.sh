#!/bin/bash

echo "SideGuy Weak Page Detector"
echo "--------------------------"

echo ""
echo "1. Pages missing meta description"
grep -rL 'name="description"' --include="*.html" . | wc -l

echo ""
echo "2. Pages missing H1"
grep -rL '<h1' --include="*.html" . | wc -l

echo ""
echo "3. Pages missing canonical tag"
grep -rL 'rel="canonical"' --include="*.html" . | wc -l

echo ""
echo "4. Pages missing OG title"
grep -rL 'og:title' --include="*.html" . | wc -l

echo ""
echo "5. Pages missing Text PJ orb"
grep -rL '773-544-1231' --include="*.html" . | wc -l

echo ""
echo "6. Possible thin pages (under 300 words)"
for f in *.html; do
  words=$(tr -d '<[^>]*>' < "$f" | wc -w)
  if [ "$words" -lt 300 ]; then
    echo "$f"
  fi
done | wc -l

echo ""
echo "7. Pages not linked from homepage"
for f in *.html; do
  name=$(basename "$f")
  grep -q "$name" index.html || echo "$name"
done | wc -l

echo ""
echo "8. Pages newer than sitemap"
find . -maxdepth 1 -name "*.html" -newer sitemap.xml | wc -l

echo ""
echo "Health check complete."
