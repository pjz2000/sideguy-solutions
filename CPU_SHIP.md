# CPU SHIP QUEUE — SideGuy

Law: No discussion without output.  
Each item must result in a file.

---

SHIP-001  
Source: CPU_INBOX.md  
Status: READY

---

SHIP-002  
Source: authority-hardening-20260223.sh  
Status: COMPLETED — 2026-02-23  
Commits: metadata-hardening-pass | hub-quality-pass | cluster-hub-linking-pass | quote-review-expansion

Results:
- Metadata: 1 generic title fixed (sideguy-placeholder.html)
- Hubs upgraded: tech-help, home-repair, north-county (added FAQ, How It Works, Pricing, 7+ FAQ items each)
- Cluster backlinks: 375 pages injected with parent-hub link (349 already had one, 271 unmatched topic)
- Quote-review pages created: HVAC, Plumbing, Electrical, Solar, Roofing (5 pages)
- Sitemap: 5 new URLs appended

---

## GPT INSTRUCTIONS — AUTHORITY HARDENING (For Future Sessions)

Paste this block into Claude/Copilot when resuming authority hardening work.

---

You are working directly in the SideGuy Solutions repo. We are in "AUTHORITY HARDENING — DO IT ALL" mode.

STRICT RULES:
- NO refactors.
- NO reordering of existing index/sitemap entries.
- NO deleting content.
- Prefer append-only improvements and targeted replacements.
- Make progress visible via commits after each step (4 commits total).
- Keep changes minimal but high-impact.
- Preserve existing styling and structure unless explicitly upgrading a hub section.
- Ensure every changed file still validates as HTML and retains a `<title>`, meta description, and H1.

TARGET DIRECTORIES:
- Primary pages live at repo root (flat structure, 1,700+ .html files)
- Sitemaps: sitemap.xml at repo root
- Index: index.html at repo root
- Hub pages follow pattern: `[topic]-hub-san-diego.html` or `[topic]-problems-hub-san-diego.html`

EXECUTE IN THIS EXACT ORDER:

============================================================
STEP 1 — METADATA CLEANUP (GENERIC TITLES / DESCRIPTIONS)
============================================================
Goal: fix all pages flagged as generic title OR missing title.
Actions:
1) Find all HTML pages at root with missing or generic `<title>` (Untitled, Document, Home, Page, New Page, Template, Lorem Ipsum, "Sideguy")
2) For each flagged page:
   - Set `<title>` to: "[Primary Intent Keyword] in San Diego | SideGuy Solutions"
   - Set meta description: clear 150–165 char intent description (Clarity-before-cost tone)
   - Ensure H1 matches page intent and location
3) Do NOT change body content in this step except if H1 is missing or clearly generic.
Commit message: "metadata-hardening-pass"

============================================================
STEP 2 — HUB QUALITY UPGRADE (MAKE THIN HUBS MATCH BEST HUB)
============================================================
Current hub inventory (root level):
- hvac-problems-hub-san-diego.html
- plumbing-problems-hub-san-diego.html
- electrical-problems-hub-san-diego.html
- roofing-hub-san-diego.html
- contractor-services-hub-san-diego.html
- home-repair-hub-san-diego.html
- tech-help-hub-san-diego.html
- software-development-hub-san-diego.html
- payment-processing-hub-san-diego.html
- seo-hub-san-diego.html
- solar-hub-san-diego.html
- ai-automation-san-diego-hub.html
- north-county-help-hub.html

For EACH hub that is thin (< 1,500 words OR missing FAQ OR missing How It Works), upgrade to contract-page quality ensuring:
- Strong opening paragraph (calm, clarity-before-cost, human-layer positioning)
- Scannable "What we help with" bullet list (8–14 bullets)
- "How it works" section (3–5 steps)
- "What it costs" / pricing philosophy block
- FAQ section (6–10 questions with `<details>` tags)
- Internal links: Popular pages section linking to 10+ relevant cluster pages
- Strong CTA block with Text PJ (773-544-1231 / sms:+17735441231)

Do NOT change site-wide nav/footer patterns.
Commit message: "hub-quality-pass"

============================================================
STEP 3 — CLUSTER → HUB BACKLINK ENFORCEMENT (POWER GRID)
============================================================
Goal: every cluster page links back to its parent hub near the top.
Rules:
- Add exactly ONE contextual link near top of content (after first `</p>` in body).
- Avoid duplicates: if a link to any hub already exists anywhere, skip.
- Do NOT add sitewide nav changes.
- Keep anchor text natural.

Parent hub routing (filename keyword → hub file):
- "north-county" → north-county-help-hub.html
- "hvac", "ac-", "-ac-", "heating", "furnace", "thermostat", "heat-pump", "mini-split" → hvac-problems-hub-san-diego.html
- "plumb", "toilet", "faucet", "drain", "pipe", "sewer", "water-heater", "leak", "shower", "sink" → plumbing-problems-hub-san-diego.html
- "electr", "outlet", "breaker", "panel-", "wiring", "circuit", "generator", "ev-charg" → electrical-problems-hub-san-diego.html
- "roof", "shingle", "gutter", "flashing", "skylight" → roofing-hub-san-diego.html
- "solar", "photovoltaic" → solar-hub-san-diego.html
- "payment", "merchant", "invoice", "billing", "crypto", "accounting", "pos-" → payment-processing-hub-san-diego.html
- "seo", "search-engine", "google-ranking", "keyword", "backlink" → seo-hub-san-diego.html
- "ai-", "automation", "chatgpt", "agentic", "agent-" → ai-automation-san-diego-hub.html
- "software", "app-dev", "web-dev", "website-", "developer", "saas-", "mobile-app" → software-development-hub-san-diego.html
- "contractor", "remodel", "renovation", "foundation", "adu-", "deck-", "drywall", "flooring" → contractor-services-hub-san-diego.html
- "wifi", "internet-", "computer-", "printer", "tech-help", "laptop" → tech-help-hub-san-diego.html
- "home-repair", "window-", "door-", "garage", "pest-", "mold-", "insulation" → home-repair-hub-san-diego.html

