"""
Build Report — writes signals/build-report-YYYY-MM-DD.json after each run.
"""
import os, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

pages   = len([f for f in os.listdir(".") if f.endswith(".html")])
hubs    = len(os.listdir("hubs"))    if os.path.isdir("hubs")    else 0
pillars = len(os.listdir("pillars")) if os.path.isdir("pillars") else 0

try:
    with open("seo-reserve/manifest.json") as f:
        manifest_size = len(json.load(f).get("topics", []))
except Exception:
    manifest_size = 0

report = {
    "timestamp":     datetime.datetime.now(datetime.UTC).isoformat(),
    "pages":         pages,
    "hubs":          hubs,
    "pillars":       pillars,
    "manifest_size": manifest_size,
}

os.makedirs("signals", exist_ok=True)
outfile = f"signals/build-report-{datetime.date.today()}.json"
with open(outfile, "w") as f:
    json.dump(report, f, indent=2)

print(f"Build report → {outfile}")
print(f"  pages={pages}  hubs={hubs}  pillars={pillars}  manifest={manifest_size}")
