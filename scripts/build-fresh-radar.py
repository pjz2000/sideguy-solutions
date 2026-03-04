import csv
import os
import datetime

INPUT      = "radar/problem-radar-new.csv"
OUTPUT     = "fresh/radar.html"
PHONE      = "773-544-1231"
PHONE_HREF = "+17735441231"


def page_exists(slug):
    dirs = ["problems", "auto", "concepts", "generated", "longtail"]
    for d in dirs:
        if os.path.exists(f"{d}/{slug}.html"):
            return True
    return False


rows = []
if os.path.exists(INPUT):
    with open(INPUT) as f:
        reader = csv.DictReader(f)
        for r in reader:
            slug   = r["slug"]
            exists = page_exists(slug)
            rows.append({
                "title":  r["title"],
                "slug":   slug,
                "score":  r["score"],
                "exists": exists,
            })

rows.sort(key=lambda r: float(r["score"]), reverse=True)
top = rows[:100]

today = datetime.date.today().isoformat()

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>SideGuy Fresh Radar · SideGuy Solutions</title>
<meta name="description" content="Latest discovered operator problems and page build candidates from live signals.">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{{--ink:#073044;--muted:#3f6173;--line:#cce8f0;--bg0:#eefcff;--accent:#1f7cff;}}
body{{font-family:-apple-system,system-ui,sans-serif;max-width:1000px;margin:auto;padding:40px 20px;background:var(--bg0);color:var(--ink);line-height:1.6;}}
a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
table{{width:100%;border-collapse:collapse;margin-top:16px;}}
td,th{{border-bottom:1px solid var(--line);padding:10px;text-align:left;}}
th{{font-size:13px;color:var(--muted);}}
.yes{{color:#059669;font-weight:700;}}
.no{{color:#dc2626;font-weight:700;}}
.small{{font-size:13px;color:var(--muted);}}
.floatBtn{{position:fixed;right:16px;bottom:16px;z-index:9999;background:#073044;color:#fff;border-radius:999px;padding:14px 18px;font-weight:700;text-decoration:none;font-size:14px;box-shadow:0 8px 24px rgba(7,48,68,.25);}}
</style>
</head>
<body>
<a href="/">← SideGuy Home</a> &nbsp;•&nbsp; <a href="/fresh/index.html">Fresh</a> &nbsp;•&nbsp; <a href="/fresh/gravity.html">Gravity</a>
<h1>SideGuy Problem Radar</h1>
<p class="small">Latest discovered operator problems and page build candidates (top 100 by signal score). Last updated: {today}</p>
<table>
<tr><th>Problem</th><th>Score</th><th>Page Exists</th></tr>
"""

for r in top:
    if r["exists"]:
        status_cls  = "yes"
        status_text = "YES"
    else:
        status_cls  = "no"
        status_text = "NO"
    html += f"<tr><td>{r['title']}</td><td>{r['score']}</td><td class=\"{status_cls}\">{status_text}</td></tr>\n"

html += f"""</table>
<br>
<a class="floatBtn" href="sms:{PHONE_HREF}">Text PJ &nbsp;·&nbsp; {PHONE}</a>
</body>
</html>
"""

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, "w") as f:
    f.write(html)

print(f"Fresh Radar created → {OUTPUT}  ({len(top)} rows)")
