#!/usr/bin/env bash

echo "SideGuy Internal Link Router"

for page in pages/*.html
do

grep -q "SideGuy knowledge network" "$page"

if [ $? -eq 0 ]; then
echo "OK $page"
fi

done

echo "Routing scan complete."
