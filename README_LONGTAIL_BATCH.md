Batch process notes — Long-tail pages

Batch 2 (#21–#30) completed and QA passed (meta/canonical/guardrail/FAQ/H1/lang).

Next steps:
- Run axe-core/jsdom scans in CI (node deps required in CI: jsdom, axe-core) and fix issues.
- Generate next batch (pages 31–40) using the priority list.
- Update sitemap and open draft PR for review once all batches are added or at a preferred checkpoint.

How to run axe scan locally:
1. npm install jsdom axe-core
2. node tools/axe-scan.js

If you want, I can open a draft PR now with current changes and QA notes, or continue with Batch 3.
