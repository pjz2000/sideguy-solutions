#!/usr/bin/env python3
"""
FAQ/Schema Injector — SideGuy Solutions
=======================================
Injects FAQPage JSON-LD schema and a simple FAQ block into public/ pages.
Idempotent: skips pages already containing FAQ schema.

Run after builder/context steps for SEO rich results.
"""
from pathlib import Path
import random

ROOT = Path("/workspaces/sideguy-solutions/public")
FAQ_MARKER = "FAQPage JSON-LD"

FAQS = [
    ("What is AI automation?", "AI automation uses software to handle repetitive tasks, saving time and reducing errors."),
    ("How can AI help my business?", "AI can automate scheduling, reminders, lead followup, and more, improving efficiency."),
    ("Is AI expensive?", "Most small businesses start with $50-200/month for basic automations."),
    ("Can AI automate office memes?", "Yes, meme generators and content tools can create fun, engaging office memes automatically."),
]

pages = list(ROOT.rglob("*.html"))
updated = 0
skipped = 0

for page in pages:
    text = page.read_text(errors="ignore")
    if FAQ_MARKER in text:
        skipped += 1
        continue
    faq_block = "\n<!-- FAQPage JSON-LD -->\n<script type=\"application/ld+json\">\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"FAQPage\",\n  \"mainEntity\": [\n" + \
        ",\n".join(f"    {{\n      '@type': 'Question',\n      'name': '{q}',\n      'acceptedAnswer': {{'@type': 'Answer', 'text': '{a}'}}\n    }}" for q,a in FAQS) + \
        "\n  ]\n}\n</script>\n<div class=\"sideguy-faq\" style=\"background:#fffbe6;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;\">\n  <strong>FAQ:</strong>\n  <ul>" + \
        "".join(f"<li><strong>{q}</strong><br>{a}</li>" for q,a in FAQS) + \
        "</ul>\n</div>\n"
    if "</body>" in text:
        text = text.replace("</body>", faq_block + "</body>", 1)
        page.write_text(text)
        updated += 1

print(f"FAQ/schema injector: {updated} pages updated, {skipped} already marked.")
