#!/bin/bash

echo "Pages missing knowledge hub links:"
echo "----------------------------------"

find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'knowledge-hub' \
| sed 's|^\./||'

echo ""
echo "Count:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'knowledge-hub' \
| wc -l
