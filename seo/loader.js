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
    <div style="width:60px;height:60px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #4affdb, #00c896 70%);box-shadow:0 0 20px #00ffcc,0 0 40px #00ffcc99,0 0 60px #00ffcc55;margin-bottom:25px;"></div>
    <h1>${page.h1}</h1>
    <p>${page.intro}</p>
    <ul>${page.bullets.map(b=>`<li>• ${b}</li>`).join("")}</ul>
    <h3>Related Pages</h3>
    <ul>${page.relatedSlugs.map(s=>`<li><a href="/seo-pages/${s}.html">${s.replace(/-/g," ")}</a></li>`).join("")}</ul>
    <p style="opacity:.7;">Last updated: ${new Date().toLocaleString("en-US",{timeZone:"America/Los_Angeles"})}</p>
    <a href="/" style="display:inline-block;margin-top:30px;padding:10px 20px;background:#00ffcc;border-radius:12px;text-decoration:none;color:#000;">← Return Home</a>
  `;
});
