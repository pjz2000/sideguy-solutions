// SideGuy CMS GPT · content-suggester.js · V1
// --------------------------------------------
// Scans /payments, /problems, /services, /local pages
// Suggests NEW pages based on patterns in existing slugs.
// Later versions will call GPT automatically.

import fs from "fs";
import path from "path";

const ROOT = process.cwd();

export function suggestContent() {
  const dirs = ["payments", "problems", "services", "local"];
  let suggestions = [];

  for (const dir of dirs) {
    const folder = path.join(ROOT, dir);
    if (!fs.existsSync(folder)) continue;

    const files = fs.readdirSync(folder);
    const slugs = files.map(f => f.replace(".html", ""));

    // Detect patterns
    const keywords = slugs.flatMap(s => s.split("-"));

    // Frequency table
    const freq = {};
    keywords.forEach(k => (freq[k] = (freq[k] || 0) + 1));

    // High-value keywords
    const top = Object.keys(freq)
      .filter(k => freq[k] > 3)
      .slice(0, 10);

    top.forEach(k => {
      suggestions.push({
        slug: `${k}-services-san-diego`,
        idea: `Pages related to: ${k}`,
        category: "services"
      });
    });
  }

  return suggestions;
}
