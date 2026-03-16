# SideGuy Page Factory

## Purpose
Generate starter pages at scale from a manifest.

## Command
bash tools/factory/page-factory.sh manifests/factory/cluster-ai-operators-1773703096.csv

## Inputs
CSV columns: page_type, slug, title, parent, category, intent

## Output
- HTML pages in pages/factory
- Log in logs/factory/cluster-ai-operators-1773703096-build.log
- Report in reports/factory/cluster-ai-operators-1773703096-report.md

## Workflow
1. Build from manifest
2. Upgrade strongest pages
3. Run publish gate
4. Link to hubs
5. Add only qualified pages to sitemap
