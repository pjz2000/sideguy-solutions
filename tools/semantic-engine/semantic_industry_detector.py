from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions/public")

industry_terms = {
    "hvac":        ["hvac", "heating", "cooling", "air conditioning", "furnace"],
    "plumber":     ["plumbing", "pipe", "water heater", "drain"],
    "dentist":     ["dental", "dentist", "teeth", "patient"],
    "restaurant":  ["restaurant", "menu", "reservation", "dining"],
    "law firm":    ["law", "legal", "attorney", "case"],
    "real estate": ["real estate", "property", "listing", "realtor"],
    "contractor":  ["contractor", "construction", "project"],
    "auto repair": ["mechanic", "auto repair", "vehicle", "garage"],
    "salon":       ["salon", "hair", "stylist", "beauty"],
    "medical":     ["clinic", "doctor", "medical", "patient"],
}

pages = list(ROOT.rglob("*.html"))

matches = []

for page in pages:
    text = page.read_text(errors="ignore").lower()

    detected = "business"

    for industry, terms in industry_terms.items():
        if any(term in text for term in terms):
            detected = industry
            break

    matches.append((page.name, detected))

for m in matches[:25]:
    print(m)

print("Semantic detection complete")
