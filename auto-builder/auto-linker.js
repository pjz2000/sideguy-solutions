/**
 * SideGuy CMS GPT — Auto Linker v1
 * -------------------------------------------------------
 * Scans generated pages and injects:
 *  - Related links by category
 *  - “Next problem” links
 *  - “Nearby services” links
 *  - Local SEO internal mesh
 * 
 * This makes every page a small “web” on its own,
 * increasing crawl depth, time-on-site, and ranking.
 */

import fs from 'fs';
import path from 'path';

const pagesDir = path.join(process.cwd(), 'pages');
const outputDir = path.join(process.cwd(), 'pages-linked');

// ensure folder exists
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

// load all pages
const pages = fs.readdirSync(pagesDir).filter(f => f.endsWith('.html'));

// helper: extract slug
const slug = file => file.replace('.html', '');

// classifier for linking logic
function getRelatedPages(currentSlug) {
  return pages
    .filter(p => p !== currentSlug + '.html')
    .filter(p => p.includes(currentSlug.split('-')[0])) // share a keyword
    .slice(0, 5); // limit to 5 links
}

// build new pages with injected links
for (const file of pages) {
  const filePath = path.join(pagesDir, file);
  let html = fs.readFileSync(filePath, 'utf8');

  const related = getRelatedPages(slug(file));

  const linksBlock = `
    <div class="related-links">
      <h3>Related SideGuy Pages</h3>
      <ul>
        ${related.map(r => `<li><a href="/pages/${r}">${slug(r)}</a></li>`).join('')}
      </ul>
    </div>
  `;

  const finalHtml = html.replace('</body>', `${linksBlock}</body>`);

  fs.writeFileSync(
    path.join(outputDir, file),
    finalHtml,
    'utf8'
  );
}

console.log(`Auto-Linker: Linked ${pages.length} pages → completed.`);
