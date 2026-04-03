# Crawl Velocity Telemetry
**Site:** sideguysolutions.com
**Initialized:** 2026-04-03 · GSC layer v19
**Purpose:** Track daily commit velocity, page freshness signals, and estimated Google recrawl cycle compression.

---

## How Crawl Velocity Works Here

Every commit to a winner page or `index.html` sends a freshness signal to Googlebot via:
1. GitHub Pages `Last-Modified` HTTP header (auto-updated on push)
2. Sitemap `<lastmod>` tags (manual — update after winner loop runs)
3. GSC impressions confirming Google has already found the URL
4. Internal link equity from homepage trending cards → winner pages

The goal: compress Google's recrawl cycle from weeks → days by maintaining consistent daily activity on high-signal URLs.

---

## Crawl Velocity Log

### 2026-04-03

| Signal | Detail |
|---|---|
| **Homepage modified** | 6× (v14 → v19) |
| **Winner pages refreshed** | 3 (Twilio, Zapier, n8n) — title + meta + H1 + og + schema |
| **GSC winner loop runs** | 2 (gsc-winners.json written twice, trending cards rebuilt twice) |
| **Sitemap lastmod updated** | Pending — run crawl-velocity-check.sh to flag stale entries |
| **Homepage trending cards** | 5 live cards pointing to winner URLs |
| **Commits pushing freshness** | 9 commits since 2026-04-01 touching content files |
| **Estimated recrawl shrinkage** | ~40–60% — daily commits on known-indexed URLs typically compress crawl interval from 14–21 days to 3–7 days |

---

## Winner Page Freshness Status

| Page | Last Modified | GSC Position | Impressions | Homepage Card | Recrawl Likely |
|---|---|---|---|---|---|
| /problems/quick-fix-for-zapier-task-failed-webhook-timeout.html | 2026-04-03 | 4.91 | 12 | ✅ | ✅ High |
| /problems/twilio-sms-not-delivering-in-2026.html | 2026-04-03 | 8.77 | 26 | ✅ | ✅ High |
| /problems/n8n-ai-agent-memory-not-working.html | 2026-04-03 | 2.0 | 4 | ✅ | ✅ High |
| /decisions/stripe-vs-solana-payments.html | Not yet refreshed | 1.0 | 2 | ✅ | Medium |
| /ai-chatbot-for-drywall-contractors-san-diego.html | Not yet refreshed | 28.4 | 5 | ✅ | Medium |
| /index.html | 2026-04-03 | — | — | — | ✅ High (daily changes) |

---

## Sitemap Freshness

| Sitemap | Location | Last Checked | Status |
|---|---|---|---|
| sitemap.xml | /sitemap.xml | 2026-04-03 | Verify lastmod dates |
| sitemap-longtail.xml | /sitemap-longtail.xml | 2026-04-03 | Verify lastmod dates |
| sitemap-index.xml | /sitemap-index.xml | 2026-04-03 | Verify lastmod dates |
| public/sitemap.xml | /public/sitemap.xml | 2026-04-03 | Verify lastmod dates |
| public/sitemap-money.xml | /public/sitemap-money.xml | 2026-04-03 | Verify lastmod dates |

**Action:** After each winner loop run, update `<lastmod>` on modified winner URLs in `sitemap.xml` and `public/sitemap-money.xml`.

---

## Recrawl Attractors

Pages most likely to be recrawled next by Googlebot:

1. **index.html** — modified 6× this session, homepage = highest crawl priority
2. **zapier-webhook-timeout.html** — pos 4.91, already indexed, title changed, homepage card live
3. **twilio-sms-not-delivering.html** — pos 8.77, 26 impressions, title changed, homepage card live
4. **n8n-ai-agent-memory.html** — pos 2.0, title + schema + og all changed today
5. **stripe-vs-solana-payments.html** — pos 1.0, homepage card live, not yet title-refreshed

---

## Estimated Recrawl Cycle

| Condition | Estimated Cycle |
|---|---|
| No changes, no impressions | 21–30 days |
| Indexed, no recent changes | 14–21 days |
| Indexed + impressions, no changes | 7–14 days |
| Indexed + impressions + title changed | 3–7 days |
| Indexed + impressions + title + homepage card + daily commits | **1–3 days** |

Current site velocity places winner pages in the **1–3 day** recrawl band.

---

## Daily Checklist

```
[ ] Run: tools/seo/crawl-velocity-check.sh
[ ] Check git log for files modified today
[ ] Verify homepage trending cards reflect today's winners
[ ] Update sitemap <lastmod> for any refreshed winner pages
[ ] Append scan entry to this file
```

---

## Change Log

| Date | Action | Freshness Impact |
|---|---|---|
| 2026-04-03 | 9 commits — homepage v14→v19, 3 winner pages title-refreshed | High — daily crawl band activated |
| 2026-04-03 | gsc-winners.json created, trending cards rebuilt ×2 | Homepage freshness signal reinforced |
| 2026-04-03 | page1-watchtower.sh initialized | Monitoring layer active |

---

## Crawl Velocity Scan — 2026-04-03 10:22 PDT

- **Commits today:** 9
- **HTML files modified:** 4
- **Winner feed entries:** 5

**Modified today:**
- index.html
- problems/n8n-ai-agent-memory-not-working.html
- problems/quick-fix-for-zapier-task-failed-webhook-timeout.html
- problems/twilio-sms-not-delivering-in-2026.html

**Winner feed positions:**
| Query | Position | Impressions |
|---|---|---|
| Stripe vs Solana Payments | 1.0 | 2 |
| n8n AI Agent Memory Not Working | 2.0 | 4 |
| Zapier Webhook Timeout (2026) | 4.91 | 12 |
| Twilio SMS Not Delivering in 2026? | 8.77 | 26 |
| AI Chatbot for Drywall Contractors | 28.4 | 5 |

