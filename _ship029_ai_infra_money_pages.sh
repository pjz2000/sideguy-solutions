#!/usr/bin/env bash
########################################
# SIDEGUY AI INFRASTRUCTURE MONEY PAGES
# Production-quality pages for infrastructure/compute inquiries
# Architecture: Root-level HTML, inline CSS, real content
########################################

set -eo pipefail

PROJECT_ROOT="/workspaces/sideguy-solutions"
DATE="$(date +"%Y-%m-%d-%H%M%S")"

cd "$PROJECT_ROOT" || exit 1

SITEMAP_NOTE="sitemap-new-pages-$DATE.txt"
> "$SITEMAP_NOTE"

########################################
# PAGE GENERATOR FUNCTION
########################################
create_page() {
  SLUG="$1"
  TITLE="$2"
  META_DESC="$3"
  H1="$4"
  INTRO="$5"
  WHAT_THIS_MEANS="$6"
  WHAT_MATTERS="$7"
  NEXT_STEPS="$8"
  
  FILE="$PROJECT_ROOT/$SLUG.html"
  
  if [ -f "$FILE" ]; then
    echo "⏭️  Skipping: $SLUG (already exists)"
    return
  fi

  cat > "$FILE" <<HTMLEOF
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>${TITLE} | SideGuy Solutions</title>
<link rel="canonical" href="https://sideguy.solutions/${SLUG}.html"/>
<meta name="description" content="${META_DESC}" />

<style>
:root {
  --bg0:#eefcff;
  --bg1:#d7f5ff;
  --bg2:#bfeeff;
  --ink:#073044;
  --muted:#3f6173;
  --muted2:#5e7d8e;
  --card:#ffffffcc;
  --stroke:rgba(7,48,68,.10);
  --shadow:0 18px 50px rgba(7,48,68,.10);
  --mint:#21d3a1;
  --mint2:#00c7ff;
  --blue:#4aa9ff;
  --r:22px;
  --pill:999px;
  --phone:"+1-773-544-1231";
  --phonePretty:"773-544-1231";
  --city:"San Diego";
}

* { box-sizing:border-box; }
html, body { height:100%; }
body {
  margin:0;
  font-family:-apple-system, system-ui, Segoe UI, Roboto, Inter, Arial, sans-serif;
  color:var(--ink);
  background:radial-gradient(1200px 900px at 22% 10%, #ffffff 0%, var(--bg0) 25%, var(--bg1) 60%, var(--bg2) 100%);
  -webkit-font-smoothing:antialiased;
  overflow-x:hidden;
}

body:before {
  content:"";
  position:fixed;
  inset:-20%;
  background:
    radial-gradient(closest-side at 18% 20%, rgba(33,211,161,.18), transparent 55%),
    radial-gradient(closest-side at 78% 28%, rgba(74,169,255,.16), transparent 52%),
    radial-gradient(closest-side at 62% 82%, rgba(0,199,255,.12), transparent 55%);
  filter:blur(18px);
  pointer-events:none;
  z-index:-2;
}

.wrap {
  max-width:820px;
  margin:0 auto;
  padding:26px 22px 92px;
}

h1 {
  font-size:36px;
  line-height:1.1;
  margin:0 0 16px;
  letter-spacing:-.02em;
  color:var(--ink);
}

@media (max-width:640px) {
  h1 { font-size:28px; }
}

h2 {
  font-size:22px;
  font-weight:700;
  margin:32px 0 12px;
  color:var(--ink);
}

h3 {
  font-size:18px;
  font-weight:700;
  margin:24px 0 10px;
  color:var(--ink);
}

p {
  line-height:1.7;
  margin:0 0 16px;
  color:var(--muted);
}

ul {
  line-height:1.8;
  margin:0 0 16px;
  padding-left:22px;
  color:var(--muted);
}

li {
  margin-bottom:8px;
}

a {
  color:var(--mint);
  text-decoration:none;
  font-weight:600;
}

a:hover {
  text-decoration:underline;
}

.callout {
  margin:32px 0;
  padding:24px;
  border-radius:var(--r);
  background:var(--card);
  border:1px solid var(--stroke);
  box-shadow:var(--shadow);
}

.callout h3 {
  margin-top:0;
}

.cta-box {
  margin:40px 0;
  padding:28px;
  border-radius:var(--r);
  background:linear-gradient(135deg, rgba(33,211,161,.12), rgba(74,169,255,.10));
  border:1px solid rgba(33,211,161,.25);
}

.cta-box p {
  margin-bottom:12px;
  font-size:15px;
}

.phone-link {
  display:inline-block;
  padding:14px 24px;
  background:linear-gradient(135deg, var(--mint), var(--mint2));
  color:#ffffff;
  font-weight:700;
  border-radius:var(--pill);
  box-shadow:0 12px 24px rgba(33,211,161,.25);
  transition:transform .15s ease;
}

.phone-link:hover {
  transform:translateY(-2px);
  box-shadow:0 16px 32px rgba(33,211,161,.35);
  text-decoration:none;
}

.toplink {
  display:inline-block;
  margin-bottom:20px;
  font-size:14px;
  color:var(--muted2);
}

.timestamp {
  font-size:13px;
  color:var(--muted2);
  margin-bottom:20px;
  opacity:.8;
}

hr {
  border:none;
  border-top:1px solid var(--stroke);
  margin:32px 0;
}
</style>

<script>
document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("timestamp");
  if (el) el.textContent = new Date().toLocaleString();
});
</script>
</head>

