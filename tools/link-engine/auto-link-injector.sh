#!/bin/bash
# Auto Link Injector — scoped to a directory to prevent O(n²) blast across 57k files.
# Default scope: pages/factory/
# Usage: bash tools/link-engine/auto-link-injector.sh [directory]

DIR="${1:-pages/factory}"
REPORT="reports/auto-link-injected.txt"

echo "====================================="
echo "SideGuy Auto Link Injector"
echo "Directory: $DIR"
echo "====================================="

mkdir -p reports
> "$REPORT"

FILES=$(find "$DIR" -maxdepth 1 -name "*.html" | sort)
COUNT=$(echo "$FILES" | grep -c .)

echo "Files in scope: $COUNT"
echo ""

updated=0

for file in $FILES; do
  slug=$(basename "$file" .html)

  # Skip if already injected
  if grep -q 'auto-link-block' "$file"; then
    continue
  fi

  # Find related pages: other files in same dir whose slug shares a word with this one
  links=""
  for word in $(echo "$slug" | tr '-' '\n' | awk 'length>3'); do
    matches=$(echo "$FILES" | grep -i "$word" | grep -v "^$file$")
    for match in $matches; do
      other_slug=$(basename "$match" .html)
      label=$(echo "$other_slug" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2); print}')
      links="$links<li><a href=\"/$other_slug.html\">$label</a></li>"
    done
  done

  # Deduplicate links with python
  if [ -n "$links" ]; then
    python3 - "$file" "$links" <<'PYEOF'
import sys
path, links_str = sys.argv[1], sys.argv[2]
content = open(path).read()
if 'auto-link-block' in content:
    sys.exit(0)
# Deduplicate href anchors
seen = set()
out = []
import re
for m in re.finditer(r'<li><a href="([^"]+)">([^<]+)</a></li>', links_str):
    href = m.group(1)
    if href not in seen:
        seen.add(href)
        out.append(f'<li><a href="{href}">{m.group(2)}</a></li>')
if not out:
    sys.exit(0)
block = '<!-- auto-link-block --><div style="margin:1.5rem 0;padding:16px;background:#f3fbff;border-radius:10px;"><h3 style="margin:0 0 10px;font-size:.95rem;">Related Topics</h3><ul style="margin:0;padding-left:1.2em;">' + ''.join(out) + '</ul></div>'
if '</body>' in content:
    content = content.replace('</body>', block + '\n</body>', 1)
    open(path, 'w').write(content)
    print(f'  linked: {path} (+{len(out)} links)')
PYEOF
    updated=$((updated+1))
  fi
done

echo ""
echo "Auto linking complete."
echo "Files updated: $updated"
echo "Report: $REPORT"
echo "$updated files updated in $DIR" >> "$REPORT"
