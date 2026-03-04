#!/usr/bin/env python3
"""
SIDEGUY Manifest Builder + Topic Gap Intelligence
- Generates future page ideas (industry × problem matrix)
- Scans existing generated/longtail/clusters slugs
- Compares against curated "top-site" topic library
- Outputs: manifests/sideguy_generated_manifest.tsv
           intelligence/topic-gaps-report.md
- Updates: knowledge/sideguy-knowledge-map.html
"""

import os
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
MANIFEST_PATH = ROOT / "manifests" / "sideguy_generated_manifest.tsv"
REPORT_PATH   = ROOT / "intelligence" / "topic-gaps-report.md"
KM_PATH       = ROOT / "knowledge" / "sideguy-knowledge-map.html"

MANIFEST_PATH.parent.mkdir(exist_ok=True)
REPORT_PATH.parent.mkdir(exist_ok=True)

# ──────────────────────────────────────────────
# 1.  INDUSTRY × PROBLEM MATRIX  (Future page ideas)
# ──────────────────────────────────────────────

INDUSTRIES = [
    "plumbers",
    "electricians",
    "roofers",
    "hvac-contractors",
    "landscapers",
    "restaurants",
    "dentists",
    "law-firms",
    "real-estate-agents",
    "contractors",
    "construction-companies",
    "marketing-agencies",
    "consultants",
    "retail-stores",
    "fitness-gyms",
    "medical-offices",
    "insurance-agents",
    "accountants",
    "barbershops",
    "salons",
]

PROBLEMS = [
    ("ai-automation",               "ai-automation",       "ai-workflow-automation"),
    ("customer-service-automation", "ai-automation",       "ai-customer-service"),
    ("scheduling-automation",       "ai-automation",       "ai-scheduling"),
    ("workflow-automation",         "ai-automation",       "ai-workflow-automation"),
    ("reduce-payment-processing-fees", "payments",         "payment-fees"),
    ("ai-customer-intake",          "ai-automation",       "ai-workflow-automation"),
    ("missed-call-systems",         "small-business-tech", "customer-ops"),
    ("crm-automation",              "small-business-tech", "software-selection"),
    ("email-automation",            "ai-automation",       "ai-email-automation"),
    ("ai-marketing-automation",     "ai-automation",       "ai-marketing-automation"),
]

PAYMENT_INDUSTRIES = [
    "restaurants", "retail", "contractors", "plumbers",
    "electricians", "salons", "dentists", "law-firms", "consultants", "gyms",
]

# ──────────────────────────────────────────────
# 2.  CURATED "TOP-SITE" TOPIC LIBRARY
#     (what authoritative sites rank for – topics not yet covered)
# ──────────────────────────────────────────────

