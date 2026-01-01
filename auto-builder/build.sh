
#!/usr/bin/env bash



ROOT="$(git rev-parse --show-toplevel)"

DATE="$(date '+%Y-%m-%d %H:%M %Z')"



while IFS='|' read -r TYPE SLUG TITLE DESC HUB; do



  case "$TYPE" in

    who) DIR="who-do-i-call" ;;

    decision) DIR="decision-engine" ;;

    city) DIR="cities" ;;

    vertical) DIR="verticals" ;;

    ppc) DIR="ppc" ;;

    *) continue ;;

  esac



  mkdir -p "$ROOT/$DIR"

  FILE="$ROOT/$DIR/$SLUG.html"



  if [ -f "$FILE" ]; then

    echo "↪︎ Skipped existing $FILE"

    continue

  fi



cat <<PAGE > "$FILE"

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<title>$TITLE · SideGuy Solutions</title>

<meta name="description" content="$DESC">

</head>

<body>



<h1>$TITLE</h1>



<p>SideGuy exists to reduce panic and unnecessary cost.</p>



<p>$DESC</p>



<a href="sms:17604541860&body=SideGuy%20Auto:%20$SLUG"

style="display:inline-block;padding:14px 18px;

background:#00c896;color:#003f2f;

border-radius:18px;text-decoration:none;

font-weight:700">

Text PJ

</a>



<p><strong>Updated:</strong> $DATE</p>



<p>

<a href="/$DIR/index.html">Back to hub</a> ·

<a href="/">Home</a>

</p>



</body>

</html>

PAGE



  echo "✅ Built $FILE"



done < auto-builder/manifest.txt



# -----------------------------------------

# REBUILD SITEMAP

# -----------------------------------------



FILES=$(find "$ROOT" -type f -name "*.html" | sed "s|$ROOT||" | sort)

COUNT=$(echo "$FILES" | wc -l | tr -d ' ')



cat <<EOF > "$ROOT/sitemap.html"

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<title>SideGuy Sitemap</title>

</head>

<body>

<h1>SideGuy Sitemap</h1>

<p>Total pages: <strong>$COUNT</strong></p>

<p>Updated: $DATE</p>

<ul>

