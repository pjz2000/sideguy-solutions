# SideGuy Index Health

Updated: 2026-03-07

## Current State

| Metric | Value |
|---|---|
| Pages in production | ~13,545 |
| Indexed by Google | ~1,420 |
| Index rate | ~10.5% |
| Stage | Discovery Phase |

## Recent Fixes (2026-03-07)

- `404.html` → noindex (was indexed, wasting crawl budget)
- `new-prolem-x.html` → noindex (placeholder with typo)
- `robots.txt` → added `sitemap-index.xml` (unlocks 14,408 additional URLs Google couldn't see)
- `sitemap.xml` → removed 3 noindex pages
- Created `crawl-map.html` — internal hub linking all major problem clusters
- Created `sideguy.html` — brand authority page with Organization schema

## Sitemap Coverage

| Sitemap | URLs | Submitted to GSC? |
|---|---|---|
| `sitemap.xml` | 10,104 | Yes (via robots.txt) |
| `sitemap-index.xml` (sitemaps 1–15) | 14,408 | Now yes (added to robots.txt 2026-03-07) |
| `sitemaps/priority-sitemap.xml` | 1,286 | Manual submit recommended |
| `sitemaps/deep-sitemap.xml` | 409 | Manual submit recommended |

## Goals

- [ ] 3,000 indexed pages
- [ ] CTR > 1% on top 10 ranking queries
- [ ] Brand query "sideguy" ranking #1 (currently position 8.5)
- [ ] Crawl rate increase after `sitemap-index.xml` discovery

## Next Actions

1. **GSC → Sitemaps:** manually submit `sitemap-index.xml` and `sitemaps/priority-sitemap.xml`  
2. Run `python3 tools/crawl-amplifier/link_boost.py --dry-run` to preview hub link additions (14 targeted pages only)
3. Monitor GSC Coverage report for uptick in "Discovered, not yet indexed" moving to "Indexed"
