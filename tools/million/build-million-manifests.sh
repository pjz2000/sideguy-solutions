#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

mkdir -p docs/million-page/manifests

mapfile -t THEMES < docs/million-page/keywords/core-themes.txt
mapfile -t AUDIENCES < docs/million-page/keywords/audiences.txt
mapfile -t USE_CASES < docs/million-page/keywords/use-cases.txt
mapfile -t INDUSTRIES < docs/million-page/keywords/industries.txt
mapfile -t CITIES < docs/million-page/keywords/cities.txt
mapfile -t STATES < docs/million-page/keywords/states.txt
mapfile -t MODIFIERS < docs/million-page/keywords/modifiers.txt
mapfile -t PAGE_TYPES < docs/million-page/keywords/page-types.txt

slugify() {
  echo "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]/-/g' \
    | sed 's/--*/-/g' \
    | sed 's/^-//' \
    | sed 's/-$//'
}

# URL uniqueness comes from: theme × page_type × industry × city × state (5 dims)
# audience, use_case, modifier are stored as representative metadata (first non-empty value)
AUDIENCE="${AUDIENCES[0]}"
USE_CASE="${USE_CASES[0]}"
MODIFIER="${MODIFIERS[0]}"

for theme in "${THEMES[@]}"; do
  [[ -z "$theme" ]] && continue
  THEME_SLUG="$(slugify "$theme")"
  OUT="docs/million-page/manifests/${THEME_SLUG}.csv"

  echo "url,title,h1,theme,audience,use_case,industry,city,state,modifier,page_type,intent" > "$OUT"
  ROW_COUNT=0

  for page_type in "${PAGE_TYPES[@]}"; do
    [[ -z "$page_type" ]] && continue
    for industry in "${INDUSTRIES[@]}"; do
      [[ -z "$industry" ]] && continue
      for city in "${CITIES[@]}"; do
        [[ -z "$city" ]] && continue
        for state in "${STATES[@]}"; do
          [[ -z "$state" ]] && continue

          URL="/$(slugify "$theme")-$(slugify "$page_type")-for-$(slugify "$industry")-in-$(slugify "$city")-$(slugify "$state").html"
          TITLE="$(printf "%s %s for %s in %s, %s | SideGuy Solutions" "$theme" "$page_type" "$industry" "$city" "$state")"
          H1="$(printf "%s %s for %s in %s, %s" "$theme" "$page_type" "$industry" "$city" "$state")"
          INTENT="$(printf "%s | %s | %s | %s" "$AUDIENCE" "$USE_CASE" "$MODIFIER" "$page_type")"

          printf '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' \
            "$URL" "$TITLE" "$H1" "$theme" "$AUDIENCE" "$USE_CASE" \
            "$industry" "$city" "$state" "$MODIFIER" "$page_type" "$INTENT" >> "$OUT"

          ROW_COUNT=$(( ROW_COUNT + 1 ))
        done
      done
    done
  done

  echo "Built $OUT ($ROW_COUNT rows)"
done
