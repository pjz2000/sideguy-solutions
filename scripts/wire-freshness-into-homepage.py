import os, re

HOME = "index.html"
if not os.path.exists(HOME):
    print("No index.html found. Skipping.")
    raise SystemExit(0)

html   = open(HOME, "r", encoding="utf-8", errors="ignore").read()
marker = "<!-- FRESHNESS_ENGINE_CARD -->"

if marker in html:
    print("Already wired.")
    raise SystemExit(0)

card = (
    f"\n{marker}\n"
    '<a href="/fresh/index.html" style="text-decoration:none;">'
    '<div style="border:1px solid #cce8f0;border-radius:16px;padding:14px;background:#ffffff;">'
    '<div style="font-weight:800;">Freshness Hub</div>'
    '<div style="opacity:.75;margin-top:4px;">Recently updated pages + trending internal guides →</div>'
    "</div></a>\n"
)

inserted = False

if "<main" in html and "</main>" in html:
    m = re.search(r"<main[^>]*>", html)
    if m:
        i    = m.end()
        html = html[:i] + "\n" + card + "\n" + html[i:]
        inserted = True

if not inserted and "</h1>" in html:
    html     = html.replace("</h1>", "</h1>\n" + card, 1)
    inserted = True

if inserted:
    open(HOME, "w", encoding="utf-8").write(html)
    print("Wired Freshness Hub card into homepage.")
else:
    print("No safe insertion point found. Skipping.")
