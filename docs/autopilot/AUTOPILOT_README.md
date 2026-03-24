# SideGuy Autopilot System

**Query-driven content automation with human-first safety guardrails**

## What This Is

Three complementary automation engines that analyze Google Search Console data and intelligently upgrade pages based on real user queries:

1. **Hyper Productize** — Injects interactive tools (calculators, decision widgets)
2. **Hyper Auto-Adapt** — Detects winning patterns and replicates them globally
3. **Autopilot Orchestrator** — Master controller that runs all engines in sequence

## Philosophy Alignment

This automation **respects SideGuy's human-first philosophy**:

- ✅ **Dry-run by default** — Preview before applying
- ✅ **Hard limits** — Max pages per run (no runaway automation)
- ✅ **Skip markers** — Won't re-inject content (uses `data-sg-productized`, `data-auto-adapt`)
- ✅ **Decision logs** — Full reports and audit trails
- ✅ **Quality over scale** — Targets high-performing queries only

## Quick Start

### 1. Dry Run (Preview Only)

```bash
# Preview what hyper-productize would do
./hyper-productize.sh

# Preview what auto-adapt would do
./hyper-auto-adapt.sh

# Preview full autopilot sequence
./autopilot-orchestrator.sh
```

### 2. Run Live (Apply Changes)

```bash
# Apply productize changes
DRY_RUN=false ./hyper-productize.sh

# Apply auto-adapt changes
DRY_RUN=false ./hyper-auto-adapt.sh

# Run full autopilot live
DRY_RUN=false ./autopilot-orchestrator.sh
```

### 3. Review Reports

After each run, check:

```
docs/hyper-productize/productize-report.md
docs/auto-adapt/adapt-report.md
docs/autopilot/runs/[timestamp]/summary.md
```

## Script Details

### hyper-productize.sh

**Purpose:** Inject interactive tools based on query intent

**How it works:**
1. Reads `docs/gsc/query-pages.csv`
2. Detects cluster (hvac, tesla, payments, etc.)
3. Detects intent (cost, compare, decision, call)
4. Matches appropriate tool template
5. Injects after first `<h1>` tag

**Tools available:**
- HVAC cost calculator (sq ft → price estimate)
- Tesla charger install estimator
- Repair vs. replace decision tool
- Quick comparison table

**Safety limits:**
- Default: `MAX_UPDATES=50` (set higher if needed)
- Skips pages already marked `data-sg-productized`
- Dry-run by default

### hyper-auto-adapt.sh

**Purpose:** Detect winning content patterns and replicate globally

**How it works:**
1. Scans GSC data for high performers (configurable thresholds)
2. Groups winners by cluster (hvac, tesla, payments, etc.)
3. Identifies pattern type (decision tool, cost estimator, etc.)
4. Applies winning pattern to ALL similar pages in that cluster

**Safety limits:**
- Default: `MIN_CLICKS=20`, `MIN_IMPRESSIONS=300`
- Default: `MAX_UPDATES=100`
- Skips pages already marked `data-auto-adapt`
- Dry-run by default

**⚠️ Warning:** This is the most aggressive engine — it applies patterns globally. Always dry-run first.

### autopilot-orchestrator.sh

**Purpose:** Master controller for multi-phase automation

**Execution sequence:**
1. **Phase 1:** Hyper updates (existing `_hyper_update_engine.sh`)
2. **Phase 2:** Productize tools (`hyper-productize.sh`)
3. **Phase 3:** Auto-adapt patterns (`hyper-auto-adapt.sh`)
4. **Phase 4:** Sitemap regeneration (if changes were made)

**Configuration:**

```bash
# Run all phases
./autopilot-orchestrator.sh

# Disable specific phases
RUN_ADAPT=false ./autopilot-orchestrator.sh

# Run live with custom phase toggles
DRY_RUN=false RUN_HYPER=true RUN_PRODUCTIZE=true RUN_ADAPT=false ./autopilot-orchestrator.sh
```

