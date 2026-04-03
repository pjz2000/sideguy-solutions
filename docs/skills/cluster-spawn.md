# Skill: Cluster Spawn
**Version:** 1.0 · Append-only doctrine
**Purpose:** Turn GSC query signals into cluster children, hub pages, and long-tail geo expansions — systematically, without over-building.

---

## The Model: Hub → Cluster → Leaf

```
Hub page (1)
├── Cluster child A (problem variant)
├── Cluster child B (comparison)
├── Cluster child C (cost guide)
├── Cluster child D (local geo)
└── Cluster child E (FAQ)
```

**Hub** = high-level authority page covering a vertical or problem category
**Cluster child** = one specific angle, query, or intent under that hub
**Leaf** = ultra-specific page (single question, single city, single tool)

---

## Step 1 — Query → Cluster Signal

A cluster spawn is triggered when GSC shows:
- 3+ related queries all pointing to the same hub page but at position 15–50
- A hub page with 10+ impressions but no children covering the specific queries
- A new query cluster emerging (3+ queries with same root term, none ranked < 20)

**Example signal:**
```
"zapier webhook timeout issue 2026"      pos 4.91   → already has page
"zapier webhook not firing"              pos 22      → no page → spawn
"zapier webhook delay too long"          pos 31      → no page → spawn
"zapier task failed webhook limit"       pos 44      → no page → spawn
```
→ These three spawn a `zapier-webhooks` cluster hub + 3 leaf pages.

---

## Step 2 — Hub Page Rules

A hub page is worth building when:
- 5+ distinct queries share the same root intent
- The root intent maps to a SideGuy vertical (payments, AI automation, HVAC, local SD, future tech)
- No existing page covers it at position < 30

**Hub page structure:**
```
/hubs/[vertical]-[topic].html
  H1: [Topic] — SideGuy Clarity Hub
  Intro: 2 sentences on what this cluster covers
  Card grid: links to all cluster children
  CTA: Text PJ for [vertical] problems
  Internal links: → authority page → homepage
```

**Hub naming convention:**
```
/hubs/payments-processing.html
/hubs/ai-workflow-automation.html
/hubs/hvac-repair-vs-replace.html
/hubs/operator-problems.html
```

---

## Step 3 — Cluster Child Types

For each hub, spawn these child types based on query signals:

### A) Problem / Fix Page
**Trigger:** Query with "not working", "failing", "error", "issue", "broken"
**URL pattern:** `/problems/[tool]-[symptom]-in-2026.html`
**Title pattern:** `[Tool] [Symptom] in 2026? [Fast Fix / Root Cause]`
**Content:** Symptom → ranked causes → exact fix steps → Text PJ CTA

### B) Comparison Page
**Trigger:** Query with "vs", "or", "versus", "difference", "better"
**URL pattern:** `/[tool-a]-vs-[tool-b].html`
**Title pattern:** `[Tool A] vs [Tool B] ([Year]): [Operator Decision Frame]`
**Content:** Side-by-side feature/cost/use-case table → operator verdict → links to both tools

### C) Cost Guide Page
**Trigger:** Query with "cost", "price", "fees", "how much", "pricing"
**URL pattern:** `/pages/matrix/[topic]-cost-guide-[city].html`
**Title pattern:** `[Topic] Cost in [City] (2026): What Operators Actually Pay`
**Content:** Real ranges → what drives variance → red flags → Text PJ for review

### D) Local Geo Page
**Trigger:** Existing non-local page ranking in position 15–40 for queries with city modifiers
**URL pattern:** `/[topic]-[city].html` or `/hubs/industry-[vertical]-in-[city].html`
**Title pattern:** `[Topic] in [City] — [Operator Outcome]`
**Rule:** Only build geo page if local intent is genuine. Don't copy-paste national pages.

### E) FAQ / Decision Page
**Trigger:** Query phrased as a question ("how do I", "what is", "should I", "can I")
**URL pattern:** `/decisions/[topic].html` or `/concepts/[topic].html`
**Title pattern:** `[Question, title-cased] — SideGuy Answer`
**Content:** Direct answer in first paragraph → context → operator implications → CTA

---

## Step 4 — FAQ Page Logic

FAQ pages rank for long-tail question queries. Rules:
- Answer in the first sentence — Google pulls this as the featured snippet
- Keep answer under 60 words for snippet capture
- Expand below with operator context (why this matters, what to do next)
- Link to the parent hub page and one comparison or problem page

---

## Step 5 — Local Geo Expansion

The geo expansion pattern for San Diego:

**Priority cities (by operator density + search volume):**
1. San Diego (broadest)
2. North County San Diego (trust modifier)
3. Encinitas (highest-converting for home services)
4. Solana Beach (operator density)
5. Del Mar, Carlsbad, Oceanside (secondary)

**Geo expansion rule:** Build city pages only when:
- A non-city page already ranks 15–40 for `[topic] san diego`
- Monthly impressions ≥ 3 for the geo-modified query
- The topic has genuine local relevance (not developer tools)

**Geo page template path:** `/pages/matrix/[topic]-[intent]-[city].html`

---

## Step 6 — Authority Linking Map

Every new cluster page must connect into the authority graph:

```
New page
  ↑ linked from: parent hub OR authority category page
  ↑ linked from: homepage trending card (if it becomes a GSC winner)
  → links to: parent hub
  → links to: one comparison or decision page (cross-vertical)
  → links to: Text PJ SMS CTA
```

**Authority category pages** (already exist):
- `/authority/payments.html`
- `/authority/ai-automation.html`
- `/authority/google-ads.html`
- `/authority/operator-tools.html`
- `/authority/prediction-markets.html`
- `/authority/infrastructure.html`

New cluster pages in those verticals should get a link from the relevant authority page.

---

## Step 7 — When NOT to Spawn

**Don't spawn when:**
- Position is already < 5 — ranking is working, CTR fix beats new page
- The query is a near-synonym of an existing page — update the existing title instead
- The topic has no SideGuy vertical fit (e.g., consumer electronics, unrelated B2C)
- You'd be creating a 5th page on the same sub-topic — consolidate instead

**Consolidation signal:** 3+ pages on same sub-topic all ranking 20–50 with low impressions → merge into one stronger page with 301 redirects.

---

## Spawn Checklist

```
[ ] Identify query cluster (3+ related queries, no existing page < pos 15)
[ ] Confirm hub page exists or create it
[ ] Select child types: fix / comparison / cost / geo / FAQ
[ ] Write title using correct pattern for child type
[ ] Connect to authority linking map (hub + authority category)
[ ] Add to sitemap.xml with today's lastmod
[ ] Log new URLs in data/gsc-winners.json if they have impressions
[ ] Commit: feat: cluster spawn — [vertical] [topic]
```
