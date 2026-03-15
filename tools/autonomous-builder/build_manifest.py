from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
DOCS = ROOT / "docs" / "autonomous-builder"
MANIFEST = DOCS / "manifests" / "master-manifest.tsv"

topics = [x.strip() for x in (DOCS / "topics.txt").read_text().splitlines() if x.strip()]
mods = [x.strip() for x in (DOCS / "modifiers.txt").read_text().splitlines() if x.strip()]
locs = [x.strip() for x in (DOCS / "locations.txt").read_text().splitlines() if x.strip()]
inds = [x.strip() for x in (DOCS / "industries.txt").read_text().splitlines() if x.strip()]

rows = []
for topic in topics:
    for mod in mods:
        for loc in locs:
            for ind in inds:
                slug = f"{topic}-{mod}-{loc}-{ind}.html"
                title = f"{topic.replace('-',' ').title()} {mod.replace('-',' ').title()} for {ind.replace('-',' ').title()} in {loc.replace('-',' ').title()} | SideGuy"
                h1 = f"{topic.replace('-',' ').title()} {mod.replace('-',' ').title()} for {ind.replace('-',' ').title()} in {loc.replace('-',' ').title()}"
                rows.append((topic, mod, loc, ind, slug, title, h1))

MANIFEST.parent.mkdir(parents=True, exist_ok=True)
with open(MANIFEST, "w", encoding="utf-8") as f:
    f.write("topic\tmodifier\tlocation\tindustry\tslug\ttitle\th1\n")
    for row in rows:
        f.write("\t".join(row) + "\n")

print(f"Wrote {MANIFEST}")
print(f"Total rows: {len(rows)}")
