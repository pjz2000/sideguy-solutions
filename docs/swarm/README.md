# SideGuy Swarm Intelligence System

**Version:** 8.1  
**Philosophy:** Human-first automated assistance, not autopilot

## What It Does

The Swarm script analyzes Google Search Console data to intelligently:
- **Rewrite** titles on mid-performing pages (score 8-15)
- **Expand** high-performing pages into pattern-specific variants (score 15+)
- **Inject** tool placeholders into elite top-20 pages
- **Protect** declining pages from further optimization (negative trend)

## Key Improvements in v8.1

### Safety Features
- ✅ **Dry-run mode** - preview changes before applying
- ✅ **Automatic backups** - all modified files get `.bak` copies
- ✅ **GSC file validation** - fails gracefully if data missing
- ✅ **Error handling** - proper exit codes and validation

### Smart Scoring
- **Old formula:** `(impressions/30) + (clicks*2) + ctr`
- **New formula:** `(impressions/30) + (clicks*5) + (ctr*10)`
- **Why:** Values engagement over visibility

### Better Intent Detection
Recognizes 5 intents (vs 3 in v8):
- `money` - cost, price, pricing, how much
- `call` - urgent, emergency, who do i call, help me
- `compare` - vs, best, which, should i
- `service` - near me, repair, install
- `info` - everything else

### Pattern Detection
Expands from 3 to 6 patterns:
- `cost`, `vs`, `best`, `guide`, `local`, `decision`

### Human-First Workflow
- **No auto-commit by default** - review before pushing
- **Detailed markdown reports** - track every decision
- **Revert instructions** - easy undo path

## Usage

### 1. Prepare GSC Data

Export from Google Search Console as CSV with columns:
```
PAGE,QUERY,CLICKS,IMPRESSIONS,CTR,POSITION
```

Save to: `data/gsc-export.csv`

### 2. Dry Run (Preview Only)

```bash
DRY_RUN=1 ./swarm-v8.sh
```

Reviews all data and shows what *would* happen without making changes.

### 3. Live Run (Apply Changes)

```bash
./swarm-v8.sh
```

Modifies files but waits for manual git commit.

### 4. Auto-Commit Mode

```bash
AUTO_COMMIT=1 ./swarm-v8.sh
```

⚠️ **Use with caution** - automatically commits changes to git.

## Configuration

Edit these variables in `swarm-v8.sh`:

```bash
MAX_REWRITES=25      # Max title tag rewrites
MAX_EXPANDS=10       # Max new page expansions
MAX_TOOLS=15         # Max tool slot injections

SCORE_EXPAND=15.0    # Minimum score for expansion
SCORE_REWRITE=8.0    # Minimum score for rewrite
SCORE_ELITE=12.0     # Threshold for elite status
```

## Memory System

The swarm maintains a memory file at `data/swarm-memory.csv`:

```csv
slug,score,trend_streak,last_action,last_seen
ac-repair-san-diego,42.5,0,rewrite,2026-03-24-215034
```

### Loser Protection

Pages with `trend_streak ≤ -3` are skipped automatically to avoid optimizing dead content.

## Reports

Every run generates a detailed report:

```
docs/swarm/swarm-report-YYYY-MM-DD-HHMMSS.md
```

Contains:
- Configuration used
- Elite pages (top 20)
- All rewrites with new titles
- All expansions with patterns
- Tool slots added
- Skipped pages (losers)
- Revert instructions
- Human review checklist

## Alignment with SideGuy Philosophy

### ✅ Human-First Design
- Dry-run mode for preview
- Manual commit by default
- Detailed reports for review
- Easy revert path

### ✅ Observation Over Automation
- Reports track *why* decisions were made
- Memory system learns from performance
- Loser protection prevents wasted effort

### ✅ Quality Over Quantity
- Caps on all actions (25/10/15)
- Elite prioritization (top 20)
- Score-based thresholds

### ⚠️ Tension Points

The swarm *does* generate content programmatically, which conflicts with:
> "DO NOT create automated page generators"

**Mitigation:**
1. Generated pages are **placeholders only** - HTML comments say "Human review required"
2. Caps prevent runaway generation (max 10 per run)
3. Reports list every generated page for quality review

## Workflow Integration

### Morning Routine
1. Export fresh GSC data weekly
2. Run swarm in dry-run mode: `DRY_RUN=1 ./swarm-v8.sh`
3. Review report in `docs/swarm/`
4. If satisfied, run live: `./swarm-v8.sh`
5. Manually review expanded pages
6. Add real content to placeholders
7. Test changes locally
8. Commit: `git add . && git commit -m "swarm: applied intelligence"`

### Weekly Review
- Check `data/swarm-memory.csv` for trend patterns
- Identify recurring losers (manual intervention)
- Validate expanded pages have real content
- Test tool slots before implementing

## Troubleshooting

### "GSC file not found"
```bash
# Create sample data for testing
echo "PAGE,QUERY,CLICKS,IMPRESSIONS,CTR,POSITION" > data/gsc-export.csv
echo "https://sideguy.solutions/ac-repair-san-diego.html,ac repair san diego,5,100,0.05,8" >> data/gsc-export.csv
```

### "No changes made"
- Check if public/ directory exists
- Verify GSC file has more than header row
- Check score thresholds (may be too high)

### "Git commit failed"
- May have no actual changes (all pages already processed)
- Check git status manually
- Review swarm report for details

## Future Enhancements

Ideas for v8.2+:
- [ ] Integration with GSC API (auto-fetch data)
- [ ] A/B testing framework for title rewrites
- [ ] LLM-generated content for expansions (with human review queue)
- [ ] Alerting when elite pages drop below threshold
- [ ] Automatic linking between parent → expanded pages
- [ ] Tool slot templates by intent type

---

**Remember:** The swarm is an *assistant*, not an autopilot. Always review before deploying.
