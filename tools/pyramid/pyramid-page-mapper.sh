#!/usr/bin/env bash

PAGE="$1"

if [ -z "$PAGE" ]; then
echo "Usage:"
echo "bash tools/pyramid/pyramid-page-mapper.sh slug"
exit 0
fi

echo ""
echo "SideGuy Pyramid Page Mapper"
echo "Page: $PAGE"
echo ""

if [[ "$PAGE" =~ ^why|^how|^what|^best ]]; then
echo "Layer: Problem Layer"
echo "Intent: Search question"

elif [[ "$PAGE" =~ automation|payments|system|infrastructure ]]; then
echo "Layer: System Layer"
echo "Intent: System explanation"

else
echo "Layer: Resolution Layer"
echo "Intent: Decision guidance"
fi

echo ""
echo "Recommended linking:"
echo "Problem → System → Resolution"
