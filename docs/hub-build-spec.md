# SideGuy Hub Build Specification
# Source: GPT instructions — added to worksheet 2026-02-23

# ============================================================
# SIDEGUY HUB BUILD — MASTER SPEC
# ============================================================

# OBJECTIVE:
# Build ONE hub page per cluster.
# Each hub becomes the master entry point for that vertical.
#
# COMPLETED HUBS:
#   ✅ hvac-problems-hub-san-diego.html
#   ✅ plumbing-problems-hub-san-diego.html
#   ✅ payment-processing-hub-san-diego.html
#   ✅ ai-automation-san-diego-hub.html
#   ✅ home-repair-hub-san-diego.html
#   ✅ electrical-problems-hub-san-diego.html
#   ✅ roofing-hub-san-diego.html
#   ✅ contractor-services-hub-san-diego.html
#   ✅ software-development-hub-san-diego.html
#   ✅ seo-hub-san-diego.html
#   ✅ solar-hub-san-diego.html

# ============================================================
# STRUCTURE REQUIREMENTS (ALL HUBS)
# ============================================================

# Mirror HVAC hub page as structural template.
# Match:
#   - Layout (CSS classes, container structure, section spacing)
#   - .wrap > h1 > .lede > .section > .grid > .card pattern
#   - Link formatting within .card elements
#   - CTA block (gradient, Text PJ orb)
#   - Footer strip

# DO NOT invent new layout patterns.
# DO NOT use external CSS.
# DO NOT link to external frameworks.

# ============================================================
# REQUIRED PAGE STRUCTURE (EACH HUB)
# ============================================================

# A. <title>:
#    "[Vertical] San Diego — Complete Guide · SideGuy"

# B. <meta description>:
#    ~150 chars, problem-first, no hype, actionable

# C. <link rel="canonical">:
#    Self-referencing, full URL

# D. H1:
#    "[Vertical] in San Diego"

# E. .lede (intro):
#    1–2 sentences. Clear scope. Calm, human-first tone.

# F. Warning block (if urgent vertical — electrical, roofing, plumbing):
#    Yellow/amber banner. Direct. Phone link.

# G. Sections (4–6 per hub):
#    - Break cluster into logical subgroups
#    - 4 cards per section preferred (max 6)
#    - Each card: link + 1 sentence description
#    - Descriptions written for a stressed non-expert

# H. CTA block (mid-page):
#    - Gradient mint→blue
#    - "Text 773-544-1231"
#    - Calm, no sales language

# I. FAQPage schema (JSON-LD):
#    - 3 Q&A pairs
#    - Real questions people search
#    - Honest, specific answers

# J. Footer strip:
#    - SideGuy Solutions · San Diego · Text link

# ============================================================
# INTERNAL LINKING RULES
# ============================================================
# - Prioritize highest-intent slugs
# - No raw dumps of all cluster pages
# - Curated, grouped links only
# - Max 20 links per section
# - Total links per hub: under 80
# - Alphabetized within sections

# ============================================================
# BREADCRUMB BACK-LINKS (child pages → hub)
# ============================================================
# After hub is created:
# - Add "← Back to [Vertical] Hub" breadcrumb to top of
#   key child pages in the cluster.
# - Style: small, muted, plain <a> tag near top of <body>
# - DO NOT add to every child — curate top 10–20 per cluster.

# ============================================================
# CONSTRAINTS
# ============================================================
# - No deleting files
# - No modifying other hubs (unless adding cross-links)
# - No changing global CSS
# - No extracting CSS to external files
# - Each hub is self-contained with inline styles
# - Pages live at root level (not /docs/pages/)

# ============================================================
# COMMIT FORMAT
# ============================================================
# "Add: [vertical]-hub-san-diego.html — [N] cluster pages covered"

# ============================================================
# REMAINING CLUSTERS (as of 2026-02-23)
# ============================================================
# SEO     — 33 pages  → seo-hub-san-diego.html
# Solar   — 25 pages  → solar-hub-san-diego.html
