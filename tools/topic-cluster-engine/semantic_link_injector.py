#!/usr/bin/env python3
"""
Semantic Link Injector — SideGuy Solutions
=========================================
Injects a "Related Guides" block into public HTML pages, linking to 3-5 semantically related pages from topic clusters.
Idempotent: skips pages already containing the block.

Run after topic_cluster_builder.py for maximum effect.
"""
from pathlib import Path
import json, random

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
CLUSTERS = ROOT / "docs" / "topic-clusters" / "clusters.json"
MARKER = "<!-- SideGuy Related Guides -->"

with CLUSTERS.open() as f:
    clusters = json.load(f)

pages = list(PUBLIC.rglob("*.html"))
updated = 0
skipped = 0

for page in pages:
    text = page.read_text(errors="ignore")
    if MARKER in text:
        skipped += 1
        continue
    # Find page's topics
    related = set()
    for topic, files in clusters.items():
        if str(page.relative_to(ROOT)) in files:
            related.update(files)
    related.discard(str(page.relative_to(ROOT)))
    if not related:
        continue
    links = random.sample(list(related), min(5, len(related)))
    block = f"\n{MARKER}\n<section style='background:#f0faff;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;'>\n  <strong>Related Guides:</strong>\n  <ul>" + "".join([f"<li><a href='/{l}' style='color:#21d3a1;text-decoration:underline;'>{l.split('/')[-1].replace('.html','').replace('-',' ').title()}</a></li>" for l in links]) + "</ul>\n</section>\n"
    if "</body>" in text:
        text = text.replace("</body>", block + "</body>")
        page.write_text(text)
        updated += 1
print(f"Related Guides injected: {updated} pages, {skipped} skipped.")
