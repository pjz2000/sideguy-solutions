#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

echo "======================================"
echo "SIDEGUY GEO LATTICE INTERLINKER v1"
echo "======================================"

CITIES=(
  san-diego
  encinitas
  carlsbad
  oceanside
  del-mar
  la-jolla
  solana-beach
  coronado
)

TARGETS=$(find . -maxdepth 1 -name "*.html" | grep -E 'san-diego|encinitas|carlsbad|oceanside|del-mar|la-jolla|solana-beach|coronado')

COUNT=0

for file in $TARGETS; do
  [ -f "$file" ] || continue

  base=$(basename "$file")
  city=$(echo "$base" | grep -oE 'san-diego|encinitas|carlsbad|oceanside|del-mar|la-jolla|solana-beach|coronado' | head -1)

  links=""
  for nearby in "${CITIES[@]}"; do
    [ "$nearby" = "$city" ] && continue
    nearby_file="${base/$city/$nearby}"
    if [ -f "$nearby_file" ]; then
      label=$(echo "$nearby" | tr '-' ' ')
      links+="<li><a href='/$nearby_file'>$label</a></li>"
    fi
  done

  [ -z "$links" ] && continue

  block="
<section style='margin:36px 0;padding:22px;border-radius:18px;background:rgba(255,255,255,.03)'>
<h2>Nearby Service Routes</h2>
<p>Same SideGuy pathway available across nearby North County and San Diego cities.</p>
<ul>$links</ul>
</section>
"

  perl -0pi -e "s|</body>|$block</body>|s" "$file"

  echo "linked $base"
  COUNT=$((COUNT+1))
done

echo "======================================"
echo "DONE: Geo lattice linked across $COUNT pages"
echo "Expected result: stronger local crawl mesh"
echo "======================================"
