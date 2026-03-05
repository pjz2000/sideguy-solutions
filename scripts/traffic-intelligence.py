#!/usr/bin/env python3
"""
SideGuy Traffic Intelligence Engine
------------------------------------
Reads GSC export data, scores clusters by opportunity signal,
and writes a prioritized expansion queue.

Usage:
  python3 scripts/traffic-intelligence.py

Input:
  docs/traffic-intel/gsc_export_template.csv
  (fill with GSC Performance > Pages > Last 28 days export)

  CSV column order expected:
  date_range, type, impressions, clicks, ctr, position, url, top_query

  Lines starting with # are ignored (comments).

Outputs:
  docs/traffic-intel/generated/opportunity-queries.csv
  docs/traffic-intel/generated/cluster-opportunities.csv
  docs/traffic-intel/expansion/BUILD_QUEUE.md
"""

import csv, json, os, re
from collections import defaultdict
from datetime import datetime

TIMESTAMP = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
INPUT_CSV = 'docs/traffic-intel/gsc_export_template.csv'

# Thresholds (tunable)
MIN_IMPRESSIONS = 5
MAX_POSITION = 30

os.makedirs('docs/traffic-intel/generated', exist_ok=True)
os.makedirs('docs/traffic-intel/expansion', exist_ok=True)

# ─────────────────────────────────────────
# Load cluster inventory
# ─────────────────────────────────────────
with open('docs/auto-cluster/generated/records.json') as f:
    records = json.load(f)

cluster_meta = {}
for r in records:
    k = (r['pillar'], r['cluster'])
    if k not in cluster_meta:
        cluster_meta[k] = {
            'title': r['cluster_title'],
            'pillar': r['pillar'],
            'cluster': r['cluster'],
            'pages': [],
            'hub': f"auto-hubs/clusters/{r['pillar']}--{r['cluster']}.html",
        }
    cluster_meta[k]['pages'].append(r)

# ─────────────────────────────────────────
# Cluster routing rules
# ─────────────────────────────────────────
CLUSTER_RULES = [
    (r'ai cost|automation cost|ai roi|return on investment',       'ai-automation', 'ai-cost'),
    (r'schedul|appointment|booking|calendar',                      'ai-automation', 'ai-scheduling'),
    (r'customer service|chatbot|support bot|customer support',     'ai-automation', 'ai-customer-service'),
    (r'ai tool|automation tool|workflow tool|zapier|make\.com|n8n','ai-automation', 'ai-tools'),
    (r'ai|artificial intel|machine learning|llm|gpt|automat',      'ai-automation', 'ai-overview'),
    (r'chargeback|dispute|friendly fraud|refund chargeback',       'payments',      'chargebacks'),
    (r'payment|merchant|credit card|processing fee|stripe|square|paypal|ach|invoice', 'payments', 'payments-overview'),
    (r'bitcoin|crypto|solana|usdc|stablecoin|wallet|web3',         'payments',      'crypto'),
    (r'hvac|ac unit|air condition|furnace|heat pump|thermostat|cooling|heating',
                                                                   'problem-intelligence', 'general'),
    (r'plumb|water heater|leak|drain|pipe',                        'problem-intelligence', 'general'),
    (r'electr|breaker|outlet|panel|wiring',                        'problem-intelligence', 'general'),
    (r'tesla|ev charging|electric vehicle|level 2|wall connector', 'operator-tools', 'general'),
    (r'san diego|carlsbad|encinitas|escondido|chula vista|el cajon','problem-intelligence', 'general'),
]

def route_query(query):
    q = query.lower()
    for pattern, pillar, cluster in CLUSTER_RULES:
        if re.search(pattern, q):
            return pillar, cluster
    return 'problem-intelligence', 'general'

# ─────────────────────────────────────────
# Parse GSC data
# ─────────────────────────────────────────
opportunities = []
has_real_data = False

