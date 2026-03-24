#!/usr/bin/env bash

########################################
# SIDEGUY AI INFRASTRUCTURE CLUSTER
# Educational/informational pages on AI infrastructure trends
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
DATE="$(date +"%Y-%m-%d-%H%M%S")"

cd "$PROJECT_ROOT" || exit 1

create_page() {
  SLUG="$1"
  TITLE="$2"
  META_DESC="$3"
  
  FILE="$PROJECT_ROOT/$SLUG.html"
  
  if [ -f "$FILE" ]; then
    echo "⏭️  Skipped (exists): $SLUG"
    return
  fi
  
  cat > "$FILE" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TITLE_PLACEHOLDER | SideGuy Solutions</title>
<meta name="description" content="META_DESC_PLACEHOLDER">
<link rel="canonical" href="https://sideguy.solutions/SLUG_PLACEHOLDER.html">
<style>
:root {
  --bg0: #eefcff;
  --bg1: #ffffff;
  --ink: #073044;
  --ink-dim: #5a7b8c;
  --mint: #21d3a1;
  --mint-hover: #1ab88a;
  --border: #d1e8ed;
  --phone: "+17735441231";
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
  background: radial-gradient(circle at 30% 20%, rgba(33, 211, 161, 0.08) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(7, 48, 68, 0.06) 0%, transparent 50%),
              var(--bg0);
  color: var(--ink);
  line-height: 1.7;
  padding: 20px;
}

.container {
  max-width: 820px;
  margin: 0 auto;
  background: var(--bg1);
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 2px 12px rgba(7, 48, 68, 0.08);
}

header {
  margin-bottom: 40px;
}

h1 {
  font-size: 2.2em;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.2;
  margin-bottom: 16px;
}

h2 {
  font-size: 1.5em;
  font-weight: 600;
  color: var(--ink);
  margin-top: 32px;
  margin-bottom: 16px;
}

h3 {
  font-size: 1.2em;
  font-weight: 600;
  color: var(--ink);
  margin-top: 24px;
  margin-bottom: 12px;
}

p {
  margin-bottom: 16px;
  color: var(--ink);
}

ul {
  margin: 16px 0 16px 24px;
  color: var(--ink);
}

li {
  margin-bottom: 8px;
}

.context-box {
  margin: 32px 0;
  padding: 24px;
  background: rgba(33, 211, 161, 0.05);
  border-left: 4px solid var(--mint);
  border-radius: 8px;
}

.cta-box {
  margin: 40px 0;
  padding: 32px;
  background: linear-gradient(135deg, rgba(33, 211, 161, 0.08) 0%, rgba(33, 211, 161, 0.03) 100%);
  border: 2px solid var(--border);
  border-radius: 12px;
}

.cta-box h3 {
  margin-top: 0;
  color: var(--ink);
}

.phone-link {
  display: inline-block;
  font-size: 1.2em;
  font-weight: 700;
  color: var(--mint);
  text-decoration: none;
  margin: 16px 0;
  padding: 12px 24px;
  background: var(--bg1);
  border: 2px solid var(--mint);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.phone-link:hover {
  background: var(--mint);
  color: var(--bg1);
}

.back-link {
  display: inline-block;
  margin-top: 32px;
  color: var(--ink-dim);
  text-decoration: none;
  font-size: 0.95em;
}

.back-link:hover {
  color: var(--mint);
}

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 32px 0;
}

@media (max-width: 640px) {
  body {
    padding: 12px;
  }
  
  .container {
    padding: 24px;
  }
  
  h1 {
    font-size: 1.8em;
  }
  
  h2 {
    font-size: 1.3em;
  }
}
</style>
</head>

<body>

<div class="container">

<header>
<h1>TITLE_PLACEHOLDER</h1>
</header>

<main>

<p>This topic is coming up more often as AI deployment accelerates. Most people hear about it in passing but don't fully understand what's actually happening at the infrastructure level.</p>

<h2>What this means</h2>
<p>AI systems — especially large language models and training workloads — require massive amounts of computing power. That translates directly to physical infrastructure: electricity generation, distribution systems, cooling, and data center construction at unprecedented scale.</p>

<div class="context-box">
<p style="margin: 0;"><strong>Context:</strong> A single large AI training run can consume as much power as a small town for weeks. Multiply that across hundreds of companies racing to build and deploy AI systems, and the infrastructure demands become substantial.</p>
</div>

<h2>Why it matters</h2>
<p>This isn't just a tech industry issue. It affects:</p>
<ul>
  <li><strong>Energy costs</strong> — increased demand impacts pricing and availability</li>
  <li><strong>Business operations</strong> — companies planning AI deployments need infrastructure strategies</li>
  <li><strong>Investment decisions</strong> — infrastructure buildout creates new opportunities and risks</li>
  <li><strong>Grid stability</strong> — regional power systems need to adapt to concentrated demand</li>
</ul>

<h2>What to watch</h2>
<p>The space is evolving rapidly. Key trends include:</p>
<ul>
  <li>Hyperscale data center construction accelerating</li>
  <li>Energy companies partnering directly with AI/tech firms</li>
  <li>New cooling technologies to handle dense compute loads</li>
  <li>Regulatory discussions around energy allocation</li>
  <li>On-site power generation (solar, natural gas) becoming more common</li>
</ul>

<h2>Reality check</h2>
<p>Much of the conversation around AI infrastructure is either overhyped ("AI will crash the grid") or dismissive ("it's not a big deal"). The reality is somewhere in the middle — it's a significant challenge that requires planning and investment, but it's solvable with existing technology and reasonable capital allocation.</p>

<hr>

<section class="cta-box">
<h3>Trying to figure this out for your business?</h3>
<p>Whether you're planning AI infrastructure, evaluating costs, or just trying to understand what's real vs. hype — SideGuy can help you cut through the noise.</p>
<a href="tel:+17735441231" class="phone-link">Text PJ: 773-544-1231</a>
<p style="font-size: 0.9em; color: var(--ink-dim); margin-top: 12px;">Fast clarity, no sales pressure. We'll either help or tell you we can't.</p>
</section>

</main>

<footer>
<a href="/" class="back-link">← Back to SideGuy Solutions</a>
</footer>

</div>

</body>
</html>
EOF

  # Replace placeholders
  sed -i "s|TITLE_PLACEHOLDER|$TITLE|g" "$FILE"
  sed -i "s|META_DESC_PLACEHOLDER|$META_DESC|g" "$FILE"
  sed -i "s|SLUG_PLACEHOLDER|$SLUG|g" "$FILE"
  
  echo "✅ Created: $SLUG.html"
}

