import os
from collections import Counter

SKIP_DIRS = {".git", "node_modules", ".sideguy-backups", "_BACKUPS", "backups"}

html_pages = 0
topics = Counter()

for dirpath, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith(".html"):
            continue
        html_pages += 1
        name = f.lower()
        if "ai" in name or "automation" in name:
            topics["ai-automation"] += 1
        if "payment" in name or "merchant" in name or "processor" in name:
            topics["payments"] += 1
        if "lead" in name:
            topics["lead-generation"] += 1
        if "crm" in name or "bookkeeping" in name:
            topics["business-operations"] += 1
        if "hvac" in name or "plumbing" in name or "electrical" in name:
            topics["home-services"] += 1


def count_lines(path):
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8", errors="ignore") as f:
        return sum(1 for line in f if line.strip())


signals  = count_lines("docs/cluster-intelligence/signal_clusters.txt")
clusters = count_lines("docs/cluster-expansion/page-expansion-list.txt")
gravity  = count_lines("docs/problem-gravity/gravity_pages.txt")
radar    = count_lines("docs/problem-radar/radar-signals.tsv") - 1  # minus header
problems = count_lines("docs/problem-engine/problem-signals.txt")
queue    = count_lines("docs/build-orchestrator/build_log.txt")

print("\nSIDEGUY SIGNAL COMMAND CENTER")
print("=" * 40)
print(f"  HTML pages total:      {html_pages:,}")
print(f"  Radar signals (v2):    {max(radar, 0):,}")
print(f"  Problem signals:       {problems:,}")
print(f"  Signal clusters:       {signals:,}")
print(f"  Expansion clusters:    {clusters:,}")
print(f"  Gravity signals:       {gravity:,}")
print(f"  Build cycles logged:   {queue:,}")

print("\n  Top topics (by filename keywords):")
for t, c in topics.most_common(5):
    bar = "█" * min(c // 500, 30)
    print(f"    {t:<25} {c:>6,}  {bar}")

# Quick subsystem status
print("\n  Subsystem files:")
checks = [
    ("Radar V2",        "tools/problem-radar-v2/radar_v2.py"),
    ("Traffic Engine",  "tools/traffic-engine/traffic_engine.py"),
    ("Network Engine",  "tools/network-engine/network_engine.py"),
    ("Trend Engine",    "tools/trend-engine/trend_engine.py"),
    ("Surface Engine",  "tools/surface-engine/surface_engine.py"),
    ("Build Orch.",     "tools/build-orchestrator/build_orchestrator.py"),
    ("Problem Heatmap", "tools/problem-heatmap/problem_heatmap.py"),
    ("Meme Factory",    "tools/meme-factory/meme_post_generator.py"),
]
for name, path in checks:
    tag = "✓" if os.path.exists(path) else "·"
    print(f"    {tag} {name}")

print("\nCommand Center ready\n")
