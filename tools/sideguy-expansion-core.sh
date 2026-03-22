#!/usr/bin/env bash
# tools/sideguy-expansion-core.sh
# Usage: bash tools/sideguy-expansion-core.sh [--dry-run] [--no-build] [--limit N] [--help]

DRY_RUN=0
NO_BUILD=0
LIMIT=500

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run|-n)  DRY_RUN=1 ;;
    --no-build)    NO_BUILD=1 ;;
    --limit)       shift; LIMIT="${1:?'--limit requires a number'}"; [[ "$LIMIT" =~ ^[0-9]+$ ]] || { echo "Error: --limit must be a number"; exit 1; } ;;
    --help|-h)
      echo "Usage: bash tools/sideguy-expansion-core.sh [options]"
      echo ""
      echo "Options:"
      echo "  --dry-run, -n     Show what would be done; write nothing"
      echo "  --no-build        Skip section 2 (auto page builder)"
      echo "  --limit N         Max pages to build (default: 500)"
      echo "  --help, -h        Show this help"
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

echo ""
echo "===================================================="
echo "SIDEGUY EXPANSION CORE"
echo "Build → Expand → Prioritize → Position"
[[ $DRY_RUN -eq 1 ]] && echo "(DRY RUN — no files will be written)"
echo "===================================================="
echo ""

cd /workspaces/sideguy-solutions || exit 1

DATE=$(date +"%Y-%m-%d")

########################################
# HELPERS
########################################

run() {
  # run CMD... — skips execution in dry-run mode
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

write_file() {
  # write_file PATH CONTENT — skips in dry-run; no-ops if file already exists
  local path="$1" content="$2"
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] would write: $path"
  elif [[ ! -f "$path" ]]; then
    printf '%s\n' "$content" > "$path"
  fi
}

########################################
# DIRECTORIES
########################################

if [[ $DRY_RUN -eq 0 ]]; then
  mkdir -p seo-reserve/million-expansion
  mkdir -p public/auto
  mkdir -p docs/million-expansion/logs
  mkdir -p docs/auto-builder/logs
  mkdir -p docs/intelligence/reports
  mkdir -p docs/intelligence/logs
  mkdir -p docs/future-systems/{manifests,research,logs}
  mkdir -p seo-reserve/future-systems
else
  echo "[dry-run] would create required directories"
fi

########################################
# 1. MILLION EXPANSION ENGINE
########################################

echo "Generating expansion paths..."

TECH=(robotics automation ai-agents machine-economy smart-factories autonomous-vehicles energy-automation industrial-ai digital-factories robot-micro-factories)
INDUSTRIES=(restaurants warehouses construction manufacturing hospitals hotels retail logistics farming delivery security maintenance cleaning)
USECASES=(automation robots integration software roi cost systems consulting tools future)

