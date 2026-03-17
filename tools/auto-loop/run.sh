#!/usr/bin/env bash
set -euo pipefail

INPUT="manifests/auto-loop/generated.json"
OUTPUT="public/auto-loop"
LOG="logs/auto-loop.log"

mkdir -p "$OUTPUT"

jq -n '
[
  {
    "slug": "future-search-is-prediction",
    "title": "Future Search Is Prediction",
    "intent": "future search ai prediction",
    "category": "ai",
    "type": "future"
  },
  {
    "slug": "ai-prediction-engine-explained",
    "title": "AI Prediction Engine Explained",
    "intent": "ai prediction engine explained",
    "category": "ai",
    "type": "explainer"
  }
]
' > "$INPUT"

jq -c '.[]' "$INPUT" | while read -r row; do
  slug=$(echo "$row" | jq -r '.slug')
  title=$(echo "$row" | jq -r '.title')

  cat > "$OUTPUT/$slug.html" <<HTML
<h1>$title</h1>
<p>Predicted page.</p>
<a href="sms:+17735441231">Text PJ</a>
HTML

  echo "built $slug" >> "$LOG"
done

echo "auto-loop done"
