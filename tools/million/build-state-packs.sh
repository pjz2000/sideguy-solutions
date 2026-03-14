#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

mkdir -p docs/million-page/state-packs

for manifest in docs/million-page/manifests/*.csv; do
  [ -f "$manifest" ] || continue

  BASENAME="$(basename "$manifest" .csv)"

  # Build per-state files (no header yet)
  tail -n +2 "$manifest" | while IFS= read -r line; do
    state="$(echo "$line" | awk -F, '{gsub(/"/, "", $9); print $9}')"
    [ -z "$state" ] && continue
    echo "$line" >> "docs/million-page/state-packs/${BASENAME}-${state}.csv"
  done

  # Prepend header to each state pack
  HEADER="$(head -n 1 "$manifest")"
  for f in docs/million-page/state-packs/${BASENAME}-*.csv; do
    [ -f "$f" ] || continue
    TMP="${f}.tmp"
    { echo "$HEADER"; cat "$f"; } > "$TMP"
    mv "$TMP" "$f"
  done

  echo "Built state packs for $BASENAME"
done

echo "Done. State packs in docs/million-page/state-packs/"
