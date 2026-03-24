#!/usr/bin/env bash
########################################
# SIDEGUY SMART MONETIZATION LAYER v2
# Injects contextual CTAs on high-intent pages
# Architecture: Root-level pages, matches existing style
########################################

set -eo pipefail

PROJECT_ROOT="/workspaces/sideguy-solutions"
DATE="$(date +"%Y-%m-%d-%H%M%S")"
LOG_FILE="$PROJECT_ROOT/_money_layer_log_$DATE.txt"

cd "$PROJECT_ROOT" || exit 1

########################################
# CONFIGURATION
########################################

# High-intent page patterns (decision-making moments)
PATTERNS=(
  "who-do-i-call-*"
  "who-builds-*"
  "*-cost-*"
  "*-vs-*"
  "best-*-contractors*"
  "*-near-me.html"
  "how-to-choose-*"
  "what-to-look-for-*"
)

# Skip pages that already have strong CTAs
SKIP_MARKERS=(
  "cta-box"
  "sideguy-money-layer"
  "Text PJ: 773-544-1231"
)

########################################
# CONTEXTUAL CTA GENERATOR
########################################

get_contextual_cta() {
  local FILE="$1"
  local BASENAME=$(basename "$FILE" .html)
  
  # Detect page type and generate contextual copy
  if [[ "$BASENAME" == *"hvac"* ]] || [[ "$BASENAME" == *"ac-"* ]] || [[ "$BASENAME" == *"air-conditioning"* ]]; then
    HEADING="Need help choosing an HVAC contractor?"
    SUBTEXT="Don't waste money on the wrong system or contractor. Get straight answers before you commit."
  
  elif [[ "$BASENAME" == *"payment"* ]] || [[ "$BASENAME" == *"processing"* ]] || [[ "$BASENAME" == *"stripe"* ]]; then
    HEADING="Confused about payment processing?"
    SUBTEXT="Processing fees add up fast. Get clarity on what you're actually paying for and whether you have better options."
  
  elif [[ "$BASENAME" == *"ai"* ]] || [[ "$BASENAME" == *"automation"* ]] || [[ "$BASENAME" == *"software"* ]]; then
    HEADING="Not sure which AI tool fits your workflow?"
    SUBTEXT="Most AI tools oversell and underdeliver. Skip the demos and get honest guidance on what actually works."
  
  elif [[ "$BASENAME" == *"plumb"* ]] || [[ "$BASENAME" == *"leak"* ]] || [[ "$BASENAME" == *"pipe"* ]]; then
    HEADING="Need to find a reliable plumber?"
    SUBTEXT="Plumbing emergencies are stressful. Get guidance on who to call and what questions to ask."
  
  elif [[ "$BASENAME" == *"electrical"* ]] || [[ "$BASENAME" == *"electric"* ]] || [[ "$BASENAME" == *"wiring"* ]]; then
    HEADING="Looking for a qualified electrician?"
    SUBTEXT="Electrical work isn't the place to cut corners. Get help finding someone who knows what they're doing."
  
  elif [[ "$BASENAME" == *"data-center"* ]] || [[ "$BASENAME" == *"infrastructure"* ]] || [[ "$BASENAME" == *"compute"* ]]; then
    HEADING="Planning critical infrastructure?"
    SUBTEXT="These decisions are expensive to get wrong. Talk to someone who's navigated this before committing."
  
  else
    # Generic high-intent CTA
    HEADING="Not sure what to do next?"
    SUBTEXT="Skip the confusion and get a straight answer. No sales pitch, just honest guidance."
  fi
  
  # Return the formatted CTA block
  cat <<CTAEOF

<div class="sideguy-money-layer" style="margin:48px 0;padding:28px;border-radius:var(--r, 16px);background:linear-gradient(135deg, rgba(33,211,161,.08), rgba(74,169,255,.06));border:1px solid rgba(33,211,161,.25);box-shadow:0 12px 32px rgba(7,48,68,.06);">
  <h3 style="margin:0 0 12px;font-size:1.3em;font-weight:700;color:var(--ink, #073044);">$HEADING</h3>
  <p style="margin:0 0 20px;color:var(--muted, #3f6173);line-height:1.6;">$SUBTEXT</p>
  <a href="tel:+17735441231" style="display:inline-block;padding:14px 28px;background:linear-gradient(135deg, #21d3a1, #00c7ff);color:#ffffff;font-weight:700;border-radius:999px;text-decoration:none;box-shadow:0 8px 20px rgba(33,211,161,.25);transition:transform .15s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">Text PJ: 773-544-1231</a>
  <p style="margin:12px 0 0;font-size:0.9em;color:var(--muted2, #5e7d8e);">Human response, usually within a few hours.</p>
</div>
CTAEOF
}

