#!/usr/bin/env bash
set -euo pipefail

OUT="public/prediction"
mkdir -p "$OUT"

pages=(
"prediction-publishing-explained"
"publish-before-demand"
)

for slug in "${pages[@]}"; do
  cat > "$OUT/$slug.html" <<HTML
<h1>$slug</h1>
<p>Prediction publishing page.</p>
<a href="sms:+17735441231">Text PJ</a>
HTML
done

echo "prediction engine done"
