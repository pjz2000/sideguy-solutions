// --------- TRENDING MOCK DATA ----------
const TREND_TOPICS = [
  "Solana yield to pay",
  "North County coastal concierge",
  "AI side hustles for 2025",
  "DFS promos in California",
  "Ethereum L2 gas savings",
  "Encinitas sunset sessions",
  "Stablecoin cash flow ideas",
  "Web3 ticketing experiments",
  "Solana Beach remote work",
  "Automating errands with AI",
  "Pacific ocean live cams",
  "Yield-backed subscriptions",
  "Coastal delivery & transport",
  "DeFi for real-world bills"
];

function pickRandomUnique(arr, count) {
  const copy = [...arr];
  const picked = [];
  while (copy.length && picked.length < count) {
    const idx = Math.floor(Math.random() * copy.length);
    picked.push(copy.splice(idx, 1)[0]);
  }
  return picked;
}

function renderTrends() {
  const list = document.getElementById("trend-list");
  if (!list) return;
  const topics = pickRandomUnique(TREND_TOPICS, 7);
  list.innerHTML = topics
    .map((t) => `<li class="trend-pill">#${t}</li>`)
    .join("");
}

// --------- SPORTS EDGE MOCK DATA ----------
const SPORTS_EDGES = [
  {
    league: "NBA",
    matchup: "Phoenix Suns vs Dallas Mavericks",
    context: "Regular Season • West Coast window",
    market: "Player Points + Rebounds + Assists",
    pick: "Dereck Lively II — Over 14.5 PRA",
    oddsMain: "+112",
    oddsAlt: "+136",
    liq: "$27 (example size)",
    disclaimer:
      "Educational only — not betting advice. Edges change fast and promos matter more than hot takes."
  },
  {
    league: "NFL",
    matchup: "San Francisco 49ers vs Seattle Seahawks",
    context: "Divisional tilt • Prime-time style game",
    market: "Rushing + Receiving Yards",
    pick: "Versatile RB Over combo line",
    oddsMain: "+104",
    oddsAlt: "+128",
    liq: "$31 (example size)",
    disclaimer:
      "Promotional money and disciplined staking usually matter more than any one angle."
  },
  {
    league: "MLB",
    matchup: "Los Angeles Dodgers vs San Diego Padres",
    context: "Night game • Pitcher-friendly park adjustment",
    market: "Total Bases",
    pick: "Contact hitter Over 1.5 TB",
    oddsMain: "+120",
    oddsAlt: "+148",
    liq: "$24 (example size)",
    disclaimer:
      "Use as a framework for how to think about edges, not as a ticket to hammer blindly."
  }
];

function renderSportsEdge() {
  const container = document.getElementById("sports-edge-body");
  if (!container) return;

  const edge = SPORTS_EDGES[Math.floor(Math.random() * SPORTS_EDGES.length)];

  container.innerHTML = `
    <div class="sports-main">
      <div class="sports-label">TODAY'S EDGE · ${edge.league}</div>
      <div class="sports-matchup">${edge.matchup}</div>
      <div class="sports-meta">${edge.context}</div>
      <div class="sports-line"><strong>${edge.market}</strong></div>
      <div class="sports-line">${edge.pick}</div>
      <div class="sports-odds">
        <span>Headline odds: ${edge.oddsMain}</span>
        <span>Alt ladder: ${edge.oddsAlt}</span>
        <span>Liq idea: ${edge.liq}</span>
      </div>
      <div class="sports-note">${edge.disclaimer}</div>
    </div>
    <div class="sports-side">
      <strong>How PJ thinks about this stuff:</strong><br/>
      Build around promos, edges, and your real life — not chasing every slate.<br/><br/>
      If you're in North County and curious about turning DFS and promos into a
      more disciplined system (instead of chaos), PJ can help you sketch it,
      test it small, and keep it fun.
    </div>
  `;
}

// --------- VERSION TIMESTAMP ----------
function updateVersionStamp() {
  const el = document.getElementById("version-info");
  if (!el) return;
  const now = new Date().toLocaleString("en-US", {
    timeZone: "America/Los_Angeles",
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true
  });
  el.textContent = `Version 4.5-oceanos-reactor • Updated ${now} PST`;
}

// --------- PORTAL REACTOR / WAVE BOOST ----------
function triggerPortalReactor() {
  // Big surge
  targetWaveAmp = 1.7;
  document.body.classList.add("portal-flash", "portal-ripple");

  // Remove flags after animation
  setTimeout(() => {
    targetWaveAmp = 1.05;
    document.body.classList.remove("portal-flash");
  }, 620);

  setTimeout(() => {
    document.body.classList.remove("portal-ripple");
  }, 1500);
}

function boostWaves() {
  triggerPortalReactor();
}

// --------- INIT ----------
document.addEventListener("DOMContentLoaded", () => {
  renderTrends();
  renderSportsEdge();
  updateVersionStamp();
  initOcean(); // from ocean.js

  const summonBtn = document.getElementById("summonPJBubble");
  if (summonBtn) {
    summonBtn.addEventListener("click", () => {
      boostWaves();
      // mailto still fires naturally
    });
  }

  const portalOrb = document.getElementById("portalOrb");
  if (portalOrb) {
    portalOrb.addEventListener("click", (e) => {
      e.preventDefault(); // just animation, no nav
      boostWaves();
    });
  }
});
