Claude,

Implement the authority stack and hub network described in:

- docs/preproduction/authority-stack-ship.md
- docs/manifests/authority-stack-pages.json

## Execution Rules
- Work inside the existing SideGuy site structure
- Use the current best live page style as your visual model
- Prefer existing reusable sections/classes/components if present
- Keep everything append-only
- Do not delete content
- Do not refactor the whole site
- Do not ship placeholder text
- Build real, useful copy

## Required Outputs
Create these pages:
- how-sideguy-works.html
- about-pj.html
- sideguy-mission.html
- payments-hub.html
- automation-hub.html
- operator-help-hub.html

Then:
1. append all six pages into sitemap.xml
2. append a six-card "Explore the SideGuy System" section into index.html
3. cross-link the pages intelligently
4. preserve or improve the Text PJ orb on every new page
5. verify titles, canonicals, H1s, and meta descriptions are present

## Copy Guidance
Use premium calm operator voice.
No fluff.
No corporate jargon.
No fake urgency.
Make the pages feel like a trustworthy system.

## Important positioning lines
Use these where helpful:
- SideGuy is where Google discovers the problem, AI explains it, and a real human resolves it.
- Clarity before cost.

## Final step
After implementation, run a quick local check of file existence and grep the new filenames inside index.html and sitemap.xml, then commit with:

Build: authority stack + hub network pages with homepage and sitemap integration
