#!/usr/bin/env bash
# Fix domain from sideguy.solutions to sideguysolutions.com
set -e

echo "🔧 Fixing domain across entire site..."
echo "From: sideguy.solutions"
echo "To: sideguysolutions.com"
echo ""

# Fix sitemaps
echo "📍 Fixing sitemaps..."
for file in sitemap*.xml; do
  if [ -f "$file" ]; then
    sed -i 's|sideguy\.solutions|sideguysolutions.com|g' "$file"
    echo "  ✅ $file"
  fi
done

# Fix robots.txt
echo "📍 Fixing robots.txt..."
if [ -f "robots.txt" ]; then
  sed -i 's|sideguy\.solutions|sideguysolutions.com|g' "robots.txt"
  echo "  ✅ robots.txt"
fi

# Fix Python scripts
echo "📍 Fixing Python scripts..."
for file in *.py; do
  if [ -f "$file" ]; then
    sed -i 's|sideguy\.solutions|sideguysolutions.com|g' "$file"
    echo "  ✅ $file"
  fi
done

# Fix HTML files (analytics domain)
echo "📍 Fixing HTML pages..."
find . -maxdepth 1 -name "*.html" -type f | while read file; do
  sed -i 's|data-domain="sideguy\.solutions"|data-domain="sideguysolutions.com"|g' "$file"
done
echo "  ✅ Fixed ~1700 HTML pages"

# Fix sitemaps directory if exists
if [ -d "sitemaps" ]; then
  echo "📍 Fixing /sitemaps/ directory..."
  find sitemaps -name "*.xml" -type f | while read file; do
    sed -i 's|sideguy\.solutions|sideguysolutions.com|g' "$file"
  done
  echo "  ✅ Fixed sitemaps directory"
fi

echo ""
echo "✅ Domain fix complete!"
echo ""
echo "Verification:"
echo "Old domain remaining:" 
grep -r "sideguy\.solutions" --include="*.xml" --include="*.txt" --include="*.py" --include="*.html" . 2>/dev/null | wc -l || echo "0"
echo ""
echo "New domain count:"
grep -r "sideguysolutions\.com" --include="*.xml" --include="*.txt" --include="*.py" --include="*.html" . 2>/dev/null | wc -l || echo "0"
