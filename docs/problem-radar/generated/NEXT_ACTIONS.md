# Next Actions — Problem Radar AI

Generated: 2026-03-05 20:12:44

## Weekly workflow

### Step 1 — Paste new signals
- Emerging topics → `docs/problem-radar/trends_notes.txt`
- Things you want to own → `docs/problem-radar/manual_seeds.txt`
- GSC export → `docs/traffic-intel/gsc_export_template.csv`
  - GSC: Performance → Pages → Last 28 days → Export CSV
  - Column order: `date_range,type,impressions,clicks,ctr,position,url,top_query`

### Step 2 — Re-run
```bash
python3 scripts/traffic-radar.py
```

### Step 3 — Feed Claude
Copy `docs/problem-radar/generated/CLAUDE_PROMPT.md` into a new Claude conversation.

### Step 4 — Build top cluster targets
Work top-to-bottom in `docs/problem-radar/generated/RADAR_QUEUE.md`.

### Step 5 — Improve rules over time
Better classification accuracy → edit `docs/auto-cluster/rules.tsv`
- Add more specific patterns ABOVE general ones
- Re-run after editing

---

## Next engine: Cluster Gap Finder
Detects clusters with GSC traffic but weak hub pages → auto-prioritizes hub upgrades.
