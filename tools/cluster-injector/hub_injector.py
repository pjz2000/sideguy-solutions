import os

hub_pages = [
    "payments.html",
    "ai-automation.html",
    "lead-generation.html",
    "business-operations.html",
    "technology-decisions.html"
]

for hub in hub_pages:
    hub_name = hub.replace(".html", "")
    card_file = f"docs/cluster-injector/{hub_name}-cards.html"

    if not os.path.exists(card_file):
        continue

    cards = open(card_file).read()
    html = open(hub).read()

    if "<!--CLUSTER_CARDS-->" in html:
        html = html.replace("<!--CLUSTER_CARDS-->", cards)
        open(hub, "w").write(html)

print("Cluster cards injected into hubs")