**Phase toggles:**
- `RUN_HYPER` (default: `true`) — Quick answer blocks
- `RUN_PRODUCTIZE` (default: `true`) — Interactive tools
- `RUN_ADAPT` (default: `false`) — Global pattern replication
- `RUN_SITEMAP` (default: `false`) — Sitemap regeneration

## Input Data

All scripts expect `docs/gsc/query-pages.csv` with this format:

```csv
page,query,clicks,impressions,ctr,position
https://www.sideguysolutions.com/ac-not-cooling-san-diego.html,ac not cooling san diego,45,892,5.0,8.2
https://www.sideguysolutions.com/hvac-repair-san-diego.html,how much does hvac repair cost,32,654,4.9,12.3
```

**How to get this:**
1. Go to Google Search Console
2. Performance > Pages
3. Export as CSV
4. Save to `docs/gsc/query-pages.csv`

## Safety Features

### Dry-Run Mode (Default)

All scripts **preview changes without modifying files** unless explicitly overridden:

```bash
DRY_RUN=false ./script.sh  # Actually apply changes
```

### Hard Limits

Scripts stop after hitting configured limits:

- `MAX_UPDATES=50` (hyper-productize)
- `MAX_UPDATES=100` (hyper-auto-adapt)

Override if needed:

```bash
MAX_UPDATES=200 DRY_RUN=false ./hyper-productize.sh
```

### Skip Markers

Scripts use HTML data attributes to avoid duplicate injections:

- `data-sg-productized="hvac-cost-v1"` — Productize marker
- `data-auto-adapt="decision-v1"` — Auto-adapt marker
- `data-hyper-update="v2"` — Hyper update marker

Once injected, pages are skipped on subsequent runs.

### Audit Trails

Every run creates:
- **Log file** — Full execution log with timestamps
- **Report file** — Markdown summary with stats
- **Outcomes file** — Structured results for tracking

## Example Workflow

### Week 1: Discovery

```bash
# Pull fresh GSC data (Performance > Pages > Export)
# Save to docs/gsc/query-pages.csv

# Preview what would happen
./autopilot-orchestrator.sh

# Review reports
cat docs/hyper-productize/productize-report.md
cat docs/auto-adapt/adapt-report.md
```

### Week 2: Test Run (Productize Only)

```bash
# Apply productize to limited set
MAX_UPDATES=25 DRY_RUN=false ./hyper-productize.sh

# Validate on 5-10 sample pages
# Check: Does tool render correctly?
# Check: Does it align with SideGuy philosophy?
# Check: Is copy calm and helpful?
```

### Week 3: Monitor

- Watch GSC for engagement changes
- Look for time-on-page improvements
- Check for any ranking drops (red flag)
- Note which tool types perform best

### Week 4: Expand (If Validated)

```bash
# Apply to more pages
MAX_UPDATES=100 DRY_RUN=false ./hyper-productize.sh

# If patterns are working, consider auto-adapt
DRY_RUN=false RUN_ADAPT=true ./autopilot-orchestrator.sh
```

## Decision Points (Human Review Required)

### Before First Live Run

- [ ] Validate tool copy matches SideGuy tone (calm, no hype)
- [ ] Test tools on sample pages (calculators work correctly?)
- [ ] Confirm GSC data is recent (within 7 days)
- [ ] Review cluster/intent detection logic (accurate?)

### After Each Live Run

- [ ] Spot-check 10-20 modified pages
- [ ] Verify no duplicate injections occurred
- [ ] Confirm HTML is valid (no broken tags)
- [ ] Check mobile rendering (tools responsive?)

### Before Global Auto-Adapt

- [ ] Identify winning patterns manually first
- [ ] Validate pattern quality (not just traffic spike)
- [ ] Confirm pattern applies broadly (not one-off edge case)
- [ ] Set conservative thresholds (`MIN_CLICKS=30+`)

## Troubleshooting

