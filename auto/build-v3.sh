#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"

cd "$PROJECT_ROOT" || return

echo "---------------------------------------"
echo "SideGuy Auto Build Engine v3"
echo "---------------------------------------"

DATE="$(date +"%Y-%m-%d-%H%M")"

QUEUE_FILE="seo-reserve/queue.csv"
MANIFEST_DIR="seo-reserve/manifests"
LOG_FILE="docs/build-log.jsonl"
STATUS_PAGE="public/build-status.html"
SITEMAP_FILE="public/sitemap.xml"
INDEX_FILE="index.html"

mkdir -p auto
mkdir -p docs
mkdir -p public
mkdir -p seo-reserve
mkdir -p "$MANIFEST_DIR"

if [ ! -f "$QUEUE_FILE" ]; then
  echo "slug,title,city,keyword,vertical,intent,status" > "$QUEUE_FILE"
fi

if [ ! -f "$LOG_FILE" ]; then
  touch "$LOG_FILE"
fi

if [ ! -f "$SITEMAP_FILE" ]; then
  cat > "$SITEMAP_FILE" <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</urlset>
XML
fi

if [ ! -f "$INDEX_FILE" ]; then
  cat > "$INDEX_FILE" <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SideGuy Solutions</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <h1>SideGuy Solutions</h1>
  <ul id="page-list">
  </ul>
</body>
</html>
HTML
fi

if [ ! -f "$MANIFEST_DIR/payments.csv" ]; then
  cat > "$MANIFEST_DIR/payments.csv" <<'EOF2'
city,service,intent,vertical
san-diego,payment-processing,decision,payments
san-diego,merchant-fees,comparison,payments
encinitas,payment-processing,local,payments
carlsbad,pos-systems,decision,payments
oceanside,credit-card-processing,local,payments
EOF2
fi

if [ ! -f "$MANIFEST_DIR/ai.csv" ]; then
  cat > "$MANIFEST_DIR/ai.csv" <<'EOF2'
city,service,intent,vertical
san-diego,ai-consulting,decision,ai
san-diego,ai-automation,comparison,ai
encinitas,ai-help,local,ai
carlsbad,business-automation,decision,ai
oceanside,chatgpt-for-business,local,ai
EOF2
fi

if [ ! -f "$MANIFEST_DIR/hvac.csv" ]; then
  cat > "$MANIFEST_DIR/hvac.csv" <<'EOF2'
city,service,intent,vertical
san-diego,hvac-help,decision,hvac
san-diego,ac-repair-options,comparison,hvac
encinitas,hvac-quote-help,local,hvac
carlsbad,mini-split-help,decision,hvac
oceanside,air-conditioning-help,local,hvac
EOF2
fi

titleize() {
  echo "$1" | tr '-' ' ' | awk '{
    for (i=1; i<=NF; i++) {
      $i=toupper(substr($i,1,1)) substr($i,2)
    }
    print
  }'
}

append_queue_row_if_missing() {
  ROW="$1"
  SLUG="$(echo "$ROW" | cut -d',' -f1)"
  if ! grep -q "^$SLUG," "$QUEUE_FILE"; then
    echo "$ROW" >> "$QUEUE_FILE"
  fi
}

insert_before_urlset_close() {
  ENTRY="$1"
  TMP_FILE="$(mktemp)"
  awk -v entry="$ENTRY" '
    /<\/urlset>/ && !done {
      print entry
      done=1
    }
    { print }
  ' "$SITEMAP_FILE" > "$TMP_FILE"
  mv "$TMP_FILE" "$SITEMAP_FILE"
}

insert_before_ul_close() {
  ENTRY="$1"
  TMP_FILE="$(mktemp)"
  awk -v entry="$ENTRY" '
    /<\/ul>/ && !done {
      print "    " entry
      done=1
    }
    { print }
  ' "$INDEX_FILE" > "$TMP_FILE"
  mv "$TMP_FILE" "$INDEX_FILE"
}

