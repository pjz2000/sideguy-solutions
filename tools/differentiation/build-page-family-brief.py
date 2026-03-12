from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
OUT = ROOT / "docs/differentiation/page-family-brief.md"

topics = [
    "ai dispatch",
    "ai scheduling",
    "payment processing fees",
    "stablecoin payments",
    "software development cost"
]

with open(OUT, "w") as f:
    f.write("# SideGuy Page Family Brief\n\n")
    for topic in topics:
        f.write(f"## {topic.title()}\n")
        f.write(f"- Explainer: what-is-{topic.replace(' ','-')}.html\n")
        f.write(f"- Cost: how-much-does-{topic.replace(' ','-')}-cost.html\n")
        f.write(f"- Comparison: {topic.replace(' ','-')}-vs-alternatives.html\n")
        f.write(f"- Industry: {topic.replace(' ','-')}-for-contractors.html\n")
        f.write(f"- Local: {topic.replace(' ','-')}-san-diego.html\n\n")

print(f"Wrote {OUT}")
