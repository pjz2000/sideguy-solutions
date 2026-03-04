#!/usr/bin/env python3
"""
SIDEGUY Sitemap Generator  (v2 — full-scan, auto-chunked)
Scans ALL *.html in root + subdirs (problems, concepts, clusters, etc.),
splits into chunks of max CHUNK_SIZE URLs, writes sitemaps/auto-NNN.xml,
and regenerates sitemap-index.xml referencing both sitemap.xml + all auto files.

Usage:
  python3 scripts/generate-sitemap.py

Env:
  CHUNK_SIZE=1000   URLs per chunk (default 1000)
"""

import os, sys, datetime
from pathlib import Path

DOMAIN    = "https://sideguysolutions.com"
ROOT      = Path(__file__).parent.parent
TODAY     = datetime.date.today().isoformat()
CHUNK     = int(os.getenv("CHUNK_SIZE", "1000"))
SITEMAPS  = ROOT / "sitemaps"

INCLUDE_SUBDIRS = [
    "problems", "concepts", "clusters", "generated",
    "intelligence", "decisions", "pillars", "knowledge",
    "longtail",
]

# ── Collect ───────────────────────────────────────────────────────────────────

seen = set()
urls = []

def add(rel: str):
    url = f"{DOMAIN}/{rel}"
    if url not in seen:
        seen.add(url)
        urls.append(url)

# root-level HTML
for f in sorted(ROOT.glob("*.html")):
    add(f.name)

# subdirectories
for sub in INCLUDE_SUBDIRS:
    subdir = ROOT / sub
    if subdir.is_dir():
        for p in sorted(subdir.rglob("*.html")):
            add(p.relative_to(ROOT).as_posix())

print(f"  Collected {len(urls):,} HTML pages\n")

# ── Write chunks ──────────────────────────────────────────────────────────────

SITEMAPS.mkdir(exist_ok=True)

# remove old auto chunks
removed = 0
for f in SITEMAPS.glob("auto-*.xml"):
    f.unlink(); removed += 1
if removed:
    print(f"  Removed {removed} old auto-*.xml files")

chunks    = [urls[i:i+CHUNK] for i in range(0, len(urls), CHUNK)]
auto_files = []
for idx, chunk in enumerate(chunks, 1):
    out = SITEMAPS / f"auto-{idx:03d}.xml"
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in chunk:
        lines.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>")
    lines.append("</urlset>")
    out.write_text("\n".join(lines) + "\n")
    auto_files.append(out)
    print(f"  {out.name}  ({len(chunk)} URLs)")

print(f"\n  {len(auto_files)} chunk files written")

# ── Regenerate sitemap-index.xml ──────────────────────────────────────────────

index_path = ROOT / "sitemap-index.xml"
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
# primary sitemap always first
lines.append(f"  <sitemap>\n    <loc>{DOMAIN}/sitemap.xml</loc>\n    <lastmod>{TODAY}</lastmod>\n  </sitemap>")
for f in sorted(auto_files):
    rel = f.relative_to(ROOT).as_posix()
    lines.append(f"  <sitemap>\n    <loc>{DOMAIN}/{rel}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </sitemap>")
lines.append("</sitemapindex>")
index_path.write_text("\n".join(lines) + "\n")
print(f"\n  sitemap-index.xml → {len(auto_files)+1} sitemaps listed")
print(f"\n✅ Sitemap generation complete — {len(urls):,} total URLs")
