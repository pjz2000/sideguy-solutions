"""
authority_map.py
----------------
Maps all HTML pages to topic clusters using keyword matching.
Produces an authority score (page count) per topic — mirroring
the taxonomy used across scale-monitor, topic-graph, and cluster-scan.
"""
import os
from collections import defaultdict

TOPICS = {
    "ai-automation":        ["ai-", "-ai-", "automation", "agent", "openai",
                             "workflow", "chatbot", "zapier", "machine-learning"],
    "payments":             ["payment", "merchant", "chargeback", "stripe",
                             "processing", "fees", "processor", "invoice", "pos"],
    "technology-decisions": ["software", "saas", "platform", "tools",
                             "comparison", "compare", "vs-", "review"],
    "finance":              ["financ", "accounting", "bookkeep", "tax",
                             "budget", "cash-flow", "revenue", "forecast"],
    "home-services":        ["hvac", "plumbing", "roofing", "landscaping",
                             "contractor", "handyman", "pest", "adu"],
    "electrical":           ["electric", "wiring", "panel", "outlet",
                             "circuit", "generator"],
    "lead-generation":      ["lead", "seo", "traffic", "google-ads",
                             "backlink", "ranking", "gmb", "local-search"],
    "business-operations":  ["crm", "operations", "inventory", "scheduling",
                             "employee", "payroll", "erp", "quickbooks"],
    "restaurants":          ["restaurant", "food", "cafe", "bar",
                             "catering", "hospitality"],
    "auto":                 ["auto-repair", "auto-glass", "auto-detail",
                             "auto-body", "mechanic"],
    "professional-services":["dental", "salon", "spa", "chiropract",
                             "optom", "veterinary", "retail"],
}

clusters = defaultdict(int)
uncategorized = 0
total = 0

for root, dirs, files in os.walk("."):
    for f in files:
        if not f.endswith(".html"):
            continue
        total += 1
        slug = f.replace(".html", "").lower()
        matched = False
        for topic, keywords in TOPICS.items():
            if any(kw in slug for kw in keywords):
                clusters[topic] += 1
                matched = True
                break
        if not matched:
            uncategorized += 1

print("SIDEGUY AUTHORITY MAP")
print("=" * 45)
print(f"{'Topic':<26} {'Pages':>7}  {'Authority Bar'}")
print("-" * 45)

for topic, count in sorted(clusters.items(), key=lambda x: -x[1]):
    bar = "█" * min(count // 100, 30)
    print(f"{topic:<26} {count:>7}  {bar}")

print("-" * 45)
print(f"{'other (uncategorized)':<26} {uncategorized:>7}")
print(f"{'TOTAL':<26} {total:>7}")
print("=" * 45)