TOPIC_LIBRARY = [
    # slug, title, description, pillar, cluster

    # AI Automation
    ("ai-automation-roi",
     "AI automation ROI calculator guide",
     "How to estimate time saved, payback period, and operational lift.",
     "ai-automation", "ai-workflow-automation"),

    ("ai-automation-examples",
     "AI automation examples for small business",
     "Real operator examples that reduce friction without complexity.",
     "ai-automation", "ai-workflow-automation"),

    ("ai-automation-workflows",
     "AI automation workflows that work",
     "Workflow patterns: intake → routing → summary → action.",
     "ai-automation", "ai-workflow-automation"),

    ("ai-customer-service-best-practices",
     "AI customer service best practices",
     "What to automate, what to keep human, and how to avoid brand damage.",
     "ai-automation", "ai-customer-service"),

    ("ai-customer-intake-automation",
     "AI customer intake automation",
     "Forms, triage, summarization, and routing that prevent missed leads.",
     "ai-automation", "ai-workflow-automation"),

    ("ai-scheduling-reminders",
     "AI scheduling reminders that reduce no-shows",
     "Reminder flows that reduce no-shows and keep calendars clean.",
     "ai-automation", "ai-scheduling"),

    ("ai-scheduling-intake-questions",
     "Scheduling intake questions templates",
     "Questions that make booking smoother and reduce reschedules.",
     "ai-automation", "ai-scheduling"),

    ("ai-email-followup-automation",
     "AI email follow-up automation",
     "Follow-up sequences that keep your voice but save time.",
     "ai-automation", "ai-marketing-automation"),

    ("ai-text-replies-for-business",
     "AI text replies for business",
     "Template patterns for fast, human-feeling text responses.",
     "ai-automation", "ai-customer-service"),

    ("ai-call-summaries",
     "AI call summaries for operators",
     "How operators use summaries and action items without losing context.",
     "ai-automation", "ai-workflow-automation"),

    ("ai-sop-writer",
     "AI SOP writer for process documentation",
     "How to turn messy ops into clean SOPs with AI and humans.",
     "ai-automation", "ai-workflow-automation"),

    ("ai-meeting-notes",
     "AI meeting notes for operators",
     "Simple systems to capture decisions and reduce forget-work.",
     "ai-automation", "ai-workflow-automation"),

    ("ai-marketing-content-calendar",
     "AI marketing content calendar",
     "A calm content system that doesn't become a second job.",
     "ai-automation", "ai-marketing-automation"),

    ("ai-review-reply-system",
     "AI review reply system",
     "Respond to reviews quickly while keeping trust and tone.",
     "ai-automation", "ai-customer-service"),

    ("ai-tools-for-contractors",
     "AI tools for contractors",
     "Tool categories that matter: intake, scheduling, quoting, follow-up.",
     "ai-automation", "ai-workflow-automation"),

    ("ai-tools-for-restaurants",
     "AI tools for restaurants",
     "Bookings, reviews, staff comms, and customer messaging.",
     "ai-automation", "ai-workflow-automation"),

    ("ai-tools-for-medical-offices",
     "AI tools for medical offices",
     "Intake, routing, reminders, and documentation basics.",
     "ai-automation", "ai-workflow-automation"),

    # Payments
    ("payment-processing-fees-explained",
     "Payment processing fees explained",
     "Plain-English breakdown of fee buckets and what operators control.",
     "payments", "payment-fees"),

    ("interchange-fees-explained",
     "Interchange fees explained",
     "How interchange works and why statements look confusing.",
     "payments", "payment-fees"),

    ("processor-markup-explained",
     "Processor markup explained",
     "What processors add and how to negotiate.",
     "payments", "payment-fees"),

    ("how-to-read-processing-statement",
     "How to read a processing statement",
     "A simple guide to identify where costs hide.",
     "payments", "payment-fees"),

    ("reduce-chargebacks",
     "How to reduce chargebacks",
     "Prevention systems and response templates.",
     "payments", "chargebacks"),

    ("chargeback-response-template",
     "Chargeback response template",
     "A practical template and evidence checklist.",
     "payments", "chargebacks"),

    ("instant-settlement-explained",
     "Instant settlement explained",
     "Why speed matters and where it helps operators most.",
     "payments", "instant-settlement"),

    ("payout-delays-why",
     "Why payouts are delayed",
     "What causes holds and how to reduce them.",
     "payments", "instant-settlement"),

    ("payment-fraud-basics",
     "Payment fraud basics",
     "Calm controls: verification, limits, monitoring, and policies.",
     "payments", "payment-security"),

    ("pci-compliance-simple",
     "PCI compliance (simple guide)",
     "What it is, what matters, and how to stay sane.",
     "payments", "payment-security"),

    ("best-payment-processor-small-business",
     "Best payment processor for small business (how to choose)",
     "A decision framework instead of hype.",
     "payments", "payment-fees"),

    ("high-risk-payments-explained",
     "High-risk payments explained",
     "What triggers high risk and how to navigate.",
     "payments", "payment-security"),

    ("stripe-vs-square-fees",
     "Stripe vs Square fees comparison",
     "How to compare fees and hidden costs.",
     "payments", "payment-fees"),

    ("payment-processing-contract-traps",
     "Payment processing contract traps",
     "Terms that cost operators money: leases, fees, early termination.",
     "payments", "payment-fees"),

    # Small Business Tech
    ("how-to-choose-crm",
     "How to choose a CRM",
     "Questions to avoid buying the wrong system.",
     "small-business-tech", "software-selection"),

    ("crm-setup-checklist",
     "CRM setup checklist",
     "A simple checklist for first-week CRM success.",
     "small-business-tech", "software-selection"),

    ("software-integration-basics",
     "Software integration basics",
     "Reduce tool sprawl and keep ops clean.",
     "small-business-tech", "software-selection"),

    ("how-to-build-sops-fast",
     "How to build SOPs fast",
     "A quick method: draft, test, refine.",
     "small-business-tech", "sops-and-process"),

    ("customer-intake-forms",
     "Customer intake form templates",
     "Intake templates that reduce back-and-forth.",
     "small-business-tech", "customer-ops"),

    ("missed-call-capture-system",
     "Missed call capture system",
     "SMS, voicemail, routing, and follow-up loops.",
     "small-business-tech", "customer-ops"),

    ("simple-ops-dashboard",
     "Simple ops dashboard for small business",
     "Track the 5 numbers that matter weekly.",
     "small-business-tech", "time-saving-systems"),

    ("automated-invoicing-workflow",
     "Automated invoicing workflow",
     "Invoice automation without losing accuracy.",
     "small-business-tech", "time-saving-systems"),
]


