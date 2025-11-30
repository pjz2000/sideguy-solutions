/* 
  SideGuy Solutions · Smart Router v1
  Compatibility Mode — fixes uppercase, spaces, dashes, .html issues
  Author: PJ + ChatGPT
*/

(function() {
  // Get the requested path
  const rawPath = window.location.pathname;

  // If visiting root, do nothing (homepage)
  if (rawPath === "/" || rawPath === "/index.html") return;

  // Normalize the path to match SideGuy rules
  let slug = rawPath
    .toLowerCase()
    .replace(/_/g, "-")        // underscores → hyphens
    .replace(/\s+/g, "-")      // spaces → hyphens
    .replace(/---+/g, "-")     // collapse triple hyphens
    .replace(/[^a-z0-9\-\.]/g, "") // remove weird characters
    .trim();

  // Ensure .html extension exists
  if (!slug.endsWith(".html")) {
    slug = slug.replace(/\/$/, "") + ".html";
  }

  // Remove leading slash
  slug = slug.replace(/^\//, "");

  // Build final target
  const finalUrl = "/" + slug;

  // If it's already correct, stop
  if (finalUrl === rawPath) return;

  // Redirect to normalized file
  window.location.replace(finalUrl);
})();
