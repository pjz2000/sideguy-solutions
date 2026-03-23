# SideGuy Clarity Layer Batch Upgrader

Safe, human-approved deployment of clarity layer content to high-intent pages.

## What It Does

- **Reads the decision report** (`docs/decision-report.md`) to identify best candidates
- **Generates real clarity-layer content** (not thin boilerplate) with:
  - Hero hook with immediate CTA
  - "What people are really asking" section
  - Quick answer tailored to the page topic
  - "You might need this if" / "You probably don't if" sections
  - Vertical-specific FAQs (HVAC, solar, payments, plumbing, etc.)
  - Multiple Text PJ CTAs throughout
- **Requires human approval** before each batch (unless `-y` flag used)
- **Tracks progress** in append-only state files

## Usage

### Check Status
```bash
python3 _ship027_batch_upgrade.py --status
```

### Preview Next Batch (Default: 5 Pages)
```bash
python3 _ship027_batch_upgrade.py
```
Shows preview, prompts for confirmation. Press `y` to proceed, `N` to cancel.

### Run Batch with Custom Size
```bash
python3 _ship027_batch_upgrade.py -n 10
```
Preview 10 pages, ask for approval.

### Auto-Approve (No Confirmation)
```bash
python3 _ship027_batch_upgrade.py -n 5 -y
```
**Use carefully** — skips human confirmation.

### Sync Existing Clarity Pages
```bash
python3 _ship027_batch_upgrade.py --sync
```
Scans all HTML files, adds already-upgraded pages to done list.

## File Structure

```
swarm/
├── state/
│   ├── clarity-done.txt       # Append-only list of upgraded slugs
│   └── clarity-log.txt         # Timestamped event log
├── queue/
│   └── clarity-queue.txt       # Reserved for future queue management
└── reports/
    └── (future batch reports)
```

## How It Works

1. **Reads decision report** → Extracts Tier 1 candidates (score 8+)
2. **Filters already-done pages** → Uses `clarity-done.txt` to avoid duplicates
3. **Scores remaining pages** → Sorts by intent score, picks top N
4. **Generates clarity content per page:**
   - Detects vertical from slug keywords (hvac/solar/payments/plumbing/etc.)
   - Extracts title from `<title>` tag (or generates from slug if mismatched)
   - Creates vertical-specific FAQs and decision guidance
   - Injects into `<main>` section while preserving all other page elements
5. **Writes to file** → Replaces `<main>` content only
6. **Marks done** → Appends slug to `clarity-done.txt`
7. **Logs** → Timestamps all actions to `clarity-log.txt`

## Safety Features

- **Read-only decision report** → Never modifies source data
- **Human approval gates** → Must confirm each batch (unless `-y`)
- **Idempotent** → Won't re-process pages already marked done
- **Preserves page structure** → Only replaces `<main>` content, keeps head/CSS/footer/sidebars
- **No cloning** → Never duplicates pages, only upgrades existing ones
- **Smart title detection** → Handles template issues where titles don't match filenames

## Content Intelligence

### Vertical Detection
Analyzes page slug for keywords to determine vertical:
- **HVAC**: hvac, ac-, furnace, heater, cooling, heating
- **Solar**: solar, panel, energy, electric-bill
- **Payments**: stripe, payment, processor, fees
- **Plumbing**: plumb, pipe, drain, water, leak
- **Electrical**: electric, wiring, circuit, breaker

### Vertical-Specific FAQs
Each vertical gets 3 tailored FAQ answers:
- **HVAC**: repair vs replace, pricing, DIY limits
- **Solar**: ROI, tax credits, avoiding overselling
- **Payments**: fee benchmarks, Stripe alternatives, negotiation
- **Plumbing**: emergency vs wait, pricing, ripoff detection
- **Generic fallback** for other topics

## Current Status

**18 pages upgraded** (as of last run):
- 15 manually curated (high-value HVAC, payments, decision pages)
- 3 batch-upgraded (processing fee reduction pages)

**339 Tier 1 candidates remaining** in decision report.

## Recommended Workflow

1. **Run decision report** weekly:
   ```bash
   python3 _decision_report.py
   ```

2. **Review Tier 1 list** in `docs/decision-report.md`

3. **Run small batches** (5-10 pages):
   ```bash
   python3 _ship027_batch_upgrade.py -n 10
   ```

4. **Spot-check output** after each batch:
   ```bash
   git diff | head -200
   ```

5. **Commit if good**, revert if bad:
   ```bash
   git add -A && git commit -m "Clarity layer: batch 2 (10 pages)"
   # OR
   git checkout -- *.html
   ```

## What This Is NOT

- ❌ **Not a page generator** → Only upgrades existing pages
- ❌ **Not automation** → Requires human approval per batch
- ❌ **Not thin content** → Real FAQs, real guidance, vertical-specific
- ❌ **Not duplicate content** → No cloning, no suffix modifiers

## Philosophy Alignment

Follows SideGuy core principles:
- **Human-first clarity** → Real answers, not SEO spam
- **Transparency** → Append-only logs, clear state tracking
- **Manual control** → Batch limits, approval gates, no daemon mode
- **Quality over quantity** → Targets high-intent pages, skips low-signal noise

---

**Questions?** Text PJ: 773-544-1231
