const fs = require("fs");



const pages = fs

  .readFileSync("page-list.txt", "utf8")

  .split("\n")

  .map(l => l.trim())

  .filter(Boolean);



const now = new Date().toLocaleString();



const links = pages

  .map(p => `<li><a href="${p}">${p}</a></li>`)

  .join("\n");



const html = `<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>SideGuy Pages Index</title>

</head>

<body>

<h1>SideGuy Pages</h1>

<p>Generated: ${now}</p>

<ul>

${links}

</ul>

</body>

</html>

`;



fs.writeFileSync("index.html", html);



console.log("✅ index.html generated with", pages.length, "pages");

