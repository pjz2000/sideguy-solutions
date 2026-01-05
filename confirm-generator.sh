
#!/usr/bin/env bash

# ============================================================

# SIDEGUY — SINGLE PAGE CLEAN GENERATOR (CANONICAL)

# ============================================================



MANIFEST_FILE="${1:-}"

OUTPUT_DIR="seo-confirm"

TIMESTAMP="$(date +%Y-%m-%d_%H-%M-%S)"

OUTPUT_FILE="$OUTPUT_DIR/confirm-$TIMESTAMP.html"



# Validate input

if [[ -z "$MANIFEST_FILE" || ! -f "$MANIFEST_FILE" ]]; then

  echo "❌ Manifest missing or not found."

  exit 0

fi



mkdir -p "$OUTPUT_DIR"



# Write exactly ONE page

cat > "$OUTPUT_FILE" <<HTML

<!DOCTYPE html>

<html>

<head>

  <title>SideGuy Single Page</title>

</head>

<body>

  <h1>SideGuy Page Generated</h1>

  <p>Manifest: $MANIFEST_FILE</p>

  <p>Generated: $TIMESTAMP</p>

</body>

</html>

HTML



# Clean confirmation only

echo "✅ SideGuy generator complete"

echo "📄 File written: $OUTPUT_FILE"

echo "🛑 Hard stop enforced (1 page only)"



