// auto-upgrade.js

// Uses template-tech-v305.html and template-realestate-v305.html

// to auto-wrap every HTML page with the right premium template.



const fs = require('fs');

const path = require('path');



const TECH_TEMPLATE_PATH = path.join(__dirname, 'templates', 'template-tech-v305.html');

const OP_TEMPLATE_PATH   = path.join(__dirname, 'templates', 'template-realestate-v305.html');



const techTemplate = fs.readFileSync(TECH_TEMPLATE_PATH, 'utf8');

const opTemplate   = fs.readFileSync(OP_TEMPLATE_PATH, 'utf8');



// Files we do NOT want to auto-wrap (homepage, 404, templates themselves)

const EXCLUDE_FILES = new Set(['index.html', '404.html']);



function extractBetween(str, start, end) {

  const s = str.indexOf(start);

  const e = str.indexOf(end);

  if (s === -1 || e === -1 || e <= s) return null;

  return str.slice(s + start.length, e);

}



// Very simple router: decide if a page is "tech" or "operator/real estate"

function isTechPage(filename) {

  const lower = filename.toLowerCase();

  const techKeywords = [

    'ai-','ml-','data-','cloud','saas','app','dev','developer','development',

    'software','api','automation','wallet','solana','crypto','payment',

    'processing','node','react','kubernetes','devops','vector','llm'

  ];

  return techKeywords.some(k => lower.includes(k));

}



function upgradeFile(filePath) {

  const fileName = path.basename(filePath);

  if (EXCLUDE_FILES.has(fileName)) return;



  let html = fs.readFileSync(filePath, 'utf8');



  // 1) Title

  let titleMatch = html.match(/<title>([\s\S]*?)<\/title>/i);

  let pageTitle = titleMatch ? titleMatch[1].trim() : fileName.replace('.html', '').replace(/-/g, ' ');



  // 2) Meta description

  let metaMatch = html.match(/<meta[^>]+name=["']description["'][^>]*content=["']([^"']*)["'][^>]*>/i);

  let metaDescription = metaMatch

    ? metaMatch[1].trim()

    : `SideGuy Solutions · Help with ${pageTitle} in San Diego. Text PJ for real operator help.`;



  // 3) Page content

  let content = null;



  // Prefer CONTENT_START/CONTENT_END markers if present

  const contentMarker = extractBetween(html, '<!--CONTENT_START-->', '<!--CONTENT_END-->');

  if (contentMarker) {

    content = contentMarker.trim();

  } else {

    // Fallback: everything inside <body>...</body>

    const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);

    content = bodyMatch ? bodyMatch[1].trim() : '<p>SideGuy will build more detail for this page soon.</p>';

  }



  // 4) Choose template

  const tpl = isTechPage(fileName) ? techTemplate : opTemplate;



  // 5) Fill template

  let newHtml = tpl

    .replace(/{{PAGE_TITLE}}/g, pageTitle)

    .replace(/{{META_DESCRIPTION}}/g, metaDescription)

    .replace('{{PAGE_CONTENT}}', content);



  // 6) Write back

  fs.writeFileSync(filePath, newHtml, 'utf8');

  console.log('Upgraded:', fileName);

}



function walk(dir) {

  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {

    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {

      if (['node_modules', '.git', 'templates'].includes(entry.name)) continue;

      walk(fullPath);

    } else if (entry.isFile() && entry.name.endsWith('.html')) {

      upgradeFile(fullPath);

    }

  }

}



console.log('Using templates:');

console.log('  Tech:     ', TECH_TEMPLATE_PATH);

console.log('  Operator: ', OP_TEMPLATE_PATH);

walk(__dirname);

console.log('✅ Done upgrading templates.');

