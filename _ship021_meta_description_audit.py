#!/usr/bin/env python3
"""
SHIP-021: Meta Description Audit — Detect duplicate or missing meta descriptions in all HTML files.
Outputs a report listing files with duplicate or missing meta descriptions.
"""
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
html_files = [f for f in os.listdir(ROOT) if f.endswith('.html')]
desc_map = defaultdict(list)
missing = []

meta_re = re.compile(r'<meta\s+name="description"\s+content="([^"]+)"', re.IGNORECASE)

def get_meta_desc(content):
    m = meta_re.search(content)
    return m.group(1).strip() if m else None

for fname in html_files:
    fpath = os.path.join(ROOT, fname)
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    desc = get_meta_desc(content)
    if not desc:
        missing.append(fname)
    else:
        desc_map[desc].append(fname)

# Write report
report_path = os.path.join(ROOT, 'SHIP-021-meta-description-report.txt')
with open(report_path, 'w') as rep:
    rep.write('Meta Description Audit Report\n')
    rep.write('============================\n\n')
    if missing:
        rep.write(f'Missing meta description ({len(missing)} files):\n')
        for fname in missing:
            rep.write(f'  ✗ {fname}\n')
        rep.write('\n')
    dupes = {desc: files for desc, files in desc_map.items() if len(files) > 1}
    if dupes:
        rep.write(f'Duplicate meta descriptions ({len(dupes)} unique, {sum(len(files) for files in dupes.values())} files):\n')
        for desc, files in dupes.items():
            rep.write(f'  "{desc}"\n')
            for fname in files:
                rep.write(f'    ✓ {fname}\n')
            rep.write('\n')
    if not missing and not dupes:
        rep.write('All meta descriptions are unique and present.\n')
print(f"Meta description audit complete. See SHIP-021-meta-description-report.txt.")
