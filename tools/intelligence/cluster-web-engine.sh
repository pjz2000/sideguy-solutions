#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"

cd "$PROJECT_ROOT" || return

echo "---------------------------------------"
echo "SideGuy Cluster Web Engine v6"
echo "---------------------------------------"

DATE="$(date +"%Y-%m-%d-%H%M")"

QUEUE_FILE="seo-reserve/queue.csv"
SCORES_FILE="docs/page-scores.csv"
LOG_FILE="docs/build-log.jsonl"
STATUS_PAGE="public/build-status.html"
INDEX_FILE="index.html"

mkdir -p auto
mkdir -p docs
mkdir -p public
mkdir -p seo-reserve

########################################
# INIT FILES
########################################

if [ ! -f "$QUEUE_FILE" ]; then
  echo "slug,title,city,keyword,vertical,intent,status" > "$QUEUE_FILE"
fi

if [ ! -f "$SCORES_FILE" ]; then
  cat > "$SCORES_FILE" <<'EOF'
slug,score,impressions,clicks,priority
san-diego-payment-processing,90,120,8,money
san-diego-ai-consulting,84,90,5,money
san-diego-hvac-help,77,65,3,cluster
encinitas-payment-processing,61,34,1,cluster
carlsbad-business-automation,58,29,1,cluster
EOF
fi

if [ ! -f "$LOG_FILE" ]; then
  touch "$LOG_FILE"
fi

########################################
# HELPERS
########################################

titleize() {
  echo "$1" | tr '-' ' ' | awk '{
    for (i=1; i<=NF; i++) {
      $i=toupper(substr($i,1,1)) substr($i,2)
    }
    print
  }'
}

safe_lookup_title() {
  TARGET_SLUG="$1"
  grep "^$TARGET_SLUG," "$QUEUE_FILE" | head -n 1 | cut -d',' -f2
}

safe_lookup_vertical() {
  TARGET_SLUG="$1"
  grep "^$TARGET_SLUG," "$QUEUE_FILE" | head -n 1 | cut -d',' -f5
}

safe_lookup_keyword() {
  TARGET_SLUG="$1"
  grep "^$TARGET_SLUG," "$QUEUE_FILE" | head -n 1 | cut -d',' -f4
}

build_vertical_page_list() {
  TARGET_VERTICAL="$1"
  grep ",$TARGET_VERTICAL," "$QUEUE_FILE" | grep ",built$" | cut -d',' -f1,2 | head -n 24 | while IFS=',' read -r SLUG TITLE
  do
    [ -n "$SLUG" ] || continue
    echo "<li><a href=\"/$SLUG/\">$TITLE</a></li>"
  done
}

build_vertical_winners() {
  TARGET_VERTICAL="$1"

  while IFS=',' read -r SLUG SCORE IMPRESSIONS CLICKS PRIORITY
  do
    [ "$SLUG" = "slug" ] && continue
    PAGE_VERTICAL="$(safe_lookup_vertical "$SLUG")"
    TITLE="$(safe_lookup_title "$SLUG")"

    if [ "$PAGE_VERTICAL" = "$TARGET_VERTICAL" ] && [ -n "$TITLE" ]; then
      echo "$SLUG,$TITLE,$SCORE,$PRIORITY"
    fi
  done < "$SCORES_FILE" | sort -t',' -k3,3nr | head -n 5 | while IFS=',' read -r WSLUG WTITLE WSCORE WPRIORITY
  do
    echo "<li><a href=\"/$WSLUG/\">$WTITLE</a> <span style=\"opacity:.7;\">— score $WSCORE • $WPRIORITY</span></li>"
  done
}

