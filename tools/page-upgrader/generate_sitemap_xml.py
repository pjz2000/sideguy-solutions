#!/usr/bin/env python3
"""
SideGuy XML Sitemap Generator
Scans all HTML pages and writes sitemap.xml and sitemap-index.xml.
Excludes: backups, quarantine, node_modules, .git, noindex pages.
"""
from pathlib import Path
from datetime import date
import re

ROOT     = Path("/workspaces/sideguy-solutions")
BASE_URL = "https://sideguysolutions.com"
TODAY    = date.today().isoformat()

EXCLUDE_DIRS = {
    "backups_20251230_191613", "backup_pages", "backup_old_pages",
    "_quarantine_backups", "node_modules", ".git", "crawl-sitemaps",
}

EXCLUDE_PATTERNS = re.compile(r'backup|\.backup\.|\.bak', re.IGNORECASE)

def is_noindex(text: str) -> bool:
    return bool(re.search(r'<meta[^>]+robots[^>]+noindex', text, re.IGNORECASE))

def url_priority(path: Path) -> str:
    stem = path.stem.lower()
    if path.parent == ROOT:           return "0.8"
    if "hubs" in str(path):           return "0.7"
    if "problems" in str(path):       return "0.6"
    if "pages" in str(path):          return "0.6"
    if "public/auto" in str(path):    return "0.5"
    return "0.5"

def to_url(path: Path) -> str:
    rel = path.relative_to(ROOT)
    return f"{BASE_URL}/{rel.as_posix()}"

pages_found = []

for p in ROOT.rglob("*.html"):
    # Skip excluded directories
    parts = set(p.relative_to(ROOT).parts)
    if parts & EXCLUDE_DIRS:
        continue
    if EXCLUDE_PATTERNS.search(p.name):
        continue
    try:
        text = p.read_text(errors="ignore")
    except Exception:
        continue
    if is_noindex(text):
        continue
    pages_found.append(p)

pages_found.sort(key=lambda p: str(p))

print(f"Pages to index: {len(pages_found)}")

# Write sitemap.xml
sitemap_path = ROOT / "sitemap.xml"
with sitemap_path.open("w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in pages_found:
        url  = to_url(p)
        prio = url_priority(p)
        f.write(f"  <url>\n")
        f.write(f"    <loc>{url}</loc>\n")
        f.write(f"    <lastmod>{TODAY}</lastmod>\n")
        f.write(f"    <changefreq>monthly</changefreq>\n")
        f.write(f"    <priority>{prio}</priority>\n")
        f.write(f"  </url>\n")
    f.write("</urlset>\n")

print(f"Written: sitemap.xml ({len(pages_found)} URLs)")

# Update sitemap-index.xml if it exists
index_path = ROOT / "sitemap-index.xml"
if index_path.exists():
    index_text = index_path.read_text()
    # Update lastmod on the primary sitemap entry
    index_text = re.sub(
        r'(<loc>[^<]*sitemap\.xml</loc>\s*<lastmod>)[^<]*(</lastmod>)',
        rf'\g<1>{TODAY}\g<2>',
        index_text
    )
    index_path.write_text(index_text)
    print(f"Updated: sitemap-index.xml lastmod → {TODAY}")
