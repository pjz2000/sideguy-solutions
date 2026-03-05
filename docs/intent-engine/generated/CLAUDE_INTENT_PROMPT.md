# Claude Prompt — SideGuy Intent Engine (Final Boss)
Generated: 2026-03-05 19:00:29

## Goal
Turn each cluster into a high-traffic intent surface area that ranks for many
related queries. Each cluster gets 16 intent pages covering every angle a
searcher might use.

## What was generated
- Intent packs doc : `docs/intent-engine/generated/INTENT_PACKS.md`
- Stub pages dir   : `auto-intent-pages/{pillar}/{cluster}/`
- Total stubs      : 256 new files

## Page structure (non-negotiable)
Every intent page must follow SideGuy format:
1. Quick answer (30 seconds, calm)
2. Why this happens (3 bullets)
3. What people misunderstand (3 bullets)
4. Simple next steps (5 steps max)
5. Text PJ CTA — Text PJ: 773-544-1231

## Internal links to inject (replace placeholders)
- `__RELATED_LEAF_1/2/3__` → 3 real sibling intent pages in same cluster
- `__SEE_ALSO_CLUSTER_1/2/3/4__` → 4 related cluster hub URLs from See-Also engine
- `__RELATED_TITLE_*__` / `__SEE_ALSO_TITLE_*__` → human-readable link text

## Priority order
Start with high-traffic clusters (most existing leaves = most authority):

- **AI Automation Cost & ROI** (`ai-automation/ai-cost`) — 5421 existing pages
- **AI Automation (Overview)** (`ai-automation/ai-overview`) — 2250 existing pages
- **AI Automation Tools** (`ai-automation/ai-tools`) — 1669 existing pages
- **AI Automation — City Pages** (`ai-automation/ai-city-pages`) — 1268 existing pages
- **AI Scheduling & Booking** (`ai-automation/ai-scheduling`) — 1201 existing pages
- **AI Agent Workflows** (`ai-automation/ai-agent-workflows`) — 446 existing pages

## Then strengthen weak clusters (need most authority injection):

- **Payment Fee Comparison** (`payments/payment-fees`) — 8 pages — hub: `/auto-hubs/clusters/payments--payment-fees.html`
- **Operator Tools (Overview)** (`operator-tools/operator-tools-overview`) — 4 pages — hub: `/auto-hubs/clusters/operator-tools--operator-tools-overview.html`
- **Stripe Troubleshooting** (`payments/stripe`) — 1 pages — hub: `/auto-hubs/clusters/payments--stripe.html`
- **Chargebacks & Disputes** (`payments/chargebacks`) — 1 pages — hub: `/auto-hubs/clusters/payments--chargebacks.html`

## Execution plan
1. Fill the first 6 intent pages for each top cluster with human-quality content
2. Use those as the writing pattern
3. Batch-fill remaining intent pages consistently
4. Replace all `__PLACEHOLDER__` strings with real content + links
5. Set canonical to: `https://sideguysolutions.com/auto-intent-pages/{pillar}/{cluster}/{slug}.html`

## Files
- Stubs: `auto-intent-pages/`
- Packs: `docs/intent-engine/generated/INTENT_PACKS.md`
- Intent library: `docs/intent-engine/intent_library.tsv`
