# SHIP: Authority Stack + Hub Network

## Objective
Upgrade SideGuy from "good project site" into a more obvious platform by adding six foundational pages:

1. how-sideguy-works.html
2. about-pj.html
3. sideguy-mission.html
4. payments-hub.html
5. automation-hub.html
6. operator-help-hub.html

These pages should strengthen trust, improve internal linking, clarify positioning, and give Google cleaner site architecture.

---

## Core Brand Rules
Keep the existing SideGuy tone:

- calm
- premium but human
- clarity before cost
- no fake urgency
- no hype language
- real person available
- local / operator / practical framing

Always preserve:

- Text PJ orb
- Back to Home link
- strong internal linking
- clean title + meta description
- canonical tag
- helpful H1
- useful intro paragraphs
- sectioned content
- local trust feel

Phone number for Text PJ orb:
773-544-1231

---

## Global Positioning Line
Use this exact line prominently where it fits:

**SideGuy is where Google discovers the problem, AI explains it, and a real human resolves it.**

Also work in:
**Clarity before cost**

---

## Design Direction
Use the current best SideGuy aesthetic, but make these pages feel more premium:

- ocean-light / coastal fintech / Solana-adjacent energy
- soft glow
- subtle gradients
- clear cards
- premium spacing
- consistent buttons
- clean section rhythm
- no giant walls of text

---

## Page Requirements

### 1) how-sideguy-works.html
Purpose:
Explain the SideGuy operating model in the simplest possible way.

Required sections:
- Hero: How SideGuy Works
- 3-step flow:
  - Google finds the problem
  - AI explains the options
  - PJ helps you make the right call
- Why this works better than random search
- Clarity before cost section
- Human + AI explanation section
- Payments / automation / operator outcomes section
- CTA with Text PJ orb

Suggested internal links:
- payments-hub.html
- automation-hub.html
- operator-help-hub.html
- sideguy-mission.html
- about-pj.html

---

### 2) about-pj.html
Purpose:
Make the site more human and trustworthy.

Required sections:
- Hero: About PJ
- Calm operator intro
- Hospitality + tech + real-world problem solving background
- Why SideGuy exists
- How PJ helps
- What kinds of problems SideGuy is good at
- Why human judgment still matters
- CTA with Text PJ orb

Tone:
Warm, grounded, authentic, no corporate bio nonsense.

Suggested internal links:
- how-sideguy-works.html
- sideguy-mission.html
- operator-help-hub.html
- payments-hub.html

---

### 3) sideguy-mission.html
Purpose:
Frame SideGuy as a bigger platform, not just a services page collection.

Required sections:
- Hero: The SideGuy Mission
- Core statement: human resolution layer over the web
- Why the internet needs clarity
- Why AI alone is not enough
- Why local operators still matter
- Why payments + automation + human support belong together
- Long-term vision: trusted problem-resolution network
- CTA with Text PJ orb

Suggested internal links:
- how-sideguy-works.html
- about-pj.html
- payments-hub.html
- automation-hub.html
- operator-help-hub.html

---

### 4) payments-hub.html
Purpose:
Create the parent hub for all payments pages.

Required sections:
- Hero: Payments Hub
- Intro explaining SideGuy Payments
- Savings / settlement / control overview
- Featured cards linking to existing payment pages
- Local business angle
- Solana / USDC / instant settlement explanation
- Calculator and comparison callouts
- CTA with Text PJ orb

Suggested child links if they exist:
- local-business-payments-san-diego.html
- solana-payments-san-diego.html
- Carlsbad-Contractor-Payments.html
- any Stripe fee / calculator / payments pages in repo

---

### 5) automation-hub.html
Purpose:
Create the parent hub for all automation pages.

Required sections:
- Hero: Automation Hub
- Intro for AI + operator workflows
- What automation helps with
- Cards linking to existing AI / business tools pages
- Why SideGuy is human-first automation
- Future-forward section for machine-to-machine systems
- CTA with Text PJ orb

Suggested child links if they exist:
- ai-business-tools-san-diego.html
- fintech-software-san-diego.html
- related software / workflow / AI pages

---

### 6) operator-help-hub.html
Purpose:
Create the parent hub for practical human-help pages.

Required sections:
- Hero: Operator Help Hub
- Calm intro for real-world problem solving
- Categories of problems SideGuy helps with
- Decision support framing
- Human resolution / first-step guidance
- Cards to practical pages across the site
- CTA with Text PJ orb

Suggested link types:
- local service pages
- software pages
- payment troubleshooting pages
- practical problem pages

---

## Homepage Upgrade Requirement
Update index.html append-only and add a new section near the top third of the homepage:

### Section title:
**Explore the SideGuy System**

Include six cards linking to:
- How SideGuy Works
- About PJ
- SideGuy Mission
- Payments Hub
- Automation Hub
- Operator Help Hub

Section intro should make it obvious that SideGuy is not just a service page site — it is a structured problem-solving system.

---

## Sitemap Requirement
Append all six URLs to sitemap.xml.

If there are multiple sitemap files, append to the primary live sitemap and any relevant html/xml structure already used by the repo.

---

## Internal Linking Requirement
Each of the six new pages must:
- link to at least 4 existing relevant pages
- link back to homepage
- cross-link to the other authority/hub pages where appropriate

Also update a handful of strong existing pages to link back into the new hubs:
- homepage
- best payments page
- best automation page
- best operator/problem page

Goal:
Create a visible internal-link ring.

---

## Technical Rules
- append-only
- use existing best SideGuy template / structure
- no mass rewrites
- no deleting content
- no reordering large blocks unless needed
- preserve current branding
- keep files production-safe
- commit only after implementation is complete and reviewed locally

---

## Commit Message
Use:

Build: authority stack + hub network pages with homepage and sitemap integration

