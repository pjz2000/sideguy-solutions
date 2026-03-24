# SideGuy Cluster Intelligence + Auto Productize System

**Location:** `/_cluster_intelligence.sh`

---

## What It Does

A two-phase GSC-driven intelligence and productization engine:

### Phase 1: Cluster Analysis
- Groups GSC queries into semantic clusters (hvac, payments, tesla-charging, etc.)
- Detects user intent patterns (decision, cost, compare, call)
- Maps geographic demand (San Diego, Encinitas, Carlsbad, etc.)
- Scores page opportunities by impressions + ranking position
- Identifies missing pages based on query clustering

### Phase 2: Smart Productization
- Auto-upgrades top opportunity pages
- Injects cluster-aware interactive product blocks
- Matches block type to user intent
- Prioritizes by cluster strength, not just individual metrics
- Preserves already-productized pages

---

## How to Run

```bash
./_cluster_intelligence.sh
```

---

## Required Input

**File:** `docs/gsc/query-pages.csv`

**Format:**
```csv
page,query,clicks,impressions,ctr,position
https://sideguy.solutions/hvac-repair-san-diego.html,hvac repair san diego,12,450,0.027,8.5
https://sideguy.solutions/tesla-charger-install.html,tesla charger cost,0,85,0,24.2
```

**How to Get:**
1. Google Search Console → Performance
2. Export with both Pages and Queries dimensions
3. Save as CSV with above headers
4. Place in `docs/gsc/query-pages.csv`

---

## Output Files

All outputs go to `docs/cluster-intelligence/`:

### Cluster Analysis
- `clusters-TIMESTAMP.csv` - Topic clusters ranked by impressions
- `intents-TIMESTAMP.csv` - User intent distribution
- `geos-TIMESTAMP.csv` - Geographic demand patterns
- `opportunities-TIMESTAMP.csv` - All pages scored and classified
- `missing-pages-TIMESTAMP.csv` - Suggested new pages based on gaps

### Productization
- `productize-log-TIMESTAMP.txt` - Detailed run log
- `outcomes-TIMESTAMP.txt` - Per-page outcomes (UPDATED/SKIPPED/MISSING/FAILED)
- `cluster-report-TIMESTAMP.md` - Human-readable summary

---

## Product Blocks

Four intent-matched interactive blocks:

### Decision Block
- Interactive repair vs. replace chooser
- Shows reasoning based on user selection
- Use case: "should i repair or replace my hvac"

### Cost Block
- Simple cost estimator (size × $150 multiplier)
- Live calculation on input
- Use case: "how much does hvac repair cost"

### Compare Block
- Side-by-side comparison table
- Option A vs Option B breakdown
- Use case: "hvac repair vs replace" or "stripe vs square"

### Call Block
- "Who should you call?" guidance
- Tiered service recommendation
- Use case: "who do i call for hvac"

All blocks include "Text PJ → 773-544-1231" CTA.

---

## Configuration

**Max pages processed:** 30 (configurable via `MAX_PAGES` variable)

**Cluster detection patterns:**
- hvac: air conditioning, mini split, furnace, heat pump
- tesla-charging: ev charger, level 2, charger install
- payments: stripe, square, payment processor, pos
- energy: solar, battery, powerwall
- roofing: roof, leak, roofer
- plumbing: plumber, water heater, drain, pipe
- electrical: electric panel, outlet, wiring
- digital: website, seo, web design, google business

**Geo detection:**
- San Diego, Encinitas, Carlsbad, Oceanside
- Del Mar, La Jolla, Cardiff, Solana Beach, Coronado

---

## Data Flow

```
GSC Export (CSV)
    ↓
Cluster Analysis (Python)
    ↓
Opportunity Scoring
    ↓
Priority Queue (sorted by score)
    ↓
Productization Loop (bash + awk)
    ↓
Inject Intent-Matched Blocks
    ↓
Verify Injection
    ↓
Git Commit
```

---

## Safety Features

- **No overwrite:** Skips pages already marked `data-sg-productized="v2"`
- **File existence check:** Won't attempt to edit missing files
- **Injection verification:** Confirms block was added before marking success
- **Detailed logging:** Every decision logged to `productize-log-*.txt`
- **Outcome tracking:** Success/failure by reason in `outcomes-*.txt`

---

## Error Handling

**Missing input file:**
```
Missing input: docs/gsc/query-pages.csv
Expected columns: page,query,clicks,impressions,ctr,position
```

**Missing page file:**
```
❌ Missing file
MISSING|hvac|decision|https://...|file.html|125.50
```

**Failed injection:**
```
⚠ Injection check failed
FAILED|hvac|cost|https://...|file.html|98.20
```

Check that file has a valid `<h1>` tag (injection target).

---

## Re-running

Safe to re-run multiple times:
- Already-productized pages are skipped
- Each run gets timestamped outputs
- Git commits only if changes detected
- Idempotent by design

---

## Example Output

```
---------------------------------------
🧠 SIDEGUY CLUSTER INTELLIGENCE LAYER v2
---------------------------------------
Timestamp: 2026-03-24 15:30:45

✅ Phase 1: Cluster analysis complete
   Top cluster: hvac
   Top intent: decision
   Top geo: san diego

---------------------------------------
⚡ Phase 2: Auto Productize Top Pages
---------------------------------------

🛠 Processing top 30 cluster opportunities...

✅ Injected decision block
✅ Injected cost block
⏭ Already productized
✅ Injected compare block

---------------------------------------
✅ COMPLETE - BOTH PHASES DONE
---------------------------------------

📊 Cluster Analysis:
   Top cluster: hvac
   Top intent: decision
   Top geo: san diego

⚡ Productization:
   Updated: 12
   Skipped: 8
   Missing: 3
   Failed:  0

📄 Full report: docs/cluster-intelligence/cluster-report-2026-03-24-153045.md
---------------------------------------

🚀 SideGuy: GSC impressions → cluster insights → product decisions
```

---

## Philosophy

This system implements the SideGuy core philosophy:

> **Offer the truth. Nothing more.**

Product blocks provide genuine utility (calculators, decision tools, comparisons) before any commercial request. They reduce stress and provide clarity at the moment of need.

The cluster intelligence layer ensures we're not just chasing individual keywords, but understanding semantic demand patterns across the entire problem space.

---

## Maintenance

**Weekly cadence:**
1. Export fresh GSC data
2. Run `_cluster_intelligence.sh`
3. Review `cluster-report-*.md`
4. Build missing pages from `missing-pages-*.csv`
5. Monitor cluster performance trends

**Monthly review:**
- Update cluster detection patterns as new verticals emerge
- Refine intent classification rules
- Add new geo targets
- Adjust opportunity scoring weights

---

## Technical Notes

**Dependencies:**
- bash 4.0+
- Python 3.x (with csv, collections, statistics, pathlib)
- awk
- Standard Unix tools (grep, sed, tr, cut, sort, tail, head)

**Performance:**
- Processes ~1000 queries in ~5 seconds
- Productizes 30 pages in ~2 seconds
- Total runtime typically under 10 seconds

**File operations:**
- Uses atomic tmp file pattern for safety
- In-place HTML modification via awk
- No external dependencies or frameworks