### "Missing input CSV"

```bash
# Check file exists
ls -lh docs/gsc/query-pages.csv

# If missing, export from GSC
# Performance > Pages > Export > Save as query-pages.csv
```

### "No pages updated"

Possible causes:
- All pages already have markers (check with `grep -r "data-sg-productized" *.html`)
- Query/page thresholds too high (check `MIN_CLICKS`, `MIN_IMPRESSIONS`)
- Cluster/intent detection not matching (review detection logic)

### "Script not found"

```bash
# Make sure scripts are executable
chmod +x hyper-productize.sh hyper-auto-adapt.sh autopilot-orchestrator.sh
```

### "Changes not appearing"

- Verify `DRY_RUN=false` was set
- Check log files for errors
- Confirm file permissions (can write to HTML files?)

## Advanced Configuration

### Custom Thresholds

```bash
# Only productize high-traffic queries
MIN_CLICKS=50 MIN_IMPRESSIONS=1000 DRY_RUN=false ./hyper-productize.sh

# More aggressive auto-adapt
MIN_CLICKS=10 MIN_IMPRESSIONS=200 MAX_UPDATES=500 DRY_RUN=false ./hyper-auto-adapt.sh
```

### Selective Execution

```bash
# Only run productize (skip adapt)
RUN_ADAPT=false ./autopilot-orchestrator.sh

# Only run adapt (skip productize and hyper)
RUN_HYPER=false RUN_PRODUCTIZE=false RUN_ADAPT=true ./autopilot-orchestrator.sh
```

### Custom Tool Templates

Edit tool generation functions in `hyper-productize.sh`:

- `build_hvac_cost_tool()`
- `build_tesla_charger_tool()`
- `build_decision_tool()`
- `build_comparison_tool()`

Follow existing patterns:
- Use inline styles (no external CSS)
- Use CSS variables (`var(--mint)`, `var(--ink)`)
- Include `data-sg-productized="tool-name-v1"` marker
- End with "Text PJ → 773-544-1231" CTA

## Monitoring & Validation

### GSC Metrics to Watch

Post-deployment (2-4 weeks):

- **CTR changes** — Should improve for productized pages
- **Time on page** — Interactive tools should increase engagement
- **Bounce rate** — Decision tools should reduce exits
- **Position changes** — Should be neutral or improve (never drop)

### Red Flags

Stop and investigate if:

- ❌ Average position drops >5 spots
- ❌ Impressions drop significantly (deindexing?)
- ❌ Duplicate content warnings in GSC
- ❌ Mobile usability errors spike

### Success Signals

Continue/expand if:

- ✅ CTR improves 10-30%
- ✅ "Text PJ" conversion tracking shows lift
- ✅ Time on page increases
- ✅ Pages rank for more query variations

## Files Created

```
/workspaces/sideguy-solutions/
├── hyper-productize.sh          # Interactive tool injector
├── hyper-auto-adapt.sh          # Winning pattern replicator
├── autopilot-orchestrator.sh    # Master controller
└── docs/
    ├── hyper-productize/
    │   ├── productize-log.txt
    │   └── productize-report.md
    ├── auto-adapt/
    │   ├── adapt-log.txt
    │   ├── adapt-report.md
    │   └── winning-patterns.txt
    └── autopilot/
        └── runs/
            └── [timestamp]/
                ├── autopilot.log
                ├── summary.md
                └── outcomes.txt
```

## Philosophy

This automation exists to **amplify human judgment, not replace it**.

- **Data-driven:** Uses real GSC queries, not guesses
- **Pattern-based:** Replicates what's working, not untested experiments
- **Reversible:** All changes are traceable via git
- **Transparent:** Full audit trails and reports
- **Conservative:** Dry-run defaults, hard limits, skip logic

**Remember:** SideGuy is a calm place for stressed people. Every automated change should reduce confusion, not create it.

---

**Questions?** Text PJ → 773-544-1231