build_related_links() {
  CURRENT_VERTICAL="$1"
  CURRENT_SLUG="$2"

  grep ",$CURRENT_VERTICAL," "$QUEUE_FILE" | grep ",built$" | cut -d',' -f1,2 | grep -v "^$CURRENT_SLUG," | tail -n 4 | while IFS=',' read -r RSLUG RTITLE
  do
    echo "<li><a href=\"/$RSLUG/\">$RTITLE</a></li>"
  done
}

echo "Loading manifests into queue..."

for MANIFEST in "$MANIFEST_DIR"/*.csv
do
  [ -f "$MANIFEST" ] || continue

  tail -n +2 "$MANIFEST" | while IFS=',' read -r CITY SERVICE INTENT VERTICAL
  do
    [ -n "$CITY" ] || continue
    [ -n "$SERVICE" ] || continue
    [ -n "$INTENT" ] || continue
    [ -n "$VERTICAL" ] || continue

    SLUG="$CITY-$SERVICE"
    TITLE="$(titleize "$SERVICE") $(titleize "$CITY")"
    KEYWORD="$(echo "$SERVICE $CITY" | tr '-' ' ')"

    append_queue_row_if_missing "$SLUG,$TITLE,$CITY,$KEYWORD,$VERTICAL,$INTENT,pending"
  done
done

MAX_PER_RUN=8
PENDING_ROWS="$(tail -n +2 "$QUEUE_FILE" | grep ',pending$' | head -n "$MAX_PER_RUN")"

echo "$PENDING_ROWS" | while IFS=',' read -r SLUG TITLE CITY KEYWORD VERTICAL INTENT STATUS
do
  [ -n "$SLUG" ] || continue

  OUTPUT_DIR="$PROJECT_ROOT/$SLUG"
  OUTPUT_FILE="$OUTPUT_DIR/index.html"

  mkdir -p "$OUTPUT_DIR"

  CITY_LABEL="$(titleize "$CITY")"
  SERVICE_LABEL="$(echo "$KEYWORD" | sed 's/\b\(.\)/\u\1/g')"
  VERTICAL_LABEL="$(titleize "$VERTICAL")"
  INTENT_LABEL="$(titleize "$INTENT")"

  RELATED_LINKS="$(build_related_links "$VERTICAL" "$SLUG")"

  cat > "$OUTPUT_FILE" <<PAGE
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>$TITLE | SideGuy Solutions</title>
  <meta name="description" content="$SERVICE_LABEL in $CITY_LABEL. SideGuy helps you get clarity before cost with real human guidance.">
  <link rel="canonical" href="https://sideguy.co/$SLUG/">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index,follow">
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 860px;
      margin: 0 auto;
      padding: 40px 20px 120px;
      line-height: 1.6;
      color: #111;
      background: linear-gradient(180deg, #f6fbff 0%, #ffffff 100%);
    }
    .card {
      background: rgba(255,255,255,0.88);
      border: 1px solid rgba(0,0,0,0.08);
      border-radius: 18px;
      padding: 22px;
      margin: 20px 0;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .muted {
      color: #555;
      font-size: 14px;
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
    ul {
      padding-left: 20px;
    }
  </style>
</head>
<body>

  <p class="muted">Build: $DATE • Vertical: $VERTICAL_LABEL • Intent: $INTENT_LABEL</p>

  <h1>$TITLE</h1>

  <div class="card">
    <p>If you are searching for <strong>$KEYWORD</strong>, you probably do not just want more generic search results. You want to understand what the problem is, what your options are, what matters first, and whether the next step is actually worth paying for.</p>
    <p>That is where SideGuy fits. We help people and operators get <strong>clarity before cost</strong> — calm guidance first, pressure second, real human help when needed.</p>
  </div>

  <div class="card">
    <h2>What this page is about</h2>
    <p>This page covers one narrow longtail topic inside the <strong>$VERTICAL_LABEL</strong> cluster for <strong>$CITY_LABEL</strong>.</p>
    <ul>
      <li>What people usually mean when they search this</li>
      <li>Where confusion usually starts</li>
      <li>What options tend to exist</li>
      <li>When human help is actually useful</li>
    </ul>
  </div>

  <div class="card">
    <h2>Why this topic matters</h2>
    <p>Most people do not need more noise. They need a clean explanation, a grounded next step, and a way to avoid overspending or choosing the wrong vendor too early.</p>
    <p><strong>Google discovers the problem, AI helps explain it, and a real human helps resolve it.</strong></p>
  </div>

  <div class="card">
    <h2>Related $VERTICAL_LABEL pages</h2>
    <ul>
      $RELATED_LINKS
    </ul>
  </div>

  <div class="card">
    <h2>Back to home</h2>
    <p><a href="/">Return to SideGuy Solutions</a></p>
  </div>

  <a class="orb" href="sms:+17735441231">💬 Text PJ — 773-544-1231</a>

</body>
</html>
PAGE

  if ! grep -q "<loc>https://sideguy.co/$SLUG/</loc>" "$SITEMAP_FILE"; then
    insert_before_urlset_close "  <url><loc>https://sideguy.co/$SLUG/</loc></url>"
  fi

  if ! grep -q "href=\"/$SLUG/\"" "$INDEX_FILE" && ! grep -q "href='/$SLUG/'" "$INDEX_FILE"; then
    insert_before_ul_close "<li><a href=\"/$SLUG/\">$TITLE</a></li>"
  fi

  echo "{\"slug\":\"$SLUG\",\"title\":\"$TITLE\",\"vertical\":\"$VERTICAL\",\"intent\":\"$INTENT\",\"built_at\":\"$DATE\"}" >> "$LOG_FILE"

  TMP_QUEUE="$(mktemp)"
  awk -F',' -v slug="$SLUG" 'BEGIN{OFS=","}
    NR==1 { print $0; next }
    $1==slug && $7=="pending" { $7="built"; print $1,$2,$3,$4,$5,$6,$7; next }
    { print $0 }
  ' "$QUEUE_FILE" > "$TMP_QUEUE"
  mv "$TMP_QUEUE" "$QUEUE_FILE"

  echo "Built: $SLUG"
done

TOTAL_QUEUED="$(tail -n +2 "$QUEUE_FILE" | wc -l | tr -d ' ')"
TOTAL_BUILT="$(tail -n +2 "$QUEUE_FILE" | grep ',built$' | wc -l | tr -d ' ')"
TOTAL_PENDING="$(tail -n +2 "$QUEUE_FILE" | grep ',pending$' | wc -l | tr -d ' ')"

cat > "$STATUS_PAGE" <<STATUS
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SideGuy Build Status</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 900px;
      margin: 0 auto;
      padding: 40px 20px;
      line-height: 1.6;
    }
    .card {
      border: 1px solid #ddd;
      border-radius: 16px;
      padding: 18px;
      margin: 16px 0;
    }
  </style>
</head>
<body>
  <h1>SideGuy Build Status</h1>
  <div class="card">
    <p><strong>Last Run:</strong> $DATE</p>
    <p><strong>Total Queued:</strong> $TOTAL_QUEUED</p>
    <p><strong>Total Built:</strong> $TOTAL_BUILT</p>
    <p><strong>Total Pending:</strong> $TOTAL_PENDING</p>
    <p><strong>Build Cap Per Run:</strong> $MAX_PER_RUN</p>
  </div>
  <div class="card">
    <h2>Recent Builds</h2>
    <ul>
STATUS

tail -n 15 "$LOG_FILE" | while read -r LINE
do
  RSLUG="$(echo "$LINE" | grep -o '"slug":"[^"]*"' | cut -d'"' -f4)"
  RTITLE="$(echo "$LINE" | grep -o '"title":"[^"]*"' | cut -d'"' -f4)"
  echo "      <li><a href=\"/$RSLUG/\">$RTITLE</a></li>" >> "$STATUS_PAGE"
done

cat >> "$STATUS_PAGE" <<'STATUS'
    </ul>
  </div>
</body>
</html>
STATUS

echo "---------------------------------------"
echo "SideGuy Auto Build Engine v3 complete"
echo "Queue: $TOTAL_QUEUED total"
echo "Built: $TOTAL_BUILT total"
echo "Pending: $TOTAL_PENDING total"
echo "Status page: public/build-status.html"
echo "---------------------------------------"
