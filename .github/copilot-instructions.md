# SideGuy Solutions — AI Agent Guide

## Core Philosophy

**SideGuy is a human-first clarity layer, not a sales funnel.** Every page exists to reduce stress and provide genuine guidance before commercial transactions. Read [SIDEGUY_CORE.md](../SIDEGUY_CORE.md) first.

### The One Rule
Offer the truth. Nothing more.

---

## Project Architecture

### What This Is
- **10,000+ static HTML pages** serving San Diego local businesses
- **Problem/solution landing pages** covering HVAC, plumbing, electrical, software, payments, AI automation
- **Zero traditional framework** — vanilla HTML/CSS/JS with inline styles
- **Observation mode:** Automation intentionally disabled; human decisions required

### Key Directories
- **Root (`/`)**: All HTML pages live at root level (flat structure)
- **`/partials/`**: Reusable components (currently minimal)
- **`/seo-reserve/`**: Reserved SEO content, automation prep (DO NOT AUTO-BUILD)
- **`/docs/`**: Business logic, decision logs, compliance docs
- **`/signals/`**: System state tracking, daily observations
- **`/data/`**: JSON state files for payments, capacity, pricing

---

## Critical Patterns

### HTML Pages: Self-Contained Design
**All pages use inline CSS with CSS variables:**
```html
<style>
  :root {
    --bg0:#eefcff;
    --ink:#073044;
    --mint:#21d3a1;
    --phone:"+17604541860";
    --city:"San Diego";
  }
  body {
    font-family:-apple-system, system-ui, sans-serif;
    background:radial-gradient(...);
  }
</style>
```

**Why:** No external CSS dependencies. Each page is portable and self-sufficient.

### Naming Conventions
- **Problem pages:** `problem-name-san-diego.html` (e.g., `ac-not-cooling-san-diego.html`)
- **Service pages:** `service-name-san-diego.html` (e.g., `hvac-repair-san-diego.html`)
- **Decision pages:** `who-do-i-call-for-X.html` (guidance, not sales)
- **Backup files:** Ignored via `.gitignore` (`*.backup.*`, `*.bak`)

### Page Title Pattern
**Title:** `[Clear Problem/Service] · SideGuy Solutions (San Diego)`  
**H1:** Direct, plain language (e.g., "AC Not Cooling in San Diego — What to Check First")  
**Meta Description:** ~150 chars, no hype, actionable clarity

---

## Build & Deployment

### There Is No Build System (By Design)
- **No bundler, no SSG, no framework**
- **No automated page generation** (see `seo-reserve/build-nothing-yet/`)
- **Manual edits only** — automation is intentionally deferred
- Changes = edit HTML directly, commit, deploy

### Sitemap Generation
```bash
./generate-sitemap-failsafe.sh
```
Creates `sitemap.html` (human-readable index) and updates `sitemap.xml` for SEO.

### Single Page Generator (Safety-Limited)
```bash
./single-page-generator.sh <manifest.json>
```
Generates ONE page only (hard stop enforced).

---

## Development Workflows

### Adding a New Page
1. **Copy an existing similar page** (e.g., `ac-not-cooling-san-diego.html`)
2. **Update inline CSS variables** if needed (`:root` section)
3. **Change `<title>`, meta description, H1, content**
4. **Keep inline styles** — do NOT extract to external CSS
5. **Test locally** (open directly in browser)
6. **Commit with clear message:** `Add: [page name] - [one-line purpose]`

### Editing Existing Pages
- **Inline CSS changes:** Update `:root` variables or styles directly in `<style>` block
- **Content changes:** Plain HTML edits
- **DO NOT refactor into components** unless explicitly requested
- **Preserve backup naming convention:** Files ending in `.backup.*` are auto-ignored

### Critical Files — DO NOT AUTO-MODIFY
- `SIDEGUY_CORE.md` — Core philosophy
- `CPU_SHIP.md` / `CPU_INBOX.md` — Human decision queue
- `seo-reserve/**` — Reserved future SEO content (automation OFF)
- `observation-notes.md` / `tech-notes.md` — System observations
- `robots.txt` / `sitemap-index.xml` — SEO infrastructure

---

## Domain & SEO

### Current Domain
**Primary:** `sideguy.solutions`  
**Robots.txt:** Points to `sitemap-index.xml`  
**Sitemap index:** References `sitemap.xml` and longtail variants

### SEO Strategy
- **Long-tail problem/solution keywords** (San Diego local)
- **No duplicate titles/H1s** (previously an issue, now being fixed)
- **Unique meta descriptions per page**
- **No aggressive keyword stuffing** — calm, helpful tone

