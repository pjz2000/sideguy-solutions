import os
import re
import csv

ROOT="."
OUTPUT="docs/content-upgrades/upgrade_targets.tsv"

pages=[]

for root,dirs,files in os.walk(ROOT):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(root,f))

results=[]

for p in pages:
    try:
        with open(p,"r",encoding="utf8") as f:
            c=f.read().lower()

        score=0
        flags=[]

        if "faq" not in c:
            flags.append("missing_faq")
            score+=1

        if "calculator" not in c:
            flags.append("no_calculator")
            score+=1

        if "comparison" not in c and "vs" not in p:
            flags.append("no_comparison_section")
            score+=1

        if len(c)<2500:
            flags.append("thin_content")
            score+=1

        results.append((score,p,";".join(flags)))

    except:
        pass

results.sort(reverse=True)

with open(OUTPUT,"w") as out:
    w=csv.writer(out,delimiter="\t")
    for r in results:
        w.writerow(r)

print("Upgrade targets written to",OUTPUT)
