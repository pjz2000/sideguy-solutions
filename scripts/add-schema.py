"""
SideGuy Schema + OG Engine
Injects JSON-LD schema and Open Graph meta tags into every HTML page that lacks them.
Safe to re-run: skips pages that already have both.
"""
import os, re

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN  = "https://sideguysolutions.com"

LOCAL_BIZ = """{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "SideGuy Solutions",
  "url": "https://sideguysolutions.com",
  "telephone": "+1-773-544-1231",
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
DESC_RE  = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', re.IGNORECASE | re.DOTALL)

def make_schema(page_url, title):
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

def make_og(page_url, title, description):
    t = title.replace('"', '&quot;')
    d = description.replace('"', '&quot;')
    return (
        f'\n<meta property="og:type" content="article"/>\n'
        f'<meta property="og:site_name" content="SideGuy Solutions"/>\n'
        f'<meta property="og:title" content="{t}"/>\n'
        f'<meta property="og:description" content="{d}"/>\n'
        f'<meta property="og:url" content="{page_url}"/>\n'
        f'<meta name="twitter:card" content="summary"/>\n'
        f'<meta name="twitter:title" content="{t}"/>\n'
        f'<meta name="twitter:description" content="{d}"/>\n'
    )

schema_added = 0
og_added     = 0
skipped      = 0

for dirpath, _, files in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT)
    skip_dirs = {"_quarantine_backups", "node_modules", "seo-reserve"}
    parts = rel.split(os.sep)
    if any(p.startswith(".") or p in skip_dirs for p in parts):
        continue

    for fname in files:
        if not fname.endswith(".html"):
            continue

        fpath    = os.path.join(dirpath, fname)
        rel_path = os.path.relpath(fpath, ROOT).replace("\\", "/")
        page_url = f"{DOMAIN}/{rel_path}"

        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        changed = False

        # ── JSON-LD schema ────────────────────────────────────────────────────
        if "application/ld+json" not in html:
            m     = TITLE_RE.search(html)
            title = m.group(1).strip() if m else fname.replace(".html", "").replace("-", " ").title()
            html  = html.replace("</head>", make_schema(page_url, title) + "</head>", 1)
            schema_added += 1
            changed = True

        # ── Open Graph tags ───────────────────────────────────────────────────
        if 'property="og:title"' not in html and "property='og:title'" not in html:
            m_title = TITLE_RE.search(html)
            m_desc  = DESC_RE.search(html)
            title   = m_title.group(1).strip() if m_title else fname.replace(".html", "").replace("-", " ").title()
            desc    = m_desc.group(1).strip() if m_desc else f"{title} — SideGuy Solutions, San Diego."
            html    = html.replace("</head>", make_og(page_url, title, desc) + "</head>", 1)
            og_added += 1
            changed = True

        if not changed:
            skipped += 1
            continue

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)

print(f"Schema added: {schema_added}  |  OG tags added: {og_added}  |  Already complete: {skipped}")

