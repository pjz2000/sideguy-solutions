#!/bin/bash

PAGES="${1:-100000}"

REL_PER_PAGE=5

REL_TOTAL=$((PAGES * REL_PER_PAGE))

echo ""
echo "SideGuy Wiki Graph Math"
echo "-----------------------"
echo "Pages: $PAGES"
echo "Relationships per page: $REL_PER_PAGE"
echo ""
echo "Total graph connections: $REL_TOTAL"
echo ""
