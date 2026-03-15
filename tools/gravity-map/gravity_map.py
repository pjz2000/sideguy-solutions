import os,re

ROOT="public"
report="docs/gravity-map/reports/gravity-map.csv"

results=[]

for root,dirs,files in os.walk(ROOT):
    for f in files:
        if not f.endswith(".html"): continue
        path=os.path.join(root,f)
        try:
            text=open(path).read()
        except:
            continue
        words=len(text.split())
        links=len(re.findall(r'href="/',text))
        score=words+links*300
        results.append((score,path))

results.sort(reverse=True)

with open(report,"w") as f:
    f.write("score,page\n")
    for r in results[:300]:
        f.write(f"{r[0]},{r[1]}\n")

print("Gravity map created")
