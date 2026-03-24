# SideGuy Swarm v9 Unified

**The best of both worlds:** Safety & intelligence from v8.1 + rich automation from v3

## Philosophy

Swarm v9 is a **human-first intelligent assistant**, not an autopilot. It:
- **Suggests** improvements based on real search data
- **Respects** human review through dry-run mode
- **Protects** with automatic backups
- **Reports** every decision with full transparency

## What It Does

### 1. In-Place Page Upgrades
Adds helpful sections to existing pages:
- **Swarm note**: "Need a clear next step?" CTA with Text PJ
- **Cost block**: For money-intent queries (pricing, cost)
- **Contact orb**: Fixed-position "Text PJ" button

### 2. Child Page Generation
Creates pattern-based child pages:
- `{query}-cost.html` - Cost guide and variables
- `{query}-near-me.html` - Local help and red flags
- `{query}-worth-it.html` - Decision framework

### 3. Internal Linking
Automatically links related child pages to each other.

### 4. Sitemap Integration
Appends new pages to `sitemap.xml` with proper formatting.

### 5. Index Updates
Adds "Fresh Help Paths" section to index.html with links to new pages.

## Key Features

### From v8.1 (Safety & Intelligence)
✅ **Dry-run mode** - Preview before applying  
✅ **Automatic backups** - Every modified file gets `.bak.{timestamp}`  
✅ **Validation checks** - GSC file, sitemap, index presence  
✅ **Enhanced scoring** - `(impressions/30) + (clicks*5) + (ctr*10)`  
✅ **Intent detection** - 5 types: money, call, compare, service, info  
✅ **Pattern detection** - 6 types: cost, vs, best, guide, local, decision  
✅ **No auto-commit** - Manual review by default  
✅ **Comprehensive reports** - Markdown with full action log

### From v3 (Rich Automation)
✅ **HTML upgrades** - In-place section injection  
✅ **Child spawning** - Cost/near-me/worth-it variants  
✅ **Internal linking** - Cross-reference new pages  
✅ **Sitemap updates** - Auto-append with metadata  
✅ **Index management** - "Fresh paths" section  
✅ **Queue system** - Track what's been processed  
✅ **GSC gold zone** - Filter for impressions 5+ at positions 4-30

## Usage

### Quick Start

```bash
# 1. Prepare GSC data
# Export from Google Search Console as CSV:
# Format: PAGE,QUERY,CLICKS,IMPRESSIONS,CTR,POSITION
# Save to: data/gsc.csv

# 2. Preview (safe):
DRY_RUN=1 ./swarm-v9-unified.sh

# 3. Review report:
cat docs/swarm/swarm-v9-report-YYYY-MM-DD-HHMMSS.md

# 4. Apply changes (manual review):
./swarm-v9-unified.sh
# Then review and commit manually

# 5. Auto-commit mode (use with caution):
AUTO_COMMIT=1 ./swarm-v9-unified.sh
```

### Configuration

Edit these variables in `swarm-v9-unified.sh`:

```bash
# Caps
MAX_UPGRADES=25        # In-place HTML upgrades
MAX_CHILDREN=15        # New child pages
MAX_REWRITES=10        # Title tag rewrites (not yet implemented)
MAX_SITEMAP=30         # Sitemap additions
MAX_INDEX=30           # Index additions

# Scoring thresholds
SCORE_HIGH=15.0        # High priority threshold
SCORE_MEDIUM=8.0       # Medium priority threshold
SCORE_LOW=5.0          # Low priority threshold

# GSC filtering
MIN_IMPRESSIONS=5      # Minimum impressions to consider
MIN_POSITION=4         # Best position to target
MAX_POSITION=30        # Worst position to target
```

### Input Format

**GSC CSV** can be in two formats:

Format 1 (Google Search Console export):
```csv
PAGE,QUERY,CLICKS,IMPRESSIONS,CTR,POSITION
https://example.com/page.html,search query,5,100,0.05,8
```

Format 2 (Alternative):
```csv
QUERY,CLICKS,IMPRESSIONS,CTR,POSITION,PAGE
search query,5,100,0.05,8,https://example.com/page.html
```

The script auto-detects format and processes accordingly.

### Fallback Mode

If `data/gsc.csv` is missing, the swarm falls back to **inventory scan mode**:
- Scans existing HTML files in project root
- Filters for keywords: hvac, solar, payment, repair, automation, ai, etc.
- Assigns estimated scores for priorit ization
- Processes top 30 matches

## Output & Reports

### Report Location
```
docs/swarm/swarm-v9-report-YYYY-MM-DD-HHMMSS.md
```

### Report Contents
1. **Configuration** - All caps and thresholds used
2. **Prechecks** - File validation results
3. **Signal Intelligence** - Total signals processed
4. **Top 25 Targets** - Prioritized query list
5. **Actions** - What was upgraded/created
6. **Summary Table** - Counts vs caps
7. **Recommendations** - Human review checklist
8. **Revert Instructions** - Exact commands to undo

### Log Location
```
docs/swarm-logs/swarm-v9-YYYY-MM-DD-HHMM.md
```

Legacy format appended for compatibility with v3 workflows.

## Safety Features

### 1. Dry-Run Mode
```bash
DRY_RUN=1 ./swarm-v9-unified.sh
```
- No files modified
- Full simulation of what would happen
- Report generated as if live
- Perfect for testing new GSC data

### 2. Automatic Backups
Every modified file gets backed up:
```
original-file.html -> original-file.html.bak.2026-03-24-220138
```

### 3. Revert All Changes
```bash
# From report's revert section
find /workspaces/sideguy-solutions -name "*.bak.2026-03-24-220138" \
  -exec bash -c 'mv "$0" "${0%.bak.2026-03-24-220138}"' {} \;

# Remove created children
rm {list-from-report}
```