Inject format (after first `</p>` in `<body>`):
```html
<p style="margin:8px 0 24px;font-size:14px;color:var(--muted,#3f6173)">
  &#x2190; <a href="{hub}" style="color:inherit;text-decoration:underline">{label}</a> &mdash; more San Diego guidance
</p>
```
Commit message: "cluster-hub-linking-pass"

============================================================
STEP 4 — HIGH-INTENT "QUOTE REVIEW" PAGE EXPANSION (MONEY PAGES)
============================================================
Pattern: [trade]-project-quote-review-san-diego.html

Already created (Feb 2026):
- hvac-project-quote-review-san-diego.html ✅
- plumbing-project-quote-review-san-diego.html ✅
- electrical-project-quote-review-san-diego.html ✅
- solar-project-quote-review-san-diego.html ✅
- roofing-project-quote-review-san-diego.html ✅

Next candidates to create:
- contractor-project-quote-review-san-diego.html (general contractor / remodel quotes)
- adu-project-quote-review-san-diego.html (ADU build quotes — high value San Diego)
- foundation-quote-review-san-diego.html
- landscaping-quote-review-san-diego.html
- painting-project-quote-review-san-diego.html

Each page must include:
- Title + meta description + H1 aligned to intent
- "Send me your quote" framing (clarity before cost)
- Checklist of what a quote should include (10–14 items)
- Red flags section (8–10 items)
- How SideGuy reviews it (process steps)
- FAQ section (6+ questions with `<details>` tags)
- CTA with Text PJ (sms:+17735441231)
- Floating Text PJ button
- Link back to parent hub
- JSON-LD LocalBusiness schema

Add new pages to sitemap.xml (append-only before `</urlset>`).
Commit message: "quote-review-expansion"

============================================================
SANITY CHECK (RUN AFTER STEP 4)
============================================================
```python
import re
from pathlib import Path
BASE = Path("/workspaces/sideguy-solutions")
missing_title = [f.name for f in BASE.glob("*.html")
                 if not re.search(r'<title>[^<]{10,}</title>', f.read_text(errors="ignore"), re.I)]
print(f"Pages missing real title: {len(missing_title)}")
for f in missing_title[:10]: print(f" {f}")
```

---

## SHIP-003 — INVENTORY SHARPEN PASS ✅ (COMPLETED 2025-01)

**Objective:** Create the 5 top Search Console impression pages that were missing from the repo.  
All 5 pages created at exact slugs, with pricing tables, comparison, switch-trigger bullets, CTA, FAQ, JSON-LD.

### Target Pages Created
| Slug | Bytes | Hub Link |
|------|-------|----------|
| `mobile-payment-systems-san-diego.html` | 11,566 | payment-processing-hub |
| `ai-business-solutions-san-diego.html` | 12,148 | ai-agent-automation |
| `payment-processing-solutions-san-diego.html` | 11,759 | payment-processing-hub |
| `electronic-payment-solutions-san-diego.html` | 12,004 | payment-processing-hub |
| `battery-backup-installation-san-diego.html` | 12,959 | solar-battery-backup-install |

### Each Page Includes
- Title + unique meta description + H1 aligned to search intent
- Side-by-side comparison table (providers / system options)
- Pricing section (what you should realistically pay)
- "When should you switch?" bullet list
- Mid-page CTA (Text PJ — 773-544-1231, sms:+17735441231)
- 6-question FAQ with `<details>` accordion
- JSON-LD LocalBusiness + FAQPage schema
- Floating Text PJ button
- Hub backlink in breadcrumb area

### Phone Number Canonical
**Always use:** `sms:+17735441231` / `773-544-1231` (NOT +17604541860)

### Sitemap After SHIP-003
1,769 URLs in `sitemap.xml`

### Commit Message Used
`SHIP-003: Inventory Sharpen Pass — 5 top impression pages created`

---

## SHIP-004 CANDIDATES (NEXT)

1. **Additional quote-review pages** — contractor, ADU, foundation, landscaping, painting  
   Pattern: copy `hvac-project-quote-review-san-diego.html`, adapt checklist + red flags
2. **Top-20 Search Console impressions** — pull next batch of pages with impressions but no clicks, create at exact slugs
3. **Hub word-count pass** — check remaining hubs against 2,000w target (payment-processing-hub, ai-automation hub)
4. **Internal linking pass #2** — newly created pages need incoming links from cluster pages
```python
import re
from pathlib import Path
BASE = Path("/workspaces/sideguy-solutions")
missing_title = [f.name for f in BASE.glob("*.html")
                 if not re.search(r'<title>[^<]{10,}</title>', f.read_text(errors="ignore"), re.I)]
print(f"Pages missing real title: {len(missing_title)}")
for f in missing_title[:10]: print(f" {f}")
```

