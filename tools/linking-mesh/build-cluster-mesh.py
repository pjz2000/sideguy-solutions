#!/usr/bin/env python3

import os
import re

ROOT = os.getcwd()

pages = [p for p in os.listdir(ROOT) if p.endswith(".html")]

slug_map = {}

for page in pages:
    words = page.replace(".html","").split("-")
    for w in words:
        slug_map.setdefault(w, []).append(page)

for page in pages:

    words = page.replace(".html","").split("-")

    related = set()

    for w in words:
        for p in slug_map.get(w, []):
            if p != page:
                related.add(p)

    related = list(related)[:5]

    if not related:
        continue

    path = os.path.join(ROOT,page)

    with open(path,"r",errors="ignore") as f:
        html = f.read()

    if "SideGuy Related Pages" in html:
        continue

    links = "\n".join(
        [f'<li><a href="/{r}">{r.replace(".html","").replace("-"," ")}</a></li>'
         for r in related]
    )

    block = f'''
<section class="sideguy-related-pages">
<h2>SideGuy Related Pages</h2>
<ul>
{links}
</ul>
</section>
'''

    html = html.replace("</body>", block + "\n</body>")

    with open(path,"w") as f:
        f.write(html)

print("Cluster mesh linking complete")

