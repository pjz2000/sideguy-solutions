#!/usr/bin/env bash

########################################
# SIDEGUY TOOL LAYER v2
# Conversion utility blocks (no JS, high clarity)
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
DATE="$(date +"%Y-%m-%d-%H%M%S")"

cd "$PROJECT_ROOT" || exit 1

########################################
# TARGET PAGES
########################################

# Find pages at root level matching cost/comparison patterns
TARGETS=$(find "$PROJECT_ROOT" -maxdepth 1 -name "*.html" \
  | grep -E "(cost|best|vs|compare|pricing|worth|should-i)" \
  | head -20)  # Limit to 20 for safety

if [ -z "$TARGETS" ]; then
  echo "❌ No matching pages found"
  exit 1
fi

########################################
# TOOL BLOCK INJECTION
########################################

inject_tool() {
  FILE="$1"
  
  # Skip if already has tool block
  if grep -q "sideguy-tool-v2" "$FILE"; then
    echo "⏭️  Skipped (has tool): $(basename "$FILE")"
    return
  fi
  
  # Skip if no closing body tag (malformed)
  if ! grep -q "</body>" "$FILE"; then
    echo "⚠️  Skipped (no </body>): $(basename "$FILE")"
    return
  fi
  
  TMP=$(mktemp)
  
  awk '
  BEGIN {added=0}
  /<\/body>/ && added==0 {
    
    print ""
    print "<!-- Tool Layer v2 -->"
    print "<section class=\"sideguy-tool-v2\" style=\""
    print "  margin: 48px auto 32px auto;"
    print "  padding: 28px;"
    print "  max-width: 720px;"
    print "  background: linear-gradient(135deg, rgba(33, 211, 161, 0.06) 0%, rgba(33, 211, 161, 0.02) 100%);"
    print "  border: 2px solid rgba(33, 211, 161, 0.2);"
    print "  border-radius: 16px;"
    print "  box-shadow: 0 2px 8px rgba(7, 48, 68, 0.06);"
    print "\">"
    print ""
    print "<h2 style=\"margin-top: 0; font-size: 1.5em; color: #073044;\">Quick Decision Framework</h2>"
    print "<p style=\"color: #5a7b8c; margin-bottom: 20px;\">A simple way to think about your situation before committing.</p>"
    print ""
    print "<div style=\"display: grid; gap: 12px; margin: 24px 0;\">"
    print ""
    print "<div style=\"padding: 16px; border: 1px solid #d1e8ed; border-radius: 10px; background: #ffffff;\">"
    print "<strong style=\"color: #073044; font-size: 1.05em;\">💵 Low range</strong>"
    print "<p style=\"margin: 8px 0 0 0; color: #5a7b8c; font-size: 0.95em;\">Minimal setup / basic option — works but limited</p>"
    print "</div>"
    print ""
    print "<div style=\"padding: 16px; border: 1px solid #d1e8ed; border-radius: 10px; background: #ffffff;\">"
    print "<strong style=\"color: #073044; font-size: 1.05em;\">💰 Mid range</strong>"
    print "<p style=\"margin: 8px 0 0 0; color: #5a7b8c; font-size: 0.95em;\">Typical real-world solution — balanced approach</p>"
    print "</div>"
    print ""
    print "<div style=\"padding: 16px; border: 1px solid #d1e8ed; border-radius: 10px; background: #ffffff;\">"
    print "<strong style=\"color: #073044; font-size: 1.05em;\">💎 High end</strong>"
    print "<p style=\"margin: 8px 0 0 0; color: #5a7b8c; font-size: 0.95em;\">Advanced / optimized setup — long-term quality</p>"
    print "</div>"
    print ""
    print "</div>"
    print ""
    print "<h3 style=\"margin-top: 28px; margin-bottom: 12px; font-size: 1.2em; color: #073044;\">What Actually Matters</h3>"
    print "<ul style=\"line-height: 1.9; color: #073044; margin-left: 20px;\">"
    print "<li>Scale of the project / system</li>"
    print "<li>Efficiency vs. upfront cost tradeoffs</li>"
    print "<li>Long-term reliability vs. short-term savings</li>"
    print "<li>Your actual usage patterns (not theoretical maximums)</li>"
    print "</ul>"
    print ""
    print "<div style=\"margin-top: 28px; padding: 20px; background: #ffffff; border-radius: 12px; border: 2px solid #21d3a1; box-shadow: 0 2px 6px rgba(33, 211, 161, 0.12);\">"
    print "<strong style=\"font-size: 1.1em; color: #073044;\">Want a real answer for your situation?</strong>"
    print "<p style=\"margin: 12px 0 8px 0; color: #5a7b8c;\">Text PJ for straight guidance — no sales pitch, no vendor steering.</p>"
    print "<a href=\"tel:+17735441231\" style=\"display: inline-block; margin-top: 8px; padding: 12px 24px; background: #21d3a1; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: 600;\">📱 773-544-1231</a>"
    print "<p style=\"font-size: 0.9em; color: #5a7b8c; margin-top: 12px;\">Usually responds within a few hours. We will either help or tell you we cannot.</p>"
    print "</div>"
    print ""
    print "</section>"
    print ""
    
    added=1
  }
  { print }
  ' "$FILE" > "$TMP"
  
  mv "$TMP" "$FILE"
  
  echo "✅ Tool added: $(basename "$FILE")"
}

########################################
# RUN
########################################

echo "🧰 Applying Tool Layer v2 to cost/comparison pages..."
echo ""

COUNT=0

for FILE in $TARGETS
do
  inject_tool "$FILE"
  COUNT=$((COUNT+1))
done

########################################
# FINISH
########################################

echo ""
echo "✅ Tool layer deployment complete"
echo "📊 Pages updated: $COUNT"
echo "📋 Next: Test a few pages to verify layout"
echo ""
