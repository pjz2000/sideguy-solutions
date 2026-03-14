#!/usr/bin/env bash
# Delegates to fast Python selector (handles quoted CSV correctly)

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

mkdir -p docs/million-page/selected
python3 tools/million/select-wave-pages.py
exit $?

source docs/million-page/config/publish-quota.env

ALL_TMP="docs/million-page/selected/all-scored.tmp.csv"
FINAL="docs/million-page/selected/wave-selection.csv"

HEADER_WRITTEN=0
: > "$ALL_TMP"

for f in docs/million-page/scored-deduped/*.csv; do
  [ -f "$f" ] || continue
  if [ "$HEADER_WRITTEN" -eq 0 ]; then
    head -n 1 "$f" > "$ALL_TMP"
    HEADER_WRITTEN=1
  fi
  tail -n +2 "$f" >> "$ALL_TMP"
done

[ -f "$ALL_TMP" ] || { echo "No scored-deduped CSVs found."; exit 1; }

head -n 1 "$ALL_TMP" > "$FINAL"

tail -n +2 "$ALL_TMP" \
  | awk -F, -v min="$MIN_SCORE_TO_PUBLISH" '
      {
        gsub(/"/, "", $13)
        if ($13+0 >= min) print $0
      }
    ' \
  | sort -t, -k13,13nr \
  | awk -F, \
      -v max_wave="$WAVE_PUBLISH_QUOTA" \
      -v max_theme="$MAX_PAGES_PER_THEME_PER_WAVE" \
      -v max_state="$MAX_PAGES_PER_STATE_PER_WAVE" \
      -v max_industry="$MAX_PAGES_PER_INDUSTRY_PER_WAVE" '
      BEGIN { count=0 }
      {
        gsub(/"/, "", $4);  theme=$4
        gsub(/"/, "", $7);  industry=$7
        gsub(/"/, "", $9);  state=$9

        if (theme_count[theme]     >= max_theme)    next
        if (state_count[state]     >= max_state)    next
        if (industry_count[industry] >= max_industry) next
        if (count >= max_wave) next

        print $0
        theme_count[theme]++
        state_count[state]++
        industry_count[industry]++
        count++
      }
    ' >> "$FINAL"

SELECTED=$(( $(wc -l < "$FINAL") - 1 ))
echo "Built $FINAL — $SELECTED pages selected"
