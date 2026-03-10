#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PARENTS="$ROOT/docs/manifests/lattice/parent-topics.txt"
CHILDREN="$ROOT/docs/manifests/lattice/child-topics.txt"
INDUSTRIES="$ROOT/docs/manifests/lattice/industries.txt"
LOCATIONS="$ROOT/docs/manifests/lattice/locations.txt"
OUTPUT="$ROOT/docs/lattice/lattice-manifest.tsv"

mkdir -p "$ROOT/docs/lattice"

: > "$OUTPUT"
printf "type\tparent\tchild\tmodifier\tslug\n" >> "$OUTPUT"

slugify() {
  echo "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[\/&,.:?()]//g' \
    | tr ' ' '-' \
    | sed 's/--*/-/g' \
    | sed 's/^-//' \
    | sed 's/-$//'
}

while read -r parent; do
  [ -z "$parent" ] && continue
  parent_slug=$(slugify "$parent")

  while read -r child; do
    [ -z "$child" ] && continue
    child_slug=$(slugify "$child")

    printf "core\t%s\t%s\tbase\twhat-is-%s.html\n" "$parent" "$child" "$child_slug" >> "$OUTPUT"
    printf "core\t%s\t%s\tbase\thow-to-use-%s.html\n" "$parent" "$child" "$child_slug" >> "$OUTPUT"
    printf "core\t%s\t%s\tbase\thow-much-does-%s-cost.html\n" "$parent" "$child" "$child_slug" >> "$OUTPUT"
    printf "core\t%s\t%s\tbase\t%s-vs-alternatives.html\n" "$parent" "$child" "$child_slug" >> "$OUTPUT"

    while read -r industry; do
      [ -z "$industry" ] && continue
      industry_slug=$(slugify "$industry")
      printf "industry\t%s\t%s\t%s\t%s-for-%s.html\n" "$parent" "$child" "$industry" "$child_slug" "$industry_slug" >> "$OUTPUT"
      printf "industry\t%s\t%s\t%s\thow-to-use-%s-for-%s.html\n" "$parent" "$child" "$industry" "$child_slug" "$industry_slug" >> "$OUTPUT"
      printf "industry\t%s\t%s\t%s\thow-much-does-%s-cost-for-%s.html\n" "$parent" "$child" "$industry" "$child_slug" "$industry_slug" >> "$OUTPUT"
    done < "$INDUSTRIES"

    while read -r location; do
      [ -z "$location" ] && continue
      location_slug=$(slugify "$location")
      printf "local\t%s\t%s\t%s\t%s-%s.html\n" "$parent" "$child" "$location" "$child_slug" "$location_slug" >> "$OUTPUT"
      printf "local\t%s\t%s\t%s\t%s-in-%s.html\n" "$parent" "$child" "$location" "$child_slug" "$location_slug" >> "$OUTPUT"
      printf "local\t%s\t%s\t%s\thow-much-does-%s-cost-in-%s.html\n" "$parent" "$child" "$location" "$child_slug" "$location_slug" >> "$OUTPUT"
    done < "$LOCATIONS"

  done < "$CHILDREN"

done < "$PARENTS"

echo "Lattice manifest created: $OUTPUT"
wc -l "$OUTPUT"