TOTAL_PATHS=$(( ${#TECH[@]} * ${#INDUSTRIES[@]} * ${#USECASES[@]} ))
OUTPUT="seo-reserve/million-expansion/future-page-paths.md"

if [[ $DRY_RUN -eq 1 ]]; then
  echo "[dry-run] would generate $TOTAL_PATHS paths → $OUTPUT"
else
  > "$OUTPUT"
  for tech in "${TECH[@]}"; do
    for industry in "${INDUSTRIES[@]}"; do
      for use in "${USECASES[@]}"; do
        echo "/${tech}-${industry}-${use}/" >> "$OUTPUT"
      done
    done
  done
  echo "Expansion paths ready ($TOTAL_PATHS) → $OUTPUT"
fi

########################################
# 2. AUTO PAGE BUILDER (SAFE LIMIT)
########################################

echo ""

if [[ $NO_BUILD -eq 1 ]]; then
  echo "[SKIP] Auto page builder disabled (--no-build)"
else
  echo "Building pages (limit: $LIMIT)..."

  TEMPLATE="seo-template.html"
  OUTPUT_DIR="public/auto"
  COUNT=0

  if [[ ! -f "$TEMPLATE" ]]; then
    echo "[SKIP] Template $TEMPLATE not found — skipping auto page builder"
  elif [[ $DRY_RUN -eq 1 ]]; then
    # In dry-run mode the expansion file was never written; estimate from path count
    echo "[dry-run] would build up to $LIMIT pages → $OUTPUT_DIR/ (from $OUTPUT)"
  else
    while IFS= read -r PAGE; do
      SLUG="${PAGE//\//}"
      [[ -z "$SLUG" ]] && continue
      FILE="$OUTPUT_DIR/$SLUG.html"

      if [[ ! -f "$FILE" ]]; then
        cp "$TEMPLATE" "$FILE"
        sed -i "s|{{PAGE_TITLE}}|$SLUG|g" "$FILE"
        sed -i "s|{{PAGE_SLUG}}|$SLUG|g" "$FILE"
        sed -i "s|{{BUILD_DATE}}|$DATE|g" "$FILE"
        COUNT=$((COUNT + 1))
      fi

      [[ $COUNT -ge $LIMIT ]] && break
    done < "$OUTPUT"

    echo "$COUNT pages built → $OUTPUT_DIR/"
    echo "$DATE : $COUNT pages built" >> docs/auto-builder/logs/build.log
  fi
fi

########################################
# 3. PRIORITY ENGINE
########################################

echo ""
echo "Running priority scan..."

PRIORITY="docs/intelligence/reports/page-priority-$DATE.txt"
HTML_COUNT=$(find public -name "*.html" 2>/dev/null | wc -l)

if [[ $HTML_COUNT -eq 0 ]]; then
  echo "[SKIP] No HTML files found in public/ — skipping priority scan"
elif [[ $DRY_RUN -eq 1 ]]; then
  echo "[dry-run] would score $HTML_COUNT HTML files → $PRIORITY"
else
  > "$PRIORITY"

  while IFS= read -r f; do
    LINKS=$(grep -o "<a " "$f" | wc -l)
    FAQ=$(grep -ic "faq" "$f" 2>/dev/null || echo 0)
    WORDS=$(wc -w < "$f")
    SCORE=$((LINKS + (FAQ * 5) + (WORDS / 100)))
    echo "$SCORE : $f" >> "$PRIORITY"
  done < <(find public -name "*.html")

  # Sort to temp file first — avoids read/write conflict on same file
  PRIORITY_TMP=$(mktemp)
  sort -nr "$PRIORITY" | head -20 > "$PRIORITY_TMP"
  { echo ""; echo "Top pages:"; cat "$PRIORITY_TMP"; } >> "$PRIORITY"
  rm -f "$PRIORITY_TMP"

  echo "Priority report ($HTML_COUNT pages scored) → $PRIORITY"
fi

########################################
# 4. FUTURE SYSTEMS AUTHORITY
########################################

echo ""
echo "Installing future systems cluster..."

write_file "docs/future-systems/README.md" \
"SideGuy Future Systems

AI explains.
Humans decide.

Clarity before cost."

write_file "seo-reserve/future-systems/core.md" \
"/systems-for-business/
/business-automation-systems/
/production-efficiency-systems/
/ai-and-automation-for-business/
/software-and-robotics-integration/"

if [[ $DRY_RUN -eq 0 ]]; then
  echo "$DATE future systems installed" >> docs/future-systems/logs/future-systems.log
fi

echo "Future systems cluster ready"

########################################
# DONE
########################################

echo ""
echo "===================================================="
echo "SIDEGUY EXPANSION CORE COMPLETE"
[[ $DRY_RUN -eq 1 ]] && echo "(DRY RUN — nothing was written)"
echo "===================================================="
echo ""
echo "Outputs:"
echo "- Expansion paths → seo-reserve/million-expansion/"
echo "- New pages     → public/auto/ (skipped with --no-build)"
echo "- Priority report → docs/intelligence/reports/"
echo "- Future systems → docs/future-systems/"
echo ""
