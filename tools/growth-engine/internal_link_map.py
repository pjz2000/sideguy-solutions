import json

industries = json.load(open("docs/growth-engine/industries.json"))
problems = json.load(open("docs/growth-engine/problem-clusters.json"))

links = []

for p in problems:
    hub = p
    for i in industries:
        spoke = f"{p}-{i}"
        links.append((hub, spoke))

with open("docs/growth-engine/link-map.txt","w") as f:
    for h, s in links:
        f.write(f"{h} -> {s}\n")

print("Generated",len(links),"hub-spoke links")
