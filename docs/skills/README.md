# SideGuy Claude Skills Library v1

Reusable skill documents + bash launchers for rapid, repo-aware upgrades.
Designed for CPU Claude terminal speed. Append-only doctrine.

---

## What This Is

Each skill captures a repeatable SideGuy workflow as:
1. A **doctrine doc** (`docs/skills/*.md`) — rules, patterns, gotchas, checklists
2. A **bash launcher** (`tools/skills/run-*.sh`) — automated execution with safety checks

New Claude sessions load a skill doc and execute the launcher. No re-derivation, no re-learning the rules.

---

## Skills

| Skill | Doctrine | Launcher | Purpose |
|---|---|---|---|
| GSC Reality Layer | `docs/skills/gsc-reality-layer.md` | `tools/skills/run-gsc-layer.sh` | Turn GSC exports into homepage cards, CTR title passes, crawl freshness |
| Hero WOW Upgrade | `docs/skills/hero-wow-upgrade.md` | `tools/skills/run-hero-wow.sh` | Safe premium hero upgrades — ocean aesthetic, animations, no black-box bug |
| Cluster Spawn | `docs/skills/cluster-spawn.md` | `tools/skills/run-cluster-spawn.sh` | Query signals → hub pages, cluster children, geo expansions |
| Meme Factory | `docs/skills/meme-factory.md` | *(manual — see doctrine)* | Operator trench stories → trust-building memes linked to service pages |

---

## Quick Start

```bash
# After a new GSC export:
bash tools/skills/run-gsc-layer.sh

# Before any hero edit:
bash tools/skills/run-hero-wow.sh

# To find new page opportunities:
bash tools/skills/run-cluster-spawn.sh
```

---

## Doctrine Principles

**Append-only:** Never edit existing CSS style blocks or committed files in-place without reading them first. Always add new named blocks.

**Read before edit:** Every edit to `index.html` requires a `grep` or `Read` to confirm the exact string before replacing. Pattern edits without reading cause duplicate insertions.

**Version every deploy:** Every `index.html` commit bumps the GSC layer version and timestamp so the operator can confirm CDN propagation.

**One commit per pass:** Bundle all changes from a single skill run into one commit with a clear `feat:` message describing what changed and why.

**Winners drive content:** Every page built or refreshed should trace back to a real GSC signal (impressions + position). Don't build speculatively — build where demand already exists.

---

## Adding a New Skill

1. Create `docs/skills/[skill-name].md` with: trigger conditions, step-by-step process, rules, checklist
2. Create `tools/skills/run-[skill-name].sh` with: safety checks, automated steps, commit template
3. Add a row to this README
4. Commit: `feat: add [skill-name] skill to Claude skills library`

---

## Related Tools

| Tool | Purpose |
|---|---|
| `tools/seo/page1-watchtower.sh` | Daily position tracking on near-page-1 URLs |
| `tools/seo/crawl-velocity-check.sh` | Freshness signals, sitemap lastmod, recrawl scoring |
| `tools/homepage-builder/update_trending_cards.py` | Rebuild homepage GSC trending section |
| `tools/repo-ingestion/spawn-page-ideas-from-top10.sh` | Repo → page idea bridge |
| `data/gsc-winners.json` | Living winner feed — source of truth for all GSC-driven work |

---

## Key Docs

| Doc | Purpose |
|---|---|
| `docs/reports/page1-watchtower.md` | Position history for near-page-1 URLs |
| `docs/reports/crawl-velocity.md` | Crawl signal log |
| `docs/client-wins-ledger.md` | Logged client wins with money/hours saved |
| `docs/inbound-lead-memory.md` | Lead triage pipeline |
| `docs/followup-doctrine.md` | 3-pathway follow-up system |
| `docs/digital-commercial-real-estate-mantra.md` | 2027 operating philosophy |
| `docs/sunrise-command-center-doctrine.md` | Brand/operating philosophy |
