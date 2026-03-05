#!/usr/bin/env python3
"""
SideGuy Crawl Budget Optimizer
--------------------------------
Splits public/ HTML pages into two focused sitemaps to guide Google's
crawl budget toward the highest-value pages first.

  public/sitemaps/priority-sitemap.xml  — top 10 clusters, up to 200 URLs each
  public/sitemaps/deep-sitemap.xml      — remaining clusters

URLs use https://sideguysolutions.com/<path> (no www, no trailing slash on path).

Also updates public/sitemaps/sitemap-index.xml so GSC can discover both.
"""

import glob
import os
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT     = Path(__file__).parent.parent.parent.resolve()
BASE_URL = "https://sideguysolutions.com"
OUT_DIR  = ROOT / "public" / "sitemaps"
REPORT   = ROOT / "docs" / "crawl-reports" / "crawl_budget_report.md"

SKIP_DIRS = {
    ".git", "_quarantine_backups", "node_modules", "backup_pages",
    "backup_old_pages", "backups_20251230_191613", "backups",
    "_BACKUPS", ".sideguy-backups", "reports",
}

def skip(p: str) -> bool:
    parts = p.replace(os.sep, "/").split("/")
    return any(d in SKIP_DIRS for d in parts)

def page_url(rel_path: str) -> str:
    url_path = rel_path.replace(os.sep, "/").lstrip("./")
    return f"{BASE_URL}/{url_path}"

# ── Collect and cluster public/ pages ────────────────────────────────────────
clusters: dict[str, list[str]] = defaultdict(list)
for p in sorted(glob.glob(str(ROOT / "public" / "**" / "*.html"), recursive=True)):
    rel = os.path.relpath(p, ROOT)
    if skip(rel):
        continue
    rel_from_public = os.path.relpath(p, ROOT / "public")
    parts = rel_from_public.replace(os.sep, "/").split("/")
    cluster = parts[0] if len(parts) > 1 else "(root)"
    clusters[cluster].append(page_url(rel))

ranked = sorted(clusters.items(), key=lambda x: -len(x[1]))
today  = date.today().isoformat()

priority_urls: list[str] = []
deep_urls: list[str]     = []

for i, (cluster, urls) in enumerate(ranked):
    if i < 10:
        priority_urls.extend(urls[:200])
    else:
        deep_urls.extend(urls)

# ── Write sitemap XML ─────────────────────────────────────────────────────────
def write_sitemap(urls: list[str], path: Path, changefreq: str = "weekly"):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        lines += [
            "  <url>",
            f"    <loc>{url}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <changefreq>{changefreq}</changefreq>",
            "  </url>",
        ]
    lines.append("</urlset>")
    path.write_text("\n".join(lines), encoding="utf-8")

OUT_DIR.mkdir(parents=True, exist_ok=True)
write_sitemap(priority_urls, OUT_DIR / "priority-sitemap.xml", "daily")
write_sitemap(deep_urls,     OUT_DIR / "deep-sitemap.xml",     "weekly")

# ── Sitemap index ─────────────────────────────────────────────────────────────
index_path = OUT_DIR / "sitemap-index.xml"
index_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    f'  <sitemap><loc>{BASE_URL}/sitemaps/priority-sitemap.xml</loc><lastmod>{today}</lastmod></sitemap>',
    f'  <sitemap><loc>{BASE_URL}/sitemaps/deep-sitemap.xml</loc><lastmod>{today}</lastmod></sitemap>',
    '</sitemapindex>',
]
index_path.write_text("\n".join(index_lines), encoding="utf-8")

# ── Report ────────────────────────────────────────────────────────────────────
REPORT.parent.mkdir(parents=True, exist_ok=True)
report_lines = [
    "# Crawl Budget Optimization Report",
    "",
    f"Generated: {today}",
    "",
    f"| Sitemap | URLs | Priority |",
    f"|---|---:|---|",
    f"| `public/sitemaps/priority-sitemap.xml` | {len(priority_urls):,} | High (daily) |",
    f"| `public/sitemaps/deep-sitemap.xml` | {len(deep_urls):,} | Normal (weekly) |",
    "",
    "## Top 10 priority clusters",
    "",
]
for i, (cluster, urls) in enumerate(ranked[:10], 1):
    capped = min(len(urls), 200)
    report_lines.append(f"{i}. `{cluster}` — {len(urls)} pages ({capped} in priority sitemap)")
report_lines += [
    "",
    "## Next steps",
    "1. Submit `public/sitemaps/sitemap-index.xml` to GSC → Sitemaps",
    "2. Submit `public/sitemaps/priority-sitemap.xml` directly for faster crawl",
    "",
]
REPORT.write_text("\n".join(report_lines), encoding="utf-8")

print(f"Crawl budget optimizer complete")
print(f"  Priority URLs : {len(priority_urls):,}")
print(f"  Deep URLs     : {len(deep_urls):,}")
print(f"  Sitemaps      : {OUT_DIR.relative_to(ROOT)}/")
print(f"  Report        : {REPORT.relative_to(ROOT)}")
