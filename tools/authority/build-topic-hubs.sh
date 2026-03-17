#!/usr/bin/env bash

cd /workspaces/sideguy-solutions || exit 0

INPUT="manifests/authority/topic-registry.json"
OUTPUT_DIR="public/authority"
LOG="logs/topic-hubs.log"

mkdir -p "$OUTPUT_DIR"
touch "$LOG"

timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "" >> "$LOG"
echo "[$timestamp] TOPIC HUB BUILD START" >> "$LOG"

jq -c '.[]' "$INPUT" | while read -r topic; do
  slug=$(echo "$topic" | jq -r '.slug')
  title=$(echo "$topic" | jq -r '.title')
  category=$(echo "$topic" | jq -r '.category')
  priority=$(echo "$topic" | jq -r '.priority')
  file="$OUTPUT_DIR/$slug.html"

  {
    echo "<!DOCTYPE html>"
    echo "<html lang=\"en\">"
    echo "<head>"
    echo "  <meta charset=\"UTF-8\">"
    echo "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
    echo "  <title>$title | SideGuy Solutions</title>"
    echo "  <meta name=\"description\" content=\"$title and supporting SideGuy pages.\">"
    echo "  <style>"
    echo "    body { margin:0; padding:0; font-family:Arial,sans-serif; background:linear-gradient(180deg,#07131f 0%,#0b2133 55%,#103754 100%); color:#eaf6ff; }"
    echo "    .wrap { max-width:950px; margin:0 auto; padding:40px 20px 120px; }"
    echo "    .card { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10); border-radius:18px; padding:24px; margin-bottom:20px; }"
    echo "    .pill { display:inline-block; padding:6px 10px; border-radius:999px; margin-right:8px; margin-bottom:8px; background:rgba(159,227,255,0.10); border:1px solid rgba(159,227,255,0.25); font-size:12px; text-transform:uppercase; }"
    echo "    a { color:#9fe3ff; text-decoration:none; }"
    echo "    .orb { position:fixed; right:22px; bottom:22px; background:linear-gradient(135deg,#25d2ff,#78ffd1); color:#052737; padding:14px 18px; border-radius:999px; font-weight:700; box-shadow:0 0 0 0 rgba(37,210,255,0.58); animation:pulse 2s infinite; }"
    echo "    @keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(37,210,255,0.58);} 70%{box-shadow:0 0 0 18px rgba(37,210,255,0);} 100%{box-shadow:0 0 0 0 rgba(37,210,255,0);} }"
    echo "  </style>"
    echo "</head>"
    echo "<body><div class=\"wrap\">"
    echo "  <div class=\"card\">"
    echo "    <div class=\"pill\">$category</div>"
    echo "    <div class=\"pill\">$priority priority</div>"
    echo "    <h1>$title</h1>"
    echo "    <p>This topic hub reinforces SideGuy authority across a connected set of pages.</p>"
    echo "  </div>"
    echo "  <div class=\"card\">"
    echo "    <h2>Supporting Pages</h2>"

    echo "$topic" | jq -r '.pages[]' | while read -r page; do
      echo "    <p><a href=\"/$page.html\">$page</a></p>"
    done

    echo "  </div>"
    echo "  <div class=\"card\">"
    echo "    <h2>Why this hub exists</h2>"
    echo "    <p>Authority grows when a topic is covered from multiple angles: decision pages, explainers, local variants, and supporting guides.</p>"
    echo "  </div>"
    echo "  <div class=\"card\">"
    echo "    <h2>Need a real human?</h2>"
    echo "    <p>Text PJ: <strong>773-544-1231</strong></p>"
    echo "    <p><a href=\"/authority/index.html\">← Back to Authority Hub</a></p>"
    echo "  </div>"
    echo "</div><a class=\"orb\" href=\"sms:+17735441231\">💬 Text PJ</a></body></html>"
  } > "$file"

  echo "[$timestamp] BUILT $file" >> "$LOG"
done

echo "[$timestamp] TOPIC HUB BUILD END" >> "$LOG"
echo "Built topic hubs"
