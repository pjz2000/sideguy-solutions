# SideGuy Autonomous Page Builder

Purpose:
Build page families safely at scale without dumping 100k files at once.

Workflow:
1. Build manifest
2. Split into queue batches
3. Build one batch at a time
4. Keep build ledger
5. Review / commit in controlled waves

Why this matters:
Large sites stay manageable when they separate:
- discovery
- manifests
- queues
- publishing
- upgrades

Core principle:
Batch-only, append-only, idempotent builds.
