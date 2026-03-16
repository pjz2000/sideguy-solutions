#!/bin/bash

# =========================================
# SIDEGUY — 100K BATCH GENERATOR
# =========================================
# Generates topic × industry × city page matrix.
# Idempotent — skips existing pages.
# Run plan-next-batches.sh first to preview scope.
# =========================================

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TOPICS="$ROOT/docs/manifests/scale-batches/batch-001-core-topics.txt"
CITIES="$ROOT/docs/manifests/scale-batches/batch-001-cities.txt"
INDUSTRIES="$ROOT/docs/manifests/scale-batches/batch-001-industries.txt"
TEMPLATE="$ROOT/seo-template.html"

for f in "$TOPICS" "$CITIES" "$INDUSTRIES" "$TEMPLATE"; do
  if [ ! -f "$f" ]; then
    echo "❌ Missing: $f"
    exit 1
  fi
done

slugify() {
  echo "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's|[/&,.:?()]||g' \
    | tr ' ' '-' \
    | sed 's/--*/-/g' \
    | sed 's/^-//' \
    | sed 's/-$//'
}

create_page() {
  local slug="$1"
  local title="$2"
  local heading="$3"
  local file="$ROOT/$slug.html"

  if [ -f "$file" ]; then
    echo "  skip   $slug.html"
    return 1
  fi

  cp "$TEMPLATE" "$file"
  sed -i "s|PAGE_TITLE|$title|g" "$file"
  sed -i "s|PAGE_HEADING|$heading|g" "$file"
  echo "  create $slug.html"
  return 0
}

created=0
skipped=0

while IFS= read -r topic || [ -n "$topic" ]; do
  [ -z "$topic" ] && continue
  topic_slug="$(slugify "$topic")"

  # Core triangle (5 per topic)
  for combo in \
    "how-to-$topic_slug|||How to $topic" \
    "$topic_slug-vs-alternatives|||$topic vs alternatives" \
    "how-much-does-$topic_slug-cost|||How much does $topic cost" \
    "$topic_slug-breakdown|||$topic breakdown" \
    "what-is-$topic_slug|||What is $topic"
  do
    slug="${combo%%|||*}"
    title="${combo##*|||}"
    if create_page "$slug" "$title" "$title"; then
      created=$((created+1))
    else
      skipped=$((skipped+1))
    fi
  done

  # Industry overlays (3 per topic × industry)
  while IFS= read -r industry || [ -n "$industry" ]; do
    [ -z "$industry" ] && continue
    industry_slug="$(slugify "$industry")"

    for combo in \
      "$topic_slug-for-$industry_slug|||$topic for $industry" \
      "how-much-does-$topic_slug-cost-for-$industry_slug|||How much does $topic cost for $industry" \
      "how-to-use-$topic_slug-for-$industry_slug|||How to use $topic for $industry"
    do
      slug="${combo%%|||*}"
      title="${combo##*|||}"
      if create_page "$slug" "$title" "$title"; then
        created=$((created+1))
      else
        skipped=$((skipped+1))
      fi
    done
  done < "$INDUSTRIES"

  # Local overlays (3 per topic × city)
  while IFS= read -r city || [ -n "$city" ]; do
    [ -z "$city" ] && continue
    city_slug="$(slugify "$city")"

    for combo in \
      "$topic_slug-$city_slug|||$topic $city" \
      "$topic_slug-in-$city_slug|||$topic in $city" \
      "how-much-does-$topic_slug-cost-in-$city_slug|||How much does $topic cost in $city"
    do
      slug="${combo%%|||*}"
      title="${combo##*|||}"
      if create_page "$slug" "$title" "$title"; then
        created=$((created+1))
      else
        skipped=$((skipped+1))
      fi
    done
  done < "$CITIES"

done < "$TOPICS"

echo ""
echo "✅ Batch complete — $created created, $skipped skipped."
echo "Next steps:"
echo "  1. python3 tools/upgrades/inject-nav-links.py --run  (add nav to new pages)"
echo "  2. node update-sitemap.js                            (rebuild sitemap)"
echo "  3. tools/scale/validate-new-pages.sh                 (quality check)"
echo "  4. git add -A && git commit -m 'Build: 100k expansion batch 001'"
