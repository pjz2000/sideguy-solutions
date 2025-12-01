// SideGuy Problem Engine · Auto Page Generator v1.0



import fs from 'fs';



// Load problem list

const problems = JSON.parse(fs.readFileSync('problems.json', 'utf8'));



// Load template

const template = fs.readFileSync('problem-template.html', 'utf8');



// Make output directory if needed

if (!fs.existsSync('problems')){

  fs.mkdirSync('problems');

}



problems.forEach(problem => {

  let page = template

    .replace('{{TITLE}}', problem.title)

    .replace('{{DESCRIPTION}}', problem.description)

    .replace('{{SOLUTION}}', problem.solution);



  fs.writeFileSync(`problems/${problem.slug}.html`, page);

  console.log(`✓ Generated: ${problem.slug}.html`);

});



console.log('All problem pages generated successfully!');

