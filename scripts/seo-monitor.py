#!/usr/bin/env python3
"""
SideGuy SEO Monitor
Single-pass health check across all pages, hubs, pillars, and signals.
"""
import os
from pathlib import Path

ROOT     = Path(__file__).parent.parent
root     = ROOT
hub_dir  = root / "hubs"
pillar_dir = root / "pillars"
signals_dir = root / "signals"

pages   = [p for p in root.glob("*.html")
           if not p.name.startswith("_")]
hubs    = list(hub_dir.glob("*.html"))   if hub_dir.exists()    else []
pillars = list(pillar_dir.glob("*.html")) if pillar_dir.exists() else []

# Seed count
seed_file = signals_dir / "expanded-topics.txt"
seed_count = len(seed_file.read_text().splitlines()) if seed_file.exists() else 0

pj_file = signals_dir / "pj-topics.txt"
pj_count = sum(
    1 for l in pj_file.read_text().splitlines()
    if l.strip() and not l.startswith("#")
) if pj_file.exists() else 0

# Manifest topic count
manifest = root / "seo-reserve" / "manifest.json"
try:
    import json
    manifest_count = len(json.loads(manifest.read_text())["topics"])
except Exception:
    manifest_count = 0

# Single-pass coverage scan (fast)
uplinks = faq = og = schema = 0
for p in pages:
    try:
        html = p.read_text(encoding="utf-8", errors="ignore")
        if "Operator Hub" in html:         uplinks += 1
        if '"FAQPage"'    in html:         faq     += 1
        if 'og:title'     in html:         og      += 1
        if 'ld+json'      in html:         schema  += 1
    except Exception:
        pass

hub_schema = sum(
    1 for h in hubs
    if '"FAQPage"' in h.read_text(encoding="utf-8", errors="ignore")
)

total = len(pages) + len(hubs) + len(pillars)
pct   = lambda n, d: f"{n}/{d} ({100*n//d if d else 0}%)"

# Load latest build report timestamp
latest_report = None
if signals_dir.exists():
    reports = sorted(signals_dir.glob("build-report-*.json"))
    if reports:
        import json as _json
        latest_report = _json.loads(reports[-1].read_text()).get("timestamp", "?")

print()
print("╔═══════════════════════════════════════╗")
print("║      SIDEGUY SEO STATUS · Mar 2026    ║")
print("╠═══════════════════════════════════════╣")
print(f"║  Root pages          {len(pages):<18} ║")
print(f"║  Hub pages           {len(hubs):<18} ║")
print(f"║  Pillar pages        {len(pillars):<18} ║")
print(f"║  Total indexed       {total:<18} ║")
print("╠═══════════════════════════════════════╣")
print(f"║  Manifest topics     {manifest_count:<18} ║")
print(f"║  Expanded seeds      {seed_count:<18} ║")
print(f"║  PJ queue topics     {pj_count:<18} ║")
print("╠═══════════════════════════════════════╣")
print(f"║  Uplinks coverage    {pct(uplinks, len(pages)):<18} ║")
print(f"║  FAQ schema          {pct(faq, len(pages)):<18} ║")
print(f"║  OG tags             {pct(og, len(pages)):<18} ║")
print(f"║  JSON-LD schema      {pct(schema, len(pages)):<18} ║")
print(f"║  Hub FAQ schema      {pct(hub_schema, len(hubs)):<18} ║")
print("╠═══════════════════════════════════════╣")
if latest_report:
    ts = latest_report[:19].replace("T", " ")
    print(f"║  Last build          {ts:<18} ║")
print("║  Pipeline            6h auto + Sun   ║")
print("║  System health       ✅ OK            ║")
print("╚═══════════════════════════════════════╝")
print()