########################################
# AI INFRASTRUCTURE CLUSTER
########################################

create_page \
  "ai-data-center-infrastructure-explained" \
  "AI Data Center Infrastructure Explained" \
  "Understanding the physical infrastructure behind AI systems: power requirements, cooling, and why data center construction is accelerating."

create_page \
  "electric-data-infrastructure-what-it-means" \
  "Electric Data Infrastructure — What It Means" \
  "How electrical infrastructure is evolving to support data-intensive AI workloads, and what that means for energy systems."

create_page \
  "future-of-ai-data-centers-energy-demand" \
  "Future of AI Data Centers — Energy Demand" \
  "Projecting energy requirements for next-generation AI data centers: scale, timing, and infrastructure readiness."

create_page \
  "ai-data-center-power-consumption-explained" \
  "AI Data Center Power Consumption Explained" \
  "Breaking down power usage in AI-focused data centers: training vs. inference, efficiency improvements, and real-world numbers."

create_page \
  "ai-data-center-energy-usage-breakdown" \
  "AI Data Center Energy Usage Breakdown" \
  "Where the energy goes in AI facilities: compute, cooling, networking, and overhead. Understanding the cost structure."

create_page \
  "how-ai-is-impacting-the-power-grid" \
  "How AI Is Impacting The Power Grid" \
  "AI data centers creating concentrated power demand. Grid capacity, regional impacts, and utility responses explained."

create_page \
  "data-center-electricity-demand-future" \
  "Data Center Electricity Demand — Future Outlook" \
  "Forecasting electricity needs for data centers through 2030. What's realistic, what's hype, and what infrastructure is required."

create_page \
  "why-ai-needs-more-energy-infrastructure" \
  "Why AI Needs More Energy Infrastructure" \
  "The technical reasons AI training and deployment require significantly more power than traditional computing workloads."

create_page \
  "how-ai-data-centers-are-built" \
  "How AI Data Centers Are Built" \
  "Construction and design considerations for AI-optimized facilities: power distribution, cooling architecture, and buildout timelines."

create_page \
  "ai-infrastructure-companies-to-know" \
  "AI Infrastructure Companies To Know" \
  "Key players in AI infrastructure: data center operators, electrical contractors, cooling technology providers, and emerging specialists."

create_page \
  "what-powers-modern-data-centers" \
  "What Powers Modern Data Centers" \
  "Energy sources for hyperscale facilities: grid power, on-site generation, renewables, and backup systems explained."

create_page \
  "cooling-systems-for-ai-data-centers" \
  "Cooling Systems For AI Data Centers" \
  "Why AI workloads generate more heat and how modern cooling systems (liquid, immersion, hybrid) handle extreme thermal loads."

create_page \
  "ai-data-center-cost-breakdown" \
  "AI Data Center Cost Breakdown" \
  "Understanding capex and opex for AI facilities: construction, power, cooling, hardware, and ongoing operational costs."

create_page \
  "how-businesses-can-prepare-for-ai-infrastructure" \
  "How Businesses Can Prepare For AI Infrastructure" \
  "Practical steps for companies planning AI deployments: capacity assessment, cost modeling, and infrastructure readiness."

create_page \
  "investing-in-ai-energy-infrastructure" \
  "Investing In AI Energy Infrastructure" \
  "Investment landscape for AI infrastructure: opportunities, risks, and who's building the physical systems behind AI growth."

create_page \
  "ai-data-center-management-tools" \
  "AI Data Center Management Tools" \
  "Software and monitoring systems for managing AI infrastructure: power monitoring, thermal management, and capacity planning."

create_page \
  "will-ai-break-the-power-grid" \
  "Will AI Break The Power Grid?" \
  "Separating reality from hype: can electrical grids handle AI growth, and what's needed to prevent capacity issues."

create_page \
  "next-generation-data-centers-explained" \
  "Next Generation Data Centers Explained" \
  "What's different about facilities being built now vs. five years ago: density, efficiency, and design evolution."

create_page \
  "ai-infrastructure-boom-what-to-expect" \
  "AI Infrastructure Boom — What To Expect" \
  "Market dynamics, construction timelines, and realistic expectations for AI infrastructure expansion over the next 3-5 years."

create_page \
  "electric-infrastructure-for-ai-future" \
  "Electric Infrastructure For AI Future" \
  "Long-term electrical infrastructure requirements to support AI: transmission upgrades, generation capacity, and regional strategies."

########################################
# FINISH
########################################

echo ""
echo "✅ AI infrastructure cluster created"
echo "📋 Next: Run ./generate-sitemap-failsafe.sh to update sitemap"
echo ""
