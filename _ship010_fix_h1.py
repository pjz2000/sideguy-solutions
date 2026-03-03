#!/usr/bin/env python3
"""
SHIP-010 Phase 1: Fix broken <h1>in San Diego X</h1> → <h1>X in San Diego</h1>
across all root-level HTML files.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {'docs', 'backup-who-do-i-call-20251229-1838', 'seo-reserve', 'site', 'pages', 'signals', 'data', '.git', 'partials'}

pattern = re.compile(r'<h1>in San Diego (.*?)</h1>', re.IGNORECASE)

fixed = []
skipped = []

for fname in os.listdir(ROOT):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(ROOT, fname)
    try:
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            original = f.read()
    except Exception as e:
        skipped.append((fname, str(e)))
        continue

    def fix_h1(m):
        subject = m.group(1).strip()
        return f'<h1>{subject} in San Diego</h1>'

    updated = pattern.sub(fix_h1, original)

    if updated != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(updated)
        fixed.append(fname)

print(f"Fixed {len(fixed)} files:")
for f in sorted(fixed):
    print(f"  ✓ {f}")
if skipped:
    print(f"\nSkipped {len(skipped)}:")
    for f, e in skipped:
        print(f"  ✗ {f}: {e}")
