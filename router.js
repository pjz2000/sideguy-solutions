/**
 * SideGuy CMS GPT – Router v1
 * ---------------------------------------------------
 * Maps a page's category → the correct directory path.
 * Auto-builder uses this before writing files.
 *
 * Example:
 *   category: "payments" → /payments/page-slug.html
 *   category: "problems" → /problems/page-slug.html
 *   category: "services" → /services/page-slug.html
 *   category: "ai"       → /ai/page-slug.html
 *
 * This lets the website grow into thousands of pages
 * while staying clean, consistent, and organized.
 * ---------------------------------------------------
 */

function routePath(category, slug) {
  const cleanSlug = slug.replace(/[^a-z0-9\-]/gi, "").toLowerCase();

  switch (category) {
    case "payments":
      return `payments/${cleanSlug}.html`;

    case "processing":
      return `payments/${cleanSlug}.html`;

    case "problems":
      return `problems/${cleanSlug}.html`;

    case "services":
      return `services/${cleanSlug}.html`;

    case "contractors":
      return `services/${cleanSlug}.html`;

    case "ai":
      return `ai/${cleanSlug}.html`;

    case "automation":
      return `ai/${cleanSlug}.html`;

    case "seo":
      return `seo/${cleanSlug}.html`;

    case "energy":
      return `energy/${cleanSlug}.html`;

    case "tickets":
      return `tickets/${cleanSlug}.html`;

    // fallback — catch all
    default:
      return `misc/${cleanSlug}.html`;
  }
}

module.exports = { routePath };
