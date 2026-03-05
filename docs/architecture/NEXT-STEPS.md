# Next Steps — SideGuy Pyramid-Tree Phase 2

Updated: 2026-03-05
Based on: 18,417 total pages | 3,465 mapped to 10 pillars | 29 cluster scaffolds defined

---

## Priority Queue (ranked by impact × readiness)

### 🔥 P1 — Wire Up-Links on Existing Leaves (HIGH IMPACT, ALL PILLARS)

**The single highest-ROI action.** Every existing leaf page needs:
- `Back to its pillar hub` link
- `Back to its cluster` link

**How:** Run a script that for each page in `data/pillar-leaf-map.json`:
1. Detects which pillar it belongs to
2. Injects a `<nav class="pyramid-nav">` block near the top
3. Injects a `Text PJ` CTA if missing

**Start with:** `ai-automation` (1,315 pages) → then `local-operator-tech` (1,229) → `payments` (326)

---

### 🔥 P2 — Build 3 Missing Pillar Hub Pages

These pillars have leaf pages but **no hub page yet**:

| Pillar | Leaves | Action |
|--------|--------|--------|
| `business-software` | 255 | Create `business-software-san-diego.html` |
| `energy-ev` | 24 | Create `energy-ev-san-diego.html` |
| `operator-tools` | 41 | Create `operator-tools-san-diego.html` |

Use `docs/architecture/generated/pillar-*.md` as content source.
Each hub must: list all clusters, sample 15–20 leaves, breadcrumb schema, Text PJ CTA.

---

### 🟡 P3 — Upgrade Existing Pillar Hubs

Existing hub pages need verification:

| Hub | Check |
|-----|-------|
| `hubs/category-ai-automation.html` | Lists all 8 clusters? Has breadcrumb schema? |
| `hubs/category-payments.html` | Lists all 8 clusters? Has breadcrumb schema? |
| `hubs/category-crypto-solana.html` | Lists 6 clusters? Has breadcrumb schema? |
| `electrical-problems-hub-san-diego.html` | Lists 7 home-systems clusters? |
| `authority/local-seo-hub.html` | Lists SD clusters? |

---

### 🟡 P4 — Build Cluster Pages (Phase 2B)

29 cluster scaffolds exist in `docs/architecture/generated/`.
Convert top-priority ones to real HTML pages:

**Start with:**
1. `cluster-payments-chargebacks` → highest pain point, high conversion
2. `cluster-home-systems-ac-problems` → high summer search demand
3. `cluster-payments-stripe-troubleshooting` → operators actively search this
4. `cluster-ai-automation-ai-automation-cost` → pre-purchase intent signal

**Format:** Same HTML pattern as leaf pages — inline CSS, Text PJ CTA, breadcrumb schema.

---

### 🟢 P5 — Assign Clusters to Unmapped Pages (532 pages)

`data/pillar-leaf-map.json → _unmapped` contains 532 root pages with no pillar assignment.
Audit these and assign pillar + cluster slugs so they can be wired.

---

### 🟢 P6 — GSC-Driven Cluster Expansion (Phase 3)

Once GSC data flows:
- Pages with impressions but low CTR → improve title + description
- Query clusters with no page → build cluster + leaf pages
- Thin cluster areas → add 20–50 more leaves

---

## File References

| File | Purpose |
|------|---------|
| `seo-manifests/pillars.json` | Canonical pillar manifest with leaf counts + cluster lists |
| `data/pillar-leaf-map.json` | Every root HTML file assigned to a pillar |
| `docs/architecture/generated/pillar-*.md` | Pillar hub content scaffolds (10 files) |
| `docs/architecture/generated/cluster-*.md` | Cluster content scaffolds (29 files) |
| `docs/snippets/linking-rules.md` | Linking rules paste block |
| `docs/architecture/sideguy-pyramid-tree.md` | This architecture (canonical) |

---

## Non-Negotiables (Every Page, Always)

- Calm, friendly tone — smart friend, not sales page
- Clear pyramid breadcrumb (ROOT → PILLAR → CLUSTER → LEAF)
- Text PJ CTA — human resolution layer
- Breadcrumb JSON-LD schema
