#!/usr/bin/env bash
# tools/deal-router-engine.sh
# SIDEGUY DEAL ROUTER ENGINE (PRO MODE)
# Traffic → Intent → Text → Deal → Authority

set -euo pipefail

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo "=================================================="
echo "SIDEGUY DEAL ROUTER ENGINE (PRO MODE)"
echo "Traffic → Intent → Text → Deal → Authority"
echo "=================================================="

DATE=$(date +"%Y-%m-%d-%H-%M")

#################################################
# HELPERS
#################################################

# title_case: "hello-world" → "Hello World"
# Also uppercases known acronyms: hvac→HVAC, ev→EV, ai→AI
title_case() {
  echo "$1" | sed 's/-/ /g' | awk '{
    for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))
    print
  }' | sed '
    s/\bHvac\b/HVAC/g
    s/\bEv\b/EV/g
    s/\bAi\b/AI/g
    s/\bTesla\b/Tesla/g
  '
}

# safe_write: only write if file does not already exist
safe_write() {
  FILE=$1
  if [ ! -f "$FILE" ]; then
    cat > "$FILE"
    echo "  CREATED: $FILE"
  else
    echo "  SKIPPED: $FILE (already exists)"
  fi
}

#################################################
# 1. SCALE PAGE GENERATOR (HIGH INTENT SEO)
#    6 topics × 5 locations × 4 patterns = 120 pages
#    Each page is production-quality:
#      - charset / viewport / canonical / og tags
#      - FAQPage JSON-LD schema
#      - Inline sg2026 design (aurora, glass cards, shine CTA)
#      - Text PJ floating button
#################################################

mkdir -p public/scale-pages logs/scale

topics=("hvac" "solar" "roof" "plumbing" "tesla" "payment-processing")
locations=("san-diego" "encinitas" "carlsbad" "la-jolla" "oceanside")
patterns=("repair-or-replace" "cost-of" "is-it-worth-it" "best-option")

echo ""
echo "[ 1 ] Generating scale pages..."
built=0

