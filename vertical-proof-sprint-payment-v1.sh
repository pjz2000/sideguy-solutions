#!/usr/bin/env bash

########################################
# SIDEGUY VERTICAL PROOF SPRINT v1
# PAYMENT FEE LEAK / PROCESSOR OPTIMIZATION
# Builds:
# 1) flagship page
# 2) fee leak calculator page
# 3) outcome story hub
# 4) 3 outcome story pages
# 5) 10 child pages
# 6) sitemap updates
# 7) homepage link
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

DATE="$(date +"%Y-%m-%d %H:%M:%S")"
DAY="$(date +"%F")"
DOMAIN="https://www.sideguysolutions.com"

echo "---------------------------------------"
echo "SIDEGUY VERTICAL PROOF SPRINT v1"
echo "---------------------------------------"
echo "Timestamp: $DATE"
echo ""

########################################
# CONFIG
########################################

DOCS_DIR="docs"
SPRINT_DIR="$DOCS_DIR/vertical-proof-sprint"
REPORT_FILE="$SPRINT_DIR/payment-proof-sprint-$DAY.md"
MANIFEST_FILE="$SPRINT_DIR/payment-proof-manifest-$DAY.csv"

mkdir -p "$DOCS_DIR" "$SPRINT_DIR"

FLAGSHIP="payment-fee-leak-optimization.html"
CALCULATOR="payment-fee-leak-calculator.html"
OUTCOME_HUB="payment-fee-outcomes.html"

CHILD_PAGES=(
"stripe-vs-square-hidden-fees.html"
"why-next-day-payouts-cost-more-than-you-think.html"
"software-fee-stacks-nobody-notices.html"
"ach-vs-cards-for-service-businesses.html"
"stablecoin-payouts-for-contractors.html"
"blended-processing-rate-explained.html"
"payment-processor-fee-audit-checklist.html"
"when-to-switch-payment-processors.html"
"subscription-bloat-in-payment-stacks.html"
"merchant-fee-leak-signs.html"
)

OUTCOME_PAGES=(
"restaurant-payment-fee-savings-story.html"
"contractor-payout-speed-story.html"
"small-business-processor-switch-story.html"
)

########################################
# HELPERS
########################################

ensure_sitemap() {
  if [ ! -f "sitemap.xml" ]; then
    cat > sitemap.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</urlset>
EOF
  fi
}

append_to_sitemap() {
  local FILE="$1"
  if ! grep -q "<loc>${DOMAIN}/${FILE}</loc>" sitemap.xml; then
    sed -i "/<\/urlset>/i \
<url>\n<loc>${DOMAIN}/${FILE}</loc>\n<lastmod>$(date +%F)</lastmod>\n<changefreq>weekly</changefreq>\n<priority>0.8</priority>\n</url>" sitemap.xml
  fi
}

append_home_link() {
  local FILE="$1"
  local LABEL="$2"

  if [ -f "index.html" ]; then
    if ! grep -q "$FILE" index.html; then
      sed -i "/<\/body>/i <p><a href=\"/${FILE}\">${LABEL}</a></p>" index.html
    fi
  fi
}

titleize() {
  echo "$1" | sed 's/.html$//' | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g'
}

########################################
# MANIFEST
########################################

echo "file,type" > "$MANIFEST_FILE"

########################################
# FLAGSHIP PAGE
########################################

