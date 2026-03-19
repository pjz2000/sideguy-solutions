#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"

cd "$PROJECT_ROOT" || exit 1

mkdir -p docs/problem-universe
mkdir -p seo-reserve/problem-universe

########################################
# README
########################################

if [ ! -f docs/problem-universe/README.md ]; then
cat > docs/problem-universe/README.md <<'EOF'
# SideGuy Problem Universe

Purpose:
Map the real-world problems people encounter so SideGuy can
translate confusion into clarity and action.

Framework:

Problem appears
→ explanation
→ option comparison
→ human guidance
→ execution

The Problem Universe allows SideGuy to scale content while
remaining focused on real problems.

Core philosophy:

AI explains.
Humans decide.
SideGuy helps execute.

Clarity before cost.
EOF
echo "[✓] docs/problem-universe/README.md"
else
echo "[SKIP] docs/problem-universe/README.md (exists)"
fi

########################################
# PROBLEM CLUSTERS
########################################

if [ ! -f docs/problem-universe/problem-clusters.md ]; then
cat > docs/problem-universe/problem-clusters.md <<'EOF'
# Problem Universe Clusters

SideGuy organizes problems into clusters.

Each cluster can expand into hundreds of specific problems.

Example structure:

Cluster
→ Sub-cluster
→ Specific problem

Example:

Home Systems
→ HVAC
→ Should I repair or replace my AC?

Home Systems
→ Energy
→ Should I install solar batteries?

Business Operations
→ Payments
→ Which payment processor should I use?

Technology Decisions
→ AI Automation
→ Is AI automation worth it for my business?
EOF
echo "[✓] docs/problem-universe/problem-clusters.md"
else
echo "[SKIP] docs/problem-universe/problem-clusters.md (exists)"
fi

########################################
# SEO RESERVE MANIFEST
########################################

if [ ! -f seo-reserve/problem-universe/problem-universe-manifest.md ]; then
cat > seo-reserve/problem-universe/problem-universe-manifest.md <<'EOF'
# Problem Universe Master Clusters

home-systems
energy-decisions
contractor-decisions
smart-home-technology
hvac-problems
solar-battery-decisions
plumbing-problems
electrical-upgrades

business-operations
payment-processing-decisions
software-stack-decisions
automation-opportunities
vendor-comparison

technology-confusion
ai-tool-decisions
robotics-adoption
future-technology-questions
digital-security-decisions

mobility-decisions
ev-charger-installation
vehicle-technology-questions

local-service-confusion
contractor-selection
service-cost-questions

life-optimization
productivity-systems
digital-tool-overload
EOF
echo "[✓] seo-reserve/problem-universe/problem-universe-manifest.md"
else
echo "[SKIP] seo-reserve/problem-universe/problem-universe-manifest.md (exists)"
fi

########################################
# SCALING MODEL
########################################

if [ ! -f docs/problem-universe/scaling-model.md ]; then
cat > docs/problem-universe/scaling-model.md <<'EOF'
# Problem Universe Scaling Model

Example scaling structure:

50 clusters
→ 20 sub-clusters each
→ 20 specific problems each

Result:

50 × 20 × 20 = 20,000 problem pages

Add location modifiers:

20,000 × 20 cities = 400,000 pages

Add comparison / guide pages:

400,000+ total possible pages

The key rule:

Every page must represent a real problem
someone searches for.

SideGuy expands by solving real confusion,
not by generating random content.
EOF
echo "[✓] docs/problem-universe/scaling-model.md"
else
echo "[SKIP] docs/problem-universe/scaling-model.md (exists)"
fi

echo ""
echo "SideGuy Problem Universe installed."
echo "Created directories:"
echo "  docs/problem-universe"
echo "  seo-reserve/problem-universe"
echo ""
echo "Problem clusters ready for expansion."
