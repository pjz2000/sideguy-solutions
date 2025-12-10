// SideGuy CMS GPT · loader.js · V1
// --------------------------------
// Loads manifest.json
// Loads template files
// Shared across auto-builder, expander, indexer, router.

import fs from "fs";
import path from "path";

export function loadManifest() {
  const file = path.join(process.cwd(), "seo-manifest.json");
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

export function loadTemplate() {
  const file = path.join(process.cwd(), "seo-template.html");
  return fs.readFileSync(file, "utf8");
}

export function savePage(filepath, content) {
  const dir = path.dirname(filepath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(filepath, content);
}
