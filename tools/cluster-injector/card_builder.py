import os

cluster_dir = "docs/cluster-injector"

for file in os.listdir(cluster_dir):
    if not file.endswith("-clusters.txt"):
        continue

    hub = file.replace("-clusters.txt", "")
    pages = open(cluster_dir + "/" + file).read().splitlines()
    cards = []

    for p in pages[:20]:
        cards.append(f'''
<div class="sg-card">
<h3>{p.replace("-", " ").title()}</h3>
<p>SideGuy breakdown of the problem and solutions.</p>
<a href="/{p}.html">Read solution</a>
</div>
''')

    with open(f"docs/cluster-injector/{hub}-cards.html", "w") as f:
        f.write("\n".join(cards))

print("Card HTML generated")
