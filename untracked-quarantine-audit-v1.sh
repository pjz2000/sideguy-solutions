#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

echo "======================================"
echo "SIDEGUY UNTRACKED QUARANTINE AUDIT v1"
echo "======================================"

STAMP="$(date +%Y%m%d-%H%M%S)"
REPORT="docs/untracked-audit-$STAMP.md"
mkdir -p docs quarantine

########################################
# SNAPSHOT UNTRACKED FILES
########################################
git ls-files --others --exclude-standard > quarantine/untracked-$STAMP.txt

TOTAL=$(wc -l < quarantine/untracked-$STAMP.txt | tr -d ' ')
echo "Total untracked files: $TOTAL" | tee "$REPORT"

########################################
# SAMPLE FIRST 50 HTML FILES
########################################
grep '\.html$' quarantine/untracked-$STAMP.txt | head -50 > quarantine/sample-$STAMP.txt
SAMPLE_TOTAL=$(wc -l < quarantine/sample-$STAMP.txt | tr -d ' ')

echo "" >> "$REPORT"
echo "## Sample Pages ($SAMPLE_TOTAL)" >> "$REPORT"
cat quarantine/sample-$STAMP.txt >> "$REPORT"

########################################
# AUTO-CLASSIFY SUSPECT BULK FILES
########################################
grep -E 'newsletter|anyone-rely|bulk|auto|tmp' quarantine/untracked-$STAMP.txt \
  > quarantine/suspect-$STAMP.txt || true

SUSPECT_TOTAL=$(wc -l < quarantine/suspect-$STAMP.txt | tr -d ' ')
echo "" >> "$REPORT"
echo "Suspect bulk pages: $SUSPECT_TOTAL" | tee -a "$REPORT"

########################################
# OPTIONAL GITIGNORE SAFETY NET
########################################
if ! grep -q "newsletter" .gitignore 2>/dev/null; then
  {
    echo ""
    echo "# quarantine bulk temp pages"
    echo "*newsletter*.html"
    echo "*anyone-rely*.html"
    echo "*bulk*.html"
  } >> .gitignore
fi

echo "" >> "$REPORT"
echo "Next move: inspect quarantine/sample-$STAMP.txt" >> "$REPORT"
echo "Safe recommendation: batch-delete only low-quality suspects" >> "$REPORT"

echo "======================================"
echo "DONE: quarantine snapshot created"
echo "Report: $REPORT"
echo "No tracked production pages touched"
echo "======================================"
