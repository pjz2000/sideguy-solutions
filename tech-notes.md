# SideGuy Technical Notes

This file tracks deferred technical decisions intentionally not implemented yet.

## Architecture Decisions
- **No build system:** Flat HTML with inline CSS (intentional for portability)
- **No frameworks:** Vanilla JS only (keeps pages lightweight and portable)
- **CSS variables:** All theming via `:root` variables (easy global updates)
- **Observation mode:** Analytics and automation intentionally deferred

## Technical Debt (Intentional)
- 1,664 pages with duplicate metadata (will fix based on traffic patterns)
- Some TODO placeholders in page content (awaiting real-world validation)
- No client-side routing (correct for SEO)

## Tools Created
- `metadata-audit.py` — Scans all pages for SEO issues
- `generate-xml-sitemap.py` — Automated sitemap generation
- `generate-sitemap-failsafe.sh` — Human-readable HTML sitemap

## Infrastructure Status
- ✅ Sitemap: Valid XML sitemap with 1,722 URLs
- ✅ Robots.txt: Properly configured
- ✅ .gitignore: Excludes backup files
- ✅ Repository: Clean (backup files removed)

## Future Considerations (When Traffic Justifies)
- Minimal privacy-respecting analytics (Plausible/Fathom)
- Component extraction for truly shared elements
- Manifest-driven title/meta generation
- Structured data markup for local business pages
