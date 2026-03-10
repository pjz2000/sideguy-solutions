# Claude: SideGuy 100k Expansion Engine

## Purpose
Generate high-quality static HTML pages at scale using the topic/city/industry manifests. Each batch produces ~650 clean pages ready for nav injection and sitemap update.

## When to Use This
PJ asks you to "run the expansion engine" or "build batch 001" or "generate the next wave of pages."

---

## Step-by-Step Workflow

### 1. Preview the batch size
```bash
bash tools/scale/plan-next-batches.sh
```
Confirm the numbers look right before generating.

### 2. Generate the pages
```bash
bash tools/scale/generate-100k-batch.sh
```
Creates ~650 pages at root level. All pages are idempotent — won't overwrite existing files.

### 3. Inject nav links into new pages
```bash
python3 tools/upgrades/inject-nav-links.py --run
```
Adds command center + knowledge hub navigation to any pages missing it.

### 4. Validate quality
```bash
bash tools/scale/validate-new-pages.sh
```
Check for missing meta, missing H1, missing Text PJ, missing canonical. All counts should be 0 or near-zero.

### 5. Rebuild sitemap
```bash
node update-sitemap.js
```
Regenerates `sitemap.xml` from all valid root HTML files.

### 6. Commit
```bash
git add -A
git commit -m "Build: 100k expansion batch 001"
```

---

## Key Files

| File | Purpose |
|---|---|
| `docs/manifests/scale-batches/batch-001-core-topics.txt` | Topic list (e.g., hvac-repair, ai-automation) |
| `docs/manifests/scale-batches/batch-001-cities.txt` | US city list for local variants |
| `docs/manifests/scale-batches/batch-001-industries.txt` | Industry verticals (medical, retail, etc.) |
| `tools/scale/generate-100k-batch.sh` | Batch generator |
| `tools/scale/validate-new-pages.sh` | Quality gate |
| `tools/scale/plan-next-batches.sh` | Batch size estimator |
| `docs/scale/sideguy-100k-plan.md` | Strategy overview |
| `docs/scale/expansion-model.md` | Naming and content model |

---

## Rules for Generated Pages

- **Inline CSS only** — no external stylesheets
- **Canonical tag** pointing to the page's own URL pattern
- **Meta description** unique to each page (~150 chars)
- **H1** matching the page topic and location
- **Text PJ orb** — `773-544-1231` on every page
- **Command center link** — `command-center-v2.html` in nav
- **No placeholders** — at minimum, content should be scannable and useful

---

## Expansion Philosophy

> SideGuy pages are calm guidance for stressed people. Each generated page should feel like a knowledgeable friend giving honest advice — not a sales pitch, not keyword soup.

When building topics, ask: "Would a real San Diego business owner find this helpful at 11pm when something broke?"

---

## Next Batch Customization

To expand topics, cities, or industries:
1. Edit the manifest files in `docs/manifests/scale-batches/`
2. Re-run `plan-next-batches.sh` to preview new size
3. Run `generate-100k-batch.sh`

Batch 002+ can use entirely different topic/city sets for maximum coverage.
