#!/usr/bin/env bash

########################################
# SIDEGUY RESOLUTION ANALYTICS v2
# BEEF BLOCK ESCALATION + TRUST + MONEY SIGNALS
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

DATE="$(date +"%F")"
STAMP="$(date +"%Y%m%d-%H%M%S")"

DOCS_DIR="docs"
OS_DIR="$DOCS_DIR/sideguy-os"
COMPONENT_DIR="$OS_DIR/components"
REPORT_DIR="$OS_DIR/reports"

mkdir -p "$COMPONENT_DIR" "$REPORT_DIR"

LOG="$REPORT_DIR/resolution-analytics-$STAMP.md"
ANALYTICS_JS="$COMPONENT_DIR/sideguy-resolution-analytics.js"
DASHBOARD="resolution-analytics-dashboard.html"

echo "# SideGuy Resolution Analytics v2" > "$LOG"
echo "" >> "$LOG"
echo "Timestamp: $(date +"%Y-%m-%d %H:%M:%S")" >> "$LOG"
echo "" >> "$LOG"

########################################
# 1) ANALYTICS COMPONENT
########################################

cat > "$ANALYTICS_JS" <<'EOF'
(function () {
  function detectTopic(text) {
    const lower = (text || '').toLowerCase();
    if (/hvac|mini split|repair|replace|electrical|solar|battery|roof|plumbing/.test(lower)) return "home";
    if (/payment|payments|fees|subscription|pricing|processor|stripe|square|usdc|stablecoin/.test(lower)) return "money";
    if (/ai|automation|agent|workflow|gpt|claude|llm/.test(lower)) return "ai";
    if (/move|moving|relocation|san diego|rent|apartment|lifestyle/.test(lower)) return "life";
    if (/voice|robotics|future|prediction market|kalshi|signal/.test(lower)) return "future";
    return "general";
  }

  function trackBeefExposure() {
    const topic = detectTopic(document.body.innerText || '');
    const page = window.location.pathname;
    const record = {
      t: new Date().toISOString(),
      type: "exposure",
      topic,
      page
    };

    try {
      const existing = JSON.parse(localStorage.getItem("sg_resolution_analytics") || "[]");
      existing.push(record);
      localStorage.setItem("sg_resolution_analytics", JSON.stringify(existing));
    } catch(e) {}
  }

  function attachEscalationTracking() {
    const blocks = document.querySelectorAll(".sideguy-beef-block");
    blocks.forEach(block => {
      block.addEventListener("click", function () {
        const topic = detectTopic(document.body.innerText || '');
        const page = window.location.pathname;
        const record = {
          t: new Date().toISOString(),
          type: "escalation_click",
          topic,
          page
        };

        try {
          const existing = JSON.parse(localStorage.getItem("sg_resolution_analytics") || "[]");
          existing.push(record);
          localStorage.setItem("sg_resolution_analytics", JSON.stringify(existing));
        } catch(e) {}
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    trackBeefExposure();
    attachEscalationTracking();
  });
})();
EOF

echo "- Created analytics component: \`$ANALYTICS_JS\`" >> "$LOG"

########################################
# 2) PATCH HTML PAGES (LIMITED TO FIRST 100)
########################################

COUNT=0
for FILE in $(find . -maxdepth 1 -name "*.html" | head -100); do
  if ! grep -q 'sideguy-resolution-analytics.js' "$FILE"; then
    sed -i '/<\/body>/i <script src="/docs/sideguy-os/components/sideguy-resolution-analytics.js"></script>' "$FILE"
    COUNT=$((COUNT + 1))
  fi
done

echo "- Patched HTML files: $COUNT" >> "$LOG"

echo "✅ Resolution Analytics v2 created"
echo "Component: $ANALYTICS_JS"
echo "Patched: $COUNT pages"
echo "Log: $LOG"
