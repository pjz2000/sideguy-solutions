# SideGuy Command Center — Canonical Directions

THIS FILE DEFINES HOW THE ENTIRE PROJECT OPERATES.

IT IS NOT A SCRIPT TO “RUN”.
IT IS A CONTRACT.

IF A FUTURE ACTION CONFLICTS WITH THIS FILE — THIS FILE WINS.

---

## ROLES

ChatGPT = Brain (decides WHAT)  
Cursor   = Hands (executes HOW)

Cursor performs ONE ATOMIC JOB AT A TIME.
No batching. No interpretation. No assumptions.

---

## CORE DOCTRINE (LOCKED)

- Append-only system
- Compounding archive
- Truth before traffic
- Clarity before cost

Nothing is rewritten.  
Nothing is reordered.  
Nothing is deleted.

---

## SOURCE OF TRUTH (ROOT OBJECT)

/ledger/LEDGER.md

This is the highest authority file in the repo.

It records:
- What changed
- Why it mattered
- What humans decided
- What is still unknown

Rules:
- Append only
- No edits
- No deletions
- No hindsight rewrites

---

## CONTENT DERIVATION ORDER (MANDATORY)

1. Ledger entry exists
2. SEO pages may be derived from ledger
3. Index & sitemap links may be appended

REVERSE ORDER IS NOT ALLOWED.

---

## SEO PAGE RULES

- All SEO pages are cloned from seo-template.html
- Each page is a NEW standalone HTML file
- Filename = exact long-tail keyword (hyphenated)

REQUIRED TITLE FORMAT:
<title>What Changed in the Last 12 Months with ___</title>

CONTENT CONSTRAINTS:
- State the change
- State consequences
- No selling
- No vendor defense
- Human help offered at the end

---

## INDEX RULES

index.html
- Append links only
- Never reorganize
- Never restyle

sitemap.xml
- Append URLs only
- Never delete

---

## AUTOMATION RULES

Scripts MAY:
- Create new files
- Append to index.html
- Append to sitemap.xml

Scripts MAY NOT:
- Delete files
- Overwrite files
- Modify existing content

Bash constraints:
- NO set -e
- NO explicit exit
- Fail visibly

---

## GIT RULES

- No auto-commits
- No rebasing
- No squashing

Commit messages must state EXACTLY what was added.

Example:
"Add 3 ledger-derived SEO pages for payments changes"

---

## DEFINITION OF DONE

A task is DONE only when:
- New files exist in source control
- New URLs are visible
- Nothing else changed

If output is not visible — work is not done.

---

## FAILURE MODE

If anything feels off:
- STOP
- Do NOT fix
- Do NOT optimize
- Report exactly what you see
- Wait for new instruction

---

## OPERATIONAL HELPERS (CLARITY)

Ledger → Page Rule:
- One ledger entry may produce many pages
- No page may exist without a ledger ancestor

Ledger → Page → Sitemap is a one-way flow.

If unsure:
- Add a ledger entry
- Do NOT generate pages yet

Pause is success.
