Claude,

Install and run the SideGuy Page Metadata Index.

Steps:

1. Run tools/index/run-index-system.sh
2. Verify docs/index/page-metadata.tsv exists
3. Confirm priority-report.txt and gravity output look correct

Rules:

- append-only
- do not modify existing pages
- only analyze metadata

Goal:

Prepare the infrastructure for scaling SideGuy to 1M pages.

