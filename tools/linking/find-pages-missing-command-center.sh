#!/bin/bash

echo "Pages missing command center links:"
echo "-----------------------------------"

find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'command-center' \
| sed 's|^\./||'

echo ""
echo "Count:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'command-center' \
| wc -l