with open(INPUT_CSV, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = next(csv.reader([line]))
        if len(parts) < 6:
            continue
        has_real_data = True
        try:
            impressions = float(parts[2].replace(',', ''))
            position    = float(parts[5].replace(',', ''))
            url         = parts[6].strip() if len(parts) > 6 else ''
            query       = parts[7].strip() if len(parts) > 7 else ''
        except (ValueError, IndexError):
            continue
        if impressions >= MIN_IMPRESSIONS and position <= MAX_POSITION:
            pillar, cluster = route_query(query)
            opportunities.append({
                'query': query, 'url': url,
                'impressions': int(impressions), 'position': round(position, 1),
                'pillar': pillar, 'cluster': cluster,
            })

opportunities.sort(key=lambda x: -x['impressions'])

# ─────────────────────────────────────────
# opportunity-queries.csv
# ─────────────────────────────────────────
with open('docs/traffic-intel/generated/opportunity-queries.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['query', 'url', 'impressions', 'position', 'pillar', 'cluster'])
    for o in opportunities:
        w.writerow([o['query'], o['url'], o['impressions'], o['position'], o['pillar'], o['cluster']])

# ─────────────────────────────────────────
# cluster-opportunities.csv
# ─────────────────────────────────────────
cluster_opps = defaultdict(list)
for o in opportunities:
    cluster_opps[(o['pillar'], o['cluster'])].append(o)

with open('docs/traffic-intel/generated/cluster-opportunities.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['pillar', 'cluster', 'total_impressions', 'query_count', 'avg_position', 'top_query'])
    for (pillar, cluster), opps in sorted(cluster_opps.items(), key=lambda x: -sum(o['impressions'] for o in x[1])):
        total_imp = sum(o['impressions'] for o in opps)
        avg_pos   = round(sum(o['position'] for o in opps) / len(opps), 1)
        w.writerow([pillar, cluster, total_imp, len(opps), avg_pos, opps[0]['query']])

# ─────────────────────────────────────────
# Page title suggestion helper
# ─────────────────────────────────────────
def page_suggestions(query):
    q = query.strip()
    slug = re.sub(r'[^a-z0-9]+', '-', q.lower()).strip('-')
    return [
        (f"{q.title()} — What to Know First",            f"{slug}-san-diego.html"),
        (f"{q.title()} Cost in San Diego",                f"{slug}-cost-san-diego.html"),
        (f"Best Tools for {q.title()}",                   f"best-{slug}-tools-san-diego.html"),
        (f"Common {q.title()} Mistakes",                  f"{slug}-mistakes-san-diego.html"),
        (f"How to Handle {q.title()} in San Diego",       f"how-to-handle-{slug}-san-diego.html"),
    ]

# ─────────────────────────────────────────
# BUILD_QUEUE.md
# ─────────────────────────────────────────
lines = [
    "# SideGuy Expansion Queue — Traffic Intelligence",
    "",
    f"Generated: {TIMESTAMP}",
    "",
]

if not has_real_data:
    lines += [
        "## Status: Demo Mode (no GSC data loaded yet)",
        "",
        "**To activate real GSC data:**",
        "1. Open Google Search Console → Performance → Pages → Last 28 days",
        "2. Export → Download CSV",
        "3. Paste rows (skip the GSC header row) into `docs/traffic-intel/gsc_export_template.csv`",
        "   Column order: `date_range,type,impressions,clicks,ctr,position,url,top_query`",
        "4. Run: `python3 scripts/traffic-intelligence.py`",
        "",
        "---",
        "",
        "## Demo Queue — Top Expansion Targets by Cluster Size",
        "",
        "Ranked by current page count (more pages = more ranking surface = highest priority to strengthen):",
        "",
    ]
    ranked = sorted(cluster_meta.items(), key=lambda x: -len(x[1]['pages']))
    for (pillar, cluster), meta in ranked[:12]:
        count = len(meta['pages'])
        sample = meta['pages'][:3]
        lines += [
            f"### {meta['title']}",
            f"**Pillar:** `{pillar}`  **Cluster:** `{cluster}`  **Current pages:** {count:,}",
            f"**Hub:** `/{meta['hub']}`",
            "",
            "**Sample existing pages:**",
        ]
        for p in sample:
            lines.append(f"- [{p['title']}](/{p['file']})")
        lines += [
            "",
            "**Suggested GSC queries to watch for:**",
            f"- {meta['title'].lower()} cost san diego",
            f"- {meta['title'].lower()} explained",
            f"- best {meta['title'].lower()} tools",
            f"- {meta['title'].lower()} mistakes to avoid",
            f"- how long does {meta['title'].lower()} take",
            "",
            "---",
            "",
        ]
else:
    lines += [
        f"## {len(opportunities)} opportunity queries detected",
        f"*(impressions ≥ {MIN_IMPRESSIONS}, position ≤ {MAX_POSITION})*",
        "",
        "---",
        "",
        "## Expansion targets — ranked by cluster signal",
        "",
    ]
    for (pillar, cluster), opps in sorted(cluster_opps.items(), key=lambda x: -sum(o['impressions'] for o in x[1])):
        meta = cluster_meta.get((pillar, cluster), {})
        ct = meta.get('title', cluster)
        total_imp = sum(o['impressions'] for o in opps)
        avg_pos   = round(sum(o['position'] for o in opps) / len(opps), 1)
        current   = len(meta.get('pages', []))
        action    = 'Upgrade hub + add 20–50 new leaf pages' if total_imp > 1000 else 'Add 5–15 new leaf pages'
        lines += [
            f"### {ct}",
            f"**Total impressions:** {total_imp:,}  "
            f"**Queries:** {len(opps)}  "
            f"**Avg position:** {avg_pos}  "
            f"**Existing pages:** {current:,}",
            f"**Recommended action:** {action}",
            "",
            "**Opportunity queries:**",
        ]
        for o in opps[:12]:
            lines.append(f"- `{o['query']}` — {o['impressions']:,} imp @ pos {o['position']}")
        if len(opps) > 12:
            lines.append(f"- *(+{len(opps)-12} more in opportunity-queries.csv)*")
        lines += ["", "**Suggested new pages (from top query):**"]
        for title, slug in page_suggestions(opps[0]['query']):
            lines.append(f"- **{title}** → `{slug}`")
        lines += ["", "---", ""]

lines += [
    "## How to use this file",
    "",
    "1. Work top-to-bottom (highest signal first)",
    "2. For each cluster target:",
    "   - Copy a similar existing leaf page",
    "   - Update `<title>`, meta description, H1, and body content",
    "   - Commit: `git add . && git commit -m 'Add: [page title] — [cluster]'`",
    "3. After adding 5+ pages to a cluster: regenerate cluster hub with Auto-Cluster Engine",
    "4. Re-export GSC weekly and re-run this script to refresh the queue",
    "",
    "## Reference files",
    "",
    "| File | Purpose |",
    "|------|---------|",
    "| `docs/traffic-intel/generated/clusters.tsv` | Full cluster inventory with page counts |",
    "| `docs/traffic-intel/generated/opportunity-queries.csv` | Filtered GSC queries |",
    "| `docs/traffic-intel/generated/cluster-opportunities.csv` | Cluster-level roll-up |",
    "| `docs/auto-cluster/generated/records.json` | Master page index (12,757 pages) |",
    "| `auto-hubs/directory.html` | Full site directory (crawl highway) |",
]

with open('docs/traffic-intel/expansion/BUILD_QUEUE.md', 'w') as f:
    f.write('\n'.join(lines) + '\n')

print(f'STATUS: {"DEMO MODE — no GSC data" if not has_real_data else str(len(opportunities)) + " real opportunities"}')
print(f'✅ docs/traffic-intel/generated/opportunity-queries.csv')
print(f'✅ docs/traffic-intel/generated/cluster-opportunities.csv')
print(f'✅ docs/traffic-intel/expansion/BUILD_QUEUE.md')
print()
print('Drop real GSC data into docs/traffic-intel/gsc_export_template.csv and re-run to activate.')
