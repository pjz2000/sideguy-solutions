// update-templates.js
// Auto-upgrade all HTML pages (except index/404/templates) to template-v304

const fs = require('fs');
const path = require('path');

const TEMPLATE_PATH = path.join(__dirname, 'templates', 'sideguy-universal-template.html');
const DOMAIN = 'https://sideguy.solutions';
const EXCLUDE_FILES = new Set(['index.html', '404.html']);

const templateRaw = fs.readFileSync(TEMPLATE_PATH, 'utf8');

function extractBetween(str, start, end) {
  const s = str.indexOf(start);
  const e = str.indexOf(end);
  if (s === -1 || e === -1 || e <= s) return null;
  return str.slice(s + start.length, e);
}

function upgradeFile(filePath) {
  const fileName = path.basename(filePath);
  if (EXCLUDE_FILES.has(fileName)) return;
  if (fileName.includes('.backup.') || fileName.endsWith('.tmp')) return;

  let html = fs.readFileSync(filePath, 'utf8');

  // 1) Get original <title>
  let titleMatch = html.match(/<title>([\s\S]*?)<\/title>/i);
  let pageTitle = titleMatch ? titleMatch[1].trim() : 'SideGuy Solutions';

  // 2) Get original meta description (if any)
  let metaMatch = html.match(
    /<meta[^>]+name=["']description["'][^>]*content=["']([^"']*)["'][^>]*>/i
  );
  let metaDescription = metaMatch
    ? metaMatch[1].trim()
    : `SideGuy Solutions · Help with ${pageTitle} in San Diego.`;

  // 3) Extract existing page content
  let content = null;

  // Prefer CONTENT_START/CONTENT_END if already present
  const contentMarker = extractBetween(
    html,
    '<!--CONTENT_START-->',
    '<!--CONTENT_END-->'
  );
  if (contentMarker) {
    content = contentMarker.trim();
  } else {
    // Fallback: everything inside <body>...</body>
    const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    content = bodyMatch ? bodyMatch[1].trim() : '<p>Page content coming soon.</p>';
  }

  // 4) Build new HTML from template
  const relPathPosix = path.relative(__dirname, filePath).split(path.sep).join('/');
  const canonicalUrl = `${DOMAIN}/${relPathPosix}`;

  let newHtml = templateRaw
    .replace(/{{PAGE_TITLE}}/g, pageTitle)
    .replace(/{{PAGE_HEADING}}/g, pageTitle)
    .replace(/{{PAGE_DESCRIPTION}}/g, metaDescription)
    .replace(/{{CANONICAL_URL}}/g, canonicalUrl)
    .replace('{{PAGE_CONTENT}}', content);

  fs.writeFileSync(filePath, newHtml, 'utf8');
  console.log('Upgraded:', filePath);
}

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      // Skip node_modules, .git, templates folders
      if (['node_modules', '.git', 'templates', 'tools', 'site'].includes(entry.name)) continue;
      if (entry.name.startsWith('.')) continue;
      if (entry.name.startsWith('_')) continue;
      if (entry.name.toLowerCase().startsWith('backup') || entry.name.toLowerCase().startsWith('backups')) continue;
      walk(fullPath);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      upgradeFile(fullPath);
    }
  }
}

console.log('Using template:', TEMPLATE_PATH);
walk(__dirname);
console.log('Done upgrading templates.');
