"""
HTML Sitemap Builder
----------------------
Generates paginated HTML sitemaps from root-level HTML pages.
These help Google discover pages via crawl links (not just XML sitemaps).

Output: crawl-sitemaps/sitemap-{n}.html  (200 pages per file)
Each page has a title, proper meta, and linked filenames.

Usage: python3 tools/crawl-multiplier/html_sitemap_builder.py
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "crawl-sitemaps"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SKIP = {"crawl-map.html", "authority.html", "fresh.html", "new-prolem-x.html", "404.html"}
CHUNK_SIZE = 200

pages = sorted(
    f for f in os.listdir(ROOT)
    if f.endswith(".html") and f not in SKIP
)

chunks = [pages[i:i + CHUNK_SIZE] for i in range(0, len(pages), CHUNK_SIZE)]
total_chunks = len(chunks)

for i, chunk in enumerate(chunks):
    chunk_num = i + 1
    fname = OUT_DIR / f"sitemap-{chunk_num}.html"

    prev_link = f'<a href="/crawl-sitemaps/sitemap-{chunk_num - 1}.html">← Previous</a>' if chunk_num > 1 else ""
    next_link = f'<a href="/crawl-sitemaps/sitemap-{chunk_num + 1}.html">Next →</a>' if chunk_num < total_chunks else ""

    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow" />
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>SideGuy Problem Index — Page {chunk_num} of {total_chunks} · San Diego</title>
<link rel="canonical" href="https://sideguysolutions.com/crawl-sitemaps/sitemap-{chunk_num}.html"/>
<meta name="description" content="Browse SideGuy problem pages — page {chunk_num} of {total_chunks}. Real-world problems solved across AI, payments, home systems, and software in San Diego."/>
<style>
  body{{font-family:-apple-system,system-ui,sans-serif;background:#eefcff;color:#073044;padding:24px 16px 48px;max-width:900px;margin:0 auto}}
  h1{{font-size:1.6rem;font-weight:800;margin-bottom:8px}}
  p.sub{{color:#2a5068;margin-bottom:24px;font-size:.95rem}}
  ul{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:6px}}
  li a{{display:block;padding:7px 12px;border-radius:6px;background:#fff;color:#0a7abf;text-decoration:none;font-size:.88rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;box-shadow:0 1px 3px rgba(0,0,0,.07)}}
  li a:hover{{text-decoration:underline}}
  nav{{display:flex;gap:24px;margin-top:32px;font-size:.9rem}}
  nav a{{color:#0a7abf;font-weight:700}}
  footer{{margin-top:32px;font-size:.82rem;color:#5e7d8e}}
</style>
</head>
<body>
<h1>SideGuy Problem Index — Page {chunk_num} of {total_chunks}</h1>
<p class="sub">Showing {len(chunk)} pages · <a href="/crawl-map.html">← Back to Problem Map</a></p>
<ul>
""")
        for page in chunk:
            label = page.replace("-san-diego.html", "").replace("-", " ").replace(".html", "").title()
            f.write(f'  <li><a href="/{page}" title="{label}">{label}</a></li>\n')

        f.write(f"""</ul>
<nav>
  {prev_link}
  {next_link}
</nav>
<footer>
  <p>SideGuy Solutions · <a href="/">sideguysolutions.com</a> · Text PJ: <a href="tel:+17735441231">773-544-1231</a></p>
</footer>
</body>
</html>
""")

print(f"HTML sitemap builder complete")
print(f"  Chunks     : {total_chunks}")
print(f"  Pages      : {len(pages)}")
print(f"  Output dir : crawl-sitemaps/")
