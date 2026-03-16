#!/usr/bin/env bash

SLUG="$1"

echo ""
echo "SideGuy Wiki Classifier"
echo "-----------------------"

if [[ "$SLUG" =~ ^why-|^how-|^what-|^can-|^best- ]]; then
echo "Type: problem"

elif [[ "$SLUG" =~ system|workflow|automation|infrastructure|tools ]]; then
echo "Type: system"

elif [[ "$SLUG" =~ vs-|choose|repair-vs|decision ]]; then
echo "Type: resolution"

elif [[ "$SLUG" =~ operator|pj ]]; then
echo "Type: operator"

else
echo "Type: skill-or-category"
fi
