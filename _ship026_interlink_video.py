#!/usr/bin/env python3
"""
SHIP026 — SideGuy Interlink + Video Engine (30% batch)
Injects:
  1. Related Decisions interlink block (category-aware)
  2. Video embed block (category-aware, placeholder)
  3. "Text PJ" CTA block
Only modifies files that don't already have these blocks.
Inserts before </body> tag.
"""

import os
import re
import sys

DRY_RUN = "--dry-run" in sys.argv
PROJECT_ROOT = "/workspaces/sideguy-solutions"
FILE_LIST = "/tmp/sideguy_30pct.txt"

# ─── Category detection ───────────────────────────────────────

def detect_category(filename):
    fl = filename.lower()
    if "hvac" in fl:
        return "hvac"
    elif "solar" in fl:
        return "solar"
    elif any(k in fl for k in ["stripe", "square", "payment", "pos-system", "solana"]):
        return "payments"
    elif any(k in fl for k in ["ai-automation", "ai-tools", "chatgpt", "business-automation"]):
        return "ai"
    return None

# ─── Interlink targets (real existing files) ──────────────────

INTERLINKS = {
    "hvac": [
        ("HVAC Repair in San Diego — What to Know", "/hvac-repair-san-diego-what-to-know.html"),
        ("HVAC Repair vs Replacement", "/hvac-repair-vs-replacement-san-diego.html"),
        ("HVAC Replacement Cost", "/hvac-replacement-cost-san-diego.html"),
        ("Do I Really Need HVAC Repair?", "/do-i-really-need-hvac-repair-san-diego.html"),
        ("Mini-Split Not Cooling", "/san-diego-mini-split-not-cooling.html"),
    ],
    "solar": [
        ("Solar Panel Installation San Diego", "/solar-panel-installation-san-diego.html"),
        ("Solar Battery Installation", "/solar-battery-installation-san-diego.html"),
        ("Solar Battery Backup Install", "/solar-battery-backup-install.html"),
        ("San Diego Solar Company", "/san-diego-solar-company.html"),
        ("San Diego Solar Installation", "/san-diego-solar-installation-company.html"),
    ],
    "payments": [
        ("Best Payment Processing San Diego", "/Best-Payment-Processing-San-Diego.html"),
        ("Stripe vs Stablecoin Payments", "/stripe-vs-stablecoin-payments.html"),
        ("San Diego Solana Payments", "/San-Diego-Solana-Payments.html"),
        ("Accounting Firm Payment Processing", "/accounting-firm-payment-processing-san-diego.html"),
        ("Payment Processing Near Me", "/san-diego-solana-payments-near-me.html"),
    ],
    "ai": [
        ("Best AI Tools for Small Business", "/best-ai-tools-for-small-business-san-diego.html"),
        ("ChatGPT vs Custom AI for Business", "/chatgpt-vs-custom-ai-for-business.html"),
        ("AI Automation San Diego", "/ai-automation-san-diego.html"),
        ("Is AI Automation Worth Paying For?", "/is-it-worth-paying-for-ai-automation-san-diego.html"),
        ("How to Generate Leads with AI", "/how-to-generate-leads-with-ai-automation-san-diego.html"),
    ],
}

# ─── Video slugs (placeholder — videos don't exist yet) ──────

VIDEO_SLUGS = {
    "hvac": "hvac-repair-vs-replace",
    "solar": "solar-worth-it-san-diego",
    "payments": "stripe-vs-square",
    "ai": "ai-automation-small-business",
}

# ─── Block builders ──────────────────────────────────────────

