#!/usr/bin/env python3
"""
SideGuy Decision Report — Read-Only Page Audit

Scores all root-level HTML pages and produces a ranked report:
  - Which pages are highest-intent (repair, cost, replace decisions)
  - Which already have the clarity layer
  - Which have <main> tags (eligible for clarity-layer upgrade)
  - Which are thin/duplicate and should be reviewed

Does NOT modify any files. Output only.
"""

import os
import re
from pathlib import Path
from collections import Counter

ROOT = Path("/workspaces/sideguy-solutions")
REPORT_PATH = ROOT / "docs" / "decision-report.md"


def score_page(filepath):
    """Score a page by filename + lightweight content signals."""
    name = filepath.name.lower()
    score = 0
    tags = []

    # --- Filename signals (fast, no I/O) ---

    # High-intent decision keywords
    decision_words = ["repair-or-replace", "should-i", "who-do-i-call",
                      "worth-it", "vs-", "cost-guide", "cost-of",
                      "how-much", "when-to", "fix-or"]
    for w in decision_words:
        if w in name:
            score += 5
            tags.append("decision")
            break

    # Service/problem keywords
    service_words = ["hvac", "plumbing", "electrical", "solar", "ac-",
                     "furnace", "water-heater", "roof", "insulation",
                     "duct", "thermostat", "mini-split"]
    for w in service_words:
        if w in name:
            score += 3
            tags.append("service")
            break

    # Payment/money keywords
    money_words = ["stripe", "payment", "processing", "fees",
                   "calculator", "pricing"]
    for w in money_words:
        if w in name:
            score += 3
            tags.append("payments")
            break

    # Local signals
    if "san-diego" in name:
        score += 2
        tags.append("local-sd")
    for city in ["encinitas", "carlsbad", "oceanside", "escondido",
                 "el-cajon", "chula-vista", "la-jolla"]:
        if city in name:
            score += 2
            tags.append("local-suburb")
            break

    # Penalize mass-generated city variants
    multi_city = ["austin", "chicago", "dallas", "denver", "miami",
                  "phoenix", "portland", "seattle", "los-angeles"]
    for city in multi_city:
        if city in name:
            score -= 3
            tags.append("multi-city")
            break

    # Penalize very long filenames (usually mass-gen)
    if len(name) > 120:
        score -= 2
        tags.append("long-slug")

    return score, tags


