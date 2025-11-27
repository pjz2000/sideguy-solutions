/* 

  SideGuy Engine v1.0

  Auto-builds homepage service cards + future 50–100 SEO pages.

  Author: PJ + ChatGPT

  Last Updated: 2025-11-27

*/



// 5 starter pages — you can expand to 500 later

const sideguyPages = [

  {

    title: "Software Development San Diego",

    slug: "/seo-pages/software-development-san-diego.html",

    description: "Custom apps, automation, dashboards, clean builds."

  },

  {

    title: "Custom Software Development",

    slug: "/seo-pages/custom-software-development-san-diego.html",

    description: "Internal tools, workflows, CRMs, business systems."

  },

  {

    title: "App Development San Diego",

    slug: "/seo-pages/app-development-san-diego.html",

    description: "iOS, Android, PWA, browser apps, fast delivery."

  },

  {

    title: "AI Automation & Workflows",

    slug: "/seo-pages/artificial-intelligence-san-diego.html",

    description: "AI agents, automations, data pipelines, integrations."

  },

  {

    title: "SideGuy Payments (.4s Solana)",

    slug: "/payments.html",

    description: "Instant payouts, lower fees, Solana-native business rails."

  }

];



// Build function — populates the homepage grid

function buildSEOGrid() {

  const grid = document.getElementById("seo-grid");

  if (!grid) return;



  sideguyPages.forEach(page => {

    const card = document.createElement("div");

    card.className = "seo-card";

    card.innerHTML = `

      <a href="${page.slug}">

        <h3>${page.title}</h3>

        <p>${page.description}</p>

      </a>

    `;

    grid.appendChild(card);

  });

}



// Run builder

buildSEOGrid();
