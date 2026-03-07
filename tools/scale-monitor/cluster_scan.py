"""
cluster_scan.py
---------------
Keyword-based topic cluster analysis — same taxonomy as the rest of the system.
Avoids the noise of split("-")[0] on long descriptive slugs.
"""
import os
from collections import defaultdict

TOPICS = {
    "payments":             ["payment", "stripe", "merchant", "pos", "credit-card",
                             "chargeback", "processor", "fees", "invoice"],
    "ai-automation":        ["ai-", "-ai-", "automation", "chatbot", "ai-agent",
                             "machine-learning", "openai", "zapier", "workflow"],
    "lead-generation":      ["lead", "seo", "google-ads", "traffic", "backlink",
                             "ranking", "gmb", "local-search"],
    "business-operations":  ["crm", "operations", "scheduling", "inventory",
                             "employee", "payroll", "erp", "quickbooks"],
    "technology-decisions": ["software", "saas", "tool", "tech", "platform",
                             "compare", "best-", "vs-", "review"],
    "hvac":                 ["hvac", "ac-", "-ac-", "air-conditioning", "furnace",
                             "heat-pump", "cooling", "heating"],
    "plumbing":             ["plumb", "leak", "pipe", "drain", "water-heater",
                             "sewer", "faucet"],
    "electrical":           ["electric", "wiring", "panel", "outlet", "circuit",
                             "generator"],
    "home-services":        ["contractor", "roofing", "landscaping", "adu",
                             "remodel", "handyman", "pest"],
    "finance":              ["financ", "accounting", "bookkeep", "tax",
                             "budget", "cash-flow", "revenue"],
    "restaurants":          ["restaurant", "food", "cafe", "bar", "catering",
                             "hospitality"],
}

counts = defaultdict(int)
uncategorized = 0

for root, dirs, files in os.walk("."):
    for f in files:
        if not f.endswith(".html"):
            continue
        slug = f.replace(".html", "").lower()
        matched = False
        for topic, keywords in TOPICS.items():
            if any(kw in slug for kw in keywords):
                counts[topic] += 1
                matched = True
                break
        if not matched:
            counts["other"] += 1

print("Cluster Distribution (keyword-matched):")
for topic, count in sorted(counts.items(), key=lambda x: -x[1]):
    bar = "#" * min(count // 50, 40)
    print(f"  {topic:<24} {count:>6}  {bar}")
print(f"\n  Total tracked: {sum(counts.values())}")