cat > "$FLAGSHIP" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Why Your Payment Processor Is Quietly Eating Margin | SideGuy Solutions</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="SideGuy helps small businesses find hidden payment fee leaks, compare options, and avoid quietly losing margin. Clarity before cost.">
<link rel="canonical" href="https://www.sideguysolutions.com/payment-fee-leak-optimization.html">
<meta property="og:title" content="Why Your Payment Processor Is Quietly Eating Margin | SideGuy Solutions">
<meta property="og:description" content="Find hidden fee leaks, compare payment paths, and get a real next step.">
<meta property="og:type" content="website">
<style>
:root{
  --bg1:#eefcff;
  --bg2:#ffffff;
  --ink:#0a2540;
  --sub:#4b6478;
  --card:#ffffff;
  --line:rgba(10,37,64,.08);
  --accent:#0ea5e9;
  --shadow:0 10px 30px rgba(16,24,40,.08);
}
*{box-sizing:border-box}
body{
  margin:0;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  color:var(--ink);
  background:linear-gradient(180deg,var(--bg1) 0%,var(--bg2) 100%);
  line-height:1.65;
}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px 90px}
.hero{padding:48px 0 20px}
.hero-shell,.card{
  background:var(--card);
  border-radius:20px;
  padding:24px;
  box-shadow:var(--shadow);
  border:1px solid var(--line);
  margin-bottom:18px;
}
h1{font-size:clamp(34px,5vw,58px);line-height:1.04;margin:0 0 12px}
h2{font-size:clamp(24px,3vw,34px);line-height:1.1;margin:0 0 10px}
h3{margin:0 0 8px;font-size:20px}
p{margin:0 0 14px}
a{color:#0369a1;text-decoration:none}
a:hover{text-decoration:underline}
ul{margin:0;padding-left:20px}
li{margin-bottom:8px}
.grid-2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.pill-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.pill{padding:9px 12px;border-radius:999px;background:#f0fbff;border:1px solid var(--line);font-size:14px}
.btn{display:inline-block;padding:14px 18px;border-radius:999px;background:linear-gradient(135deg,#0ea5e9,#38bdf8);color:#fff;font-weight:700}
.muted{color:var(--sub)}
.calc{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.calc input{width:100%;padding:12px;border:1px solid var(--line);border-radius:12px}
.calc button{padding:12px 16px;border:none;border-radius:12px;background:#0ea5e9;color:#fff;font-weight:700;cursor:pointer}
.result{margin-top:12px;padding:14px;border-radius:14px;background:#f6fcff;border:1px solid var(--line)}
#pj-orb{
  position:fixed;right:18px;bottom:18px;z-index:9999;
  display:inline-flex;align-items:center;gap:10px;
  padding:15px 18px;border-radius:999px;
  background:linear-gradient(135deg,#0ea5e9,#38bdf8);color:#fff;
  font-weight:800;box-shadow:0 14px 36px rgba(14,165,233,.28);
}
@media (max-width: 860px){
  .grid-2,.calc{grid-template-columns:1fr}
}
</style>

<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "mainEntity":[
    {
      "@type":"Question",
      "name":"How do I know if my payment processor is quietly eating margin?",
      "acceptedAnswer":{
        "@type":"Answer",
        "text":"Look at your effective blended fee rate, payout timing costs, extra software charges, and monthly volume. Small percentage differences compound quickly."
      }
    },
    {
      "@type":"Question",
      "name":"When should I switch payment processors?",
      "acceptedAnswer":{
        "@type":"Answer",
        "text":"Switch when the true annual margin leak is meaningful, the fee structure is unclear, or your current stack adds cost without enough value."
      }
    },
    {
      "@type":"Question",
      "name":"Can SideGuy help before I make a switch?",
      "acceptedAnswer":{
        "@type":"Answer",
        "text":"Yes. SideGuy helps you understand what actually matters before you commit, so you do not switch blindly or stay stuck by default."
      }
    }
  ]
}
</script>
</head>
<body>
<div class="wrap">

  <section class="hero">
    <div class="hero-shell">
      <p class="muted">SideGuy Solutions • Clarity before cost</p>
      <h1>Why Your Payment Processor Is Quietly Eating Margin</h1>
      <p class="muted">Most businesses do not feel the fee leak day by day. They feel it months later in thinner margins, slower cash flow, and a stack that got more expensive than it looked at first.</p>
      <p><a class="btn" href="sms:+17735441231">💬 Text PJ</a></p>
      <div class="pill-row">
        <div class="pill">Payment fee clarity</div>
        <div class="pill">Hidden margin leaks</div>
        <div class="pill">Execution-first guidance</div>
        <div class="pill">Real human fallback</div>
      </div>
    </div>
  </section>

  <div class="card">
    <h2>🥩 Squash the beef</h2>
    <p><strong>What the internet gets wrong:</strong> people argue brands before they understand the real blended fee rate.</p>
    <p><strong>What actually matters:</strong> effective fee %, software stack drag, payout timing, and whether your current setup fits your business model.</p>
    <p><strong>Best next move:</strong> run a 60-day fee leak check before switching or staying.</p>
    <p><strong>Still beefing?</strong> Text PJ: 773-544-1231</p>
  </div>

  <div class="grid-2">
    <div class="card">
      <h2>Decision snapshot</h2>
      <ul>
        <li><strong>Stay</strong> if the true blended rate is reasonable and the stack saves enough time to justify the cost.</li>
        <li><strong>Switch</strong> if fees are compounding, add-ons are bloated, or payout friction is hurting cash flow.</li>
      </ul>
    </div>
    <div class="card">
      <h2>What most people miss</h2>
      <ul>
        <li>Small percentage changes become real annual money.</li>
        <li>Convenience tools can quietly stack on top of processor fees.</li>
        <li>Fast payouts often cost more than people realize.</li>
      </ul>
    </div>
  </div>

  <div class="card">
    <h2>60-day fee leak calculator</h2>
    <div class="calc">
      <div>
        <label>Monthly volume</label>
        <input id="monthlyVolume" type="number" placeholder="50000">
      </div>
      <div>
        <label>Effective fee rate (%)</label>
        <input id="feeRate" type="number" step="0.01" placeholder="3.1">
      </div>
      <div>
        <label>Software / add-on fees per month</label>
        <input id="softwareFees" type="number" placeholder="300">
      </div>
      <div>
        <label>Alternative fee rate (%)</label>
        <input id="altRate" type="number" step="0.01" placeholder="2.5">
      </div>
    </div>
    <p style="margin-top:12px;"><button onclick="runLeakCalc()">Run leak check</button></p>
    <div id="leakResult" class="result">Run the calculator to estimate your annual margin leak.</div>
  </div>

  <div class="grid-2">
    <div class="card">
      <h2>Common mistakes</h2>
      <ul>
        <li>Looking at only the headline transaction fee.</li>
        <li>Ignoring monthly tools attached to the processor.</li>
        <li>Assuming next-day payouts are worth the hidden cost.</li>
        <li>Switching without a clear threshold.</li>
      </ul>
    </div>
    <div class="card">
      <h2>What to do next</h2>
      <ul>
        <li>Pull the last 60 days of payment volume.</li>
        <li>Calculate your effective fee rate, not just the advertised one.</li>
        <li>List all payment-related software costs.</li>
        <li>Compare the annual leak against your switching friction.</li>
      </ul>
    </div>
  </div>

  <div class="card">
    <h2>Need a real take?</h2>
    <p>Text PJ with your processor, monthly volume, and what feels off. I'll tell you what actually matters and whether switching is worth the friction.</p>
    <p><a class="btn" href="sms:+17735441231">💬 Text PJ: 773-544-1231</a></p>
  </div>

  <div class="card">
    <h2>Keep going</h2>
    <ul>
      <li><a href="/payment-fee-leak-calculator.html">Payment Fee Leak Calculator</a></li>
      <li><a href="/payment-fee-outcomes.html">Payment Fee Outcome Stories</a></li>
      <li><a href="/stripe-vs-square-hidden-fees.html">Stripe vs Square Hidden Fees</a></li>
      <li><a href="/when-to-switch-payment-processors.html">When to Switch Payment Processors</a></li>
    </ul>
  </div>

  <div class="card">
    <p><a href="/index.html">← Back to Home</a></p>
  </div>
</div>

<a id="pj-orb" href="sms:+17735441231">💬 Text PJ</a>

<script>
function runLeakCalc() {
  const vol = parseFloat(document.getElementById('monthlyVolume').value || 0);
  const fee = parseFloat(document.getElementById('feeRate').value || 0) / 100;
  const software = parseFloat(document.getElementById('softwareFees').value || 0);
  const alt = parseFloat(document.getElementById('altRate').value || 0) / 100;

  const currentAnnual = (vol * fee * 12) + (software * 12);
  const altAnnual = (vol * alt * 12);
  const leak = currentAnnual - altAnnual;

  const result = document.getElementById('leakResult');

  if (vol <= 0 || fee <= 0) {
    result.innerHTML = "Enter volume and fee rate to see your estimate.";
    return;
  }

  result.innerHTML =
    "<strong>Estimated annual processor-related cost:</strong> $" + currentAnnual.toFixed(2) + "<br>" +
    "<strong>Estimated alternative annual cost:</strong> $" + altAnnual.toFixed(2) + "<br>" +
    "<strong>Estimated annual leak:</strong> $" + leak.toFixed(2) + "<br><br>" +
    (leak > 0
      ? "If that number feels meaningful, it is worth pressure-testing your current setup."
      : "Your current setup may be fine, but still check for hidden software or payout costs.");
}
</script>
</body>
</html>
EOF

echo "${FLAGSHIP},flagship" >> "$MANIFEST_FILE"
echo "✅ Created $FLAGSHIP"

########################################
# CALCULATOR PAGE
########################################

cat > "$CALCULATOR" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Payment Fee Leak Calculator | SideGuy Solutions</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Estimate your annual payment processor margin leak with SideGuy's fee leak calculator.">
<link rel="canonical" href="https://www.sideguysolutions.com/payment-fee-leak-calculator.html">
<style>
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:linear-gradient(180deg,#eefcff 0%,#ffffff 100%);color:#0a2540}
.wrap{max-width:980px;margin:0 auto;padding:40px 20px 90px}
.card{background:#fff;border-radius:18px;padding:22px;margin:18px 0;box-shadow:0 10px 30px rgba(16,24,40,.08)}
input,button{width:100%;padding:12px;border-radius:12px;border:1px solid rgba(10,37,64,.08);margin-top:6px}
button{background:#0ea5e9;color:#fff;font-weight:700;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
#pj-orb{position:fixed;right:18px;bottom:18px;background:#0ea5e9;color:#fff;padding:14px 18px;border-radius:999px;font-weight:700}
@media (max-width: 760px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h1>Payment Fee Leak Calculator</h1>
    <p>Use this to estimate how much margin your current setup may be quietly eating every year.</p>
  </div>

  <div class="card">
    <div class="grid">
      <div>
        <label>Monthly volume</label>
        <input id="vol" type="number" placeholder="50000">
      </div>
      <div>
        <label>Average ticket</label>
        <input id="ticket" type="number" placeholder="120">
      </div>
      <div>
        <label>Current fee rate (%)</label>
        <input id="currentRate" type="number" step="0.01" placeholder="3.10">
      </div>
      <div>
        <label>Alternative fee rate (%)</label>
        <input id="newRate" type="number" step="0.01" placeholder="2.50">
      </div>
      <div>
        <label>Monthly software stack fees</label>
        <input id="stackFees" type="number" placeholder="250">
      </div>
      <div>
        <label>Payout timing cost / month</label>
        <input id="timingCost" type="number" placeholder="150">
      </div>
    </div>
    <p><button onclick="calc()">Calculate annual leak</button></p>
    <div id="out" class="card">Run the numbers to see your estimate.</div>
  </div>

  <div class="card">
    <h2>Use this result correctly</h2>
    <ul>
      <li>Do not switch blindly just because another rate looks lower.</li>
      <li>Compare annual leak against switching friction, integrations, and payout reality.</li>
      <li>If the leak is meaningful, pressure-test the stack now instead of six months from now.</li>
    </ul>
  </div>

  <div class="card">
    <p><a href="/payment-fee-leak-optimization.html">← Back to flagship page</a></p>
  </div>
</div>

<a id="pj-orb" href="sms:+17735441231">💬 Text PJ</a>

<script>
function calc() {
  const vol = parseFloat(document.getElementById('vol').value || 0);
  const ticket = parseFloat(document.getElementById('ticket').value || 0);
  const currentRate = parseFloat(document.getElementById('currentRate').value || 0) / 100;
  const newRate = parseFloat(document.getElementById('newRate').value || 0) / 100;
  const stackFees = parseFloat(document.getElementById('stackFees').value || 0);
  const timingCost = parseFloat(document.getElementById('timingCost').value || 0);

  const annualCurrent = (vol * currentRate * 12) + (stackFees * 12) + (timingCost * 12);
  const annualNew = (vol * newRate * 12);
  const annualLeak = annualCurrent - annualNew;
  const monthlyLeak = annualLeak / 12;
  const txPerMonth = ticket > 0 ? (vol / ticket) : 0;

  document.getElementById('out').innerHTML =
    "<strong>Estimated annual current cost:</strong> $" + annualCurrent.toFixed(2) + "<br>" +
    "<strong>Estimated annual alternative cost:</strong> $" + annualNew.toFixed(2) + "<br>" +
    "<strong>Estimated annual leak:</strong> $" + annualLeak.toFixed(2) + "<br>" +
    "<strong>Estimated monthly leak:</strong> $" + monthlyLeak.toFixed(2) + "<br>" +
    "<strong>Transactions per month:</strong> " + txPerMonth.toFixed(0) + "<br><br>" +
    (annualLeak > 0
      ? "If you are leaking this much, it is worth reviewing the processor and surrounding stack."
      : "Your setup may be fine on fees alone. Still check hidden tooling and payout drag.");
}
</script>
</body>
</html>
EOF

echo "${CALCULATOR},calculator" >> "$MANIFEST_FILE"
echo "✅ Created $CALCULATOR"

########################################
# OUTCOME HUB
########################################

cat > "$OUTCOME_HUB" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Payment Fee Outcome Stories | SideGuy Solutions</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Real-world payment fee leak stories and processor optimization examples from SideGuy.">
<link rel="canonical" href="https://www.sideguysolutions.com/payment-fee-outcomes.html">
<style>
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:linear-gradient(180deg,#eefcff 0%,#ffffff 100%);color:#0a2540}
.wrap{max-width:980px;margin:0 auto;padding:40px 20px 90px}
.card{background:#fff;border-radius:18px;padding:22px;margin:18px 0;box-shadow:0 10px 30px rgba(16,24,40,.08)}
#pj-orb{position:fixed;right:18px;bottom:18px;background:#0ea5e9;color:#fff;padding:14px 18px;border-radius:999px;font-weight:700}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h1>Payment Fee Outcome Stories</h1>
    <p>These stories are here to make margin leaks feel concrete instead of theoretical.</p>
  </div>

  <div class="card">
    <ul>
      <li><a href="/restaurant-payment-fee-savings-story.html">Restaurant Payment Fee Savings Story</a></li>
      <li><a href="/contractor-payout-speed-story.html">Contractor Payout Speed Story</a></li>
      <li><a href="/small-business-processor-switch-story.html">Small Business Processor Switch Story</a></li>
    </ul>
  </div>

  <div class="card">
    <p><a href="/payment-fee-leak-optimization.html">← Back to flagship page</a></p>
  </div>
</div>
<a id="pj-orb" href="sms:+17735441231">💬 Text PJ</a>
</body>
</html>
EOF

echo "${OUTCOME_HUB},outcome-hub" >> "$MANIFEST_FILE"
echo "✅ Created $OUTCOME_HUB"

########################################
# OUTCOME STORIES
########################################

cat > "restaurant-payment-fee-savings-story.html" <<'EOF'
<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<title>Restaurant Payment Fee Savings Story | SideGuy Solutions</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="A restaurant-style payment fee leak story showing how small rate differences can become meaningful annual margin.">
<link rel="canonical" href="https://www.sideguysolutions.com/restaurant-payment-fee-savings-story.html">
<style>body{margin:0;font-family:-apple-system;background:linear-gradient(#eefcff,#fff);color:#0a2540} .wrap{max-width:900px;margin:0 auto;padding:40px 20px 90px} .card{background:#fff;padding:22px;border-radius:18px;margin:18px 0;box-shadow:0 10px 30px rgba(16,24,40,.08)} #pj-orb{position:fixed;right:18px;bottom:18px;background:#0ea5e9;color:#fff;padding:14px 18px;border-radius:999px;font-weight:700}</style>
</head><body><div class="wrap">
<div class="card"><h1>Restaurant Payment Fee Savings Story</h1><p>A restaurant doing steady monthly card volume can quietly lose thousands per year without realizing where the leak lives.</p></div>
<div class="card"><h2>What felt off</h2><p>Margin looked thinner than expected even though sales were stable.</p></div>
<div class="card"><h2>What actually mattered</h2><ul><li>Blended effective fee rate</li><li>Monthly software add-ons</li><li>Payout timing costs</li></ul></div>
<div class="card"><h2>The move</h2><p>Pressure-test the true annual leak before making any processor change.</p></div>
<div class="card"><p><a href="/payment-fee-outcomes.html">← Back to outcomes</a></p></div>
</div><a id="pj-orb" href="sms:+17735441231">💬 Text PJ</a></body></html>
EOF
echo "restaurant-payment-fee-savings-story.html,outcome-story" >> "$MANIFEST_FILE"

cat > "contractor-payout-speed-story.html" <<'EOF'
<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<title>Contractor Payout Speed Story | SideGuy Solutions</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="A contractor-style payout story showing how payout speed and fee structure affect working capital.">
<link rel="canonical" href="https://www.sideguysolutions.com/contractor-payout-speed-story.html">
<style>body{margin:0;font-family:-apple-system;background:linear-gradient(#eefcff,#fff);color:#0a2540} .wrap{max-width:900px;margin:0 auto;padding:40px 20px 90px} .card{background:#fff;padding:22px;border-radius:18px;margin:18px 0;box-shadow:0 10px 30px rgba(16,24,40,.08)} #pj-orb{position:fixed;right:18px;bottom:18px;background:#0ea5e9;color:#fff;padding:14px 18px;border-radius:999px;font-weight:700}</style>
</head><body><div class="wrap">
<div class="card"><h1>Contractor Payout Speed Story</h1><p>Fast payouts feel good until the speed premium starts eating working capital in a business with tight timing.</p></div>
<div class="card"><h2>What felt off</h2><p>Cash flow was fine on paper but worse in practice.</p></div>
<div class="card"><h2>What actually mattered</h2><ul><li>Payout timing cost</li><li>Monthly processing profile</li><li>Whether speed justified the premium</li></ul></div>
<div class="card"><h2>The move</h2><p>Compare the cash flow benefit against the annual speed tax.</p></div>
<div class="card"><p><a href="/payment-fee-outcomes.html">← Back to outcomes</a></p></div>
</div><a id="pj-orb" href="sms:+17735441231">💬 Text PJ</a></body></html>
EOF
echo "contractor-payout-speed-story.html,outcome-story" >> "$MANIFEST_FILE"

cat > "small-business-processor-switch-story.html" <<'EOF'
<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<title>Small Business Processor Switch Story | SideGuy Solutions</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="A small business processor-switch story about separating real savings from switch-for-the-sake-of-switching.">
<link rel="canonical" href="https://www.sideguysolutions.com/small-business-processor-switch-story.html">
<style>body{margin:0;font-family:-apple-system;background:linear-gradient(#eefcff,#fff);color:#0a2540} .wrap{max-width:900px;margin:0 auto;padding:40px 20px 90px} .card{background:#fff;padding:22px;border-radius:18px;margin:18px 0;box-shadow:0 10px 30px rgba(16,24,40,.08)} #pj-orb{position:fixed;right:18px;bottom:18px;background:#0ea5e9;color:#fff;padding:14px 18px;border-radius:999px;font-weight:700}</style>
</head><body><div class="wrap">
<div class="card"><h1>Small Business Processor Switch Story</h1><p>Switching processors only makes sense when the annual savings are real enough to overcome friction, time, and operational change.</p></div>
<div class="card"><h2>What felt off</h2><p>The business owner knew they were paying too much but did not know if switching was worth the hassle.</p></div>
<div class="card"><h2>What actually mattered</h2><ul><li>Blended fee rate</li><li>Software stack overlap</li><li>Migration friction</li></ul></div>
<div class="card"><h2>The move</h2><p>Set a real switching threshold before doing anything.</p></div>
<div class="card"><p><a href="/payment-fee-outcomes.html">← Back to outcomes</a></p></div>
</div><a id="pj-orb" href="sms:+17735441231">💬 Text PJ</a></body></html>
EOF
echo "small-business-processor-switch-story.html,outcome-story" >> "$MANIFEST_FILE"

echo "✅ Created outcome story pages"

########################################
# CHILD PAGES
########################################

for FILE in "${CHILD_PAGES[@]}"; do
  TITLE="$(titleize "$FILE")"

  cat > "$FILE" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>${TITLE} | SideGuy Solutions</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="${TITLE}. SideGuy helps you understand the real tradeoffs before you lose more margin.">
<link rel="canonical" href="${DOMAIN}/${FILE}">
<style>
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:linear-gradient(180deg,#eefcff 0%,#ffffff 100%);color:#0a2540}
.wrap{max-width:900px;margin:0 auto;padding:40px 20px 90px}
.card{background:#fff;border-radius:18px;padding:22px;margin:18px 0;box-shadow:0 10px 30px rgba(16,24,40,.08)}
#pj-orb{position:fixed;right:18px;bottom:18px;background:#0ea5e9;color:#fff;padding:14px 18px;border-radius:999px;font-weight:700}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h1>${TITLE}</h1>
    <p>Most businesses only notice payment friction after it compounds. This page exists to make the decision simpler before that happens.</p>
  </div>

  <div class="card">
    <h2>What actually matters</h2>
    <ul>
      <li>True annual cost</li>
      <li>Operational friction</li>
      <li>What changes the decision instead of just adding noise</li>
    </ul>
  </div>

  <div class="card">
    <h2>Best next move</h2>
    <p>Pressure-test the annual leak, then compare it to the switching or execution friction.</p>
  </div>

  <div class="card">
    <h2>Keep going</h2>
    <ul>
      <li><a href="/payment-fee-leak-optimization.html">Flagship payment fee leak page</a></li>
      <li><a href="/payment-fee-leak-calculator.html">Payment fee leak calculator</a></li>
      <li><a href="/payment-fee-outcomes.html">Outcome stories</a></li>
    </ul>
  </div>

  <div class="card">
    <p><a href="/index.html">← Back to Home</a></p>
  </div>
</div>

<a id="pj-orb" href="sms:+17735441231">💬 Text PJ</a>
</body>
</html>
EOF

  echo "${FILE},child" >> "$MANIFEST_FILE"
  echo "✅ Created $FILE"
done

########################################
# SITEMAP
########################################

ensure_sitemap
append_to_sitemap "$FLAGSHIP"
append_to_sitemap "$CALCULATOR"
append_to_sitemap "$OUTCOME_HUB"

for FILE in "${OUTCOME_PAGES[@]}"; do
  append_to_sitemap "$FILE"
done

for FILE in "${CHILD_PAGES[@]}"; do
  append_to_sitemap "$FILE"
done

echo "✅ Updated sitemap"

########################################
# HOMEPAGE LINK
########################################

append_home_link "$FLAGSHIP" "Why Your Payment Processor Is Quietly Eating Margin"
echo "✅ Added homepage link if missing"

########################################
# REPORT
########################################

cat > "$REPORT_FILE" <<EOF
# SideGuy Payment Vertical Proof Sprint

Timestamp: $DATE

## Assets created
- Flagship page: $FLAGSHIP
- Calculator page: $CALCULATOR
- Outcome hub: $OUTCOME_HUB
- Outcome pages: ${#OUTCOME_PAGES[@]}
- Child pages: ${#CHILD_PAGES[@]}

## Goal
Prove the full loop:
problem -> decision -> escalation -> outcome

## KPI to track this week
- Visits to flagship page
- Calculator use
- Text PJ escalations
- Solved outcomes
- New objections discovered
EOF

echo "✅ Created report $REPORT_FILE"

########################################
# GIT
########################################

git add .
git commit -m "Build SideGuy payment vertical proof sprint v1 ($DATE)"

echo ""
echo "---------------------------------------"
echo "🔥 PAYMENT PROOF SPRINT COMPLETE"
echo "Flagship: $FLAGSHIP"
echo "Calculator: $CALCULATOR"
echo "Outcome hub: $OUTCOME_HUB"
echo "Child pages: ${#CHILD_PAGES[@]}"
echo "Manifest: $MANIFEST_FILE"
echo "Report: $REPORT_FILE"
echo "---------------------------------------"
