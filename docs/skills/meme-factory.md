# Skill: Meme Factory
**Version:** 1.0 · Append-only doctrine
**Purpose:** Format operator trench stories as memes that build human trust, drive engagement, and link back to SideGuy service pages.

---

## The Meme Formula

Every SideGuy meme has two lines:

```
TOP:    The situation (operator trench story, first person, present tense)
BOTTOM: The clarity (what actually happened / what it means / the lesson)
```

Followed by one link: `[Verb] → /relevant-page.html`

---

## Trench Story Formatting Rules

**TOP line rules:**
- First person or direct observation — "I", "We", "Client", "Competitor"
- Present tense or recent past ("called me", "ran my workflow", "quoted $14k")
- Specific numbers — $4,200 / 47 times / $0.02 per call / 3am
- One setup, no resolution — the bottom line delivers the punchline/lesson
- 15–25 words max
- No hashtags, no emojis in the text (emojis can be in the card UI wrapper)

**BOTTOM line rules:**
- Delivers the insight the operator didn't know before
- Names the real cause, the real solution, or the real dynamic
- Can be slightly wry but never mean — the target is the system, not the person
- References a SideGuy concept, page, or tool where possible
- 15–25 words max

---

## Operator Humor Rules

**What works:**
- Specificity — "$340/month in software I haven't opened since 2023" beats "expensive software"
- Relatability — every operator has been here, they should recognize themselves
- The gap between what you were told and what was true — "nobody told you because it pays less commission"
- Institutional absurdity — processors, platforms, agencies, AI chatbots behaving badly
- The quiet win — fixing something massive in 4 minutes

**What doesn't work:**
- Punching at the client or the operator — they're the hero, not the butt
- Vague frustration — "software is so expensive" is boring
- Jargon without translation — if you use "interchange-plus" in the meme, define it in the bottom line
- Trying to be funny — the humor comes from truth and specificity, not jokes

---

## Human Trust Signals

Every meme should contain at least one:
- **Real number** ($, %, time, count)
- **Specific tool or vendor name** (Zapier, Stripe, ChatGPT, HVAC tech)
- **Operator recognition moment** — "yes, this is exactly what happened to me"
- **Implicit PJ presence** — "PJ said check the capacitor" / "we looked at it for 4 minutes"

The trust comes from: *this person has actually seen this problem before.*

---

## Meme-to-Service Relevance

Every meme links to exactly one page. Match the meme topic to the page:

| Meme topic | Link target |
|---|---|
| Payment processor holds / fees | `/stripe-vs-square.html` or `/how-credit-card-processing-fees-work.html` |
| Zapier / automation failure | `/problems/quick-fix-for-zapier-task-failed-webhook-timeout.html` |
| AI chatbot gone wrong | `/ai-automation-consulting-san-diego.html` |
| HVAC oversell | `/pages/expansion/hvac-repair-repair-vs-replace.html` |
| SaaS subscription waste | Nearest operator tools page |
| Google Ads confusion | `/authority/google-ads.html` |
| Invoice / quote confusion | `/ai-quote-audit-contractor-pdf.html` (when built) |

**Link CTA verb patterns:**
- Fix it →
- See the math →
- Full story →
- Real talk →
- Audit yours →
- See the move →
- See what works →

---

## Vertical Coverage Targets

Aim for balanced vertical coverage across the meme grid (8–12 memes per grid):

| Vertical | Target memes | Current count |
|---|---|---|
| Payments | 2–3 | 2 (Amex fees, processor hold) |
| AI automation | 2–3 | 2 (chatbot apology, Zapier billing) |
| HVAC | 1–2 | 1 (capacitor) |
| SaaS/tools | 1–2 | 1 ($200/month 8 tools) |
| Invoicing/workflow | 1 | 1 (ChatGPT invoice email) |
| Ads/marketing | 1 | 1 (Facebook ads reach) |

---

## Writing Process

1. Start with the real situation — something that actually happened or a real GSC query pattern
2. Write the TOP line first — the setup, raw and specific
3. Write the BOTTOM line — the reveal, the lesson, the SideGuy frame
4. Pick the link — match to nearest service page
5. Pick the CTA verb — action-forward, 2 words max
6. Read aloud — if it doesn't land in one pass, rewrite the bottom line

---

## Example Memes (Reference)

**Payments:**
> Client paid with Amex. Processor charged 3.5%. Great meeting, no profit.
> Interchange-plus pricing exists. Nobody told you because it pays less commission.
> `See the math → /stripe-vs-square.html`

**AI Automation:**
> Built an AI chatbot for my business. It apologized to customers for 8 hours straight.
> Automation without configuration is just a new way to fail at scale.
> `Fix yours → /ai-automation-consulting-san-diego.html`

**HVAC:**
> Three HVAC quotes: $8k, $12k, $14k. PJ said check the capacitor. $400 later, fixed.
> Always get a second opinion before a second mortgage.
> `Full story → /memes/index.html#h1`

**SaaS:**
> Spent $200/month on software tools. Use 2 of them. The other 8 send "we miss you" emails.
> SaaS subscriptions are a gym membership business model and you are January.
> `Audit yours → /memes/index.html#a3`

**Zapier:**
> Zapier ran my workflow 47 times at 3am. Every run failed. Still charged per task.
> Automation is great until it automates your billing for errors you didn't fix.
> `Fix it → /problems/quick-fix-for-zapier-task-failed-webhook-timeout.html`

---

## Meme Factory Checklist

```
[ ] Identify real operator situation (GSC signal, client story, or trench pattern)
[ ] Write TOP line — specific, present tense, under 25 words
[ ] Write BOTTOM line — lesson/reveal, names the dynamic, under 25 words
[ ] Pick link target — nearest relevant service page
[ ] Pick CTA verb — 2 words, action forward
[ ] Check vertical coverage — fill gaps before repeating verticals
[ ] Add to /memes/index.html grid
[ ] Add to homepage meme strip if grid slot open
[ ] Commit: feat: meme factory — [vertical] [meme topic]
```