<body>
<div class="wrap">
  <a href="/" class="toplink">← Back to SideGuy</a>
  
  <div id="timestamp" class="timestamp"></div>
  
  <h1>${H1}</h1>
  
  <p><strong>${INTRO}</strong></p>
  
  <h2>What this usually means</h2>
  <p>${WHAT_THIS_MEANS}</p>
  
  <h2>What actually matters</h2>
  <p>${WHAT_MATTERS}</p>
  
  <h2>What to do next</h2>
  <p>${NEXT_STEPS}</p>
  
  <hr />
  
  <div class="cta-box">
    <h3>Need real guidance?</h3>
    <p>This is where SideGuy helps you skip the confusion and get clarity fast.</p>
    <p>No pressure. No upsell. Just honest answers.</p>
    <a href="tel:+17735441231" class="phone-link">Text PJ: 773-544-1231</a>
  </div>
  
  <div class="callout">
    <h3>Why this matters now</h3>
    <p>AI compute infrastructure is moving fast. Companies are making expensive mistakes by committing to solutions before understanding their actual requirements. Good decisions come from understanding power, cooling, redundancy, and execution quality — not just hardware specs.</p>
  </div>
  
  <div style="margin-top:32px;padding:16px;text-align:center;font-size:13px;color:var(--muted2);">
    <span id="lastUpdated">Updated March 2026</span>
  </div>
</div>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "${TITLE} | SideGuy Solutions",
  "description": "${META_DESC}",
  "url": "https://sideguy.solutions/${SLUG}.html",
  "isPartOf": {
    "@type": "WebSite",
    "name": "SideGuy Solutions",
    "url": "https://sideguy.solutions"
  }
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "SideGuy Solutions",
  "description": "Human-first guidance for San Diego home and business owners",
  "url": "https://sideguy.solutions",
  "telephone": "+1-773-544-1231",
  "areaServed": {
    "@type": "City",
    "name": "San Diego"
  }
}
</script>
</body>
</html>
HTMLEOF
  
  echo "https://sideguy.solutions/$SLUG.html" >> "$SITEMAP_NOTE"
  echo "✅ Created: $SLUG.html"
}

########################################
# PAGE DEFINITIONS
########################################

create_page \
  "who-builds-ai-data-centers" \
  "Who Builds AI Data Centers" \
  "Who builds AI data centers? Real guidance on contractors, costs, and what matters for AI compute facilities. No sales pressure." \
  "Who Builds AI Data Centers?" \
  "This question usually comes from someone planning compute capacity, not just curious browsing." \
  "Most AI data centers are built by specialized electrical contractors with mission-critical experience. The vendors you see in headlines (Nvidia, Supermicro) handle hardware — but the real execution risk is in power delivery, cooling infrastructure, and building systems. You're looking at design-build firms with data center + high-voltage electrical expertise, not general contractors." \
  "Power availability is the first constraint. You need clean, redundant power at scale (think 5-50+ MW depending on GPU density). Second is cooling — liquid cooling changes everything about layout and infrastructure. Third is time: lead times for electrical gear are 12-24 months. Fourth is expertise: someone who built a warehouse is not qualified to build an AI compute facility." \
  "If you're serious about this, start with a feasibility study on your site's power capacity and utility interconnect timeline. Then talk to firms that have actually delivered hyperscale or colocation projects in the last 3 years. SideGuy can help you sort real builders from resellers. Text PJ at 773-544-1231 if this is even remotely on your roadmap."

