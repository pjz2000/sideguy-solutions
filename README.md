# SideGuy Solutions

**A human-first clarity layer for San Diego operators making stressful decisions.**

## What This Is

SideGuy is 1,725+ static HTML pages serving local businesses and residents in San Diego with practical, pressure-free guidance on HVAC, plumbing, electrical, software, payments, and business decisions.

**Core Philosophy:** Offer the truth. Nothing more. (See [SIDEGUY_CORE.md](SIDEGUY_CORE.md))

## Architecture

- **Static HTML** — No build system, no framework
- **Inline CSS** — Self-contained pages with CSS variables for theming
- **Flat structure** — All pages at root level for simple deployment
- **Human-first** — Observation mode; automation deferred until traffic patterns emerge

## Repository Status

✅ **Clean** — 1,725 HTML pages, 0 backup files  
✅ **SEO Ready** — Valid XML sitemap with 1,722 indexed URLs  
✅ **Documented** — Clear philosophy, decision logs, observation notes  
✅ **Maintainable** — Audit tools and health checks included

## Quick Start

### View the Site
```bash
# Open any HTML file directly in browser (no server needed)
open index.html
```

### Run Health Check
```bash
python3 health-check.py
```

### Audit Metadata
```bash
python3 metadata-audit.py
```

### Generate Sitemap
```bash
python3 generate-xml-sitemap.py
```

### Generate HTML Sitemap
```bash
bash generate-sitemap-failsafe.sh
```

## Key Files

- [SIDEGUY_CORE.md](SIDEGUY_CORE.md) — Core philosophy (20 lines)
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — AI agent guide
- [observation-notes.md](observation-notes.md) — System observations
- [tech-notes.md](tech-notes.md) — Technical decisions
- [robots.txt](robots.txt) — Search engine directives
- [sitemap.xml](sitemap.xml) — XML sitemap (auto-generated)

## Directory Structure

```
/                          # 1,725+ HTML pages (flat structure)
/seo-reserve/              # Reserved SEO content (automation OFF)
/signals/                  # System state tracking
/docs/                     # Business logic, compliance
/data/                     # JSON state files
/.github/                  # GitHub and Copilot config
```

## Naming Conventions

- **Problem pages:** `problem-name-san-diego.html`
- **Service pages:** `service-name-san-diego.html`
- **Decision pages:** `who-do-i-call-for-X.html`
- **Backup files:** Ignored via `.gitignore` (`*.backup.*`)

## Technical Stack

- **HTML5** — Semantic structure
- **CSS3** — Custom properties, radial gradients
- **Vanilla JavaScript** — Minimal, progressive enhancement
- **Python** — Maintenance scripts (audit, sitemap generation)

## Known Issues (Intentional)

- **1,664 pages with duplicate metadata** — Template-based; will fix systematically based on traffic data
- **No analytics** — Deferred during observation mode
- **No build system** — Intentional for simplicity and portability

## Development Workflow

### Adding a New Page
1. Copy similar existing page
2. Update inline CSS variables if needed (`:root` section)
3. Change `<title>`, meta description, H1, content
4. Keep inline styles (do NOT extract to external CSS)
5. Commit with clear message: `Add: [page name] - [purpose]`

### Maintenance Commands
```bash
# Clean up (if needed)
find . -maxdepth 1 -name "*.backup.*" -delete

# Regenerate sitemap
python3 generate-xml-sitemap.py

# Check repository health
python3 health-check.py

# Audit metadata
python3 metadata-audit.py
```

## SEO Strategy

- Long-tail problem/solution keywords (San Diego local)
- Unique titles/H1s per page (systematic fixes in progress)
- Semantic HTML structure
- Mobile-first responsive design
- No keyword stuffing — calm, helpful tone

## Contact

**Text PJ:** [+1-760-454-1860](tel:+17604541860)  
**Website:** [sideguy.solutions](https://sideguy.solutions)  
**Philosophy:** Clarity before cost. Human guidance layer.

## License

Proprietary — All rights reserved.

---

**Remember:** SideGuy is not a tech showcase. It's a calm place for stressed people making hard decisions.
