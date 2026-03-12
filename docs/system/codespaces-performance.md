# SideGuy Codespaces Performance Guide

SideGuy runs best when the editor does less work.

## Fast Mode

Run:

```bash
tools/system/sideguy_fast_mode.sh
```

This will:
- reduce git scanning
- clean stale dev processes
- reduce indexing load

## What the VS Code settings do

- Excludes `docs/reports/`, `docs/problem-radar/`, `archive/` from file watcher and search
- Disables git auto-refresh and auto-fetch
- Disables Python analysis indexing
- Disables minimap and smooth scrolling
- Turns off telemetry

## Philosophy

Large SEO repos trigger heavy file watching and indexing.
SideGuy scripts should do the work — not the editor.
