#!/usr/bin/env bash
set -euo pipefail

OUT="public/confusion"
mkdir -p "$OUT"

pages=(
"what-is-ai-prediction-engine"
"hvac-repair-or-replace"
"should-i-switch-payment-processors"
)

for slug in "${pages[@]}"; do
  cat > "$OUT/$slug.html" <<HTML
<h1>$slug</h1>
<p>Confusion resolved.</p>
<a href="sms:+17735441231">Text PJ</a>
HTML
done

echo "confusion engine done"