# ──────────────────────────────────────────────
# 3.  COLLECT EXISTING SLUGS
# ──────────────────────────────────────────────

def collect_existing_slugs():
    existing = set()
    for folder in ("generated", "longtail", "clusters"):
        d = ROOT / folder
        if d.exists():
            for f in d.glob("*.html"):
                existing.add(f.stem)
    return existing


# ──────────────────────────────────────────────
# 4.  BUILD MANIFEST ROWS
# ──────────────────────────────────────────────

def build_manifest_rows():
    rows = set()

    # Industry × Problem matrix
    for industry in INDUSTRIES:
        for problem_slug, pillar, cluster in PROBLEMS:
            slug  = f"{problem_slug}-for-{industry}"
            title = f"{problem_slug.replace('-', ' ')} for {industry.replace('-', ' ')}"
            desc  = (f"How {industry.replace('-', ' ')} operators solve "
                     f"{problem_slug.replace('-', ' ')} using modern tools and clear systems.")
            rows.add((slug, title, desc, pillar, cluster))

    # Payment industry overrides
    for industry in PAYMENT_INDUSTRIES:
        slug  = f"reduce-payment-processing-fees-{industry}"
        title = f"reduce payment processing fees {industry}"
        desc  = (f"How {industry} businesses reduce payment processing costs "
                 "without hurting conversions.")
        rows.add((slug, title, desc, "payments", "payment-fees"))

    return rows


# ──────────────────────────────────────────────
# 5.  GAP ANALYSIS  (library vs existing)
# ──────────────────────────────────────────────

def find_gaps(existing_slugs):
    missing = []
    for row in TOPIC_LIBRARY:
        slug = row[0]
        if slug not in existing_slugs:
            missing.append(row)
    return missing


# ──────────────────────────────────────────────
# 6.  WRITE MANIFEST  (idempotent – merge & dedup)
# ──────────────────────────────────────────────

def write_manifest(matrix_rows, gap_rows):
    existing_lines = set()
    if MANIFEST_PATH.exists():
        existing_lines = set(MANIFEST_PATH.read_text().splitlines())

    new_lines = set()
    for row in matrix_rows:
        new_lines.add("\t".join(row))
    for row in gap_rows:
        new_lines.add("\t".join(row))

    all_lines = sorted(existing_lines | new_lines)
    MANIFEST_PATH.write_text("\n".join(all_lines) + "\n")
    return len(all_lines)


# ──────────────────────────────────────────────
# 7.  WRITE GAP REPORT
# ──────────────────────────────────────────────

def write_gap_report(existing_slugs, gap_rows, total_manifest):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "# SideGuy Topic Gaps Report",
        f"\nGenerated: {stamp}",
        "\nThis report compares your current site inventory (generated + longtail + clusters) "
        "against a curated top-traffic topic library.",
        "\n## Summary",
        f"- Existing slugs detected: {len(existing_slugs)}",
        f"- Topic library size: {len(TOPIC_LIBRARY)}",
        f"- Missing topics found: {len(gap_rows)}",
        f"- Total manifest rows: {total_manifest}",
        "\n## What to do next",
        "1. Run `scripts/build-generated.py` (add entries from this report to the PAGES list).",
        "2. Commit and deploy.",
        "3. Request indexing in Search Console for key hubs:",
        "   - /pillars/ai-automation.html",
        "   - /pillars/payments.html",
        "   - /pillars/small-business-tech.html",
        "   - /knowledge/sideguy-knowledge-map.html",
        "\n## Missing topics (ready to build)",
    ]

    if gap_rows:
        for slug, title, desc, pillar, cluster in gap_rows:
            lines.append(f"- **{title}** `{slug}` → {pillar}/{cluster}")
            lines.append(f"  > {desc}")
    else:
        lines.append("- None! You're fully covered against this library.")

    lines.append("\n## Priority recommendations")
    lines.append("Top gaps by expected search volume (based on topic library structure):")

    # Priority: payment explainers and ai tools pages tend to rank fast
    priority_keywords = ["fees-explained", "interchange", "payment-fraud", "pci-compliance",
                         "ai-tools-for", "ai-call-summaries", "ai-review-reply"]
    priority_found = [r for r in gap_rows
                      if any(kw in r[0] for kw in priority_keywords)]
    if priority_found:
        for row in priority_found[:8]:
            lines.append(f"  1. `{row[0]}` — {row[1]}")
    else:
        lines.append("  All priority topics are already covered.")

    REPORT_PATH.write_text("\n".join(lines) + "\n")
    print(f"  Gap report → {REPORT_PATH.relative_to(ROOT)}")


