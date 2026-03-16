#!/bin/bash

echo "Running SideGuy Opportunity Engine"

REPORT="docs/opportunity/opportunity-report.txt"
TOP="docs/opportunity/top-opportunities.txt"

mkdir -p docs/opportunity

echo "SideGuy Opportunity Scan $(date)" > $REPORT
echo "" >> $REPORT

echo "Scanning HTML pages (fast single-pass)..."

python3 << 'PYEOF'
import os, re, glob
from collections import defaultdict

# Single pass: collect all href targets across all HTML files
inbound_counts = defaultdict(int)
# Scope to production pages only — exclude backups, reports, build artifacts
EXCLUDE = ('backup','report','public/','docs/','authority/','hubs/','pillars/',
           '_BACKUPS','node_modules','.git','seo-reserve')
all_raw = glob.glob('**/*.html', recursive=True)
all_files = [f for f in all_raw if not any(x in f for x in EXCLUDE)]

print(f"  Found {len(all_files)} production HTML files (of {len(all_raw)} total), building link map...")

for f in all_files:
    try:
        content = open(f, encoding='utf-8', errors='ignore').read()
        for href in re.findall(r'href="([^"#?]+\.html)"', content):
            basename = os.path.basename(href)
            inbound_counts[basename] += 1
    except:
        pass

print(f"  Link map built. Scoring pages...")

rows = []
for f in all_files:
    try:
        content = open(f, encoding='utf-8', errors='ignore').read()
        words = len(content.split())
        outbound = len(re.findall(r'href="', content))
        inbound = inbound_counts.get(os.path.basename(f), 0)
        score = inbound * 2 + words // 50 - outbound
        rows.append((score, f, inbound, outbound, words))
    except:
        pass

rows.sort(reverse=True)

report_lines = []
for score, f, inbound, outbound, words in rows:
    report_lines.append(f"{score} | {f} | inbound:{inbound} outbound:{outbound} words:{words}")

with open('docs/opportunity/opportunity-report.txt', 'a') as rpt:
    rpt.write('\n'.join(report_lines) + '\n')

top30 = rows[:30]
with open('docs/opportunity/top-opportunities.txt', 'w') as top:
    for score, f, inbound, outbound, words in top30:
        top.write(f"{score} | {f} | inbound:{inbound} outbound:{outbound} words:{words}\n")

print("\nTop opportunity pages:")
for score, f, inbound, outbound, words in top30:
    print(f"  {score:>6} | {f}")

print(f"\nTotal pages scored: {len(rows)}")
PYEOF

echo ""
echo "Saved to:"
echo $TOP
