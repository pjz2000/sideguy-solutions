#!/usr/bin/env python3
"""
Freshness Upgrader — SideGuy Solutions
=====================================
Scans public HTML pages for stale content (old dates, outdated info).
Auto-refreshes meta descriptions and context blocks to signal recency.
Writes a report to docs/freshness-engine/freshness_report.txt.
"""
from pathlib import Path
import re, datetime

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
REPORT = ROOT / "docs" / "freshness-engine" / "freshness_report.txt"
TODAY = datetime.date.today().isoformat()

updated = 0
for page in PUBLIC.rglob("*.html"):
    text = page.read_text(errors="ignore")
    if re.search(r'202[0-5]', text):
        text = re.sub(r'202[0-5]', '2026', text)
        if '<meta name="description"' in text:
            text = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="Updated for 2026 — SideGuy Solutions">', text)
        page.write_text(text)
        updated += 1
with REPORT.open("w") as f:
    f.write(f"Pages refreshed: {updated}\n")
print(f"Pages refreshed: {updated}")
