#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
REPORT="$ROOT/docs/analysis/page-priority-report.txt"

echo "Running Authority Upgrader..."

head -50 "$REPORT" | while read line
do
  file=$(echo "$line" | cut -d'|' -f2 | xargs)

  [ -f "$file" ] || continue

  if ! grep -q "SideGuy FAQ" "$file"; then
    sed -i '/<\/body>/i \
<section class="sideguy-faq">\
<h2>SideGuy FAQ</h2>\
<ul>\
<li>How does this work?</li>\
<li>Can SideGuy help my business?</li>\
<li>Is this future-ready infrastructure?</li>\
</ul>\
</section>' "$file"
  fi

  if ! grep -q "Related SideGuy Guides" "$file"; then
    sed -i '/<\/body>/i \
<section class="related-guides">\
<h3>Related SideGuy Guides</h3>\
<ul>\
<li><a href="/ai-automation-knowledge-hub.html">AI Automation Hub</a></li>\
<li><a href="/payments-knowledge-hub.html">Payments Hub</a></li>\
<li><a href="/future-infrastructure-knowledge-hub.html">Future Infrastructure</a></li>\
<li><a href="/software-development-knowledge-hub.html">Software Development</a></li>\
</ul>\
</section>' "$file"
  fi

done

echo "Authority upgrades applied."
