import os
import random

ROOT="public"
OUTPUT="docs/crawl-router/authority_links.md"

targets=[
"/san-diego-mobile-business-payments.html",
"/mobile-operator-payments-san-diego.html",
"/ai-lead-generation-systems-san-diego.html",
"/tech-help-hub-san-diego.html",
"/software-development-hub-san-diego.html"
]

pages=[]

for root,dirs,files in os.walk(ROOT):

    if ".git" in root:
        continue

    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(root,f))

routes=[]

for p in pages:

    if random.random()<0.03:
        t=random.choice(targets)
        routes.append((p,t))

with open(OUTPUT,"w") as f:

    f.write("# Crawl Authority Routes\n\n")

    for r in routes:
        f.write(f"{r[0]} → {r[1]}\n")

print("Authority routing map written:",OUTPUT)
