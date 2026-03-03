#!/bin/bash
# ============================================================
# SHIP-006: SideGuy Quote Review Page Generator
# Usage:
#   ./scripts/generate-quote-review.sh "Service Name" service-slug [hub-slug] [hub-name] [category] [price-low] [price-high]
#
# Examples:
#   ./scripts/generate-quote-review.sh "Garage Door" "garage-door"
#   ./scripts/generate-quote-review.sh "Pool Service" "pool-service" "home-repair-hub-san-diego" "Home Repair Hub" "home improvement" '$500' '$3,000'
#
# Naming convention: [service-slug]-quote-review-san-diego.html  (root-level, no public/ subdir)
# ============================================================

SERVICE_NAME="$1"
SERVICE_SLUG="$2"
HUB_SLUG="${3:-home-repair-hub-san-diego}"
HUB_NAME="${4:-Home Repair Hub}"
SERVICE_CATEGORY="${5:-home improvement}"
PRICE_LOW="${6:-varies}"
PRICE_HIGH="${7:-varies}"
UPDATED="$(date '+%B %Y')"
UPDATED_ISO="$(date '+%Y-%m-%d')"

# ── Validate required args ──────────────────────────────────
if [ -z "$SERVICE_NAME" ] || [ -z "$SERVICE_SLUG" ]; then
  echo ""
  echo "Usage: ./scripts/generate-quote-review.sh \"Service Name\" service-slug [hub-slug] [hub-name] [category] [price-low] [price-high]"
  echo ""
  echo "Required:"
  echo "  SERVICE_NAME    Display name, e.g. \"Garage Door\""
  echo "  SERVICE_SLUG    URL slug,      e.g. \"garage-door\""
  echo ""
  echo "Optional (defaults shown):"
  echo "  HUB_SLUG        home-repair-hub-san-diego"
  echo "  HUB_NAME        \"Home Repair Hub\""
  echo "  CATEGORY        \"home improvement\""
  echo "  PRICE_LOW       varies"
  echo "  PRICE_HIGH      varies"
  exit 1
fi

# ── Resolve paths ───────────────────────────────────────────
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$REPO_ROOT/templates/quote-review-template.html"
OUTPUT="$REPO_ROOT/${SERVICE_SLUG}-quote-review-san-diego.html"

if [ ! -f "$TEMPLATE" ]; then
  echo "ERROR: Template not found at $TEMPLATE"
  exit 1
fi

# ── Guard: don't overwrite existing pages ──────────────────
if [ -f "$OUTPUT" ]; then
  echo "⚠  Page already exists: $(basename "$OUTPUT")"
  echo "   Skipping generation to avoid overwriting. Delete the file first if you want to regenerate."
  exit 0
fi

# ── Generate via sed ────────────────────────────────────────
sed \
  -e "s|{{SERVICE_NAME}}|${SERVICE_NAME}|g" \
  -e "s|{{SERVICE_SLUG}}|${SERVICE_SLUG}|g" \
  -e "s|{{SERVICE_CATEGORY}}|${SERVICE_CATEGORY}|g" \
  -e "s|{{HUB_SLUG}}|${HUB_SLUG}|g" \
  -e "s|{{HUB_NAME}}|${HUB_NAME}|g" \
  -e "s|{{PRICE_LOW}}|${PRICE_LOW}|g" \
  -e "s|{{PRICE_HIGH}}|${PRICE_HIGH}|g" \
  -e "s|{{UPDATED}}|${UPDATED}|g" \
  -e "s|{{UPDATED_ISO}}|${UPDATED_ISO}|g" \
  "$TEMPLATE" > "$OUTPUT"

echo "✅ Generated: $(basename "$OUTPUT")"
echo "   → $OUTPUT"
echo ""
echo "Next steps:"
echo "  1. Review and customize service-specific checklist items"
echo "  2. Add page to sitemap.xml before </urlset>"
echo "     <url><loc>https://sideguysolutions.com/${SERVICE_SLUG}-quote-review-san-diego.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>"
echo "  3. Commit: git add $(basename "$OUTPUT") sitemap.xml && git commit -m 'Add: ${SERVICE_SLUG} quote review page'"
