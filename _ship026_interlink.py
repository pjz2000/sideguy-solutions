#!/usr/bin/env python3
"""
SIDEGUY INTERLINK ENGINE v3 (DECISION WEB)
Connect problems into a decision web with cross-topic links.

Improvements over v2:
  - 13 topic clusters (was 8) — adds restaurant, CRM, Google Ads, AC, Tesla
  - Searches public/ subdirectories for hub targets (not just root + public/)
  - Richer cross-topic graph with bidirectional links
  - "Also Explore" section separates same-topic from cross-topic links
  - Re-runnable: strips old blocks and re-injects fresh ones
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC_DIR = PROJECT_ROOT / "public"
MARKER = "<!-- sideguy-interlinks -->"
MARKER_END = "<!-- /sideguy-interlinks -->"

# ── Topic clusters ────────────────────────────────────────
# Each key: regex pattern matched against filenames (case-insensitive)
# Each value: list of (label, filename) tuples — real pages that exist
# We'll verify existence at startup and drop any missing targets.

CLUSTERS = {
    "hvac": {
        "pattern": r"^hvac",
        "label": "HVAC",
        "links": [
            ("HVAC Problems Hub", "hvac-problems-hub-san-diego.html"),
            ("HVAC Repair vs Replacement", "hvac-repair-vs-replacement-san-diego.html"),
            ("HVAC Cost Guide", "hvac-cost-guide.html"),
            ("HVAC Maintenance Tips", "hvac-maintenance-san-diego.html"),
            ("HVAC Services — San Diego", "hvac-services-san-diego.html"),
        ],
    },
    "ac": {
        "pattern": r"^ac-",
        "label": "AC / Air Conditioning",
        "links": [
            ("AC Not Cooling — San Diego", "ac-not-cooling-san-diego.html"),
            ("AC Repair — San Diego", "ac-repair-san-diego.html"),
            ("AC Blowing Warm Air", "ac-blowing-warm-air.html"),
            ("AC Not Turning On", "ac-not-turning-on.html"),
        ],
    },
    "solar": {
        "pattern": r"^solar",
        "label": "Solar",
        "links": [
            ("Solar Hub — San Diego", "solar-hub-san-diego.html"),
            ("Solar Install Cost", "solar-install-cost-san-diego.html"),
            ("Solar Directory — San Diego", "solar-directory-san-diego.html"),
        ],
    },
    "tesla": {
        "pattern": r"^tesla",
        "label": "Tesla / EV",
        "links": [
            ("Tesla Overview", "public/authority/tesla.html"),
            ("Tesla vs Gas Cost", "public/money-pages/tesla-vs-gas-cost-california.html"),
        ],
    },
    "payments": {
        "pattern": r"^(payment|stripe|square|pos-|solana-pay|credit-card-process)",
        "label": "Payments",
        "links": [
            ("Stripe Alternatives — San Diego", "stripe-alternatives-for-small-business-san-diego.html"),
            ("Stripe Fees Calculator", "stripe-fees-calculator.html"),
            ("Stripe vs Square", "stripe-vs-square-san-diego.html"),
            ("Payment Processing — California", "payment-processing-california.html"),
            ("Who Do I Call About Payments?", "who-do-i-call-about-payments.html"),
        ],
    },
    "restaurant": {
        "pattern": r"^restaurant",
        "label": "Restaurant",
        "links": [
            ("Restaurant Payment Processing", "restaurant-payment-processing-san-diego.html"),
            ("Restaurant Payments — San Diego", "restaurant-payments-san-diego.html"),
            ("Restaurant Tech Support", "restaurant-tech-support-san-diego.html"),
        ],
    },
    "ai": {
        "pattern": r"^ai-",
        "label": "AI & Automation",
        "links": [
            ("AI Automation Consulting", "ai-automation-consulting-san-diego.html"),
            ("Who Do I Call About AI?", "who-do-i-call-about-ai-tools.html"),
            ("AI Automation — California", "ai-automation-california.html"),
        ],
    },
    "plumbing": {
        "pattern": r"^plumb",
        "label": "Plumbing",
        "links": [
            ("Plumbing Problems Hub", "plumbing-problems-hub-san-diego.html"),
            ("Plumber — San Diego", "plumber-san-diego.html"),
            ("Plumbing Directory — San Diego", "plumbing-directory-san-diego.html"),
        ],
    },
    "roofing": {
        "pattern": r"^roof",
        "label": "Roofing",
        "links": [
            ("Roof Leak — San Diego", "roof-leak-san-diego.html"),
            ("Roof Inspection — San Diego", "roof-inspection-san-diego.html"),
            ("Roof Leak After Rain", "roof-leak-after-rain-san-diego.html"),
        ],
    },
    "electrical": {
        "pattern": r"^electri",
        "label": "Electrical",
        "links": [
            ("Electrical Directory — San Diego", "electrical-directory-san-diego.html"),
            ("Electrical Inspection — San Diego", "electrical-inspection-san-diego.html"),
            ("Electric Bill Too High?", "electric-bill-too-high.html"),
        ],
    },
    "crm": {
        "pattern": r"^crm",
        "label": "CRM",
        "links": [
            ("CRM Setup for Small Business", "crm-setup-for-small-business-san-diego.html"),
            ("CRM Not Working?", "crm-not-working.html"),
            ("CRM Integrations — San Diego", "crm-integrations-san-diego.html"),
        ],
    },
    "google_ads": {
        "pattern": r"^google-ads",
        "label": "Google Ads",
        "links": [
            ("Google Ads Too Expensive?", "google-ads-too-expensive.html"),
        ],
    },
    "lead_gen": {
        "pattern": r"^lead-gen",
        "label": "Lead Generation",
        "links": [
            ("Lead Generation Guide", "lead-generation.html"),
        ],
    },
}

# ── Cross-topic graph ─────────────────────────────────────
# Maps cluster key → list of (label, filename) from OTHER clusters.
# These create the "decision web" — users discover adjacent problems.
CROSS_LINKS = {
    "hvac": [
        ("Energy Savings — Solar", "solar-hub-san-diego.html"),
        ("Electric Bill Too High?", "electric-bill-too-high.html"),
        ("AC Not Cooling?", "ac-not-cooling-san-diego.html"),
    ],
    "ac": [
        ("HVAC Problems Hub", "hvac-problems-hub-san-diego.html"),
        ("HVAC Cost Guide", "hvac-cost-guide.html"),
        ("Electric Bill Too High?", "electric-bill-too-high.html"),
    ],
    "solar": [
        ("HVAC Efficiency", "hvac-cost-guide.html"),
        ("Electric Bill Too High?", "electric-bill-too-high.html"),
        ("Roof Inspection — San Diego", "roof-inspection-san-diego.html"),
    ],
    "tesla": [
        ("Energy Savings — Solar", "solar-hub-san-diego.html"),
        ("Electric Bill Too High?", "electric-bill-too-high.html"),
    ],
    "payments": [
        ("AI Automation Tools", "ai-automation-consulting-san-diego.html"),
        ("Restaurant Payments", "restaurant-payment-processing-san-diego.html"),
    ],
    "restaurant": [
        ("Payment Processing — California", "payment-processing-california.html"),
        ("Stripe vs Square", "stripe-vs-square-san-diego.html"),
        ("AI Automation Tools", "ai-automation-consulting-san-diego.html"),
    ],
    "ai": [
        ("Payment Processing", "payment-processing-california.html"),
        ("Stripe vs Square", "stripe-vs-square-san-diego.html"),
        ("CRM Setup for Small Business", "crm-setup-for-small-business-san-diego.html"),
    ],
    "plumbing": [
        ("HVAC Problems Hub", "hvac-problems-hub-san-diego.html"),
        ("Roof Leak — San Diego", "roof-leak-san-diego.html"),
    ],
    "roofing": [
        ("Solar Install Cost", "solar-install-cost-san-diego.html"),
        ("Plumbing Problems Hub", "plumbing-problems-hub-san-diego.html"),
    ],
    "electrical": [
        ("HVAC Services", "hvac-services-san-diego.html"),
        ("Solar Hub — San Diego", "solar-hub-san-diego.html"),
        ("AC Repair — San Diego", "ac-repair-san-diego.html"),
    ],
    "crm": [
        ("AI Automation Tools", "ai-automation-consulting-san-diego.html"),
        ("Lead Generation Guide", "lead-generation.html"),
        ("Google Ads Too Expensive?", "google-ads-too-expensive.html"),
    ],
    "google_ads": [
        ("Lead Generation Guide", "lead-generation.html"),
        ("AI Automation Tools", "ai-automation-consulting-san-diego.html"),
        ("CRM Setup for Small Business", "crm-setup-for-small-business-san-diego.html"),
    ],
    "lead_gen": [
        ("Google Ads Too Expensive?", "google-ads-too-expensive.html"),
        ("AI Automation Tools", "ai-automation-consulting-san-diego.html"),
        ("CRM Setup for Small Business", "crm-setup-for-small-business-san-diego.html"),
    ],
}


def file_exists(name: str) -> bool:
    """Check if an HTML file exists at root, in public/, or as a relative path."""
    if (PROJECT_ROOT / name).is_file():
        return True
    if (PUBLIC_DIR / name).is_file():
        return True
    # Handle paths like "public/authority/tesla.html"
    if name.startswith("public/") and (PROJECT_ROOT / name).is_file():
        return True
    return False


def strip_existing_block(content: str) -> str:
    """Remove any previous interlink block so we can re-inject fresh."""
    # Try structured markers first
    content = re.sub(
        r"\n?<!-- sideguy-interlinks -->.*?<!-- /sideguy-interlinks -->\s*",
        "\n",
        content,
        flags=re.DOTALL,
    )
    # Fall back to old-style single marker (from v2)
    content = re.sub(
        r"\n?<!-- sideguy-interlinks -->.*?</div>\s*",
        "\n",
        content,
        flags=re.DOTALL,
    )
    return content


def inject_links(filepath: Path, block: str) -> bool:
    """Inject interlink block before </body>. Returns True if modified."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return False

    # Strip old block if present (allows re-runs with updated links)
    had_old = MARKER in content
    if had_old:
        content = strip_existing_block(content)

    # Find </body> (case-insensitive)
    match = re.search(r"</body>", content, re.IGNORECASE)
    if not match:
        return False

    insert_pos = match.start()
    new_content = content[:insert_pos] + "\n" + block + "\n" + content[insert_pos:]

    filepath.write_text(new_content, encoding="utf-8")
    return True