for topic in "${topics[@]}"; do
  for location in "${locations[@]}"; do
    for pattern in "${patterns[@]}"; do

      slug="${topic}-${pattern}-${location}"
      file="public/scale-pages/${slug}.html"

      [ -f "$file" ] && continue

      T=$(title_case "$topic")
      L=$(title_case "$location")
      P=$(title_case "$pattern")
      H1="${T}: ${P} in ${L}?"
      DESC="${T} ${P} in ${L} — get the honest answer before you spend money. SideGuy guides you. Text PJ: 773-544-1231."
      CANONICAL="https://sideguysolutions.com/scale-pages/${slug}.html"

      cat > "$file" <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>${T} ${P} ${L} · SideGuy Solutions</title>
  <meta name="description" content="${DESC}"/>
  <link rel="canonical" href="${CANONICAL}"/>
  <meta property="og:title" content="${T} ${P} ${L} · SideGuy Solutions"/>
  <meta property="og:description" content="${DESC}"/>
  <meta property="og:url" content="${CANONICAL}"/>
  <meta property="og:image" content="https://sideguysolutions.com/og-preview.png"/>
  <meta property="og:type" content="article"/>
  <meta name="robots" content="index, follow, max-image-preview:large"/>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What is the ${P} for ${T} in ${L}?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "The right answer depends on the age and condition of your equipment, current ${L} labor rates, and whether repair costs are approaching replacement value. SideGuy helps you evaluate this without a sales agenda. Text PJ at 773-544-1231."
        }
      },
      {
        "@type": "Question",
        "name": "How do I decide on ${T} ${P} without getting ripped off?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Get two assessments from different contractors, then ask an independent source. SideGuy gives you a free plain-language read on what you heard — text PJ at 773-544-1231 before you sign anything."
        }
      }
    ]
  }
  </script>
  <style>
  :root{--bg0:#eefcff;--ink:#073044;--muted:#3f6173;--mint:#21d3a1;--mint2:#00c7ff;--blue2:#1f7cff;--r:18px;--pill:999px}
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;background:radial-gradient(ellipse at 65% 0%,#c5f4ff 0%,#eefcff 55%,#fff 100%);color:var(--ink);min-height:100vh;position:relative}
  body:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;animation:sg-aurora 26s ease-in-out infinite;background:radial-gradient(closest-side at 15% 18%,rgba(33,211,161,.22),transparent 56%),radial-gradient(closest-side at 80% 24%,rgba(74,169,255,.18),transparent 52%);filter:blur(24px)}
  @keyframes sg-aurora{0%{transform:translate(0,0) scale(1)}50%{transform:translate(1.5%,-1%) scale(1.03)}100%{transform:translate(0,0) scale(1)}}
  a{color:var(--blue2);text-decoration:none}a:hover{text-decoration:underline}
  nav.bc{padding:11px 24px;font-size:.8rem;color:var(--muted);border-bottom:1px solid rgba(0,0,0,.06);background:rgba(255,255,255,.72);backdrop-filter:blur(8px);position:sticky;top:0;z-index:10}
  nav.bc a{color:var(--muted)}
  .wrap{max-width:860px;margin:0 auto;padding:48px 24px 80px;position:relative;z-index:1}
  .badge{display:inline-block;background:var(--mint);color:#073044;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 12px;border-radius:var(--pill);margin-bottom:14px}
  h1{font-size:clamp(26px,5vw,48px);font-weight:800;line-height:1.08;letter-spacing:-.03em;margin-bottom:14px;background:linear-gradient(135deg,var(--ink) 0%,#0c5f78 30%,var(--mint) 62%,var(--mint2) 88%);background-size:250% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:sg-grad 14s ease-in-out infinite}
  @keyframes sg-grad{0%,100%{background-position:0% 50%}50%{background-position:200% 50%}}
  .lede{font-size:1.05rem;color:var(--muted);line-height:1.7;margin-bottom:32px;max-width:640px}
  h2{font-size:1.1rem;font-weight:800;margin:36px 0 14px;color:var(--ink)}
  p{line-height:1.7;color:var(--muted);margin-bottom:14px}
  .card{background:linear-gradient(155deg,rgba(255,255,255,.84),rgba(255,255,255,.60));border:1px solid rgba(255,255,255,.74);border-radius:var(--r);backdrop-filter:blur(18px) saturate(160%);-webkit-backdrop-filter:blur(18px) saturate(160%);box-shadow:0 2px 0 rgba(255,255,255,.84) inset,0 12px 36px rgba(7,48,68,.08);padding:24px 22px;margin-bottom:14px;transition:transform .25s cubic-bezier(.34,1.56,.64,1)}
  .card:hover{transform:translateY(-4px)}
  .two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:16px 0}
  .two-col .card{margin-bottom:0}
  .card-icon{font-size:1.4rem;margin-bottom:8px}
  .card-title{font-weight:700;margin-bottom:6px;color:var(--ink)}
  .card-desc{font-size:.88rem;color:var(--muted);line-height:1.6}
  .cta-box{background:linear-gradient(135deg,#073044,#0e3d58);border-radius:var(--r);padding:30px 32px;color:#fff;margin:40px 0;display:flex;align-items:center;gap:22px;flex-wrap:wrap}
  .cta-box h3{font-size:1.1rem;font-weight:700;margin-bottom:5px;color:#fff}
  .cta-box p{font-size:.9rem;opacity:.82;margin:0;color:#fff}
  .cta-btn{flex-shrink:0;background:linear-gradient(100deg,var(--mint) 0%,var(--mint2) 50%,var(--mint) 100%);background-size:200% 100%;animation:sg-shine 3.8s linear infinite;color:#073044;font-weight:700;padding:12px 22px;border-radius:var(--pill);white-space:nowrap;box-shadow:0 0 0 1px rgba(255,255,255,.4) inset}
  @keyframes sg-shine{from{background-position:-200% center}to{background-position:200% center}}
  .cta-btn:hover{transform:translateY(-2px);text-decoration:none}
  .floating{position:fixed;bottom:22px;right:22px;z-index:999}
  .floatBtn{display:flex;align-items:center;gap:8px;background:linear-gradient(135deg,#0e3d58,#073044);color:#fff;padding:11px 18px;border-radius:var(--pill);font-size:.88rem;font-weight:600;text-decoration:none;box-shadow:0 4px 18px rgba(0,0,0,.22)}
  footer{text-align:center;padding:20px;font-size:.78rem;color:var(--muted);border-top:1px solid rgba(0,0,0,.06);margin-top:36px}
  @media(max-width:600px){.cta-box{flex-direction:column;gap:14px}.floating{bottom:14px;right:14px}.two-col{grid-template-columns:1fr}}
  </style>
</head>
<body>
<a href="#main" style="position:absolute;left:-999px;top:auto;width:1px;height:1px;overflow:hidden">Skip to content</a>
<nav class="bc" aria-label="Breadcrumb">
  <a href="/">SideGuy</a> › <a href="/knowledge-hub.html">Guides</a> › ${L} › ${T}
</nav>
<main id="main" class="wrap">
  <div class="badge">Decision Guide · ${L}</div>
  <h1>${H1}</h1>
  <p class="lede">Most people make the wrong call here because they're deciding under pressure, without the full picture. Here's the honest framework — before you call anyone.</p>

  <h2>The Two Questions That Actually Matter</h2>
  <div class="two-col">
    <div class="card">
      <div class="card-icon">💰</div>
      <div class="card-title">What's the real cost comparison?</div>
      <div class="card-desc">Don't just compare the quote you got. Factor in future repair probability, energy efficiency delta, and expected lifespan of current equipment.</div>
    </div>
    <div class="card">
      <div class="card-icon">🔍</div>
      <div class="card-title">Who gave you that number?</div>
      <div class="card-desc">Contractors in ${L} have financial incentive toward one answer. Get a second opinion, ideally from someone with no stake in what you decide.</div>
    </div>
  </div>

  <h2>The 50% Rule of Thumb</h2>
  <p>In the trades, there's a general guide: if repair cost exceeds 50% of replacement cost <em>and</em> the equipment is past 60% of its expected lifespan, replacement usually wins on a 5-year cost basis. But this varies significantly by equipment condition, brand reliability, and local ${L} labor rates. It's a starting point, not a verdict.</p>

  <h2>What to Do Before You Commit</h2>
  <p>Get at least two assessments. Write down the exact numbers both gave you. Then text PJ at 773-544-1231 with those numbers and what each contractor recommended — he'll give you an independent read in plain language, free.</p>

  <div class="cta-box">
    <div>
      <h3>Get an Honest Read Before You Decide</h3>
      <p>One text. No sales pitch. Just clarity on the ${T} decision in ${L}.</p>
    </div>
    <a class="cta-btn" href="sms:+17735441231">💬 Text PJ Now →</a>
  </div>
</main>
<div class="floating">
  <a class="floatBtn" href="sms:+17735441231" aria-label="Text PJ for help">💬 Text PJ</a>
</div>
<footer>
  <p>© 2026 SideGuy Solutions · San Diego, CA · <a href="/">Home</a> · <a href="/knowledge-hub.html">Knowledge Hub</a> · Clarity before cost.</p>
</footer>
</body>
</html>
HTML

      echo "${DATE} CREATED ${file}" >> logs/scale/build.log
      built=$((built + 1))

    done
  done
done

echo "  Scale pages built: ${built}"

#################################################
# 2. CONVERSION LAYER
#################################################

echo ""
echo "[ 2 ] Conversion layer..."

mkdir -p tools/conversion

safe_write tools/conversion/cta.html <<'EOF'
<a href="sms:+17735441231" style="
  position:fixed;right:20px;bottom:20px;z-index:9999;
  display:flex;align-items:center;gap:8px;
  background:linear-gradient(135deg,#21d3a1,#00c7ff);
  color:#073044;padding:13px 18px;border-radius:999px;
  font-weight:bold;font-family:-apple-system,system-ui,sans-serif;font-size:.9rem;
  text-decoration:none;box-shadow:0 4px 18px rgba(0,199,255,.32);">
  💬 Text PJ
</a>
EOF

#################################################
# 3. HIGH VALUE LEAD DETECTION
#################################################

echo ""
echo "[ 3 ] High value lead detector..."

mkdir -p logs/responder tools/escalation

safe_write tools/escalation/high-value.sh <<'EOF'
#!/usr/bin/env bash
# Filters inbox for high-intent leads (cost, price, quote, repair, install, urgent)

INPUT="logs/responder/inbox.txt"
OUTPUT="logs/responder/high-value.txt"

if [ ! -f "$INPUT" ]; then
  echo "No inbox at $INPUT — nothing to process"
  exit 0
fi

> "$OUTPUT"
grep -iE "cost|price|quote|repair|install|urgent|replace|asap|emergency" "$INPUT" >> "$OUTPUT"

count=$(wc -l < "$OUTPUT")
echo "High value leads detected: ${count}"
EOF

chmod +x tools/escalation/high-value.sh

#################################################
# 4. INTENT → DEAL MAPPING
#################################################

echo ""
echo "[ 4 ] Intent → deal mapper..."

mkdir -p docs/fusion tools/fusion

safe_write tools/fusion/map.sh <<'EOF'
#!/usr/bin/env bash
# Maps high-value leads to deal categories

INPUT="logs/responder/high-value.txt"
OUTPUT="docs/fusion/deal-map.txt"

if [ ! -f "$INPUT" ]; then
  echo "No high-value leads at $INPUT — run high-value.sh first"
  exit 0
fi

{ echo "--- Deal Map: $(date) ---"; } > "$OUTPUT"

while IFS= read -r line; do
  if   echo "$line" | grep -qiE "hvac|ac|heat|furnace|cooling";  then echo "$line → HVAC DEAL"     >> "$OUTPUT"
  elif echo "$line" | grep -qiE "solar|panel|battery|powerwall"; then echo "$line → SOLAR DEAL"    >> "$OUTPUT"
  elif echo "$line" | grep -qiE "roof|shingle|leak|gutter";      then echo "$line → ROOFING DEAL"  >> "$OUTPUT"
  elif echo "$line" | grep -qiE "plumb|pipe|drain|toilet|water"; then echo "$line → PLUMBING DEAL" >> "$OUTPUT"
  elif echo "$line" | grep -qiE "tesla|ev|charger|electric car"; then echo "$line → EV DEAL"       >> "$OUTPUT"
  elif echo "$line" | grep -qiE "payment|stripe|charge|invoice"; then echo "$line → PAYMENTS DEAL" >> "$OUTPUT"
  else                                                                 echo "$line → GENERAL"        >> "$OUTPUT"
  fi
done < "$INPUT"

echo "Deal map written → $OUTPUT"
EOF

chmod +x tools/fusion/map.sh

#################################################
# 5. PRIORITY SIGNAL
#################################################

echo ""
echo "[ 5 ] Running priority signal..."

if [ -f tools/intelligence/priority/priority-engine.sh ]; then
  bash tools/intelligence/priority/priority-engine.sh 2>/dev/null
else
  echo "  priority-engine.sh not found — skipping"
fi

#################################################
# DONE
#################################################

echo ""
echo "======================================="
echo "  SIDEGUY DEAL ENGINE COMPLETE"
echo "  Scale pages built : ${built}"
echo "  Run date          : ${DATE}"
echo "======================================="
echo ""
