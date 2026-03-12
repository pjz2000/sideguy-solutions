"""
internal_link_injector.py
--------------------------
DO NOT RUN on the root HTML directory or on pages with real content
without first reviewing the authority_links.md route map.

Random injection creates non-contextual links that hurt more than they help.
Use this only after auditing authority_router.py output and confirming
each link placement is topically relevant to the page it appears on.

Designed to operate on public/ (generated/stub pages), not the root site.
"""
import os
import random

ROOT="public"

targets=[
("San Diego Mobile Business Payments","/san-diego-mobile-business-payments.html"),
("Mobile Operator Payments","/mobile-operator-payments-san-diego.html"),
("AI Lead Generation Systems","/ai-lead-generation-systems-san-diego.html"),
("Tech Help Hub","/tech-help-hub-san-diego.html"),
("Software Development Hub","/software-development-hub-san-diego.html")
]

count=0

for root,dirs,files in os.walk(ROOT):

    if ".git" in root:
        continue

    for f in files:

        if not f.endswith(".html"):
            continue

        path=os.path.join(root,f)

        try:

            html=open(path,encoding="utf-8").read()

            if "sideguy-router" in html:
                continue

            if random.random()<0.02:

                title,link=random.choice(targets)

                block=f"""

<!-- sideguy-router -->
<p class="sideguy-router">
Related guide: <a href="{link}">{title}</a>
</p>
"""

                html=html.replace("</body>",block+"\n</body>")

                with open(path,"w",encoding="utf-8") as fh:
                    fh.write(html)

                count+=1

        except:
            pass

print("Router links injected:",count)
