const fs = require('fs');
const path = require('path');

const ROOT = '.';
const DOMAIN = 'https://sideguysolutions.com';

// Directories excluded from sitemap (mirrors robots.txt Disallow rules + non-public dirs)
const EXCLUDED_DIRS = new Set([
  'backups', 'docs', 'site', 'public', 'seo-reserve', '.github', 'signals', 'data',
  // Internal / tooling dirs
  '.git', '.sideguy-backups', '_BACKUPS', '_layout_backups', '_quarantine_backups',
  '_preview', '_autogen_audit', '__pycache__', 'node_modules',
  'stash', 'test', 'temp', 'tools', 'stored-bashes',
  'crawl-sitemaps', 'future-build', 'sitemaps',
]);

// Additional pattern-based directory exclusions
function isExcludedDir(name) {
  if (EXCLUDED_DIRS.has(name)) return true;
  if (name.startsWith('.')) return true;
  if (name.startsWith('_')) return true;
  if (/backup/i.test(name)) return true;   // backup, backups, backup_pages, backups_20251230...
  if (/archive/i.test(name)) return true;
  if (/quarantine/i.test(name)) return true;
  return false;
}

// Escape bad XML characters
function escapeXML(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);

  list.forEach(file => {
    const full = path.join(dir, file);
    const stat = fs.statSync(full);

    if (stat && stat.isDirectory()) {
      // Skip excluded directories
      if (isExcludedDir(file)) return;
      results = results.concat(walk(full));
    } else {
      if (
        full.endsWith('.html') &&
        !full.includes('404.html') &&
        !file.startsWith('.') &&
        !file.includes(' ') &&
        !file.includes('?')
      ) {
        results.push(full.replace('./', ''));
      }
    }
  });

  return results;
}

const pages = walk(ROOT);

let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
xml += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;

pages.forEach(p => {
  xml += `  <url>\n`;
  xml += `    <loc>${escapeXML(`${DOMAIN}/${p}`)}</loc>\n`;
  xml += `    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>\n`;
  xml += `    <changefreq>monthly</changefreq>\n`;
  xml += `    <priority>0.8</priority>\n`;
  xml += `  </url>\n`;
});

xml += `</urlset>`;

fs.writeFileSync('sitemap.xml', xml);
console.log(`✅ sitemap.xml written — ${pages.length} URLs`);



console.log(`Generated sitemap with ${pages.length} valid pages.`);