# SideGuy Client Wins Ledger

Living record of solved problems. Every entry becomes a reusable module for the next client.

---

## Template

```
- Client:
- Vertical:
- Problem:
- Time to clarity:
- Money saved:
- Hours saved:
- What changed:
- Reusable lesson:
- Cloneable module:
```

---

## Wins

### Win 001 — Payments Leakage / Stripe vs Square Fee Clarity

- **Client:** Small business operator (service vertical)
- **Vertical:** Payments
- **Problem:** Operator didn't know they were paying 2.9% + 30¢ flat when interchange-plus would cost ~1.7–2.1% on debit. Processing $18k/month — losing ~$180–360/month in avoidable fees.
- **Time to clarity:** 10 minutes
- **Money saved:** $180–360/month ($2,160–$4,320/year)
- **Hours saved:** 3–5 hours of vendor research
- **What changed:** Switched to interchange-plus pricing tier. Processor conversation framed as "I know what interchange-plus is and I want it."
- **Reusable lesson:** Most operators don't ask for interchange-plus because nobody told them it exists. The ask itself is the unlock — no tool needed.
- **Cloneable module:** `/how-credit-card-processing-fees-work.html` + `/stripe-vs-square.html` — fee clarity layer reusable for any merchant vertical.

---

### Win 002 — Contractor Workflow Automation

- **Client:** Trade contractor (quotes + follow-ups manual)
- **Vertical:** AI Automation / Operator Tools
- **Problem:** Sending quotes manually via email, following up by memory, losing jobs to faster responders. Estimated 2–3 lost jobs/month from slow follow-up.
- **Time to clarity:** 20 minutes
- **Money saved:** $600–1,200/month in recovered jobs (conservative)
- **Hours saved:** 4–6 hours/week on manual follow-up
- **What changed:** Zapier zap — new quote → auto follow-up email at 24h + 72h. No CRM needed. $0 tooling cost (free tier).
- **Reusable lesson:** Contractors lose jobs to speed, not price. A 2-step follow-up zap recovers more revenue than any marketing spend.
- **Cloneable module:** Quote follow-up zap template + `/ai-automation-consulting-san-diego.html` workflow clarity page.

---

### Win 003 — HVAC Repair vs Replace Clarity

- **Client:** San Diego homeowner, North County
- **Vertical:** HVAC / Home Systems
- **Problem:** Three quotes ranging $8k–$14k for "full system replacement." Operator suspected oversell but had no framework to challenge it.
- **Time to clarity:** 15 minutes
- **Money saved:** $7,400–$13,400 (capacitor + refrigerant recharge = ~$400–600 actual fix)
- **Hours saved:** 2–4 hours of contractor negotiation
- **What changed:** Taught client the repair-vs-replace decision tree: age of unit, refrigerant type (R22 vs R410A), capacitor test, efficiency delta. One question to the tech — "can you test the capacitor first?" — collapsed the oversell.
- **Reusable lesson:** HVAC contractors often quote replacement when repair is viable because replacement margins are 10×. One diagnostic question changes the frame.
- **Cloneable module:** HVAC repair-vs-replace decision tree → reusable for any home systems clarity page. `/pages/expansion/hvac-repair-repair-vs-replace.html`

---

### Win 004 — AI Lead Routing for Local SMB

- **Client:** Local service business, San Diego
- **Vertical:** AI Automation / Local SD
- **Problem:** Leads coming from 3 sources (Google form, Instagram DM, text) — all going to same inbox, no triage, response time 4–24 hours. Competitor books same-day.
- **Time to clarity:** 25 minutes
- **Money saved:** Estimated $800–1,500/month in recovered bookings
- **Hours saved:** 1–2 hours/day of manual inbox sorting
- **What changed:** Single Zapier routing layer — all 3 sources → one triage sheet → auto-reply with booking link within 5 minutes of inquiry. High-urgency flag triggers direct text to owner.
- **Reusable lesson:** Lead routing is not a CRM problem. It's a 2-step zap problem. Most operators buy $200/month software when $0 zap solves it.
- **Cloneable module:** 3-source lead routing zap template → reusable for any local SMB with multi-channel inbound.

---

## Ledger Stats

| Metric | Total (seeded) |
|---|---|
| Wins logged | 4 |
| Total money saved | $10,740–$19,480 (estimated) |
| Total hours saved | 10–17 hours |
| Reusable modules generated | 4 |
| Verticals covered | Payments, AI Automation, HVAC, Local SD |

---

## Next Wins to Log

- [ ] Zapier webhook fix (technical operator)
- [ ] Twilio SMS delivery issue (developer / SMB)
- [ ] Credit card chargeback recovery
- [ ] Google Ads suspension recovery
- [ ] n8n agent memory configuration fix
