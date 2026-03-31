#!/usr/bin/env python3
"""
_run_sitemap.py — Regenerate sitemaps for sideguysolutions.com
- Covers all HTML files in repo root + docs/pages/
- Assigns priority by page type
- Splits into 50k-URL shards
- Writes sitemap-index.xml
"""

import os, glob, math
from datetime import date

BASE_URL = "https://sideguysolutions.com"
ROOT = "/Users/kromeon/sideguy-solutions"
TODAY = date.today().isoformat()
SHARD_SIZE = 50000
SITEMAP_DIR = os.path.join(ROOT, "sitemaps")
os.makedirs(SITEMAP_DIR, exist_ok=True)

# Priority rules — matched in order, first match wins
PRIORITY_RULES = [
    # Core hubs — highest value
    (1.0, ["index.html", "san-diego-payment-processing.html",
           "San-Diego-Payment-Processing.html", "ai-automation-workflows-san-diego.html",
           "san-diego-county-payment-processing.html", "best-payment-processor-san-diego-restaurants.html",
           "best-payment-processor-san-diego-contractors.html", "best-payment-processor-san-diego-retail.html",
           "google-business-profile-san-diego.html", "san-diego-county-small-business-guide.html"]),
    # Calculators and tools
    (0.9, ["-calculator-", "-roi-calculator-", "-fee-calculator-", "-calculator."]),
    # City payment + AI pages
    (0.8, ["-payment-processing.", "-credit-card-processing.", "-ai-tools.", "-small-business-ai-tools."]),
    # Neighborhood + industry pages
    (0.7, ["-payment-processing-san-diego.", "-hvac-contractor.", "-solar-installer.",
           "-small-business-tips.", "restaurant-", "salon-", "dentist-", "plumber-",
           "electrician-", "hvac-contractor-", "solar-installer-", "food-truck-",
           "landscaper-", "cleaning-service-"]),
    # Longtail / reddit signal / faq / meme
    (0.6, []),  # catch-all
]

def get_priority(filename):
    name = os.path.basename(filename)
    for priority, patterns in PRIORITY_RULES:
        if not patterns:
            return priority
        for p in patterns:
            if p in name or name == p:
                return priority
    return 0.6

def collect_urls():
    urls = []

    # Root HTML files
    for f in glob.glob(os.path.join(ROOT, "*.html")):
        name = os.path.basename(f)
        # Skip backup/template files
        if any(x in name for x in ["pre-meme-share", "seo-template", "backup", "-hub.html"]):
            continue
        rel = name
        urls.append((f"{BASE_URL}/{rel}", get_priority(name)))

    # docs/pages/ HTML files
    for f in glob.glob(os.path.join(ROOT, "docs", "pages", "*.html")):
        name = os.path.basename(f)
        urls.append((f"{BASE_URL}/docs/pages/{name}", get_priority(name)))

    # memes/
    for f in glob.glob(os.path.join(ROOT, "memes", "*.html")):
        name = os.path.basename(f)
        urls.append((f"{BASE_URL}/memes/{name}", 0.7))

    return urls

def write_shard(urls, shard_num):
    path = os.path.join(SITEMAP_DIR, f"sitemap-{shard_num}.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url, priority in urls:
            f.write(f'  <url>\n')
            f.write(f'    <loc>{url}</loc>\n')
            f.write(f'    <lastmod>{TODAY}</lastmod>\n')
            f.write(f'    <changefreq>weekly</changefreq>\n')
            f.write(f'    <priority>{priority}</priority>\n')
            f.write(f'  </url>\n')
        f.write('</urlset>\n')
    return path

def write_index(shard_count):
    path = os.path.join(ROOT, "sitemap-index.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for i in range(1, shard_count + 1):
            f.write(f'  <sitemap>\n')
            f.write(f'    <loc>{BASE_URL}/sitemaps/sitemap-{i}.xml</loc>\n')
            f.write(f'    <lastmod>{TODAY}</lastmod>\n')
            f.write(f'  </sitemap>\n')
        f.write('</sitemapindex>\n')
    return path

def write_root_sitemap(urls):
    """Write a root sitemap.xml with top 50k priority pages for quick discovery."""
    sorted_urls = sorted(urls, key=lambda x: x[1], reverse=True)[:50000]
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url, priority in sorted_urls:
            f.write(f'  <url>\n')
            f.write(f'    <loc>{url}</loc>\n')
            f.write(f'    <lastmod>{TODAY}</lastmod>\n')
            f.write(f'    <changefreq>weekly</changefreq>\n')
            f.write(f'    <priority>{priority}</priority>\n')
            f.write(f'  </url>\n')
        f.write('</urlset>\n')

if __name__ == "__main__":
    print("Collecting URLs...")
    urls = collect_urls()
    print(f"  Total URLs: {len(urls)}")

    # Priority breakdown
    from collections import Counter
    dist = Counter(p for _, p in urls)
    for p in sorted(dist.keys(), reverse=True):
        print(f"  Priority {p}: {dist[p]:,}")

    # Write sharded sitemaps
    shards = math.ceil(len(urls) / SHARD_SIZE)
    print(f"Writing {shards} shard(s) of up to {SHARD_SIZE:,} URLs each...")
    for i in range(shards):
        chunk = urls[i * SHARD_SIZE:(i + 1) * SHARD_SIZE]
        write_shard(chunk, i + 1)
        print(f"  sitemaps/sitemap-{i+1}.xml ({len(chunk):,} URLs)")

    # Write sitemap-index.xml
    idx = write_index(shards)
    print(f"Written: {idx}")

    # Write root sitemap.xml (top 50k by priority)
    write_root_sitemap(urls)
    print(f"Written: sitemap.xml (top 50k by priority)")

    print("Done.")
