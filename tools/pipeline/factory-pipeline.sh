#!/bin/bash

echo "Running SideGuy Factory Pipeline"

echo ""
echo "Step 1: Strengthening pages"
bash tools/factory/strengthen-pages.sh

echo ""
echo "Step 2: Injecting internal links"
bash tools/link-engine/auto-link-injector.sh

echo ""
echo "Step 3: Authority flow update"
bash tools/gravity/authority-flow.sh

echo ""
echo "Step 4: Promoting qualified pages"
bash tools/factory/promote-pages.sh

echo ""
echo "Pipeline complete"
