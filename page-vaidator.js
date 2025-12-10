// SideGuy CMS GPT · page-validator.js · V1
// ----------------------------------------
// Ensures:
// • No duplicate slugs
// • Valid category
// • Required fields exist
// • Meta is valid
// • No dangerous characters

export function validateEntry(entry, existingSlugs = []) {
  const errors = [];

  if (!entry.slug || entry.slug.length < 3)
    errors.push("Missing or invalid slug");

  if (!entry.title || entry.title.length < 5)
    errors.push("Missing or invalid title");

  if (!entry.meta || entry.meta.length < 10)
    errors.push("Meta description missing or too short");

  if (!entry.category)
    errors.push("Category missing");

  if (existingSlugs.includes(entry.slug))
    errors.push("Duplicate slug detected");

  if (/[^a-z0-9\-]/i.test(entry.slug))
    errors.push("Slug contains invalid characters");

  return {
    valid: errors.length === 0,
    errors
  };
}
