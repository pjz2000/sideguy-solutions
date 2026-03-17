#!/bin/bash

read -p "Incoming message: " msg

echo "$msg" >> logs/responder/inbox.txt

echo "Saved to inbox."
