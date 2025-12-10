// SIDEGUY CMS GPT — SEO CATEGORY MATRIX v1
// Defines all major clusters so auto-builder + auto-expander
// know where to put new pages AND what to generate next.

export const seoCategories = {
  payments: {
    folder: "payments/pages",
    keywords: ["processing", "credit card", "merchant", "solana", "rates"],
    priority: 10
  },

  problems: {
    folder: "problems/pages",
    keywords: ["fix", "repair", "why", "not working", "leak", "broken"],
    priority: 9
  },

  software: {
    folder: "software/pages",
    keywords: ["software", "custom", "app", "automation"],
    priority: 8
  },

  local: {
    folder: "local/pages",
    keywords: ["san diego", "encinitas", "carlsbad", "del mar"],
    priority: 7
  },

  tickets: {
    folder: "tickets/pages",
    keywords: ["tickets", "concert", "events"],
    priority: 5
  }
};
