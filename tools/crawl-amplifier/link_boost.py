"""
Crawl Amplifier — Targeted Internal Link Booster
-------------------------------------------------
Adds a "Explore more problems" footer link to SPECIFIC high-value pages
(not all 13,545 pages). Target list is curated manually to avoid bulk
injection that could look manipulative to Google.

Usage:
  python3 tools/crawl-amplifier/link_boost.py [--dry-run]

Safety:
  - Only touches pages in TARGETS list below
  - --dry-run flag shows changes without writing
  - Skips any file that already contains the link
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRY_RUN = "--dry-run" in sys.argv

INSERT_HTML = (
    "\n<!-- crawl-amplifier -->\n"
    "<p style='text-align:center;margin:32px 0 0;font-size:.9rem;color:#5e7d8e'>"
    "<a href='/crawl-map.html' style='color:#0a7abf'>Explore more SideGuy problem topics →</a>"
    "</p>\n"
)

# Curated high-value hub pages only — do NOT expand to bulk/all pages
TARGETS = [
    "payment-processing-san-diego-hub.html",
    "tech-help-hub-san-diego.html",
    "hvac-problems-hub-san-diego.html",
    "plumbing-problems-hub-san-diego.html",
    "electrical-problems-hub-san-diego.html",
    "home-repair-hub-san-diego.html",
    "software-development-hub-san-diego.html",
    "contractor-services-hub-san-diego.html",
    "roofing-hub-san-diego.html",
    "solar-hub-san-diego.html",
    "ai-business-solutions-san-diego.html",
    "ai-lead-generation-systems-san-diego.html",
    "mobile-payment-processing.html",
    "contractor-payment-processing.html",
]

updated = []
skipped = []

for filename in TARGETS:
    path = ROOT / filename
    if not path.exists():
        skipped.append(f"{filename} (not found)")
        continue

    text = path.read_text(encoding="utf-8", errors="ignore")

    if "crawl-map.html" in text:
        skipped.append(f"{filename} (already linked)")
        continue

    if "</body>" not in text:
        skipped.append(f"{filename} (no </body> tag)")
        continue

    new_text = text.replace("</body>", INSERT_HTML + "</body>", 1)

    if DRY_RUN:
        print(f"[dry-run] Would update: {filename}")
    else:
        path.write_text(new_text, encoding="utf-8")
        updated.append(filename)

print(f"\nCrawl amplifier link boost {'(dry run) ' if DRY_RUN else ''}complete")
print(f"  Updated : {len(updated)}")
print(f"  Skipped : {len(skipped)}")
for f in updated:
    print(f"  ✓ {f}")
for f in skipped:
    print(f"  ✗ {f}")
