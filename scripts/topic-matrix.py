"""
SideGuy Topic Matrix
Cross-products signal topics × industries × cities
to generate expanded topic seeds → signals/expanded-topics.txt

Reads:
  signals/signal-topics.txt   (from signal-harvester + signal-connector)
  signals/industries.txt      (curated industry list)
  signals/cities.txt          (target cities)

Outputs:
  signals/expanded-topics.txt (deduped, sorted)
"""
import itertools, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def read_lines(path):
    try:
        with open(path) as f:
            return [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        return []

signals    = read_lines("signals/signal-topics.txt")
industries = read_lines("signals/industries.txt")
cities     = read_lines("signals/cities.txt")

if not signals:
    print("No signal topics found — run signal-harvester.py first.")
    raise SystemExit(0)

expanded = set()

for sig in signals:
    # signal for industry  (e.g. "ai tools for restaurants for hvac")
    # — skip signals that already end in "for <industry>" to avoid redundancy
    for ind in industries:
        expanded.add(f"{sig} for {ind}")

    # signal for industry in city
    for ind, city in itertools.product(industries, cities):
        expanded.add(f"{sig} for {ind} in {city}")

# Also plain industry × city seeds (no signal prefix)
for ind, city in itertools.product(industries, cities):
    expanded.add(f"ai automation for {ind} in {city}")

result = sorted(expanded)
with open("signals/expanded-topics.txt", "w") as f:
    for t in result:
        f.write(t + "\n")

print(f"Generated {len(result)} expanded topics → signals/expanded-topics.txt")
print(f"  signals={len(signals)}  industries={len(industries)}  cities={len(cities)}")
