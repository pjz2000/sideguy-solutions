import os
import glob
import datetime

HUB_DIR="public/auto/hubs"
MASTER_HUB="public/auto/hubs/index.html"
LOG="docs/hub-router/hub_router_log.tsv"

os.makedirs(HUB_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG), exist_ok=True)

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def read_file(path):
    with open(path,"r") as f:
        return f.read()

def write_file(path,content):
    with open(path,"w") as f:
        f.write(content)

def list_hubs():
    hubs=[]
    for f in glob.glob(f"{HUB_DIR}/*.html"):
        if "index.html" in f:
            continue
        slug=os.path.basename(f)
        title=slug.replace("-hub.html","").replace("-"," ").title()
        hubs.append((slug,title))
    return sorted(hubs)

def build_master_index(hubs):

    items=[]
    for slug,title in hubs:
        items.append(f'<li><a href="/auto/hubs/{slug}">{title} Hub</a></li>')

    html=f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>SideGuy Authority Hubs</title>
<meta name="description" content="SideGuy topical authority hubs — problem cluster guides for San Diego operators."/>
<style>
  body{{font-family:-apple-system,system-ui,sans-serif;max-width:820px;margin:0 auto;padding:32px 20px;color:#073044;background:#eefcff}}
  h1{{font-size:1.6rem;font-weight:800;margin-bottom:8px}}
  ul{{line-height:1.9;padding-left:18px}}
  a{{color:#073044}}
</style>
</head>
<body>
<h1>SideGuy Authority Hubs</h1>
<p>These hubs organize SideGuy problem clusters.</p>
<ul>
{''.join(items)}
</ul>
<p><a href="/">Return to SideGuy</a></p>
</body>
</html>
"""

    write_file(MASTER_HUB,html)

def crosslink_hubs(hubs):

    for slug,title in hubs:

        path=f"{HUB_DIR}/{slug}"
        html=read_file(path)

        links=[]
        for s,t in hubs:
            if s!=slug:
                links.append(f'<li><a href="/auto/hubs/{s}">{t} Hub</a></li>')

        block=f"""
<!-- SIDEGUY_HUB_ROUTER_START -->
<nav aria-label="Other SideGuy Hubs" style="margin-top:32px;padding-top:16px;border-top:1px solid rgba(7,48,68,.1)">
<h2>Explore Other SideGuy Hubs</h2>
<ul>
{''.join(links)}
</ul>
<p><a href="/auto/hubs/index.html">View All Hubs</a></p>
</nav>
<!-- SIDEGUY_HUB_ROUTER_END -->
"""

        if "SIDEGUY_HUB_ROUTER_START" not in html:
            html=html.replace("</body>",block+"\n</body>")
            write_file(path,html)

        with open(LOG,"a") as log:
            log.write(f"{now()}\thub_routed\t{slug}\n")

def run():

    hubs=list_hubs()

    if not hubs:
        print("No hubs found — run cluster_intelligence.py first")
        return

    build_master_index(hubs)
    crosslink_hubs(hubs)

    print(f"Hub router complete: {len(hubs)} hubs cross-linked, master index written")

run()
