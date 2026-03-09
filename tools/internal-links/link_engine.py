import os
from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions/public")

keywords = [
    "ai automation",
    "ai chatbot",
    "ai scheduling automation",
    "ai crm automation",
    "ai invoice automation",
    "ai lead qualification",
    "ai email automation"
]

pages = list(ROOT.rglob("*.html"))

for page in pages:

    text = page.read_text()

    for keyword in keywords:

        link = f'<a href="/search?q={keyword.replace(" ","-")}">{keyword}</a>'

        if keyword in text and link not in text:
            text = text.replace(keyword, link, 1)

    page.write_text(text)

print("Internal links inserted")
