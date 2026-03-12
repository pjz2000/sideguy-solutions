from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
pages = list(ROOT.glob("*.html"))

families = {
    "cost": ["Cost Considerations", "ROI", "pricing", "cost"],
    "comparison": ["vs", "tradeoff", "Where", "wins"],
    "explainer": ["How It Works", "What", "Overview"],
    "industry": ["workflow", "operator", "use case", "team"],
    "local": ["San Diego", "local", "regional", "nearby"]
}

for page in pages[:500]:
    text = page.read_text(errors="ignore")
    lower = text.lower()
    matched = []

    for family, hints in families.items():
        for hint in hints:
            if hint.lower() in lower:
                matched.append(family)
                break

    if len(set(matched)) == 0:
        print(f"NO_FAMILY_SIGNAL | {page.name}")
