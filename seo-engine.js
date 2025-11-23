// SideGuy SEO Engine v2

// Auto-links all SEO pages in /seo-pages/



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

  "custom-software-development-san-diego",

  "data-automation-san-diego",

  "fintech-software-san-diego",

  "mobile-app-development-san-diego",

  "north-county-san-diego-software",

  "software-development-san-diego",

  "solana-developers-san-diego",

  "web-app-development-san-diego"

  // Add more any time — website updates automatically

];



window.onload = () => {

  const list = document.getElementById("seoList");



  seoPages.forEach((slug) => {

    const li = document.createElement("li");

    li.innerHTML = `<a href="seo-pages/${slug}.html">${slug.replace(/-/g, " ")}</a>`;

    list.appendChild(li);

  });

};

