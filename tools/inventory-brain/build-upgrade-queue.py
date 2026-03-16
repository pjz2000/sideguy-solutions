from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
INV = ROOT / "docs" / "inventory-brain" / "reports" / "master-inventory.tsv"
OUT = ROOT / "docs" / "inventory-brain" / "reports" / "priority-upgrade-queue.md"

rows = []
with open(INV, encoding="utf-8") as f:
    next(f)
    for line in f:
        score, cluster, path, words, links, h2s, faq, textpj, age_days, title = line.rstrip("\n").split("\t")
        score = int(score)
        words = int(words)
        links = int(links)
        h2s = int(h2s)
        faq = int(faq)
        textpj = int(textpj)
        age_days = int(age_days)

        priority = 0
        reasons = []

        if words < 700:
            priority += 2
            reasons.append("expand-content")
        if links < 8:
            priority += 2
            reasons.append("add-links")
        if faq == 0:
            priority += 3
            reasons.append("add-faq")
        if textpj == 0:
            priority += 2
            reasons.append("add-text-pj")
        if h2s < 4:
            priority += 1
            reasons.append("add-sections")
        if age_days > 30:
            priority += 2
            reasons.append("refresh-page")
        if score > 20:
            priority += 2
            reasons.append("already-has-gravity")

        if priority > 0:
            rows.append((priority, cluster, path, reasons))

rows.sort(key=lambda x: (-x[0], x[1], x[2]))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Priority Upgrade Queue\n\n")
    for priority, cluster, path, reasons in rows[:200]:
        f.write(f"- **{path}** ({cluster}) — priority {priority} — {', '.join(reasons)}\n")

print(f"Wrote {OUT}")
