#!/usr/bin/env bash

PAGE="$1"

if [ -z "$PAGE" ]; then
echo "Usage:"
echo "bash link-optimizer.sh page.html"
exit 0
fi

echo ""
echo "Link Optimization Suggestions"
echo "-----------------------------"

echo "Add links to:"
echo "1 parent hub"
echo "2 related pages"
echo "1 system explanation"
echo "1 resolution page"
