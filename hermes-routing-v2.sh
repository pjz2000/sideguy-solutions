#!/usr/bin/env bash

########################################
# SIDEGUY HERMES ROUTING ENGINE v2
# Geo-aware vendor routing pages
# Standards-compliant, manual workflow
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
DOCS_DIR="docs/hermes-routing"
DATE="$(date +"%Y-%m-%d-%H%M")"
REPORT_FILE="$DOCS_DIR/hermes-routing-$DATE.md"

cd "$PROJECT_ROOT" || exit 1

mkdir -p "$DOCS_DIR"

echo "---------------------------------------"
echo "🌍 SIDEGUY HERMES ROUTING ENGINE v2"
echo "---------------------------------------"
echo ""

########################################
# CORE VERTICALS
########################################

VERTICALS=(
"hvac"
"solar"
"payments"
"ai-automation"
"website-help"
"tesla-charging"
"mini-split"
"crypto-help"
"relocation"
"vacation-rentals"
)

########################################
# GEO EXPANSION (North County SD)
########################################

LOCATIONS=(
"san-diego"
"encinitas"
"carlsbad"
"oceanside"
"del-mar"
"la-jolla"
"solana-beach"
"coronado"
)

########################################
# REPORT HEADER
########################################

cat > "$REPORT_FILE" <<EOF
# SideGuy Hermes Routing Report
Generated: $DATE

## Routes Built

EOF

ROUTES=0
SKIPPED=0

########################################
# ROUTE GENERATION
########################################

for VERTICAL in "${VERTICALS[@]}"; do
  for CITY in "${LOCATIONS[@]}"; do

    PAGE="${VERTICAL}-${CITY}.html"

    if [ -f "$PAGE" ]; then
      echo "⏭️  Skipped (exists): $PAGE"
      echo "- Skipped (exists): $PAGE" >> "$REPORT_FILE"
      SKIPPED=$((SKIPPED + 1))
      continue
    fi

    # Format display names
    VERTICAL_DISPLAY="${VERTICAL//-/ }"
    CITY_DISPLAY="${CITY//-/ }"
    CITY_TITLE="$(echo "$CITY_DISPLAY" | sed 's/\b\(.\)/\u\1/g')"  # Title case
    
    # Create page title
    if [ "$CITY" = "san-diego" ]; then
      CITY_CONTEXT="San Diego"
      PHONE_NUMBER="+17735441231"
    else
      CITY_CONTEXT="$CITY_TITLE (San Diego County)"
      PHONE_NUMBER="+17735441231"
    fi

cat > "$PAGE" <<'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>VERTICAL_TITLE in CITY_DISPLAY — Local Vendor Routing · SideGuy Solutions</title>
<meta name="description" content="Best VERTICAL_DISPLAY help in CITY_CONTEXT. SideGuy routes your problem to the right local vendor, operator, or next action based on urgency, cost, and trust."/>
<meta property="og:title" content="VERTICAL_TITLE in CITY_DISPLAY — SideGuy Solutions"/>
<meta property="og:description" content="Get routed to the best-fit local vendor or operator for VERTICAL_DISPLAY in CITY_CONTEXT. Clear guidance, no sales pitch."/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://sideguy.solutions/FILENAME"/>
<link rel="canonical" href="https://sideguy.solutions/FILENAME"/>
<style>
:root {
  --bg0:#eefcff;
  --bg1:rgba(255,255,255,.85);
  --card:rgba(255,255,255,.70);
  --ink:#073044;
  --muted:#3f6173;
  --muted2:#7a9aab;
  --mint:#21d3a1;
  --mint2:#00c7ff;
  --stroke:rgba(7,48,68,.12);
  --stroke2:rgba(7,48,68,.08);
  --pill:9999px;
  --rad:20px;
}

* {
  box-sizing:border-box;
  margin:0;
  padding:0;
}

