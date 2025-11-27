// ------------------------------------------------------------

//  SideGuy SEO Engine v2.0

//  Next Perfect Build — Meme Efficient Edition

//  Auto-generates 50+ SEO pages with clean metadata + bullets

//  Timestamp auto-injected via JS

//  Author: PJ + ChatGPT

// ------------------------------------------------------------



export const seoPages = [

  // --------------------------------------------------------

  // TEMPLATE:

  // {

  //   slug: "your-slug-here",

  //   title: "Page Title | SideGuy Solutions",

  //   metaDescription: "Short SEO description here.",

  //   h1: "Main Page Heading",

  //   intro: "Clean intro paragraph.",

  //   bullets: ["Point A", "Point B", "Point C"],

  //   relatedSlugs: ["other-page", "another-page"]

  // }

  // --------------------------------------------------------



  // 1. software-development-san-diego

  {

    slug: "software-development-san-diego",

    title: "Software Development San Diego | Custom Apps & Automation",

    metaDescription:

      "Looking for software development in San Diego? SideGuy Solutions builds custom apps, automations, and Web3 tools for local businesses.",

    h1: "Software Development in San Diego",

    intro:

      "SideGuy Solutions builds clean, modern software for San Diego founders, operators, and teams who want results — fast.",

    bullets: [

      "Custom business software",

      "Web & mobile apps",

      "AI automation tools",

      "Solana & Web3 integrations",

      "Dashboards & internal tools"

    ],

    relatedSlugs: [

      "custom-software-development-san-diego",

      "app-development-san-diego"

    ]

  },



  // 2. custom-software-development-san-diego

  {

    slug: "custom-software-development-san-diego",

    title: "Custom Software Development San Diego | SideGuy Solutions",

    metaDescription:

      "Custom software development for San Diego businesses. Fast builds, clean UX, dashboards, automation, and Solana-powered tools.",

    h1: "Custom Software Development San Diego",

    intro:

      "We help San Diego companies build exactly what they need — no cookie-cutter templates, just clean custom tools.",

    bullets: [

      "Automated workflows",

      "Internal tools & dashboards",

      "Process acceleration",

      ".4 second Solana settlement optional",

      "API integrations"

    ],

    relatedSlugs: [

      "software-development-san-diego",

      "san-diego-ai-development"

    ]

  },



  // 3. app-development-san-diego

  {

    slug: "app-development-san-diego",

    title: "App Development San Diego | Mobile & Web Experts",

    metaDescription:

      "Web and mobile app development for San Diego startups and businesses. Clean designs, fast builds, and real support.",

    h1: "App Development San Diego",

    intro:

      "We build modern apps that look clean, feel premium, and perform fast — perfect for San Diego founders.",

    bullets: [

      "iOS & Android apps",

      "Web apps & dashboards",

      "AI-powered features",

      "Payments & subscriptions",

      "Real-time notifications"

    ],

    relatedSlugs: [

      "software-development-san-diego",

      "custom-software-development-san-diego"

    ]

  },



  // More pages auto-load below… (we will drop the next 47 after this)

];



// ------------------------------------------------------------

// Auto timestamp injection (for every SEO page footer)

// ------------------------------------------------------------

export function getTimestamp() {

  const now = new Date();

  return now.toLocaleString("en-US", {

    timeZone: "America/Los_Angeles",

    month: "short",

    day: "numeric",

    year: "numeric",

    hour: "numeric",

    minute: "2-digit"

  });

}

