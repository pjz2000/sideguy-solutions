# SideGuy Trend Radar

Turns raw problem phrases into build-ready cluster intelligence.

## Files

| File | Purpose |
|---|---|
| `data/trend-radar/seed_topics.txt` | Raw problem phrases — add new ones here |
| `docs/trend-radar/radar-signals.tsv` | Full signal output (tab-separated) |
| `docs/trend-radar/radar-report.md` | Prioritized build queue (human-readable) |
| `data/trend-radar/radar-clusters.json` | Cluster data (machine-readable) |
| `docs/trend-radar/claude-build-queue.md` | Build rules and quality checklist |

## Usage

```bash
# Add new seed phrases to seed_topics.txt, then:
python3 tools/trend-radar/trend_radar.py

# Or via the runner script:
bash tools/trend-radar/run_trend_radar.sh
```

## Purpose

Keep SideGuy aligned with real-world problems operators are searching for — not random page spam.

Scoring priority:
- `money-pain` intent + core bucket = 5 points (build first)
- `diagnostic` intent + core bucket = 4 points
- `guidance` intent + core bucket = 3 points
