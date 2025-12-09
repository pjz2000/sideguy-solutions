const fs = require('fs');

const path = require('path');



const root = '.';



function getAllHTMLFiles(dir) {

  let results = [];

  const list = fs.readdirSync(dir);



  list.forEach(file => {

    const full = path.join(dir, file);

    const stat = fs.statSync(full);



    if (stat && stat.isDirectory()) {

      results = results.concat(getAllHTMLFiles(full));

    } else if (

      file.endsWith('.html') &&

      !file.includes('index.html') &&

      !file.includes('offline') &&

      !file.startsWith('.')

    ) {

      results.push(full.replace('./', ''));

    }

  });



  return results;

}



const pages = getAllHTMLFiles(root).sort();



fs.writeFileSync('page-list.json', JSON.stringify(pages, null, 2));



console.log(`Generated page-list.json with ${pages.length} pages.`);