inject_page_web_block() {
  PAGE_FILE="$1"
  PAGE_SLUG="$2"
  PAGE_VERTICAL="$3"
  PAGE_TITLE="$4"

  HUB_SLUG="$PAGE_VERTICAL-hub"
  HUB_TITLE="$(titleize "$PAGE_VERTICAL") Hub"

  RELATED_HTML="$(
    grep ",$PAGE_VERTICAL," "$QUEUE_FILE" | grep ",built$" | cut -d',' -f1,2 | grep -v "^$PAGE_SLUG," | head -n 5 | while IFS=',' read -r RSLUG RTITLE
    do
      echo "<li><a href=\"/$RSLUG/\">$RTITLE</a></li>"
    done
  )"

  MONEY_HTML="$(
    tail -n +2 "$SCORES_FILE" | grep ',money$' | sort -t',' -k2,2nr | head -n 3 | while IFS=',' read -r MSLUG MSCORE MIMP MCLK MPRIORITY
    do
      MTITLE="$(safe_lookup_title "$MSLUG")"
      [ -n "$MTITLE" ] || MTITLE="$MSLUG"
      echo "<li><a href=\"/$MSLUG/\">$MTITLE</a></li>"
    done
  )"

  TMP_FILE="$(mktemp)"

  awk -v hubslug="$HUB_SLUG" -v hubtitle="$HUB_TITLE" -v vertical="$PAGE_VERTICAL" -v related="$RELATED_HTML" -v money="$MONEY_HTML" '
    BEGIN { inserted=0; skip=0 }
    /<div id="sideguy-cluster-web">/ { skip=1; next }
    /<\/div><!-- end sideguy-cluster-web -->/ { skip=0; next }
    /<\/body>/ && inserted==0 {
      print "<div id=\"sideguy-cluster-web\" style=\"max-width:860px;margin:24px auto;padding:22px;border:1px solid rgba(0,0,0,0.08);border-radius:18px;background:rgba(255,255,255,0.92);\">"
      print "  <h2>Explore this cluster</h2>"
      print "  <p>This page is part of the <strong>" vertical "</strong> cluster. If you want the bigger picture, start at the hub or jump to closely related pages below.</p>"
      print "  <p><a href=\"/" hubslug "/\">→ Visit the " hubtitle "</a></p>"
      print "  <h3>Related pages</h3>"
      print "  <ul>" related "</ul>"
      print "  <h3>Featured money pages</h3>"
      print "  <ul>" money "</ul>"
      print "</div><!-- end sideguy-cluster-web -->"
      inserted=1
    }
    { print }
  ' "$PAGE_FILE" > "$TMP_FILE"

  mv "$TMP_FILE" "$PAGE_FILE"
}

########################################
# STEP 1: BUILD HUB PAGES
########################################

VERTICALS="$(tail -n +2 "$QUEUE_FILE" | cut -d',' -f5 | sort | uniq)"

echo "$VERTICALS" | while read -r VERTICAL
do
  [ -n "$VERTICAL" ] || continue

  HUB_SLUG="$VERTICAL-hub"
  HUB_TITLE="$(titleize "$VERTICAL") Hub"
  HUB_DIR="$PROJECT_ROOT/$HUB_SLUG"
  HUB_FILE="$HUB_DIR/index.html"

  mkdir -p "$HUB_DIR"

  PAGE_LIST_HTML="$(build_vertical_page_list "$VERTICAL")"
  WINNERS_HTML="$(build_vertical_winners "$VERTICAL")"

  cat > "$HUB_FILE" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>$HUB_TITLE | SideGuy Solutions</title>
  <meta name="description" content="Explore the $VERTICAL SideGuy cluster. Clear pages, local context, and real human guidance.">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://sideguy.co/$HUB_SLUG/">
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 960px;
      margin: 0 auto;
      padding: 40px 20px 120px;
      line-height: 1.6;
      color: #111;
      background: linear-gradient(180deg, #f6fbff 0%, #ffffff 100%);
    }
    .card {
      background: rgba(255,255,255,0.92);
      border: 1px solid rgba(0,0,0,0.08);
      border-radius: 18px;
      padding: 22px;
      margin: 20px 0;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .orb {
      position: fixed;
      right: 20px;
      bottom: 20px;
      background: #0b0b0b;
      color: #fff;
      padding: 14px 18px;
      border-radius: 999px;
      font-weight: bold;
      text-decoration: none;
      box-shadow: 0 0 24px rgba(0,0,0,0.2);
      animation: pulse 2.2s infinite;
    }
    @keyframes pulse {
      0% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.04); opacity: 0.92; }
      100% { transform: scale(1); opacity: 1; }
    }
  </style>
</head>
<body>

  <p>Build: $DATE • Cluster Hub</p>
  <h1>$HUB_TITLE</h1>

  <div class="card">
    <p>This hub collects SideGuy pages inside the <strong>$(titleize "$VERTICAL")</strong> cluster. The goal is to make the topic easier to explore, easier to understand, and easier for both humans and search engines to navigate.</p>
    <p><strong>Clarity before cost.</strong> That means helping people get oriented before they commit money, time, or the wrong vendor.</p>
  </div>

  <div class="card">
    <h2>Top pages in this cluster</h2>
    <ul>
      $WINNERS_HTML
    </ul>
  </div>

  <div class="card">
    <h2>Browse cluster pages</h2>
    <ul>
      $PAGE_LIST_HTML
    </ul>
  </div>

  <div class="card">
    <h2>Back to home</h2>
    <p><a href="/">Return to SideGuy Solutions</a></p>
  </div>

  <a class="orb" href="sms:+17735441231">💬 Text PJ — 773-544-1231</a>

