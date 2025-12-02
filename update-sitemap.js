const fs = require('fs');

const path = require('path');



const ROOT = '.';

const DOMAIN = 'https://sideguysolutions.com';



function walk(dir) {

  let results = [];

  const list = fs.readdirSync(dir);



  list.forEach(file => {

    const full = path.join(dir, file);

    const stat = fs.statSync(full);



    if (stat && stat.isDirectory()) {

      results = results.concat(walk(full));

    } else {

      if (full.endsWith('.html') && !full.includes('404.html')) {

        results.push(full);

      }

    }

  });



  return results;

}



const pages = walk(ROOT);



const sitemap =

  `<?xml version="1.0" encoding="UTF-8"?>\n` +

  `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +

  pages

    .map(p => {

      const clean = p.replace('./', '');

      return `  <url><loc>${DOMAIN}/${clean}</loc></url>`;

    })

    .join('\n') +

  `\n</urlset>`;



fs.writeFileSync('sitemap.xml', sitemap);



console.log(`Generated sitemap with ${pages.length} pages!`);

