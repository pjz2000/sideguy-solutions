#!/bin/bash

FILE="manifests/trends/emerging-tech.txt"

echo ""
echo "SideGuy Cluster Generator"
echo "-------------------------"

while read TOPIC
do
  echo "$TOPIC-explained"
  echo "future-of-$TOPIC"
  echo "how-$TOPIC-works"
  echo ""
done < "$FILE"
