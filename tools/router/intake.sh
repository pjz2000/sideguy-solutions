#!/bin/bash

echo ""
echo "SideGuy Intake"

read -p "Problem: " problem

echo "---------------------------"

echo "Captured:"
echo "$problem"

echo ""

echo "$problem" >> logs/router/raw-leads.txt

echo "Saved to logs/router/raw-leads.txt"
