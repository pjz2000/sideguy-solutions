# SideGuy Self-Improving SEO Engine

## What it does
1. Reads GSC Pages export → identifies "winner" pages (impressions ≥ threshold)
2. Injects **contextual internal links** on non-winner pages → pointing to winners (funnels authority to strong pages)
3. Generates an **expansion queue** of 8 intent angles per winner page
4. Writes a full report to `docs/self-improving-seo/report.md`

## Setup

1. Export Search Console → **Performance → Pages → Export CSV**
2. Save as: `docs/gsc/gsc_pages.csv`
3. Run:
   ```
   python3 tools/self-improving-seo/self_improving_seo.py
   ```

## Outputs

| File | Description |
|---|---|
| `docs/self-improving-seo/report.md` | Full run report (winners, stats, next steps) |
| `docs/self-improving-seo/winners.txt` | Tab-separated: impr / clicks / page |
| `docs/self-improving-seo/expansion-queue.tsv` | Intent expansion ideas for each winner |

## Config (in `self_improving_seo.py`)

| Variable | Default | Description |
|---|---|---|
| `MIN_IMPRESSIONS` | 5 | Minimum impressions to count as a winner |
| `TOP_WINNERS` | 80 | Max winner pages per run |
| `INJECT_PAGES_MAX` | 350 | Max pages modified per run |
| `CONTEXT_LINKS` | 3 | Links injected per page |
| `SEED` | 402 | Deterministic random seed (stable diffs) |

## Safety

- Pages already injected are **skipped** (guarded by `<!-- SideGuy Context Links (Auto) -->` marker)
- `_quarantine_backups/` and `.git/` are **never touched**
- All changes are **idempotent**: re-running never double-injects
