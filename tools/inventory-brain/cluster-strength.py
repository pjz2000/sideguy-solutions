from pathlib import Path
from collections import defaultdict

ROOT = Path("/workspaces/sideguy-solutions")
INV = ROOT / "docs" / "inventory-brain" / "reports" / "master-inventory.tsv"
STRONG = ROOT / "docs" / "inventory-brain" / "reports" / "strong-clusters.md"
WEAK = ROOT / "docs" / "inventory-brain" / "reports" / "weak-clusters.md"

clusters = defaultdict(list)

with open(INV, encoding="utf-8") as f:
    next(f)
    for line in f:
        score, cluster, path, words, links, h2s, faq, textpj, age_days, title = line.rstrip("\n").split("\t")
        clusters[cluster].append({
            "score": int(score),
            "path": path,
            "words": int(words),
            "links": int(links),
            "faq": int(faq),
            "age_days": int(age_days),
        })

summary = []
for cluster, rows in clusters.items():
    pages = len(rows)
    avg_score = round(sum(r["score"] for r in rows) / max(1, pages), 2)
    avg_words = round(sum(r["words"] for r in rows) / max(1, pages), 2)
    avg_links = round(sum(r["links"] for r in rows) / max(1, pages), 2)
    faq_rate = round(sum(r["faq"] for r in rows) / max(1, pages), 2)
    summary.append((cluster, pages, avg_score, avg_words, avg_links, faq_rate))

summary.sort(key=lambda x: (-x[2], -x[1], x[0]))

with open(STRONG, "w", encoding="utf-8") as f:
    f.write("# Strong Clusters\n\n")
    for cluster, pages, avg_score, avg_words, avg_links, faq_rate in summary[:20]:
        f.write(f"- **{cluster}** — pages: {pages}, avg score: {avg_score}, avg words: {avg_words}, avg links: {avg_links}, faq rate: {faq_rate}\n")

with open(WEAK, "w", encoding="utf-8") as f:
    f.write("# Weak Clusters\n\n")
    weak_sorted = sorted(summary, key=lambda x: (x[2], x[1], x[0]))
    for cluster, pages, avg_score, avg_words, avg_links, faq_rate in weak_sorted[:20]:
        f.write(f"- **{cluster}** — pages: {pages}, avg score: {avg_score}, avg words: {avg_words}, avg links: {avg_links}, faq rate: {faq_rate}\n")

print(f"Wrote {STRONG}")
print(f"Wrote {WEAK}")
