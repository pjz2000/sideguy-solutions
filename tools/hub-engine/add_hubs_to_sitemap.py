from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
SITEMAP = ROOT / "public" / "sitemap.xml"
HUBS = ROOT / "docs" / "hubs" / "hub_topics.txt"

if not SITEMAP.exists():
    print("No sitemap.xml found")
    raise SystemExit

topics = [x.strip() for x in HUBS.read_text().splitlines() if x.strip()]

urls = []
for topic in topics:
    urls.append(f"<url>\n<loc>https://sideguysolutions.com/hubs/{topic}.html</loc>\n</url>")
    urls.append(f"<url>\n<loc>https://sideguysolutions.com/hubs/{topic}.html</loc>\n</url>")

xml = SITEMAP.read_text()
insert = "\n".join(urls)
xml = xml.replace("</urlset>", insert + "\n</urlset>")
SITEMAP.write_text(xml)

print(f"Added {len(urls)} hub URLs to sitemap")
