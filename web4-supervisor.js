// ===============================================
// SIDEGUY CMS GPT — WEB4 SUPERVISOR · V1
// Master Orchestrator for Auto-Pages, Auto-Index,
// Auto-Links, Auto-SEO, and Auto-Expansion.
// Author: PJ + ChatGPT
// ===============================================

import { execSync } from "child_process";
import path from "path";
import fs from "fs";

// Utility: run a module safely
function run(name, cmd) {
  try {
    console.log(`\n🧠  Running: ${name}`);
    const out = execSync(cmd, { encoding: "utf8" });
    console.log(out);
  } catch (err) {
    console.error(`❌  ${name} failed`);
    console.error(err.message);
  }
}

// Resolve full paths
const root = process.cwd();
const file = p => path.join(root, p);

// Verify all required modules exist
const required = [
  "auto-builder.js",
  "auto-expander.js",
  "auto-indexer.js",
  "auto-linker.js",
  "seo/meta-engine.js",
  "seo/sitemap-generator.js",
  "seo/page-validator.js"
];

console.log("\n🔍 Checking required modules...\n");

required.forEach(r => {
  if (!fs.existsSync(file(r))) {
    console.error(`❌ Missing: ${r}`);
  } else {
    console.log(`✅ Found: ${r}`);
  }
});

// ===============================================
// RUN WEB 4.0 PIPELINE
// ===============================================

console.log("\n🚀 SIDEGUY WEB 4.0 — ACTIVATING\n");

run("Auto-Builder",     "node auto-builder.js");
run("Auto-Expander",    "node auto-expander.js");
run("Auto-Indexer",     "node auto-indexer.js");
run("Auto-Linker",      "node auto-linker.js");

// SEO Modules
run("Meta-Engine",      "node seo/meta-engine.js");
run("Page Validator",   "node seo/page-validator.js");
run("Sitemap Generator","node seo/sitemap-generator.js");

console.log("\n✨ WEB 4.0 PIPELINE COMPLETE ✨");
console.log("SideGuy CMS GPT is now self-building.\n");