create_page \
  "ai-data-center-electrical-contractors" \
  "AI Data Center Electrical Contractors" \
  "Finding electrical contractors for AI data centers. What to ask, how to vet, and what separates real expertise from marketing." \
  "AI Data Center Electrical Contractors — What You're Actually Looking For" \
  "You need someone who understands mission-critical power, not just commercial electrical work." \
  "AI data centers have different requirements than enterprise IT. You're looking at: medium voltage switchgear (15kV+), redundant UPS systems (2N or better), generator backup with fuel for 48+ hours, synchronous transfer switches, and liquid cooling distribution. Most 'data center electricians' have never touched this level of power density or redundancy. You need a contractor with experience in hyperscale colocation, utility substations, or critical healthcare facilities." \
  "Vet them on three things: (1) Have they delivered projects over 5 MW? (2) Do they have in-house engineers or just field crews? (3) Can they handle utility coordination and long-lead procurement? A good contractor will ask about your PUE targets, N+1 redundancy requirements, and backup fuel strategy before giving you a number. A bad one will quote per square foot without understanding your actual load." \
  "Get references from projects they completed in the last 24 months. Ask about change orders and commissioning timelines. If someone promises a 6-month build for greenfield AI compute, they're either lying or underestimating scope. Real timelines are 18-36 months depending on utility service and equipment lead times."

create_page \
  "data-center-power-infrastructure-cost" \
  "Data Center Power Infrastructure Cost" \
  "Real costs for data center power infrastructure — utility fees, equipment, installation, and what drives pricing." \
  "What Does Data Center Power Infrastructure Actually Cost?" \
  "Most estimates you find online are outdated or don't include utility interconnect fees." \
  "Power infrastructure costs break into four buckets: (1) Utility service extension ($50K-$2M+ depending on distance and capacity), (2) Switchgear and transformers ($200-$400/kW), (3) UPS systems ($150-$300/kW for N+1 lithium-ion), (4) Generator + fuel systems ($250-$400/kW). For a 10 MW facility, you're looking at $8-15M just for electrical infrastructure — before you touch HVAC, building shell, or IT equipment. Liquid cooling adds another 20-30% to mechanical costs." \
  "The real cost driver is redundancy level. Going from N to N+1 to 2N essentially doubles your electrical spend. Lead times matter too: if you need gear fast, expect 30-50% premiums for expedited manufacturing. Utility interconnect timeline is the wildcard — some regions have 6-month waits, others are 2+ years. That delay costs money in carrying costs even before you're operational." \
  "Budget for 15-20% contingency on power infrastructure. Equipment prices are volatile, and supply chain delays are common. Get a utility feasibility study ($15-50K) before signing a lease or purchasing land. If the site can't support your load without a substation upgrade, you just added $3-10M and 24 months to your timeline."

create_page \
  "how-to-build-ai-compute-facility" \
  "How To Build AI Compute Facility" \
  "Step-by-step reality check on building an AI compute facility — permitting, power, cooling, and execution timeline." \
  "How to Build an AI Compute Facility — What Nobody Tells You" \
  "This isn't just racking servers in a warehouse. It's a multi-year capital project." \
  "The real process: (1) Site selection based on power availability and fiber connectivity, (2) Utility feasibility study + interconnect application (6-24 months), (3) Design-build RFP with firms that have data center + electrical experience, (4) Permitting (3-12 months depending on jurisdiction), (5) Long-lead equipment procurement (transformers, switchgear, generators: 12-24 months), (6) Construction (12-18 months for shell + MEP), (7) Commissioning + testing (3-6 months). If everything goes perfectly, you're looking at 30-42 months from site selection to operational." \
  "Power and cooling dominate the timeline. Liquid cooling infrastructure changes your mechanical design entirely — you're dealing with coolant distribution, heat exchangers, and pumps instead of just CRAC units. Miss the cooling design and your GPUs will throttle. Miss the power design and you'll trip breakers under load. Both have happened to well-funded AI compute projects in the last 18 months." \
  "Don't start with hardware selection. Start with load calculations (kW per rack), redundancy requirements (N, N+1, 2N), and target PUE (power usage effectiveness). Work backwards from those to building requirements. If you're buying land, verify utility capacity in writing before closing. If you're leasing, confirm existing power infrastructure can support your load without major upgrades."

