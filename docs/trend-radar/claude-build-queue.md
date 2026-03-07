# Claude Build Queue

Use `docs/trend-radar/radar-report.md` as the daily source of truth.

## Build Rules

- Prioritize **money-pain** and **diagnostic** pages first (highest scores)
- Prefer SideGuy-style real-world queries — plain English, problem-first
- Create pages from the existing template system (`_template.html`)
- Append only — no rewrites, no reordering
- Do not delete existing pages
- Add each new URL to `sitemap.xml` only after the file exists and has real content

## Build Order

1. `payments` — highest commercial intent
2. `ai-software` — growing search volume
3. `home-operator` — proven indexed (dishwasher, drafty windows already crawled)
4. `future-industries` — plant early, low competition
5. `signal-lab` — experimental, build last

## SideGuy Lens

> Google discovers the problem  
> AI explains it  
> A real human resolves it

## Page Quality Checklist

- [ ] Unique `<title>` — problem-first, "· San Diego · SideGuy"
- [ ] Meta description — 140-155 chars, no hype, actionable
- [ ] H1 — plain language version of the problem
- [ ] At minimum: what to check first, who to call, what it costs
- [ ] `canonical` tag pointing to `https://sideguysolutions.com/<slug>.html`
- [ ] `robots` set to `index, follow`
- [ ] Internal link to relevant hub page
