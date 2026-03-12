import csv

SRC = "docs/monetization/monetization-radar.tsv"
OUT = "docs/monetization/upgrade-targets.md"

rows = []
with open(SRC, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        row["score"] = int(row["score"])
        row["word_count"] = int(row["word_count"])
        row["cta_count"] = int(row["cta_count"])
        row["faq_count"] = int(row["faq_count"])
        row["has_text_pj"] = int(row["has_text_pj"])
        rows.append(row)

high_value_quick_wins = []
for r in rows:
    if r["score"] >= 45 and (r["has_text_pj"] == 0 or r["faq_count"] == 0 or r["cta_count"] == 0):
        high_value_quick_wins.append(r)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("# SideGuy Upgrade Targets\n\n")
    f.write("These are high-value pages with easy monetization improvements.\n\n")
    for r in high_value_quick_wins[:25]:
        f.write(f"## {r['page']}\n")
        f.write(f"- Score: **{r['score']}**\n")
        f.write(f"- Category: **{r['category']}**\n")
        f.write(f"- Word count: {r['word_count']}\n")
        f.write(f"- CTA count: {r['cta_count']}\n")
        f.write(f"- FAQ count: {r['faq_count']}\n")
        f.write(f"- Text PJ present: {r['has_text_pj']}\n")
        f.write(f"- Quick wins: {r['quick_wins']}\n\n")

print("Upgrade targets report written to", OUT)
