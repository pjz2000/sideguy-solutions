import os

ROOT="public"
OUTPUT="docs/seo-boost/link-opportunities.md"

targets=[
"san-diego-mobile-business-payments.html",
"mobile-operator-payments-san-diego.html",
"ai-lead-generation-systems-san-diego.html",
"tech-help-hub-san-diego.html",
"software-development-hub-san-diego.html"
]

results=[]

for root,dirs,files in os.walk(ROOT):

    for file in files:

        if file.endswith(".html"):

            path=os.path.join(root,file)

            try:

                text=open(path,encoding="utf-8").read().lower()

                for t in targets:

                    key=t.replace(".html","").replace("-"," ")

                    if key.split()[0] in text:
                        results.append((file,t))

            except:
                pass

with open(OUTPUT,"w") as f:

    f.write("# Internal Link Opportunities\n\n")

    for r in results:
        f.write(f"{r[0]} → {r[1]}\n")

print("Link opportunities written:",OUTPUT)
