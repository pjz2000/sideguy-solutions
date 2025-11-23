// SideGuy SEO Engine — Perfect Match Version

// Matches EXACTLY the filenames in /seo-pages/



const seoPages = [

  "ai-automation-san-diego",

  "ai-consulting-san-diego",

  "api-integration-san-diego",

  "app-consulting-san-diego",

  "app-development-san-diego",

  "automation-consulting-san-diego",

  "automation-software-san-diego",

  "booking-systems-san-diego",

  "business-automation-san-diego",

  "business-systems-san-diego",

  "carlsbad-software-development",

  "cloud-software-san-diego",

  "custom-crm-san-diego",

  "custom-software-development-san-diego",

  "database-design-san-diego",

  "digital-transformation-san-diego",

  "ecommerce-development-san-diego",

  "enterprise-software-san-diego",

  "inventory-software-san-diego",

  "legacy-software-upgrades-san-diego",

  "machine-learning-development-san-diego",

  "membership-software-san-diego",

  "mobile-app-development-san-diego",

  "near-me-custom-software",

  "north-county-app-development",

  "north-county-software",

  "saas-development-san-diego",

  "san-diego-software-company",

  "san-diego-software-consulting",

  "software-development-san-diego",

  "software-maintenance-san-diego",

  "solana-beach-software",

  "solana-developers-san-diego",

  "startup-software-san-diego",

  "tech-consulting-san-diego",

  "web-app-development-san-diego",

  "workflow-automation-san-diego"

];



window.onload = () => {

  const list = document.getElementById("seoList");



  seoPages.forEach((slug) => {

    const li = document.createElement("li");

    li.innerHTML = `<a href="seo-pages/${slug}.html">${slug.replace(/-/g, " ")}</a>`;

    list.appendChild(li);

  });

};
};