### 4. Manual Review by Default
- No auto-commit unless `AUTO_COMMIT=1`
- Review changes before pushing
- Check report for recommendations

## Workflow Integration

### Daily Routine
1. Export fresh GSC data (weekly)
2. Run dry-run: `DRY_RUN=1 ./swarm-v9-unified.sh`
3. Review report in `docs/swarm/`
4. If satisfied, run live: `./swarm-v9-unified.sh`
5. Review generated pages - add real content
6. Test modifications locally
7. Commit: `git add . && git commit -m "swarm v9: applied intelligence"`

### Weekly Review
- Check `data/gsc.csv` for trend changes
- Review created child pages for content quality
- Monitor upgraded pages for engagement metrics
- Adjust caps/thresholds if needed

## Scoring Logic

### Formula
```
score = (impressions / 30) + (clicks * 5) + (ctr * 10)
```

### Why This Works
- **Impressions** indicate visibility (but don't over-weight)
- **Clicks** prove actual interest (5x multiplier)
- **CTR** shows relevance (10x multiplier - most important)

### Priority Buckets
- **HIGH**: score ≥ 15.0
- **MEDIUM**: score ≥ 8.0
- **LOW**: score < 8.0

### GSC Gold Zone Filter
Only processes queries that meet ALL criteria:
- Impressions ≥ 5 (has real traffic)
- Position 4-30 (not already winning, not too far down)

This focuses effort on **movable queries** with existing demand.

## Intent & Pattern Classification

### Intents (5 types)
- **money**: cost, price, how much, pricing, estimate
- **call**: urgent, emergency, who do i call, help me
- **compare**: vs, versus, best, which, should i
- **service**: near me, repair, install, fix, replace
- **info**: everything else

### Patterns (6 types)
- **cost**: pricing/money queries
- **vs**: comparison queries
- **best**: ranking/review queries
- **guide**: how-to/tutorial queries
- **local**: geographic queries
- **decision**: decision-framework queries

These drive child page generation and content strategies.

## Child Page Strategy

### Three Variants
Every high-scoring query gets three children:

1. **{query}-cost.html**
   - Cost guide and variables
   - Real-world factors
   - Budget expectations

2. **{query}-near-me.html**
   - Local context
   - Red flags to avoid
   - How to vet providers

3. **{query}-worth-it.html**
   - Decision framework
   - Repair vs replace logic
   - Clear next steps

### Why This Works
- Captures **full search intent spectrum**
- Each variant targets different user needs
- Internal links create **topic clusters**
- Sitemap organization signals topical authority

## Comparison: v8.1 vs v3 vs v9

| Feature | v8.1 | v3 Autopilot | v9 Unified |
|---------|------|--------------|------------|
| Dry-run mode | ✅ | ❌ | ✅ |
| Auto-backup | ✅ | ❌ | ✅ |
| Auto-commit | ❌ (flag) | ✅ | ❌ (flag) |
| Title rewrites | ✅ | ❌ | 🔜 Planned |
| HTML upgrades | ❌ | ✅ | ✅ |
| Child pages | Pattern-based | Suffix-based | Suffix-based |
| Sitemap updates | ❌ | ✅ | ✅ |
| Index updates | ❌ | ✅ | ✅ |
| Internal linking | ❌ | ✅ | ✅ |
| Scoring formula | Advanced | Basic | Advanced |
| Intent detection | 5 types | 3 types | 5 types |
| Pattern detection | 6 types | 3 types | 6 types |
| Reports | Markdown | Markdown | Markdown |
| GSC format support | 1 format | 1 format | 2 formats |
| Fallback mode | ❌ | ✅ | ✅ |

## Troubleshooting

### "No signals processed"
- Check GSC CSV format (header row required)
- Verify queries meet gold zone criteria (impressions ≥5, position 4-30)
- Try fallback mode by moving/renaming GSC file

### "Pages already exist"
- Child pages only created if missing
- Existing pages get upgrades instead
- Check report for "Exists:" messages

### "Git commit failed"
- May have no actual changes (all pages already upgraded)
- Check git status manually
- Review report to see what was skipped

### "Script hangs"
- Check GSC CSV is well-formed (no embedded commas)
- Verify awk is available (`which awk`)
- Use timeout: `timeout 60 ./swarm-v9-unified.sh`

## Future Enhancements

Ideas for v9.1+:
- [ ] Title tag rewrites (from v8.1)
- [ ] Expand on pattern (from v8.1 expand feature)
- [ ] Tool slot injection for money intent
- [ ] A/B testing framework
- [ ] LLM-generated content (with human review queue)
- [ ] GSC API integration (auto-fetch data)
- [ ] Engagement tracking (clicks/CTR post-upgrade)
- [ ] Smart throttling (don't upgrade same page twice in X days)

## Philosophy Alignment

### Human-First ✅
- Dry-run for preview
- Manual commit by default
- Comprehensive reports for review
- Revert instructions included

### Quality Over Quantity ✅
- Caps enforce limits
- Gold zone filtering
- Score-based prioritization
- Only process movable queries

### Transparency ✅
- Every action logged
- Full reasoning in reports
- Backup trail maintained
- Git history preserved

### Intelligent Assistance ✅
- Scoring combines visibility + engagement
- Intent detection drives content strategy
- Pattern matching enables smart expansions
- Queue system prevents double-work

---

**Swarm v9 is production-ready.** It combines the safety of v8.1 with the automation power of v3, while maintaining SideGuy's human-first philosophy throughout.

Run with confidence. Review with care. Deploy with intention.
