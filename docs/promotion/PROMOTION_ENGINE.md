# SideGuy Promotion Engine

Purpose:
Move approved pages from factory inventory into the live site.

Why this matters:
Large sites should not auto-publish everything they generate.

This engine ensures:

inventory first
quality filtering
controlled promotion
append-only publishing

Command:

bash tools/factory/promote-pages.sh

Source:
pages/factory/

Destination:
site root

Rules:
- skip existing pages
- skip thin pages (<500 words)
- append sitemap entries if sitemap exists

Workflow:

page factory
→ strengthen pages
→ publish gate
→ promotion engine
→ internal linking
→ authority growth
