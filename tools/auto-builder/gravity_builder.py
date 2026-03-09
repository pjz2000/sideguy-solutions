import os

signal_file = "docs/problem-gravity/gravity_pages.txt"
template_file = "seo-template.html"
output_dir = "public/auto"

if not os.path.exists(signal_file):
    print("No gravity signals found")
    exit()

if not os.path.exists(template_file):
    print("Template missing")
    exit()

os.makedirs(output_dir, exist_ok=True)

signals = open(signal_file).read().splitlines()
template = open(template_file).read()

built = 0

for slug in signals[:250]:
    slug = slug.strip()
    if not slug:
        continue

    title = slug.replace("-", " ").title()

    html = template.replace("{{TITLE}}", title)
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{QUERY}}", title)

    out_file = os.path.join(output_dir, slug + ".html")

    if os.path.exists(out_file):
        continue

    with open(out_file, "w") as f:
        f.write(html)

    built += 1

print("Auto builder created", built, "pages")
print("Output directory:", output_dir)
