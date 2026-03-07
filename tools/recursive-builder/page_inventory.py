import os

pages = []

for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".html"):
            pages.append(f.replace(".html", ""))

with open("docs/recursive-builder/site-pages.txt", "w") as f:
    for p in sorted(pages):
        f.write(p + "\n")

print("Pages found:", len(pages))
