import json
import os

industries = json.load(open("docs/growth-engine/industries.json"))
locations = json.load(open("docs/growth-engine/locations.json"))
problems = json.load(open("docs/growth-engine/problem-clusters.json"))

out = []

for p in problems:
    for i in industries:
        for l in locations:
            slug = f"{p}-{i}-{l}"
            out.append(slug)

os.makedirs("docs/growth-engine", exist_ok=True)

with open("docs/growth-engine/page-expansion.txt","w") as f:
    for s in out:
        f.write(s + "\n")

print("Generated",len(out),"page slugs")