### Known Issues (Documented)
- 10,000+ pages with template duplication (refactor deferred intentionally)
- Some pages have placeholder content (`<!-- TODO: ... -->`)
- Backup files polluting directory (`.gitignore` now handles this)

---

## Code Style & Conventions

### HTML
- **Semantic HTML5:** Use `<header>`, `<main>`, `<section>`, `<footer>`
- **Inline styles only** (no external `styles.css` linking)
- **Minimal JavaScript:** Inline `<script>` tags for timestamps, simple interactions
- **Accessibility:** Alt text, ARIA labels, semantic structure

### CSS
- **CSS Custom Properties (variables)** for colors, spacing, phone numbers
- **Mobile-first responsive design** with `@media` queries
- **Radial gradient backgrounds** for visual cohesion (ocean theme)
- **System fonts:** `-apple-system, system-ui, Segoe UI, Roboto, Inter, sans-serif`

### JavaScript
- **Vanilla JS only** — no frameworks, no build step
- **Progressive enhancement:** Pages work without JS
- **Common patterns:**
  - Dynamic timestamp insertion
  - Weather widget (San Diego local)
  - Simple DOM manipulation

---

## Human-in-the-Loop Decision Points

### When to STOP and Ask PJ
1. **Adding automation** (deferred intentionally)
2. **Creating page templates/generators** (see `seo-reserve/build-nothing-yet/`)
3. **Bulk content generation** (requires human approval per `seo-reserve/_auto-generation-prep/`)
4. **Domain/DNS changes**
5. **Payment processing changes** (Solana, Stripe alternatives)
6. **Changing core philosophy** (SIDEGUY_CORE.md)

### Decision Logs
**Location:** `decisions/decision-YYYY-MM-DD-HH:MM.md`  
**Format:** Timestamped, context-aware, tracks "why" behind changes

---

## Testing & Validation

### Manual Testing
- Open HTML files directly in browser (no server required)
- Test on mobile viewport (Chrome DevTools)
- Verify phone number links work (`tel:+17604541860`)
- Check CSS variable inheritance

### No Automated Tests
- No Jest, Mocha, Playwright, etc.
- Manual QA only (human observation)

---

## Git Workflow

### Branches
- `main` — production (auto-deploys to sideguy.solutions)
- `robots-sitemap-domain-flip` — current working branch (per attachment)

### Commit Messages
- **Format:** `Action: file/component - brief description`
- **Examples:**
  - `Add: ac-repair-pricing.html - San Diego HVAC pricing calculator`
  - `Fix: duplicate H1 tags across 200+ payment processing pages`
  - `Update: SIDEGUY_CORE.md - clarify human-first philosophy`

### PR Strategy
- **Keep PRs small** (single concern)
- **Reference decision logs** if architectural
- **No automated CI/CD** (manual review & deploy)

---

## External Dependencies

### None (By Design)
- **No npm packages**
- **No CDN dependencies** (exception: Font Awesome on some pages)
- **No analytics/tracking** (deferred during observation mode)
- **No third-party frameworks** (React, Vue, etc.)

---

## Common Pitfalls to Avoid

1. **DO NOT extract CSS to external files** — inline styles are intentional
2. **DO NOT create automated page generators** — see `build-nothing-yet/` policy
3. **DO NOT assume "more pages = better SEO"** — quality over quantity
4. **DO NOT remove "backup" files manually** — .gitignore handles them
5. **DO NOT change phone number** without updating `:root` CSS variables everywhere
6. **DO NOT add build tools** (Webpack, Vite, etc.) — flat HTML is the architecture

---

## Quick Reference

### Key Files
- `SIDEGUY_CORE.md` — Philosophy & mission
- `robots.txt` — SEO crawler directives
- `sitemap.xml` — Primary sitemap for Google
- `sideguy-include.js` — Client-side HTML includes (minimal use)
- `generate-sitemap-failsafe.sh` — Manual sitemap regeneration

### Key Directories
- `/seo-reserve/` — Reserved content (DO NOT AUTO-BUILD)
- `/signals/` — System state & observations
- `/docs/` — Business logic & compliance

### Contact
**Text PJ:** +1-760-454-1860  
**Philosophy:** Clarity before cost. Human guidance layer.

---

## Final Note for AI Agents

This project prioritizes **human judgment over automation**. When in doubt:
1. Check `SIDEGUY_CORE.md` for philosophical alignment
2. Look for similar existing pages as templates
3. Preserve inline styles (no refactoring to external CSS)
4. Ask PJ before adding automation or bulk generation
5. Focus on clarity, not clever code

**Remember:** SideGuy is not a tech showcase. It's a calm place for stressed people making hard decisions.
