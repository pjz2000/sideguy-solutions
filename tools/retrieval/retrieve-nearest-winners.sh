
#!/bin/bash

QUERY="$1"

echo "🔎 Retrieving nearest winners for: $QUERY"

grep -ril "$QUERY" . --include="*.html" --include="*.md" | head -20 > logs/retrieval/nearest-winners.txt

echo "Saved to logs/retrieval/nearest-winners.txt"

