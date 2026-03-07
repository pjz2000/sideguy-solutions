"""
build_graph.py
--------------
Walks all HTML pages and bins them into topic buckets by keyword matching.
Writes docs/topic-graph/topic_graph.json with { topic: [page_paths] }.
"""
import os, json

topics = {
    "payments":             ["payment", "merchant", "chargeback", "stripe",
                             "processing", "fees", "processor", "invoice"],
    "ai-automation":        ["ai-", "-ai-", "automation", "agent", "openai",
                             "workflow", "chatbot", "zapier"],
    "lead-generation":      ["seo", "traffic", "ads", "google", "lead",
                             "ranking", "backlink", "gmb"],
    "business-operations":  ["crm", "operations", "inventory", "scheduling",
                             "erp", "employee", "payroll"],
    "technology-decisions": ["software", "platform", "tools", "comparison",
                             "saas", "compare", "review"],
    "finance":              ["finance", "accounting", "tax", "forecast",
                             "bookkeep", "budget", "cash-flow"],
    "home-services":        ["hvac", "plumbing", "electrical", "repair",
                             "contractor", "roofing", "landscaping",
                             "handyman", "pest"],
    "restaurants":          ["restaurant", "food", "cafe", "bar", "catering",
                             "hospitality"],
    "auto":                 ["auto-repair", "auto-glass", "auto-detail",
                             "auto-body", "mechanic"],
    "professional-services":["dental", "salon", "spa", "chiropract",
                             "optom", "veterinary"],
}

graph = {}

for root, dirs, files in os.walk("."):
    for f in files:
        if not f.endswith(".html"):
            continue
        name = f.lower()
        for topic, words in topics.items():
            for w in words:
                if w in name:
                    graph.setdefault(topic, []).append(os.path.join(root, f))
                    break  # one topic per page (first match wins)

print("\nTopics discovered:", len(graph))
for t, pages in sorted(graph.items(), key=lambda x: -len(x[1])):
    print(f"  {t:<26} {len(pages):>6} pages")

os.makedirs("docs/topic-graph", exist_ok=True)

with open("docs/topic-graph/topic_graph.json", "w") as f:
    json.dump(graph, f, indent=2)

print("\nGraph written to docs/topic-graph/topic_graph.json")
