import csv
import os

INPUT  = "radar/problem-radar-new.csv"
OUTPUT = "longtail/longtail-keywords.csv"

PLATFORMS = [
    "shopify", "wordpress", "stripe", "square", "quickbooks",
    "hubspot", "zapier", "make.com", "gmail", "google ads", "cloudflare",
]

INDUSTRIES = [
    "restaurants", "dentists", "hvac", "law firms", "accountants",
    "ecommerce stores", "agencies", "consultants", "contractors",
]

LOCATIONS = [
    "san diego", "california", "usa",
]

rows = []

if os.path.exists(INPUT):
    with open(INPUT) as f:
        reader = csv.DictReader(f)
        for r in reader:
            base = r["slug"].replace("-", " ")
            for p in PLATFORMS:
                rows.append(base + " " + p)
            for i in INDUSTRIES:
                rows.append(base + " for " + i)
            for l in LOCATIONS:
                rows.append(base + " " + l)

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["keyword"])
    for r in rows:
        writer.writerow([r])

print(f"Generated {len(rows)} long tail keywords → {OUTPUT}")
