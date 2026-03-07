import os
import json
import datetime
from collections import defaultdict

CONTENT_DIR="."
OUTPUT_JSON="docs/topic-galaxy/topic-galaxy.json"
OUTPUT_MD="docs/topic-galaxy/topic-galaxy.md"
GAPS_FILE="docs/topic-galaxy/cluster-gaps.txt"
NEXT_FILE="docs/topic-galaxy/next-20-authority-pages.txt"
CLAUDE_FILE="docs/claude/topic-galaxy-brief.md"

NOW=datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

TOPIC_PATTERNS={
    "payments":["payment","payments","merchant","processing","chargeback","settlement"],
    "ai":["ai","agent","automation","llm","gpt"],
    "seo":["seo","ranking","traffic","google","lead"],
    "crypto":["crypto","solana","blockchain","stablecoin","kalshi","prediction-market"],
    "software":["software","platform","saas","system","compliance"],
    "local":["san-diego","carlsbad","encinitas","coronado","near-me","california"],
    "future":["future","robot","autonomous","prediction"],
    "memes":["meme","funny","viral"]
}

pages=[]

for root, dirs, files in os.walk(CONTENT_DIR):
    for f in files:
        if f.endswith(".html"):
            path=os.path.join(root,f)
            pages.append(path.replace("./",""))

clusters=defaultdict(list)

for path in pages:
    slug=os.path.basename(path).replace(".html","").lower()
    for topic,words in TOPIC_PATTERNS.items():
        for w in words:
            if w in slug:
                clusters[topic].append(path)
                break

cluster_counts={k:len(v) for k,v in clusters.items()}
ideal_cluster_size=50
gaps=[]

for topic in TOPIC_PATTERNS:
    count=cluster_counts.get(topic,0)
    if count < ideal_cluster_size:
        gaps.append((topic, ideal_cluster_size-count))

next_pages=[]
for topic,missing in gaps:
    for i in range(min(3, missing)):
        next_pages.append(f"{topic}-guide-{i+1}")

galaxy={
    "generated":NOW,
    "total_pages":len(pages),
    "clusters":cluster_counts,
    "gaps":gaps
}

with open(OUTPUT_JSON,"w",encoding="utf-8") as f:
    json.dump(galaxy,f,indent=2)

md=[]
md.append("# SideGuy Topic Galaxy")
md.append("")
md.append(f"Generated: {NOW}")
md.append("")
md.append(f"Total pages detected: {len(pages)}")
md.append("")
md.append("## Cluster Counts")
md.append("")
for k in sorted(cluster_counts):
    md.append(f"- {k}: {cluster_counts[k]}")
md.append("")
md.append("## Cluster Gaps")
md.append("")
for topic,missing in gaps:
    md.append(f"- {topic} needs {missing} more pages")
md.append("")

with open(OUTPUT_MD,"w",encoding="utf-8") as f:
    f.write("\n".join(md))

with open(GAPS_FILE,"w",encoding="utf-8") as f:
    for topic,missing in gaps:
        f.write(f"{topic} {missing}\n")

with open(NEXT_FILE,"w",encoding="utf-8") as f:
    for p in next_pages[:20]:
        f.write(p+"\n")

claude=[]
claude.append("# Claude Topic Galaxy Execution")
claude.append("")
claude.append("Use `docs/topic-galaxy/next-20-authority-pages.txt`.")
claude.append("")
claude.append("Rules:")
claude.append("- append-only")
claude.append("- use existing SideGuy template")
claude.append("- add to sitemap")
claude.append("- add to index")
claude.append("- cross-link hubs")
claude.append("- commit after each page")
claude.append("- include Text PJ orb with 773-544-1231")

with open(CLAUDE_FILE,"w",encoding="utf-8") as f:
    f.write("\n".join(claude) + "\n")

print("Topic Galaxy generated")
print("Total pages:", len(pages))
print("Clusters:", cluster_counts)
