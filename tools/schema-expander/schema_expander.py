#!/usr/bin/env python3
"""
Schema Expander — SideGuy Solutions
==================================
Injects rich schema (FAQ, HowTo, Product, Review, Event) into public HTML pages.
Idempotent: skips pages already containing schema blocks.
Writes a summary to docs/schema-expander/schema_report.txt.
"""
from pathlib import Path
import random

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
REPORT = ROOT / "docs" / "schema-expander" / "schema_report.txt"
SCHEMA_MARKER = "<!-- SideGuy Schema Block -->"
SCHEMA_TYPES = ["FAQ", "HowTo", "Product", "Review", "Event"]

updated = 0
skipped = 0
for page in PUBLIC.rglob("*.html"):
    text = page.read_text(errors="ignore")
    if SCHEMA_MARKER in text:
        skipped += 1
        continue
    schema_type = random.choice(SCHEMA_TYPES)
    block = f"\n{SCHEMA_MARKER}\n<script type='application/ld+json'>{{'@context':'https://schema.org','@type':'{schema_type}','name':'{page.name}','description':'SideGuy Solutions {schema_type} schema'}} </script>\n"
    if "</body>" in text:
        text = text.replace("</body>", block + "</body>")
        page.write_text(text)
        updated += 1
with REPORT.open("w") as f:
    f.write(f"Schema injected: {updated} pages, {skipped} skipped\n")
print(f"Schema injected: {updated} pages, {skipped} skipped")