body {
  font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
  background:radial-gradient(circle at 50% -20%, #d4f4ff 0%, #eefcff 28%, #f0fbff 55%, #fff 100%);
  color:var(--ink);
  line-height:1.65;
  min-height:100vh;
  padding:0;
  -webkit-font-smoothing:antialiased;
}

.container {
  max-width:720px;
  margin:0 auto;
  padding:80px 28px 60px;
}

h1 {
  font-size:clamp(28px, 5vw, 42px);
  font-weight:900;
  letter-spacing:-0.03em;
  line-height:1.15;
  margin:0 0 18px;
  color:var(--ink);
}

h2 {
  font-size:clamp(20px, 3.5vw, 26px);
  font-weight:800;
  letter-spacing:-0.02em;
  margin:40px 0 16px;
  color:var(--ink);
}

section {
  background:var(--card);
  border:1px solid var(--stroke2);
  border-radius:var(--rad);
  padding:28px;
  margin:24px 0;
  backdrop-filter:blur(18px);
  box-shadow:0 8px 28px rgba(7,48,68,.06);
}

p {
  margin:0 0 16px;
  font-size:16px;
  line-height:1.7;
  color:var(--muted);
}

p:last-child {
  margin-bottom:0;
}

ul {
  margin:16px 0;
  padding-left:22px;
  color:var(--muted);
}

li {
  margin-bottom:10px;
  line-height:1.7;
}

strong {
  color:var(--ink);
  font-weight:700;
}

.cta-btn {
  display:inline-block;
  background:linear-gradient(135deg, var(--mint), var(--mint2));
  color:#fff;
  padding:14px 28px;
  border-radius:var(--pill);
  text-decoration:none;
  font-weight:700;
  font-size:16px;
  margin-top:12px;
  box-shadow:0 10px 25px rgba(0,0,0,0.15);
  transition:transform .25s;
}

.cta-btn:hover {
  transform:translateY(-2px) scale(1.03);
}

.highlight {
  background:rgba(33,211,161,0.1);
  padding:2px 8px;
  border-radius:6px;
  font-weight:600;
}

.routing-card {
  background:linear-gradient(135deg,rgba(33,211,161,.12),rgba(0,199,255,.08));
  border:1px solid rgba(33,211,161,.3);
  border-radius:var(--rad);
  padding:22px 24px;
  margin:20px 0;
}

.routing-card h3 {
  margin:0 0 12px;
  font-size:18px;
  font-weight:800;
  color:var(--ink);
}

#pj-orb {
  position:fixed;
  bottom:24px;
  right:24px;
  background:linear-gradient(135deg, var(--mint), var(--mint2));
  color:#fff;
  padding:16px 24px;
  border-radius:var(--pill);
  font-weight:700;
  font-size:15px;
  cursor:pointer;
  box-shadow:0 12px 32px rgba(33,211,161,0.35);
  text-decoration:none;
  z-index:100;
  animation:pulse 2.4s ease-in-out infinite;
}

@keyframes pulse {
  0%,100%{box-shadow:0 12px 32px rgba(33,211,161,0.35);}
  50%{box-shadow:0 12px 40px rgba(33,211,161,0.6), 0 0 0 8px rgba(33,211,161,0.12);}
}

@media (max-width: 640px) {
  h1{font-size:28px;}
  section{padding:22px;}
  #pj-orb{bottom:18px; right:18px; padding:14px 20px; font-size:14px;}
}
</style>
</head>
<body>

<div class="container">

<h1>VERTICAL_TITLE in CITY_DISPLAY</h1>

<section>
<p>You've got a VERTICAL_DISPLAY problem in CITY_CONTEXT. You're comparing 12 tabs, reading contradictory Reddit threads, and wondering if you're about to get ripped off.</p>
<p><strong>SideGuy routes your problem to the best-fit path</strong> — whether that's a trusted local vendor, a Text PJ consultation, or a clear next action you can handle yourself.</p>
<p>No sales funnel. No comparison matrix with 40 businesses. Just the clearest next move based on your specific situation.</p>
</section>

<div class="routing-card">
<h3>🧭 How Hermes Routing Works</h3>
<p><strong>1. You text your problem</strong> → not a form, not a chatbot, just SMS to PJ</p>
<p><strong>2. We classify intent</strong> → emergency vs exploratory, cost-sensitive vs time-sensitive, DIY vs needs-expert</p>
<p><strong>3. Geo + vendor match</strong> → CITY_CONTEXT-specific routing to operators who've earned trust through prior SideGuy referrals</p>
<p><strong>4. You get clarity</strong> → 1-3 vendor intros (not a list of 20), cost ranges, or a "you can handle this yourself" with instructions</p>
</div>

<section>
<h2>Why CITY_DISPLAY needs local routing</h2>
<p>CITY_CONTEXT has unique context:</p>
<ul>
<li><strong>Local codes & permits</strong> — what flies in one city doesn't in another</li>
<li><strong>Vendor availability</strong> — some operators serve all of North County, others stick to their zone</li>
<li><strong>Community trust</strong> — SideGuy tracks which vendors deliver on promises vs who oversells</li>
<li><strong>Cost variance</strong> — prices shift based on drive time, permitting complexity, competition density</li>
</ul>
<p>Generic Google searches give you SEO-optimized spam. Hermes routing gives you the 2-3 names that actually make sense for <strong>your VERTICAL_DISPLAY problem in CITY_DISPLAY</strong>.</p>
</section>

