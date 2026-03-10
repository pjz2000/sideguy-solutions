#!/bin/bash

echo "Pages missing command center links:"
echo "-----------------------------------"

grep -rL 'sideguy-command-center.html' --include="*.html" . | sed 's|^\./||'

echo ""
echo "Count:"
grep -rL 'sideguy-command-center.html' --include="*.html" . | wc -l
