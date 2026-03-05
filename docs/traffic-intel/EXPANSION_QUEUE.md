# SideGuy Expansion Queue (Traffic Intelligence)

Generated: 2026-03-05 18:00:44

## How to use

1. Export GSC pages (last 28 days) → paste into: `docs/traffic-intel/gsc_export_template.csv`
2. Identify:
   - Pages with impressions rising
   - Positions 8–30 (close to ranking)
   - Clusters where multiple leaf pages show impressions
3. For each high-signal cluster:
   - Upgrade cluster hub (better intro + common misunderstandings + step list)
   - Generate +10–50 new leaf pages (answering adjacent questions)
   - Add internal links (leaf↔leaf, cluster↔cluster, category↔category)

## Next best build rule

**Follow demand.** Expand where impressions appear.

## Quick cluster reference

| Pillar | Cluster | Pages |
|--------|---------|-------|
| ai-automation | AI Automation Cost & ROI | 5,421 |
| ai-automation | AI Automation (Overview) | 2,250 |
| ai-automation | AI Automation Tools | 1,669 |
| ai-automation | AI Automation — City Pages | 1,268 |
| ai-automation | AI Scheduling & Booking | 1,201 |
| ai-automation | AI Agent Workflows | 446 |
| ai-automation | AI Consulting | 231 |
| ai-automation | AI for Restaurants | 116 |
| ai-automation | AI Customer Service | 36 |
| ai-automation | AI for Healthcare Practices | 36 |
| operator-tools | Operator Tools (Overview) | 4 |
| payments | Payment Processing (Overview) | 17 |
| payments | Payment Fee Comparison | 8 |
| payments | Stripe Troubleshooting | 1 |
| payments | Chargebacks & Disputes | 1 |
| problem-intelligence | General (Other) | 52 |

## Templates ready

- **Cluster hub template:** copy any file in `auto-hubs/clusters/`
- **Leaf page template:** copy any comparable leaf + update title/content/meta

## Traffic-Weighted Expansion Engine (next step)

When GSC export is available, run:

1. Load `gsc_export_template.csv`
2. Join impressions/clicks/position to `docs/auto-cluster/generated/records.json` by URL
3. Score each cluster: `sum(impressions) / page_count × avg_position_proximity`
4. Output top-10 expansion targets
5. Auto-generate leaf stubs for each target cluster
