/**
 * SideGuy CMS GPT · Auto Expander v1
 *
 * This module scans your repo, finds categories that are growing,
 * and automatically expands the manifest suggestions.
 *
 * In v1, it:
 *  - Reads existing slugs
 *  - Identifies "clusters" by prefix
 *  - Suggests new page slugs automatically
 *  - Writes them to /suggestions/ for the operator (you, Peege)
 *
 * Future versions:
 *  - Direct GPT integration to auto-generate pages
 *  - Auto-create industry verticals
 *  - Auto create long-tail problem pages
 */

import fs from 'fs';
import path from 'path';

export function autoExpand() {
  const pagesDir = path.join(process.cwd(), 'pages');
  const suggestionsDir = path.join(process.cwd(), 'suggestions');

  if (!fs.existsSync(suggestionsDir)) {
    fs.mkdirSync(suggestionsDir);
  }

  const files = fs.readdirSync(pagesDir);
  const clusters = {};

  // Group slugs by prefix
  files.forEach(file => {
    if (!file.endsWith('.html')) return;

    const slug = file.replace('.html', '');
    const prefix = slug.split('-').slice(0, 2).join('-');

    clusters[prefix] = clusters[prefix] || [];
    clusters[prefix].push(slug);
  });

  // Create suggestions for clusters with 3+ related pages
  const suggestions = [];

  for (const prefix in clusters) {
    if (clusters[prefix].length < 3) continue;

    const example = clusters[prefix][0];
    const base = example.split('-').slice(0, 2).join('-');

    const newSlug = `${base}-services-san-diego`;
    const newTitle = `${base.replace('-', ' ').toUpperCase()} Services San Diego`;
    const newDesc = `Explore all ${base.replace('-', ' ')}-related services in San Diego.`;

    suggestions.push({
      slug: newSlug,
      title: newTitle,
      metaDescription: newDesc,
      category: "auto"
    });
  }

  // Write suggestions out
  fs.writeFileSync(
    path.join(suggestionsDir, "auto-suggestions.json"),
    JSON.stringify(suggestions, null, 2)
  );

  console.log("Auto-expander generated:", suggestions.length, "new suggestions 🚀");
}
