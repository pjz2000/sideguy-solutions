/**
 * SideGuy CMS GPT · Category Brain v1
 * ------------------------------------
 * This module decides what category a new page belongs to
 * based on URL, title, description, or keywords.
 *
 * Later versions can plug into GPT for “smart classification,”
 * but v1 is deterministic, fast, safe, and stable.
 */

const CategoryBrain = {
  
  classify(entry) {
    const slug = (entry.slug || "").toLowerCase();
    const title = (entry.title || "").toLowerCase();
    const desc = (entry.metaDescription || "").toLowerCase();

    // Combined content for scanning
    const content = slug + " " + title + " " + desc;

    // --- PAYMENT CATEGORY -----------------------------------
    if (
      content.includes("payment") ||
      content.includes("processing") ||
      content.includes("merchant") ||
      content.includes("settlement") ||
      content.includes("solana") ||
      content.includes("credit-card") ||
      content.includes("pos")
    ) {
      return "payments";
    }

    // --- HOME SERVICES --------------------------------------
    if (
      content.includes("repair") ||
      content.includes("plumber") ||
      content.includes("leak") ||
      content.includes("ac") ||
      content.includes("hvac") ||
      content.includes("heater") ||
      content.includes("roof") ||
      content.includes("electric") ||
      content.includes("contractor") ||
      content.includes("landscap") ||
      content.includes("pest") ||
      content.includes("foundation")
    ) {
      return "home-services";
    }

    // --- AI / AUTOMATION ------------------------------------
    if (
      content.includes("ai") ||
      content.includes("automation") ||
      content.includes("software") ||
      content.includes("app-development") ||
      content.includes("integration") ||
      content.includes("cloud") ||
      content.includes("it")
    ) {
      return "automation";
    }

    // --- SIDEGUY IDENTITY / PLATFORM --------------------------------
    if (
      content.includes("sideguy") ||
      content.includes("operator") ||
      content.includes("command") ||
      content.includes("network") ||
      content.includes("vision") ||
      content.includes("mission") ||
      content.includes("gallery")
    ) {
      return "platform";
    }

    // --- PROBLEM / TROUBLESHOOTING -----------------------------------
    if (
      content.includes("why") ||
      content.includes("how") ||
      content.includes("not working") ||
      content.includes("won't") ||
      content.includes("wont") ||
      content.includes("fix") ||
      content.includes("problem")
    ) {
      return "problems";
    }

    // --- DEFAULT CATEGORY ---------------------------------------------
    return "misc";
  }
};

module.exports = CategoryBrain;
