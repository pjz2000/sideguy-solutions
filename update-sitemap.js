const fs = require('fs');

const path = require('path');



const ROOT = '.';

const DOMAIN = 'https://sideguysolutions.com';



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

  xml += `  <url><loc>${escapeXML(`${DOMAIN}/${p}`)}</loc></url>\n`;

});



xml += `</urlset>`;



fs.writeFileSync('sitemap.xml', xml);



console.log(`Generated sitemap with ${pages.length} valid pages.`);