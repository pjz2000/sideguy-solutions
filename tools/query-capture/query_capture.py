import csv, re
from collections import Counter, defaultdict

INPUT = "data/query-capture/gsc_queries.csv"
IDEAS_TXT = "docs/query-capture/page-ideas.txt"
IDEAS_CSV = "docs/query-capture/page-ideas.csv"
CLUSTERS = "docs/query-capture/top-clusters.txt"

stop = {"a","the","for","to","and","of","in","on","with","is","are","how","what","best","near","me"}

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s[:120]

queries = []
with open(INPUT) as f:
    r = csv.DictReader(f)
    for row in r:
        q = (row.get("Top queries") or row.get("Query") or row.get("query") or "").strip()
        if q:
            queries.append(q.lower())

# cluster by keyword tokens
clusters = defaultdict(list)
for q in queries:
    tokens = [t for t in re.split(r"\W+", q) if t and t not in stop]
    key = " ".join(tokens[:2]) if tokens else q
    clusters[key].append(q)

top = Counter({k: len(v) for k, v in clusters.items()}).most_common(50)

ideas = []
for key, count in top:
    sample = clusters[key][:5]
    for q in sample:
        title = f"{q} — options, tools, and how to fix it"
        slug = slugify(q)
        ideas.append((q, title, slug))

# write clusters
with open(CLUSTERS, "w") as f:
    for k, c in top:
        f.write(f"{k}\t{c}\n")

# write ideas
with open(IDEAS_TXT, "w") as f:
    for q, t, s in ideas:
        f.write(f"{t} | /{s}\n")

with open(IDEAS_CSV, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["query", "title", "slug"])
    for q, t, s in ideas:
        w.writerow([q, t, s])

print("Queries read:", len(queries))
print("Clusters written:", len(top))
print("Page ideas:", len(ideas))
