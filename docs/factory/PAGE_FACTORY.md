# SideGuy Page Factory

Purpose:
Generate starter HTML pages at scale from CSV manifests.

Why this matters:
- safer than random mass page generation
- manifest-driven
- easy to review
- compatible with publish-gate workflows
- useful for reserve inventory and future cluster builds

Suggested doctrine:
- do not auto-sitemap everything
- do not auto-link everything
- build inventory first
- promote only the strongest pages
- strengthen hubs before exposing full clusters

Example:
bash tools/factory/page-factory.sh manifests/factory/page-factory-example.csv
