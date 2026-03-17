#!/bin/bash

INPUT="logs/responder/classified.txt"

echo ""
echo "Escalation Check"
echo "----------------"

while read line
do

if echo "$line" | grep -Ei "expensive|urgent|asap|help" > /dev/null
then
echo "HIGH PRIORITY → escalate to PJ"
fi

done < "$INPUT"

echo ""
