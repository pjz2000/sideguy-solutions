// SIDEGUY CMS GPT — SEO ROUTER v1

import { seoCategories } from "./seo-categories.js";

export function routeSEO(slug) {
  const clean = slug.toLowerCase();

  for (const key in seoCategories) {
    const cat = seoCategories[key];

    for (const kw of cat.keywords) {
      if (clean.includes(kw)) {
        return `${cat.folder}/${clean}.html`;
      }
    }
  }

  // Fallback for unknown
  return `misc/${clean}.html`;
}
