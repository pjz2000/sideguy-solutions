/* 
  SideGuy Auto SEO Engine
  Version: 1.0
  Author: PJ + ChatGPT
  Generates fully styled SEO pages automatically from filename.
*/

// ------ Helper: Convert filename into readable text ------
function filenameToTitle(filename) {
  let name = filename.replace(".html", "");
  name = name.replace(/-/g, " ");
  name = name.replace(/\b\w/g, (l) => l.toUpperCase());
  return name;
}

// ------ Auto-generate core content ------
const filename = window.location.pathname.split("/").pop();
const pageTitle = filenameToTitle(filename);

// SEO title
document.title = `${pageTitle} | SideGuy Solutions`;

// ------ Build Page Layout ------
document.body.innerHTML = `
<style>
  :root {
    --bg-soft: #ecf7ff;
    --bg-card: #ffffff;
    --bg-hero: #f5fbff;
    --text-main: #020617;
    --text-soft: #475569;
    --accent: #00f18f;
    --accent-blue: #0f172a;
    --shadow-soft: 0 18px 45px rgba(15,23,42,0.1);
    --radius-lg: 32px;
    font-family: -apple-system, Inter, sans-serif;
  }
  body {
    margin: 0;
    padding: 0;
    background: radial-gradient(circle at top left, #e0f4ff 0, #f8fbff 40%, #edf5ff 100%);
    -webkit-font-smoothing: antialiased;
    color: var(--text-main);
  }
  .page-shell {
    max-width: 900px;
    margin: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 30px;
  }
  /* HEADER */
  .sg-header {
    display: flex; justify-content: space-between; align-items: center;
  }
  .sg-brand {
    display: flex; align-items: center; gap: 12px;
  }
  .brand-pill {
    width: 20px; height: 20px; border-radius: 999px;
    background: radial-gradient(circle at 30% 30%, #bfffdf 0, #00e676 30%, #00c853 60%, #008f3f 100%);
    box-shadow: 0 0 18px rgba(34,197,94,0.8);
  }
  .brand-lines { display: flex; flex-direction: column; line-height: 1.1; }
  .brand-top { font-size: 11px; letter-spacing: 0.12em; color: #64748b; }
  .brand-main { font-size: 22px; font-weight: 800; letter-spacing: 0.08em; }
  .sg-updated {
    background: rgba(255,255,255,0.8);
    padding: 10px 16px; border-radius: 999px;
    font-size: 12px; color: #475569;
    border: 1px solid rgba(148,163,184,0.35);
    backdrop-filter: blur(12px);
    display: flex; align-items: center; gap: 8px;
  }
  .sg-updated-dot {
    width: 8px; height: 8px; border-radius: 999px;
    background: #22c55e; box-shadow: 0 0 6px rgba(34,197,94,1);
  }
  /* CARD */
  .content-card {
    background: #ffffff;
    border-radius: var(--radius-lg);
    padding: 32px;
    box-shadow: var(--shadow-soft);
    border: 1px solid rgba(148,163,184,0.25);
  }
  h1 { font-size: 30px; font-weight: 800; margin-bottom: 12px; }
  p { font-size: 15px; color: #475569; margin-bottom: 12px; }
  ul { margin-left: 20px; margin-bottom: 20px; color: #475569; }
  li { margin-bottom: 8px; }
  .btn-home {
    display: inline-block; margin-top: 24px;
    padding: 10px 16px; background: #22c55e;
    border-radius: 999px; text-decoration: none;
    color: #022c22; font-weight: 600;
  }
  /* FOOTER */
  .sg-footer {
    margin-top: 10px; padding: 14px 18px;
    border-radius: 22px; background: rgba(15,23,42,0.98);
    color: #e5e7eb; font-size: 12px;
    display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
  }
  /* ORB */
  .pj-orb {
    position: fixed; right: 18px; bottom: 18px;
    background: #020617; color: #f9fafb;
    border-radius: 32px; padding: 12px 16px;
    display: flex; align-items: center; gap: 10px;
    border: 1px solid rgba(148,163,184,0.7);
    box-shadow: 0 20px 50px rgba(15,23,42,0.85);
  }
  .pj-orb-avatar {
    background: radial-gradient(circle, #a7f3d0 0, #22c55e 60%, #16a34a 100%);
    width: 32px; height: 32px; border-radius: 999px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 14px; color: #022c22;
    box-shadow: 0 0 12px rgba(34,197,94,0.9);
  }
  .pj-orb-text-main { font-size: 12px; font-weight: 600; }
  .pj-orb-text-sub { font-size: 11px; color: #9ca3af; }
</style>

<div class="page-shell">

  <!-- HEADER -->
  <header class="sg-header">
    <div class="sg-brand">
      <div class="brand-pill"></div>
      <div class="brand-lines">
        <div class="brand-top">SIDEGUY SOLUTIONS</div>
        <div class="brand-main">SideGuy Solutions</div>
      </div>
    </div>
    <div class="sg-updated">
      <div class="sg-updated-dot"></div>
      Updated: ${new Date().toLocaleDateString()}
    </div>
  </header>

  <!-- CONTENT -->
  <div class="content-card">
    <h1>${pageTitle}</h1>

    <p>
      SideGuy Solutions helps San Diego operators upgrade their payments,
      workflows, automations, and business tools. This page covers
      <strong>${pageTitle}</strong> — built clean, local, and tuned for real operators.
    </p>

    <ul>
      <li>Instant-settlement payments (0.4 sec)</li>
      <li>Clean dashboards instead of clutter</li>
      <li>Lower fees than Stripe & PayPal</li>
      <li>Local support from PJ</li>
    </ul>

    <a class="btn-home" href="index.html">← Back to Home</a>
  </div>

  <!-- FOOTER -->
  <footer class="sg-footer">
    Built for San Diego & North County operators — instant Solana payments · Local support from PJ
  </footer>

</div>

<!-- ORB -->
<div class="pj-orb">
  <div class="pj-orb-avatar">PJ</div>
  <div>
    <div class="pj-orb-text-main">Text PJ · 0.4 sec payments</div>
    <div class="pj-orb-text-sub">Send volume for exact savings</div>
  </div>
</div>
`;
