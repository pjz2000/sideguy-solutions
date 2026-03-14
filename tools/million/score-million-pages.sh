#!/usr/bin/env bash
# Delegates to fast Python scorer

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

mkdir -p docs/million-page/scored
python3 tools/million/score-million-pages.py
exit $?

get_weight() {
  local file="$1"
  local key="$2"
  local value
  value="$(awk -F, -v k="$key" 'NR>1 && $1==k {print $2; exit}' "$file" 2>/dev/null)"
  echo "${value:-5}"
}

for manifest in docs/million-page/manifests/*.csv; do
  [ -f "$manifest" ] || continue

  OUT="docs/million-page/scored/$(basename "$manifest")"
  echo "url,title,h1,theme,audience,use_case,industry,city,state,modifier,page_type,intent,score" > "$OUT"

  tail -n +2 "$manifest" | while IFS=, read -r url title h1 theme audience use_case industry city state modifier page_type intent; do
    clean_theme="$(echo "$theme"     | tr -d '"' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
    clean_industry="$(echo "$industry" | tr -d '"' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
    clean_state="$(echo "$state"     | tr -d '"' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
    clean_page_type="$(echo "$page_type" | tr -d '"' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
    clean_modifier="$(echo "$modifier"  | tr -d '"')"
    clean_use_case="$(echo "$use_case"  | tr -d '"')"
    clean_city="$(echo "$city"       | tr -d '"')"

    tw="$(get_weight docs/million-page/config/theme-weights.csv     "$clean_theme")"
    sw="$(get_weight docs/million-page/config/state-priority.csv    "$clean_state")"
    iw="$(get_weight docs/million-page/config/industry-priority.csv "$clean_industry")"
    pw="$(get_weight docs/million-page/config/page-type-priority.csv "$clean_page_type")"

    modifier_bonus=0
    use_case_bonus=0
    city_bonus=0

    echo "$clean_modifier" | grep -Eiq 'pricing|comparison|security|compliance|implementation|buyer.guide|guide' && modifier_bonus=8
    echo "$clean_use_case" | grep -Eiq 'pricing|comparison|security|compliance|implementation'                   && use_case_bonus=8
    echo "$clean_city"     | grep -Eiq 'san-diego|los-angeles|san-francisco|new-york|chicago|miami|austin|seattle' && city_bonus=4

    score=$(( tw + sw + iw + pw + modifier_bonus + use_case_bonus + city_bonus ))

    printf '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"%s"\n' \
      "$url" "$title" "$h1" "$theme" "$audience" "$use_case" \
      "$industry" "$city" "$state" "$modifier" "$page_type" "$intent" "$score" >> "$OUT"
  done

  echo "Scored $OUT"
done
