#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit

echo "=================================="
echo "SideGuy Exit Ramp Spawner (20%)"
echo "=================================="

SCRIPT="_run_exit_ramps_20pct.py"

cat > "$SCRIPT" <<'PY'
import glob, os, re, random

SEED_PAGES = []
for f in glob.glob("*.html"):
    low = f.lower()
    if any(x in low for x in [
        "san-diego", "payment", "hvac", "mini-split",
        "repair", "replace", "cost", "vs", "calculator"
    ]):
        SEED_PAGES.append(f)

SEED_PAGES = sorted(SEED_PAGES)[:100]

created = 0
MAX_PAGES = 100  # 20% limit

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://sideguysolutions.com/{slug}.html">
<meta name="robots" content="index,follow,max-image-preview:large">
<style>
:root {{
  --bg0:#eefcff;
  --ink:#073044;
  --mint:#21d3a1;
  --phone:"+17735441231";
}}
body {{
  margin:0;
  padding:0;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,sans-serif;
  background:radial-gradient(circle at 50% 0%, #d4f1ff 0%, #eefcff 50%, #fff 100%);
  color:var(--ink);
  line-height:1.6;
}}
header {{
  text-align:center;
  padding:2rem 1rem;
}}
h1 {{
  font-size:2rem;
  margin:0 0 1rem 0;
}}
main {{
  max-width:800px;
  margin:0 auto;
  padding:1rem;
}}
.card {{
  background:#fff;
  border-radius:8px;
  padding:1.5rem;
  margin:1rem 0;
  box-shadow:0 2px 8px rgba(7,48,68,0.1);
}}
a {{
  color:var(--mint);
  text-decoration:none;
}}
a:hover {{
  text-decoration:underline;
}}
</style>
</head>
<body>
<header>
<h1>{title}</h1>
</header>
<main>
<div class="card">
<p>{body}</p>
</div>
<div class="card">
<h2>Need direct help?</h2>
<p><strong>Text PJ: <a href="sms:+17735441231">773-544-1231</a></strong></p>
<p>Send your situation. Get clarity.</p>
</div>
</main>
</body>
</html>
"""

candidates = []
for seed in SEED_PAGES:
    base = os.path.splitext(os.path.basename(seed))[0]
    for suffix in ["cost", "comparison", "near-me", "urgent", "decision"]:
        slug = f"{{base}}-{{suffix}}"
        fn = f"{{slug}}.html"
        if not os.path.exists(fn):
            candidates.append((slug, fn))

# Shuffle and take only first MAX_PAGES
random.seed(42)
random.shuffle(candidates)
candidates = candidates[:MAX_PAGES]

for slug, fn in candidates:
    html = TEMPLATE.format(
        title=slug.replace("-", " ").title(),
        desc=f"Decision support for {{slug.replace('-', ' ')}} in San Diego.",
        slug=slug,
        body="Compare next best options, understand urgency, and escalate to a real human fast."
    )
    
    with open(fn, "w", encoding="utf-8") as f:
        f.write(html)
    created += 1

print(f"Created {{created}} exit ramp pages (20% sample)")
PY

python3 "$SCRIPT"

if [ $? -eq 0 ]; then
  git add .
  git commit -m "Exit Ramp Spawner: 20% sample (~100 pages)"
  git push origin main
  echo ""
  echo "✅ DONE: 20% exit ramps created & committed"
else
  echo "❌ Script failed"
  exit 1
fi
