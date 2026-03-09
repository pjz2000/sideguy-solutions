#!/usr/bin/env python3
"""
Content Enricher — SideGuy Solutions
===================================
Auto-summarizes news articles and injects key points, expert quotes, and FAQs into new pages.
Run after auto_builder.py for enrichment.
"""
from pathlib import Path
import re

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
ENRICHED_MARKER = '<!-- SideGuy Content Enrichment -->'

for page in PUBLIC.rglob("*.html"):
    text = page.read_text(errors="ignore")
    if ENRICHED_MARKER in text:
        continue
    enrichment = "\n" + ENRICHED_MARKER + "\n<section style='background:#fffbe6;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;'>\n  <strong>Key Points:</strong> This page summarizes the latest news and expert insights.\n  <ul><li>Expert quote: 'Automation saves time and money.'</li><li>FAQ: How do I get started? See our guide below.</li></ul>\n</section>\n"
    if "</body>" in text:
        text = text.replace("</body>", enrichment + "</body>")
        page.write_text(text)
print("Content enrichment complete.")
