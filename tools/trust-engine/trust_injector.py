#!/usr/bin/env python3
"""
Trust Injector — SideGuy Solutions
==================================
Injects trust badges, testimonials, and expert quotes into public HTML pages.
Writes a summary to docs/trust-engine/trust_report.txt.
"""
from pathlib import Path
import random

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
REPORT = ROOT / "docs" / "trust-engine" / "trust_report.txt"
TRUST_MARKER = "<!-- SideGuy Trust Block -->"
BADGES = ["BBB Accredited", "Google Reviews", "Expert Verified", "HIPAA Compliant", "Licensed & Insured"]
QUOTES = [
    "'SideGuy Solutions helped us recover missed leads.' — HVAC Owner",
    "'The automation saved hours every week.' — Plumbing Manager",
    "'Our reviews improved overnight.' — Dental Practice Owner",
    "'Dispatch is now seamless.' — Contractor",
    "'We trust SideGuy for compliance.' — Office Admin"
]

updated = 0
skipped = 0
for page in PUBLIC.rglob("*.html"):
    text = page.read_text(errors="ignore")
    if TRUST_MARKER in text:
        skipped += 1
        continue
    badge = random.choice(BADGES)
    quote = random.choice(QUOTES)
    block = f"\n{TRUST_MARKER}\n<div style='background:#eafaf1;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;text-align:center;'>\n  <strong>Trust Signal:</strong> {badge}<br><em>{quote}</em>\n</div>\n"
    if "</body>" in text:
        text = text.replace("</body>", block + "</body>")
        page.write_text(text)
        updated += 1
with REPORT.open("w") as f:
    f.write(f"Trust blocks injected: {updated} pages, {skipped} skipped\n")
print(f"Trust blocks injected: {updated} pages, {skipped} skipped")
