#!/bin/bash

SLUG="${1:-can-ai-agents-pay-for-apis}"
TITLE="${2:-Can AI Agents Pay for APIs?}"
OUT_DIR="${3:-logs/agent-page-seeds}"

mkdir -p "$OUT_DIR"
FILE="$OUT_DIR/$SLUG.txt"

cat > "$FILE" <<EOF2
TITLE: $TITLE
SLUG: $SLUG

INTRO:
Many people are hearing about AI agents, but fewer understand how those agents could actually pay for tools, APIs, compute, or data. This page explains the basic model in plain English.

SECTIONS:
- what the problem is
- what an AI agent does
- how pricing could work
- how payment rails fit in
- what trust and verification are needed
- when humans should stay in the loop

SIDEGUY ANGLE:
Clarity before cost.
Explain the system calmly.
Help people understand what is real, what is early, and what is still forming.
EOF2

echo "Built seed: $FILE"
