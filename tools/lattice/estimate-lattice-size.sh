#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PARENTS="$ROOT/docs/manifests/lattice/parent-topics.txt"
CHILDREN="$ROOT/docs/manifests/lattice/child-topics.txt"
INDUSTRIES="$ROOT/docs/manifests/lattice/industries.txt"
LOCATIONS="$ROOT/docs/manifests/lattice/locations.txt"

parent_count=$(grep -cve '^\s*$' "$PARENTS")
child_count=$(grep -cve '^\s*$' "$CHILDREN")
industry_count=$(grep -cve '^\s*$' "$INDUSTRIES")
location_count=$(grep -cve '^\s*$' "$LOCATIONS")

core=$((parent_count * child_count * 4))
industry=$((parent_count * child_count * industry_count * 3))
local=$((parent_count * child_count * location_count * 3))
total=$((core + industry + local))

echo "SideGuy Semantic Topic Lattice Estimate"
echo "--------------------------------------"
echo "Parents: $parent_count"
echo "Children: $child_count"
echo "Industries: $industry_count"
echo "Locations: $location_count"
echo ""
echo "Core pages: $core"
echo "Industry pages: $industry"
echo "Local pages: $local"
echo ""
echo "Estimated total lattice pages: $total"
