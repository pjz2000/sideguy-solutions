# SideGuy Intelligence Stack

## Installed tools

- tools/intelligence/priority-engine.sh
- tools/intelligence/news-radar.sh
- tools/intelligence/page-upgrader.sh
- tools/intelligence/run-intelligence.sh

## Purpose

Turn SideGuy from a page library into an operating intelligence system.

## Workflow

1. Run the full stack
2. Review the priority report
3. Upgrade top pages
4. Build 1-3 fresh signal pages
5. Repeat

## Commands

```bash
bash tools/intelligence/run-intelligence.sh .
bash tools/intelligence/page-upgrader.sh machine-to-machine-payments.html
cat logs/intelligence/priority-report.txt
cat logs/intelligence/news-radar.txt
cat data/intelligence/news-page-ideas.txt
```
