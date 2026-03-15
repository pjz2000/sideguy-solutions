import os,re

ROOT="public"
report="docs/signal-miner/reports/signal-report.csv"

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
        score=words+links*200
        results.append((score,path))

results.sort(reverse=True)

with open(report,"w") as f:
    f.write("score,page\n")
    for s,p in results[:200]:
        f.write(f"{s},{p}\n")

print("Signal miner report written")
