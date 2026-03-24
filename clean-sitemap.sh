#!/usr/bin/env bash

########################################
# SIDEGUY SITEMAP CLEANER & REBUILDER
# Excludes backups, templates, junk
########################################

set -eo pipefail

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

DATE="$(date +"%Y-%m-%d-%H%M%S")"

echo "🧹 Cleaning and rebuilding sitemap..."
echo ""

# Backup old sitemap
if [ -f "sitemap.xml" ]; then
  cp sitemap.xml "sitemap.backup.$DATE.xml"
  echo "✅ Backed up old sitemap to sitemap.backup.$DATE.xml"
fi

# Find valid HTML pages (root level only, exclude junk)
PAGES=$(find . -maxdepth 1 -type f -name "*.html" \
  ! -name "*backup*" \
  ! -name "*tmp*" \
  ! -name "*temp*" \
  ! -name "_template*" \
  ! -name "sitemap*.html" \
  ! -name "index-backup*" \
  ! -name "index-working*" \
  | sed 's|^\./||' \
  | sort -u)

COUNT=$(echo "$PAGES" | wc -l | tr -d ' ')

echo "📄 Found $COUNT valid HTML pages (root level only, no backups)"
echo ""

# Build sitemap.xml
cat > sitemap.xml <<'XML_HEADER'
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
XML_HEADER

for PAGE in $PAGES; do
  # Skip if page is empty or a known junk pattern
  if [ ! -s "$PAGE" ]; then
    continue
  fi
  
  LASTMOD=$(date -r "$PAGE" +"%Y-%m-%d" 2>/dev/null || date +"%Y-%m-%d")
  
  # Prioritization logic
  PRIORITY="0.7"
  CHANGEFREQ="monthly"
  
  if [[ "$PAGE" == "index.html" ]] || [[ "$PAGE" == "-hub.html" ]]; then
    PRIORITY="1.0"
    CHANGEFREQ="weekly"
  elif [[ "$PAGE" == *"who-do-i-call"* ]] || [[ "$PAGE" == *"-cost"* ]]; then
    PRIORITY="0.9"
    CHANGEFREQ="weekly"
  elif [[ "$PAGE" == *"san-diego"* ]]; then
    PRIORITY="0.8"
    CHANGEFREQ="monthly"
  fi
  
  cat >> sitemap.xml <<URL_ENTRY
  <url>
    <loc>https://sideguysolutions.com/$PAGE</loc>
    <lastmod>$LASTMOD</lastmod>
    <changefreq>$CHANGEFREQ</changefreq>
    <priority>$PRIORITY</priority>
  </url>
URL_ENTRY
done

echo "</urlset>" >> sitemap.xml

echo "✅ sitemap.xml generated with $COUNT URLs"
echo ""

# Build human-readable sitemap.html
cat > sitemap.html <<HTML_HEADER
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SideGuy Solutions — All Pages</title>
<style>
body{font-family:system-ui,sans-serif;background:#f7fbff;color:#073044;padding:32px;max-width:1200px;margin:auto}
h1{margin-bottom:6px}
.meta{color:#5e7d8e;margin-bottom:24px}
ul{columns:3;column-gap:24px}
li{margin:6px 0;break-inside:avoid}
a{text-decoration:none;color:#1f7cff}
a:hover{text-decoration:underline}
@media(max-width:900px){ul{columns:2}}
@media(max-width:600px){ul{columns:1}}
</style>
</head>
<body>
<h1>SideGuy Solutions — All Pages</h1>
<div class="meta">
Total: <strong>$COUNT pages</strong><br>
Last updated: $(date)<br>
<a href="/">← Home</a> · <a href="/sitemap.xml">sitemap.xml</a>
</div>
<ul>
HTML_HEADER

for PAGE in $PAGES; do
  TITLE=$(echo "$PAGE" | sed 's/.html$//' | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')
  echo "<li><a href=\"/$PAGE\">$TITLE</a></li>" >> sitemap.html
done

cat >> sitemap.html <<HTML_FOOTER
</ul>
</body>
</html>
HTML_FOOTER

echo "✅ sitemap.html created (human-readable index)"
echo ""
echo "📊 Summary:"
echo "  - Valid pages: $COUNT"
echo "  - Backups excluded: ✓"
echo "  - Templates excluded: ✓"
echo "  - Root level only: ✓"
echo ""
echo "✅ Sitemap rebuild complete!"
