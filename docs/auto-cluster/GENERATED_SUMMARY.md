# SideGuy Auto-Cluster Engine — Generated Summary

Generated: 2026-03-05 · Engine: Python (idempotent, re-runnable)

## What ran

- Scanned all HTML pages: root level + `pages/`, `hubs/`, `authority/` subdirs
- Excluded: `backups*/`, `backup_pages/`, `docs/`, `auto-hubs/`, `.git/`, `node_modules/`
- Built page → pillar/cluster classification from: `docs/auto-cluster/rules.tsv`
- Generated:
  - Cluster hubs: `auto-hubs/clusters/` (16 files)
  - Pillar hubs: `auto-hubs/pillars/` (4 files)
- Injected "Related Problems" nav into leaf pages (idempotent, marker: `sideguy-related-problems`)

## Inventory

| Metric | Count |
|--------|-------|
| Pages scanned | 12,757 |
| Unique pillars | 4 |
| Unique clusters | 16 |
| Cluster hub pages | 16 |
| Pillar hub pages | 4 |

## Top 25 clusters by page count

| Cluster | Pages |
|---------|-------|
| ai-automation/ai-cost | 5421 |
| ai-automation/ai-overview | 2250 |
| ai-automation/ai-tools | 1669 |
| ai-automation/ai-city-pages | 1268 |
| ai-automation/ai-scheduling | 1201 |
| ai-automation/ai-agent-workflows | 446 |
| ai-automation/ai-consulting | 231 |
| ai-automation/ai-restaurants | 116 |
| problem-intelligence/general | 52 |
| ai-automation/ai-customer-service | 36 |
| ai-automation/ai-healthcare | 36 |
| payments/payments-overview | 17 |
| payments/payment-fees | 8 |
| operator-tools/operator-tools-overview | 4 |
| payments/stripe | 1 |
| payments/chargebacks | 1 |

## Pillar distribution

| Pillar | Pages |
|--------|-------|
| ai-automation | 12674 |
| problem-intelligence | 52 |
| payments | 27 |
| operator-tools | 4 |


## Files

| File | Purpose |
|------|---------|
| `docs/auto-cluster/rules.tsv` | Classification rules (pattern → pillar/cluster) |
| `docs/auto-cluster/generated/page-index.tsv` | Full page index (TSV) |
| `docs/auto-cluster/generated/page-index.jsonl` | Full page index (JSONL) |
| `docs/auto-cluster/generated/records.json` | Full page records (JSON array) |
| `auto-hubs/clusters/` | HTML cluster hub pages (linked from every leaf) |
| `auto-hubs/pillars/` | HTML pillar hub index pages |

## Next best tuning

1. **Expand `rules.tsv`** — add patterns for underserved pillars (home-systems, local-operator-tech, etc.)
2. **Move auto-hubs** into site root or `/hubs/` for canonical URLs
3. **Add See Also** cluster-to-cluster cross-links on hub pages
4. **Re-run classification** anytime with: `python3 scripts/problem-map.py` (or equivalent)
5. **Fix `pages/` subdir** — many pages land in `ai-automation/general` due to generic titles; improving `<title>` tags will improve cluster accuracy
