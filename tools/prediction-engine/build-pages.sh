#!/usr/bin/env bash

cd /workspaces/sideguy-solutions || exit 0

INPUT="manifests/prediction-engine/prediction-pages.json"
OUTPUT_DIR="public/prediction"

mkdir -p "$OUTPUT_DIR"

echo "Building prediction pages..."

jq -c '.[]' "$INPUT" | while read -r page; do

  slug=$(echo "$page" | jq -r '.slug')
  title=$(echo "$page" | jq -r '.title')
  intent=$(echo "$page" | jq -r '.intent')

  file="$OUTPUT_DIR/$slug.html"

  cat > "$file" <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>$title | SideGuy</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="$intent">
</head>
<body style="font-family: Arial; max-width: 800px; margin: auto; padding: 20px;">

<h1>$title</h1>

<p><strong>Predicted Intent:</strong> $intent</p>

<p>
This page exists because SideGuy predicts that someone will need this answer.
</p>

<h2>What You Need to Know</h2>
<p>
AI, search, and real-world problems are converging into prediction systems.
This page is part of that system.
</p>

<h2>Real Answer</h2>
<p>
We break down the problem clearly, without fluff, and help you make a real decision.
</p>

<h2>Get Help</h2>
<p>
Text PJ for real-world help: <strong>773-544-1231</strong>
</p>

<p><a href="/">← Back to Home</a></p>

</body>
</html>
HTML

  echo "Built: $file"

done

echo "Done."
