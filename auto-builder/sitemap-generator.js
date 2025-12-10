/**
 * SideGuy CMS GPT — Sitemap Generator v1
 * -----------------------------------------
 * Generates:
 *   /sitemap.xml
 *   /sitemaps/payments.xml
 *   /sitemaps/problems.xml
 *   /sitemaps/services.xml
 *   /sitemaps/ai.xml
 * 
 * Future versions:
 *   - Auto-ping Google
 *   - Auto-ping Bing
 *   - Solana-based notarization of sitemap hashes
 */

import fs from "fs";
import path from "path";

export function generateSitemaps(baseUrl = "https://sideguysolutions.com") {
  const pagesDir = path.join(process.cwd(), "pages");
  const categories = fs.readdirSync(pagesDir);

  let masterUrls = [];

  for (const category of categories) {
    const catDir = path.join(pagesDir, category);
    const files = fs.readdirSync(catDir)
      .filter(f => f.endsWith(".html"));

    const urls = files.map(f => `${baseUrl}/${category}/${f}`);
    masterUrls.push(...urls);

    const xml = urls.map(u => `<url><loc>${u}</loc></url>`).join("");

    fs.mkdirSync("sitemaps", { recursive: true });
    fs.writeFileSync(`sitemaps/${category}.xml`,
      `<?xml version="1.0" encoding="UTF-8"?>
       <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
         ${xml}
       </urlset>`
    );
  }

  const masterXml = masterUrls.map(u => `<url><loc>${u}</loc></url>`).join("");

  fs.writeFileSync("sitemap.xml",
    `<?xml version="1.0" encoding="UTF-8"?>
     <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
       ${masterXml}
     </urlset>`
  );

  console.log("✅ Sitemaps generated.");
}
