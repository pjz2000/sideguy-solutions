"""
Internal Link Amplifier — Targeted authority.html footer link
--------------------------------------------------------------
Adds an "Explore the SideGuy problem network" footer link to
SPECIFIC hub pages only. NOT run on all 13,545 pages to avoid
bulk injection patterns.

Usage:
  python3 tools/crawl-multiplier/link_amplifier.py [--dry-run]

Safety:
  - Only touches pages in TARGETS list
  - --dry-run shows what would change without writing
  - Skips files that already contain the link
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRY_RUN = "--dry-run" in sys.argv

INSERT_HTML = (
    "\n<!-- crawl-multiplier -->\n"
    "<p style='text-align:center;margin:32px 0 0;font-size:.9rem;color:#5e7d8e'>"
    "<a href='/authority.html' style='color:#0a7abf'>Explore the SideGuy problem network →</a>"
    "</p>\n"
)

# Curated hub pages only — do NOT expand to bulk/all pages
TARGETS = [
    "crawl-map.html",
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
    "sideguy.html",
]

updated, skipped = [], []

for filename in TARGETS:
    path = ROOT / filename
    if not path.exists():
        skipped.append(f"{filename} (not found)")
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "authority.html" in text:
        skipped.append(f"{filename} (already linked)")
        continue
    if "</body>" not in text:
        skipped.append(f"{filename} (no </body>)")
        continue
    new_text = text.replace("</body>", INSERT_HTML + "</body>", 1)
    if DRY_RUN:
        print(f"[dry-run] Would update: {filename}")
    else:
        path.write_text(new_text, encoding="utf-8")
        updated.append(filename)

print(f"\nLink amplifier {'(dry run) ' if DRY_RUN else ''}complete")
print(f"  Updated : {len(updated)}")
print(f"  Skipped : {len(skipped)}")
for f in updated:  print(f"  ✓ {f}")
for f in skipped: print(f"  ✗ {f}")
