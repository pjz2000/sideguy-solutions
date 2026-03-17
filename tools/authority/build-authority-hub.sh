#!/usr/bin/env bash

cd /workspaces/sideguy-solutions || exit 0

INPUT="manifests/authority/topic-registry.json"
OUTPUT="public/authority/index.html"
LOG="logs/authority-hub.log"

mkdir -p public/authority
touch "$LOG"

timestamp=$(date +"%Y-%m-%d %H:%M:%S")

{
  echo "<!DOCTYPE html>"
  echo "<html lang=\"en\">"
  echo "<head>"
  echo "  <meta charset=\"UTF-8\">"
  echo "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
  echo "  <title>SideGuy Authority Engine</title>"
  echo "  <meta name=\"description\" content=\"Authority hubs, clusters, and decision pages built across SideGuy topic zones.\">"
  echo "  <style>"
  echo "    body { margin:0; padding:0; font-family:Arial,sans-serif; background:linear-gradient(180deg,#07131f 0%,#0b2133 55%,#103754 100%); color:#eaf6ff; }"
  echo "    .wrap { max-width:1000px; margin:0 auto; padding:40px 20px 120px; }"
  echo "    .card { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10); border-radius:18px; padding:24px; margin-bottom:20px; }"
  echo "    .pill { display:inline-block; padding:6px 10px; border-radius:999px; margin-right:8px; margin-bottom:8px; background:rgba(159,227,255,0.10); border:1px solid rgba(159,227,255,0.25); font-size:12px; text-transform:uppercase; }"
  echo "    a { color:#9fe3ff; text-decoration:none; }"
  echo "    .orb { position:fixed; right:22px; bottom:22px; background:linear-gradient(135deg,#25d2ff,#78ffd1); color:#052737; padding:14px 18px; border-radius:999px; font-weight:700; box-shadow:0 0 0 0 rgba(37,210,255,0.58); animation:pulse 2s infinite; }"
  echo "    @keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(37,210,255,0.58);} 70%{box-shadow:0 0 0 18px rgba(37,210,255,0);} 100%{box-shadow:0 0 0 0 rgba(37,210,255,0);} }"
  echo "  </style>"
  echo "</head>"
  echo "<body><div class=\"wrap\">"
  echo "  <div class=\"card\">"
  echo "    <h1>SideGuy Authority Engine</h1>"
  echo "    <p>Problem-space coverage, cluster reinforcement, internal linking, and human-first resolution.</p>"
  echo "  </div>"

  jq -c '.[]' "$INPUT" | while read -r topic; do
    slug=$(echo "$topic" | jq -r '.slug')
    title=$(echo "$topic" | jq -r '.title')
    category=$(echo "$topic" | jq -r '.category')
    priority=$(echo "$topic" | jq -r '.priority')

    echo "<div class=\"card\">"
    echo "  <div class=\"pill\">$category</div>"
    echo "  <div class=\"pill\">$priority priority</div>"
    echo "  <h2><a href=\"/authority/$slug.html\">$title</a></h2>"
    echo "  <p>This authority zone organizes supporting pages around a real decision surface.</p>"
    echo "</div>"
  done

  echo "<div class=\"card\">"
  echo "  <h2>Need real help?</h2>"
  echo "  <p>Text PJ: <strong>773-544-1231</strong></p>"
  echo "  <p><a href=\"/\">← Back to Home</a></p>"
  echo "</div>"
  echo "</div><a class=\"orb\" href=\"sms:+17735441231\">💬 Text PJ</a></body></html>"
} > "$OUTPUT"

echo "[$timestamp] BUILT $OUTPUT" >> "$LOG"
echo "Built authority hub: $OUTPUT"
