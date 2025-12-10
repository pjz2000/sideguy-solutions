/**

 * SideGuy CMS GPT — Router V1

 * ----------------------------

 * Decides WHERE a page gets saved in the repo based on CATEGORY.

 * Auto-builder calls this before writing files.

 *

 * Example:

 *   category = "payments" → /payments/pages/slug.html

 *   category = "problems" → /problems/pages/slug.html

 *

 * This keeps the repo clean, scalable, and organized forever.

 */



function cleanSlug(slug) {

  return slug.replace(/[^a-z0-9\-]/gi, "").toLowerCase();

}



/**

 * ROUTER: map CATEGORY → DIRECTORY PATH

 */

function route(category, slug) {

  const safeSlug = cleanSlug(slug);



  switch (category) {

    case "payments":

      return `payments/pages/${safeSlug}.html`;



    case "processing":

      return `processing/pages/${safeSlug}.html`;



    case "problems":

      return `problems/pages/${safeSlug}.html`;



    case "contractors":

      return `contractors/pages/${safeSlug}.html`;



    case "ai":

      return `ai/pages/${safeSlug}.html`;



    case "services":

      return `services/pages/${safeSlug}.html`;



    case "tickets":

      return `tickets/pages/${safeSlug}.html`;



    case "energy":

      return `energy/pages/${safeSlug}.html`;



    case "seo":

      return `seo/pages/${safeSlug}.html`;



    default:

      // Fallback: place unknown categories in /misc

      return `misc/pages/${safeSlug}.html`;

  }

}



module.exports = { route };