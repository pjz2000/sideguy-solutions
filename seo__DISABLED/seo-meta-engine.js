/**
 * SideGuy CMS GPT · SEO Meta Engine v1
 * ------------------------------------
 * Generates:
 *  • <title>
 *  • <meta name="description">
 *  • Local SEO tags
 *  • JSON-LD schema (LocalBusiness, Service, FAQ when available)
 *  • Auto-injects into templates
 */

export function generateMeta(entry) {
  const title = entry.title || entry.slug.replace(/-/g, " ");
  const desc  = entry.description || `Solve ${title} fast in San Diego. SideGuy finds the real fix in seconds.`;

  const keywords = [
    title,
    "San Diego",
    entry.category,
    "SideGuy Solutions",
    "Instant Settlement",
    "Local Operator Help"
  ].filter(Boolean).join(", ");

  const schema = {
    "@context": "https://schema.org",
    "@type": "Service",
    "serviceType": title,
    "provider": {
      "@type": "Organization",
      "name": "SideGuy Solutions",
      "url": "https://sideguysolutions.com"
    },
    "areaServed": "San Diego",
    "description": desc
  };

  return {
    title,
    desc,
    keywords,
    schemaJson: JSON.stringify(schema, null, 2)
  };
}
