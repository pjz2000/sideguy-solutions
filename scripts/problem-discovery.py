#!/usr/bin/env python3
# ==============================================================
# SIDEGUY PROBLEM DISCOVERY ENGINE
# Generates future problem page ideas automatically
# ==============================================================
# Cross-joins topics × question patterns to produce a CSV of
# problem page candidates, along with slug, priority score, and
# whether a page for that slug already exists in the repo.
#
# Output:
#   data/problem-ideas.csv        — full matrix
#   data/problem-ideas-new.csv    — only slugs that don't exist yet
#
# Usage:  python3 scripts/problem-discovery.py
# ==============================================================

import csv, os, re, datetime
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

TODAY = datetime.date.today().isoformat()

# ── Topics ────────────────────────────────────────────────────
# Grouped by domain for priority scoring

TOPICS = {
    # AI & automation (priority 9)
    "ai-automation":            9,
    "ai-agents":                9,
    "ai-customer-service":      9,
    "ai-scheduling":            8,
    "ai-lead-generation":       8,
    "ai-workflow":              8,
    "ai-email-automation":      7,
    "ai-marketing-automation":  7,
    "chatgpt-api":              8,
    "openai-api":               8,
    "claude-api":               7,
    "langchain":                7,
    "n8n-automation":           7,
    "zapier-automation":        8,
    "make-com-scenarios":       7,
    "airtable-automation":      6,
    # Payments (priority 9)
    "stripe-payments":          9,
    "stripe-connect":           8,
    "stripe-radar":             8,
    "stripe-webhooks":          9,
    "payment-processing":       9,
    "payment-gateway":          8,
    "chargebacks":              9,
    "ach-payments":             7,
    "subscription-billing":     8,
    "invoicing":                7,
    "payment-fraud":            8,
    "crypto-payments":          7,
    "solana-payments":          6,
    "square-payments":          7,
    "paypal-business":          7,
    # Tech / infrastructure (priority 7)
    "dns-configuration":        7,
    "cloudflare-setup":         7,
    "ssl-certificate":          7,
    "website-deployment":       7,
    "hosting-configuration":    6,
    "api-integration":          8,
    "webhook-configuration":    8,
    "oauth-setup":              7,
    "google-analytics":         7,
    "google-ads-tracking":      7,
    "google-search-console":    6,
    # CRM / ops (priority 7)
    "crm-automation":           7,
    "hubspot-crm":              7,
    "salesforce-crm":           6,
    "email-deliverability":     8,
    "email-marketing":          7,
    "twilio-sms":               7,
    "calendar-booking":         7,
    "scheduling-software":      6,
    # Small business (priority 6)
    "quickbooks-accounting":    6,
    "xero-accounting":          6,
    "shopify-store":            6,
    "woocommerce":              6,
    "google-my-business":       7,
    "local-seo":                7,
}

# ── Question patterns ─────────────────────────────────────────
# {topic} is replaced, slug is derived from the result

PATTERNS = [
    ("{topic} not working",              9),
    ("{topic} error fix",                8),
    ("{topic} troubleshooting guide",    7),
    ("how to fix {topic}",               8),
    ("why is {topic} failing",           8),
    ("{topic} setup guide",              7),
    ("{topic} configuration issue",      7),
    ("best way to set up {topic}",       6),
    ("{topic} problems and solutions",   6),
    ("{topic} keeps disconnecting",      7),
    ("{topic} timeout error",            8),
    ("{topic} permission denied",        7),
    ("{topic} rate limit exceeded",      8),
    ("{topic} integration not working",  8),
    ("{topic} webhook failing",          8),
    ("{topic} authentication error",     7),
    ("{topic} billing issue",            8),
    ("{topic} payment declined",         9),
    ("{topic} refund not processed",     7),
    ("{topic} payout delayed",           8),
    ("{topic} account suspended",        7),
    ("{topic} data not syncing",         7),
    ("{topic} slow performance fix",     6),
    ("{topic} duplicate records fix",    6),
    ("{topic} api key invalid",          8),
]

# ── Slug helper ───────────────────────────────────────────────

def to_slug(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s

# ── Collect existing problem slugs ───────────────────────────

existing_slugs: set[str] = set()
for p in (ROOT / "problems").glob("*.html"):
    existing_slugs.add(p.stem)
# Also root-level problem pages
for p in ROOT.glob("*.html"):
    existing_slugs.add(p.stem)

# ── Generate matrix ───────────────────────────────────────────

rows: list[dict] = []

for topic_key, topic_priority in TOPICS.items():
    # Human-readable label (hyphens → spaces)
    topic_label = topic_key.replace("-", " ")

    for pattern, pattern_priority in PATTERNS:
        title   = pattern.format(topic=topic_label)
        slug    = to_slug(title)
        score   = round((topic_priority + pattern_priority) / 2, 1)
        exists  = "yes" if slug in existing_slugs else "no"
        url     = f"https://sideguysolutions.com/problems/{slug}.html"

        rows.append({
            "topic":           topic_key,
            "problem_title":   title,
            "slug":            slug,
            "priority_score":  score,
            "already_exists":  exists,
            "suggested_url":   url,
            "generated_date":  TODAY,
        })

# Sort: new pages first, then by score desc, then alpha
rows.sort(key=lambda r: (r["already_exists"], -r["priority_score"], r["slug"]))

# ── Write full CSV ────────────────────────────────────────────

FIELDS = ["topic", "problem_title", "slug", "priority_score",
          "already_exists", "suggested_url", "generated_date"]

full_path = DATA_DIR / "problem-ideas.csv"
with full_path.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)

# ── Write net-new CSV ─────────────────────────────────────────

new_rows = [r for r in rows if r["already_exists"] == "no"]
new_path = DATA_DIR / "problem-ideas-new.csv"
with new_path.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(new_rows)

# ── Summary ───────────────────────────────────────────────────

print("✅  Problem Discovery Engine complete\n")
print(f"   Topics         : {len(TOPICS)}")
print(f"   Patterns       : {len(PATTERNS)}")
print(f"   Total ideas    : {len(rows):,}")
print(f"   Already built  : {len(rows) - len(new_rows):,}")
print(f"   New candidates : {len(new_rows):,}")
print(f"\n   data/problem-ideas.csv      — full matrix")
print(f"   data/problem-ideas-new.csv  — {len(new_rows):,} unbuilt pages")

# Print top-10 highest-priority new ideas
print(f"\n   Top 10 highest-priority unbuilt pages:")
top10 = sorted(new_rows, key=lambda r: -r["priority_score"])[:10]
for r in top10:
    print(f"   [{r['priority_score']}] {r['slug']}")
