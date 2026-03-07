import subprocess
import os
from datetime import datetime, timezone

print("\nSIDEGUY BUILD ORCHESTRATOR\n")


def run(name, script):
    if not os.path.exists(script):
        print(f"  [skip] {name} — not found: {script}")
        return False
    print(f"\n  [run]  {name}")
    result = subprocess.run(["python3", script], stdin=subprocess.DEVNULL)
    status = "ok" if result.returncode == 0 else f"exit {result.returncode}"
    print(f"         → {status}")
    return result.returncode == 0


steps = [
    ("Radar V2",           "tools/problem-radar-v2/radar_v2.py"),
    ("Traffic Engine",     "tools/traffic-engine/traffic_engine.py"),
    ("Gravity Ranker",     "tools/gravity-ranking/gravity_ranker.py"),
    ("Build Queue",        "tools/gravity-ranking/build_queue.py"),
    ("Auto Builder",       "tools/auto-builder/run_builder.py"),
    ("Network Engine",     "tools/network-engine/network_engine.py"),
    ("Authority Surface",  "tools/authority-surface/authority_surface.py"),
    ("Trend Engine",       "tools/trend-engine/trend_engine.py"),
    ("Surface Engine",     "tools/surface-engine/surface_engine.py"),
]

results = [(name, run(name, script)) for name, script in steps]

print("\n--- BUILD SUMMARY ---")
for name, ok in results:
    tag = "✓" if ok else "·"
    print(f"  {tag} {name}")

now = datetime.now(timezone.utc).isoformat()
os.makedirs("docs/build-orchestrator", exist_ok=True)
with open("docs/build-orchestrator/build_log.txt", "a") as f:
    ok_count = sum(1 for _, ok in results if ok)
    f.write(f"{now}  build cycle completed  ({ok_count}/{len(results)} steps ran)\n")

print(f"\nBuild cycle complete — {now}")
