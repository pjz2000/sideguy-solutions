
#!/usr/bin/env bash



MANIFEST_FILE="$1"



if [[ -z "$MANIFEST_FILE" || ! -f "$MANIFEST_FILE" ]]; then

  echo "❌ Manifest missing or not found."

  exit 0

fi



OUTPUT_DIR="seo-pages"

mkdir -p "$OUTPUT_DIR"



TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

OUTFILE="$OUTPUT_DIR/page-$TIMESTAMP.html"



cat > "$OUTFILE" <<HTML

<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8" />

  <title>SideGuy Single Page</title>

</head>

<body>

  <h1>SideGuy Single Page</h1>

  <p>Generated at $TIMESTAMP</p>

</body>

</html>

HTML



echo "✅ Page generated:"

echo "📄 $OUTFILE"

echo "🛑 Hard stop enforced (1 page only)"

