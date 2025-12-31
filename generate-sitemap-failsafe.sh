#!/usr/bin/env bash

# =========================================
# SIDEGUY — FAILSAFE VISUAL SITEMAP + COUNTS
# =========================================

echo "📂 Scanning repo..."

# 1. Find ALL html except system junk
PAGES=$(find . -type f -name "*.html" \
  ! -path "./node_modules/*" \
  ! -path "./.git/*" \
  | sed 's|^\./||' \
  | sort)

TOTAL=$(echo "$PAGES" | wc -l | tr -d ' ')

echo "📄 Found $TOTAL html files"

# 2. Backup existing sitemap
[ -f sitemap.html ] && cp sitemap.html sitemap.backup.$(date +%Y%m%d-%H%M).html

# 3. Build sitemap.html
cat <<HTML > sitemap.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SideGuy Solutions — Full Page Index</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:system-ui,-apple-system,sans-serif;background:#f7fbff;color:#073044;padding:32px;max-width:1200px;margin:auto}
h1{margin-bottom:6px}
.meta{color:#5e7d8e;margin-bottom:24px}
ul{columns:2}
li{margin:4px 0;break-inside:avoid}
a{text-decoration:none;color:#1f7cff}
a:hover{text-decoration:underline}
.count{font-weight:700;color:#21d3a1}
@media(max-width:800px){ul{columns:1}}
</style>
</head>
<body>

<h1>SideGuy Solutions — All Pages</h1>
<div class="meta">
Total HTML files: <span class="count">$TOTAL</span><br>
Generated: $(date)
</div>

<ul>
HTML

# 4. Insert links
echo "$PAGES" | while read -r page; do
  echo "<li><a href=\"/$page\">$page</a></li>" >> sitemap.html
done

# 5. Close file
cat <<HTML >> sitemap.html
</ul>
</body>
</html>
HTML

echo "✅ sitemap.html rebuilt successfully"
