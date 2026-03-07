"""
problem_gravity_engine.py
--------------------------
Generates page slugs from the cartesian product of:
  signals × industries × locations

Slug order matches site conventions: {signal}-{industry}-{location}
e.g. payment-processing-fees-too-high-hvac-san-diego

Output: docs/problem-gravity/gravity_pages.txt
"""
import os
import datetime

source_file = "docs/problem-gravity/gravity_sources.txt"

if not os.path.exists(source_file):
    print("No gravity sources found at:", source_file)
    exit(1)

signals = [s.strip() for s in open(source_file).read().splitlines() if s.strip()]

industries = [
    "hvac",
    "restaurants",
    "plumbing",
    "agencies",
    "contractors",
    "real-estate",
    "retail",
    "salons",
    "dental",
    "landscaping",
    "electricians",
    "auto-repair",
    "roofing",
    "construction",
    "property-management",
]

locations = [
    "san-diego",
    "north-county",
    "california",
]

out_dir = "docs/problem-gravity"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "gravity_pages.txt")

pages = []
seen = set()

for signal in signals:
    base = signal.replace(" ", "-")
    for industry in industries:
        for location in locations:
            # Convention: signal-industry-location (matches existing site pattern)
            slug = f"{base}-{industry}-{location}"
            if slug not in seen:
                seen.add(slug)
                pages.append(slug)

with open(out_file, "w") as f:
    for p in pages:
        f.write(p + "\n")

print("\nProblem Gravity Engine")
print("=" * 40)
print(f"  Signals:          {len(signals)}")
print(f"  Industries:       {len(industries)}")
print(f"  Locations:        {len(locations)}")
print(f"  Generated pages:  {len(pages)}")
print(f"  Output:           {out_file}")
print(f"  Timestamp:        {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
print()

# Show sample
print("Sample slugs:")
for p in pages[:6]:
    print(f"  {p}")
print(f"  ... ({len(pages) - 6} more)")
