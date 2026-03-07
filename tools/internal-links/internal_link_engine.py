import os
import random

pages_dir="public/problem-pages"
manifest="docs/internal-links/link-map.txt"

files=[f for f in os.listdir(pages_dir) if f.endswith(".html")]

link_map={}

for f in files:

    others=[x for x in files if x!=f]

    related=random.sample(others,min(5,len(others)))

    link_map[f]=related

with open(manifest,"w") as out:

    for page,links in link_map.items():

        out.write(page+" -> "+",".join(links)+"\n")

# Inject links — use a unique marker so we don't conflict with template content
MARKER="<!-- SG_AUTO_LINKS -->"

for page,links in link_map.items():

    path=os.path.join(pages_dir,page)

    html=open(path).read()

    if MARKER in html:
        continue  # already linked

    block="\n"+MARKER+"\n<h3>Related Problems</h3>\n<ul>\n"

    for l in links:

        slug=l.replace(".html","")

        block+=f'<li><a href="/problem-pages/{slug}.html">{slug.replace("-"," ")}</a></li>\n'

    block+="</ul>\n"

    html=html.replace("</body>",block+"\n</body>")

    with open(path,"w") as f:
        f.write(html)

print("Internal linking complete:",len(link_map),"pages linked")
