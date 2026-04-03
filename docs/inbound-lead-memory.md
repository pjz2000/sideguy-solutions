# SideGuy Inbound Lead Memory Pipeline

Every inbound contact gets logged here. Pattern recognition compounds over time — the 10th HVAC question is faster than the first because the module already exists.

---

## Template

```
- Date:
- Inbound source:        (text / GSC / referral / DM / form)
- First 10 words:
- Likely vertical:       (payments / AI automation / HVAC / local SD / future tech / other)
- Urgency score:         (1 = curious · 3 = active problem · 5 = bleeding money now)
- Classification:        (ready now / needs proof / not yet–nurture)
- Recommended next move:
- Future reusable insight:
```

---

## Urgency Score Guide

| Score | Signal | Response Time |
|---|---|---|
| 1 | Browsing, no stated problem | 48–72h nurture |
| 2 | Has a question, low stakes | 24h, one good answer |
| 3 | Active problem, looking for direction | Same day |
| 4 | Problem costing money now | Within hours |
| 5 | Bleeding / urgent / can't wait | Immediate Text PJ |

---

## Classification Guide

| Class | Signal | Next Move |
|---|---|---|
| **Ready now** | Clear problem + budget signal + urgency 3–5 | Respond same day, offer 10-min call or text thread |
| **Needs proof** | Interested but skeptical, wants to see a win first | Send one relevant win from client-wins-ledger.md |
| **Not yet / nurture** | Early stage, no urgency, wrong timing | Add to nurture list, check back in 30 days |

---

## Pipeline Log

### Lead 001 — Seed Entry

- **Date:** 2026-04-03
- **Inbound source:** GSC organic (zapier webhook timeout)
- **First 10 words:** "zapier webhook timing out, zap fails every time it runs"
- **Likely vertical:** AI Automation / Workflow
- **Urgency score:** 4 — automation is broken, work is stopped
- **Classification:** Ready now
- **Recommended next move:** Send `/problems/quick-fix-for-zapier-task-failed-webhook-timeout.html` + offer a 10-min text thread to diagnose specific endpoint
- **Future reusable insight:** Webhook timeout queries at position 4.91 — this is a near-page-1 signal. Every organic visitor on this query has an active broken zap. High urgency = high conversion potential.

---

### Lead 002 — Seed Entry

- **Date:** 2026-04-03
- **Inbound source:** GSC organic (twilio sms not delivering)
- **First 10 words:** "twilio messages show delivered but recipient never gets them"
- **Likely vertical:** AI Automation / Developer tools
- **Urgency score:** 4 — SMS system broken, leads or notifications not arriving
- **Classification:** Ready now
- **Recommended next move:** Send `/problems/twilio-sms-not-delivering-in-2026.html` + ask "is this sending to one carrier or all carriers?" — narrows root cause in one text
- **Future reusable insight:** "Delivered but not received" = carrier filtering issue 80% of the time. The diagnostic question is the value, not a long answer.

---

### Lead 003 — Seed Entry

- **Date:** 2026-04-03
- **Inbound source:** GSC organic (stripe vs square fees)
- **First 10 words:** "we're paying too much in processing fees, don't know why"
- **Likely vertical:** Payments
- **Urgency score:** 3 — ongoing cost leak, not emergency
- **Classification:** Needs proof
- **Recommended next move:** Ask for monthly volume + current processor. Run 2-minute fee comparison. Send result with `/how-credit-card-processing-fees-work.html`
- **Future reusable insight:** "Paying too much" without knowing why = interchange-plus conversation. One question (what's your monthly volume?) qualifies immediately.

---

### Lead 004 — Seed Entry

- **Date:** 2026-04-03
- **Inbound source:** Text / referral (North County SD)
- **First 10 words:** "got three HVAC quotes, huge range, don't know who to trust"
- **Likely vertical:** HVAC / Home Systems
- **Urgency score:** 3 — has quotes in hand, about to make decision
- **Classification:** Ready now
- **Recommended next move:** Ask for the quote range and unit age. Apply repair-vs-replace framework from Win 003. Send one-line verdict via text.
- **Future reusable insight:** "Huge range in quotes" = diagnostic oversell pattern. The right question ("how old is the unit and what refrigerant does it use?") closes this in 5 minutes.

---

## Pattern Library (grows with each entry)

| Pattern | Vertical | Conversion Signal | Module |
|---|---|---|---|
| "Timing out / failing every run" | AI Automation | High — active break | zapier-webhook page |
| "Delivered but not received" | Automation / Dev | High — system broken | twilio-sms page |
| "Paying too much in fees" | Payments | Medium — cost awareness | stripe-vs-square page |
| "Three quotes, huge range" | HVAC | High — decision imminent | HVAC clarity framework |
| "My AI keeps forgetting" | AI Automation | Medium — frustration | n8n memory page |
