from pathlib import Path
import math

ROOT = Path("/workspaces/sideguy-solutions")
DOCS = ROOT / "docs" / "autonomous-builder"
MANIFEST = DOCS / "manifests" / "master-manifest.tsv"
QUEUE_DIR = DOCS / "queues"

BATCH_SIZE = 500

lines = MANIFEST.read_text(encoding="utf-8").splitlines()
header = lines[0]
rows = lines[1:]

QUEUE_DIR.mkdir(parents=True, exist_ok=True)

for old in QUEUE_DIR.glob("batch-*.tsv"):
    old.unlink()

num_batches = math.ceil(len(rows) / BATCH_SIZE)

for i in range(num_batches):
    batch_rows = rows[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
    out = QUEUE_DIR / f"batch-{i+1:04d}.tsv"
    with open(out, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for row in batch_rows:
            f.write(row + "\n")

print(f"Created {num_batches} batch files in {QUEUE_DIR}")
