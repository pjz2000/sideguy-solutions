# SideGuy Solutions — Refactoring Plan
**Date:** 2026-01-13  
**Issue:** Technical debt from mass-generated pages with 95% template duplication

---

## Critical Problems Identified

1. **10,296+ HTML files** with full template duplication
2. **Duplicate SEO metadata** across reserve pages (same titles, H1s, meta descriptions)
3. **1,300+ lines of template code** in every single page
4. **Unmaintainable at scale** — every CSS/JS change requires editing 10K+ files
5. **SEO penalty risk** — Google will see these as duplicate/thin content

---

## Phase 1: Template Extraction (Week 1)

### Goal: Separate template from content

**Create:**
- `/templates/base-layout.html` — Shared HTML structure
- `/templates/components/` — Reusable pieces (header, footer, nav, weather widget)
- `/content/` — Markdown or JSON files with page-specific content only

**Tools to use:**
- Static site generator (11ty, Hugo, or Astro)
- OR: Server-side includes (PHP/Node.js)
- OR: Build script that combines templates + content

**Action:**
```bash
# Extract one page as proof-of-concept
# Example: ai-vs-reality-energy-decisions.html
# Split into:
#   - /templates/base-layout.html (reusable)
#   - /content/ai-vs-reality-energy-decisions.md (unique content only)
```

---

## Phase 2: Fix SEO Metadata (Week 1)

### Goal: Make every page unique in Google's eyes

**Required for each page:**
- ✅ Unique `<title>` tag
- ✅ Unique `<h1>` tag
- ✅ Unique meta description
- ✅ Unique content (100+ words minimum)
- ✅ Internal linking between related pages

**Action:**
```bash
# Create metadata.json with unique values per page
{
  "ai-vs-reality-energy-decisions": {
    "title": "AI vs Reality: Energy Decisions in San Diego | SideGuy",
    "h1": "AI vs Reality — Why Local Energy Decisions Still Need Humans",
    "description": "AI is great at explaining options, but local energy decisions in San Diego require human context. Here's when to trust AI and when to call PJ."
  },
  "ai-clarity-vs-ai-confidence": {
    "title": "AI Clarity vs AI Confidence | When to Get a Second Opinion",
    "h1": "AI Confidence Doesn't Mean Clarity",
    "description": "AI sounds confident even when it's wrong. Learn when AI clarity breaks down for local San Diego decisions."
  }
}
```

---

## Phase 3: Content Consolidation (Week 2)

### Goal: Reduce bloat and focus on quality

**Decision framework:**
1. **Keep if:** Page has unique, substantial content (200+ words) AND serves a specific search intent
2. **Merge if:** Multiple pages cover the same topic with minor variations
3. **Delete if:** Page is 95% template with generic placeholder content

**Example consolidations:**
- Merge all "AI vs Reality" variants into 5-10 strong pages instead of 50 weak ones
- Group similar reserve pages under category indexes

---

## Phase 4: Build System (Week 2)

### Recommended approach: Static Site Generator (11ty)

**Why 11ty:**
- Simple to learn
- Works with Markdown, HTML, JSON
- Generates static HTML (fast, SEO-friendly)
- No build complexity

**Structure:**
```
/sideguy-solutions/
├── _templates/
│   ├── base.html
│   └── components/
├── content/
│   ├── ai-reality/
│   │   ├── energy-decisions.md
│   │   └── confidence-vs-clarity.md
│   └── seo-reserve/
│       └── build-nothing-yet/
├── _data/
│   └── metadata.json
└── package.json
```

**Build command:**
```bash
npm run build
# Generates /dist/ with final HTML files
```

---

## Phase 5: Migration Strategy (Week 3)

### Step-by-step:

1. **Backup everything** (git branch: `pre-refactor-backup`)
2. **Pick 10 pages** as pilot (e.g., all "AI vs Reality" pages)
3. **Extract templates** for those 10
4. **Write unique content** for each
5. **Test SEO metadata** (Google Search Console)
6. **Validate build** produces identical output
7. **Delete old files** once confirmed
8. **Repeat** for next 50 pages, then 100, etc.

---

## Emergency Quick Fix (If No Time for Full Refactor)

**Minimum viable fix (1-2 days):**

1. **Fix duplicate titles:**
   ```bash
   # Script to update <title> tags in bulk
   for file in ai-*.html; do
     sed -i 's/<title>Who Do I Call?/<title>'"$UNIQUE_TITLE"'/g' "$file"
   done
   ```

2. **Fix duplicate H1s:**
   - Add unique H1 content after template closes
   - Use HTML comments to mark custom content sections

3. **Add noindex to thin pages:**
   ```html
   <meta name="robots" content="noindex, follow">
   ```
   - Prevents Google from indexing duplicate/thin pages
   - Keeps them functional for internal use

---

## Success Metrics

**Before:**
- 10,296 HTML files
- ~95% template duplication
- Same title/H1 across hundreds of pages
- Unmaintainable

**After:**
- 1 base template
- 500-1,000 unique content pages (quality over quantity)
- Every page has unique SEO metadata
- CSS/JS updates = edit 1 file, rebuild all

---

## Timeline

| Phase | Duration | Priority |
|-------|----------|----------|
| Phase 1: Template Extraction | 3 days | Critical |
| Phase 2: Fix SEO Metadata | 2 days | Critical |
| Phase 3: Content Consolidation | 5 days | High |
| Phase 4: Build System Setup | 3 days | High |
| Phase 5: Migration | 7 days | Medium |

**Total:** ~3 weeks for complete refactor  
**Quick fix:** 2 days to address immediate SEO issues

---

## Next Steps

1. Decide: Full refactor OR emergency SEO fix?
2. If full refactor → Choose static site generator (recommend 11ty)
3. If emergency fix → Run bulk title/H1 update scripts
4. Start with 10-page pilot to validate approach
5. Monitor Google Search Console for indexing changes

---

## Questions to Answer

- [ ] Which pages actually get traffic? (Keep those, delete dead weight)
- [ ] Which reserve pages should stay hidden (noindex)?
- [ ] What's the priority: SEO or maintainability? (Both need fixing, but order matters)
- [ ] Do you want to build this yourself or bring in help?

---

**Bottom line:** You built a content factory but shipped it with every product. The ideas are strong; now let's make the execution match the vision.

Text PJ when ready to implement.
