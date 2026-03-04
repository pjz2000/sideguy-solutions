#!/usr/bin/env python3
# ==============================================================
# SIDEGUY SITE INVENTORY + ORPHAN DETECTOR
# ==============================================================
# - Counts HTML pages by folder (inventory)
# - Builds an internal link graph
# - Reports orphaned pages (zero incoming internal links)
#
# Output:
#   reports/site-inventory.json   — folder counts + orphan list
#   reports/orphans.txt           — one slug per line, sorted by folder
#
# Usage:  python3 scripts/site-inventory.py
# ==============================================================

import os, re, json, collections
from pathlib import Path

ROOT     = Path(__file__).parent.parent
REPORTS  = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

SKIP_DIRS = {
    "node_modules", ".git", ".next", "dist", "build",
    ".vercel", "__pycache__", "reports", "scripts",
    "seo-reserve", "signals", "docs", "manifests", "data",
}

HREF_RE = re.compile(r'href\s*=\s*["\']([^"\'#?]+)["\']', re.IGNORECASE)

# ── Collect all HTML ──────────────────────────────────────────

def collect_pages() -> list[str]:
    pages = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in sorted(dirnames)
                       if d not in SKIP_DIRS and not d.startswith(".")]
        dp = Path(dirpath)
        for f in sorted(f for f in filenames if f.endswith(".html")):
            rel = (dp / f).relative_to(ROOT).as_posix()
            pages.append(rel)
    return pages

pages     = collect_pages()
page_set  = set(pages)

print(f"  Collected {len(pages):,} HTML pages")

# ── Folder inventory ──────────────────────────────────────────

folder_counts: collections.Counter = collections.Counter()
for p in pages:
    folder = p.split("/")[0] if "/" in p else "(root)"
    folder_counts[folder] += 1

# ── Link graph ────────────────────────────────────────────────

def normalize_href(href: str) -> str:
    href = href.strip()
    if not href or href.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
        return ""
    href = href.split("#")[0].split("?")[0].strip("/")
    if not href:
        return "index.html"
    # bare dir → index.html
    if not href.endswith(".html"):
        candidate_html  = href + ".html"
        candidate_index = href + "/index.html"
        if candidate_html in page_set:
            href = candidate_html
        elif candidate_index in page_set:
            href = candidate_index
        else:
            return ""
    # normalize
    return href.lstrip("/")

incoming: collections.Counter = collections.Counter()
outgoing: dict[str, int]      = {}

for p in pages:
    try:
        txt = (ROOT / p).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    links: set[str] = set()
    for href in HREF_RE.findall(txt):
        nh = normalize_href(href)
        if nh and nh in page_set and nh != p:
            links.add(nh)
    outgoing[p] = len(links)
    for nh in links:
        incoming[nh] += 1

# ── Orphan detection ─────────────────────────────────────────

NEVER_ORPHAN = {"index.html", "404.html", "sitemap.html"}

orphans = sorted(
    p for p in page_set
    if p not in NEVER_ORPHAN
    and incoming[p] == 0
)

print(f"  Orphans: {len(orphans):,} pages with zero incoming internal links")

# ── Reports ───────────────────────────────────────────────────

report = {
    "generated":           __import__("datetime").date.today().isoformat(),
    "total_pages":         len(pages),
    "counts_by_folder":    dict(folder_counts.most_common()),
    "orphans_count":       len(orphans),
    "orphans_sample":      orphans[:200],
    "most_linked": [
        {"page": p, "incoming": c}
        for p, c in sorted(incoming.items(), key=lambda x: -x[1])[:25]
    ],
    "least_linked_built_pages": [
        {"page": p, "outgoing": outgoing.get(p, 0)}
        for p in sorted(pages, key=lambda x: outgoing.get(x, 0))[:25]
    ],
}

(REPORTS / "site-inventory.json").write_text(
    json.dumps(report, indent=2) + "\n"
)

(REPORTS / "orphans.txt").write_text(
    "\n".join(orphans) + "\n"
)

# ── Terminal summary ──────────────────────────────────────────

print(f"\n  Folder counts (top 15):")
for folder, cnt in folder_counts.most_common(15):
    print(f"    {folder:<30} {cnt:>5,}")

print(f"\n  Most-linked pages:")
for item in report["most_linked"][:10]:
    print(f"    [{item['incoming']:>4}] {item['page']}")

print(f"\n  Top orphans to wire (first 20):")
for o in orphans[:20]:
    print(f"    {o}")

print(f"\n✅  Inventory complete")
print(f"   reports/site-inventory.json")
print(f"   reports/orphans.txt  ({len(orphans):,} orphans)")
