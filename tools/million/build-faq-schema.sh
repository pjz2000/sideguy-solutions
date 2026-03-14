#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

INPUT="docs/million-page/authority/upgrade-candidates.csv"
[ -f "$INPUT" ] || { echo "No upgrade-candidates.csv found."; exit 1; }

mkdir -p docs/million-page/authority/schema

tail -n +2 "$INPUT" | while IFS=, read -r url title h1 theme audience use_case industry city state modifier page_type intent score; do
  clean_url="$(echo "$url"       | tr -d '"')"
  clean_theme="$(echo "$theme"   | sed 's/^"//;s/"$//' | sed "s/'/\\\\'/g")"
  clean_industry="$(echo "$industry" | sed 's/^"//;s/"$//' | sed "s/'/\\\\'/g")"
  slug="$(basename "$clean_url" .html)"
  schema="docs/million-page/authority/schema/${slug}.json"

  cat > "$schema" <<JSON
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is ${clean_theme}?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "${clean_theme} refers to modern systems designed to solve specific operational or technological challenges."
      }
    },
    {
      "@type": "Question",
      "name": "Why are companies searching for ${clean_theme}?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Organizations search for clearer explanations of how new technologies improve workflows and automation."
      }
    },
    {
      "@type": "Question",
      "name": "How does ${clean_theme} apply to ${clean_industry}?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "In ${clean_industry}, these technologies are often used to improve efficiency, automation, and operational decision making."
      }
    }
  ]
}
JSON
done

echo "FAQ schemas created in docs/million-page/authority/schema/"
