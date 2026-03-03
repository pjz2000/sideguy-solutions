#!/usr/bin/env python3
"""
SHIP-016: Crawl Budget Reclamation + Canonical Deduplication + City Hub Links

Phase 1 — Noindex non-production pages (templates, admin, backups, test)
Phase 2 — Canonical tags on 32 uppercase URL files → point to lowercase counterparts
Phase 3 — Hub-spoke links: inject city variant links into each of 6 SD quote-review pages
Phase 4 — Remove noindexed pages from sitemap.xml
"""

import os
import re

ROOT = "/workspaces/sideguy-solutions"
BASE_URL = "https://sideguysolutions.com"

# ---------------------------------------------------------------------------
# PHASE 1 — NOINDEX TEMPLATE / ADMIN / TEST / BACKUP PAGES
# ---------------------------------------------------------------------------

NOINDEX_FILES = [
    "_template.html",
    "aaa-PJ-dashboard.html",
    "aaa-blanket-template.html",
    "aaa-help-in-san-diego-handshake.html",
    "aaa-intake.html",
    "aaa-side-guy-help.html",
    "aaa-sideguy-handshake-.html",
    "aaa-test-home.html",
    "clean-template.html",
    "human-solution-template.html",
    "index-backup.html",
    "index-test.html",
    "index-working-backup.html",
    "aaa-global-layout",          # not .html but checking anyway
    "aaa-homepage-test",
    "-hub.html",                   # dash-prefix junk file
]

# Also target any file matching these glob-style patterns
import glob

# Build final noindex list (only real .html files)
noindex_targets = []
for f in NOINDEX_FILES:
    fp = os.path.join(ROOT, f)
    if os.path.isfile(fp) and fp.endswith(".html"):
        noindex_targets.append(fp)

# Also catch any remaining aaa-*.html we might have missed
for fp in glob.glob(os.path.join(ROOT, "aaa-*.html")):
    if fp not in noindex_targets:
        noindex_targets.append(fp)

NOINDEX_TAG = '<meta name="robots" content="noindex, nofollow">'

phase1_updated = 0
phase1_skipped = 0

for fp in noindex_targets:
    with open(fp, "r", encoding="utf-8") as fh:
        content = fh.read()

    # Already has noindex?
    if "noindex" in content.lower():
        phase1_skipped += 1
        continue

    # Inject right after <head> opening tag or before </head>
    if "</head>" in content:
        content = content.replace("</head>", f"  {NOINDEX_TAG}\n</head>", 1)
        with open(fp, "w", encoding="utf-8") as fh:
            fh.write(content)
        phase1_updated += 1
        print(f"  [noindex] {os.path.basename(fp)}")
    else:
        print(f"  [WARN] no </head> in {os.path.basename(fp)}, skip")
        phase1_skipped += 1

print(f"\nPhase 1 done — {phase1_updated} noindexed, {phase1_skipped} already handled\n")

# ---------------------------------------------------------------------------
# PHASE 2 — CANONICAL TAGS ON UPPERCASE DUPLICATE FILES
# ---------------------------------------------------------------------------

def to_lowercase_slug(filename):
    """Convert 'Cardiff-Payment-Processing.html' → 'cardiff-payment-processing.html'"""
    return filename.lower()

uppercase_files = sorted([
    f for f in os.listdir(ROOT)
    if f.endswith(".html") and f[0].isupper()
])

phase2_canonical = 0
phase2_nomate = 0
phase2_skip = 0