def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("---------------------------------------")
    print("🧠 SIDEGUY INTERLINK ENGINE v3 (DECISION WEB)")
    print("---------------------------------------")
    print(f"Timestamp: {timestamp}")
    print()

    # Validate link targets exist
    missing = []
    for key, cluster in CLUSTERS.items():
        valid_links = []
        for label, filename in cluster["links"]:
            if file_exists(filename):
                valid_links.append((label, filename))
            else:
                missing.append(filename)
        CLUSTERS[key]["links"] = valid_links

    # Also validate cross-link targets
    cross_missing = []
    for key in list(CROSS_LINKS.keys()):
        valid = []
        for label, filename in CROSS_LINKS[key]:
            if file_exists(filename):
                valid.append((label, filename))
            else:
                cross_missing.append(filename)
        CROSS_LINKS[key] = valid

    all_missing = missing + cross_missing
    if all_missing:
        print(f"⚠  {len(all_missing)} link targets not found (skipped):")
        for m in set(all_missing):
            print(f"   - {m}")
        print()

    # Remove clusters with no valid links
    active_clusters = {k: v for k, v in CLUSTERS.items() if v["links"]}
    print(f"Active topic clusters: {len(active_clusters)}")
    for key, cluster in active_clusters.items():
        print(f"  {cluster['label']}: {len(cluster['links'])} links")
    print()

    # Collect all HTML files — public/ (recursive) and root level
    html_files = []
    for f in PUBLIC_DIR.rglob("*.html"):
        html_files.append(f)
    for f in PROJECT_ROOT.glob("*.html"):
        if f.name.startswith("_") or f.name == "sitemap.html":
            continue
        html_files.append(f)

    print(f"Scanning {len(html_files)} HTML files...")
    print()

    updated = 0

    for filepath in html_files:
        basename = filepath.name.lower()

        for key, cluster in active_clusters.items():
            if re.match(cluster["pattern"], basename, re.IGNORECASE):
                # Don't link to yourself
                same_topic = [
                    (label, fn)
                    for label, fn in cluster["links"]
                    if fn != basename
                ]

                # Cross-topic links (also excluding self)
                cross_topic = []
                for label, fn in CROSS_LINKS.get(key, []):
                    if fn != basename and (label, fn) not in same_topic:
                        cross_topic.append((label, fn))

                if not same_topic and not cross_topic:
                    continue

                # Build HTML: same-topic section
                links_html = ""
                for label, filename in same_topic:
                    links_html += f'  <li><a href="/{filename}">{label}</a></li>\n'

                # Add cross-topic section if present
                if cross_topic:
                    links_html += f'  <li style="list-style:none;margin-top:8px;font-size:0.9rem;color:#64748b;font-weight:600;">Also explore:</li>\n'
                    for label, filename in cross_topic:
                        links_html += f'  <li><a href="/{filename}">{label}</a></li>\n'

                block = f"""{MARKER}
<div style="margin:24px 0;padding:16px 20px;border-radius:12px;background:#f1f5f9;border:1px solid #e2e8f0;">
<h3 style="margin:0 0 12px;font-size:1.1rem;color:#073044;">Related Decisions — {cluster["label"]}</h3>
<ul style="margin:0;padding:0 0 0 20px;line-height:1.8;">
{links_html.rstrip()}
</ul>
</div>
{MARKER_END}
"""
                if inject_links(filepath, block):
                    updated += 1
                    if updated <= 20:
                        print(f"  🔗 {filepath.name} → {cluster['label']} ({len(same_topic)}+{len(cross_topic)} links)")
                    elif updated == 21:
                        print("  ... (suppressing further output)")
                break  # Only one cluster per page

    print()
    print("---------------------------------------")
    print("✅ INTERLINKING COMPLETE")
    print("---------------------------------------")
    print(f"Pages updated:  {updated}")
    print()
    print("👉 SideGuy now behaves like a decision network")


if __name__ == "__main__":
    main()
