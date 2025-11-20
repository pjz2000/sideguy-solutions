// -------------------------------------------

//  SideGuy SEO Engine v1

//  Each page auto-generates from this file.

// -------------------------------------------



const seoPages = [



  // 1. software-development-san-diego

  {

    slug: "software-development-san-diego",

    title: "Software Development San Diego | Custom Apps & Automation",

    metaDescription:

      "Looking for software development in San Diego? SideGuy Solutions builds custom apps, automations, and Web3 tools for local businesses.",

    h1: "Software Development in San Diego",

    intro:

      "SideGuy Solutions builds clean, modern software for San Diego founders, operators, and companies who want real results — not agency fluff.",

    bullets: [

      "Custom business software",

      "Web & mobile apps",

      "AI automation tools",

      "Solana & Web3 integrations",

      "Dashboards & internal tools"

    ],

    relatedSlugs: [

      "custom-software-development-san-diego",

      "app-development-san-diego",

      "web-development-san-diego"

    ]

  },



  // 2. custom-software-development-san-diego

  {

    slug: "custom-software-development-san-diego",

    title: "Custom Software Development San Diego | Local App Builders",

    metaDescription:

      "Custom software development in San Diego for startups and businesses. Local builds, fast communication, and real results.",

    h1: "Custom Software Development in San Diego",

    intro:

      "We build custom software for teams who need fast development, clean execution, and local support across San Diego and North County.",

    bullets: [

      "Custom platform development",

      "Process automation",

      "Mobile & web apps",

      "Database & backend systems",

      "Cloud + API integrations"

    ],

    relatedSlugs: [

      "software-development-san-diego",

      "app-development-san-diego",

      "mobile-app-development-san-diego"

    ]

  },



  // 3. software-company-san-diego

  {

    slug: "software-company-san-diego",

    title: "Software Company San Diego | SideGuy Solutions",

    metaDescription:

      "Looking for a software company in San Diego? SideGuy Solutions builds apps, automations, and Web3 tools for local businesses.",

    h1: "Software Company in San Diego",

    intro:

      "SideGuy Solutions is a modern software company serving San Diego startups, small businesses, and growth-stage teams.",

    bullets: [

      "Full-stack development",

      "App & automation builds",

      "Internal tools",

      "Technical architecture",

      "Long-term support"

    ],

    relatedSlugs: [

      "software-development-san-diego",

      "custom-software-development-san-diego",

      "web-development-san-diego"

    ]

  },



  // 4. app-development-san-diego

  {

    slug: "app-development-san-diego",

    title: "App Development San Diego | iOS & Android Apps",

    metaDescription:

      "App development in San Diego for iOS, Android, and web. Local builds for founders and businesses.",

    h1: "App Development in San Diego",

    intro:

      "We design and build modern apps for startups, founders, and companies across San Diego and North County.",

    bullets: [

      "iOS & Android apps",

      "Cross-platform builds",

      "Web apps",

      "Backend systems",

      "UI/UX design"

    ],

    relatedSlugs: [

      "mobile-app-development-san-diego",

      "web-development-san-diego",

      "software-development-san-diego"

    ]

  },



  // 5. mobile-app-development-san-diego

  {

    slug: "mobile-app-development-san-diego",

    title: "Mobile App Development San Diego | Local App Builders",

    metaDescription:

      "Mobile app development in San Diego for iPhone, Android, and cross-platform. Built locally with fast communication.",

    h1: "Mobile App Development in San Diego",

    intro:

      "We create mobile apps that look great, run fast, and scale — built locally for San Diego founders and businesses.",

    bullets: [

      "iPhone & Android apps",

      "Cross-platform frameworks",

      "Mobile UI/UX",

      "API integrations",

      "Full-stack support"

    ],

    relatedSlugs: [

      "app-development-san-diego",

      "software-development-san-diego",

      "custom-software-development-san-diego"

    ]

  }



];



// ------------------------------------------------

// Required exports for the Next.js dynamic route

// ------------------------------------------------



export function getAllSeoSlugs() {

  return seoPages.map((p) => p.slug);

}



export function getSeoPage(slug) {

  return seoPages.find((p) => p.slug === slug);

}

