#!/usr/bin/env bash

########################################
# QUICK REFERENCE CARD
# SideGuy Autopilot System
########################################

cat <<'EOF'

╔══════════════════════════════════════════════════════════════╗
║          SIDEGUY AUTOPILOT QUICK REFERENCE                   ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│ PREVIEW CHANGES (Dry Run)                                    │
└──────────────────────────────────────────────────────────────┘

  ./hyper-productize.sh              # Preview tool injections
  ./hyper-auto-adapt.sh              # Preview pattern replication
  ./autopilot-orchestrator.sh        # Preview full sequence


┌──────────────────────────────────────────────────────────────┐
│ APPLY CHANGES (Live Run)                                     │
└──────────────────────────────────────────────────────────────┘

  DRY_RUN=false ./hyper-productize.sh
  DRY_RUN=false ./hyper-auto-adapt.sh
  DRY_RUN=false ./autopilot-orchestrator.sh


┌──────────────────────────────────────────────────────────────┐
│ CUSTOM LIMITS                                                 │
└──────────────────────────────────────────────────────────────┘

  MAX_UPDATES=25 ./hyper-productize.sh          # Limit to 25 pages
  MIN_CLICKS=50 ./hyper-auto-adapt.sh           # Higher quality bar
  MAX_UPDATES=200 DRY_RUN=false ./script.sh     # Combine flags


┌──────────────────────────────────────────────────────────────┐
│ SELECTIVE PHASES (Orchestrator Only)                         │
└──────────────────────────────────────────────────────────────┘

  RUN_ADAPT=false ./autopilot-orchestrator.sh             # Skip adapt
  RUN_HYPER=false RUN_PRODUCTIZE=true ./autopilot.sh      # Only productize


┌──────────────────────────────────────────────────────────────┐
│ CHECK RESULTS                                                 │
└──────────────────────────────────────────────────────────────┘

  cat docs/hyper-productize/productize-report.md
  cat docs/auto-adapt/adapt-report.md
  cat docs/autopilot/runs/*/summary.md | tail -100


┌──────────────────────────────────────────────────────────────┐
│ TROUBLESHOOTING                                               │
└──────────────────────────────────────────────────────────────┘

  # Check if CSV exists
  ls -lh docs/gsc/query-pages.csv

  # See what pages already have tools
  grep -c "data-sg-productized" *.html

  # See what pages already adapted
  grep -c "data-auto-adapt" *.html

  # View recent logs
  tail -50 docs/hyper-productize/productize-log.txt


┌──────────────────────────────────────────────────────────────┐
│ SAFETY DEFAULTS                                               │
└──────────────────────────────────────────────────────────────┘

  DRY_RUN          = true     (preview only)
  MAX_UPDATES      = 50       (productize)
  MAX_UPDATES      = 100      (auto-adapt)
  RUN_ADAPT        = false    (orchestrator)
  MIN_CLICKS       = 20       (auto-adapt)
  MIN_IMPRESSIONS  = 300      (auto-adapt)


┌──────────────────────────────────────────────────────────────┐
│ WHAT EACH SCRIPT DOES                                         │
└──────────────────────────────────────────────────────────────┘

  hyper-productize.sh
    → Injects calculators, decision widgets based on query intent
    → Uses: data-sg-productized marker
    → Conservative: 50 page default limit

  hyper-auto-adapt.sh
    → Detects winning patterns from GSC
    → Applies patterns globally to similar pages
    → Uses: data-auto-adapt marker
    → Aggressive: 100 page default limit

  autopilot-orchestrator.sh
    → Runs all engines in sequence
    → Generates unified report
    → Coordinates sitemap updates
    → Disabled adapt by default


┌──────────────────────────────────────────────────────────────┐
│ WORKFLOW EXAMPLE                                              │
└──────────────────────────────────────────────────────────────┘

  # 1. Get fresh GSC data
  # Performance > Pages > Export > save to docs/gsc/query-pages.csv

  # 2. Preview changes
  ./autopilot-orchestrator.sh

  # 3. Review reports
  cat docs/autopilot/runs/*/summary.md | less

  # 4. Test on small batch
  MAX_UPDATES=10 DRY_RUN=false ./hyper-productize.sh

  # 5. Validate 5-10 pages manually
  # Check: tools render, copy is calm, mobile works

  # 6. If good, expand
  MAX_UPDATES=100 DRY_RUN=false ./hyper-productize.sh

  # 7. Monitor GSC for 2-4 weeks
  # Watch: CTR, time on page, positions


┌──────────────────────────────────────────────────────────────┐
│ DECISION GATES (Human Review Required)                       │
└──────────────────────────────────────────────────────────────┘

  Before first live run:
    ☐ Validate tool copy matches SideGuy tone
    ☐ Test tools on sample pages
    ☐ Confirm GSC data is recent (<7 days)

  After each live run:
    ☐ Spot-check 10-20 modified pages
    ☐ Verify no duplicate injections
    ☐ Check mobile rendering

  Before global auto-adapt:
    ☐ Identify winning patterns manually first
    ☐ Validate pattern quality
    ☐ Set conservative thresholds


┌──────────────────────────────────────────────────────────────┐
│ FILES & LOCATIONS                                             │
└──────────────────────────────────────────────────────────────┘

  Scripts:
    ./hyper-productize.sh
    ./hyper-auto-adapt.sh
    ./autopilot-orchestrator.sh

  Input data:
    docs/gsc/query-pages.csv          (from Google Search Console)

  Output:
    docs/hyper-productize/productize-report.md
    docs/auto-adapt/adapt-report.md
    docs/autopilot/runs/[timestamp]/summary.md

  Logs:
    docs/hyper-productize/productize-log.txt
    docs/auto-adapt/adapt-log.txt
    docs/autopilot/runs/[timestamp]/autopilot.log


┌──────────────────────────────────────────────────────────────┐
│ PHILOSOPHY REMINDER                                           │
└──────────────────────────────────────────────────────────────┘

  This automation amplifies human judgment, not replaces it.

  • Data-driven (real GSC queries)
  • Pattern-based (replicate what works)
  • Reversible (git tracks everything)
  • Transparent (full audit trails)
  • Conservative (dry-run defaults)

  SideGuy is a calm place for stressed people.
  Every automated change should reduce confusion.


╔══════════════════════════════════════════════════════════════╗
║  Need help? Text PJ → 773-544-1231                           ║
╚══════════════════════════════════════════════════════════════╝

EOF
