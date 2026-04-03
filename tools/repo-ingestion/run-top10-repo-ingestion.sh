#!/bin/bash

echo "=== SIDEGUY TOP 10 REPO INGESTION ENGINE ==="

DATE=$(date +"%Y-%m-%d")
OUT="docs/repo-intelligence/top10-repo-ingestion-$DATE.md"

cat > "$OUT" <<REPORT
# Top 10 Repo Ingestion Report ($DATE)

## Mission
Convert top GitHub AI / agent / workflow repos into SideGuy-native business modules.

## Watchlist
1. superpowers → workflow doctrine + skills registry
2. microsoft/agent-lightning → trainable routing + client agents
3. OpenBMB/ChatDev → multi-agent client teams
4. PaddleOCR → invoice / quote / PDF extraction
5. awesome-ai-agents → weekly radar feed
6. 500-AI-Agent-Projects → cheap vertical demo cloning
7. claude-flow → CPU terminal orchestration
8. sherlock → SMB presence audit
9. TaxHacker → cost leak detector
10. skills repos → per-client skill packs

## Extraction Template
For each repo:
- primitive:
- client use case:
- homepage trust angle:
- vertical deployment:
- SEO long-tail expansion:
- cloneable module:
- embedded intelligence use:

## Immediate SideGuy Modules
- AI Stack Clarity OS
- Client Skill Pack Registry
- Cost Leak Detector
- OCR Quote Audit
- Multi-Agent SMB Ops Team
- Contractor Dispatch AI
- HIPAA Workflow Parsing
- Payment Leakage Scanner
REPORT

echo "Report created at $OUT"

cat > data/repo-watchlists/top10-sideguy-watchlist.yaml <<YAML
frequency: weekly
goal: convert trending repos into business modules
top_priority:
  - superpowers
  - agent-lightning
  - ChatDev
  - PaddleOCR
  - skills-marketplaces
redeploy_targets:
  - homepage modules
  - client clone kits
  - local smb verticals
  - san diego trust pages
  - embedded intelligence packs
YAML

echo "Watchlist saved."
echo "=== INGESTION ENGINE READY ==="
