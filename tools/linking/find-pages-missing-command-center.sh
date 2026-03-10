#!/bin/bash

echo "Pages missing command center links:"
echo "-----------------------------------"

find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'sideguy-command-center.html' \
| sed 's|^\./||'

echo ""
echo "Count:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'sideguy-command-center.html' \
| wc -l
