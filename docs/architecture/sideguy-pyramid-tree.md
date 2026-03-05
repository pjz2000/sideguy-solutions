# SideGuy Pyramid-Tree Architecture (Canonical)

Last updated: 2026-03-05

---

## Why This Exists

SideGuy is not "a blog." SideGuy is a **Problem Intelligence Infrastructure**:

1. Google discovers the problem
2. AI explains it clearly
3. A real human resolves it — **Text PJ: 773-544-1231**

This doc locks the **pyramid + tree** site architecture:

```
ROOT (identity)
 └── PILLARS ×10  (trunk / section homepages)
      └── CLUSTERS ×20–50 per pillar  (branches / topical authority)
           └── LEAVES ×18,000+  (long-tail programmatic pages)
```

---

## URL / File Structure Convention

```
ROOT:    index.html
PILLAR:  hubs/category-ai-automation.html
         hubs/category-payments.html
         electrical-problems-hub-san-diego.html
CLUSTER: [pillar-slug]-[cluster-slug]-san-diego.html
         (e.g.) ai-automation-consulting-san-diego.html
LEAF:    [problem]-[city].html
         (e.g.) stripe-chargeback-how-to-fight-san-diego.html
```

---

## 1) The Root (Site Identity)

Every page carries these three roots implicitly:

| Root signal | How it appears |
|-------------|---------------|
| Clarity before cost | subtly in meta description or hero text |
| AI explains → Human resolves | friendly intelligence block |
| Text PJ | CTA at bottom of every page |

---

## 2) The Trunk (Authority Pillars) — Current Inventory

| Priority | Pillar | Slug | Leaf Pages | Hub Page |
|----------|--------|------|-----------|---------|
| 1 | AI Automation | `ai-automation` | 1,315 | hubs/category-ai-automation.html |
| 2 | Payments & Processing | `payments` | 326 | hubs/category-payments.html |
| 3 | Business Software | `business-software` | 255 | (needs hub page) |
| 4 | Home Systems | `home-systems` | 194 | electrical-problems-hub-san-diego.html |
| 5 | Local Operator Tech | `local-operator-tech` | 1,229 | authority/local-seo-hub.html |
| 6 | Crypto & Web3 | `crypto-web3` | 54 | hubs/category-crypto-solana.html |
| 7 | Energy & EV | `energy-ev` | 24 | (needs hub page) |
| 8 | Operator Tools | `operator-tools` | 41 | (needs hub page) |
| 9 | Prediction Markets | `prediction-markets` | 5 | prediction-markets-hub.html |
| 10 | Problem Intelligence | `problem-intelligence` | 22 | (needs hub page) |

**Total mapped leaves: 3,465** (of 18,417 total pages — rest in `local-operator-tech` SF/city pattern or `_unmapped`)

---

## 3) The Branches (Clusters) — What's Defined

Clusters are defined in `docs/architecture/generated/cluster-*.md`.

**Defined so far:** 29 clusters across 6 pillars.
**Target:** 20–50 clusters per pillar.

Each cluster page must:
- Explain the topic in calm, human language
- Link up to its pillar hub
- List its leaf pages
- Link sideways to 3–8 related clusters
- Have a "Text PJ" CTA

---

## 4) The Leaves (Long-Tail Pages) — 18,000+

Every leaf page must carry:

```html
<!-- PYRAMID NAV (required on every page) -->
<nav class="pyramid-nav">
  <a href="/[pillar-hub]">← [Pillar Name]</a>
  <a href="/[cluster-page]">← [Cluster Name]</a>
</nav>

<!-- RELATED PAGES (same cluster, 2–5 links) -->
<section class="related-pages">
  <h3>Related</h3>
  <ul>...</ul>
</section>

<!-- TEXT PJ CTA -->
<div class="text-pj">
  Still unsure? <a href="sms:+17735441231">Text PJ</a>
</div>
```

---

## 5) Internal Linking Rules (Non-Negotiable)

### Leaf page
- `Back to Cluster` link
- `Back to Pillar` link
- `Related Pages` 2–5 (same cluster)
- `Text PJ` CTA

### Cluster page
- `Back to Pillar` link
- `Top leaf pages` list (10–30)
- `Related clusters` list (3–8)
- `Text PJ` CTA

### Pillar page
- `Top clusters` list (all defined clusters)
- `Featured leaf pages` list (10–20)
- `Related pillars` list (3–5)
- `Text PJ` CTA

---

## 6) Friendly Intelligence Block (Tone Contract)

Sound like **a smart friend explaining things calmly**.

**Standard block structure (use on every leaf):**
1. **Quick answer** — 1–3 sentences, direct
2. **Why this happens** — plain language, no jargon
3. **What people misunderstand** — 3 bullets
4. **Simple next steps** — 5 max
5. **When to text PJ** — honest, non-salesy

**Tone examples:**

| Wrong | Right |
|-------|-------|
| "Thermodynamic systems operate at..." | "Your AC compressor is basically the heart of the system..." |
| "Payment rail velocity impacts..." | "The money usually takes 1–2 business days to land." |
| "Leverage AI paradigms to..." | "You can set this up once and it handles itself." |

---

## 7) Schema.org Breadcrumb (Required on All Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "SideGuy Solutions", "item": "https://sideguysolutions.com/"},
    {"@type": "ListItem", "position": 2, "name": "[Pillar]", "item": "https://sideguysolutions.com/[pillar-hub]"},
    {"@type": "ListItem", "position": 3, "name": "[Cluster]", "item": "https://sideguysolutions.com/[cluster-page]"},
    {"@type": "ListItem", "position": 4, "name": "[Page Title]", "item": "https://sideguysolutions.com/[leaf-page]"}
  ]
}
```

---

## 8) The Intelligence Loop

```
Search demand → pages rank → GSC queries reveal gaps
→ build deeper cluster + leaf pages → more demand
```

Problem Radar rule:
- Build where impressions are already emerging
- Don't guess forever — respond to real signal
- `data/pillar-leaf-map.json` tracks current inventory

---

## 9) Phase Status

| Phase | Status | What |
|-------|--------|------|
| Phase 1 | ✅ Done | 18,417 leaves + authority loop + KGB mode |
| Phase 2A | ✅ Done | Pyramid architecture locked + pillar manifests |
| Phase 2B | 🔄 Next | Wire up-links on existing leaves (leaf → cluster → pillar) |
| Phase 2C | 🔄 Next | Build missing hub pages (business-software, energy-ev, operator-tools) |
| Phase 3 | ⏳ Future | Cluster expansion (20–50 per pillar) driven by GSC signal |

