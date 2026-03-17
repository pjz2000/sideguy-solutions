#!/bin/bash

FILE="logs/router/routed-leads.txt"

echo ""
echo "SideGuy Deal Value Estimator"
echo "----------------------------"

total=0

while read line
do

value=50

if echo "$line" | grep -q "HVAC"; then
value=500
fi

if echo "$line" | grep -q "ENERGY"; then
value=800
fi

if echo "$line" | grep -q "PAYMENTS"; then
value=300
fi

total=$((total + value))

done < "$FILE"

echo "Estimated value: $total USD"
