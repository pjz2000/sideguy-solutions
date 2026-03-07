import os
import re
import json
import datetime
from difflib import SequenceMatcher

CONTENT_DIR="."
OUT_DIR="docs/slug-intelligence"

REPORT=os.path.join(OUT_DIR,"slug-report.md")
DUPES=os.path.join(OUT_DIR,"duplicate-slugs.txt")
CANONICAL=os.path.join(OUT_DIR,"canonical-slugs.txt")
CLAUDE=os.path.join("docs/claude","slug-intelligence-brief.md")

NOW=datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

# Scan root-level HTML only (avoids tools/docs subdirs and keeps O(n²) feasible)
slugs=[]
for f in os.listdir(CONTENT_DIR):
    if f.endswith(".html") and os.path.isfile(os.path.join(CONTENT_DIR, f)):
        slugs.append(f.replace(".html",""))

def normalize_slug(s):
    s = s.lower().strip()
    s = s.replace("_","-")
    s = re.sub(r"-+","-",s)
    return s

def similarity(a,b):
    return SequenceMatcher(None,a,b).ratio()

duplicates=[]
checked=set()

for s1 in slugs:
    for s2 in slugs:
        if s1 == s2:
            continue
        a=normalize_slug(s1)
        b=normalize_slug(s2)
        key=tuple(sorted([a,b]))
        if key in checked:
            continue
        checked.add(key)
        score=similarity(a,b)
        if score > 0.85:
            duplicates.append((a,b,score))

canonical=[]

for s1,s2,score in sorted(duplicates, key=lambda x: -x[2]):
    shorter=min(s1,s2,key=len)
    canonical.append((s1,s2,shorter,score))

os.makedirs(OUT_DIR,exist_ok=True)

with open(DUPES,"w",encoding="utf-8") as f:
    for a,b,s in canonical:
        f.write(f"{a} | {b} | {s:.4f}\n")

with open(CANONICAL,"w",encoding="utf-8") as f:
    for a,b,c,s in canonical:
        f.write(f"{a} | {b} -> {c} | {s:.4f}\n")

md=[]
md.append("# SideGuy Slug Intelligence Report")
md.append("")
md.append(f"Generated: {NOW}")
md.append("")
md.append(f"Total pages scanned: {len(slugs)}")
md.append("")
md.append("## Potential Duplicates")
md.append("")
for a,b,c,s in canonical[:100]:
    md.append(f"- {a} ↔ {b} → canonical `{c}` ({s:.2f})")

with open(REPORT,"w",encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

claude=[]
claude.append("# Claude Slug Intelligence Instructions")
claude.append("")
claude.append("Use slug intelligence system before building pages.")
claude.append("")
claude.append("Rules:")
claude.append("- If slug similarity > 0.85 exists, do NOT build duplicate page")
claude.append("- Prefer expanding the existing page or choosing a better canonical slug")
claude.append("- Check docs/slug-intelligence/duplicate-slugs.txt")
claude.append("- Prefer canonical slugs listed in docs/slug-intelligence/canonical-slugs.txt")
claude.append("- Keep append-only behavior")
claude.append("- Include Text PJ orb with 773-544-1231 on all shipped pages")

with open(CLAUDE,"w",encoding="utf-8") as f:
    f.write("\n".join(claude) + "\n")

print("Slug Intelligence Generated")
print("Total slugs:", len(slugs))
print("Possible duplicates:", len(canonical))
