document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector("[data-seo-slug]");
  if (!container) return;

  const slug = container.getAttribute("data-seo-slug");

  const res = await fetch("/seo/engine.json");
  const pages = await res.json();

  const page = pages.find((p) => p.slug === slug);

  if (!page) {
    container.innerHTML = "<h1>Page not found</h1>";
    return;
  }

  container.innerHTML = `
    <div style="max-width: 800px; margin: auto; padding: 40px;">

      <div style="
        width: 60px; height: 60px; border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #4affdb, #00c896 70%);
        box-shadow: 0 0 20px #00ffcc, 0 0 40px #00ffcc99;
        margin-bottom: 30px;">
      </div>

      <h1 style="margin-bottom: 16px;">${page.h1}</h1>

      <p style="margin-bottom: 28px; line-height: 1.6;">
        ${page.intro}
      </p>

      <ul style="margin-bottom: 32px; padding-left: 20px;">
        ${page.bullets.map(b => `<li style="margin-bottom: 8px;">• ${b}</li>`).join("")}
      </ul>

      <h3 style="margin-bottom: 12px;">Related Pages</h3>
      <ul style="padding-left: 18px; margin-bottom: 40px;">
        ${page.relatedSlugs
          .map(s => `<li><a href="/seo-pages/${s}.html">${s.replace(/-/g, " ")}</a></li>`)
          .join("")}
      </ul>

      <p style="opacity:.7; font-size:.9rem; margin-bottom: 30px;">
        Last updated: ${new Date().toLocaleString("en-US",{timeZone:"America/Los_Angeles"})}
      </p>

      <a href="/" style="
        display:inline-block; padding:12px 22px;
        border-radius:12px; background:#00ffcc;
        text-decoration:none; color:#000; font-weight:600;">
        ← Return Home
      </a>

    </div>
  `;
});
