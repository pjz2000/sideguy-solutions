#!/bin/bash

MANIFEST="$1"

if [ -z "$MANIFEST" ]; then
  echo "Usage:"
  echo "bash tools/factory/page-factory.sh manifests/factory/page-factory-example.csv"
  exit
fi

if [ ! -f "$MANIFEST" ]; then
  echo "Manifest not found: $MANIFEST"
  exit
fi

STAMP=$(date +"%Y-%m-%d %H:%M:%S")
BASENAME=$(basename "$MANIFEST" .csv)

OUTDIR="pages/factory"
LOG="logs/factory/$BASENAME-build.log"
REPORT="reports/factory/$BASENAME-report.md"
DOC="docs/factory/$BASENAME-factory-doc.md"

mkdir -p "$OUTDIR" logs/factory reports/factory docs/factory

echo "" >> "$LOG"
echo "=== SideGuy Page Factory Run $STAMP ===" >> "$LOG"
echo "Manifest: $MANIFEST" >> "$LOG"
echo "" >> "$LOG"

tail -n +2 "$MANIFEST" | while IFS=',' read page_type slug title parent category intent
do
  FILE="$OUTDIR/$slug.html"

  if [ -f "$FILE" ]; then
    echo "SKIP existing: $slug" >> "$LOG"
    continue
  fi

  if [ -z "$slug" ]; then
    continue
  fi

  PARENT_LINK="/factory/$parent.html"
  CANONICAL="https://sideguysolutions.com/factory/$slug.html"

  cat > "$FILE" <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>$title | SideGuy</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="$title explained in clear, calm language for operators, business owners, and normal people.">
<link rel="canonical" href="$CANONICAL">
</head>
<body>

<h1>$title</h1>

<p>SideGuy explains <strong>$title</strong> in calm, useful language so people can understand changing systems without hype or confusion.</p>

<p>This page is part of a larger SideGuy topic cluster focused on clarity before cost, practical understanding, and real-world decision support.</p>

<h2>What This Means</h2>
<p>$title is part of a broader shift in how software, payments, automation, infrastructure, and business systems work. Many operators hear these terms long before they get a clean explanation.</p>

<h2>Why It Matters</h2>
<p>Understanding new systems early helps businesses, homeowners, and operators make better decisions before the market gets crowded and confusing.</p>

<h2>Real-World Context</h2>
<p>Some pages in this cluster focus on basics, some focus on decisions, some on local use cases, and some on future direction. Together they help SideGuy build strong topic authority without relying on spammy copy.</p>

<h2>Quick Take</h2>
<ul>
<li>Understand the system before paying for it</li>
<li>Compare new rails to old workflows</li>
<li>Watch incentives, pricing, and implementation friction</li>
<li>Use calm explanation before making expensive decisions</li>
</ul>

<h2>Related Pages</h2>
<ul>
<li><a href="$PARENT_LINK">Parent Hub</a></li>
<li><a href="/factory/$parent-faq.html">$parent FAQ</a></li>
<li><a href="/factory/future-of-$parent.html">Future of $parent</a></li>
<li><a href="/factory/$parent-for-small-business.html">$parent for Small Business</a></li>
</ul>

<h2>FAQ</h2>
<p><strong>Is this already mainstream?</strong><br>Sometimes yes, sometimes not. SideGuy tracks systems early so people can understand what is real before the hype cycle peaks.</p>

<p><strong>Who is this for?</strong><br>Operators, business owners, curious normal people, and anyone trying to make better decisions without wasting money.</p>

<p><strong>What does SideGuy do here?</strong><br>AI explains. Human resolves. SideGuy helps translate confusing systems into practical next steps.</p>

<h2>Need Help?</h2>
<p><strong>Text PJ:</strong> 773-544-1231</p>
<p>Clarity before cost.</p>

</body>
</html>
HTML

  echo "CREATED: $slug" >> "$LOG"
done

TOTAL=$(($(wc -l < "$MANIFEST") - 1))
CREATED_COUNT=$(grep -c '^CREATED:' "$LOG" 2>/dev/null || echo 0)
SKIPPED_COUNT=$(grep -c '^SKIP existing:' "$LOG" 2>/dev/null || echo 0)

cat > "$REPORT" <<EOF2
# SideGuy Page Factory Report

## Timestamp
$STAMP

## Manifest
$MANIFEST

## Totals
- Rows in manifest: $TOTAL
- Pages created: $CREATED_COUNT
- Pages skipped: $SKIPPED_COUNT

## Output Directory
$OUTDIR

## Log
$LOG

## Notes
This factory creates starter pages only.

Recommended next steps:
1. Strengthen the hub page first
2. Add internal links intentionally
3. Run publish gate before sitemap promotion
4. Move strongest pages into live clusters
EOF2

cat > "$DOC" <<EOF2
# SideGuy Page Factory

## Purpose
Generate starter pages at scale from a manifest.

## Command
bash tools/factory/page-factory.sh $MANIFEST

## Inputs
CSV columns: page_type, slug, title, parent, category, intent

## Output
- HTML pages in $OUTDIR
- Log in $LOG
- Report in $REPORT

## Workflow
1. Build from manifest
2. Upgrade strongest pages
3. Run publish gate
4. Link to hubs
5. Add only qualified pages to sitemap
EOF2

echo ""
echo "======================================"
echo "SIDEGUY PAGE FACTORY COMPLETE"
echo "======================================"
echo ""
echo "Manifest: $MANIFEST"
echo "Rows:     $TOTAL"
echo "Created:  $CREATED_COUNT"
echo "Skipped:  $SKIPPED_COUNT"
echo ""
echo "Pages:    $OUTDIR"
echo "Report:   $REPORT"
echo "Log:      $LOG"
