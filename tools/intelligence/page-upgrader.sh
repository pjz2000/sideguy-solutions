#!/usr/bin/env bash

TARGET="${1:-}"
OUT_DIR="logs/intelligence"
OUT_FILE="$OUT_DIR/page-upgrader.txt"

mkdir -p "$OUT_DIR"

if [ -z "$TARGET" ]; then
  echo "Usage: bash tools/intelligence/page-upgrader.sh your-page.html"
  echo "Example: bash tools/intelligence/page-upgrader.sh machine-to-machine-payments.html"
  exit 1
else
  if [ ! -f "$TARGET" ]; then
    echo "File not found: $TARGET"
    exit 1
  else
    words=$(tr '\n' ' ' < "$TARGET" | sed 's/<[^>]*>/ /g' | tr -s ' ' '\n' | wc -l | tr -d ' ')
    has_faq=$(grep -Eic 'FAQPage|faq' "$TARGET" 2>/dev/null | tr -d ' ')
    has_schema=$(grep -Eic 'application/ld\+json' "$TARGET" 2>/dev/null | tr -d ' ')
    has_og=$(grep -Eic 'og:title|og:description' "$TARGET" 2>/dev/null | tr -d ' ')
    has_examples=$(grep -Eic 'example|for example|use case|scenario' "$TARGET" 2>/dev/null | tr -d ' ')
    has_text_pj=$(grep -Eic 'Text PJ|773-544-1231' "$TARGET" 2>/dev/null | tr -d ' ')
    internal_links=$(grep -Eoi 'href="[^"]+\.html"' "$TARGET" 2>/dev/null | wc -l | tr -d ' ')

    {
      echo "SideGuy Page Upgrade Report"
      echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
      echo "Target: $TARGET"
      echo
      echo "Current signals:"
      echo "- word count: $words"
      echo "- FAQ presence: $has_faq"
      echo "- schema presence: $has_schema"
      echo "- OG tags: $has_og"
      echo "- examples: $has_examples"
      echo "- Text PJ presence: $has_text_pj"
      echo "- internal links: $internal_links"
      echo
      echo "Recommended upgrades:"
      echo "1. Strengthen title + H1 so the page clearly matches the exact search phrase."
      echo "2. Add a calm intro that explains the problem in plain language."
      echo "3. Add a 'How it works' section."
      echo "4. Add 2-4 use cases or examples."
      echo "5. Add FAQ schema if missing."
      echo "6. Add 3-6 internal links to related hub and service pages."
      echo "7. Make sure the Text PJ orb / direct human help CTA is obvious."
      echo "8. Add 'climate / local / operator / business owner' language where relevant."
      echo "9. Add trust language: clarity before cost, real human help, no pressure."
      echo "10. Add a last-updated timestamp if the page does not already have one."
      echo
      echo "Upgrade flags:"
      [ "$words" -lt 700 ] && echo "- Expand content depth"
      [ "$has_faq" -eq 0 ] && echo "- Add FAQ block + FAQPage schema"
      [ "$has_schema" -eq 0 ] && echo "- Add structured data"
      [ "$has_og" -eq 0 ] && echo "- Add OG meta tags (og:title, og:description)"
      [ "$has_examples" -eq 0 ] && echo "- Add examples/use-cases"
      [ "$has_text_pj" -eq 0 ] && echo "- Add Text PJ CTA"
      [ "$internal_links" -lt 4 ] && echo "- Add more internal links"
    } | tee "$OUT_FILE"

    echo ""
    echo "Report saved → $OUT_FILE"
  fi
fi
