/* ================================
   SIDEGUY SOLUTIONS — script.js
   Version 2.1
   Author: PJ + Kromeon Dev Team
   ================================ */

/* ------------------------------
   1. VERSION TIMESTAMP
------------------------------ */
document.addEventListener("DOMContentLoaded", () => {
  const ts = document.getElementById("timestamp");
  if (ts) {
    ts.textContent = new Date().toLocaleString("en-US", {
      timeZone: "America/Los_Angeles",
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }
});


/* ------------------------------
   2. LIVE SOL/ETH/USDC TICKER
------------------------------ */

async function loadTicker() {
  const el = document.getElementById("ticker-content");
  if (!el) return;

  try {
    const res = await fetch(
      "https://api.coingecko.com/api/v3/simple/price?ids=solana,ethereum,usd-coin&vs_currencies=usd&include_24hr_change=true"
    );
    const d = await res.json();

    el.innerHTML = `
      SOL: $${d.solana.usd.toFixed(2)} (${d.solana.usd_24h_change.toFixed(2)}%) | 
      ETH: $${d.ethereum.usd.toFixed(2)} (${d.ethereum.usd_24h_change.toFixed(2)}%) | 
      USDC: $${d["usd-coin"].usd.toFixed(2)} (0.00%)
    `;
  } catch (err) {
    el.textContent = "SOL $185 | ETH $3450 | USDC $1.00";
  }
}

loadTicker();
setInterval(loadTicker, 15000);


/* ------------------------------
   3. RANDOMIZED SPORTS EDGE
------------------------------ */

const edges = [
  {
    emoji: "🏀",
    game: "Phoenix Suns vs Dallas Mavericks",
    line: "Dereck Lively II — Over 14.5 PRA",
    oddsA: "+112",
    oddsB: "+136",
    note: "North County Exclusive 🔒"
  },
  {
    emoji: "🏈",
    game: "49ers vs Seahawks",
    line: "Christian McCaffrey — Anytime TD",
    oddsA: "-110",
    oddsB: "+105",
    note: "Premium Edge Only"
  },
  {
    emoji: "⚾",
    game: "Dodgers vs Padres",
    line: "Mookie Betts — Over 1.5 Bases",
    oddsA: "+125",
    oddsB: "+140",
    note: "Local NL West Value"
  },
  {
    emoji: "🏒",
    game: "Rangers vs Avalanche",
    line: "Mikko Rantanen — Over 3.5 Shots",
    oddsA: "-120",
    oddsB: "+102",
    note: "Sharp Money Movement"
  }
];

function loadEdge() {
  const el = document.getElementById("edge-card");
  if (!el) return;

  const pick = edges[Math.floor(Math.random() * edges.length)];

  el.innerHTML = `
    <div class="edge-line">
      <h3>${pick.emoji} ${pick.game}</h3>
      <p>${pick.line}</p>
      <p><strong>${pick.oddsA}</strong> → <strong>${pick.oddsB}</strong></p>
      <p class="muted">${pick.note}</p>
    </div>
  `;
}

loadEdge();


/* ------------------------------
   4. SOLANA YIELD — MOCK LIVE
------------------------------ */

async function loadApy() {
  const box = document.getElementById("apy-box");
  if (!box) return;

  try {
    // Replace with real Helius / SolanaFM / Marinade API later
    const mockApy = (6 + Math.random() * 3).toFixed(2);

    box.innerHTML = `
      <strong>Current SOL Staking APY:</strong> ${mockApy}%<br>
      <span class="muted">Yield-to-Pay Ready</span>
    `;
  } catch {
    box.innerHTML = "Unable to load APY. Try again later.";
  }
}

loadApy();
setInterval(loadApy, 30000);


/* ------------------------------
   5. TRENDING TOPICS
------------------------------ */

async function loadTrends() {
  const el = document.getElementById("trendList");
  if (!el) return;

  try {
    const res = await fetch(
      "https://trends.google.com/trends/hottrends/visualize/internal/data/en-us"
    );
    const data = await res.json();

    const trends = data.slice(0, 10).map(t => t.title || t.name);
    el.innerHTML = trends.map(t => `<li>${t}</li>`).join("");
  } catch (err) {
    // fallback static
    el.innerHTML = `
      <li>AI Assistants</li>
      <li>Solana Yield</li>
      <li>DFS Promos</li>
      <li>NFL Props</li>
      <li>North County Weather</li>
    `;
  }
}

loadTrends();


/* ------------------------------
   6. NEWSLETTER → EMAIL PJ
------------------------------ */

document.getElementById("newsletterButton")?.addEventListener("click", () => {
  const email = document.getElementById("newsletterEmail").value.trim();
  const status = document.getElementById("newsletter-status");

  if (!email) {
    status.textContent = "Please enter a valid email.";
