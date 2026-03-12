import csv
import os

INPUT="Table.csv"
OUTPUT="docs/seo-boost/impression-pages.md"

def slug_to_title(slug):

    slug=slug.replace(".html","")
    parts=slug.split("-")
    parts=[p.capitalize() for p in parts]

    return " ".join(parts)

def build_title(slug):

    base=slug_to_title(slug)

    if "san-diego" in slug:
        return f"{base} | San Diego Guide (Costs, Tools & Setup)"

    if "ai" in slug:
        return f"{base} | AI Automation Guide for Businesses"

    if "payments" in slug:
        return f"{base} | Lower Payment Processing Fees"

    return f"{base} | SideGuy Guide"

def build_meta(slug):

    base=slug_to_title(slug)

    return f"Learn how {base.lower()} works, what it costs, and how businesses use it to save time or reduce fees."

pages=[]

if os.path.exists(INPUT):

    with open(INPUT) as f:

        reader=csv.DictReader(f)

        for r in reader:

            url=r["Page"]

            if ".html" in url:

                slug=url.split("/")[-1]
                pages.append(slug)

with open(OUTPUT,"w") as f:

    f.write("# Pages With Google Impressions\n\n")

    for p in pages:

        title=build_title(p)
        meta=build_meta(p)

        f.write(f"## {p}\n\n")
        f.write("Suggested Title:\n")
        f.write(f"{title}\n\n")
        f.write("Suggested Meta Description:\n")
        f.write(f"{meta}\n\n")

print("Report written:",OUTPUT)
