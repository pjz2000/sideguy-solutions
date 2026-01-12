const fs = require('fs');

const path = require('path');



const ROOT = '.';

const DOMAIN = 'https://sideguy.solutions';

const EXCLUDED_DIRS = new Set([
  '.git',
  'node_modules',
  'tools',
  'templates',
  'stored-bashes',
  'seo__DISABLED',
  'auto-builder__DISABLED',
  'test',
  'site',
]);

const EXCLUDED_FILE_BASENAMES = new Set([
  '404.html',
  '__tmp__-hub.html',
  '-hub.html',
  '<!DOCTYPE html>.html',
  '_template.html',
  'template.html',
]);



// Escape bad XML characters

function escapeXML(str) {

  return str

    .replace(/&/g, '&amp;')

    .replace(/</g, '&lt;')

    .replace(/>/g, '&gt;')

    .replace(/"/g, '&quot;')

    .replace(/'/g, '&apos;');

}



function isBackupDirName(dirName) {

  const lower = dirName.toLowerCase();

  return lower.startsWith('backup') || lower.startsWith('backups');

}



function shouldIncludeFile(relPathPosix) {

  const base = path.posix.basename(relPathPosix);



  if (!base.endsWith('.html')) return false;

  if (EXCLUDED_FILE_BASENAMES.has(base)) return false;



  if (base.startsWith('.')) return false;

  if (base.includes(' ') || base.includes('?')) return false;



  if (base.includes('.backup.')) return false;

  if (base.endsWith('.tmp')) return false;



  if (base.startsWith('template-') || base.startsWith('template_') || base === 'seo-template.html') {

    return false;

  }

  if (base.includes('template') && base !== 'stripe-fees-calculator.html') {

    return false;

  }



  const lower = relPathPosix.toLowerCase();

  if (lower.includes('/_backups/') || lower.includes('/_layout_backups/') || lower.includes('/_quarantine_backups/')) {

    return false;

  }

  if (lower.includes('/backups/') || lower.includes('/backup_pages/') || lower.includes('/.sideguy-backups/')) {

    return false;

  }

  if (lower.includes('/backups_') || lower.includes('/backup_') || lower.includes('/backup-') || lower.includes('/backups-')) {

    return false;

  }

  if (lower.startsWith('seo-reserve/') || lower.includes('/seo-reserve/')) {

    return false;

  }



  return true;

}



function walk(dirAbs, relDirPosix) {

  let results = [];

  const entries = fs.readdirSync(dirAbs, { withFileTypes: true });

  for (const entry of entries) {

    const entryAbs = path.join(dirAbs, entry.name);

    const entryRelPosix = relDirPosix ? `${relDirPosix}/${entry.name}` : entry.name;



    if (entry.isDirectory()) {

      if (EXCLUDED_DIRS.has(entry.name)) continue;

      if (entry.name.startsWith('.')) continue;

      if (entry.name.startsWith('_')) continue;

      if (isBackupDirName(entry.name)) continue;

      results = results.concat(walk(entryAbs, entryRelPosix));

      continue;

    }



    if (!entry.isFile()) continue;



    const relPosix = entryRelPosix.split(path.sep).join('/');

    if (shouldIncludeFile(relPosix)) results.push(relPosix);

  }



  return results;

}



const pages = walk(path.resolve(ROOT), '');



let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;

xml += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;



pages.forEach(p => {

  xml += `  <url><loc>${escapeXML(`${DOMAIN}/${p}`)}</loc></url>\n`;

});



xml += `</urlset>`;



fs.writeFileSync('sitemap.xml', xml);



console.log(`Generated sitemap with ${pages.length} valid pages.`);