#!/bin/bash

echo "Running SideGuy Authority Flow Engine"

REPORT="docs/gravity/authority-links.txt"
mkdir -p docs/gravity

echo "Authority flow run $(date)" > "$REPORT"

PAGES=(
  "ai-tools-for-small-business-san-diego.html"
  "machine-to-machine-payments.html"
  "ai-automation-for-contractors-san-diego.html"
  "battery-backup-installation-san-diego.html"
  "hvac-repair-vs-replacement-san-diego.html"
)

BLOCK='<div style="background:#f3fbff;padding:20px;border-radius:10px;margin-top:40px;"><h3>Related Guides</h3><ul><li><a href="/ai-tools-for-small-business-san-diego.html">AI Tools for Small Business</a></li><li><a href="/machine-to-machine-payments.html">Machine-to-Machine Payments</a></li><li><a href="/ai-automation-for-contractors-san-diego.html">AI Automation for Contractors</a></li><li><a href="/battery-backup-installation-san-diego.html">Battery Backup Installation</a></li><li><a href="/hvac-repair-vs-replacement-san-diego.html">HVAC Repair vs Replacement</a></li></ul></div>'

for page in "${PAGES[@]}"; do
  echo "Processing $page" | tee -a "$REPORT"

  if [ ! -f "$page" ]; then
    echo "  SKIP (not found): $page" | tee -a "$REPORT"
    continue
  fi

  # Skip if already has this block
  if grep -q 'authority-flow-block' "$page"; then
    echo "  SKIP (already upgraded): $page" | tee -a "$REPORT"
    continue
  fi

  python3 - "$page" <<PYEOF
import sys
path = sys.argv[1]
content = open(path).read()
marker = '<div style="background:#f3fbff;padding:20px;border-radius:10px;margin-top:40px;"><!-- authority-flow-block -->'
block = marker + '<h3>Related Guides</h3><ul><li><a href="/ai-tools-for-small-business-san-diego.html">AI Tools for Small Business</a></li><li><a href="/machine-to-machine-payments.html">Machine-to-Machine Payments</a></li><li><a href="/ai-automation-for-contractors-san-diego.html">AI Automation for Contractors</a></li><li><a href="/battery-backup-installation-san-diego.html">Battery Backup Installation</a></li><li><a href="/hvac-repair-vs-replacement-san-diego.html">HVAC Repair vs Replacement</a></li></ul></div>'
if 'authority-flow-block' not in content and '</body>' in content:
    content = content.replace('</body>', block + '\n</body>', 1)
    open(path, 'w').write(content)
    print(f'  upgraded: {path}')
else:
    print(f'  skipped (no </body> or already present): {path}')
PYEOF

  echo "$page processed" >> "$REPORT"
done

echo ""
echo "Authority Flow Complete"
echo "Report: $REPORT"
