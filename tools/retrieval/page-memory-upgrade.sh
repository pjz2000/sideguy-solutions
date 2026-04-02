
#!/bin/bash

PAGE="$1"

echo "🧠 Memory-guided upgrade target: $PAGE"

URL_KEY=$(basename "$PAGE" .html | tr '-' ' ')

tools/retrieval/retrieve-nearest-winners.sh "$URL_KEY"

echo "Use retrieved winners as enhancement inspiration before editing $PAGE"

