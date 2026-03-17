#!/usr/bin/env bash

cd /workspaces/sideguy-solutions || exit 0

INPUT="manifests/authority/topic-registry.json"
OUTPUT="docs/authority/internal-link-map.md"
LOG="logs/link-map.log"

touch "$LOG"
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

{
  echo "# SideGuy Internal Link Map"
  echo ""
  echo "Generated: $timestamp"
  echo ""
  echo "## Linking Rules"
  echo ""
  echo "- Every supporting page should link up to its topic hub"
  echo "- Every topic hub should link down to all supporting pages"
  echo "- Related topics should cross-link when the decision journey overlaps"
  echo "- Local pages should link to the broader topic hub"
  echo "- Explainers should link to decision pages where relevant"
  echo ""

  jq -c '.[]' "$INPUT" | while read -r topic; do
    slug=$(echo "$topic" | jq -r '.slug')
    title=$(echo "$topic" | jq -r '.title')
    echo "## $title"
    echo ""
    echo "Hub: /authority/$slug.html"
    echo ""

    echo "$topic" | jq -r '.pages[]' | while read -r page; do
      echo "- /$page.html → /authority/$slug.html"
      echo "- /authority/$slug.html → /$page.html"
    done

    echo ""
  done
} > "$OUTPUT"

echo "[$timestamp] BUILT $OUTPUT" >> "$LOG"
echo "Built link map: $OUTPUT"
