from pathlib import Path
from collections import defaultdict

ROOT = Path("/workspaces/sideguy-solutions")
INV = ROOT / "docs" / "inventory-brain" / "reports" / "master-inventory.tsv"
OUT = ROOT / "docs" / "inventory-brain" / "reports" / "link-improvement-queue.md"

clusters = defaultdict(list)
with open(INV, encoding="utf-8") as f:
    next(f)
    for line in f:
        score, cluster, path, words, links, h2s, faq, textpj, age_days, title = line.rstrip("\n").split("\t")
        clusters[cluster].append({
            "path": path,
            "score": int(score),
            "links": int(links),
        })

with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Link Improvement Queue\n\n")
    for cluster, rows in sorted(clusters.items()):
        strong = sorted(rows, key=lambda x: (-x["score"], x["path"]))[:5]
        weak = sorted([r for r in rows if r["links"] < 6], key=lambda x: (x["links"], -x["score"], x["path"]))[:15]
        if not strong or not weak:
            continue
        f.write(f"## {cluster}\n\n")
        for w in weak:
            sources = ", ".join(s["path"] for s in strong if s["path"] != w["path"])
            f.write(f"- Add links into **{w['path']}** from: {sources}\n")
        f.write("\n")

print(f"Wrote {OUT}")
