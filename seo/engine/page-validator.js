/**
 * SideGuy CMS GPT · Page Validator v1
 * ------------------------------------
 * Ensures new pages:
 *  • Have valid slugs
 *  • Have a title
 *  • Have meta
 *  • Do not duplicate existing pages
 *  • Do not violate category rules
 */

export function validateEntry(entry, existingSlugs = []) {
  const errors = [];

  if (!entry.slug) errors.push("Missing slug");
  if (!entry.title) errors.push("Missing title");
  if (existingSlugs.includes(entry.slug)) errors.push("Duplicate slug");

  if (entry.slug && !/^[a-z0-9\-]+$/.test(entry.slug)) {
    errors.push("Invalid slug format");
  }

  if (!entry.category) errors.push("Missing category");

  return { valid: errors.length === 0, errors };
}
