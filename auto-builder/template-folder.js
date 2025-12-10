/**
 * SideGuy CMS GPT — Template Loader v1
 * -----------------------------------------
 * Allows:
 *   - Multiple templates
 *   - Versioning
 *   - Dynamic switching
 *   - Rebuilding the entire site instantly
 */

import fs from "fs";
import path from "path";

export function loadTemplate(templateName = "default") {
  const file = path.join(process.cwd(), "templates", `${templateName}.html`);

  if (!fs.existsSync(file)) {
    throw new Error(`❌ Template not found: ${file}`);
  }

  const html = fs.readFileSync(file, "utf-8");
  return html;
}
