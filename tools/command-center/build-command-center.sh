#!/bin/bash

REPORT="docs/command-center/system-report.txt"
PAGE="pages/system/command-center.html"

echo "System scan $(date)" > $REPORT

TOTAL=$(find . -name "*.html" | wc -l)
HUBS=$(find pages/hubs -name "*.html" 2>/dev/null | wc -l)
EXPANSION=$(find pages/expansion -name "*.html" 2>/dev/null | wc -l)
MATRIX=$(find pages/matrix -name "*.html" 2>/dev/null | wc -l)
FACTORY=$(find pages/factory -name "*.html" 2>/dev/null | wc -l)

echo "Total pages: $TOTAL" >> $REPORT
echo "Hub pages: $HUBS" >> $REPORT
echo "Expansion pages: $EXPANSION" >> $REPORT
echo "Matrix pages: $MATRIX" >> $REPORT
echo "Factory pages: $FACTORY" >> $REPORT

STAMP=$(date +"%Y-%m-%d %H:%M:%S")

cat > $PAGE <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SideGuy Command Center</title>
<style>
body{font-family:-apple-system,system-ui,Segoe UI,Roboto,sans-serif;background:#eefcff;margin:0;padding:40px 24px;color:#073044;}
h1{color:#0a4a6e;font-size:1.8rem;margin-bottom:4px;}
.ts{font-size:.8rem;color:#3f6173;margin-bottom:2rem;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:2rem;}
.card{background:#fff;padding:20px;border-radius:14px;box-shadow:0 4px 18px rgba(7,48,68,.09);}
.card h2{font-size:.85rem;color:#3f6173;margin:0 0 8px;text-transform:uppercase;letter-spacing:.04em;}
.metric{font-size:2.2rem;font-weight:900;color:#21d3a1;line-height:1;}
.wide{background:#fff;padding:20px;border-radius:14px;box-shadow:0 4px 18px rgba(7,48,68,.09);margin-bottom:16px;}
.wide h2{font-size:1rem;font-weight:800;color:#0a4a6e;margin:0 0 10px;}
.wide p{margin:.4rem 0;font-size:.93rem;}
a{color:#21d3a1;text-decoration:none;font-weight:600;}
</style>
</head>
<body>

<h1>SideGuy Command Center</h1>
<p class="ts">Last scan: $STAMP</p>

<div class="grid">

<div class="card">
<h2>Total Pages</h2>
<div class="metric">$TOTAL</div>
</div>

<div class="card">
<h2>Hub Pages</h2>
<div class="metric">$HUBS</div>
</div>

<div class="card">
<h2>Expansion Pages</h2>
<div class="metric">$EXPANSION</div>
</div>

<div class="card">
<h2>Matrix Pages</h2>
<div class="metric">$MATRIX</div>
</div>

<div class="card">
<h2>Factory Inventory</h2>
<div class="metric">$FACTORY</div>
</div>

</div>

<div class="wide">
<h2>Operator Status</h2>
<p>System infrastructure online.</p>
<p>Problem engine active.</p>
<p>Clarity before cost.</p>
</div>

<div class="wide">
<h2>Tools</h2>
<p>Page Factory → <code>bash tools/factory/page-factory.sh &lt;manifest&gt;</code></p>
<p>Promotion Engine → <code>bash tools/factory/promote-pages.sh</code></p>
<p>Publish Gate → <code>bash tools/intelligence/publish-gate.sh .</code></p>
<p>Authority Gravity → <code>bash tools/gravity/authority-gravity-engine.sh</code></p>
<p>Internet Radar → <code>bash tools/intelligence/internet-radar.sh</code></p>
</div>

<div class="wide">
<h2>Human Help</h2>
<p>Text PJ: <strong>773-544-1231</strong></p>
</div>

</body>
</html>
HTML

echo "Command center built."
echo "Report: $REPORT"
echo "Open:   $PAGE"
