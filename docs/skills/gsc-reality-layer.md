# Skill: GSC Reality Layer
**Version:** 1.0 · Append-only doctrine
**Purpose:** Turn GSC winner data into homepage query cards, CTR-optimized titles, and internal link equity — fast.

---

## Trigger Conditions
Run this skill when:
- New GSC export is available (download from Search Console → Performance → Export)
- Position of a known winner shifts ±2 spots
- A page breaks into top 10 for the first time
- Homepage trending cards are stale (>7 days since last update)

---

## Step 1 — Parse the Export

Drop the zip into `/Users/kromeon/Downloads/` and run:
```bash
unzip ~/Downloads/sideguysolutions.com-Performance-on-Search-*.zip -d ~/Downloads/gsc-latest/
```

Read `Queries.csv` and `Pages.csv`. Pull:
- Queries with impressions ≥ 1 sorted by position ascending
- Pages with impressions ≥ 1 sorted by impressions descending

**Key filters:**
- Position < 30 = active signal, worth tracking
- Position < 10 = on page 1, CTR optimization priority
- Position < 5 = crack zone, one title cycle away from clicks
- Impressions ≥ 5 = statistically meaningful

---

## Step 2 — Select Winners for gsc-winners.json

Winners = pages where position ≤ 30 AND impressions ≥ 1, sorted by:
1. Position (ascending — closest to page 1 first)
2. Impressions (descending — most eyes first as tiebreaker)

**Winner JSON schema:**
```json
{
  "query": "Exact query text from GSC (title-cased for display)",
  "description": "One sentence. Lead with the symptom. End with the resolution hint.",
  "page": "/relative/path/to/page.html",
  "impressions": 12,
  "position": 4.91,
  "pulled_date": "YYYY-MM-DD",
  "window_start": "YYYY-MM-DD"
}
```

**Description writing rules:**
- Match the search intent in the first 5 words
- Include the pain state ("timing out", "not delivering", "not retaining memory")
- End with a resolution signal ("exact fix", "ranked causes", "no paid tier required")
- 15–22 words max

---

## Step 3 — Update data/gsc-winners.json

Write the top 5–8 winners. Re-run:
```bash
python3 tools/homepage-builder/update_trending_cards.py
```

This rebuilds the `<!-- GSC_TRENDING_START -->` block in `index.html` automatically.

---

## Step 4 — Homepage Card Design Rules

Cards are rendered by `tools/homepage-builder/update_trending_cards.py` via `render_card()`.

**Card anatomy:**
```html
<a class="sg-tcard" href="/page-url.html">
  <span class="sg-tcard-pulse"></span>          <!-- live dot -->
  <div class="sg-tcard-query">{impr_label}</div> <!-- "12 impr" or "live now" -->
  <div class="sg-tcard-title">{query}</div>       <!-- exact query, title-cased -->
  <div class="sg-tcard-desc">{description}</div>  <!-- pain → resolution -->
  <div class="sg-tcard-cta">See how SideGuy solves this →</div>
</a>
```

**Rules:**
- Never change the card CTA text — "See how SideGuy solves this →" is the click trigger
- `impr_label` = impressions formatted as "1,840 impr" or "live now" if 0
- Keep description to one sentence — two is too long for the card
- Query text should match exactly what appeared in GSC (with light title-casing)

---

## Step 5 — CTR Title Patterns

When a page has impressions but 0 clicks, apply this sequence:

**Cycle 1 — Add year + pain signal:**
```
Before: Page Title About Topic
After:  Topic Pain State in 2026 — Root Cause + Fix
```

**Cycle 2 — Mirror exact query:**
```
Before: Topic Pain State in 2026 — Root Cause + Fix
After:  [Exact GSC Query] (2026): Why It Happens + Fast Fix
```

**Cycle 3 — Urgency + consequence:**
```
Before: [Exact GSC Query] (2026): Why It Happens + Fast Fix
After:  [Exact GSC Query] in 2026? Fix It Before [Consequence]
```

**Proven patterns:**
- `[Problem] in 2026? [Outcome Before Cost]` → highest CTR on pos 6–10
- `[Exact Query] (2026): Why It Happens + Fast Fix` → best for pos 3–6
- `[Exact Query] — Root Cause & Exact Fix` → clean, works on pos 1–3

**Always update together:** `<title>`, `<meta name="description">`, H1, `og:title`, `og:description`

**Meta description formula:**
`[Symptom in searcher's words]? [Root cause in one clause]. [Resolution signal]. [Differentiator: no paid tier / no rebuild / no vendor runaround]`

---

## Step 6 — Internal Linking Rules

Every winner page should have:
1. One internal link FROM the homepage trending cards (auto, via update_trending_cards.py)
2. One internal link FROM a related hub page (`/hubs/`, `/clusters/`, or `/authority/`)
3. One internal link TO a deeper problem page or decision page

**Priority linking targets:**
- Winner pages at position 5–10 need internal link equity most — a link from the homepage or a hub can close the gap
- Position 1–4 pages: already ranking, don't over-link — focus on CTR instead
- New pages (no impressions yet): link from 2+ existing indexed pages before expecting ranking

---

## Step 7 — Local Trust Modifiers

For any query where local intent is possible, add a local modifier to title/description:

**Modifiers by priority:**
1. "San Diego" — broadest, highest search volume
2. "North County San Diego" — trust signal for Solana Beach / Encinitas / Del Mar
3. "Solana Beach" / "Encinitas" — hyper-local, lower volume, higher trust conversion

**Rule:** Only add local modifier if the page content actually serves local intent. Don't stuff a technical Zapier fix page with "San Diego" — it dilutes relevance.

---

## Step 8 — New Page vs Link Existing

**Create a new page when:**
- Query has 3+ impressions at position 1–30 and no existing page matches it within 80% topic overlap
- Query cluster has 5+ related queries with no hub page covering them
- Local variant exists with clear geo intent and no local page exists

**Link to existing when:**
- Query is a near-synonym of an existing page title
- Position is already < 10 — ranking is working, CTR fix beats new page
- The existing page just needs a title refresh to capture the query

---

## Execution Checklist

```
[ ] Download GSC export
[ ] Parse Queries.csv + Pages.csv
[ ] Select top winners (pos < 30, impr ≥ 1)
[ ] Update data/gsc-winners.json
[ ] Run update_trending_cards.py
[ ] Run title surgery on pos 5–15 pages with 0 CTR
[ ] Run page1-watchtower.sh to log scan
[ ] Run crawl-velocity-check.sh to confirm freshness
[ ] Bump homepage version + timestamp
[ ] Commit: feat: gsc reality layer pass — [date]
[ ] Push
```
