#!/usr/bin/env bash

echo ""
echo "SideGuy System Status"
echo "---------------------"

HTML=$(find . -name "*.html" | wc -l)
MANIFESTS=$(find manifests -type f | wc -l)
TOOLS=$(find tools -type f | wc -l)

echo "HTML pages: $HTML"
echo "Manifest files: $MANIFESTS"
echo "Tool scripts: $TOOLS"

echo ""

echo "Foundation configuration:"
grep SITE_NAME config/sideguy-foundation.conf

echo ""
echo "System ready."
