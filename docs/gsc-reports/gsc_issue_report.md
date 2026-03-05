# GSC Issue Report — March 5, 2026

Source: `routing/Critical issues.csv`

| Priority | Reason | Source | Pages | Action |
|---|---|---|---:|---|
| 🟠 Already fixed (verify) | Duplicate without user-selected canonical | Website | 90 | Verify <link rel='canonical'> points to the correct self-URL on every duplicate (fixer already ran: 3,457 fixed) |
| 🔴 Fix now | Not found (404) | Website | 86 | Export URL list from GSC → Pages (filter Not found) and create redirects or restore pages |
| 🟢 Monitor | Alternate page with proper canonical tag | Website | 13 | Expected behaviour — page correctly defers to its canonical; no action needed |
| 🔴 Fix now | Soft 404 | Website | 4 | Find pages returning HTTP 200 with thin/empty content → add real content or return a proper 404 |
| 🟢 Monitor | Page with redirect | Website | 3 | Update internal links pointing to these URLs to use the final destination directly |
| 🔴 Fix now | Redirect error | Website | 1 | Check redirect chain for loops or broken targets |
| 🟢 Monitor | Discovered - currently not indexed | Google systems | 1280 | Waiting on Google crawl — resubmit sitemap.xml in GSC → Sitemaps to accelerate |
| 🟡 Review quality | Crawled - currently not indexed | Google systems | 57 | Review page quality: thin content, no internal links, or blocked by robots? Add value or consolidate |

**Total affected pages: 1,534**

---

## Recommended fix order

1. **404s (86 pages)** — Export the specific URLs from GSC and restore or redirect
2. **Soft 404s (4 pages)** — Add real content or return proper 404 status
3. **Redirect error (1 page)** — Find and break the redirect loop
4. **Duplicate canonical (90 pages)** — Already fixed by `tools/coverage-fixer/gsc_coverage_fixer.py`
5. **Discovered not indexed (1,280 pages)** — Resubmit sitemap; wait 2–4 weeks
