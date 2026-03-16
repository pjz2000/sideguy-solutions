#!/usr/bin/env bash

echo ""
echo "SideGuy Foundation Check"
echo "------------------------"

echo ""
echo "Checking config..."

if [ -f config/sideguy-foundation.conf ]; then
echo "✓ config present"
else
echo "⚠ missing config"
fi

echo ""
echo "Checking page types..."

if [ -f manifests/foundation/page-types.txt ]; then
wc -l manifests/foundation/page-types.txt
else
echo "⚠ page-types manifest missing"
fi

echo ""
echo "Checking verticals..."

if [ -f manifests/foundation/verticals.txt ]; then
wc -l manifests/foundation/verticals.txt
else
echo "⚠ vertical manifest missing"
fi

echo ""
echo "Checking docs..."

ls docs/foundation

echo ""
echo "Foundation check complete"
