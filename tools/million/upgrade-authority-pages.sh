#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

INPUT="docs/million-page/authority/upgrade-candidates.csv"
[ -f "$INPUT" ] || { echo "No upgrade-candidates.csv found."; exit 1; }

UPGRADED=0
SKIPPED=0

tail -n +2 "$INPUT" | while IFS=, read -r url title h1 theme audience use_case industry city state modifier page_type intent score; do
  clean_url="$(echo "$url" | tr -d '"')"
  slug="$(basename "$clean_url" .html)"
  page="public${clean_url}"
  block="docs/million-page/authority/blocks/${slug}.html"
  schema="docs/million-page/authority/schema/${slug}.json"

  [ -f "$page" ]   || continue
  [ -f "$block" ]  || continue
  [ -f "$schema" ] || continue

  # Skip already-upgraded pages
  grep -q "sideguy-authority" "$page" && continue

  python3 - "$page" "$block" "$schema" <<'PY'
import sys
from pathlib import Path

page_path   = Path(sys.argv[1])
block_text  = Path(sys.argv[2]).read_text()
schema_text = Path(sys.argv[3]).read_text()
text        = page_path.read_text()

authority = f"""
<!-- SideGuy Authority Upgrade -->
{block_text}
<script type="application/ld+json">
{schema_text}
</script>
"""

if "</main>" in text:
    text = text.replace("</main>", authority + "\n</main>", 1)
else:
    text += authority

page_path.write_text(text)
PY

  echo "Upgraded $page"
done

echo "Authority upgrades complete."
