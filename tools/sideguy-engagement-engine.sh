#!/usr/bin/env bash
# tools/sideguy-engagement-engine.sh
# Injects a "Quick Reality Check" engagement block before </body> in HTML pages.
# Usage: bash tools/sideguy-engagement-engine.sh [--dry-run] [--dir DIR] [--help]

DRY_RUN=0
SCAN_DIR="public"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run|-n)  DRY_RUN=1 ;;
    --dir)         shift; SCAN_DIR="${1:?'--dir requires a path'}" ;;
    --help|-h)
      echo "Usage: bash tools/sideguy-engagement-engine.sh [options]"
      echo ""
      echo "Options:"
      echo "  --dry-run, -n    Show which files would be updated; write nothing"
      echo "  --dir DIR        Directory to scan (default: public)"
      echo "  --help, -h       Show this help"
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

echo ""
echo "========================================="
echo "SIDEGUY ENGAGEMENT ENGINE"
echo "Turning clicks into dwell time + texts"
[[ $DRY_RUN -eq 1 ]] && echo "(DRY RUN — no files will be modified)"
echo "========================================="
echo ""

cd /workspaces/sideguy-solutions || exit 1

DATE=$(date +"%Y-%m-%d")
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/engagement.log"

[[ $DRY_RUN -eq 0 ]] && mkdir -p "$LOG_DIR"

# The block to inject — written to a temp file so sed never needs to handle
# multi-line strings inline (which is fragile and shell-version-sensitive).
BLOCK_MARKER="SIDEGUY ENGAGEMENT BLOCK"
BLOCK=$(cat <<'ENGAGEMENT'
<!-- SIDEGUY ENGAGEMENT BLOCK -->
<hr>
<h2>Quick Reality Check</h2>
<p>This is where most people get stuck. There are multiple paths, but only one that makes sense for your situation.</p>

<h2>Before You Decide</h2>
<ul>
<li>What are you actually trying to solve?</li>
<li>Is this urgent or can it wait?</li>
<li>What's the downside of choosing wrong?</li>
</ul>

<h2>SideGuy Tip</h2>
<p>Most people spend money too early. The goal is clarity first — then action.</p>

<h2>Want a second opinion?</h2>
<p>Text PJ your situation and get a real answer before you commit. <a href="sms:+17604541860">Text PJ now →</a></p>
ENGAGEMENT
)

BLOCK_FILE=$(mktemp)
printf '%s\n' "$BLOCK" > "$BLOCK_FILE"

UPDATED=0
SKIPPED=0

while IFS= read -r file; do

  if grep -q "$BLOCK_MARKER" "$file"; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  if ! grep -q "</body>" "$file"; then
    echo "[skip] No </body> tag: $file"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] would update: $file"
  else
    # Use a temp output file to avoid in-place corruption
    TMP=$(mktemp)
    # Insert block content immediately before the closing </body> tag
    while IFS= read -r line; do
      if [[ "$line" == *"</body>"* ]]; then
        cat "$BLOCK_FILE"
        echo ""
      fi
      printf '%s\n' "$line"
    done < "$file" > "$TMP"
    mv "$TMP" "$file"
    echo "[ok] Engagement layer added → $file"
  fi

  UPDATED=$((UPDATED + 1))

done < <(find "$SCAN_DIR" -name "*.html" -type f 2>/dev/null)

rm -f "$BLOCK_FILE"

if [[ $DRY_RUN -eq 0 ]]; then
  echo "$DATE engagement layer deployed ($UPDATED pages updated, $SKIPPED skipped)" >> "$LOG_FILE"
fi

echo ""
echo "========================================="
echo "ENGAGEMENT ENGINE COMPLETE"
[[ $DRY_RUN -eq 1 ]] && echo "(DRY RUN — nothing was written)"
echo "========================================="
echo ""
echo "Results:"
echo "- Updated : $UPDATED"
echo "- Skipped : $SKIPPED (already have block or no </body>)"
echo "- Log     : $LOG_FILE"
echo ""
