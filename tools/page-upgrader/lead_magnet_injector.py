#!/usr/bin/env python3
"""
Lead Magnet Injector — SideGuy Solutions
========================================
Injects a lead magnet CTA block (download guide, checklist, SMS opt-in)
into public/ pages. Idempotent: skips pages already containing the marker.

Run after meme and FAQ injectors for maximum conversion.
"""
from pathlib import Path
import random

ROOT = Path("/workspaces/sideguy-solutions/public")
MAGNET_MARKER = "<!-- SideGuy Lead Magnet -->"

MAGNETS = [
    ("Download the AI Automation Guide", "Get a free PDF guide to practical AI automations for your business.", "/downloads/ai-automation-guide.pdf"),
    ("Get the Payment Fee Checklist", "Download our checklist to lower your payment processing costs.", "/downloads/payment-fee-checklist.pdf"),
    ("SMS Opt-In: Text PJ for Answers", "Text 773-544-1231 for a real human answer to your automation question.", "sms:+17735441231"),
    ("Download the Office Meme Pack", "Get 20+ office memes for Slack, Teams, and newsletters.", "/downloads/office-meme-pack.zip"),
]

pages = list(ROOT.rglob("*.html"))
updated = 0
skipped = 0

for page in pages:
    text = page.read_text(errors="ignore")
    if MAGNET_MARKER in text:
        skipped += 1
        continue
    title, desc, link = random.choice(MAGNETS)
    if link.startswith("sms:"):
        cta = f'<a href="{link}" class="sideguy-magnet-btn" style="background:#21d3a1;color:#073044;font-weight:700;padding:11px 22px;border-radius:999px;text-decoration:none;">💬 {title}</a>'
    else:
        cta = f'<a href="{link}" class="sideguy-magnet-btn" style="background:#21d3a1;color:#073044;font-weight:700;padding:11px 22px;border-radius:999px;text-decoration:none;">⬇️ {title}</a>'
    block = f"\n{MAGNET_MARKER}\n<div class=\"sideguy-lead-magnet\" style=\"background:#fffbe6;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;text-align:center;\">\n  <strong>{title}</strong><br>{desc}<br>{cta}\n</div>\n"
    if "</body>" in text:
        text = text.replace("</body>", block + "</body>", 1)
        page.write_text(text)
        updated += 1

print(f"Lead magnet injector: {updated} pages updated, {skipped} already marked.")
