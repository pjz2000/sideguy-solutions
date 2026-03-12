import os
import sys

PLAN="docs/cluster-plans/cluster_outline.json"

if len(sys.argv) < 2:
    print("Usage: python3 build_page.py <page-slug>")
    sys.exit()

slug=sys.argv[1]
title=slug.replace("-"," ").title()

path=f"public/{slug}.html"

if os.path.exists(path):
    print("Page already exists:",path)
    sys.exit()

template=f"""
<!DOCTYPE html>
<html>
<head>
<title>{title} | SideGuy</title>
<meta charset="UTF-8">
<meta name="description" content="Guide explaining {title.lower()} for businesses and operators.">
</head>

<body>

<h1>{title}</h1>

<p>
SideGuy explains {title.lower()} so business owners can make better decisions
without wasting time or money.
</p>

<h2>What This Means</h2>

<p>
Understanding {title.lower()} helps operators evaluate tools,
costs, and workflows before committing to new systems.
</p>

<h2>Why Businesses Care</h2>

<ul>
<li>reduce operational friction</li>
<li>improve response time</li>
<li>avoid unnecessary costs</li>
</ul>

<section class="sideguy-help">

<h2>Need help figuring this out?</h2>

<p>Text PJ directly for real-world guidance.</p>

<a href="sms:+17735441231">Text PJ</a>

</section>

</body>
</html>
"""

os.makedirs("public",exist_ok=True)

with open(path,"w",encoding="utf-8") as f:
    f.write(template)

print("Created stub:",path)
print("NOTE: This is a stub. Add real, specific content before publishing.")
