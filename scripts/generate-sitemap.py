#!/usr/bin/env python3
"""
SideGuy Sitemap Generator
Produces:
  sitemap.xml                  — all root .html pages (main sitemap)
  sitemaps/sitemap-pages.xml   — same as above (named copy in /sitemaps/)
  sitemaps/sitemap-hubs.xml    — /hubs/*.html pages
  sitemaps/sitemap-pillars.xml — /pillars/*.html pages
  sitemap_index.xml            — points to the four sitemaps above
"""

import os, datetime

DOMAIN  = "https://sideguysolutions.com"
ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY   = datetime.date.today().isoformat()

SKIP_PREFIXES = ("aaa-", "_")
SKIP_FILES    = {"404.html", "hub-template.html"}

os.makedirs(os.path.join(ROOT, "sitemaps"), exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def write_urlset(filepath, urls):
    with open(filepath, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in urls:
            f.write(f"  <url>\n")
            f.write(f"    <loc>{url}</loc>\n")
            f.write(f"    <lastmod>{TODAY}</lastmod>\n")
            f.write(f"  </url>\n")
        f.write("</urlset>\n")
    print(f"  {os.path.relpath(filepath, ROOT)} — {len(urls)} URLs")

# ── Collect pages ─────────────────────────────────────────────────────────────

root_pages = sorted(
    f"{DOMAIN}/{f}"
    for f in os.listdir(ROOT)
    if f.endswith(".html")
    and not any(f.startswith(p) for p in SKIP_PREFIXES)
    and f not in SKIP_FILES
)

hubs_dir = os.path.join(ROOT, "hubs")
hub_pages = []
if os.path.isdir(hubs_dir):
    hub_pages = sorted(
        f"{DOMAIN}/hubs/{f}"
        for f in os.listdir(hubs_dir)
        if f.endswith(".html")
    )

pillars_dir = os.path.join(ROOT, "pillars")
pillar_pages = []
if os.path.isdir(pillars_dir):
    pillar_pages = sorted(
        f"{DOMAIN}/pillars/{f}"
        for f in os.listdir(pillars_dir)
        if f.endswith(".html")
    )

kg_hubs_dir = os.path.join(ROOT, "kg", "hubs")
kg_pages = []
if os.path.isdir(kg_hubs_dir):
    kg_pages = sorted(
        f"{DOMAIN}/kg/hubs/{f}"
        for f in os.listdir(kg_hubs_dir)
        if f.endswith(".html")
    )

# ── Write individual sitemaps ─────────────────────────────────────────────────

print("Writing sitemaps...")
write_urlset(os.path.join(ROOT, "sitemap.xml"), root_pages)
write_urlset(os.path.join(ROOT, "sitemaps", "sitemap-pages.xml"),   root_pages)
write_urlset(os.path.join(ROOT, "sitemaps", "sitemap-hubs.xml"),    hub_pages)
write_urlset(os.path.join(ROOT, "sitemaps", "sitemap-pillars.xml"), pillar_pages)
os.makedirs(os.path.join(ROOT, "sitemaps"), exist_ok=True)
if kg_pages:
    write_urlset(os.path.join(ROOT, "sitemaps", "sitemap-kg.xml"), kg_pages)

# ── Write sitemap_index.xml ───────────────────────────────────────────────────

index_path = os.path.join(ROOT, "sitemap_index.xml")
sitemaps = [
    f"{DOMAIN}/sitemaps/sitemap-pages.xml",
    f"{DOMAIN}/sitemaps/sitemap-hubs.xml",
    f"{DOMAIN}/sitemaps/sitemap-pillars.xml",
]
if kg_pages:
    sitemaps.append(f"{DOMAIN}/sitemaps/sitemap-kg.xml")

with open(index_path, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for sm in sitemaps:
        f.write(f"  <sitemap>\n")
        f.write(f"    <loc>{sm}</loc>\n")
        f.write(f"    <lastmod>{TODAY}</lastmod>\n")
        f.write(f"  </sitemap>\n")
    f.write("</sitemapindex>\n")

print(f"  sitemap_index.xml — {len(sitemaps)} sitemaps")
print(f"\n✅ Sitemap generation complete.")
print(f"   Root pages:    {len(root_pages)}")
print(f"   Hub pages:     {len(hub_pages)}")
print(f"   Pillar pages:  {len(pillar_pages)}")
print(f"   Total indexed: {len(root_pages) + len(hub_pages) + len(pillar_pages)}")
