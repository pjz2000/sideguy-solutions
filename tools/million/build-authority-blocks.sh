#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

INPUT="docs/million-page/authority/upgrade-candidates.csv"
[ -f "$INPUT" ] || { echo "No upgrade-candidates.csv found."; exit 1; }

mkdir -p docs/million-page/authority/blocks

tail -n +2 "$INPUT" | while IFS=, read -r url title h1 theme audience use_case industry city state modifier page_type intent score; do
  clean_url="$(echo "$url"       | tr -d '"')"
  clean_theme="$(echo "$theme"   | sed 's/^"//;s/"$//')"
  clean_industry="$(echo "$industry" | sed 's/^"//;s/"$//')"
  clean_city="$(echo "$city"     | sed 's/^"//;s/"$//')"
  clean_state="$(echo "$state"   | sed 's/^"//;s/"$//')"
  slug="$(basename "$clean_url" .html)"
  block="docs/million-page/authority/blocks/${slug}.html"

  cat > "$block" <<HTML
<section class="sideguy-authority">
  <h2>How this technology is actually used</h2>
  <p>Organizations exploring <strong>${clean_theme}</strong> typically want practical clarity, not hype. Implementation, security, and operational impact matter more than buzzwords.</p>
  <p>For <strong>${clean_industry}</strong> teams operating in <strong>${clean_city}, ${clean_state}</strong>, the real question is whether the technology solves a real operational problem or simply adds complexity.</p>
</section>

<section>
  <h2>Practical implementation considerations</h2>
  <ul>
    <li>Integration with existing systems</li>
    <li>Security and compliance implications</li>
    <li>Cost versus operational value</li>
    <li>Training and change management</li>
    <li>Vendor lock-in risk</li>
  </ul>
</section>

<section>
  <h2>SideGuy perspective</h2>
  <p>SideGuy focuses on clarity before cost. Many organizations adopt technology too quickly without understanding the operational implications.</p>
  <p>Our goal is calm explanation first — implementation second.</p>
</section>

<section>
  <h2>Related technology topics</h2>
  <ul>
    <li><a href="/ai-agents-answer-engine-traffic.html">AI Agents &amp; Answer Engines</a></li>
    <li><a href="/machine-to-machine-payments.html">Machine to Machine Payments</a></li>
    <li><a href="/solana-payments.html">Solana Payments</a></li>
    <li><a href="/usdc-merchant-payments.html">USDC Merchant Payments</a></li>
  </ul>
</section>
HTML
done

echo "Authority blocks generated in docs/million-page/authority/blocks/"
