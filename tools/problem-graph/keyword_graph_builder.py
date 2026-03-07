import os
import json
from collections import Counter

STOPWORDS = {
    "the","a","an","and","or","of","to","in","for","on","at","is","it",
    "with","that","this","was","are","be","by","from","as","we","you",
    "your","our","not","so","if","can","do","how","what","why","when",
    "but","more","about","get","have","all","just","too","also","its",
    "has","will","i","my","one","s","via","per","vs","see","new","way",
}

SOURCES = [
    "docs/problem-engine/problem-signals.txt",
    "docs/problem-scanner/problem-signals.txt",
    "docs/trend-radar/trend-signals.txt",
]

words = []
loaded = 0
for s in SOURCES:
    if os.path.exists(s):
        with open(s) as f:
            for line in f:
                words.extend(
                    w.strip(".,:-()[]")
                    for w in line.lower().split()
                    if w.strip(".,:-()[]") and w.strip(".,:-()[]") not in STOPWORDS
                )
        loaded += 1

counts = Counter(words)
top_words = [w for w, c in counts.most_common(40) if len(w) > 2]
nodes = [{"id": w, "value": counts[w]} for w in top_words]

# Co-occurrence links only (not full cartesian product)
cooccur = Counter()
for s in SOURCES:
    if not os.path.exists(s):
        continue
    with open(s) as f:
        for line in f:
            tokens = list({
                w.strip(".,:-()[]")
                for w in line.lower().split()
                if w.strip(".,:-()[]") in set(top_words)
            })
            for i, a in enumerate(tokens):
                for b in tokens[i+1:]:
                    cooccur[tuple(sorted([a, b]))] += 1

links = [
    {"source": a, "target": b, "strength": c}
    for (a, b), c in cooccur.most_common(80)
]

graph = {"nodes": nodes, "links": links, "loaded_sources": loaded}
os.makedirs("docs/problem-graph", exist_ok=True)
with open("docs/problem-graph/problem-graph.json", "w") as f:
    json.dump(graph, f, indent=2)

print(f"Graph data created: {len(nodes)} nodes, {len(links)} links")
print(f"Top keywords: {', '.join(n['id'] for n in nodes[:10])}")
