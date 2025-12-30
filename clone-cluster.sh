
#!/bin/bash

SERVICE=$1

CITY="San Diego"

CITY_SLUG="san-diego"



BASE="hvac"



FILES=(

  "who-do-i-call-for-${BASE}-${CITY_SLUG}.html"

  "${BASE}-repair-cost-options-${CITY_SLUG}.html"

  "${BASE}-emergency-or-can-it-wait-${CITY_SLUG}.html"

  "${BASE}-repair-${CITY_SLUG}-what-to-know.html"

  "${BASE}-fix-examples-${CITY_SLUG}.html"

)



for f in "${FILES[@]}"; do

  NEW=$(echo "$f" | sed "s/${BASE}/${SERVICE}/g")

  cp "$f" "$NEW"

  sed -i '' "s/${BASE}/${SERVICE}/g" "$NEW"

  sed -i '' "s/$(echo $BASE | tr a-z A-Z)/$(echo $SERVICE | tr a-z A-Z)/g" "$NEW"

done



echo "Cluster cloned for: $SERVICE"

