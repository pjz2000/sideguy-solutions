import os

KM = "knowledge/sideguy-knowledge-map.html"
if not os.path.exists(KM):
    print("No knowledge map found. Skipping.")
    raise SystemExit(0)

html   = open(KM, "r", encoding="utf-8", errors="ignore").read()
marker = "<!-- FRESHNESS_ENGINE_LINK -->"

if marker in html:
    print("Already wired.")
    raise SystemExit(0)

ins = (
    f"\n{marker}\n"
    '<div class="nodeCard">'
    '<div class="nodeTitle">Freshness Hub</div>'
    '<div class="nodeMeta">Recently updated + trending pages (crawl accelerator)</div>'
    '<a class="nodeLink" href="/fresh/index.html">Open Freshness Hub</a>'
    "</div>\n"
)

if "</h1>" in html:
    html = html.replace("</h1>", "</h1>" + ins, 1)
    open(KM, "w", encoding="utf-8").write(html)
    print("Wired Freshness Hub into knowledge map.")
else:
    print("No header marker found. Skipping.")
