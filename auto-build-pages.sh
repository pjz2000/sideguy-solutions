
#!/usr/bin/env bash

set -u



INPUT="data/pages.txt"

OUT="site/pages"

mkdir -p "$OUT"



while read -r TITLE; do

  [ -z "$TITLE" ] && continue



  SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g' | tr ' ' '-')

  FILE="$OUT/$SLUG.html"



  cat <<PAGE > "$FILE"

<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <title>$TITLE | SideGuy Solutions</title>

  <meta name="description" content="$TITLE — real answers, real humans, SideGuy Solutions.">

</head>

<body>

  <h1>$TITLE</h1>

  <p>SideGuy Solutions exists for people searching for "$TITLE".</p>

  <p>No sales pitch. No fluff. Just clarity, options, and real help.</p>

  <p>Text PJ if you want to talk.</p>

</body>

</html>

PAGE



  echo "BUILT: $FILE"

done < "$INPUT"

