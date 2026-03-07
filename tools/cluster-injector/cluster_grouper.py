import os

expansion_file = "docs/growth-engine/page-expansion.txt"

hubs = {
    "payments": [],
    "ai-automation": [],
    "lead-generation": [],
    "business-operations": [],
    "technology-decisions": []
}

if not os.path.exists(expansion_file):
    print("Missing page expansion list")
    exit()

pages = open(expansion_file).read().splitlines()

for p in pages:
    if "payment" in p or "stripe" in p or "merchant" in p:
        hubs["payments"].append(p)
    elif "ai" in p:
        hubs["ai-automation"].append(p)
    elif "lead" in p or "seo" in p:
        hubs["lead-generation"].append(p)
    elif "crm" in p or "operations" in p:
        hubs["business-operations"].append(p)
    else:
        hubs["technology-decisions"].append(p)

os.makedirs("docs/cluster-injector", exist_ok=True)

for h in hubs:
    with open(f"docs/cluster-injector/{h}-clusters.txt", "w") as f:
        for p in hubs[h]:
            f.write(p + "\n")

print("Cluster grouping complete")
