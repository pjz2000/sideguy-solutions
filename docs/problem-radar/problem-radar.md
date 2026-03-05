# SideGuy Problem Radar

## Purpose
Detect real search problems before building pages.
Build where demand exists — not where we guess.

## How It Works

```
Real search demand appears
  → SideGuy page ranks for related query
  → GSC shows impressions + new queries
  → New cluster identified
  → 20–50 leaf pages generated for that cluster
  → Cluster page built to anchor them
  → Internal links wired up
  → Repeat
```

This creates a self-compounding SEO system — every page that ranks reveals the next cluster to build.

## Current Signals (tracked in data/)

| File | What it tracks |
|------|---------------|
| `data/pillar-leaf-map.json` | All pages mapped to their pillar |
| `data/reputation-gravity.json` | Top 100 authority nodes by inbound link score |
| `data/problem-map.json` | Problem taxonomy from knowledge graph |
| `signals/signals.json` | Rising search signals (Trend Seismograph) |
| `signals/problem-taxonomy.json` | Structured problem categories |

## Radar Decision Rules

1. **If a page has impressions but < 2% CTR** → fix title + meta description
2. **If a query cluster has impressions but no page** → build a leaf page this week
3. **If a leaf is pulling queries from a related topic** → build a cluster to anchor it
4. **If a pillar has < 5 clusters** → build more clusters (topical authority signal)
5. **If a pillar hub page doesn't exist** → build it (high-priority gap)

## Current Gaps (Phase 2B)

| Pillar | Missing |
|--------|---------|
| `business-software` | Hub page |
| `energy-ev` | Hub page |
| `operator-tools` | Hub page |
| All pillars | Pyramid nav on leaf pages |
| All clusters | Real HTML cluster pages |

## Refresh Cycle
- Weekly: check GSC impressions by pillar
- Monthly: run `data/pillar-leaf-map.json` regen to capture new pages
- Quarterly: review cluster gaps vs. actual search demand
