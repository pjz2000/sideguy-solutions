"""
build_related.py
----------------
Reads topic_graph.json and writes one related-pages list per topic
to docs/topic-graph/<topic>_related.txt (capped at 100 per file).
"""
import json, os

path = "docs/topic-graph/topic_graph.json"

if not os.path.exists(path):
    print("Topic graph missing — run build_graph.py first")
    exit(1)

with open(path) as f:
    graph = json.load(f)

for topic, pages in sorted(graph.items(), key=lambda x: -len(x[1])):
    out = f"docs/topic-graph/{topic}_related.txt"
    with open(out, "w") as f2:
        for p in pages[:100]:
            f2.write(p + "\n")
    print(f"  {topic:<26} -> {len(pages):>6} pages  (saved top 100)")

print("\nRelated page lists built")
