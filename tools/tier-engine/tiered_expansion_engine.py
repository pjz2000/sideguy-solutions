"""
Tiered Expansion Engine
Classifies web-accessible HTML pages into 4 tiers by URL depth,
outputs a tier map for site architecture review.
"""
import os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "site-structure" / "tier_map.md"

SKIP_DIRS = {
    ".git", "node_modules", "public", "docs", "seo-reserve",
    "signals", "data", "tools", "scripts", "backups",
    "_BACKUPS", ".sideguy-backups", "reports", "reasoning", "routing",
}

TIER_LABELS = {
    1: "Tier 1 — Authority Hub",
    2: "Tier 2 — Cluster Pages",
    3: "Tier 3 — Long Tail Pages",
    4: "Tier 4 — Experimental Pages",
}

tiers = defaultdict(list)

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith(".html"):
            continue
        path = Path(dirpath) / f
        rel = path.relative_to(ROOT)
        depth = len(rel.parts)  # 1 = root file, 2 = one subdir, etc.
        tier_num = min(depth, 4)
        tiers[TIER_LABELS[tier_num]].append(str(rel))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT, "w") as f:
    f.write("# SideGuy Tier Map\n\n")
    total = sum(len(v) for v in tiers.values())
    f.write(f"Total pages: {total}\n\n")
    for label in TIER_LABELS.values():
        pages = tiers.get(label, [])
        f.write(f"## {label}\n")
        f.write(f"Pages: {len(pages)}\n\n")
        for p in pages[:10]:
            f.write(f"- {p}\n")
        f.write("\n")

print("Tiered site structure generated")
for label in TIER_LABELS.values():
    print(f"  {label}: {len(tiers.get(label, []))}")
print(f"Report: {OUTPUT.relative_to(ROOT)}")
