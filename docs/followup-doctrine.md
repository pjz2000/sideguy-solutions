# SideGuy Follow-Up Doctrine

Simple, repeatable. Three pathways. No guessing.

---

## Pathway A — Ready Now

**Signal:** Clear problem + urgency score 3–5 + budget or timeline mentioned

### Response Style
Direct. One sentence on the problem, one sentence on the fix, one sentence on next step. No preamble. No "great to hear from you." Get to the answer in the first line.

### What to Send
1. One relevant clarity page link (from problems/, hubs/, or decisions/)
2. One sentence framing what usually causes this
3. One question that confirms the root cause
4. Text PJ option if they want to go faster

**Example:**
> "Webhook timeouts are almost always a slow endpoint response. Is the URL you're hitting an internal server or a third-party API? That narrows it to one of 3 fixes — I can walk through it in 10 minutes if easier. [link]"

### When to Follow Up
- If no response: once at 48h with a single sentence ("Did the fix work or still stuck?")
- If replied: continue thread until resolved or handed off

### Module to Reuse
- Match to nearest problem page in `/problems/`
- If no page exists → log in inbound-lead-memory.md → that pattern becomes the next page

### Escalate to Text PJ When
- Urgency 5 (money flowing out now)
- Problem requires account access, vendor call, or decision under time pressure
- Client is a potential anchor tenant (high volume, multi-vertical, referral potential)

---

## Pathway B — Needs Proof

**Signal:** Interested but asking "how do you actually help" or "what's the cost" without a specific problem stated

### Response Style
Lead with a win, not a pitch. One relevant result from the client wins ledger. Keep it specific — real numbers, real timeline, real outcome. Don't explain the process, show the result.

### What to Send
1. One win from `docs/client-wins-ledger.md` relevant to their vertical
2. One line: "Similar situation?" 
3. If yes → move to Pathway A flow

**Example:**
> "Last week: operator paying 2.9% flat on $18k/month. Moved to interchange-plus, saves ~$280/month, took 10 minutes to negotiate with their processor. Similar situation? [stripe-vs-square link]"

### When to Follow Up
- First follow-up: 72h — send a second win from a different vertical
- Second follow-up: 7 days — one line, no pitch ("Anything shift on the [problem] front?")
- Third: 30 days — requalify or move to nurture list

### Module to Reuse
- Client wins ledger → pick the most dollar-specific relevant win
- If no matching win exists → use the nearest GSC winner page as social proof (real Google demand = real problem prevalence)

### Escalate to Text PJ When
- They've seen 2 wins and are still asking questions — they want a conversation, not content
- They mention a specific dollar amount or deadline

---

## Pathway C — Not Yet / Future Nurture

**Signal:** Urgency 1–2, no immediate problem, "just exploring," timing is wrong

### Response Style
One sentence of value, no ask. Leave them with something useful they didn't have before. Don't follow up immediately — they'll feel the pressure and disengage.

### What to Send
1. One relevant page link with a single useful framing line
2. No CTA, no ask, no "let me know if you need anything"

**Example:**
> "For when the timing is right — most operators don't know interchange-plus exists until they've overpaid for 2 years. [link] — no rush."

### When to Follow Up
- 30 days: one relevant signal ("GSC is routing [their vertical] queries to SideGuy — seeing real demand for this")
- 60 days: one new win from their vertical
- 90 days: requalify ("Has anything changed on the [problem] front?")
- If still cold at 90 days: quarterly check-in only

### Module to Reuse
- Add to a vertical-specific nurture sequence in `data/drip/state.json` if exists
- Tag in inbound-lead-memory.md with "nurture" + next contact date

### Escalate to Text PJ When
- They re-engage with a specific problem after nurture — this is a warm signal, prioritize immediately

---

## Universal Rules

1. **Answer first.** Every response leads with the answer or the most useful framing. Never lead with process.
2. **One link max.** More than one link = diluted attention = no action.
3. **Specific beats general.** "$280/month saved" beats "we help with payments."
4. **Short wins.** If the response is more than 5 sentences, cut it.
5. **The follow-up is one sentence.** "Did the fix work?" "Still stuck on this?" "Anything shift?"
6. **Every win gets logged.** Even a "thanks, that fixed it" is a win. Log it.
7. **Text PJ is the upgrade path.** Every pathway ends with a natural escalation to direct human contact. That's the product.

---

## Module Cross-Reference

| Pathway | Primary Module | Backup Module |
|---|---|---|
| A — Ready Now | `/problems/` page matching symptom | `docs/client-wins-ledger.md` Win matching vertical |
| B — Needs Proof | `docs/client-wins-ledger.md` Win | Nearest GSC winner page (impressions as social proof) |
| C — Nurture | GSC winner page for their vertical | `docs/inbound-lead-memory.md` pattern library |
