// auto-builder.cjs
const fs = require('fs');
const path = require('path');

const TEMPLATE_PATH = path.join(__dirname, 'seo-template.html');
const MANIFEST_PATH = path.join(__dirname, 'seo-manifest.json');
const OUTPUT_DIR = __dirname; // same folder as index, or change if you want /seo

function loadTemplate() {
  return fs.readFileSync(TEMPLATE_PATH, 'utf8');
}

function loadManifest() {
  const raw = fs.readFileSync(MANIFEST_PATH, 'utf8');
  return JSON.parse(raw);
}

function buildPageFromEntry(template, entry) {
  let html = template;

  const replacements = {
    '{{TITLE}}': entry.title,
    '{{META_DESCRIPTION}}': entry.metaDescription,
    '{{H1}}': entry.h1,
    '{{SUBHEAD}}': entry.subhead,
    '{{CITY_LABEL}}': entry.cityLabel || '',
    '{{INTRO_HTML}}': entry.introHtml || '',
    '{{BODY_HTML}}': entry.bodyHtml || ''
  };

  for (const [token, value] of Object.entries(replacements)) {
    html = html.split(token).join(value);
  }

  return html;
}

function main() {
  const template = loadTemplate();
  const manifest = loadManifest();

  manifest.forEach(entry => {
    if (!entry.slug) {
      console.warn('Skipping entry with no slug:', entry);
      return;
    }
    const filename = `${entry.slug}.html`;
    const outPath = path.join(OUTPUT_DIR, filename);
    const html = buildPageFromEntry(template, entry);

    fs.writeFileSync(outPath, html, 'utf8');
    console.log('✅ Built', filename);
  });

  console.log('\n🎯 Done. Pages generated from seo-manifest.json');
}

main();
