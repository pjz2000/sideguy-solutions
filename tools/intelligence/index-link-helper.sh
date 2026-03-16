#!/bin/bash

PAGE="$1"
LABEL="$2"

if [ -z "$PAGE" ] || [ -z "$LABEL" ]; then
  echo "Usage: ./tools/intelligence/index-link-helper.sh \"page.html\" \"Link Label\""
  exit
fi

if [ ! -f "index.html" ]; then
  echo "index.html not found in current directory"
  exit
fi

if grep -q "$PAGE" index.html; then
  echo "Page already linked in index.html"
  exit
fi

sed -i "/<\/body>/i <p><a href=\"$PAGE\">$LABEL</a></p>" index.html

echo "Added link to index.html:"
echo "$LABEL -> $PAGE"
