import os
import re
import datetime

MANIFEST="docs/learning-loop/next-build-manifest.md"
OUTPUT="auto/learning-pages"
SITEMAP="public/sitemaps/learning-pages.xml"
LOG="docs/learning-builder/build-log.md"

BASE_URL="https://www.sideguysolutions.com"

def slugify(text):
    text=text.lower()
    text=re.sub(r'[^a-z0-9\s-]','',text)
    text=re.sub(r'\s+','-',text)
    return text.strip("-")

def parse_manifest():

    topics=[]

    if not os.path.exists(MANIFEST):
        return topics

    in_section=False

    with open(MANIFEST) as f:

        for line in f:

            stripped=line.strip()

            # Enter the recommended pages section
            if stripped.lower().startswith("## recommended"):
                in_section=True
                continue

            # Stop at any new ## section
            if stripped.startswith("##") and in_section:
                in_section=False
                continue

            if not in_section:
                continue

            if not stripped.startswith("-"):
                continue

            topic=stripped.split("|")[0].lstrip("-").strip()

            if topic:
                topics.append(topic)

    return topics

def build_page(topic):

    slug=slugify(topic)

    if not slug:
        return None

    path=f"{OUTPUT}/{slug}.html"

    if os.path.exists(path):
        return None

    html=f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{topic} | SideGuy</title>
<meta name="description" content="SideGuy explains {topic} clearly before you spend money."/>
<style>
  body{{font-family:-apple-system,system-ui,sans-serif;max-width:760px;margin:0 auto;padding:32px 20px;color:#073044;background:#eefcff}}
  h1{{font-size:1.8rem;margin-bottom:16px}}
  p{{line-height:1.7;margin-bottom:14px;color:#3f6173}}
  .cta{{margin-top:32px;padding:20px;background:#21d3a1;border-radius:12px;text-align:center}}
  .cta a{{color:#fff;font-weight:700;font-size:1.1rem;text-decoration:none}}
</style>
</head>
<body>
<h1>{topic}</h1>
<p>
Searching for <strong>{topic}</strong> usually means something is unclear,
expensive, broken, or confusing.
</p>
<p>
SideGuy explains the problem clearly so you can decide what to do next.
</p>
<p>
Google discovers the problem. AI explains it. A real human resolves it.
</p>
<div class="cta">
  <a href="sms:+17735441231">Text PJ if you want help &rarr;</a>
</div>
</body>
</html>
"""

    with open(path,"w") as f:
        f.write(html)

    return slug

def update_sitemap(slugs):

    today=datetime.date.today().isoformat()

    xml='<?xml version="1.0" encoding="UTF-8"?>\n'
    xml+='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for slug in slugs:

        url=f"{BASE_URL}/auto/learning-pages/{slug}.html"

        xml+=f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n"

    xml+='</urlset>'

    with open(SITEMAP,"w") as f:
        f.write(xml)

def log_build(slugs):

    now=datetime.datetime.now(datetime.timezone.utc).isoformat()

    out=f"# Learning Builder Log\n\nRun: {now}\n\n"

    if slugs:
        for s in slugs:
            out+=f"- built {s}\n"
    else:
        out+="_No pages built — manifest has no topics yet. Add GSC data to trigger learning loop._\n"

    with open(LOG,"w") as f:
        f.write(out)

def run():

    os.makedirs(OUTPUT,exist_ok=True)

    topics=parse_manifest()

    built=[]

    for t in topics[:30]:

        slug=build_page(t)

        if slug:
            built.append(slug)

    update_sitemap(built)

    log_build(built)

    print(f"Learning build complete. Topics found: {len(topics)}, Pages built: {len(built)}")

run()
