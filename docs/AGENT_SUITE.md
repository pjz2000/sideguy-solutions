# SideGuy Agent Suite

**Status:** Manual execution only (observation mode)  
**Philosophy:** Human-first clarity layer, automation deferred

---

## Available Agents

### Core Orchestrator

**`swarm-orchestrator.sh`**  
Master orchestrator running 9 specialized agents in sequence:
1. Signal Agent - Build opportunity queue from GSC data
2. Hyper Update Agent - Query-specific "Quick Answer" blocks
3. Product Agent - Weighted tool injection (calculators/decision tools)
4. Spawn Agent - Generate child inventory pages
5. Link Agent - Reinforce parent/child relationships
6. Cluster Agent - Generate intelligence reports
7. Adaptive Agent - Detect winning patterns
8. Memory Agent - Save winning defaults
9. Weighted Brain Agent - Reinforce successful patterns

**Input:** `docs/gsc/query-pages.csv`  
**Limits:** MAX_HYPER=20, MAX_PRODUCT=15, MAX_SPAWN_PARENTS=10

---

### Specialized Agents

**`money-agent.sh`**  
Injects conversion-focused CTA blocks on money-intent queries.

**Triggers:** cost|price|quote|install|repair|near|who|best  
**Block:** Green CTA section with PJ contact  
**Marker:** `data-sg-money="v1"`

---

### Feedback Loop (Human Observatory)

**`close-the-loop-engine.sh`**  
Manual feedback collection from real PJ interactions.

**Captures:** page, question, intent, confusion point, outcome  
**Storage:** `docs/pj-feedback/feedback-log.csv`  
**Philosophy:** Pure observation, no auto-modification

**`analyze-feedback.sh`**  
Generates intelligence reports from feedback log.

**Output:** Intent distribution, outcome patterns, confusion themes  
**Reports:** `docs/pj-feedback/reports/analysis-*.md`  
**Use:** Identify patterns to inform manual content improvements

---

## Safety Features

- **Idempotency:** All agents check for existing markers before injecting
- **File validation:** Normalize URLs, verify files exist before edit
- **Logging:** All actions logged to timestamped run directories
- **Git commits:** Automatic commit after swarm runs (optional)

---

## Expected CSV Format

```csv
page,query,clicks,impressions,ctr,position
```

**Example:**
```csv
https://www.sideguysolutions.com/hvac-repair-san-diego.html,hvac repair cost,3,450,0.0067,18.5
```

---

## Memory System

**`docs/memory/patterns.json`** - Cluster → best tool mappings  
**`docs/memory/weighted.json`** - Tool weights per cluster (adaptive)

Default tools:
- `decision_tool` - Repair vs Replace logic
- `cost_tool` - Quick cost estimator
- `compare_tool` - Side-by-side comparison
- `call_tool` - Who to call guidance

---

## Execution Order (Recommended)

```bash
# 1. Run swarm orchestrator (does everything)
./swarm-orchestrator.sh

# 2. OR run specialized agents individually
./money-agent.sh

# 3. Collect feedback after PJ interactions
./close-the-loop-engine.sh

# 4. Analyze patterns periodically
./analyze-feedback.sh
```

### Feedback Loop Workflow

1. **After helping someone** → Run `./close-the-loop-engine.sh`
2. **Log the interaction** → Page, question, confusion, outcome
3. **Weekly review** → Run `./analyze-feedback.sh`
4. **Identify patterns** → What's confusing? What's working?
5. **Manual improvements** → Rewrite problem areas, test new blocks
6. **Close loop** → Next feedback cycle validates changes

---

## Output Directories

- `docs/swarm/runs/YYYY-MM-DD-HHMMSS/` - Swarm run logs
- `docs/swarm/runs/*/reports/` - Cluster/intent/geo intelligence
- `docs/money/` - Money agent logs
- `docs/memory/` - Pattern memory (JSON)

---

## Human Decision Points

⚠️ **STOP and ask PJ before:**
- Running swarm orchestrator for the first time
- Changing MAX limits
- Modifying tool block HTML
- Adding new agent logic
- Changing memory weights manually

---

## Sanity Checks

Before running:
1. ✅ GSC CSV exists at `docs/gsc/query-pages.csv`
2. ✅ CSV has correct header format
3. ✅ Backup recent changes (git commit)
4. ✅ Verify template exists or uses fallback
5. ✅ Test on 1-2 pages first (modify MAX_HYPER=2)

After running:
1. ✅ Check `summary.md` in run directory
2. ✅ Review `outcomes.txt` for errors
3. ✅ Spot-check updated HTML files
4. ✅ Validate sitemap.xml if children spawned
5. ✅ Test injected tools in browser

---

## Notes

- All scripts use inline AWK for surgical HTML injection
- Python used for JSON/CSV analysis and memory updates
- No external dependencies beyond bash/python3/git
- Preserves inline CSS, does not extract to external files
- Compatible with SideGuy flat HTML architecture
