import os
import re
import glob
import datetime
from collections import defaultdict

AUTO_DIR = "public/auto"
HUB_DIR = "public/auto/hubs"
LOG_FILE = "docs/cluster-intelligence/cluster_log.tsv"

CLUSTER_RULES = {
    "payments": [
        "payment", "payments", "merchant", "stripe", "square", "paypal",
        "processing", "processor", "chargeback", "credit-card", "fees"
    ],
    "ai-automation": [
        "ai", "automation", "automate", "gpt", "chatbot", "workflow",
        "agent", "agents"
    ],
    "contractor": [
        "contractor", "contractors", "hvac", "plumber", "plumbing",
        "electrician", "roofing", "landscaping", "solar"
    ],
    "local-business": [
        "restaurant", "restaurants", "small-business", "local-business",
        "service-business", "business"
    ],
    "software": [
        "software", "crm", "erp", "platform", "tool", "tools",
        "scheduling", "dispatch", "billing"
    ]
}

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def slug_to_title(slug):
    return slug.replace(".html", "").replace("-", " ").strip().title()

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def detect_cluster(slug):
    scores = defaultdict(int)
    for cluster, keywords in CLUSTER_RULES.items():
        for kw in keywords:
            if kw in slug:
                scores[cluster] += 1
    if not scores:
        return "general"
    return sorted(scores.items(), key=lambda x: (-x[1], x[0]))[0][0]

def list_pages():
    pages = []
    for path in glob.glob(f"{AUTO_DIR}/*.html"):
        if "/hubs/" in path:
            continue
        slug = os.path.basename(path)
        if slug in ["index.html"]:
            continue
        pages.append({
            "path": path,
            "slug": slug,
            "title": slug_to_title(slug)
        })
    return sorted(pages, key=lambda x: x["slug"])

def group_pages(pages):
    grouped = defaultdict(list)
    for page in pages:
        cluster = detect_cluster(page["slug"])
        page["cluster"] = cluster
        grouped[cluster].append(page)
    return grouped

def build_related_links(page, cluster_pages, max_links=6):
    related = [p for p in cluster_pages if p["slug"] != page["slug"]]
    related = sorted(related, key=lambda x: x["slug"])[:max_links]
    if not related:
        return ""
    links = []
    for item in related:
        links.append(f'<li><a href="/auto/{item["slug"]}">{item["title"]}</a></li>')
    return (
        '\n<section class="sg-related-links" data-sideguy-cluster="true">\n'
        '  <div class="wrap">\n'
        '    <h2>Related SideGuy Guides</h2>\n'
        '    <p>Explore more pages in this problem cluster.</p>\n'
        '    <ul>\n'
        f'      {"".join(links)}\n'
        '    </ul>\n'
        '  </div>\n'
        '</section>\n'
    )

def inject_related_links(page_path, related_html):
    content = read_file(page_path)

    start_marker = '<!-- SIDEGUY_CLUSTER_LINKS_START -->'
    end_marker = '<!-- SIDEGUY_CLUSTER_LINKS_END -->'
    replacement = f'{start_marker}\n{related_html}{end_marker}'

    if start_marker in content and end_marker in content:
        content = re.sub(
            r'<!-- SIDEGUY_CLUSTER_LINKS_START -->.*?<!-- SIDEGUY_CLUSTER_LINKS_END -->',
            replacement,
            content,
            flags=re.S
        )
        write_file(page_path, content)
        return "updated"

    if "</main>" in content:
        content = content.replace("</main>", f"{replacement}\n</main>")
        write_file(page_path, content)
        return "inserted"

    if "</body>" in content:
        content = content.replace("</body>", f"{replacement}\n</body>")
        write_file(page_path, content)
        return "inserted"

    return "skipped"

def create_hub_page(cluster, pages):
    hub_slug = f"{cluster}-hub.html"
    hub_path = os.path.join(HUB_DIR, hub_slug)

    items = []
    for page in sorted(pages, key=lambda x: x["slug"]):
        items.append(f'<li><a href="/auto/{page["slug"]}">{page["title"]}</a></li>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{cluster.replace("-", " ").title()} | SideGuy Cluster Hub</title>
  <meta name="description" content="SideGuy cluster hub for {cluster.replace('-', ' ')} topics — plain-language guides for San Diego operators."/>
  <style>
    body{{font-family:-apple-system,system-ui,sans-serif;max-width:820px;margin:0 auto;padding:32px 20px;color:#073044;background:#eefcff}}
    h1{{font-size:1.6rem;font-weight:800;margin-bottom:8px}}
    ul{{line-height:1.9;padding-left:18px}}
    a{{color:#073044}}
  </style>
</head>
<body>
  <main>
    <section>
      <h1>{cluster.replace("-", " ").title()} Hub</h1>
      <p>SideGuy guides on {cluster.replace("-", " ")} — clarity before cost.</p>
      <ul>
        {''.join(items)}
      </ul>
      <p><a href="/">Back to SideGuy</a> · <a href="/auto/hubs/index.html">All Hubs</a></p>
    </section>
  </main>
</body>
</html>
"""
    write_file(hub_path, html)
    return hub_slug, hub_path

def append_log(line):
    exists = os.path.exists(LOG_FILE)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        if not exists:
            f.write("timestamp\taction\tcluster\tslug\tpath\tstatus\n")
        f.write(line + "\n")

def main():
    pages = list_pages()
    if not pages:
        print("No pages found in public/auto/")
        return

    grouped = group_pages(pages)
    os.makedirs(HUB_DIR, exist_ok=True)

    total_pages = 0
    for cluster, cluster_pages in grouped.items():
        hub_slug, hub_path = create_hub_page(cluster, cluster_pages)
        append_log(f"{now()}\thub_created\t{cluster}\t{hub_slug}\t{hub_path}\tok")

        for page in cluster_pages:
            related_html = build_related_links(page, cluster_pages)
            if related_html:
                related_html += (
                    f'\n<p><a href="/auto/hubs/{hub_slug}">View the full {cluster.replace("-", " ").title()} hub</a></p>\n'
                )
            status = inject_related_links(page["path"], related_html)
            append_log(f"{now()}\tpage_clustered\t{cluster}\t{page['slug']}\t{page['path']}\t{status}")
            total_pages += 1

    print(f"Cluster intelligence complete: {total_pages} pages across {len(grouped)} clusters")

if __name__ == "__main__":
    main()
