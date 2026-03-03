#!/bin/bash
# ============================================================
# SHIP-012: SideGuy Quote Review Page Generator (Trade-Aware)
#
# Positional usage (backward-compatible):
#   ./scripts/generate-quote-review.sh "Service Name" service-slug \
#       [hub-slug] [hub-name] [category]
#
# Named options (new in SHIP-012):
#   --price   "STRING"     Typical San Diego price range for this trade
#                          e.g. "$800–$4,500 installed"
#   --cslb    "STRING"     CSLB license class required
#                          e.g. "CSLB C-61/D28 Limited Specialty license"
#   --permit  "STRING"     Permit paragraph text (replaces generic default)
#   --redflags FILE|STRING File of <li> items OR inline HTML for trade red flags
#   --checklist FILE|STRING File of <li> items OR inline HTML for trade checklist
#   --faqfile FILE         File of <details> blocks for trade-specific FAQs
#
# Examples:
#   ./scripts/generate-quote-review.sh "Garage Door" "garage-door"
#
#   ./scripts/generate-quote-review.sh "Tree Service" "tree-service" \
#       --price '$500–$5,000' \
#       --cslb "CSLB C-61/D49 Tree Service license" \
#       --permit "Tree removal in San Diego requires a permit when the trunk exceeds 6 inches in diameter. Your contractor should pull it — cost is typically \$75–\$150." \
#       --faqfile ./snippets/tree-service-faqs.html
#
# Naming convention: [service-slug]-quote-review-san-diego.html (root-level)
# ============================================================

# ── Parse positional + named args ──────────────────────────
POSITIONAL=()
PRICE_RANGE=""
CSLB_LICENSE=""
PERMIT_NOTES=""
REDFLAGS_INPUT=""
CHECKLIST_INPUT=""
FAQ_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --price)     PRICE_RANGE="$2";      shift 2 ;;
    --cslb)      CSLB_LICENSE="$2";     shift 2 ;;
    --permit)    PERMIT_NOTES="$2";     shift 2 ;;
    --redflags)  REDFLAGS_INPUT="$2";   shift 2 ;;
    --checklist) CHECKLIST_INPUT="$2";  shift 2 ;;
    --faqfile)   FAQ_FILE="$2";         shift 2 ;;
    --*)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
    *) POSITIONAL+=("$1"); shift ;;
  esac
done

SERVICE_NAME="${POSITIONAL[0]}"
SERVICE_SLUG="${POSITIONAL[1]}"
HUB_SLUG="${POSITIONAL[2]:-contractor-services-hub-san-diego}"
HUB_NAME="${POSITIONAL[3]:-Contractor Services Hub}"
SERVICE_CATEGORY="${POSITIONAL[4]:-home improvement}"
UPDATED="$(date '+%B %Y')"
UPDATED_ISO="$(date '+%Y-%m-%d')"

# ── Defaults for new placeholders ──────────────────────────
[[ -z "$PRICE_RANGE" ]]   && PRICE_RANGE="varies by scope and materials"
[[ -z "$CSLB_LICENSE" ]]  && CSLB_LICENSE="the appropriate CSLB license class"
# PERMIT_NOTES default is handled in Python (needs SERVICE_CATEGORY interpolation)

# ── Validate required args ──────────────────────────────────
if [[ -z "$SERVICE_NAME" || -z "$SERVICE_SLUG" ]]; then
  echo ""
  echo "Usage: ./scripts/generate-quote-review.sh \"Service Name\" service-slug [hub-slug] [hub-name] [category]"
  echo ""
  echo "Required:"
  echo "  SERVICE_NAME    Display name, e.g. \"Tree Service\""
  echo "  SERVICE_SLUG    URL slug,      e.g. \"tree-service\""
  echo ""
  echo "Optional positional (defaults shown):"
  echo "  HUB_SLUG        contractor-services-hub-san-diego"
  echo "  HUB_NAME        \"Contractor Services Hub\""
  echo "  CATEGORY        \"home improvement\""
  echo ""
  echo "Optional named flags:"
  echo "  --price    STRING     Typical price range, e.g. '\$800–\$4,500'"
  echo "  --cslb     STRING     License class, e.g. 'CSLB C-61/D28 license'"
  echo "  --permit   STRING     Permit FAQ paragraph text"
  echo "  --redflags FILE|STR   Extra <li> items for red flags section"
  echo "  --checklist FILE|STR  Extra <li> items for checklist section"
  echo "  --faqfile  FILE       File of <details> blocks for trade FAQs"
  exit 1
fi

# ── Resolve paths ───────────────────────────────────────────
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$REPO_ROOT/templates/quote-review-template.html"
OUTPUT="$REPO_ROOT/${SERVICE_SLUG}-quote-review-san-diego.html"

