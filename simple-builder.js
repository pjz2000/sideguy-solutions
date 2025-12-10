import fs from "fs";



const pages = [

  "plumber-san-diego.html",

  "hvac-installation-san-diego.html",

  "san-diego-instant-settlement.html"

  // add more pages here

];



const template = (title) => `

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>${title} · SideGuy Solutions</title>

</head>

<body>

<h1>${title}</h1>

<p>Auto-generated SideGuy page.</p>

</body>

</html>

`;



pages.forEach((filename) => {

  const title = filename.replace(".html", "").replace(/-/g, " ");

  fs.writeFileSync(filename, template(title));

  console.log("Generated:", filename);

});