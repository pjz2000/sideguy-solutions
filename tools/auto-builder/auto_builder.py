import os, subprocess

queue="docs/build-queue/build-queue.txt"
template="seo-template.html"
output="public/problem-pages"

os.makedirs(output,exist_ok=True)

if not os.path.exists(queue):
    print("Queue missing")
    exit()

slugs=open(queue).read().splitlines()

template_html=open(template).read()

built=0

for slug in slugs:

    file=os.path.join(output,slug+".html")

    if os.path.exists(file):
        continue

    title=slug.replace("-"," ").title()

    html=template_html.replace("{{TITLE}}",title)

    with open(file,"w") as f:
        f.write(html)

    built+=1

print("Pages built:",built)

# Run CTR optimizer on all pages whenever new ones are built
if built > 0:
    subprocess.run("python3 tools/auto-builder/ctr_optimizer.py", shell=True)

