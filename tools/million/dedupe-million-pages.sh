#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

mkdir -p docs/million-page/scored-deduped
SEEN_FILE="docs/million-page/.seen-million-urls.txt"
: > "$SEEN_FILE"

for scored in docs/million-page/scored/*.csv; do
  [ -f "$scored" ] || continue

  OUT="docs/million-page/scored-deduped/$(basename "$scored")"
  head -n 1 "$scored" > "$OUT"

  tail -n +2 "$scored" | while IFS= read -r line; do
    url="$(echo "$line"   | awk -F, '{print $1}' | tr -d '"')"
    title="$(echo "$line" | awk -F, '{print $2}' | tr -d '"')"

    # Skip already-seen URLs
    grep -Fxq "$url" "$SEEN_FILE" && continue

    # Skip junk titles
    echo "$title" | grep -Eiq 'null|undefined|test|temp' && continue

    echo "$url" >> "$SEEN_FILE"
    echo "$line" >> "$OUT"
  done

  echo "Deduped $OUT"
done