for fname in uppercase_files:
    fp = os.path.join(ROOT, fname)
    lowercase_fname = to_lowercase_slug(fname)
    lowercase_fp = os.path.join(ROOT, lowercase_fname)

    # Check lowercase counterpart exists
    if not os.path.isfile(lowercase_fp):
        # No lowercase counterpart — just add noindex since it's probably orphaned
        with open(fp, "r", encoding="utf-8") as fh:
            content = fh.read()
        if "noindex" not in content.lower():
            if "</head>" in content:
                content = content.replace("</head>", f"  {NOINDEX_TAG}\n</head>", 1)
                with open(fp, "w", encoding="utf-8") as fh:
                    fh.write(content)
                print(f"  [noindex-orphan] {fname} (no lowercase counterpart)")
                phase2_nomate += 1
        continue

    # Has lowercase counterpart — add canonical pointing to lowercase URL
    with open(fp, "r", encoding="utf-8") as fh:
        content = fh.read()

    canonical_url = f"{BASE_URL}/{lowercase_fname}"
    canonical_tag = f'<link rel="canonical" href="{canonical_url}">'

    # Already has canonical pointing to lowercase?
    if canonical_url in content:
        phase2_skip += 1
        continue

    # Replace existing canonical if it points to itself (uppercase), else inject
    if 'rel="canonical"' in content:
        # Replace whatever canonical is there
        content = re.sub(
            r'<link\s+rel="canonical"[^>]*>',
            canonical_tag,
            content,
            count=1
        )
    elif "</head>" in content:
        content = content.replace("</head>", f"  {canonical_tag}\n</head>", 1)
    else:
        print(f"  [WARN] no </head> in {fname}")
        continue

    with open(fp, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  [canonical] {fname} → /{lowercase_fname}")
    phase2_canonical += 1

print(f"\nPhase 2 done — {phase2_canonical} canonicals added, {phase2_nomate} orphans noindexed, {phase2_skip} already correct\n")

# ---------------------------------------------------------------------------
# PHASE 3 — HUB-SPOKE: INJECT CITY LINKS INTO 6 SD QUOTE-REVIEW PAGES
# ---------------------------------------------------------------------------

CITY_DATA = {
    "carlsbad": "Carlsbad",
    "encinitas": "Encinitas",
    "oceanside": "Oceanside",
    "la-jolla": "La Jolla",
    "chula-vista": "Chula Vista",
}

TRADE_LABELS = {
    "garage-door":        "Garage Door",
    "roof-repair":        "Roof Repair",
    "kitchen-remodel":    "Kitchen Remodel",
    "window-replacement": "Window Replacement",
    "stucco-repair":      "Stucco Repair",
    "pool-installation":  "Pool Installation",
}

INJECTION_MARKER = "<!-- SIDEGUY_MESH_BLOCK -->"

phase3_updated = 0
phase3_skip = 0

for trade_key, trade_label in TRADE_LABELS.items():
    sd_page = os.path.join(ROOT, f"{trade_key}-quote-review-san-diego.html")
    if not os.path.isfile(sd_page):
        print(f"  [WARN] missing {trade_key}-quote-review-san-diego.html")
        continue

    with open(sd_page, "r", encoding="utf-8") as fh:
        content = fh.read()

    # Already injected?
    if "SHIP-016: City Hub" in content:
        phase3_skip += 1
        continue

    # Build city link list
    city_links = []
    for city_key, city_name in CITY_DATA.items():
        city_page = f"{trade_key}-quote-review-{city_key}.html"
        city_fp = os.path.join(ROOT, city_page)
        if os.path.isfile(city_fp):
            city_links.append(
                f'    <li><a href="/{city_page}">{trade_label} Quote Review — {city_name}</a></li>'
            )

    if not city_links:
        print(f"  [WARN] no city pages found for {trade_key}")
        continue

    city_links_html = "\n".join(city_links)

    nearby_block = f"""
  <!-- SHIP-016: City Hub — auto-injected 2026-03-03 -->
  <section class="section" style="margin-top:2rem;">
    <h2 style="font-size:1.2rem;color:var(--ink);">Serving Greater San Diego — {trade_label} Quote Reviews</h2>
    <p style="color:var(--muted);font-size:0.95rem;margin-bottom:1rem;">
      We cover quote reviews across San Diego County. If you're outside central San Diego,
      check the city-specific page for local permit contacts and adjusted pricing ranges.
    </p>
    <ul style="list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:0.6rem;">
{city_links_html}
    </ul>
  </section>
  <!-- /SHIP-016 -->

  {INJECTION_MARKER}"""

    if INJECTION_MARKER in content:
        content = content.replace(
            f"  {INJECTION_MARKER}",
            nearby_block,
            1
        )
        # Handle case where marker isn't indented
        if INJECTION_MARKER in content:
            content = content.replace(
                INJECTION_MARKER,
                nearby_block.replace(f"  {INJECTION_MARKER}", INJECTION_MARKER),
                1
            )
    else:
        print(f"  [WARN] no MESH_BLOCK marker in {trade_key}-quote-review-san-diego.html")
        continue

    with open(sd_page, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  [hub-spoke] {trade_key}-quote-review-san-diego.html → {len(city_links)} city links")
    phase3_updated += 1

print(f"\nPhase 3 done — {phase3_updated} hub pages updated, {phase3_skip} already done\n")

# ---------------------------------------------------------------------------
# PHASE 4 — REMOVE NOINDEXED PAGES FROM SITEMAP.XML
# ---------------------------------------------------------------------------

sitemap_path = os.path.join(ROOT, "sitemap.xml")
with open(sitemap_path, "r", encoding="utf-8") as fh:
    sitemap = fh.read()

original_count = sitemap.count("<url>")

# Build list of all URLs to remove — noindexed pages
def get_noindexed_slugs():
    slugs = set()
    # Template / admin pages
    for f in noindex_targets:
        slugs.add(os.path.basename(f))
    # Uppercase files that are now canonical'd or noindex'd
    for fname in uppercase_files:
        slugs.add(fname)
    return slugs

slugs_to_remove = get_noindexed_slugs()

# Remove each <url>...</url> block whose <loc> matches a noindexed slug
removed = 0
for slug in slugs_to_remove:
    url_to_remove = f"{BASE_URL}/{slug}"
    # Match the full <url>...</url> block
    pattern = r'\s*<url>\s*<loc>' + re.escape(url_to_remove) + r'</loc>.*?</url>'
    new_sitemap, n = re.subn(pattern, '', sitemap, flags=re.DOTALL)
    if n > 0:
        sitemap = new_sitemap
        removed += n

# Clean up any double blank lines
sitemap = re.sub(r'\n{3,}', '\n\n', sitemap)

with open(sitemap_path, "w", encoding="utf-8") as fh:
    fh.write(sitemap)

final_count = sitemap.count("<url>")
print(f"Phase 4 done — sitemap: {original_count} → {final_count} URLs ({removed} removed)\n")

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
print("=" * 60)
print("SHIP-016 COMPLETE")
print(f"  Phase 1: {phase1_updated} admin/template pages noindexed")
print(f"  Phase 2: {phase2_canonical} uppercase pages canonicalized, {phase2_nomate} orphans noindexed")
print(f"  Phase 3: {phase3_updated} SD hub pages got city spoke links")
print(f"  Phase 4: sitemap pruned → {final_count} production URLs")
print("=" * 60)
