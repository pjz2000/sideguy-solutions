#!/bin/bash

echo "Pages missing knowledge hub links:"
echo "----------------------------------"

grep -rL 'knowledge-hub' --include="*.html" . | sed 's|^\./||'

echo ""
echo "Count:"
grep -rL 'knowledge-hub' --include="*.html" . | wc -l
