# SideGuy Production System

Purpose:

Deploy lattice pages in clean controlled batches.

Workflow:

1. Run intelligence stack
2. Build 500 pages
3. Update sitemap
4. Update discovery index
5. Run health checks
6. Commit batch

Command:

./tools/production/run-production-cycle.sh

This ensures SideGuy grows steadily and safely.