if [[ ! -f "$TEMPLATE" ]]; then
  echo "ERROR: Template not found at $TEMPLATE"
  exit 1
fi

# ── Guard: don't overwrite existing pages ──────────────────
if [[ -f "$OUTPUT" ]]; then
  echo "⚠  Page already exists: $(basename "$OUTPUT")"
  echo "   Skipping to avoid overwriting. Delete the file first to regenerate."
  exit 0
fi

# ── Export all values for Python substitution ──────────────
export GQR_TEMPLATE="$TEMPLATE"
export GQR_OUTPUT="$OUTPUT"
export GQR_SERVICE_NAME="$SERVICE_NAME"
export GQR_SERVICE_SLUG="$SERVICE_SLUG"
export GQR_SERVICE_CATEGORY="$SERVICE_CATEGORY"
export GQR_HUB_SLUG="$HUB_SLUG"
export GQR_HUB_NAME="$HUB_NAME"
export GQR_PRICE_RANGE="$PRICE_RANGE"
export GQR_CSLB_LICENSE="$CSLB_LICENSE"
export GQR_PERMIT_NOTES="$PERMIT_NOTES"
export GQR_REDFLAGS_INPUT="$REDFLAGS_INPUT"
export GQR_CHECKLIST_INPUT="$CHECKLIST_INPUT"
export GQR_FAQ_FILE="$FAQ_FILE"
export GQR_UPDATED="$UPDATED"
export GQR_UPDATED_ISO="$UPDATED_ISO"

# ── Generate via Python (handles multiline content safely) ─
python3 << 'PYEOF'
import os, sys

def load_input(val):
    """If val is a path to an existing file, read it. Otherwise treat as raw HTML."""
    if val and os.path.isfile(val):
        with open(val) as f:
            return f.read().rstrip('\n') + '\n'
    return val  # inline HTML string or empty

e = os.environ
template_path  = e['GQR_TEMPLATE']
output_path    = e['GQR_OUTPUT']
service_name   = e['GQR_SERVICE_NAME']
service_slug   = e['GQR_SERVICE_SLUG']
service_cat    = e['GQR_SERVICE_CATEGORY']
hub_slug       = e['GQR_HUB_SLUG']
hub_name       = e['GQR_HUB_NAME']
price_range    = e['GQR_PRICE_RANGE']
cslb_license   = e['GQR_CSLB_LICENSE']
permit_notes   = e.get('GQR_PERMIT_NOTES', '')
updated        = e['GQR_UPDATED']
updated_iso    = e['GQR_UPDATED_ISO']

trade_checklist = load_input(e.get('GQR_CHECKLIST_INPUT', ''))
trade_redflags  = load_input(e.get('GQR_REDFLAGS_INPUT', ''))
trade_faqs      = load_input(e.get('GQR_FAQ_FILE', ''))

# Default permit notes if not provided
if not permit_notes:
    permit_notes = (
        f"It depends on the scope. San Diego Development Services requires permits "
        f"for many {service_cat} projects. Your contractor should know the requirements "
        f"— if they claim permits aren't needed and you're not sure, call the city "
        f"before work starts."
    )

with open(template_path) as f:
    content = f.read()

replacements = {
    '{{SERVICE_NAME}}':            service_name,
    '{{SERVICE_SLUG}}':            service_slug,
    '{{SERVICE_CATEGORY}}':        service_cat,
    '{{HUB_SLUG}}':                hub_slug,
    '{{HUB_NAME}}':                hub_name,
    '{{PRICE_RANGE}}':             price_range,
    '{{CSLB_LICENSE}}':            cslb_license,
    '{{PERMIT_NOTES}}':            permit_notes,
    '{{TRADE_SPECIFIC_CHECKLIST}}': trade_checklist,
    '{{COMMON_RED_FLAGS}}':        trade_redflags,
    '{{TRADE_SPECIFIC_FAQ}}':      trade_faqs,
    '{{UPDATED}}':                 updated,
    '{{UPDATED_ISO}}':             updated_iso,
}

for token, value in replacements.items():
    content = content.replace(token, value)

with open(output_path, 'w') as f:
    f.write(content)

print(f"✅ Generated: {os.path.basename(output_path)}")
print(f"   → {output_path}")
PYEOF

echo ""
echo "Next steps:"
echo "  1. Open the page and review/enhance trade-specific sections"
echo "  2. Add to sitemap.xml before </urlset>:"
echo "     <url><loc>https://sideguysolutions.com/${SERVICE_SLUG}-quote-review-san-diego.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>"
echo "  3. Add the page to the All Guides list on existing quote-review pages"
echo "  4. Commit: git add ${SERVICE_SLUG}-quote-review-san-diego.html sitemap.xml && git commit -m 'Add: ${SERVICE_SLUG} quote review page'"
