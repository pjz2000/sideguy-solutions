#!/usr/bin/env bash

HUB="$1"

if [ -z "$HUB" ]; then
echo "Usage:"
echo "bash cluster-expander.sh hub-slug"
exit 0
fi

echo ""
echo "Cluster expansion ideas for: $HUB"
echo ""

echo "$HUB-explained"
echo "$HUB-benefits"
echo "$HUB-tools"
echo "$HUB-faq"
echo "$HUB-business-use"
echo "$HUB-vs-traditional"
echo "$HUB-future"
