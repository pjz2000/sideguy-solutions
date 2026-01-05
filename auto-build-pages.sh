
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

  <title>$TITLE | SideGuy</title>

  <meta name="description" content="$TITLE — real help, real humans, SideGuy Solutions.">

</head>

<body>

  <h1>$TITLE</h1>



  <p>

    SideGuy Solutions helps people searching for "$TITLE"

    get clarity, options, and real-world answers.

  </p>



  <p>

    This page exists because Google users are asking real questions.

    If you're here, you're in the right place.

  </p>



  <p>

    Text PJ for help. No pressure. No sales pitch.

  </p>

</body>

</html>

PAGE



  echo "BUILT: $FILE"

done < "$INPUT"

