#!/usr/bin/env bash
set -euo pipefail

OUT="public/local"
mkdir -p "$OUT"

cities=("san-diego" "encinitas")

for city in "${cities[@]}"; do
  slug="hvac-repair-$city"

  cat > "$OUT/$slug.html" <<HTML
<h1>HVAC Repair in $city</h1>
<p>Local decision page.</p>
<a href="sms:+17735441231">Text PJ</a>
HTML
done

echo "local engine done"
