#!/bin/bash

SLUG="${1:-self-improving-agent-skills}"
TITLE="${2:-Self-Improving Agent Skills Explained}"
OUT_DIR="${3:-logs/future-ai-seeds}"

mkdir -p "$OUT_DIR"
FILE="$OUT_DIR/$SLUG.txt"

cat > "$FILE" <<EOF2
TITLE: $TITLE
SLUG: $SLUG

ANGLE:
Explain how AI agents can iteratively improve workflows, code, prompts, or instructions through repeated feedback loops.

SECTIONS:
- what self-improving agent skills are
- how baseline instructions work
- why iteration loops matter
- how evaluation and testing fit in
- where humans still matter
- practical business use cases
- risks and guardrails
- future outlook

SIDEGUY POSITIONING:
SideGuy explains future systems calmly.
No hype.
No panic.
Just clear explanation of what is real, what is useful, and where human oversight still matters.

LINK OUT TO:
- /autonomous-agent-economy-explained.html
- /mcp-tools-for-business.html
- /human-confirmed-ai.html
- /distributed-intelligence-for-business.html
EOF2

echo "Built seed: $FILE"
