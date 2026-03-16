from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
INV = ROOT / "docs" / "inventory-brain" / "reports" / "master-inventory.tsv"
OUT = ROOT / "docs" / "inventory-brain" / "reports" / "freshness-queue.md"

rows = []
with open(INV, encoding="utf-8") as f:
    next(f)
    for line in f:
        score, cluster, path, words, links, h2s, faq, textpj, age_days, title = line.rstrip("\n").split("\t")
        rows.append((int(age_days), cluster, path, int(score)))

rows.sort(key=lambda x: (-x[0], -x[3], x[2]))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Freshness Queue\n\n")
    for age_days, cluster, path, score in rows[:200]:
        f.write(f"- **{path}** ({cluster}) — age {age_days} days — score {score}\n")

print(f"Wrote {OUT}")