# ──────────────────────────────────────────────
# 8.  UPDATE KNOWLEDGE MAP
# ──────────────────────────────────────────────

def update_knowledge_map():
    if not KM_PATH.exists():
        print("  Knowledge map not found — skipping link injection.")
        return

    content = KM_PATH.read_text()
    if "topic-gaps-report" in content:
        print("  Knowledge map already links Topic Gaps Report — skipping.")
        return

    # Find the microFooter / closing body area to inject before it
    inject_block = """
<!-- SIDEGUY_TOPIC_GAP_LINK -->
<section style="padding:18px 24px;margin:24px 0;border:1px solid rgba(0,0,0,0.09);border-radius:14px;background:#f5fefd;">
  <h2 style="margin:0 0 10px 0;font-size:1rem;color:#073044;">📊 Site Intelligence</h2>
  <ul style="margin:0;padding:0 0 0 18px;color:#3f6173;">
    <li><a href="/intelligence/topic-gaps-report.md" style="color:#1f7cff;">Topic Gaps Report</a> — Missing pages vs top-traffic topic library</li>
    <li><a href="/manifests/sideguy_generated_manifest.tsv" style="color:#1f7cff;">Generated Manifest</a> — Future page ideas (industry × problem matrix)</li>
  </ul>
</section>
<!-- END SIDEGUY_TOPIC_GAP_LINK -->
"""

    # Insert before closing body or microFooter
    if '<div class="microFooter"' in content:
        new_content = content.replace(
            '<div class="microFooter"',
            inject_block + '<div class="microFooter"',
            1
        )
    elif "</body>" in content:
        new_content = content.replace("</body>", inject_block + "</body>", 1)
    else:
        print("  Could not find injection point in knowledge map — skipping.")
        return

    KM_PATH.write_text(new_content)
    print("  Knowledge map updated with Topic Gaps Report link.")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=== SIDEGUY Manifest Builder + Topic Gap Intelligence ===\n")

    # Step 1 — collect existing slugs
    existing = collect_existing_slugs()
    print(f"Existing slugs found: {len(existing)}")
    print(f"  Generated: {len(list((ROOT / 'generated').glob('*.html')) if (ROOT / 'generated').exists() else [])}")
    print(f"  Longtail:  {len(list((ROOT / 'longtail').glob('*.html')) if (ROOT / 'longtail').exists() else [])}")
    print(f"  Clusters:  {len(list((ROOT / 'clusters').glob('*.html')) if (ROOT / 'clusters').exists() else [])}")

    # Step 2 — build industry × problem matrix rows
    matrix_rows = build_manifest_rows()
    print(f"\nMatrix rows generated: {len(matrix_rows)}")

    # Step 3 — find topic library gaps
    gap_rows = find_gaps(existing)
    print(f"Topic library gaps:    {len(gap_rows)}")

    # Step 4 — write manifest
    total = write_manifest(matrix_rows, gap_rows)
    print(f"Manifest total rows:   {total}")
    print(f"  Saved → {MANIFEST_PATH.relative_to(ROOT)}")

    # Step 5 — write gap report
    write_gap_report(existing, gap_rows, total)

    # Step 6 — update knowledge map
    update_knowledge_map()

    print("\n=== Done ===")
    print(f"Manifest:   manifests/sideguy_generated_manifest.tsv  ({total} rows)")
    print(f"Gap report: intelligence/topic-gaps-report.md  ({len(gap_rows)} missing topics)")
    print("\nNext: pick high-priority rows from the gap report, add to")
    print("      scripts/build-generated.py PAGES list, and re-run.")
