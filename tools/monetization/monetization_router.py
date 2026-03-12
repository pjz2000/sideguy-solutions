import os
import glob
import datetime

ROOT = "."
LOG = "docs/monetization/page-monetization.tsv"

def detect_vertical(page):
    p = page.lower()
    if "hvac" in p or "ac-" in p:
        return "hvac_service"
    if "payment" in p or "merchant" in p:
        return "payments"
    if "ai" in p or "automation" in p:
        return "ai_services"
    if "software" in p or "saas" in p:
        return "affiliate_tools"
    return "general_help"

pages = glob.glob("*.html")

rows = []

for page in pages:
    vertical = detect_vertical(page)
    rows.append(page + "\t" + vertical + "\t" + datetime.datetime.utcnow().isoformat())

with open(LOG, "w") as f:
    f.write("page\tvertical\ttimestamp\n")
    for r in rows:
        f.write(r + "\n")

print("Monetization router mapped", len(rows), "pages")
