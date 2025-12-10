// SIDEGUY CMS GPT — Auto Topic Generator v1
// Future AI expansion component. Right now it only seeds top topics.

export function generateTopicIdeas(existingSlugs = []) {
  const seeds = [
    "ai-small-business-automation-san-diego",
    "solana-merchant-processing",
    "lower-credit-card-fees-2025",
    "mobile-payment-processing-san-diego",
    "emergency-plumber-san-diego",
    "hvac-installation-san-diego",
    "web-app-developer-san-diego",
  ];

  return seeds.filter(slug => !existingSlugs.includes(slug));
}
