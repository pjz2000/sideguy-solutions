# Discovery → Index Upgrade
Goals:
- kill homepage orphan rectangle
- strengthen page freshness
- reinforce canonical uniqueness
- improve crawl gravity
- convert discovered URLs into indexed URLs faster

## What runs safely
- Defensive CSS for empty media placeholders (display:none for :empty elements)
- Per-page content upgrades (manual, targeted — not bulk sed)
- Canonical audit (non-www only — no www. prefix)

## What to avoid
- Bulk freshness timestamps across 500 pages (thin duplicate content)
- www. canonical injection (conflicts with existing non-www setup)
- Appending after </html> (ignored by browsers)
