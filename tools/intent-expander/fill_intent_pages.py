#!/usr/bin/env python3
"""
SideGuy Intent Page Filler
----------------------------
Replaces the string __PLACEHOLDER__ inside auto-intent-pages/**/*.html with
a standard "explained / cost / mistakes / checklist / next-steps" content block.

Safe to re-run: only modifies files still containing __PLACEHOLDER__.

Usage:
  python3 tools/intent-expander/fill_intent_pages.py
"""

import glob
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.resolve()

PLACEHOLDER = "__PLACEHOLDER__"

TEMPLATE_BLOCK = """\
<section style="margin-top:28px">
  <h2 style="font-size:1.3rem;font-weight:800;margin-bottom:10px">Overview</h2>
  <p>This guide explains the topic in plain language — what it means, why it matters,
  and what to do next.</p>
</section>

<section style="margin-top:28px">
  <h2 style="font-size:1.3rem;font-weight:800;margin-bottom:10px">Typical Cost</h2>
  <p>Costs vary based on scope, provider, and location. This page outlines typical ranges
  and the factors that drive prices up or down — so you're not guessing.</p>
</section>

<section style="margin-top:28px">
  <h2 style="font-size:1.3rem;font-weight:800;margin-bottom:10px">Common Mistakes</h2>
  <p>Most issues come from moving too fast without a clear picture. Key mistakes:</p>
  <ul style="margin:10px 0 0 20px;line-height:1.7">
    <li>Skipping the comparison step</li>
    <li>Choosing based on price alone</li>
    <li>Not asking the right questions upfront</li>
    <li>Underestimating implementation time</li>
  </ul>
</section>

<section style="margin-top:28px">
  <h2 style="font-size:1.3rem;font-weight:800;margin-bottom:10px">Quick Checklist</h2>
  <ul style="margin:10px 0 0 20px;line-height:1.7">
    <li>Clarify your actual goal (what outcome do you need?)</li>
    <li>List your current tools and constraints</li>
    <li>Compare at least two options before deciding</li>
    <li>Estimate total cost including setup and ongoing fees</li>
    <li>Plan your first small test before full rollout</li>
  </ul>
</section>

<section style="margin-top:28px">
  <h2 style="font-size:1.3rem;font-weight:800;margin-bottom:10px">Next Steps</h2>
  <p>If you want a human to look at your specific situation — no forms, no sales pitch —
  text PJ directly: <strong><a href="sms:+17735441231">773-544-1231</a></strong>.</p>
</section>
"""

# Search auto-intent-pages only (not the full repo — avoid pollution)
pattern = str(ROOT / "auto-intent-pages" / "**" / "*.html")
candidates = glob.glob(pattern, recursive=True)

filled = 0
already_done = 0

for path in sorted(candidates):
    try:
        html = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue

    if PLACEHOLDER not in html:
        already_done += 1
        continue

    new_html = html.replace(PLACEHOLDER, TEMPLATE_BLOCK)
    Path(path).write_text(new_html, encoding="utf-8")
    filled += 1

print(f"Intent pages filled   : {filled}")
print(f"Already complete      : {already_done}")
print(f"Total scanned         : {len(candidates)}")
