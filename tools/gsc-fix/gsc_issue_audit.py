#!/usr/bin/env python3
"""
SideGuy GSC Issue Audit
------------------------
Reads routing/Critical issues.csv (GSC Coverage export) and generates
an actionable Markdown report with per-issue action plans.

CSV columns: Reason, Source, Validation, Pages
"""

import csv
from pathlib import Path

ROOT   = Path(__file__).parent.parent.parent.resolve()
INPUT  = ROOT / "routing" / "Critical issues.csv"
OUTPUT = ROOT / "docs" / "gsc-reports" / "gsc_issue_report.md"

ACTION_MAP = {
    "Not found (404)":                         "Export URL list from GSC → Pages (filter Not found) and create redirects or restore pages",
    "Duplicate without user-selected canonical":"Verify <link rel='canonical'> points to the correct self-URL on every duplicate (fixer already ran: 3,457 fixed)",
    "Soft 404":                                "Find pages returning HTTP 200 with thin/empty content → add real content or return a proper 404",
    "Page with redirect":                      "Update internal links pointing to these URLs to use the final destination directly",
    "Redirect error":                          "Check redirect chain for loops or broken targets",
    "Alternate page with proper canonical tag":"Expected behaviour — page correctly defers to its canonical; no action needed",
    "Discovered - currently not indexed":      "Waiting on Google crawl — resubmit sitemap.xml in GSC → Sitemaps to accelerate",
    "Crawled - currently not indexed":         "Review page quality: thin content, no internal links, or blocked by robots? Add value or consolidate",
}

def priority(reason: str) -> str:
    if "404" in reason or "Soft 404" in reason or "Redirect error" in reason:
        return "🔴 Fix now"
    if "Duplicate" in reason:
        return "🟠 Already fixed (verify)"
    if "Crawled" in reason:
        return "🟡 Review quality"
    return "🟢 Monitor"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

rows = []
if INPUT.exists():
    with open(INPUT, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)

lines = [
    "# GSC Issue Report — March 5, 2026",
    "",
    f"Source: `{INPUT.relative_to(ROOT)}`",
    "",
    "| Priority | Reason | Source | Pages | Action |",
    "|---|---|---|---:|---|",
]
total_pages = 0
for r in rows:
    reason   = r.get("Reason", "").strip()
    source   = r.get("Source", "").strip()
    pages    = r.get("Pages", "0").strip()
    action   = ACTION_MAP.get(reason, "Review manually")
    pri      = priority(reason)
    try:
        total_pages += int(pages)
    except ValueError:
        pass
    lines.append(f"| {pri} | {reason} | {source} | {pages} | {action} |")

lines += [
    "",
    f"**Total affected pages: {total_pages:,}**",
    "",
    "---",
    "",
    "## Recommended fix order",
    "",
    "1. **404s (86 pages)** — Export the specific URLs from GSC and restore or redirect",
    "2. **Soft 404s (4 pages)** — Add real content or return proper 404 status",
    "3. **Redirect error (1 page)** — Find and break the redirect loop",
    "4. **Duplicate canonical (90 pages)** — Already fixed by `tools/coverage-fixer/gsc_coverage_fixer.py`",
    "5. **Discovered not indexed (1,280 pages)** — Resubmit sitemap; wait 2–4 weeks",
    "",
]

OUTPUT.write_text("\n".join(lines), encoding="utf-8")
print(f"GSC issue report generated: {OUTPUT.relative_to(ROOT)}")
for r in rows:
    print(f"  {r.get('Pages','?'):>5} pages — {r.get('Reason','?')}")
