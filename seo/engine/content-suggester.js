/**
 * SideGuy CMS GPT · Content Suggester v1
 * --------------------------------------
 * Reads all slugs, detects patterns, proposes new pages:
 *  • city variants
 *  • service variants
 *  • question-based SEO (why / how / cost / near-me)
 *  • problem-based expansions
 */

import fs from "fs";
import path from "path";

export function suggestContent(pagesDir = "./pages") {
  const files = fs.readdirSync(pagesDir);
  const slugs = files.map(f => f.replace(".html", ""));

  const suggestions = new Set();

  for (const slug of slugs) {
    // Generate Q&A variants
    suggestions.add(`how-to-${slug}`);
    suggestions.add(`why-is-${slug}`);
    suggestions.add(`${slug}-cost`);
    suggestions.add(`${slug}-near-me`);

    // City variants
    const base = slug.replace(/-san-diego/g, "");
    suggestions.add(`${base}-san-diego`);
    suggestions.add(`${base}-carlsbad`);
    suggestions.add(`${base}-encinitas`);
    suggestions.add(`${base}-del-mar`);
  }

  return Array.from(suggestions);
}
