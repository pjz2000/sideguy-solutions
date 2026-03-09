from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
gravity_file = ROOT / "docs" / "problem-gravity" / "gravity_pages.txt"
new_file     = ROOT / "docs" / "inventory-intelligence" / "generated" / "gravity_append.txt"

if not gravity_file.exists():
    raise SystemExit(f"Missing gravity file: {gravity_file}")

existing  = set(x.strip() for x in gravity_file.read_text().splitlines() if x.strip())
new_items = [x.strip() for x in new_file.read_text().splitlines() if x.strip()]

added = []

for item in new_items:
    if item not in existing:
        added.append(item)
        existing.add(item)

with gravity_file.open("a") as f:
    for item in added:
        f.write(item + "\n")

print(f"Appended {len(added)} new signals to gravity_pages.txt")
