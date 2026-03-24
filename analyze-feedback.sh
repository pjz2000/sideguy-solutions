#!/usr/bin/env bash

########################################
# SIDEGUY FEEDBACK ANALYZER v1
# Patterns from real human interactions
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit

FEEDBACK_CSV="docs/pj-feedback/feedback-log.csv"
REPORT_DIR="docs/pj-feedback/reports"
DATE="$(date +"%Y-%m-%d-%H%M%S")"
REPORT="$REPORT_DIR/analysis-$DATE.md"

mkdir -p "$REPORT_DIR"

echo "---------------------------------------"
echo "📊 FEEDBACK ANALYZER"
echo "---------------------------------------"

if [ ! -f "$FEEDBACK_CSV" ]; then
  echo "No feedback log found at: $FEEDBACK_CSV"
  exit 1
fi

TOTAL=$(tail -n +2 "$FEEDBACK_CSV" | wc -l)

if [ "$TOTAL" -eq 0 ]; then
  echo "No feedback entries yet"
  exit 0
fi

echo "Total feedback entries: $TOTAL"

########################################
# GENERATE REPORT
########################################

python3 - <<PY
import csv
from collections import Counter, defaultdict
from pathlib import Path

feedback_path = Path("$FEEDBACK_CSV")
rows = []

with feedback_path.open() as f:
    reader = csv.DictReader(f)
    rows = list(reader)

if not rows:
    print("No data to analyze")
    exit(0)

# Count by category
intent_counts = Counter(r["intent"] for r in rows)
outcome_counts = Counter(r["outcome"] for r in rows)
confusion_themes = Counter(r["confusion"].lower()[:50] for r in rows if r["confusion"])

# Page frequency
page_counts = Counter(r["page"] for r in rows)
top_pages = page_counts.most_common(10)

# Confusion by intent
confusion_by_intent = defaultdict(list)
for r in rows:
    if r["confusion"]:
        confusion_by_intent[r["intent"]].append(r["confusion"])

# Build report
report = f"""# SideGuy Feedback Analysis

**Generated:** {Path("$REPORT").name.replace("analysis-", "").replace(".md", "")}  
**Total Entries:** {len(rows)}

---

## Intent Distribution

"""

for intent, count in intent_counts.most_common():
    pct = (count / len(rows)) * 100
    report += f"- **{intent}**: {count} ({pct:.1f}%)\n"

report += f"""

---

## Outcome Distribution

"""

for outcome, count in outcome_counts.most_common():
    pct = (count / len(rows)) * 100
    report += f"- **{outcome}**: {count} ({pct:.1f}%)\n"

report += f"""

---

## Top Pages (by feedback volume)

"""

for page, count in top_pages:
    report += f"- {page} — {count} feedback entries\n"

report += f"""

---

## Common Confusion Themes

"""

for theme, count in confusion_themes.most_common(15):
    if len(theme.strip()) > 5:
        report += f"- "{theme}" ({count})\n"

report += f"""

---

## Confusion by Intent

"""

for intent in sorted(confusion_by_intent.keys()):
    report += f"\n### {intent.title()}\n\n"
    for conf in confusion_by_intent[intent][:5]:
        report += f"- {conf}\n"

report += f"""

---

## Recommended Actions

Based on this feedback:

1. **Pages needing attention:** {", ".join(p for p, c in top_pages[:3])}
2. **High-confusion intents:** {", ".join(i for i, c in intent_counts.most_common(3))}
3. **Outcome to improve:** {outcome_counts.most_common(1)[0][0] if outcome_counts else "N/A"}

---

## Next Steps

- Review top confusion themes
- Check if blocks address common questions
- Test pages with highest feedback volume
- Consider manual rewrites for persistent confusion
"""

Path("$REPORT").write_text(report)
print(f"✅ Report generated: $REPORT")

PY

cat "$REPORT"
