"""
cluster_generator.py
--------------------
Generates page slugs from the cartesian product of:
  problems × industries × locations

Output: one slug per line → docs/cluster-expansion/page-expansion-list.txt

To extend coverage, edit the three JSON files in data/cluster-expansion/.
"""
import json

problems   = json.load(open("data/cluster-expansion/problems.json"))
industries = json.load(open("data/cluster-expansion/industries.json"))
locations  = json.load(open("data/cluster-expansion/locations.json"))

ideas = []

for problem in problems:
    for industry in industries:
        for location in locations:
            slug = (problem + "-" + industry + "-" + location).replace(" ", "-")
            ideas.append(slug)

# Deduplicate while preserving order
seen = set()
unique = []
for idea in ideas:
    if idea not in seen:
        seen.add(idea)
        unique.append(idea)

for idea in unique:
    print(idea)

import sys
print(f"\n{len(unique)} slugs generated "
      f"({len(problems)} problems × {len(industries)} industries × {len(locations)} locations)",
      file=sys.stderr)
