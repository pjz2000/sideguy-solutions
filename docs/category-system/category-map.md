# SideGuy Category System

## Purpose

Category hubs sit **above clusters** in the authority pyramid:

```
Category  ← this layer
  → Cluster hub
    → Leaf pages
```

Each category collects search traffic for a broad topic, then distributes authority downward to cluster hubs and leaf pages.

Generated: 2026-03-05 17:56:57

---

## Categories

| Slug | Label | Pillar | Sub-clusters | Path |
|------|-------|--------|-------------|------|
| ai-automation | AI Automation | ai-automation | ai-overview, ai-tools, ai-consulting, ai-scheduling | /auto-hubs/categories/ai-automation.html |
| hvac | HVAC Troubleshooting | home-systems | hvac, ac-problems, thermostat, heating | /auto-hubs/categories/hvac.html |
| payments | Payment Processing | payments | payments-overview, payment-fees, merchant-accounts | /auto-hubs/categories/payments.html |
| chargebacks | Chargebacks & Disputes | payments | chargebacks | /auto-hubs/categories/chargebacks.html |
| tesla-charging | Tesla Charging at Home | energy-ev | ev-charging | /auto-hubs/categories/tesla-charging.html |
| ev-charging | EV Charging | energy-ev | ev-charging, energy-savings, solar | /auto-hubs/categories/ev-charging.html |
| crypto-wallets | Crypto Wallets & Safety | crypto-web3 | crypto-wallets, accepting-crypto, bitcoin-basics | /auto-hubs/categories/crypto-wallets.html |
| prediction-markets | Prediction Markets | prediction-markets | overview, signals | /auto-hubs/categories/prediction-markets.html |
| business-software | Business Software | business-software | software-overview, crm, accounting-software | /auto-hubs/categories/business-software.html |
| automation-tools | Automation Tools | ai-automation | ai-tools, ai-agent-workflows, ai-scheduling | /auto-hubs/categories/automation-tools.html |

---

## Structure

- **HTML files:** `auto-hubs/categories/{slug}.html`
- **Each page includes:**
  - BreadcrumbList JSON-LD schema
  - FAQPage JSON-LD schema (3 real Q&As per category)
  - Cluster chip navigation (links to cluster hubs)
  - Leaf tile grid (up to 48 unique pages)
  - Text PJ CTA

---

## Navigation Hierarchy

```
/  (home)
  → Pillar hub  (e.g. /hubs/category-ai-automation.html)
    → Category page  (e.g. /auto-hubs/categories/ai-automation.html)
      → Cluster hub  (e.g. /auto-hubs/clusters/ai-automation--ai-tools.html)
        → Leaf page  (e.g. /ai-automation-consulting-san-diego.html)
```
