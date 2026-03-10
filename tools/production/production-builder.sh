#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
MANIFEST="$ROOT/docs/lattice/lattice-manifest.tsv"
SITEMAP="$ROOT/sitemap.xml"
INDEX="$ROOT/index.html"

LIMIT="${1:-500}"

echo "-------------------------------------"
echo "SideGuy Production Builder"
echo "-------------------------------------"

echo ""
echo "Building $LIMIT pages..."

tools/lattice/build-lattice-batch.sh "$LIMIT"

echo ""
echo "Updating sitemap..."

grep -oP '(?<=<loc>)[^<]+' "$SITEMAP" | sed 's|https://sideguysolutions.com/||' > /tmp/current_urls.txt

find "$ROOT" -maxdepth 1 -name "*.html" -printf "%f\n" | sort > /tmp/all_pages.txt

comm -23 /tmp/all_pages.txt /tmp/current_urls.txt > /tmp/new_pages.txt

while read -r page
do
    echo "Adding $page to sitemap"

    sed -i "/<\/urlset>/i \
<url>\n\
<loc>https://sideguysolutions.com/$page</loc>\n\
</url>" "$SITEMAP"

done < /tmp/new_pages.txt


echo ""
echo "Updating index discovery links..."

while read -r page
do

    if ! grep -q "$page" "$INDEX"; then

        sed -i "/<\/body>/i \
<li><a href=\"/$page\">$page</a></li>" "$INDEX"

    fi

done < /tmp/new_pages.txt


echo ""
echo "Running health checks..."

if [ -f tools/health/health-check.sh ]; then
    bash tools/health/health-check.sh
fi


echo ""
echo "Production batch complete."
