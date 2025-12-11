import fs from "fs";
import path from "path";

// Load the universal template
const template = fs.readFileSync("./template.html", "utf8");

// Load manifest
const manifest = JSON.parse(fs.readFileSync("./manifest.json", "utf8"));

manifest.forEach((page) => {
  const output = template
    .replace(/{{PAGE_TITLE}}/g, page.title)
    .replace(/{{META_DESCRIPTION}}/g, page.description)
    .replace(/{{SUBHEAD}}/g, page.subhead || "")
    .replace(/{{PAGE_CONTENT}}/g, page.content);

  const filename = `${page.filename}.html`;
  fs.writeFileSync(filename, output);
  console.log("Generated:", filename);
});

console.log("\n✔ Auto-builder finished.\n");
