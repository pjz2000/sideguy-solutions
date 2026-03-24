# SideGuy Swarm Evolution: Which One to Use?

## TL;DR

**Use Swarm v9 Unified** - It's the best of both worlds.

## The Three Swarms

### Swarm v8.1 (Strategic Intelligence)
**File:** `swarm-v8.sh`  
**Purpose:** Title rewrites, pattern-based expansions, tool slots  
**Best for:** Strategic SEO moves with careful targeting

**Strengths:**
- Elite page prioritization (top 20)
- Pattern-based expansion (cost, vs, best, guide, local, decision)
- Tool slot injection for money pages
- Excellent scoring formula

**Limitations:**
- No HTML upgrades
- No sitemap/index management
- No child page generation

### Swarm v3 Autopilot (Rich Automation)
**File:** `swarm-v3-autopilot.sh` (paste into file if needed)  
**Purpose:** Daily autopilot for page upgrades and child generation  
**Best for:** Hands-off daily optimization

**Strengths:**
- In-place HTML upgrades (sections, CTAs, orbs)
- Child page generation (-cost, -near-me, -worth-it)
- Sitemap/index auto-updates
- Internal linking

**Limitations:**
- No dry-run mode
- Auto-commits everything
- Basic scoring
- No backups

### **Swarm v9 Unified** ⭐ RECOMMENDED
**File:** `swarm-v9-unified.sh`  
**Purpose:** Everything from v8.1 + v3 with full safety  
**Best for:** Production use with confidence

**Strengths:**
- ✅ All v3 automation features
- ✅ All v8.1 intelligence features
- ✅ Dry-run mode
- ✅ Auto-backups
- ✅ Manual review by default
- ✅ Comprehensive reports
- ✅ Revert instructions

**No limitations** - It's the complete package.

## Decision Matrix

| If you want... | Use... |
|----------------|--------|
| **Production-ready system** | Swarm v9 Unified |
| **Daily automation with safety** | Swarm v9 Unified |
| **Page upgrades + child generation** | Swarm v9 Unified |
| **Title rewrites only** | Swarm v8.1 |
| **Quick strategic moves** | Swarm v8.1 |
| **Truly hands-off autopilot** | Swarm v3 (not recommended) |

## Quick Start: Swarm v9

```bash
# 1. Prepare data
# Export GSC as CSV: PAGE,QUERY,CLICKS,IMPRESSIONS,CTR,POSITION
# Save to: data/gsc.csv

# 2. Preview
DRY_RUN=1 ./swarm-v9-unified.sh

# 3. Review report
cat docs/swarm/swarm-v9-report-*.md | tail -100

# 4. Apply
./swarm-v9-unified.sh

# 5. Review and commit
git status
git add .
git commit -m "swarm v9: applied intelligence"
```

## File Reference

| File | Status | Purpose |
|------|--------|---------|
| `swarm-v8.sh` | ✅ Improved | Strategic intelligence (v8.1) |
| `swarm-v9-unified.sh` | ✅ Production | Best of both worlds |
| `swarm-v9-help.sh` | ✅ Helper | Quick reference guide |
| `swarm-examples.sh` | ✅ Helper | v8.1 examples |
| `docs/swarm/README.md` | ✅ Docs | v8.1 documentation |
| `docs/swarm/README-v9-unified.md` | ✅ Docs | v9 complete guide |

## Migration Path

### From v3 → v9
1. Copy your `data/gsc.csv` (v9 auto-detects format)
2. Run `DRY_RUN=1 ./swarm-v9-unified.sh`
3. Compare with v3 behavior
4. Switch to v9 for production

### From v8.1 → v9
1. Use same `data/gsc-export.csv`
2. v9 includes all v8.1 scoring logic
3. Adds HTML upgrades + child generation
4. Same safety features you're used to

## What Got Committed

**Commit 1:** Swarm v8.1 improvements
- Enhanced v8 with safety features
- Comprehensive documentation
- Sample GSC data

**Commit 2:** Swarm v9 Unified
- Combined system (v8.1 + v3)
- Full documentation
- Quick reference guide
- Tested and validated

## Next Steps

1. **Read:** `docs/swarm/README-v9-unified.md`
2. **Test:** `DRY_RUN=1 ./swarm-v9-unified.sh`
3. **Review:** Check the report in `docs/swarm/`
4. **Deploy:** Run live when ready

## Philosophy Alignment

All three swarms align with SideGuy's principles, but **v9 does it best**:

- ✅ **Human-first:** Dry-run + manual review by default
- ✅ **Quality over quantity:** Caps on all actions
- ✅ **Transparency:** Comprehensive reports
- ✅ **Safety:** Backups + revert instructions
- ✅ **Intelligence:** Advanced scoring + intent detection

---

**You now have a production-ready swarm system that combines safety, intelligence, and automation.**

Run `./swarm-v9-help.sh` anytime for quick reference.
