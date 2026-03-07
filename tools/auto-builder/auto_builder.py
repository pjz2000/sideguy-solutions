import os, re

queue="docs/build-queue/build-queue.txt"
ranked="docs/build-queue/gravity-ranked.txt"
template="seo-template.html"
output="public/problem-pages"

os.makedirs(output,exist_ok=True)

if not os.path.exists(queue):
    print("No build queue")
    exit()

# Load queue (pages to build) and full ranked list (pool for related links)
queue_slugs=[l.strip() for l in open(queue).read().splitlines() if l.strip()]
all_ranked=[l.split("|")[1].strip() for l in open(ranked).read().splitlines() if "|" in l]

# Stop-words to ignore when scoring keyword overlap
STOP={"san","diego","for","to","the","a","an","of","in","is","how","do","i","my",
      "near","me","so","why","what","when","get","be","not","are","with","on","at"}

RELATED_START="<!-- sideguy-related-problems -->"
RELATED_END="<!-- end sideguy-related-problems -->"

def keywords(slug):
    return [w for w in slug.split("-") if len(w)>2 and w not in STOP]

def related_slugs(slug, pool, n=5):
    kw=set(keywords(slug))
    if not kw:
        return pool[:n]
    scored=[]
    for s in pool:
        if s==slug:
            continue
        overlap=len(kw & set(keywords(s)))
        if overlap>0:
            scored.append((overlap,s))
    scored.sort(key=lambda x:-x[0])
    # deduplicate by first token (topic root) to keep variety
    seen=set()
    result=[]
    for _,s in scored:
        root=s.split("-")[0]
        if root not in seen:
            seen.add(root)
            result.append(s)
        if len(result)>=n:
            break
    # fallback: fill from top of pool if not enough
    if len(result)<n:
        for s in pool:
            if s not in result and s!=slug:
                result.append(s)
            if len(result)>=n:
                break
    return result

def build_related_nav(slug, related):
    items=""
    for r in related:
        label=r.replace("-"," ").title()
        items+=f'\n    <li><a href="/{r}.html" style="color:#073044;text-decoration:underline;">{label}</a></li>'
    return (
        f'{RELATED_START}\n'
        f'<nav aria-label="Related Problems" style="'
        f'background:linear-gradient(135deg,rgba(238,252,255,.98) 0%,rgba(210,245,240,.98) 100%);'
        f'border-top:2px solid rgba(33,211,161,.30);padding:20px 22px 18px;'
        f'font-family:-apple-system,system-ui,sans-serif;color:#073044;margin-top:28px;">\n'
        f'  <p style="font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#3f6173;margin:0 0 8px">Related Problems</p>\n'
        f'  <ul style="margin:0;padding:0 0 0 18px;font-size:.9rem;line-height:1.7">{items}\n  </ul>\n'
        f'</nav>\n'
        f'{RELATED_END}'
    )

template_html=open(template).read()

built=0

for slug in queue_slugs:

    file=os.path.join(output,slug+".html")

    if os.path.exists(file):
        continue

    title=slug.replace("-"," ").title()
    html=template_html.replace("{{TITLE}}",title)

    # Inject related pages between the markers
    related=related_slugs(slug, all_ranked)
    nav_block=build_related_nav(slug, related)
    html=re.sub(
        re.escape(RELATED_START)+".*?"+re.escape(RELATED_END),
        nav_block,
        html,
        flags=re.DOTALL
    )

    with open(file,"w") as f:
        f.write(html)

    built+=1

print("Pages built:",built)
