import os, re

KM = "knowledge/sideguy-knowledge-map.html"
if not os.path.exists(KM):
    print("No knowledge map found. Skipping.")
    raise SystemExit(0)

html = open(KM, "r", encoding="utf-8", errors="ignore").read()

marker = "<!-- AUTHORITY_ENGINE_LINK -->"
if marker in html:
    print("Already wired.")
    raise SystemExit(0)

ins = (
    f"\n{marker}\n"
    '<div class="nodeCard">'
    '<div class="nodeTitle">Authority Engine</div>'
    '<div class="nodeMeta">Topic hubs → cluster hubs → best guides</div>'
    '<a class="nodeLink" href="/authority/index.html">Authority Engine</a>'
    "</div>\n"
)

if "</h1>" in html:
    html = html.replace("</h1>", "</h1>" + ins, 1)
else:
    html = ins + html

open(KM, "w", encoding="utf-8").write(html)
print("Wired Authority Engine link into knowledge map.")
