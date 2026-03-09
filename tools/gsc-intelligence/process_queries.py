import csv
from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
INPUT = ROOT / "docs/gsc-intelligence/search_console_queries.csv"
OUTPUT = ROOT / "docs/gsc-intelligence/generated/page_ideas.txt"

queries = []

with open(INPUT) as f:
    reader = csv.DictReader(f)

    for row in reader:
        q = row["Query"].lower()

        if "ai" in q or "automation" in q or "chatbot" in q:
            queries.append(q)

queries = list(set(queries))

with open(OUTPUT, "w") as out:
    for q in queries:
        out.write(q + "\n")

print("Generated page ideas:", len(queries))
