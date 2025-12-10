// WEB4 SUPERVISOR · SideGuy CMS GPT

// The conductor that runs the whole pipeline in order.



import { execSync } from "child_process";

import path from "path";



const run = (label, cmd) => {

  console.log(`\n▶ ${label}...`);

  execSync(cmd, { stdio: "inherit" });

};



const root = path.resolve(process.cwd());



// PIPELINE SEQUENCE

run("Validating pages", "node page-validator.js");

run("Generating links", "node auto-linker.js");

run("Indexing pages", "node auto-indexer.js");

run("Auto expanding SEO", "node auto-expander.js");

run("Generating sitemap", "node sitemap-generator.js");



console.log("\n✨ WEB 4.0 PIPELINE COMPLETE ✨");

console.log("SideGuy CMS GPT is now self-building.\n");