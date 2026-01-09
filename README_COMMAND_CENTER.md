
# Command Center Guardrails for Cursor

## Guardrail Workflow

Cursor may ONLY:
- create new files listed in the manifest
- append (not rewrite) index/sitemap files
- show the exact filenames created before stopping

This prevents invisible changes and ensures every action is visible in source control.

## Atomic Job Prompt (Paste This Into Cursor)

Create exactly 5 new HTML files using seo-template.html.

Filenames (create these exact files):

ai-automation-consultant-san-diego.html
payment-processing-consultant-san-diego.html
small-business-tech-help-san-diego.html
solana-payments-consultant-san-diego.html
operator-command-center-san-diego.html

Place them in the same directory as existing SEO pages.

After creating the files, STOP and list the filenames created.
Do not modify any other files.

## What To Do Next

- If you SEE the 5 files appear:
  - Commit immediately
  - You are officially unblocked
  - Next step: batch 20–50 URLs

- If you do NOT see files:
  - Stop instantly
  - Do not retry with variations
  - Tell your lead exactly what Cursor responded

## Command Center Rule (Pin This)

Cursor success = files created + visible in source control
No files → no progress → stop.

## Recommended Workflow

1. **Lock Guardrails**
   - Create or confirm existence of `README_COMMAND_CENTER.md` and `seo-manifest.json` in the repo root.
   - Add the guardrail rule above.

2. **Generate & Commit New URLs**
   - Use the atomic job prompt above.

3. **Batch Operations**
   - Use Cursor for repetitive, scoped tasks (clone templates, append links, update metadata).

4. **Optional**
   - Create a `CURSOR_JOBS/` folder for atomic task files.

5. **Command Center Rule**
   - Every Cursor action must result in visible file changes (commits).

## TL;DR — The Exact Order
- Lock Cursor guardrails
- Generate 5–10 new URLs
- Commit immediately
- Only then scale batches