create_page \
  "data-center-electrical-upgrade-guide" \
  "Data Center Electrical Upgrade Guide" \
  "Planning electrical upgrades for existing data centers — capacity analysis, costs, and how to avoid downtime." \
  "Data Center Electrical Upgrade Guide — Adding Capacity Without Taking Everything Offline" \
  "Most electrical upgrades fail because they underestimate coordination complexity, not technical difficulty." \
  "Upgrading data center power means: (1) Load analysis to confirm current vs available capacity, (2) Determining if your utility service can support additional draw without infrastructure upgrades, (3) Evaluating if existing UPS/generator systems can scale or need replacement, (4) Planning phased cutover to avoid full-facility downtime. The hardest part isn't the electrical work — it's maintaining uptime during installation. You'll need bypass plans, temporary power, and load shedding strategies." \
  "If your existing service is near capacity, adding load may require utility transformer upgrades or service entrance expansion. That means utility coordination, permit delays, and extended timelines (6-18 months). UPS upgrades often require parallel operation of old + new systems during transition. Battery replacements (switching from VRLA to lithium-ion) can happen hot, but you need careful load balancing. Generator additions need fuel system tie-ins, synchronization controls, and load testing under real conditions." \
  "Get an electrical engineer to perform a detailed load study before buying any equipment. Verify your utility service agreement and confirm you're not near your contracted demand limit. Plan upgrades in phases to limit blast radius if something goes wrong. Testing under full load (not just nameplate capacity) is non-negotiable — many UPS and generator failures happen during first real-world loading, not during commissioning tests."

create_page \
  "mission-critical-electrical-services-explained" \
  "Mission Critical Electrical Services Explained" \
  "What 'mission critical' actually means for electrical infrastructure — redundancy, uptime requirements, and cost implications." \
  "Mission Critical Electrical Services Explained — What 'Five Nines' Really Costs" \
  "Mission critical doesn't just mean 'important.' It's a specific design and operational standard." \
  "Mission critical electrical systems are designed to deliver 99.999% uptime (five nines), which translates to ~5 minutes of downtime per year. Achieving this requires: redundant power paths (2N or N+1), automatic failover systems, continuous monitoring, predictive maintenance, and tested disaster recovery procedures. It's not just about having a backup generator — it's about ensuring every component in the power chain has a parallel path that can carry full load instantly." \
  "2N architecture means two independent power systems, each capable of supporting full load. N+1 means capacity for full load plus one additional unit. Going from N to 2N roughly doubles your electrical infrastructure cost. You're paying for redundant transformers, switchgear, UPS modules, generators, and distribution. Operating costs are higher too: you're running systems in parallel, performing weekly/monthly testing, and maintaining spare parts inventory." \
  "If you don't actually need five nines, don't pay for it. Many businesses claim 'mission critical' when they actually need 99.9% (8 hours/year downtime), which is achievable with N+1 and proper maintenance. Be honest about your uptime requirements and risk tolerance. Overbuilding redundancy means you're carrying capital and OpEx costs for insurance you may never use."

create_page \
  "ai-data-center-construction-companies" \
  "AI Data Center Construction Companies" \
  "Vetting construction companies for AI data center projects — what separates real builders from resellers." \
  "AI Data Center Construction Companies — Who Actually Knows What They're Doing" \
  "The AI boom has brought a lot of vendors claiming data center expertise. Most have zero experience with GPU-dense compute." \
  "Real AI data center builders have recent hyperscale or colocation experience (last 3 years). They should be able to reference projects over 5 MW with liquid cooling systems. Ask for: (1) PUE targets they've delivered (under 1.3 is credible for modern facilities), (2) Rack density maximums (40+ kW/rack is GPU territory), (3) Utility coordination experience (medium voltage, substation tie-ins), (4) Commissioning process for high-density compute loads. If they've only done enterprise IT or telecom, they're learning on your dime." \
  "Watch for design-build firms vs general contractors. Design-build integrates engineering into construction, which is critical for fast-moving requirements. General contractors coordinate subs but often lack in-house engineering depth. For AI compute, you want design-build with MEP (mechanical, electrical, plumbing) engineering in-house. Ask how they handle change orders, long-lead procurement, and commissioning delays — those are where projects blow up." \
  "Vet references hard. Call the project owners, not just the contractor. Ask: Did they deliver on time? How many change orders? Were there post-commissioning issues? How did they handle unexpected site conditions? What's their spare parts and warranty support like? A good builder will give you references who are happy to talk. A bad one will dodge or give you cherry-picked examples."

