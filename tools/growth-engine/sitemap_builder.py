import os

base = "https://sideguysolutions.com/"

pages = []

for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".html"):
            slug = f.replace(".html", "")
            pages.append(slug)

xml = []

xml.append('<?xml version="1.0" encoding="UTF-8"?>')
xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for p in pages:
    xml.append("<url>")
    xml.append(f"<loc>{base}{p}.html</loc>")
    xml.append("</url>")

xml.append("</urlset>")

with open("sitemap.xml","w") as f:
    f.write("\n".join(xml))

print("Sitemap generated for",len(pages),"pages")
