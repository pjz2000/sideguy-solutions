/**
 * SIDEGUY CMS GPT — Template Loader v1
 * Reads / loads the main SEO template for building pages.
 */

import fs from "fs";
import path from "path";

export function loadTemplate() {
  const file = path.join(process.cwd(), "seo-template.html");
  return fs.readFileSync(file, "utf8");
}

export function savePage(filepath, content) {
  const dir = path.dirname(filepath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(filepath, content);
}