<section>
<h2>Common VERTICAL_TITLE scenarios in CITY_DISPLAY</h2>
<p>SideGuy has routed VERTICAL_DISPLAY problems across CITY_CONTEXT including:</p>
<ul>
<li>Emergency situations requiring same-day response</li>
<li>Cost-comparison scenarios where you need 3 honest bids</li>
<li>DIY-or-call decisions where you just need a second opinion</li>
<li>Vendor vetting (someone quoted you $X — is that reasonable?)</li>
<li>Long-term planning (exploring options, no immediate purchase)</li>
</ul>
<p>Every scenario gets routed differently. That's the point.</p>
</section>

<section style="background:linear-gradient(135deg,rgba(33,211,161,.16),rgba(0,199,255,.12));border:2px solid var(--mint);">
<h2 style="margin:0 0 12px;">Ready to get routed?</h2>
<p style="margin:0 0 16px;">Text your VERTICAL_DISPLAY problem to PJ. You'll get clarity within 15 minutes (usually faster).</p>
<a href="sms:PHONE_NUMBER" class="cta-btn" style="margin-top:0;">📱 Text PJ — VERTICAL_TITLE in CITY_DISPLAY</a>
<p style="margin:16px 0 0;font-size:14px;opacity:.85;">No form. No sales call. Just straight routing to your best next move.</p>
</section>

<section style="border-top:2px solid var(--stroke);margin-top:50px;padding-top:24px;">
<p style="font-size:14px;color:var(--muted2);">
<strong>SideGuy Solutions</strong> is a human-first clarity layer for home services, technology decisions, and business automation across San Diego County. We route problems to solutions — not marketing funnels.
</p>
</section>

</div>

<a id="pj-orb" href="sms:PHONE_NUMBER">💬 Text PJ</a>

</body>
</html>
HTMLEOF

    # Replace placeholders
    VERTICAL_TITLE="$(echo "$VERTICAL_DISPLAY" | sed 's/\b\(.\)/\u\1/g')"
    
    sed -i "s|VERTICAL_TITLE|$VERTICAL_TITLE|g" "$PAGE"
    sed -i "s|VERTICAL_DISPLAY|$VERTICAL_DISPLAY|g" "$PAGE"
    sed -i "s|CITY_DISPLAY|$CITY_TITLE|g" "$PAGE"
    sed -i "s|CITY_CONTEXT|$CITY_CONTEXT|g" "$PAGE"
    sed -i "s|PHONE_NUMBER|$PHONE_NUMBER|g" "$PAGE"
    sed -i "s|FILENAME|$PAGE|g" "$PAGE"

    echo "✅ Created $PAGE"
    echo "- Built route: $PAGE" >> "$REPORT_FILE"
    ROUTES=$((ROUTES + 1))

  done
done

########################################
# FINAL REPORT
########################################

cat >> "$REPORT_FILE" <<EOF

## Totals
- Routes created: $ROUTES
- Skipped (existed): $SKIPPED
- Total routes: $((ROUTES + SKIPPED))

## Philosophy
Internet problem in CITY_CONTEXT
↓
intent classified (emergency/cost/DIY/vendor-vet)
↓
geo matched with local vendor trust database
↓
best local vendor or SideGuy human resolution
↓
clarity + next action (no 20-tab comparison stress)

## Standards Compliance
✅ Full inline CSS with SideGuy :root variables
✅ Mobile-responsive (clamp() typography)
✅ Text PJ CTAs throughout (SMS links)
✅ Radial gradient ocean theme backgrounds
✅ Glass-effect cards with backdrop-filter
✅ Semantic HTML5 structure
✅ Proper meta descriptions & OG tags

## Next Steps (Manual)
1. Review generated pages for quality
2. Update sitemap: ./generate-sitemap-failsafe.sh
3. Stage changes: git add *.html sitemap.xml sitemap.html
4. Commit: git commit -m "🌍 Hermes routing: VERTICAL × LOCATION vendor paths"
5. Push when ready: git push origin main

EOF

echo ""
echo "---------------------------------------"
echo "✅ Hermes Routing Engine Complete"
echo "---------------------------------------"
echo "🌊 Built: $ROUTES new location-aware vendor routes"
echo "⏭️  Skipped: $SKIPPED existing pages"
echo "📄 Report: $REPORT_FILE"
echo ""
echo "📋 NEXT STEPS (MANUAL):"
echo "   1. Review generated pages"
echo "   2. ./generate-sitemap-failsafe.sh"
echo "   3. git add *.html sitemap.xml sitemap.html"
echo "   4. git commit -m '🌍 Hermes: geo vendor routing pages'"
echo "   5. git push origin main"
echo ""
