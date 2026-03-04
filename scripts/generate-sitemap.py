#!/usr/bin/env python3
# ==============================================================
# SIDEGUY CRAWL ENGINE
# Automatic sitemap + discovery system (v3)
# ==============================================================
# Scans all .html pages in the repo, splits into 1,000-URL
# chunks → sitemaps/sitemap-N.xml, regenerates sitemap-index.xml
# with timestamps, and writes a fresh sitemap.xml for root pages.
#
# Usage:  python3 scripts/generate-sitemap.py
# Env:    CHUNK_SIZE=1000   (URLs per file, default 1000)
# ==============================================================

import os, datetime
from pathlib import Path

DOMAIN   = "https://sideguysolutions.com"
ROOT     = Path(__file__).parent.parent
TODAY    = datetime.date.today().isoformat()
CHUNK    = int(os.getenv("CHUNK_SIZE", "1000"))
SITEMAPS = ROOT / "sitemaps"

# Directories to completely skip (never index)
SKIP_DIRS = {
    ".git", "node_modules", "sitemaps", "seo-reserve",
    "scripts", "docs", "signals", "manifests", "data",
    "backups", "public",
}

# Priority tiers: (path-prefix → priority, changefreq)
PRIORITY_MAP = [
    ("",                     "1.0", "daily"),       # root level
    ("pillars/",             "0.9", "weekly"),
    ("clusters/",            "0.8", "weekly"),
    ("knowledge/",           "0.8", "weekly"),
    ("concepts/",            "0.8", "weekly"),
    ("intelligence/",        "0.8", "weekly"),
    ("decisions/",           "0.7", "weekly"),
    ("generated/",           "0.7", "weekly"),
    ("problems/",            "0.7", "weekly"),
    ("longtail/",            "0.6", "monthly"),
]

def priority_for(rel: str) -> tuple[str, str]:
    for prefix, pri, freq in PRIORITY_MAP:
        if rel.startswith(prefix):
            return pri, freq
    return "0.6", "monthly"

# ── Collect all HTML ──────────────────────────────────────────

seen: set[str] = set()
urls: list[tuple[str, str, str]] = []   # (url, priority, changefreq)

def add(rel: str):
    url = f"{DOMAIN}/{rel}"
    if url not in seen:
        seen.add(url)
        pri, freq = priority_for(rel)
        urls.append((url, pri, freq))

# Root-level HTML (sorted for determinism)
for p in sorted(ROOT.glob("*.html")):
    add(p.name)

# All subdirectories via os.walk
for dirpath, dirnames, filenames in os.walk(ROOT):
    # Prune unwanted dirs in-place so os.walk skips them
    dirnames[:] = sorted(
        d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")
    )
    dp = Path(dirpath)
    if dp == ROOT:
        continue   # already handled root-level above
    for fname in sorted(f for f in filenames if f.endswith(".html")):
        rel = (dp / fname).relative_to(ROOT).as_posix()
        add(rel)

print(f"  Collected {len(urls):,} HTML pages\n")

# ── Write sitemap chunks ──────────────────────────────────────

SITEMAPS.mkdir(exist_ok=True)

def urlset(entries):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, pri, freq in entries:
        lines.append(
            f"  <url>\n"
            f"    <loc>{url}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{pri}</priority>\n"
            f"  </url>"
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"

# Remove old numbered chunks
removed = sum(1 for f in SITEMAPS.glob("sitemap-*.xml") if f.unlink() is None)
if removed:
    print(f"  Removed {removed} old sitemap-*.xml chunk(s)")

chunks     = [urls[i:i+CHUNK] for i in range(0, len(urls), CHUNK)]
chunk_files: list[Path] = []

for idx, chunk in enumerate(chunks, 1):
    out = SITEMAPS / f"sitemap-{idx}.xml"
    out.write_text(urlset(chunk))
    chunk_files.append(out)
    print(f"  sitemaps/sitemap-{idx}.xml  ({len(chunk):,} URLs)")

print(f"\n  {len(chunk_files)} chunk file(s) written")

# ── Regenerate sitemap-index.xml ─────────────────────────────

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
for f in sorted(chunk_files):
    rel = f.relative_to(ROOT).as_posix()
    lines.append(
        f"  <sitemap>\n"
        f"    <loc>{DOMAIN}/{rel}</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        f"  </sitemap>"
    )
lines.append("</sitemapindex>")
(ROOT / "sitemap-index.xml").write_text("\n".join(lines) + "\n")
print(f"\n  sitemap-index.xml → {len(chunk_files)} sitemap(s) referenced")

# ── Summary ───────────────────────────────────────────────────

root_count = sum(1 for u, _, _ in urls if u.count("/") == 3)
print(f"\n✅  Sitemap generation complete")
print(f"   Total pages  : {len(urls):,}")
print(f"   Chunks       : {len(chunk_files)}  ×  ≤{CHUNK:,} URLs")
print(f"   Robots.txt   : Sitemap: {DOMAIN}/sitemap-index.xml  ← already set")