create_page \
  "data-center-power-requirements-explained" \
  "Data Center Power Requirements Explained" \
  "Understanding data center power requirements — load calculations, redundancy, and how to size infrastructure." \
  "Data Center Power Requirements Explained — How to Size Your Infrastructure Without Overbuilding" \
  "Most data center power sizing is either overbuilt (wasting capital) or undersized (limiting future capacity)." \
  "Start with IT load: compute (servers, GPUs), networking (switches, routers), and storage. Multiply by 1.3-1.5x for power distribution losses and inefficiencies. Add cooling load: for air-cooled facilities, plan 0.8-1.2x the IT load. For liquid-cooled GPU clusters, cooling can be 0.3-0.5x IT load (much more efficient). Then add overhead: lighting, physical security, fire suppression (usually 5-10% of total). That gives you total facility load in kW." \
  "Redundancy adds to requirements. N+1 means you size for peak load plus one additional unit of capacity. 2N means two independent systems, each capable of full load. If your IT load is 10 MW and you go 2N, you're building electrical infrastructure for 20 MW. UPS and generator systems must match your redundancy target: if power fails, your backup systems need to carry full load without overloading." \
  "Size for growth but don't overbuild. Electrical infrastructure has 15-30 year lifespans, but IT load density changes every 3-5 years. Build your power backbone (utility service, main switchgear) for 10-year capacity, but keep UPS and branch distribution modular so you can add capacity incrementally. Overbuilding costs you in capital, financing, and operational overhead for capacity you're not using."

create_page \
  "ai-infrastructure-contractors-near-me" \
  "AI Infrastructure Contractors Near Me" \
  "Finding qualified AI infrastructure contractors — local vs national firms, what to look for, and how to vet experience." \
  "AI Infrastructure Contractors — Local vs National and What Actually Matters" \
  "Location matters less than experience. A local contractor with zero data center work will cost you more than a national firm with hyperscale expertise." \
  "For AI compute infrastructure, you want: (1) Electrical contractors with medium voltage + mission critical experience, (2) Mechanical contractors with liquid cooling or high-density HVAC expertise, (3) Controls integrators who understand BMS, DCIM, and automated failover systems. Local presence helps for permitting and site logistics, but execution quality depends on specialized experience. A national firm with a local project office often delivers better results than a local GC subbing out to specialized trades." \
  "Ask about recent projects: facility size (MW), rack density (kW/rack), cooling type (air vs liquid), and commissioning outcomes. If they can't cite specific numbers or reference projects, they're not experienced. Check licensing: data center electrical work often requires PE (professional engineer) stamps for permit approval. Verify insurance: mission critical work should carry $5-10M+ general liability and professional liability coverage." \
  "Use RFPs wisely. Don't ask for lump-sum pricing on incomplete designs — you'll get inflated bids with huge contingencies. Instead, use GMP (guaranteed maximum price) contracts with clear scope definition and allowance items for long-lead procurement. Negotiate change order processes upfront. Have a third-party commissioning agent to verify work quality before you take ownership."

create_page \
  "electrical-infrastructure-for-ai-facilities" \
  "Electrical Infrastructure For AI Facilities" \
  "Electrical infrastructure for AI facilities — power density, redundancy, cooling integration, and future-proofing." \
  "Electrical Infrastructure for AI Facilities — What GPU Clusters Actually Need" \
  "AI workloads are not traditional IT loads. Power density and transient loads break standard data center assumptions." \
  "Modern GPU clusters (H100, B200-class) pull 40-80 kW per rack under full load, with transient spikes 20% higher during training runs. That's 5-10x denser than traditional enterprise IT (5-10 kW/rack). Your electrical infrastructure needs: (1) Oversized branch circuits to handle transient loads without tripping breakers, (2) UPS systems with high crest factor tolerance (lithium-ion handles this better than VRLA), (3) Power monitoring at rack-level granularity to catch overloads before they cascade, (4) Cooling integration — liquid cooling changes your electrical distribution because you're pumping coolant, not just running fans." \
  "Redundancy strategy changes with AI workloads. Training runs can checkpoint and restart, so some facilities accept N+1 instead of 2N to save costs. Inference workloads serving live applications need higher availability. Match your redundancy to workload type, not blanket 'mission critical' standards. Generator sizing matters: plan for 110-120% of peak IT load to handle startup inrush and transient loads. Fuel capacity for 48-72 hours of runtime is standard." \
  "Future-proof your power backbone. Utility service, main switchgear, and transformers have 20-30 year lifespans. Size these for 10-year growth based on rack density trends (currently doubling every 3-4 years). Keep branch distribution modular: use busway or overhead distribution that can be reconfigured as rack layouts change. Plan for liquid cooling even if you're starting with air — retrofitting infrastructure later is expensive."

########################################
# FINISH
########################################

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ AI INFRASTRUCTURE MONEY PAGES COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📄 New URLs saved to: $SITEMAP_NOTE"
echo "🔄 Run ./generate-sitemap-failsafe.sh to regenerate sitemap"
echo ""
echo "Next steps:"
echo "  1. Review pages for content accuracy"
echo "  2. git add *.html"
echo "  3. git commit -m 'Add: AI infrastructure money pages ($DATE)'"
echo "  4. Regenerate sitemap"
echo ""