def build_interlinks_block(category, current_file):
    links = INTERLINKS.get(category, [])
    # Don't link to self
    current_basename = "/" + os.path.basename(current_file)
    links = [(label, href) for label, href in links if href != current_basename]
    if not links:
        return ""
    items = "\n".join(f'  <li><a href="{href}">{label}</a></li>' for label, href in links)
    return f"""
<!-- SHIP026_INTERLINKS -->
<section style="margin:24px auto;max-width:700px;padding:20px 24px;border-radius:12px;background:#f1f5f9;">
<h3 style="margin:0 0 12px;">Related Decisions</h3>
<ul style="margin:0;padding-left:20px;">
{items}
</ul>
</section>
"""

def build_video_block(category):
    slug = VIDEO_SLUGS.get(category)
    if not slug:
        return ""
    return f"""
<!-- SHIP026_VIDEO -->
<section style="margin:24px auto;max-width:700px;padding:16px 24px;border-radius:12px;background:#0f172a;color:#fff;">
<p style="margin:0 0 8px;"><strong>Quick Explanation (30 sec):</strong></p>
<video controls style="width:100%;border-radius:8px;" preload="none" poster="/videos/{slug}-poster.jpg">
  <source src="/videos/{slug}.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
</section>
"""

PJ_BLOCK = """
<!-- SHIP026_CTA -->
<section style="margin:24px auto;max-width:700px;padding:20px 24px;border-radius:12px;background:#0f172a;color:#fff;">
<h3 style="margin:0 0 8px;color:#21d3a1;">Need help deciding?</h3>
<p style="margin:0;">Text PJ at <a href="sms:+17735441231" style="color:#21d3a1;font-weight:bold;">773-544-1231</a>. Clarity before cost.</p>
</section>
"""

# ─── Main processing ─────────────────────────────────────────

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    basename = os.path.basename(filepath)
    category = detect_category(basename)
    if not category:
        return None, "no-category"

    injection = ""

    # Interlinks
    if "Related Decisions" not in content and "SHIP026_INTERLINKS" not in content:
        injection += build_interlinks_block(category, filepath)

    # Video
    if "SHIP026_VIDEO" not in content and "Quick Explanation" not in content:
        injection += build_video_block(category)

    # PJ CTA — only if no existing "Text PJ" AND no SHIP026_CTA
    if "SHIP026_CTA" not in content and "Text PJ" not in content:
        injection += PJ_BLOCK

    if not injection.strip():
        return None, "already-done"

    # Find </body> and inject before it
    body_match = re.search(r"</body>", content, re.IGNORECASE)
    if not body_match:
        return None, "no-body-tag"

    pos = body_match.start()
    new_content = content[:pos] + injection + "\n" + content[pos:]

    if not DRY_RUN:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return category, "updated"

# ─── Run ──────────────────────────────────────────────────────

def main():
    with open(FILE_LIST) as f:
        files = [l.strip() for l in f if l.strip()]

    stats = {"updated": 0, "already-done": 0, "no-body-tag": 0, "no-category": 0, "error": 0}
    cat_counts = {}

    for rel_path in files:
        filepath = os.path.join(PROJECT_ROOT, rel_path.lstrip("./"))
        if not os.path.isfile(filepath):
            stats["error"] += 1
            continue
        try:
            cat, status = process_file(filepath)
            stats[status] += 1
            if status == "updated" and cat:
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
        except Exception as e:
            print(f"  ERROR: {filepath}: {e}")
            stats["error"] += 1

    mode = "DRY-RUN" if DRY_RUN else "LIVE"
    print(f"\n{'='*45}")
    print(f"  SHIP026 INTERLINK + VIDEO — {mode}")
    print(f"{'='*45}")
    print(f"  Files processed:  {len(files)}")
    print(f"  Updated:          {stats['updated']}")
    print(f"  Already done:     {stats['already-done']}")
    print(f"  No </body>:       {stats['no-body-tag']}")
    print(f"  No category:      {stats['no-category']}")
    print(f"  Errors:           {stats['error']}")
    print()
    if cat_counts:
        print("  By category:")
        for k, v in sorted(cat_counts.items()):
            print(f"    {k}: {v}")
    print()

if __name__ == "__main__":
    main()
