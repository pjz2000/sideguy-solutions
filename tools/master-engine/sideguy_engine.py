import subprocess
import datetime
import os
import sys

print("\nSIDEGUY MASTER ENGINE")
print("---------------------")
print("Run time:", datetime.datetime.now(datetime.timezone.utc).isoformat())

steps = [
    ("Trend Radar",              "tools/trend-radar/trend_fetcher.py"),
    ("Trend Cluster Builder",    "tools/trend-radar/trend_cluster_builder.py"),

    ("Internet Problem Scanner", "tools/problem-scanner/discussion_scanner.py"),
    ("Problem Detector",         "tools/problem-scanner/problem_detector.py"),
    ("Problem Clusters",         "tools/problem-scanner/problem_clusters.py"),

    ("Problem Engine Collector", "tools/problem-engine/problem_collector.py"),
    ("Problem Keyword Map",      "tools/problem-engine/problem_extractor.py"),
    ("Problem Page Ideas",       "tools/problem-engine/problem_page_builder.py"),

    ("Problem Heatmap",          "tools/problem-heatmap/problem_heatmap.py"),
    ("Idea Board",               "tools/idea-board/idea_board.py"),
    ("Page Factory",             "tools/page-factory/page_factory.py"),
    ("Auto Linker",              "tools/auto-linker/auto_linker.py"),
]

results = []
for name, script in steps:
    if not os.path.exists(script):
        print(f"\n[SKIP] {name} — script not found: {script}")
        results.append((name, "skipped"))
        continue

    print(f"\n[RUN]  {name}")
    sys.stdout.flush()
    try:
        proc = subprocess.run(
            ["python3", script],
            timeout=120,
            stdin=subprocess.DEVNULL,
        )
        status = "ok" if proc.returncode == 0 else f"exit {proc.returncode}"
        results.append((name, status))
        print(f"       → {status}")
    except subprocess.TimeoutExpired:
        print(f"       → TIMEOUT (120s)")
        results.append((name, "timeout"))
    except Exception as e:
        print(f"       → ERROR: {e}")
        results.append((name, f"error: {e}"))

print("\n--- SUMMARY ---")
for name, status in results:
    tag = "✓" if status == "ok" else "·"
    print(f"  {tag} {name:<30} {status}")

print("\nSideGuy Engine complete.")
print("Report saved to: docs/master-engine/engine-report.txt")
