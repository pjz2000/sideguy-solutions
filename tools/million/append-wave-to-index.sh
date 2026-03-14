#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

SELECTION="docs/million-page/selected/wave-selection.csv"
INDEX_FILE="index.html"

[ -f "$SELECTION" ] || { echo "No wave-selection.csv found."; exit 1; }
[ -f "$INDEX_FILE" ] || { echo "No index.html found."; exit 1; }

TMP_BLOCK="docs/million-page/selected/index-links-block.html"

{
  echo '<section class="million-wave-links">'
  echo '  <h2>New Technology Intelligence Pages</h2>'
  echo '  <ul>'
  tail -n +2 "$SELECTION" | head -n 50 | while IFS=, read -r url title h1 rest; do
    CLEAN_URL="$(echo "$url" | tr -d '"')"
    CLEAN_H1="$(echo "$h1"  | sed 's/^"//;s/"$//')"
    echo "    <li><a href=\"${CLEAN_URL}\">${CLEAN_H1}</a></li>"
  done
  echo '  </ul>'
  echo '</section>'
} > "$TMP_BLOCK"

# Backup index
cp "$INDEX_FILE" "${INDEX_FILE}.bak-million"

python3 - <<'PY'
from pathlib import Path

index = Path("index.html")
block = Path("docs/million-page/selected/index-links-block.html").read_text()
text  = index.read_text()

if "</main>" in text:
    text = text.replace("</main>", block + "\n</main>", 1)
else:
    text += "\n" + block + "\n"

index.write_text(text)
print("Appended wave links to index.html")
PY
