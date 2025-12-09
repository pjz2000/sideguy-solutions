// apply-universal-template.cjs
// Fill empty / stub HTML files with sideguy-universal-template.html

const fs = require("fs");
const path = require("path");

const TEMPLATE_FILE = path.join(__dirname, "sideguy-universal-template.html");

// files we NEVER want to overwrite
const EXCLUDE = new Set([
  "index.html",
  "index-backup.html",
  "index-test.html",
  "money-index.html",
  "page-index.html",
  "seo.html",
  "seo-page-template.html",
  "seo-template.html",
  "sideguy-header.html",
  "sideguy-footer.html",
  "sideguy-orb.html",
  "problem-template.html"
]);

// if a file is smaller than this, we treat it as "empty / stub"
const MIN_BYTES = 1500;

function slugToTitle(slug) {
  // remove extension
  const base = slug.replace(/\.html$/i, "");
  // pure slug like "ac-repair-san-diego"
  const cleaned = base
    .replace(/[-_]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  // basic title case
  return cleaned
    .split(" ")
    .map(word => {
      if (!word) return "";
      if (word.toLowerCase() === "and") return "and";
      if (word.toLowerCase() === "san") return "San";
      if (word.toLowerCase() === "diego") return "Diego";
      return word[0].toUpperCase() + word.slice(1).toLowerCase();
    })
    .join(" ");
}

(async () => {
  const template = await fs.promises.readFile(TEMPLATE_FILE, "utf8");

  const allFiles = (await fs.promises.readdir(__dirname))
    .filter(f => f.toLowerCase().endsWith(".html"));

  let updatedCount = 0;

  for (const file of allFiles) {
    if (EXCLUDE.has(file)) {
      console.log(`Skipping (excluded): ${file}`);
      continue;
    }

    const fullPath = path.join(__dirname, file);
    const stats = await fs.promises.stat(fullPath);

    // Only touch very small / obviously stubby files
    if (stats.size >= MIN_BYTES) {
      console.log(`Keeping existing content (size ${stats.size}): ${file}`);
      continue;
    }

    const pageTitle = slugToTitle(file);
    const filled = template.replace(/{{PAGE_TITLE}}/g, pageTitle);

    await fs.promises.writeFile(fullPath, filled, "utf8");
    updatedCount++;
    console.log(`Filled with universal template: ${file} → "${pageTitle}"`);
  }

  console.log(`\nDone. Updated ${updatedCount} file(s) with the universal template.`);
})();