########################################
# INJECTION LOGIC
########################################

inject_cta() {
  local FILE="$1"
  
  # Check if page already has a CTA
  for MARKER in "${SKIP_MARKERS[@]}"; do
    if grep -q "$MARKER" "$FILE"; then
      echo "⏭️  Skipped: $(basename "$FILE") (already has CTA)"
      return
    fi
  done
  
  # Find injection point (before </body> or before footer)
  if ! grep -q "</body>" "$FILE"; then
    echo "⚠️  Warning: $(basename "$FILE") - no </body> tag found"
    return
  fi
  
  # Generate contextual CTA
  CTA_BLOCK=$(get_contextual_cta "$FILE")
  
  # Create temporary file with injection
  TMP=$(mktemp)
  
  awk -v cta="$CTA_BLOCK" '
  BEGIN { injected=0 }
  /<\/body>/ && injected==0 {
    print cta
    injected=1
  }
  { print }
  ' "$FILE" > "$TMP"
  
  # Verify the injection worked
  if grep -q "sideguy-money-layer" "$TMP"; then
    mv "$TMP" "$FILE"
    echo "✅ Monetized: $(basename "$FILE")"
    echo "$(basename "$FILE")" >> "$LOG_FILE"
  else
    rm "$TMP"
    echo "❌ Failed: $(basename "$FILE")"
  fi
}

########################################
# TARGET PAGE COLLECTION
########################################

echo "🎯 Collecting high-intent pages..."
echo ""

TARGET_FILES=()

for PATTERN in "${PATTERNS[@]}"; do
  while IFS= read -r FILE; do
    if [ -f "$FILE" ]; then
      TARGET_FILES+=("$FILE")
    fi
  done < <(find "$PROJECT_ROOT" -maxdepth 1 -name "$PATTERN" -type f)
done

# Remove duplicates
TARGET_FILES=($(printf '%s\n' "${TARGET_FILES[@]}" | sort -u))

TOTAL=${#TARGET_FILES[@]}

if [ $TOTAL -eq 0 ]; then
  echo "⚠️  No matching pages found."
  echo "Patterns searched: ${PATTERNS[*]}"
  exit 0
fi

echo "Found $TOTAL high-intent pages matching patterns"
echo ""

########################################
# PROCESS PAGES
########################################

echo "💰 Applying contextual CTAs..."
echo ""

INJECTED=0
SKIPPED=0
FAILED=0

for FILE in "${TARGET_FILES[@]}"; do
  if inject_cta "$FILE"; then
    INJECTED=$((INJECTED + 1))
  else
    FAILED=$((FAILED + 1))
  fi
done

########################################
# SUMMARY
########################################

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ MONETIZATION LAYER COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Results:"
echo "   Total pages scanned:  $TOTAL"
echo "   CTAs injected:        $INJECTED"
echo "   Skipped (has CTA):    This run didn't track skips separately"
echo "   Failed:               $FAILED"
echo ""
echo "📄 Log saved to: $(basename "$LOG_FILE")"
echo ""
echo "Next steps:"
echo "  1. Review a few pages to verify CTA quality"
echo "  2. git add *.html"
echo "  3. git commit -m 'Add: Contextual CTAs to high-intent pages ($DATE)'"
echo ""
