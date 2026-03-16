#!/bin/bash

PAGE="$1"

if [ -z "$PAGE" ]; then
  echo "Usage: ./tools/intelligence/sitemap-helper.sh \"page.html\""
  exit
fi

if [ ! -f "sitemap.xml" ]; then
  echo "sitemap.xml not found in current directory"
  exit
fi

if grep -q "$PAGE" sitemap.xml; then
  echo "Page already appears in sitemap.xml"
  exit
fi

sed -i "/<\/urlset>/i \  <url>\n    <loc>https://sideguy.com/$PAGE</loc>\n  </url>" sitemap.xml

echo "Added to sitemap.xml:"
echo "https://sideguy.com/$PAGE"
