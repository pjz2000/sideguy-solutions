#!/usr/bin/env python3
"""
Realtime Page Logger — SideGuy Solutions
=======================================
Logs every new page built by the auto-builder in real time to docs/trending-topic-engine/realtime_pages.txt.
Run after auto_builder.py for instant visibility.
"""
from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
LOG = ROOT / "docs" / "trending-topic-engine" / "realtime_pages.txt"

# Find all pages built in the last 10 minutes
import time
now = time.time()
recent = []
for page in PUBLIC.rglob("*.html"):
    if page.stat().st_mtime > now - 600:  # 10 minutes
        recent.append(str(page.relative_to(ROOT)))

with LOG.open("w") as f:
    for p in sorted(recent):
        f.write(p + "\n")
print(f"Realtime pages logged: {len(recent)}")
