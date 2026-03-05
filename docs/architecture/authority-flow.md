# SideGuy Authority Flow
Generated: 2026-03-05 17:15:52

## How ranking gravity works in this system

```
External backlinks land on pillar pages (highest authority nodes)
    ↓
Pillar pages distribute authority to clusters via internal links
    ↓
Clusters distribute authority to leaf pages
    ↓
Leaf pages link back to clusters and pillars (closing the loop)
    ↓
Google sees dense topical authority → entire pillar ranks better
```

---

## Authority Distribution Rules

### Pillar pages (10 pages)
- Receive the most inbound internal links
- Link out to all clusters in their domain
- Feature top 15–20 leaf pages
- Target: highest organic impressions / topical authority signals

### Cluster pages (61 defined)
- Receive links from all leaves in their cluster
- Link up to their pillar
- Link sideways to 3–8 related clusters
- Target: mid-funnel queries (2–4 word searches)

### Leaf pages (18,417+)
- Receive 0–5 inbound internal links (from cluster pages)
- Link up to cluster + pillar (mandatory)
- Link sideways to 2–5 related leaves
- Target: long-tail queries (5–10 word searches)

---

## Current Authority Injection Status

| System | Pages affected | Status |
|--------|---------------|--------|
| Pyramid nav (`sideguy-authority-links`) | 3,461 root pages | ✅ Complete |
| Intelligence network (orphan rescue) | 532 unmapped pages | ✅ Complete |
| Cluster chips on hub pages | 10 pillar hubs | ✅ Complete |
| Breadcrumb JSON-LD | 10 pillar hubs | ✅ Complete |

---

## Refresh Cycle
Re-run `data/pillar-leaf-map.json` generation monthly.
New pages auto-injected on next authority-link-engine pass.
Engine is idempotent — safe to re-run.
