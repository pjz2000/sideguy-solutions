"""
SideGuy Schema Engine
Injects JSON-LD LocalBusiness + WebPage schema into every HTML page
that doesn't already have application/ld+json.
"""
import os, re

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN  = "https://sideguysolutions.com"
PHONE   = "+1-760-454-1860"

LOCAL_BIZ = """{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "SideGuy Solutions",
  "url": "https://sideguysolutions.com",
  "telephone": "+1-760-454-1860",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "San Diego",
    "addressRegion": "CA",
    "addressCountry": "US"
  },
  "areaServed": "United States",
  "sameAs": ["https://sideguysolutions.com"]
}"""

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)

def make_schema(html, page_url, title):
    webpage = f"""{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "{title.replace('"', "'")}",
  "url": "{page_url}",
  "isPartOf": {{"@type": "WebSite", "url": "https://sideguysolutions.com"}}
}}"""
    return (
        f'\n<script type="application/ld+json">\n{LOCAL_BIZ}\n</script>\n'
        f'<script type="application/ld+json">\n{webpage}\n</script>\n'
    )

added = 0
skipped = 0

for dirpath, _, files in os.walk(ROOT):
    # skip hidden dirs, backups, quarantine
    rel = os.path.relpath(dirpath, ROOT)
    skip_dirs = {"_quarantine_backups", "node_modules", "seo-reserve"}
    parts = rel.split(os.sep)
    if any(p.startswith(".") or p in skip_dirs for p in parts):
        continue

    for fname in files:
        if not fname.endswith(".html"):
            continue

        fpath = os.path.join(dirpath, fname)
        rel_path = os.path.relpath(fpath, ROOT).replace("\\", "/")

        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        if "application/ld+json" in html:
            skipped += 1
            continue

        page_url = f"{DOMAIN}/{rel_path}"
        m = TITLE_RE.search(html)
        title = m.group(1).strip() if m else fname.replace(".html", "").replace("-", " ").title()

        schema_block = make_schema(html, page_url, title)
        html = html.replace("</head>", schema_block + "</head>", 1)

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        added += 1

print(f"Schema added to {added} pages ({skipped} already had schema).")
