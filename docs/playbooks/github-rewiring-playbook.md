# SideGuy GitHub Rewiring Playbook

## Core Doctrine

No secrets until the shell is proven.
Build the fallback first. Wire the API second.
Every utility page must work without a key.

---

## The 6-Step Install Workflow

### Step 1 — Find the High-Signal GitHub Primitive
- Browse public-apis, apilayer.com, or RapidAPI
- Match to an existing GSC gap or solder map `next_action`
- Ask: does this API serve a question a stressed person types at 11pm?
- If yes → proceed. If no → skip.

### Step 2 — Choose the SideGuy Page Gap
- Check `data/solder/search-page-map-latest.tsv` for orphan intent
- Check `docs/reasoning/reasoning-gap-report.md` for missing calculators
- Priority order: calculator gap → escalation gap → local trust gap
- The gap must already have GSC impressions OR a confirmed cluster need

### Step 3 — Install the Static Utility Shell First
- Build the full page UI in static HTML + inline JS
- Populate all data sections with hardcoded reference data
- The page must be useful without a single API call
- Test: cover the API section — does the page still help someone?

### Step 4 — Add Fallback + CTA Ladder
- Every API call gets a `try/catch` or `.catch()` handler
- Fallback shows: best static answer + action steps + Text PJ CTA
- CTA is always `sms:+17735441231` — never a form, never email
- The fallback should feel like an intentional feature, not an error state

### Step 5 — Defer API Keys
- Add a `CONFIG` block at the top of the script section
- Set `useLive: false` by default
- Document free tier limits and HTTPS constraints in comments
- Commit with `YOUR_ACCESS_KEY` placeholder — never a real key in git

### Step 6 — Clone Pattern Across Verticals
- Once shell is proven (crawled, fallback working, CTA firing), clone
- Swap: vertical name, static data, decay causes, trust ladder steps
- Keep: layout, config block pattern, fallback logic, CTA block
- Update `data/solder/search-page-map-latest.tsv` with new route

---

## Case Studies

### Airport Stress Hub — Aviationstack
**Gap:** `airport-stress-hub.html` didn't exist. Solder map showed `spawn-airline-pages`.
**Primitive:** Aviationstack API (apilayer.com) — real-time flight status
**Shell:** Terminal guide (T1/T2W/T2E), delay cause explainer, 10-airline on-time bars, 5-step delay action ladder
**Fallback:** Static terminal info + action ladder fires when `useLive: false` or HTTP blocked
**API constraint:** Free tier = HTTP only. HTTPS requires $9.99/mo paid plan. Documented in config.
**Key lesson:** The static shell was immediately useful. The API is an upgrade, not a dependency.

---

### Payments Fee Calculator — Stripe (No External API)
**Gap:** `stripe-fees` at pos 4, 33 impr, no interactive tool
**Primitive:** No API needed — pure math
**Shell v1:** Volume + ticket size → Stripe cost vs interchange-plus
**Shell v2:** Added international card % slider (+1.5%), disputes slider ($15 each), Stripe Billing toggle (+0.5%)
**Live calc:** `oninput` handler — no button click required
**Result:** Title promised "after card mix, disputes, and international fees" — v2 delivered it
**Key lesson:** Not every utility needs an API. The calculator IS the primitive.

---

### HVAC Weather Urgency — Weatherstack (Clone Path)
**Gap:** HVAC cluster has zero impressions. `mini-split-san-diego.html` → `spawn-cost-calculator`
**Primitive:** Weatherstack API — real-time temperature + humidity
**Shell to build:** Coastal weather stress explainer, marine layer + compressor strain guide, mini-split decision ladder, repair vs replace cost trust ladder, 5-step urgency action plan, North County trust cues
**Config block:** `WEATHER_CONFIG { accessKey, useLive: false, city: 'San Diego' }`
**Fallback:** Static San Diego climate data (June Gloom, Santa Ana winds, marine layer) + action ladder
**Clone from:** `airport-stress-hub.html` — same layout, same config pattern, same CTA block

---

## Screenshot Solder Loop

When a screenshot of a SERP, competitor page, or analytics panel arrives:

1. Drop into `uploads/screenshots/`
2. Run `bash tools/solder/run-pic-signal-solder.sh`
3. Review `docs/solder/pic-signal-report.md` — HIGH confidence routes flagged
4. Pick top `next_action` → match to Step 2 above
5. Build the shell → commit → let crawl run

---

## Hard Rules

- Never commit a real API key. `YOUR_ACCESS_KEY` is the only value that goes to git.
- Never build a page that requires the API to be useful. Shell first.
- Never add a form where a `sms:` link works. Text PJ is the escalation.
- Never block on API tier upgrade. Free fallback ships today. Paid upgrade is a future PR.
- Every new utility page gets a route in `data/solder/search-page-map-latest.tsv`.
- Every new hub gets added to `data/reasoning/reasoning-seeds.csv`.

---

## Version

April 5, 2026 · Proven on: airport-stress-hub, stripe-fees-calculator, reasoning-gap-scorer