</body>
</html>
EOF

  if ! grep -q "^$HUB_SLUG," "$QUEUE_FILE"; then
    echo "$HUB_SLUG,$HUB_TITLE,global,$VERTICAL hub,$VERTICAL,hub,built" >> "$QUEUE_FILE"
  fi

  if [ -f "public/sitemap.xml" ] && ! grep -q "<loc>https://sideguy.co/$HUB_SLUG/</loc>" "public/sitemap.xml"; then
    TMP_SITEMAP="$(mktemp)"
    awk -v entry="  <url><loc>https://sideguy.co/$HUB_SLUG/</loc></url>" '
      /<\/urlset>/ && !done { print entry; done=1 }
      { print }
    ' public/sitemap.xml > "$TMP_SITEMAP"
    mv "$TMP_SITEMAP" public/sitemap.xml
  fi

  if [ -f "$INDEX_FILE" ] && ! grep -q "href=\"/$HUB_SLUG/\"" "$INDEX_FILE" && ! grep -q "href='/$HUB_SLUG/'" "$INDEX_FILE"; then
    TMP_INDEX="$(mktemp)"
    awk -v entry="<li><a href=\"/$HUB_SLUG/\">$HUB_TITLE</a></li>" '
      /<\/ul>/ && !done { print "    " entry; done=1 }
      { print }
    ' "$INDEX_FILE" > "$TMP_INDEX"
    mv "$TMP_INDEX" "$INDEX_FILE"
  fi

  echo "{\"slug\":\"$HUB_SLUG\",\"event\":\"hub-built\",\"vertical\":\"$VERTICAL\",\"at\":\"$DATE\"}" >> "$LOG_FILE"
  echo "Hub built: $HUB_SLUG"
done

########################################
# STEP 2: INJECT CLUSTER BLOCK INTO PAGES
########################################

echo "Injecting cluster web blocks into pages..."

tail -n +2 "$QUEUE_FILE" | grep ',built$' | while IFS=',' read -r SLUG TITLE CITY KEYWORD VERTICAL INTENT STATUS
do
  [ -n "$SLUG" ] || continue
  [ "$INTENT" = "hub" ] && continue

  PAGE_FILE="$PROJECT_ROOT/$SLUG/index.html"
  [ -f "$PAGE_FILE" ] || continue

  inject_page_web_block "$PAGE_FILE" "$SLUG" "$VERTICAL" "$TITLE"
  echo "{\"slug\":\"$SLUG\",\"event\":\"cluster-web-injected\",\"vertical\":\"$VERTICAL\",\"at\":\"$DATE\"}" >> "$LOG_FILE"
done

########################################
# STEP 3: BUILD CLUSTER STATUS PAGE
########################################

TOTAL_BUILT="$(tail -n +2 "$QUEUE_FILE" | grep ',built$' | wc -l | tr -d ' ')"
TOTAL_HUBS="$(tail -n +2 "$QUEUE_FILE" | grep ',hub,built$' | wc -l | tr -d ' ')"

cat > "$STATUS_PAGE" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SideGuy Build Status</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { font-family: Arial, sans-serif; max-width: 960px; margin: 0 auto; padding: 40px 20px; line-height: 1.6; }
    .card { border: 1px solid #ddd; border-radius: 18px; padding: 18px; margin: 16px 0; }
    ul { line-height: 1.8; }
  </style>
</head>
<body>
  <h1>SideGuy Build Status</h1>

  <div class="card">
    <p><strong>Last Cluster Run:</strong> $DATE</p>
    <p><strong>Total Built Pages:</strong> $TOTAL_BUILT</p>
    <p><strong>Total Hubs:</strong> $TOTAL_HUBS</p>
  </div>

  <div class="card">
    <h2>Cluster Hubs</h2>
    <ul>
EOF

echo "$VERTICALS" | while read -r VERTICAL
do
  [ -n "$VERTICAL" ] || continue
  HUB_SLUG="$VERTICAL-hub"
  HUB_TITLE="$(titleize "$VERTICAL") Hub"
  PAGE_COUNT="$(grep ",$VERTICAL," "$QUEUE_FILE" | grep ',built$' | grep -v ',hub,built$' | wc -l | tr -d ' ')"
  echo "      <li><a href=\"/$HUB_SLUG/\">$HUB_TITLE</a> — $PAGE_COUNT pages</li>" >> "$STATUS_PAGE"
done

cat >> "$STATUS_PAGE" <<'EOF'
    </ul>
  </div>
</body>
</html>
EOF

echo "---------------------------------------"
echo "Cluster Web Engine v6 complete"
echo "Hub pages built"
echo "Page web blocks injected"
echo "Status page rebuilt"
echo "---------------------------------------"
