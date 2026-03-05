# Claude Prompt — Link Equity Balancing
Generated: 2026-03-05 18:56:15

## Goal
Strengthen internal authority distribution across SideGuy by auditing and fixing
cluster hubs and leaf pages that lack required internal links.

## Actions

### 1. Strengthen weak clusters
The following clusters have fewer than 10 pages and need incoming links
from the directory hub (`auto-hubs/directory.html`) and from related strong clusters:

  - Stripe Troubleshooting (payments/stripe) — 1 pages
  - Chargebacks & Disputes (payments/chargebacks) — 1 pages
  - Operator Tools (Overview) (operator-tools/operator-tools-overview) — 4 pages
  - Payment Fee Comparison (payments/payment-fees) — 8 pages

### 2. Source authority from strong clusters
Add contextual outbound links from these strong clusters pointing toward the weak ones above:

  - AI Automation Cost & ROI (ai-automation/ai-cost) — 5421 pages
  - AI Automation (Overview) (ai-automation/ai-overview) — 2250 pages
  - AI Automation Tools (ai-automation/ai-tools) — 1669 pages
  - AI Automation — City Pages (ai-automation/ai-city-pages) — 1268 pages
  - AI Scheduling & Booking (ai-automation/ai-scheduling) — 1201 pages
  - AI Agent Workflows (ai-automation/ai-agent-workflows) — 446 pages
  - AI Consulting (ai-automation/ai-consulting) — 231 pages
  - AI for Restaurants (ai-automation/ai-restaurants) — 116 pages
  - General (Other) (problem-intelligence/general) — 52 pages

### 3. Ensure every cluster hub links to:
- Its pillar category page (e.g., `auto-hubs/categories/payments.html`)
- At least 5 related cluster hubs
- At least 10 leaf pages in its own cluster

### 4. Ensure every leaf page links to:
- Its cluster hub (`auto-hubs/clusters/<cluster>.html`)
- Its pillar hub (`auto-hubs/categories/<pillar>.html`)
- 3 related leaf pages in the same cluster

### 5. Maintain SideGuy page structure:
- Quick answer
- Why it happens
- Common misunderstandings
- Next steps
- Text PJ CTA: "Text PJ: 773-544-1231"

## Files to review
- Rebalance plan: `docs/link-equity/generated/link_rebalance_plan.md`
- Hub audit: `docs/link-equity/generated/hub_audit.json`
- Leaf issues: `docs/link-equity/generated/leaf_backlink_issues.json`
- Cluster sizes: `docs/link-equity/generated/cluster_sizes.tsv`
