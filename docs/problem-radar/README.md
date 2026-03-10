# SideGuy Problem Radar

This system logs emerging problems detected across the internet.

Sources may include:

- Google autocomplete
- Reddit discussions
- Twitter/X tech chatter
- AI tool launches
- Payment industry changes
- Small business automation trends

Each signal recorded contains:

- `source` — where the signal came from
- `topic` — the problem/query observed
- `timestamp` — UTC ISO timestamp

These signals can later be turned into:

- SEO pages
- Problem clusters
- SideGuy solution hubs

## Usage

Run from the repo root:

```bash
python tools/problem-radar/problem_radar.py
```

Output appends to `docs/problem-radar/radar-signals.tsv`.
