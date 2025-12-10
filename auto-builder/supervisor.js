/**
 * SideGuy CMS GPT — Supervisor Engine v1
 * --------------------------------------
 * The orchestrator. Watches everything.
 * Future versions will integrate AI that decides WHAT to build next.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { execSync } from "child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const manifestPath = path.join(__dirname, "seo-manifest.json");
const pagesDir = path.join(__dirname, "pages");
const suggestionsDir = path.join(__dirname, "suggestions");
const autoBuilder = "node auto-builder.cjs";
const autoExpander = "node auto-expander.js";

/**
 * Logs Supervisor actions.
 */
function log(msg) {
  const time = new Date().toLocaleString();
  console.log(`[Supervisor ${time}] ${msg}`);
}

/**
 * Scan keywords in pages → auto suggest new ones.
 */
function scanForNewKeywords() {
  log("Scanning repo for new SEO opportunities...");

  const files = fs.readdirSync(pagesDir);
  const keywords = new Set();

  files.forEach(f => {
    const content = fs.readFileSync(path.join(pagesDir, f), "utf8").toLowerCase();

    // Simple v1 keyword extraction
    const terms = content.match(/[a-z]{4,}/g) || [];
    terms.forEach(t => keywords.add(t));
  });

  // Save suggestion keywords
  const out = Array.from(keywords).slice(0, 200);
  fs.writeFileSync(path.join(suggestionsDir, "keywords.json"), JSON.stringify(out, null, 2));

  log(`Found ${out.length} keywords. Saved for AI expansion.`);
}

/**
 * Auto-update manifest if new slugs or categories appear.
 */
function refreshManifest() {
  log("Refreshing manifest...");

  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  const files = fs.readdirSync(pagesDir);

  files.forEach(f => {
    const slug = f.replace(".html", "");
    const exists = manifest.some(m => m.slug === slug);

    if (!exists) {
      manifest.push({
        slug,
        title: slug.replace(/-/g, " "),
        description: `Auto-generated page for ${slug}`,
        category: "auto"
      });
      log(`Added ${slug} to manifest.`);
    }
  });

  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
}

/**
 * MAIN LOOP — everything runs here:
 */
function run() {
  log("Supervisor Engine started.");

  // 1. Extract new keywords
  scanForNewKeywords();

  // 2. Refresh manifest
  refreshManifest();

  // 3. Run auto-builder
  log("Running auto-builder...");
  execSync(autoBuilder, { stdio: "inherit" });

  // 4. Run auto-expander
  log("Running auto-expander...");
  execSync(autoExpander, { stdio: "inherit" });

  log("Supervisor cycle complete.");
}

// Execute
run();
