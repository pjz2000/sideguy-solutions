Claude,

Install and run the SideGuy Traffic Gravity Engine.

Steps:

1. Run tools/gravity/gravity-analyzer.sh
2. Review docs/gravity/gravity-report.txt
3. Run tools/gravity/gravity-booster.sh

Also available:

- tools/gravity/gravity-engine.sh — finds newest pages, recommends hub links
- tools/gravity/run-gravity.sh — runs analyzer + booster in sequence

Rules:

- append-only
- no page rewrites
- do not break existing HTML
- inject links before </body>

Goal:

Allow the strongest pages to accumulate internal authority.

Commit message:

Upgrade: content gravity linking
