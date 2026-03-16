#!/bin/bash

TOPIC="$1"

if [ -z "$TOPIC" ]; then
  echo "Usage: ./tools/intelligence/auto-brief.sh \"topic name\""
  echo "Example: ./tools/intelligence/auto-brief.sh \"machine to machine payments\""
  exit
fi

slug=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
DATE=$(date +"%Y-%m-%d")
BRIEF="docs/briefs/$slug-brief.md"

score=0
category="general"
hub="index.html"
cta="Text PJ for help"
schema="FAQPage"

echo "$TOPIC" | grep -qi "AI\|agent\|automation" && score=$((score+4)) && category="ai-automation"
echo "$TOPIC" | grep -qi "payment\|payments\|stablecoin\|USDC\|settlement\|merchant" && score=$((score+5)) && category="payments"
echo "$TOPIC" | grep -qi "robotics\|machine-to-machine\|infrastructure\|API" && score=$((score+3)) && [ "$category" = "general" ] && category="future-infrastructure"
echo "$TOPIC" | grep -qi "local\|service\|business owner\|operator" && score=$((score+4))
echo "$TOPIC" | grep -qi "EV\|Tesla\|charging\|energy" && score=$((score+3)) && [ "$category" = "general" ] && category="energy"

case "$category" in
  payments)
    hub="payments.html"
    ;;
  ai-automation)
    hub="ai-automation.html"
    ;;
  future-infrastructure)
    hub="future-infrastructure.html"
    ;;
  energy)
    hub="energy.html"
    ;;
  *)
    hub="index.html"
    ;;
esac

cat <<EOF2 > "$BRIEF"
# SideGuy Auto-Brief

## Topic
$TOPIC

## Date
$DATE

## Slug
$slug

## Suggested URL
/$slug.html

## Category
$category

## Opportunity Score
$score

## Recommended Hub
$hub

## Purpose
Explain $TOPIC in calm, helpful, human language for business owners, operators, and curious normal people.

## SideGuy Angle
This page should help visitors understand what $TOPIC is, why it matters, where old systems struggle, what the future may look like, and when they may need human guidance.

## Audience
- small business owners
- operators
- non-technical decision makers
- future-curious normal people

## Page Structure
1. H1: What $TOPIC Is
2. Why It Matters
3. Real-World Examples
4. Why Traditional Systems Struggle
5. What Technologies Enable It
6. Benefits
7. Challenges / Risks
8. Future Outlook
9. FAQ
10. Text PJ CTA

## SEO Targets
- $TOPIC
- $TOPIC explained
- what is $TOPIC
- $TOPIC for business
- future of $TOPIC
- $TOPIC SideGuy guide

## Internal Link Suggestions
- link to $hub
- link to homepage
- link to related future infrastructure pages
- link to payments / AI / local operator pages when relevant

## CTA
$cta

## Schema
Use $schema schema with 4-6 strong FAQs.

## Writing Doctrine
- clarity before cost
- no hype
- no spam tone
- explain like a calm operator
- AI explains, human resolves

## Build Notes
After page creation:
1. add URL to sitemap.xml
2. add internal link from appropriate hub
3. add card/link on index.html if high priority
4. log to docs/signals/signal-log.md
EOF2

echo "Created brief:"
echo "$BRIEF"
