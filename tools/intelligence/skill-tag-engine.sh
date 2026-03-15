#!/usr/bin/env bash

echo "=============================="
echo "SideGuy Skill Tag Engine"
echo "=============================="

TAGS="docs/skill-tags/skill-tags.txt"

if [ ! -f "$TAGS" ]; then
  echo "Skill tag list missing."
  exit
fi

echo ""
echo "Registered Skill Tags:"
echo ""
cat "$TAGS"
echo ""
echo "Use these tags to connect pages and operators."
