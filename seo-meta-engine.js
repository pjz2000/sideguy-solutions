/**
 * SIDEGUY CMS GPT — SEO Meta Engine v1
 * Generates meta title, description, bullets, intro from templates.
 * Dynamic SEO for every generated page.
 */

export function buildMeta(entry) {
  const { title, metaDescription, intro, bullets } = entry;

  const meta = {
    title: title || `SideGuy Solutions — ${entry.slug.replace(/-/g, " ")}`,
    description:
      metaDescription ||
      `SideGuy Solutions solves real problems in San Diego — fast. Learn about ${title}.`,
    intro:
      intro ||
      `SideGuy Solutions helps real operators fix issues fast — here is your guide to ${title}.`,
    bullets:
      bullets ||
      [
        "Instant answers",
        "Real human support (Text PJ)",
        "0.4 second payments rail",
      ],
  };

  return meta;
}
