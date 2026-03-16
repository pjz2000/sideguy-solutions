#!/usr/bin/env bash

CATEGORIES=${1:-10}
PROBLEMS=${2:-8000}
SYSTEMS=${3:-800}
RESOLUTIONS=${4:-800}
SKILLS=${5:-300}
OPERATORS=${6:-100}

TOTAL=$((CATEGORIES*(PROBLEMS+SYSTEMS+RESOLUTIONS+SKILLS+OPERATORS)))

echo ""
echo "SideGuy Wiki Scale Math"
echo "-----------------------"
echo "Categories: $CATEGORIES"
echo "Problems: $PROBLEMS"
echo "Systems: $SYSTEMS"
echo "Resolutions: $RESOLUTIONS"
echo "Skills: $SKILLS"
echo "Operators: $OPERATORS"
echo ""
echo "Potential pages: $TOTAL"
echo ""
