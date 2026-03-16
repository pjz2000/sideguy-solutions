#!/usr/bin/env python3
"""
SideGuy Authority Gravity Engine
Scans all HTML pages, counts internal links, and reports:
  - Top authority hub candidates (most links out)
  - Weak pages needing more internal links
  - Orphaned pages (zero inbound links from other pages)
Run: python3 tools/gravity/authority-gravity-engine.py [pages_dir]
"""
import os
import re
import sys
from collections import defaultdict
from datetime import date

PAGES_DIR = sys.argv[1] if len(sys.argv) > 1 else "."
REPORT    = "docs/gravity/gravity-report.md"
RAW_CSV   = "logs/gravity/raw-links.csv"
LOG       = "logs/gravity/gravity.log"

os.makedirs("docs/gravity", exist_ok=True)
os.makedirs("logs/gravity", exist_ok=True)

# ── Scan ──────────────────────────────────────────────────────────────────────
outbound  = {}   # slug → count of internal href links
inbound   = defaultdict(int)  # slug → count of inbound links from other pages

html_re   = re.compile(r'href=["\']/?([^"\'#?]+\.html)["\']', re.I)

pages = []
for dirpath, _, files in os.walk(PAGES_DIR):
    for f in files:
        if f.endswith(".html"):
            pages.append((f, os.path.join(dirpath, f)))

for slug, filepath in pages:
    try:
        content = open(filepath, encoding="utf-8", errors="ignore").read()
    except Exception:
        continue
    hrefs = html_re.findall(content)
    # strip path prefixes — keep only the basename
    targets = [os.path.basename(h) for h in hrefs if h != slug]
    outbound[slug] = len(targets)
    for t in targets:
        inbound[t] += 1

all_slugs = {s for s, _ in pages}

# ── CSV ───────────────────────────────────────────────────────────────────────
with open(RAW_CSV, "w") as f:
    f.write("page,outbound,inbound\n")
    for slug in sorted(all_slugs):
        f.write(f"{slug},{outbound.get(slug,0)},{inbound.get(slug,0)}\n")

# ── Report ────────────────────────────────────────────────────────────────────
sorted_out = sorted(all_slugs, key=lambda s: outbound.get(s, 0), reverse=True)
weak       = [s for s in all_slugs if outbound.get(s, 0) < 3]
hubs       = [s for s in all_slugs if outbound.get(s, 0) > 15]
orphans    = [s for s in all_slugs if inbound.get(s, 0) == 0]

lines = [
    "# SideGuy Authority Gravity Report",
    f"\nGenerated: {date.today()} | Pages scanned: {len(all_slugs)}",
    "\n---\n",
    "## Top Authority Hub Candidates (outbound links > 15)\n",
]
for s in sorted(hubs, key=lambda x: outbound[x], reverse=True)[:30]:
    lines.append(f"- `{s}` → {outbound[s]} out / {inbound.get(s,0)} in")

lines += [
    "\n---\n",
    "## Weak Pages — Need More Internal Links (outbound < 3)\n",
    f"Total: {len(weak)} pages\n",
]
for s in sorted(weak, key=lambda x: inbound.get(x, 0), reverse=True)[:50]:
    lines.append(f"- `{s}` → {outbound.get(s,0)} out / {inbound.get(s,0)} in")

lines += [
    "\n---\n",
    "## Orphaned Pages — Zero Inbound Links\n",
    f"Total: {len(orphans)} pages\n",
]
for s in sorted(orphans)[:50]:
    lines.append(f"- `{s}` → {outbound.get(s,0)} out")

lines += [
    "\n---\n",
    "## All Pages — Sorted by Outbound Links\n",
]
for s in sorted_out[:50]:
    lines.append(f"- `{s}` → {outbound.get(s,0)} out / {inbound.get(s,0)} in")

open(REPORT, "w").write("\n".join(lines) + "\n")

with open(LOG, "a") as f:
    f.write(f"Gravity scan {date.today()}: {len(all_slugs)} pages, "
            f"{len(hubs)} hubs, {len(weak)} weak, {len(orphans)} orphans\n")

print(f"\nPages scanned:   {len(all_slugs):,}")
print(f"Hub candidates:  {len(hubs)} (outbound > 15)")
print(f"Weak pages:      {len(weak)} (outbound < 3)")
print(f"Orphaned pages:  {len(orphans)} (zero inbound)")
print(f"\nReport: {REPORT}")
print(f"CSV:    {RAW_CSV}")
