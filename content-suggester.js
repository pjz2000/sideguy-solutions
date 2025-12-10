/**
 * SIDEGUY CMS GPT — Content Suggester v1
 * Auto-suggests new pages based on patterns + verticals.
 */

export function suggestContent(existingPages) {
  const suggestions = [];

  const patterns = [
    "best-{{category}}-san-diego",
    "{{category}}-pricing-san-diego",
    "{{category}}-near-me-san-diego",
    "emergency-{{category}}-san-diego",
  ];

  const categories = [
    "plumbing",
    "hvac",
    "electrical",
    "software-development",
    "ai-automation",
    "payment-processing",
    "solana-payments",
  ];

  for (const cat of categories) {
    for (const pattern of patterns) {
      const slug = pattern.replace("{{category}}", cat);
      if (!existingPages.includes(slug + ".html")) {
        suggestions.push({
          slug,
          title: slug.replace(/-/g, " ").toUpperCase(),
          category: cat,
        });
      }
    }
  }

  return suggestions;
}
