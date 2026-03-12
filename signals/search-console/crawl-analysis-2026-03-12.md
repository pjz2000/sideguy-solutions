# Crawl Coverage Analysis — March 12, 2026
Source: Google Search Console crawl export (999 URLs, all last crawled 2026-03-09)

---

## Summary Numbers

| Metric | Count |
|---|---|
| HTML pages on disk (total) | 51,543 |
| Root-level pages | 34,294 |
| Pages in sitemap.xml | 42,412 |
| Pages Google has crawled (CSV) | 1,000 |
| Root pages crawled | 986 |
| **Root crawl coverage** | **2.88%** |

Google has crawled fewer than 3% of root pages. The sitemap has 42,412 URLs but only 1,000 have been reached — 2.4% coverage.

---

## What Google IS Crawling (Crawl Preference Signal)

| Page Series | Crawled | On Disk | % |
|---|---|---|---|
| 150-customer-messages-... | 573 | 1,200 | 47.7% |
| anyone-using-premium-irish-hampers-... | 125 | 1,200 | 10.4% |
| are-small-businesses-... | 99 | 1,420 | 7.0% |
| almost-30-left-my-job-... | 71 | 1,420 | 5.0% |
| anyone-use-a-one-stop-shop-... | 71 | 980 | 7.2% |
| a-seller-on-our-marketplace-... | 28 | 1,420 | 2.0% |
| 1-year-into-my-business-... | 2 | 1,420 | 0.1% |
| ai-automation-for-... | 2 | 2,422 | 0.1% |

**Takeaway:** The "150-customer-messages" story series is getting the bulk of crawl attention (573 pages). The AI service pages (ai-automation-for, ai-booking-software, etc.) are nearly invisible — only 1-2 crawled per series despite being the commercial core.

---

## Critical Issue: Exposed Backup Directories

**8 backup directories are NOT blocked by robots.txt** and contain ~2,900 pages of duplicate content that could dilute crawl budget and cause duplicate content penalties:

| Directory | Pages | Status Before Fix |
|---|---|---|
| /backups_20251230_191613/ | 1,641 | EXPOSED |
| /backup_pages/ | 1,105 | EXPOSED |
| /_quarantine_backups/ | 93 | EXPOSED |
| /backup_old_pages/ | 62 | EXPOSED |
| /backup-who-do-i-call-20251229-1838/ | 10 | EXPOSED |
| /sideguy-backups/ | 2 | EXPOSED |
| /_BACKUPS/ | 2 | EXPOSED |
| /_layout_backups/ | 1 | EXPOSED |

**ACTION TAKEN (2026-03-12):** All 8 directories added to robots.txt Disallow rules.

---

## Root Cause of Low Crawl Coverage

1. **34,294 root pages with minimal internal linking** — Google's crawler needs links to discover pages. With flat structure and no hub pages linking out to most content, Googlebot cannot find most pages even if sitemap is submitted.

2. **Crawl budget spread too thin** — 42,412 URLs submitted in sitemap. Google crawls ~1,000/crawl cycle. At this rate, full coverage would take ~42 crawl cycles.

3. **Near-duplicate page series** — Many series have 1,200-2,422 nearly identical pages with just industry/city swaps. This may suppress crawl priority as Google deduplicates.

4. **AI service pages not getting crawled** — The commercial pages (ai-automation, ai-booking-software, ai-dispatch-software, etc.) have only 1-2 crawled per series. These need link equity from higher-authority pages.

---

## Recommended Actions (for PJ review)

### Immediate (done)
- [x] Block 8 exposed backup directories in robots.txt

### Short-term
- [ ] Add internal linking from crawled/trusted pages to AI service pages — especially from the "150-customer-messages" series (573 crawled) pointing to relevant ai-automation pages
- [ ] Consider reducing sitemap to highest-quality pages only (hubs, core service pages, ai-* pages) to concentrate crawl budget
- [ ] Verify sidemap-index.xml is not including backup/noise dirs

### Observation
- The "150-customer-messages" series is Google's entry point right now. Whatever is linking to those pages is working. Identify the source and replicate for commercial pages.
