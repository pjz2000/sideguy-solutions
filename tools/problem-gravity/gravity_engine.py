import os
import datetime

TEMPLATE="seo-template.html"
OUTPUT_DIR="public/auto"
SIGNAL_FILE="signals/problem_signals.txt"
LOG="docs/problem-gravity/gravity_log.tsv"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG), exist_ok=True)

def slugify(text):
    import re
    text=text.lower()
    text=re.sub(r'[^a-z0-9\s-]','',text)
    return re.sub(r'\s+','-',text).strip('-')

def create_page(topic):

    slug=slugify(topic)
    filename=f"{OUTPUT_DIR}/{slug}.html"

    if os.path.exists(filename):
        return

    with open(TEMPLATE,"r") as f:
        template=f.read()

    page=template.replace("{{TITLE}}",topic.title())
    page=page.replace("{{H1}}",topic.title())
    page=page.replace("{{DESCRIPTION}}",f"SideGuy explanation and human help for: {topic}")

    with open(filename,"w") as f:
        f.write(page)

    with open(LOG,"a") as log:
        log.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()}\t{topic}\t{slug}\n")

    return slug

def run():

    if not os.path.exists(SIGNAL_FILE):
        print(f"Signal file not found: {SIGNAL_FILE}")
        return

    with open(SIGNAL_FILE,"r") as f:
        topics=[x.strip() for x in f.readlines() if x.strip()]

    built=0
    for t in topics:
        result=create_page(t)
        if result:
            built+=1

    print(f"Gravity engine complete: {built} pages built from {len(topics)} signals")

run()
