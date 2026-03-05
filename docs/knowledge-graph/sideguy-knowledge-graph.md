# SideGuy Knowledge Graph
Generated: 2026-03-05 17:15:52

## Goal
Build a structured topic graph — modeled on Wikipedia's internal linking density — that makes every SideGuy page a node in a navigable intelligence network.

---

## Node Types

| Type | Role | Count |
|------|------|-------|
| PILLAR | Top-level authority domain (trunk) | 10 |
| CLUSTER | Subtopic group within a pillar (branch) | 61 |
| LEAF | Specific problem or question page (leaf) | 18,417+ |

---

## Graph Structure

```
PILLAR (1)
 └── CLUSTER ×20–50 (branches)
      └── LEAF ×50–500 (specific pages)
```

---

## Linking Rules (enforced by authority-link-engine)

| Link direction | What it does |
|----------------|-------------|
| LEAF → CLUSTER | Passes authority up; creates topical grouping signal |
| LEAF → PILLAR | Passes authority to section homepage |
| CLUSTER → PILLAR | Reinforces pillar as authority hub |
| CLUSTER ↔ CLUSTER | Sideways authority within same pillar (builds topical depth) |
| PILLAR → ROOT | Ties everything back to SideGuy home |

---

## Node Index

Maintained in `data/pillar-leaf-map.json` (auto-regenerated from repo scan).

Current counts:
- ai-automation: 1,315 leaves
- local-operator-tech: 1,229 leaves
- payments: 326 leaves
- business-software: 255 leaves
- home-systems: 194 leaves
- crypto-web3: 54 leaves
- operator-tools: 41 leaves
- energy-ev: 24 leaves
- problem-intelligence: 22 leaves
- prediction-markets: 5 leaves
- _unmapped (orphan): 532 leaves

---

## Orphan Prevention
Any page with no pillar assignment gets the Intelligence Network block injected,
linking it into the top-level pillar structure. This ensures zero orphan pages.

---

## Knowledge Gravity Principle
Pages with more inbound links rank better.
The pyramid structure deliberately funnels link equity:
- All leaves point up to clusters + pillars (distributed equity upward)
- Pillar hubs receive the most inbound equity (highest authority nodes)
- Internal link density signals topical authority to Google
