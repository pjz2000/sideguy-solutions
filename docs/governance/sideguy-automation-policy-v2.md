# SideGuy Automation Policy v2

Status: ACTIVE — March 2026

---

## Purpose

Allow intelligent automation while preventing thin-content spam and uncontrolled publishing.

SideGuy operates at 10k+ indexed pages. Automation is permitted in analysis, planning, and enhancement layers. Publishing authority remains human-controlled.

---

## Core Principle

Automation may assist creation.  
Automation may NOT control publishing.

Human approval is required for all live content.

---

## Allowed Automation

Automation may generate:

- Search opportunity reports
- Page-2 ranking opportunities
- Authority gravity reports
- Cluster planning documents
- Page briefs
- Draft pages (for human review)
- Page enhancement scripts (FAQ schema, calculators, comparison tables, structured data, internal links)
- Internal linking suggestions

Example output locations:

```
data/signals/
docs/intel-reports/
docs/authority-gravity/
docs/cluster-plans/
```

These outputs assist editorial decisions. They do not publish pages.

---

## Page Enhancement Automation

Automation may enhance **existing pages** by adding:

- FAQ schema (FAQPage JSON-LD)
- Comparison tables
- Interactive calculators
- Structured data (Article, LocalBusiness)
- Internal links to related pages

Enhancement scripts operate only on existing pages. No new pages are created.

---

## Cluster Planning

Automation may propose clusters and page briefs automatically. Example:

- AI receptionist (explainer)
- AI receptionist cost (cost page)
- AI receptionist vs human (comparison)
- AI receptionist for salons (local/industry page)

Cluster plans may be generated automatically. Pages must be reviewed before publication.

---

## Validation and Auditing

Automation may audit:

- Orphan pages
- Duplicate page structures
- Missing schema
- Internal linking gaps
- Page family violations

These tools produce reports only. No files are modified.

---

## Restricted Automation

### Auto Publishing

Automation may NOT:

- Auto-deploy pages
- Auto-merge content to main
- Auto-commit generated content without human review

### Bulk Template Page Generation

Automation may NOT generate pages using simple variable substitution:

```
# Prohibited pattern
{city} + {service}  →  "San Diego HVAC guide", "Phoenix HVAC guide", ...
```

These structures create thin programmatic content.

### Cron Content Engines

Scheduled automation may run **reports** but may NOT generate or publish content automatically.

---

## Approved Scaling Patterns

### Comparison Pages
Examples: `stripe-vs-square`, `zapier-vs-make`, `chatgpt-vs-claude`  
May include calculators, real fee tables, and San Diego business scenarios.

### Tool Pages
Pages containing calculators, workflows, or decision frameworks.

### Guide Clusters
Topic clusters where each page has unique explanations, not template fills.

---

## Page Families

Every page must belong to one family:

| Family | Purpose |
|---|---|
| guide | How-to, step-by-step |
| comparison | Side-by-side evaluation |
| tool | Calculator or decision aid |
| local | San Diego neighborhood/industry focus |
| explanation | What is X, why it matters |

Each family has required structural sections (see `docs/differentiation/page-family-doctrine.md`).

---

## Publishing Workflow

```
signal engine
    ↓
cluster planner
    ↓
page brief
    ↓
draft page
    ↓
human review  ← automation stops here
    ↓
publish
```

---

## Scaling Policy

| Stage | Pages | Approach |
|---|---|---|
| Early | 0–5k | Manual creation only |
| Growth | 5k–15k | Draft automation allowed |
| Authority | 15k–50k | Controlled programmatic pages |
| Scale | 50k+ | Partial automation with validation |

SideGuy currently operates in the **10k+ authority stage** — draft automation and enhancement scripts are permitted.

---

## Guiding Rule

> Automation must produce **better pages**, not simply more pages.