def analyze_content(filepath):
    """Light content analysis — only done for high-scoring pages."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {}

    info = {
        "lines": text.count("\n"),
        "has_main": bool(re.search(r"<main[\s>]", text)),
        "has_clarity": "SIDEGUY CLARITY LAYER" in text,
        "has_right_rail": "rightRail" in text,
        "has_floating_pj": "floatBtn" in text or "floating" in text,
        "sms_links": len(re.findall(r"sms:", text)),
        "has_schema": '"@context"' in text,
        "has_canonical": 'rel="canonical"' in text,
    }

    # Extract title
    m = re.search(r"<title>(.*?)</title>", text, re.DOTALL)
    info["title"] = m.group(1).strip()[:80] if m else "(no title)"

    return info


def main():
    print("Scanning root-level HTML pages...")

    pages = sorted(ROOT.glob("*.html"))
    print(f"Found {len(pages)} pages")

    # Score all pages (fast — filename only)
    scored = []
    for p in pages:
        s, tags = score_page(p)
        scored.append((s, p, tags))

    scored.sort(key=lambda x: -x[0])

    # Always analyze the 15 clarity-layer pages + top 100 by score
    CLARITY_PAGES = [
        "Best-Payment-Processing-San-Diego.html",
        "ac-not-cooling-san-diego.html",
        "best-payment-processor-for-contractors-san-diego.html",
        "best-payment-processor-for-ecommerce-san-diego.html",
        "best-payment-processor-for-medical-offices-san-diego.html",
        "best-payment-processor-for-restaurants-san-diego.html",
        "electric-bill-too-high.html",
        "hvac-repair-san-diego-what-to-know.html",
        "hvac-repair-san-diego.html",
        "plumbing-emergency-or-can-it-wait-san-diego.html",
        "stripe-alternatives-for-small-business-san-diego.html",
        "stripe-alternatives-san-diego.html",
        "stripe-fees-calculator.html",
        "stripe-fees-for-small-business-san-diego.html",
        "who-do-i-call.html",
    ]
    analyze_set = set(p.name for _, p, _ in scored[:100])
    analyze_set.update(CLARITY_PAGES)

    print(f"Analyzing {len(analyze_set)} candidates...")
    detailed = {}
    for s, p, tags in scored:
        if p.name in analyze_set:
            detailed[p.name] = analyze_content(p)

    # Build report
    os.makedirs(REPORT_PATH.parent, exist_ok=True)

    with open(REPORT_PATH, "w") as f:
        f.write("# SideGuy Decision Report\n\n")
        f.write(f"**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Total pages scanned:** {len(pages)}\n\n")

        # --- Summary stats ---
        clarity_count = sum(1 for d in detailed.values() if d.get("has_clarity"))
        main_count = sum(1 for d in detailed.values() if d.get("has_main"))
        f.write(f"**Top 100 with clarity layer:** {clarity_count}\n")
        f.write(f"**Top 100 with `<main>` tags (upgrade-eligible):** {main_count}\n\n")

        # --- Tier 1: Ready for clarity layer upgrade ---
        f.write("---\n\n")
        f.write("## Tier 1: Upgrade Candidates (high intent + has `<main>` + no clarity layer yet)\n\n")
        f.write("These pages are the next batch to receive the clarity-layer treatment.\n\n")
        f.write("| Score | File | Title | Tags |\n")
        f.write("|-------|------|-------|------|\n")

        tier1_count = 0
        for s, p, tags in scored[:100]:
            d = detailed.get(p.name, {})
            if d.get("has_main") and not d.get("has_clarity") and s >= 3:
                title = d.get("title", "")
                f.write(f"| {s} | {p.name} | {title} | {', '.join(tags)} |\n")
                tier1_count += 1

        if tier1_count == 0:
            f.write("| — | No candidates found | — | — |\n")

        # --- Tier 2: Already upgraded ---
        f.write(f"\n## Tier 2: Already Upgraded (clarity layer deployed)\n\n")
        f.write("| File | Title |\n")
        f.write("|------|-------|\n")

        for s, p, tags in scored:
            d = detailed.get(p.name, {})
            if d.get("has_clarity"):
                title = d.get("title", "")
                f.write(f"| {p.name} | {title} |\n")

        # --- Tier 3: High intent but no <main> tag ---
        f.write(f"\n## Tier 3: High Intent, No `<main>` Tag (needs manual review)\n\n")
        f.write("These score well but don't have `<main>` tags, so the automated clarity-layer script can't process them.\n\n")
        f.write("| Score | File | Title | Lines |\n")
        f.write("|-------|------|-------|-------|\n")

        for s, p, tags in scored[:100]:
            d = detailed.get(p.name, {})
            if not d.get("has_main") and not d.get("has_clarity") and s >= 3:
                title = d.get("title", "")
                lines = d.get("lines", 0)
                f.write(f"| {s} | {p.name} | {title} | {lines} |\n")

        # --- Tag distribution ---
        f.write(f"\n## Tag Distribution (top 100 pages)\n\n")
        all_tags = []
        for s, p, tags in scored[:100]:
            all_tags.extend(tags)
        tag_counts = Counter(all_tags)
        f.write("| Tag | Count |\n")
        f.write("|-----|-------|\n")
        for tag, count in tag_counts.most_common():
            f.write(f"| {tag} | {count} |\n")

        # --- Score distribution ---
        f.write(f"\n## Score Distribution (all {len(pages)} pages)\n\n")
        buckets = {"8+ (strong)": 0, "5-7 (emerging)": 0, "1-4 (weak)": 0, "0 or below (noise)": 0}
        for s, p, tags in scored:
            if s >= 8:
                buckets["8+ (strong)"] += 1
            elif s >= 5:
                buckets["5-7 (emerging)"] += 1
            elif s >= 1:
                buckets["1-4 (weak)"] += 1
            else:
                buckets["0 or below (noise)"] += 1

        f.write("| Bucket | Count |\n")
        f.write("|--------|-------|\n")
        for bucket, count in buckets.items():
            f.write(f"| {bucket} | {count} |\n")

        f.write(f"\n---\n\n*Read-only report. No files were modified.*\n")

    print(f"\nReport written to: {REPORT_PATH}")
    print(f"  Tier 1 (upgrade candidates): {tier1_count}")
    print(f"  Already upgraded: {clarity_count}")


if __name__ == "__main__":
    main()
