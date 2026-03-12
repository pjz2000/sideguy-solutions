# SideGuy Crawl Authority Router

Purpose:

Distribute internal authority signals across the site.

Strategy:

High-crawl pages pass internal links to revenue pages.

Improves:

- crawl discovery
- ranking signals
- topical relevance

Rules:

1-2 contextual links per page only.

Avoid unnatural link stuffing.

## Usage

1. Run authority_router.py to generate the route map (read-only audit)
2. Review docs/crawl-router/authority_links.md manually
3. Only run internal_link_injector.py after confirming each route is
   topically relevant — random injection is NOT acceptable on real content pages.
