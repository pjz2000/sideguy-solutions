// ------------------------------------------------------------

// SideGuy SEO Auto-Page Loader v1.0

// Pure HTML auto-generation system

// ------------------------------------------------------------



// Wait until DOM is ready

document.addEventListener("DOMContentLoaded", async () => {

  // Find the slug from the HTML wrapper

  const container = document.querySelector("[data-seo-slug]");

  if (!container) return;



  const slug = container.getAttribute("data-seo-slug");



  // Load engine.json

  const res = await fetch("/seo/engine.json");

  const pages = await res.json();



  // Find the correct page by slug

  const page = pages.find((p) => p.slug === slug);



  if (!page) {

    container.innerHTML = `<h1>Page not found</h1><p>Peege hasn’t built this yet.</p>`;

    return;

  }



  // Inject HTML auto-generated content

  container.innerHTML = `

    <div style="

      width: 60px;

      height: 60px;

      border-radius: 50%;

      background: radial-gradient(circle at 30% 30%, #4affdb, #00c896 70%);

      box-shadow: 0 0 20px #00ffcc, 0 0 40px #00ffcc99, 0 0 60px #00ffcc55;

      margin-bottom: 25px;">

    </div>



    <h1 style="font-size: 2.3rem; margin-bottom: 18px;">

      ${page.h1}

    </h1>



    <p style="margin-bottom: 25px;">${page.intro}</p>



    <ul style="padding-left: 20px; margin-bottom: 30px;">

      ${page.bullets.map((b) => `<li style="margin-bottom: 8px;">• ${b}</li>`).join("")}

    </ul>



    <h3 style="margin-top: 40px;">Related Pages</h3>

    <ul style="padding-left: 18px;">

      ${page.relatedSlugs

        .map(

          (slug) => `

        <li>

          <a href="/seo-pages/${slug}.html" 

             style="color:#0070f3; text-decoration:none;">

             ${slug.replace(/-/g, " ")}

          </a>

        </li>`

        )

        .join("")}

    </ul>



    <p style="opacity: .7; margin-top: 40px; font-size: .9rem;">

      Last updated: ${new Date().toLocaleString("en-US", {

        timeZone: "America/Los_Angeles",

        month: "short",

        day: "numeric",

        year: "numeric",

        hour: "numeric",

        minute: "2-digit"

      })}

    </p>



    <a href="/" style="

      display:inline-block;

      margin-top:35px;

      padding:12px 22px;

      border-radius:12px;

      background:linear-gradient(135deg,#00ffcc,#00c896);

      color:#000;

      font-weight:600;

      text-decoration:none;

      box-shadow:0 0 12px #00ffcc88,0 0 24px #00ffcc66;">

      ← Return Home

    </a>

  `;

});
