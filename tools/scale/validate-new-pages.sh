#!/bin/bash

# =========================================
# SIDEGUY — BATCH VALIDATION
# Quality gate before committing new pages.
# =========================================

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "SideGuy Batch Validation"
echo "------------------------"

echo ""
echo "Root HTML count:"
find "$ROOT" -maxdepth 1 -name "*.html" | wc -l

echo ""
echo "Pages missing meta description:"
find "$ROOT" -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'name="description"' \
| wc -l

echo ""
echo "Pages missing canonical:"
find "$ROOT" -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'rel="canonical"' \
| wc -l

echo ""
echo "Pages missing H1:"
find "$ROOT" -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L '<h1' \
| wc -l

echo ""
echo "Pages missing Text PJ:"
find "$ROOT" -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L '773-544-1231' \
| wc -l

echo ""
echo "Pages missing command center link:"
find "$ROOT" -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'command-center' \
| wc -l

echo ""
echo "Validation complete."
