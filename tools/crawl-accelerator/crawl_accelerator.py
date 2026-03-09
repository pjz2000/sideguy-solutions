#!/usr/bin/env python3
"""
Crawl Accelerator — SideGuy Solutions
Builds a navigable index hub at public/auto/index.html for all auto/ pages
and inserts their URLs into sitemap.xml before the closing </urlset> tag.

Fixes applied vs. original spec:
  - Sitemap URLs are inserted before </urlset> (not appended after it, which
    would produce invalid XML).
  - URL base uses sideguysolutions.com (no www), consistent with site canonicals.
  - Hub page is valid HTML5 with meta charset and canonical.
  - Skip URLs already present in the sitemap to keep it idempotent.
"""
from pathlib import Path
from datetime import date

ROOT    = Path("/workspaces/sideguy-solutions")
AUTO    = ROOT / "public/auto"
HUB     = AUTO / "index.html"
SITEMAP = ROOT / "public/sitemap.xml"
BASE    = "https://sideguysolutions.com"
TODAY   = date.today().isoformat()

pages = sorted(AUTO.glob("*.html"))
pages = [p for p in pages if p.name != "index.html"]

# ── Build the hub index ────────────────────────────────────────────────────────
link_items = ""
for p in pages:
    url  = f"{BASE}/public/auto/{p.name}"
    slug = p.stem.replace("-", " ").title()
    link_items += f'    <li><a href="{url}">{slug}</a></li>\n'

hub_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>AI Automation Guides · SideGuy Solutions</title>
  <meta name="description" content="Directory of AI automation guides for San Diego businesses — HVAC, plumbing, dental, and more."/>
  <link rel="canonical" href="{BASE}/public/auto/index.html"/>
  <meta name="robots" content="index,follow"/>
  <style>
    body{{font-family:-apple-system,system-ui,sans-serif;max-width:860px;margin:0 auto;padding:40px 24px;color:#073044}}
    h1{{font-size:1.8rem;margin-bottom:8px}}
    p.lede{{color:#3f6173;margin-bottom:28px}}
    ul{{list-style:none;padding:0;display:flex;flex-direction:column;gap:8px}}
    li a{{display:block;padding:10px 16px;background:#f0faff;border:1px solid #cce8f4;border-radius:10px;color:#1f7cff;text-decoration:none;font-size:.95rem}}
    li a:hover{{background:#daf0ff}}
    footer{{margin-top:40px;font-size:.8rem;color:#3f6173}}
  </style>
</head>
<body>
  <h1>AI Automation Guides</h1>
  <p class="lede">Industry-specific guides covering AI scheduling, chatbots, invoicing, and follow-up automation.</p>
  <ul>
{link_items}  </ul>
  <footer><a href="{BASE}">SideGuy Solutions</a> · Updated {TODAY}</footer>
</body>
</html>
"""

HUB.write_text(hub_html)
print(f"Hub written: {HUB} ({len(pages)} links)")

# ── Update sitemap — insert before </urlset> ───────────────────────────────────
sitemap_text = SITEMAP.read_text()

# Collect URLs not yet in the sitemap
new_urls = []
for p in pages:
    url = f"{BASE}/public/auto/{p.name}"
    if url not in sitemap_text:
        new_urls.append(url)

if new_urls:
    insert_block = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>0.5</priority></url>"
        for u in new_urls
    )
    sitemap_text = sitemap_text.replace(
        "</urlset>",
        insert_block + "\n</urlset>"
    )
    SITEMAP.write_text(sitemap_text)
    print(f"Sitemap updated: {len(new_urls)} new URLs added")
else:
    print("Sitemap: all URLs already present, no changes")

print("Crawl accelerator complete")
