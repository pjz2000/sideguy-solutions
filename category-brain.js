/**

 * SideGuy CMS GPT - Category Brain v1

 * --------------------------------------------------------

 * Decides what category a new page belongs to.

 * Uses:

 *   - URL slug

 *   - Title

 *   - Description

 *   - Keywords

 * This lets auto-builder plug into smart classification

 * so thousands of pages stay organized, fast, and scalable.

 */



function categoryBrain(entry) {

  const slug = entry.slug.toLowerCase();

  const title = entry.title.toLowerCase();

  const desc = entry.metaDescription.toLowerCase();

  const content = slug + " " + title + " " + desc;



  // PAYMENTS

  if (content.includes("payment") ||

      content.includes("processing") ||

      content.includes("merchant") ||

      content.includes("credit") ||

      content.includes("fees")) {

    return "payments";

  }



  // PROBLEMS (home repair, HVAC, plumbing, electrical)

  if (content.includes("repair") ||

      content.includes("fix") ||

      content.includes("not working") ||

      content.includes("leak") ||

      content.includes("ac") ||

      content.includes("heater") ||

      content.includes("water") ||

      content.includes("plumb") ||

      content.includes("elect")) {

    return "problems";

  }



  // AUTOMATION / AI

  if (content.includes("automation") ||

      content.includes("ai") ||

      content.includes("software") ||

      content.includes("development")) {

    return "automation";

  }



  // SERVICES / CONTRACTORS

  if (content.includes("landscaping") ||

      content.includes("roof") ||

      content.includes("hvac") ||

      content.includes("install") ||

      content.includes("contractor") ||

      content.includes("service")) {

    return "services";

  }



  // DEFAULT

  return "general";

}



module.exports = categoryBrain;

