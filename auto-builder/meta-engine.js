/**
 * SideGuy CMS GPT — SEO Meta Engine v1
 * -----------------------------------------
 * Injects dynamic meta tags into generated pages.
 * 
 * Future:
 *   - GPT-driven meta optimization
 *   - Auto A/B testing
 *   - Local intent scoring
 */

export function applyMeta(html, entry) {
  const meta = `
    <meta name="description" content="${entry.description}">
    <meta property="og:title" content="${entry.title}">
    <meta property="og:description" content="${entry.description}">
    <meta name="keywords" content="${entry.keywords.join(", ")}">
    <meta property="og:url" content="https://sideguysolutions.com/${entry.category}/${entry.slug}.html">
  `;

  return html.replace("</head>", `${meta}\n</head>`);
}
