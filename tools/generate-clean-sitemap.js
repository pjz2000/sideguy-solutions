#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const DOMAIN = 'https://sideguy.solutions';

const OUTPUT_INDEX = path.join(ROOT, 'sitemap-index.xml');
const OUTPUT_SITEMAP_PREFIX = path.join(ROOT, 'sitemap-clean');
const OUTPUT_STATS = path.join(ROOT, 'sitemap-clean-stats.json');

const MAX_URLS_PER_SITEMAP = 45000;

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

function isBackupDirName(dirName) {
  const lower = dirName.toLowerCase();
  // Catches: backups/, backup_pages/, backup_old_pages/, backups_2025..., etc.
  return lower.startsWith('backup') || lower.startsWith('backups');
}

const EXCLUDED_FILE_BASENAMES = new Set([
  '404.html',
  '__tmp__-hub.html',
  '-hub.html',
  '<!DOCTYPE html>.html',
  '_template.html',
  'template.html',
]);

function escapeXML(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function isoDateFromStat(stat) {
  // Keep it simple: sitemap supports YYYY-MM-DD.
  const date = new Date(stat.mtimeMs);
  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, '0');
  const day = String(date.getUTCDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function shouldExcludeFile(relPathPosix) {
  const base = path.posix.basename(relPathPosix);

  if (!base.endsWith('.html')) return { exclude: true, reason: 'not_html' };

  if (EXCLUDED_FILE_BASENAMES.has(base)) return { exclude: true, reason: 'excluded_basename' };

  if (base.startsWith('.')) return { exclude: true, reason: 'dotfile' };

  // Exclude backup/tmp artifacts by filename.
  if (base.includes('.backup.')) return { exclude: true, reason: 'backup_file' };
  if (base.endsWith('.tmp')) return { exclude: true, reason: 'tmp_file' };

  // Exclude template-ish HTML files by name (common in this repo).
  if (base.startsWith('template-') || base.startsWith('template_') || base === 'seo-template.html') {
    return { exclude: true, reason: 'template_file' };
  }
  if (base.includes('template') && base !== 'stripe-fees-calculator.html') {
    // Defensive: keep rare legitimate pages if needed; otherwise treat as template.
    return { exclude: true, reason: 'template_file' };
  }

  // Exclude files with spaces or obvious junk (keep consistent with existing generator).
  if (base.includes(' ') || base.includes('?')) return { exclude: true, reason: 'invalid_filename' };

  // Exclude known backup folders already covered by robots; keep sitemap clean too.
  const lower = relPathPosix.toLowerCase();
  if (lower.includes('/_backups/') || lower.includes('/_layout_backups/') || lower.includes('/_quarantine_backups/')) {
    return { exclude: true, reason: 'backup_dir' };
  }
  if (lower.includes('/backups/') || lower.includes('/backup_pages/') || lower.includes('/.sideguy-backups/')) {
    return { exclude: true, reason: 'backup_dir' };
  }
  if (lower.includes('/backups_') || lower.includes('/backup_') || lower.includes('/backup-') || lower.includes('/backups-')) {
    return { exclude: true, reason: 'backup_dir' };
  }

  // Exclude SEO reserve pages (often noindex or experiments).
  if (lower.startsWith('seo-reserve/') || lower.includes('/seo-reserve/')) {
    return { exclude: true, reason: 'seo_reserve' };
  }

  return { exclude: false };
}

async function walk(dirAbs, relDirPosix, collector) {
  const entries = await fs.promises.readdir(dirAbs, { withFileTypes: true });

  for (const entry of entries) {
    const entryAbs = path.join(dirAbs, entry.name);

    // Use POSIX paths for URLs and stable matching.
    const entryRelPosix = relDirPosix
      ? `${relDirPosix}/${entry.name}`
      : entry.name;

    if (entry.isDirectory()) {
      if (EXCLUDED_DIRS.has(entry.name)) {
        collector.excludedDirs[entry.name] = (collector.excludedDirs[entry.name] ?? 0) + 1;
        continue;
      }
      if (isBackupDirName(entry.name)) {
        collector.excludedDirs['backup_dir'] = (collector.excludedDirs['backup_dir'] ?? 0) + 1;
        continue;
      }
      if (entry.name.startsWith('.')) {
        collector.excludedDirs['dot_dir'] = (collector.excludedDirs['dot_dir'] ?? 0) + 1;
        continue;
      }
      // Exclude underscore dirs (tend to be internal/backups in this repo)
      if (entry.name.startsWith('_')) {
        collector.excludedDirs['underscore_dir'] = (collector.excludedDirs['underscore_dir'] ?? 0) + 1;
        continue;
      }
      await walk(entryAbs, entryRelPosix, collector);
      continue;
    }

    if (!entry.isFile()) continue;

    collector.totalFiles += 1;

    const decision = shouldExcludeFile(entryRelPosix);
    if (decision.exclude) {
      collector.excludedFiles[decision.reason] = (collector.excludedFiles[decision.reason] ?? 0) + 1;
      continue;
    }

    const stat = await fs.promises.stat(entryAbs);

    collector.included.push({
      relPathPosix: entryRelPosix,
      lastmod: isoDateFromStat(stat),
    });
  }
}

function buildSitemapXml(urlItems) {
  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  xml += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;
  for (const item of urlItems) {
    const loc = `${DOMAIN}/${item.relPathPosix}`;
    xml += `  <url><loc>${escapeXML(loc)}</loc><lastmod>${escapeXML(item.lastmod)}</lastmod></url>\n`;
  }
  xml += `</urlset>\n`;
  return xml;
}

function buildSitemapIndexXml(sitemapLocs) {
  const today = new Date();
  const year = today.getUTCFullYear();
  const month = String(today.getUTCMonth() + 1).padStart(2, '0');
  const day = String(today.getUTCDate()).padStart(2, '0');
  const lastmod = `${year}-${month}-${day}`;

  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  xml += `<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;
  for (const loc of sitemapLocs) {
    xml += `  <sitemap><loc>${escapeXML(loc)}</loc><lastmod>${escapeXML(lastmod)}</lastmod></sitemap>\n`;
  }
  xml += `</sitemapindex>\n`;
  return xml;
}

(async function main() {
  const collector = {
    totalFiles: 0,
    included: [],
    excludedFiles: {},
    excludedDirs: {},
  };

  await walk(ROOT, '', collector);

  collector.included.sort((a, b) => a.relPathPosix.localeCompare(b.relPathPosix));

  const totalIncluded = collector.included.length;
  const chunkCount = Math.max(1, Math.ceil(totalIncluded / MAX_URLS_PER_SITEMAP));

  const writtenSitemaps = [];

  for (let i = 0; i < chunkCount; i++) {
    const start = i * MAX_URLS_PER_SITEMAP;
    const end = Math.min(start + MAX_URLS_PER_SITEMAP, totalIncluded);
    const chunk = collector.included.slice(start, end);

    const filename = chunkCount === 1 ? 'sitemap-clean.xml' : `sitemap-clean-${i + 1}.xml`;
    const filePath = path.join(ROOT, filename);

    fs.writeFileSync(filePath, buildSitemapXml(chunk), 'utf8');
    writtenSitemaps.push(filename);
  }

  const sitemapLocs = writtenSitemaps.map((name) => `${DOMAIN}/${name}`);

  // Replace sitemap-index.xml to point ONLY at the clean sitemap(s).
  fs.writeFileSync(OUTPUT_INDEX, buildSitemapIndexXml(sitemapLocs), 'utf8');

  const stats = {
    domain: DOMAIN,
    generatedAtUtc: new Date().toISOString(),
    totals: {
      totalFilesScanned: collector.totalFiles,
      includedHtmlUrls: totalIncluded,
      sitemapFilesWritten: writtenSitemaps.length,
      maxUrlsPerSitemap: MAX_URLS_PER_SITEMAP,
    },
    included: {
      first10: collector.included.slice(0, 10).map((x) => x.relPathPosix),
      last10: collector.included.slice(-10).map((x) => x.relPathPosix),
    },
    excludedFilesByReason: Object.fromEntries(Object.entries(collector.excludedFiles).sort((a, b) => b[1] - a[1])),
    excludedDirsByReason: Object.fromEntries(Object.entries(collector.excludedDirs).sort((a, b) => b[1] - a[1])),
    outputs: {
      sitemapIndex: path.basename(OUTPUT_INDEX),
      sitemaps: writtenSitemaps,
      statsFile: path.basename(OUTPUT_STATS),
    },
  };

  fs.writeFileSync(OUTPUT_STATS, JSON.stringify(stats, null, 2) + '\n', 'utf8');

  console.log(`Clean sitemap generated.`);
  console.log(`Included URLs: ${totalIncluded}`);
  console.log(`Sitemap files: ${writtenSitemaps.join(', ')}`);
  console.log(`Stats written: ${path.basename(OUTPUT_STATS)}`);
})();
