#!/usr/bin/env python3
"""
Engagement Injector — SideGuy Solutions
======================================
Injects simple feedback widgets and CTA blocks into public HTML pages.
Tracks engagement in docs/engagement-engine/engagement_report.txt.
"""
from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
REPORT = ROOT / "docs" / "engagement-engine" / "engagement_report.txt"
WIDGET_MARKER = "<!-- SideGuy Engagement Widget -->"

updated = 0
skipped = 0
for page in PUBLIC.rglob("*.html"):
    text = page.read_text(errors="ignore")
    if WIDGET_MARKER in text:
        skipped += 1
        continue
    block = f"\n{WIDGET_MARKER}\n<div style='background:#fffbe6;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;text-align:center;'>\n  <strong>Was this guide helpful?</strong>\n  <button style='background:#21d3a1;color:#fff;border:none;padding:8px 16px;border-radius:6px;margin:8px;'>Yes</button>\n  <button style='background:#073044;color:#fff;border:none;padding:8px 16px;border-radius:6px;margin:8px;'>No</button>\n  <a href='mailto:help@sideguysolutions.com?subject=Feedback' style='color:#21d3a1;text-decoration:underline;margin-left:12px;'>Send feedback</a>\n</div>\n"
    if "</body>" in text:
        text = text.replace("</body>", block + "</body>")
        page.write_text(text)
        updated += 1
with REPORT.open("w") as f:
    f.write(f"Engagement widgets injected: {updated} pages, {skipped} skipped\n")
print(f"Engagement widgets injected: {updated} pages, {skipped} skipped")
